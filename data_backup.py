#!/usr/bin/env python3
"""Backup/verificación/restauración de datos locales con snapshots SQLite y hashes."""
import argparse
import hashlib
import hmac
import json
import os
import re
import shutil
import sqlite3
import stat
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

PROJECT = Path(__file__).resolve().parent
DEFAULT_DATA = PROJECT / "data"
LOCK_SUFFIXES = {".lock", ".pid", ".sock", "-wal", "-shm"}
SCHEMA = "cyber-ai-data-backup-v1"
MAX_BACKUP_FILES = 50_000
MAX_MANIFEST_BYTES = 16 * 1024 * 1024


class BackupError(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BackupError("El manifiesto contiene claves JSON duplicadas.")
        result[key] = value
    return result


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise BackupError(f"Hay symlink en el backup: {key}")
        if not path.is_file():
            raise BackupError(f"Falta archivo: {key}")
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
            if (current_path / name).is_symlink():
                raise BackupError("No se permiten symlinks en el backup.")
        for name in names:
            path = current_path / name
            if path.is_symlink():
                raise BackupError("No se permiten symlinks en el backup.")
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
    with sqlite3.connect(str(source), timeout=30) as src:
        with sqlite3.connect(str(destination), timeout=30) as dst:
            src.backup(dst)
            result = dst.execute("PRAGMA integrity_check").fetchone()[0]
            if result != "ok":
                raise BackupError(f"SQLite integrity_check falló para {source.name}.")


def create_backup(data_dir=DEFAULT_DATA, destination=None):
    signing_key = _backup_signing_key()
    data_dir = Path(data_dir)
    if data_dir.is_symlink():
        raise BackupError("El directorio de datos no puede ser symlink.")
    data_dir = data_dir.resolve()
    if not data_dir.is_dir():
        raise BackupError("El directorio de datos debe existir y no ser symlink.")
    if destination is None:
        raise BackupError("Indica un destino de backup.")
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise BackupError("El destino ya existe; no se sobrescriben backups.")
    resolved_destination = destination.resolve()
    if resolved_destination == data_dir or data_dir in resolved_destination.parents:
        raise BackupError("El backup no puede guardarse dentro del directorio de datos.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.parent / f".{destination.name}.tmp-{uuid.uuid4().hex}"
    staging.mkdir(mode=0o700)
    entries = []
    try:
        for current, dirs, files in os.walk(data_dir, followlinks=False):
            current_path = Path(current)
            for name in list(dirs):
                child = current_path / name
                if child.is_symlink():
                    raise BackupError(f"No se permiten symlinks: {child.relative_to(data_dir)}")
            for name in sorted(files):
                source = current_path / name
                source_info = source.lstat()
                relative_source = source.relative_to(data_dir)
                if stat.S_ISLNK(source_info.st_mode):
                    raise BackupError(f"No se permiten symlinks: {relative_source}")
                if not stat.S_ISREG(source_info.st_mode):
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
                if source.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
                    _sqlite_snapshot(source, target)
                    kind = "sqlite_snapshot"
                else:
                    shutil.copy2(source, target)
                    kind = "file_copy_quiesced"
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
        os.replace(staging, destination)
        return {"destination": str(destination), "files": len(entries),
                "encrypted": False, "signed": signing_key is not None,
                "manifest_sha256": _sha256(destination / "manifest.json")}
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def verify_backup(snapshot, *, require_signature=False):
    snapshot = Path(snapshot)
    if snapshot.is_symlink():
        raise BackupError("El backup no puede ser symlink.")
    snapshot = snapshot.resolve()
    if not snapshot.is_dir():
        raise BackupError("El backup debe ser un directorio existente.")
    manifest_path = snapshot / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise BackupError("Falta manifest.json válido.")
    try:
        if manifest_path.stat().st_size > MAX_MANIFEST_BYTES:
            raise BackupError("El manifiesto del backup supera 16 MiB.")
        manifest_bytes = manifest_path.read_bytes()
        if len(manifest_bytes) > MAX_MANIFEST_BYTES:
            raise BackupError("El manifiesto del backup supera 16 MiB.")
        manifest = json.loads(
            manifest_bytes.decode("utf-8"), object_pairs_hook=_unique_object
        )
    except RecursionError as error:
        raise BackupError("El manifiesto supera la profundidad JSON permitida.") from error
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise BackupError("El manifiesto no es JSON UTF-8 válido.") from error
    report = _validate_manifest(snapshot, manifest, require_signature=require_signature)
    report["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
    return report


def restore_backup(snapshot, data_dir=DEFAULT_DATA, *, confirm_quiesced=False,
                   confirm_replace=False, require_signature=False):
    if confirm_quiesced is not True:
        raise BackupError("La restauración requiere --confirm-quiesced.")
    snapshot = Path(snapshot)
    if snapshot.is_symlink():
        raise BackupError("El backup no puede ser symlink.")
    snapshot = snapshot.resolve()
    report = verify_backup(snapshot, require_signature=require_signature)
    data_dir = Path(data_dir)
    if data_dir.is_symlink():
        raise BackupError("El directorio de datos no puede ser symlink.")
    data_dir = data_dir.resolve()
    if (
        data_dir == snapshot
        or data_dir in snapshot.parents
        or snapshot in data_dir.parents
    ):
        raise BackupError("El destino de restauración y el backup deben ser rutas independientes.")
    if data_dir.exists() and not confirm_replace:
        raise BackupError("El destino existe; usa --confirm-replace para sustituirlo.")
    if data_dir.is_symlink():
        raise BackupError("El directorio de datos no puede ser symlink.")
    data_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = data_dir.parent / f".{data_dir.name}.restore-{uuid.uuid4().hex}"
    staging.mkdir(mode=0o700)
    previous = None
    try:
        manifest_bytes = (snapshot / "manifest.json").read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != report["manifest_sha256"]:
            raise BackupError("El manifiesto cambió después de su verificación.")
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        for item in manifest["files"]:
            relative = _safe_relative(item["path"])
            source = snapshot.joinpath(*relative.parts)
            target = staging.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(source, target)
            if target.stat().st_size != item["size"] or _sha256(target) != item["sha256"]:
                raise BackupError(f"El archivo cambió durante la restauración: {relative.as_posix()}")
            if target.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
                with sqlite3.connect(str(target), timeout=30) as db:
                    integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
                    if integrity != "ok":
                        raise BackupError(f"Snapshot SQLite corrupto: {relative.as_posix()}")
            try:
                os.chmod(target, 0o600)
            except OSError:
                pass
        if data_dir.exists():
            previous = data_dir.parent / f"{data_dir.name}.pre-restore-{uuid.uuid4().hex}"
            os.replace(data_dir, previous)
        os.replace(staging, data_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        if previous and previous.exists() and not data_dir.exists():
            os.replace(previous, data_dir)
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
    verify = sub.add_parser("verify")
    verify.add_argument("--snapshot", type=Path, required=True)
    verify.add_argument("--require-signature", action="store_true")
    restore = sub.add_parser("restore")
    restore.add_argument("--snapshot", type=Path, required=True)
    restore.add_argument("--confirm-quiesced", action="store_true")
    restore.add_argument("--confirm-replace", action="store_true")
    restore.add_argument("--require-signature", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "backup":
            if not args.confirm_quiesced:
                raise BackupError("El backup requiere --confirm-quiesced para evitar copiar logs activos.")
            result = create_backup(args.data_dir, args.destination)
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
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
