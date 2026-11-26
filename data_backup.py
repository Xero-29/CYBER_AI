#!/usr/bin/env python3
"""Backup/verificación/restauración de datos locales con snapshots SQLite y hashes."""
import argparse
import hashlib
import hmac
import json
import math
import os
import re
import shutil
import sqlite3
import stat
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from private_sqlite import connect_private_sqlite
from safe_io import SafeWriteError
from secret_redaction import redact_sensitive_data, redact_text

PROJECT = Path(__file__).resolve().parent
DEFAULT_DATA = PROJECT / "data"
LOCK_SUFFIXES = {".lock", ".pid", ".sock", "-wal", "-shm"}
SCHEMA = "cyber-ai-data-backup-v1"
MAX_BACKUP_FILES = 50_000
MAX_MANIFEST_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_DEPTH = 64


class BackupError(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BackupError("El manifiesto contiene claves JSON duplicadas.")
        result[key] = value
    return result


def _reject_manifest_constant(value):
    raise BackupError("El manifiesto contiene una constante JSON no estándar.")


def _parse_manifest_float(value):
    parsed = float(value)
    if not math.isfinite(parsed):
        raise BackupError("El manifiesto contiene un número no finito.")
    mantissa = value.lower().split("e", 1)[0]
    if parsed == 0.0 and any(digit in "123456789" for digit in mantissa):
        raise BackupError("El manifiesto contiene un número subdesbordado.")
    return parsed


def _strict_manifest_json(text):
    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_manifest_constant,
        parse_float=_parse_manifest_float,
    )


def _enforce_manifest_json_depth(text):
    """Reject excessive JSON nesting before the recursive stdlib decoder runs."""
    depth = 0
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if depth > MAX_MANIFEST_DEPTH:
                raise BackupError("El manifiesto supera la profundidad JSON permitida.")
        elif character in "]}":
            depth -= 1


def _is_regular_file_info(info):
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return (
        stat.S_ISREG(info.st_mode)
        and not (getattr(info, "st_file_attributes", 0) & reparse_flag)
    )


def _file_state(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        getattr(info, "st_ctime_ns", 0),
        info.st_mode,
        info.st_nlink,
    )


def _is_directory_info(info):
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return (
        stat.S_ISDIR(info.st_mode)
        and not (getattr(info, "st_file_attributes", 0) & reparse_flag)
    )


def _validate_directory_path(path):
    """Reject symlink/reparse ancestors and directories writable by untrusted users."""
    candidate = Path(os.path.abspath(os.fspath(path)))
    chain = []
    for directory in (*reversed(candidate.parents), candidate):
        try:
            info = directory.lstat()
        except (OSError, ValueError) as error:
            raise BackupError("La ruta de directorios del backup no está disponible.") from error
        if not _is_directory_info(info):
            raise BackupError("No se permiten symlinks, puntos de reanálisis ni archivos en la ruta del backup.")
        if os.name == "posix":
            mode = stat.S_IMODE(info.st_mode)
            trusted_owner = info.st_uid in {0, os.geteuid()}
            root_sticky = info.st_uid == 0 and bool(info.st_mode & stat.S_ISVTX)
            if not trusted_owner or (mode & 0o022 and not root_sticky):
                raise BackupError("Los directorios del backup deben pertenecer a root/usuario y no ser modificables por terceros.")
        chain.append((directory, info.st_dev, info.st_ino))
    return chain


def _same_directory_chain(before, after):
    return (
        len(before) == len(after)
        and all(
            old_path == new_path and (old_dev, old_ino) == (new_dev, new_ino)
            for (old_path, old_dev, old_ino), (new_path, new_dev, new_ino)
            in zip(before, after)
        )
    )


def _ensure_directory_path(path):
    """Create missing private path components only after validating their ancestors."""
    candidate = Path(os.path.abspath(os.fspath(path)))
    missing = []
    current = candidate
    while True:
        try:
            current.lstat()
            break
        except FileNotFoundError:
            missing.append(current)
            current = current.parent
        except (OSError, ValueError) as error:
            raise BackupError("No se pudo inspeccionar el directorio del backup.") from error
    _validate_directory_path(current)
    for directory in reversed(missing):
        try:
            directory.mkdir(mode=0o700)
        except FileExistsError:
            pass
        _validate_directory_path(directory)
    return _validate_directory_path(candidate)


def _open_regular_file(path):
    """Open one regular file without following links in its path or hard links."""
    path = Path(os.path.abspath(os.fspath(path)))
    parent_chain_before = _validate_directory_path(path.parent)
    descriptor = None
    try:
        before = path.lstat()
        if not _is_regular_file_info(before):
            raise BackupError("El archivo del backup debe ser regular y no puede ser un enlace.")
        flags = (
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        after = path.lstat()
        parent_chain_after = _validate_directory_path(path.parent)
        if (
            not _is_regular_file_info(opened)
            or not _is_regular_file_info(after)
            or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
            or (opened.st_dev, opened.st_ino) != (after.st_dev, after.st_ino)
            or not _same_directory_chain(parent_chain_before, parent_chain_after)
        ):
            raise BackupError("El archivo cambió durante su apertura o no es regular.")
        if os.name == "posix" and opened.st_nlink != 1:
            raise BackupError("No se permiten enlaces duros en archivos del backup.")
        stream = os.fdopen(descriptor, "rb")
        descriptor = None
        return stream
    except BackupError:
        raise
    except OSError as error:
        raise BackupError("No se pudo abrir un archivo regular del backup.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _assert_open_file_stable(path, stream, initial):
    try:
        final = os.fstat(stream.fileno())
        current = Path(path).lstat()
    except OSError as error:
        raise BackupError("El archivo desapareció durante su lectura.") from error
    if (
        not _is_regular_file_info(final)
        or not _is_regular_file_info(current)
        or _file_state(initial) != _file_state(final)
        or (final.st_dev, final.st_ino) != (current.st_dev, current.st_ino)
    ):
        raise BackupError("El archivo cambió durante su lectura.")


def _read_regular_file(path, *, max_bytes):
    with _open_regular_file(path) as stream:
        initial = os.fstat(stream.fileno())
        if initial.st_size > max_bytes:
            raise BackupError("El manifiesto del backup supera 16 MiB.")
        chunks = []
        total = 0
        while True:
            chunk = stream.read(min(8192, max_bytes + 1 - total))
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise BackupError("El manifiesto del backup supera 16 MiB.")
            chunks.append(chunk)
        _assert_open_file_stable(path, stream, initial)
        if total != initial.st_size:
            raise BackupError("El archivo cambió de tamaño durante su lectura.")
        return b"".join(chunks)


def _sha256(path):
    digest = hashlib.sha256()
    with _open_regular_file(path) as stream:
        initial = os.fstat(stream.fileno())
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
        _assert_open_file_stable(path, stream, initial)
    return digest.hexdigest()


def _copy_regular_file(source, destination):
    """Copy a regular source without following links or overwriting a destination."""
    destination = Path(os.path.abspath(os.fspath(destination)))
    destination_parent_chain = _validate_directory_path(destination.parent)
    with _open_regular_file(source) as src:
        initial = os.fstat(src.fileno())
        flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0)
        )
        descriptor = None
        try:
            descriptor = os.open(destination, flags, 0o600)
            with os.fdopen(descriptor, "wb") as dst:
                descriptor = None
                opened_destination = os.fstat(dst.fileno())
                if not _is_regular_file_info(opened_destination):
                    raise BackupError("El destino de copia debe ser un archivo regular.")
                shutil.copyfileobj(src, dst, length=1024 * 1024)
                dst.flush()
                os.fsync(dst.fileno())
                final_destination = os.fstat(dst.fileno())
                if (
                    not _is_regular_file_info(final_destination)
                    or (opened_destination.st_dev, opened_destination.st_ino)
                    != (final_destination.st_dev, final_destination.st_ino)
                    or (
                        os.name == "posix"
                        and (opened_destination.st_nlink != 1 or final_destination.st_nlink != 1)
                    )
                ):
                    raise BackupError("El destino cambió durante la copia.")
        except OSError as error:
            raise BackupError("No se pudo copiar un archivo regular del backup.") from error
        finally:
            if descriptor is not None:
                os.close(descriptor)
        _assert_open_file_stable(source, src, initial)
        destination_after = destination.lstat()
        parent_chain_after = _validate_directory_path(destination.parent)
        if (
            not _is_regular_file_info(destination_after)
            or (opened_destination.st_dev, opened_destination.st_ino)
            != (destination_after.st_dev, destination_after.st_ino)
            or not _same_directory_chain(destination_parent_chain, parent_chain_after)
        ):
            raise BackupError("El destino o su ruta cambió durante la copia.")


def _backup_signing_key():
    value = os.environ.get("CYBER_AI_BACKUP_HMAC_KEY", "")
    if not value:
        return None
    key = value.encode("utf-8")
    if len(key) < 32:
        raise BackupError("CYBER_AI_BACKUP_HMAC_KEY debe tener al menos 32 bytes.")
    return key


def _manifest_payload(manifest):
    unsigned = {key: value for key, value in manifest.items() if key != "signature"}
    return json.dumps(
        unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _manifest_signature(manifest, key):
    return hmac.new(key, _manifest_payload(manifest), hashlib.sha256).hexdigest()


def _safe_relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise BackupError(f"Ruta insegura en manifiesto: {value!r}")
    rel = PurePosixPath(value)
    if (
        rel.is_absolute() or not rel.parts or ".." in rel.parts
        or value != rel.as_posix() or rel.parts[0].endswith(":")
        or rel.as_posix() == "manifest.json"
    ):
        raise BackupError(f"Ruta insegura en manifiesto: {value!r}")
    return rel


def _validate_manifest(snapshot, manifest, *, require_signature=False):
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise BackupError("Esquema de backup desconocido.")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise BackupError("Lista de archivos del manifiesto inválida.")
    if len(files) > MAX_BACKUP_FILES:
        raise BackupError("El manifiesto supera el límite de archivos del backup.")
    if manifest.get("encrypted") is not False:
        raise BackupError("Metadato de cifrado inválido o no compatible.")
    if manifest.get("requires_quiesced_writers") is not True:
        raise BackupError("El manifiesto no acredita escritores detenidos.")
    seen = set()
    expected = {"manifest.json"}
    verified = []
    for item in files:
        if not isinstance(item, dict):
            raise BackupError("Entrada de manifiesto inválida.")
        relative = _safe_relative(item.get("path"))
        key = relative.as_posix()
        if key in seen:
            raise BackupError("Ruta duplicada en manifiesto.")
        seen.add(key)
        if (
            isinstance(item.get("size"), bool)
            or not isinstance(item.get("size"), int)
            or item["size"] < 0
        ):
            raise BackupError(f"Tamaño inválido en manifiesto: {key}")
        digest = item.get("sha256")
        if (
            not isinstance(digest, str) or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
        ):
            raise BackupError(f"SHA-256 inválido en manifiesto: {key}")
        if item.get("kind") not in {"sqlite_snapshot", "file_copy_quiesced"}:
            raise BackupError(f"Tipo de archivo no permitido: {key}")
        for parent in relative.parents:
            if parent.as_posix() != "." and parent.as_posix() in seen:
                raise BackupError("Conflicto entre archivo y directorio en manifiesto.")
        if any(existing.startswith(key + "/") for existing in seen):
            raise BackupError("Conflicto entre archivo y directorio en manifiesto.")
        path = snapshot.joinpath(*relative.parts)
        cursor = snapshot
        for index, part in enumerate(relative.parts):
            cursor = cursor / part
            try:
                info = cursor.lstat()
            except OSError as error:
                raise BackupError(f"Falta archivo o directorio del backup: {key}") from error
            if index < len(relative.parts) - 1:
                if not _is_directory_info(info):
                    raise BackupError(f"Hay un directorio no seguro en el backup: {key}")
            elif not _is_regular_file_info(info):
                raise BackupError(f"El archivo del backup no es regular: {key}")
        try:
            path.resolve().relative_to(snapshot)
        except ValueError as error:
            raise BackupError(f"Ruta fuera del backup: {key}") from error
        if path.stat().st_size != item["size"] or _sha256(path) != digest:
            raise BackupError(f"Integridad no válida: {key}")
        expected.add(key)
        verified.append(key)

    actual = set()
    for current, dirs, names in os.walk(snapshot, followlinks=False):
        current_path = Path(current)
        for name in dirs:
            try:
                info = (current_path / name).lstat()
            except OSError as error:
                raise BackupError("No se pudo inspeccionar un directorio del backup.") from error
            if not _is_directory_info(info):
                raise BackupError("No se permiten symlinks ni puntos de reanálisis en el backup.")
        for name in names:
            path = current_path / name
            try:
                info = path.lstat()
            except OSError as error:
                raise BackupError("No se pudo inspeccionar un archivo del backup.") from error
            if not _is_regular_file_info(info):
                raise BackupError("El backup solo puede contener archivos regulares.")
            actual.add(path.relative_to(snapshot).as_posix())
    if actual != expected:
        raise BackupError("El contenido del backup no coincide con el manifiesto.")

    signature = manifest.get("signature")
    signed = signature is not None
    if not signed and require_signature:
        raise BackupError("El backup no tiene firma y se exigió --require-signature.")
    if signed:
        if (
            not isinstance(signature, dict)
            or set(signature) != {"algorithm", "value"}
            or signature.get("algorithm") != "HMAC-SHA256"
            or not isinstance(signature.get("value"), str)
            or not re.fullmatch(r"[a-f0-9]{64}", signature["value"])
        ):
            raise BackupError("Firma del manifiesto inválida.")
        key = _backup_signing_key()
        if key is None:
            raise BackupError("El backup está firmado pero falta CYBER_AI_BACKUP_HMAC_KEY.")
        expected_signature = _manifest_signature(manifest, key)
        if not hmac.compare_digest(expected_signature, signature["value"]):
            raise BackupError("La firma HMAC del manifiesto no coincide.")

    return {"valid": True, "files": len(verified), "paths": verified,
            "encrypted": False, "signed": signed}


def _sqlite_snapshot(source, destination):
    source = Path(source)
    parent_chain = _validate_directory_path(source.parent)
    try:
        initial = source.lstat()
    except OSError as error:
        raise BackupError("La base SQLite de origen no está disponible.") from error
    if not _is_regular_file_info(initial):
        raise BackupError("La base SQLite de origen debe ser un archivo regular.")
    if os.name == "posix" and initial.st_nlink != 1:
        raise BackupError("No se permiten enlaces duros en bases SQLite de origen.")

    source_connection = None
    destination_connection = None
    try:
        source_connection = sqlite3.connect(
            source.as_uri() + "?mode=ro", uri=True, timeout=30
        )
        opened = source.lstat()
        if (
            not _is_regular_file_info(opened)
            or (initial.st_dev, initial.st_ino) != (opened.st_dev, opened.st_ino)
            or not _same_directory_chain(parent_chain, _validate_directory_path(source.parent))
        ):
            raise BackupError("La base SQLite cambió durante su apertura.")
        source_connection.execute("PRAGMA trusted_schema=OFF")

        destination_connection = connect_private_sqlite(destination, timeout=30)
        source_connection.backup(destination_connection)
        result = destination_connection.execute("PRAGMA integrity_check").fetchone()[0]
        final = source.lstat()
        if (
            result != "ok"
            or _file_state(initial) != _file_state(final)
            or not _same_directory_chain(parent_chain, _validate_directory_path(source.parent))
        ):
            raise BackupError(f"SQLite integrity o estabilidad falló para {source.name}.")
    except (sqlite3.Error, SafeWriteError) as error:
        raise BackupError(f"No se pudo crear el snapshot SQLite de {source.name}.") from error
    finally:
        if destination_connection is not None:
            destination_connection.close()
        if source_connection is not None:
            source_connection.close()


def create_backup(data_dir=DEFAULT_DATA, destination=None, *, allow_unsigned=False):
    if not isinstance(allow_unsigned, bool):
        raise BackupError("allow_unsigned debe ser un booleano explícito.")
    signing_key = _backup_signing_key()
    if signing_key is None and allow_unsigned is not True:
        raise BackupError(
            "Se requiere CYBER_AI_BACKUP_HMAC_KEY para crear backups firmados; "
            "allow_unsigned=True solo se admite para desarrollo explícito."
        )
    data_dir = Path(os.path.abspath(os.fspath(data_dir)))
    _validate_directory_path(data_dir)
    data_dir = data_dir.resolve(strict=True)
    data_directory_chain = _validate_directory_path(data_dir)
    if not data_dir.is_dir():
        raise BackupError("El directorio de datos debe existir y no ser symlink.")
    if destination is None:
        raise BackupError("Indica un destino de backup.")
    destination = Path(os.path.abspath(os.fspath(destination)))
    if destination.exists() or destination.is_symlink():
        raise BackupError("El destino ya existe; no se sobrescriben backups.")
    destination_parent_chain = _ensure_directory_path(destination.parent)
    resolved_destination = destination.resolve()
    if resolved_destination == data_dir or data_dir in resolved_destination.parents:
        raise BackupError("El backup no puede guardarse dentro del directorio de datos.")
    staging = destination.parent / f".{destination.name}.tmp-{uuid.uuid4().hex}"
    staging.mkdir(mode=0o700)
    _validate_directory_path(staging)
    entries = []
    try:
        for current, dirs, files in os.walk(data_dir, followlinks=False):
            current_path = Path(current)
            for name in list(dirs):
                child = current_path / name
                child_info = child.lstat()
                if not _is_directory_info(child_info):
                    raise BackupError(f"No se permiten symlinks ni puntos de reanálisis: {child.relative_to(data_dir)}")
            for name in sorted(files):
                source = current_path / name
                source_info = source.lstat()
                relative_source = source.relative_to(data_dir)
                if not _is_regular_file_info(source_info):
                    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
                    if stat.S_ISLNK(source_info.st_mode) or getattr(source_info, "st_file_attributes", 0) & reparse_flag:
                        raise BackupError(f"No se permiten symlinks ni puntos de reanálisis: {relative_source}")
                    raise BackupError(
                        f"Solo se respaldan archivos regulares: {relative_source}"
                    )
                if source.suffix in LOCK_SUFFIXES or source.name.endswith(("-wal", "-shm")):
                    continue
                if len(entries) >= MAX_BACKUP_FILES:
                    raise BackupError("El directorio de datos supera el límite de archivos del backup.")
                relative = source.relative_to(data_dir).as_posix()
                if relative == "manifest.json":
                    raise BackupError("data/manifest.json está reservado para el manifiesto del backup.")
                target = staging / relative
                target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                source_parent_chain = _validate_directory_path(source.parent)
                if source.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
                    target_parent_chain = _validate_directory_path(target.parent)
                    _sqlite_snapshot(source, target)
                    if not _same_directory_chain(
                        target_parent_chain, _validate_directory_path(target.parent)
                    ):
                        raise BackupError("La ruta del snapshot SQLite cambió durante la copia.")
                    kind = "sqlite_snapshot"
                else:
                    _copy_regular_file(source, target)
                    kind = "file_copy_quiesced"
                source_after = source.lstat()
                if (
                    not _is_regular_file_info(source_after)
                    or _file_state(source_info) != _file_state(source_after)
                    or not _same_directory_chain(
                        source_parent_chain, _validate_directory_path(source.parent)
                    )
                ):
                    raise BackupError(f"El origen cambió durante el backup: {relative_source}")
                try:
                    os.chmod(target, 0o600)
                except OSError:
                    pass
                entries.append({
                    "path": relative, "kind": kind, "size": target.stat().st_size,
                    "sha256": _sha256(target),
                })
        manifest = {
            "schema": SCHEMA,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source": "data-directory",
            "encrypted": False,
            "requires_quiesced_writers": True,
            "files": sorted(entries, key=lambda item: item["path"]),
        }
        if signing_key is not None:
            manifest["signature"] = {
                "algorithm": "HMAC-SHA256",
                "value": _manifest_signature(manifest, signing_key),
            }
        manifest_path = staging / "manifest.json"
        rendered_manifest = (
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )
        if len(rendered_manifest.encode("utf-8")) > MAX_MANIFEST_BYTES:
            raise BackupError("El manifiesto del backup supera 16 MiB.")
        manifest_path.write_text(rendered_manifest, encoding="utf-8")
        try:
            os.chmod(manifest_path, 0o600)
            os.chmod(staging, 0o700)
        except OSError:
            pass
        if not _same_directory_chain(data_directory_chain, _validate_directory_path(data_dir)):
            raise BackupError("El directorio de datos cambió durante el backup.")
        current_parent_chain = _validate_directory_path(destination.parent)
        if not _same_directory_chain(destination_parent_chain, current_parent_chain):
            raise BackupError("El directorio padre del backup cambió durante la creación.")
        if destination.exists() or destination.is_symlink():
            raise BackupError("El destino apareció durante la creación; no se sobrescribe.")
        os.replace(staging, destination)
        return {"destination": str(destination), "files": len(entries),
                "encrypted": False, "signed": signing_key is not None,
                "manifest_sha256": _sha256(destination / "manifest.json")}
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def verify_backup(snapshot, *, require_signature=True):
    if not isinstance(require_signature, bool):
        raise BackupError("require_signature debe ser un booleano explícito.")
    snapshot = Path(os.path.abspath(os.fspath(snapshot)))
    input_snapshot_chain = _validate_directory_path(snapshot)
    snapshot = snapshot.resolve(strict=True)
    snapshot_chain = _validate_directory_path(snapshot)
    if not _same_directory_chain(input_snapshot_chain, snapshot_chain):
        raise BackupError("La ruta del backup cambió al resolverla.")
    if not snapshot.is_dir():
        raise BackupError("El backup debe ser un directorio existente.")
    manifest_path = snapshot / "manifest.json"
    try:
        manifest_bytes = _read_regular_file(
            manifest_path, max_bytes=MAX_MANIFEST_BYTES
        )
        manifest_text = manifest_bytes.decode("utf-8")
        _enforce_manifest_json_depth(manifest_text)
        manifest = _strict_manifest_json(manifest_text)
    except BackupError:
        raise
    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as error:
        raise BackupError("El manifiesto no es JSON UTF-8 válido o contiene números fuera de rango.") from error
    report = _validate_manifest(snapshot, manifest, require_signature=require_signature)
    if not _same_directory_chain(snapshot_chain, _validate_directory_path(snapshot)):
        raise BackupError("La ruta del backup cambió durante la verificación.")
    report["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
    return report


def restore_backup(snapshot, data_dir=DEFAULT_DATA, *, confirm_quiesced=False,
                   confirm_replace=False, require_signature=True):
    if not all(isinstance(value, bool) for value in (
        confirm_quiesced, confirm_replace, require_signature
    )):
        raise BackupError("Las confirmaciones de restauración deben ser booleanos explícitos.")
    if confirm_quiesced is not True:
        raise BackupError("La restauración requiere --confirm-quiesced.")
    snapshot = Path(os.path.abspath(os.fspath(snapshot)))
    input_snapshot_chain = _validate_directory_path(snapshot)
    snapshot = snapshot.resolve(strict=True)
    snapshot_chain = _validate_directory_path(snapshot)
    if not _same_directory_chain(input_snapshot_chain, snapshot_chain):
        raise BackupError("La ruta del backup cambió al resolverla.")
    report = verify_backup(snapshot, require_signature=require_signature)
    data_dir = Path(os.path.abspath(os.fspath(data_dir)))
    data_dir_chain = None
    if data_dir.exists() or data_dir.is_symlink():
        data_dir_chain = _validate_directory_path(data_dir)
        data_dir = data_dir.resolve(strict=True)
        data_dir_chain = _validate_directory_path(data_dir)
    else:
        _ensure_directory_path(data_dir.parent)
    data_parent_chain = _validate_directory_path(data_dir.parent)
    if (
        data_dir == snapshot
        or data_dir in snapshot.parents
        or snapshot in data_dir.parents
    ):
        raise BackupError("El destino de restauración y el backup deben ser rutas independientes.")
    if data_dir.exists() and not confirm_replace:
        raise BackupError("El destino existe; usa --confirm-replace para sustituirlo.")
    staging = data_dir.parent / f".{data_dir.name}.restore-{uuid.uuid4().hex}"
    staging.mkdir(mode=0o700)
    _validate_directory_path(staging)
    previous = None
    try:
        manifest_path = snapshot / "manifest.json"
        manifest_bytes = _read_regular_file(
            manifest_path, max_bytes=MAX_MANIFEST_BYTES
        )
        if hashlib.sha256(manifest_bytes).hexdigest() != report["manifest_sha256"]:
            raise BackupError("El manifiesto cambió después de su verificación.")
        manifest_text = manifest_bytes.decode("utf-8")
        _enforce_manifest_json_depth(manifest_text)
        manifest = _strict_manifest_json(manifest_text)
        for item in manifest["files"]:
            relative = _safe_relative(item["path"])
            source = snapshot.joinpath(*relative.parts)
            target = staging.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            _copy_regular_file(source, target)
            if target.stat().st_size != item["size"] or _sha256(target) != item["sha256"]:
                raise BackupError(f"El archivo cambió durante la restauración: {relative.as_posix()}")
            if target.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
                try:
                    db = connect_private_sqlite(target, timeout=30)
                except SafeWriteError as error:
                    raise BackupError(
                        f"Snapshot SQLite no seguro: {relative.as_posix()}"
                    ) from error
                try:
                    integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
                    if integrity != "ok":
                        raise BackupError(f"Snapshot SQLite corrupto: {relative.as_posix()}")
                finally:
                    db.close()
            try:
                os.chmod(target, 0o600)
            except OSError:
                pass
        if not _same_directory_chain(snapshot_chain, _validate_directory_path(snapshot)):
            raise BackupError("La ruta del backup cambió durante la restauración.")
        if not _same_directory_chain(data_parent_chain, _validate_directory_path(data_dir.parent)):
            raise BackupError("El directorio padre del destino cambió durante la restauración.")
        if data_dir.exists():
            current_data_chain = _validate_directory_path(data_dir)
            if data_dir_chain is None or not _same_directory_chain(data_dir_chain, current_data_chain):
                raise BackupError("El destino de restauración cambió durante la operación.")
            previous = data_dir.parent / f"{data_dir.name}.pre-restore-{uuid.uuid4().hex}"
            os.replace(data_dir, previous)
        elif data_dir_chain is not None:
            raise BackupError("El destino de restauración desapareció durante la operación.")
        if data_dir.exists() or data_dir.is_symlink():
            raise BackupError("El destino apareció antes de publicar la restauración.")
        if not _same_directory_chain(data_parent_chain, _validate_directory_path(data_dir.parent)):
            raise BackupError("El directorio padre del destino cambió antes de publicar la restauración.")
        os.replace(staging, data_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        if previous and previous.exists() and not data_dir.exists():
            try:
                if _same_directory_chain(
                    data_parent_chain, _validate_directory_path(data_dir.parent)
                ):
                    os.replace(previous, data_dir)
            except BackupError:
                # Preserve the previous snapshot in place if its parent path changed.
                pass
        raise
    return {"restored": True, "files": report["files"],
            "previous_data_preserved_at": str(previous) if previous else None,
            "encrypted": False, "signed": report["signed"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    sub = parser.add_subparsers(dest="command", required=True)
    backup = sub.add_parser("backup")
    backup.add_argument("--destination", type=Path, required=True)
    backup.add_argument("--confirm-quiesced", action="store_true")
    backup.add_argument("--allow-unsigned", action="store_true")
    verify = sub.add_parser("verify")
    verify.add_argument("--snapshot", type=Path, required=True)
    verify.add_argument("--require-signature", dest="require_signature", action="store_true")
    verify.add_argument("--allow-unsigned", dest="require_signature", action="store_false")
    verify.set_defaults(require_signature=True)
    restore = sub.add_parser("restore")
    restore.add_argument("--snapshot", type=Path, required=True)
    restore.add_argument("--confirm-quiesced", action="store_true")
    restore.add_argument("--confirm-replace", action="store_true")
    restore.add_argument("--require-signature", dest="require_signature", action="store_true")
    restore.add_argument("--allow-unsigned", dest="require_signature", action="store_false")
    restore.set_defaults(require_signature=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "backup":
            if not args.confirm_quiesced:
                raise BackupError("El backup requiere --confirm-quiesced para evitar copiar logs activos.")
            if not args.allow_unsigned and _backup_signing_key() is None:
                raise BackupError(
                    "Configura CYBER_AI_BACKUP_HMAC_KEY o usa --allow-unsigned "
                    "solo para backups no productivos."
                )
            result = create_backup(
                args.data_dir, args.destination, allow_unsigned=args.allow_unsigned
            )
        elif args.command == "verify":
            result = verify_backup(args.snapshot, require_signature=args.require_signature)
        else:
            result = restore_backup(
                args.snapshot, args.data_dir,
                confirm_quiesced=args.confirm_quiesced,
                confirm_replace=args.confirm_replace,
                require_signature=args.require_signature,
            )
    except (OSError, sqlite3.Error, BackupError, json.JSONDecodeError) as error:
        print(f"ERROR: {redact_text(str(error))}", file=sys.stderr)
        return 2
    print(json.dumps(redact_sensitive_data(result), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
