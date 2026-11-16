#!/usr/bin/env python3
"""Backup/verificación/restauración de datos locales con snapshots SQLite y hashes."""
import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

PROJECT = Path(__file__).resolve().parent
DEFAULT_DATA = PROJECT / "data"
LOCK_SUFFIXES = {".lock", ".pid", ".sock", "-wal", "-shm"}
SCHEMA = "cyber-ai-data-backup-v1"


class BackupError(ValueError):
    pass


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_relative(value):
    rel = PurePosixPath(value)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts or "\\" in value:
        raise BackupError(f"Ruta insegura en manifiesto: {value!r}")
    return rel


def _sqlite_snapshot(source, destination):
    with sqlite3.connect(str(source), timeout=30) as src:
        with sqlite3.connect(str(destination), timeout=30) as dst:
            src.backup(dst)
            result = dst.execute("PRAGMA integrity_check").fetchone()[0]
            if result != "ok":
                raise BackupError(f"SQLite integrity_check falló para {source.name}.")


def create_backup(data_dir=DEFAULT_DATA, destination=None):
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
                if source.is_symlink():
                    raise BackupError(f"No se permiten symlinks: {source.relative_to(data_dir)}")
                if source.suffix in LOCK_SUFFIXES or source.name.endswith(("-wal", "-shm")):
                    continue
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
        manifest_path = staging / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        try:
            os.chmod(manifest_path, 0o600)
            os.chmod(staging, 0o700)
        except OSError:
            pass
        os.replace(staging, destination)
        return {"destination": str(destination), "files": len(entries),
                "encrypted": False, "manifest_sha256": _sha256(destination / "manifest.json")}
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def verify_backup(snapshot):
    snapshot = Path(snapshot)
    if snapshot.is_symlink():
        raise BackupError("El backup no puede ser symlink.")
    snapshot = snapshot.resolve()
    if not snapshot.is_dir():
        raise BackupError("El backup debe ser un directorio existente.")
    manifest_path = snapshot / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise BackupError("Falta manifest.json válido.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or not isinstance(manifest.get("files"), list):
        raise BackupError("Esquema de backup desconocido.")
    seen = set()
    verified = []
    for item in manifest["files"]:
        if not isinstance(item, dict):
            raise BackupError("Entrada de manifiesto inválida.")
        relative = _safe_relative(item.get("path", ""))
        if relative.as_posix() in seen:
            raise BackupError("Ruta duplicada en manifiesto.")
        seen.add(relative.as_posix())
        path = snapshot
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise BackupError(f"Hay symlink en el backup: {relative.as_posix()}")
        if not path.is_file():
            raise BackupError(f"Falta archivo: {relative.as_posix()}")
        try:
            path.resolve().relative_to(snapshot)
        except ValueError as error:
            raise BackupError(f"Ruta fuera del backup: {relative.as_posix()}") from error
        actual_hash = _sha256(path)
        if actual_hash != item.get("sha256") or path.stat().st_size != item.get("size"):
            raise BackupError(f"Integridad no válida: {relative.as_posix()}")
        verified.append(relative.as_posix())
    return {"valid": True, "files": len(verified), "paths": verified,
            "encrypted": manifest.get("encrypted") is True}


def restore_backup(snapshot, data_dir=DEFAULT_DATA, *, confirm_quiesced=False,
                   confirm_replace=False):
    if confirm_quiesced is not True:
        raise BackupError("La restauración requiere --confirm-quiesced.")
    snapshot = Path(snapshot)
    if snapshot.is_symlink():
        raise BackupError("El backup no puede ser symlink.")
    snapshot = snapshot.resolve()
    report = verify_backup(snapshot)
    data_dir = Path(data_dir)
    if data_dir.is_symlink():
        raise BackupError("El directorio de datos no puede ser symlink.")
    data_dir = data_dir.resolve()
    if data_dir.exists() and not confirm_replace:
        raise BackupError("El destino existe; usa --confirm-replace para sustituirlo.")
    if data_dir.is_symlink():
        raise BackupError("El directorio de datos no puede ser symlink.")
    staging = data_dir.parent / f".{data_dir.name}.restore-{uuid.uuid4().hex}"
    staging.mkdir(mode=0o700)
    previous = None
    try:
        manifest = json.loads((snapshot / "manifest.json").read_text(encoding="utf-8"))
        for item in manifest["files"]:
            relative = _safe_relative(item["path"])
            source = snapshot.joinpath(*relative.parts)
            target = staging.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(source, target)
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
            "encrypted": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    sub = parser.add_subparsers(dest="command", required=True)
    backup = sub.add_parser("backup")
    backup.add_argument("--destination", type=Path, required=True)
    backup.add_argument("--confirm-quiesced", action="store_true")
    verify = sub.add_parser("verify")
    verify.add_argument("--snapshot", type=Path, required=True)
    restore = sub.add_parser("restore")
    restore.add_argument("--snapshot", type=Path, required=True)
    restore.add_argument("--confirm-quiesced", action="store_true")
    restore.add_argument("--confirm-replace", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "backup":
            if not args.confirm_quiesced:
                raise BackupError("El backup requiere --confirm-quiesced para evitar copiar logs activos.")
            result = create_backup(args.data_dir, args.destination)
        elif args.command == "verify":
            result = verify_backup(args.snapshot)
        else:
            result = restore_backup(
                args.snapshot, args.data_dir,
                confirm_quiesced=args.confirm_quiesced,
                confirm_replace=args.confirm_replace,
            )
    except (OSError, sqlite3.Error, BackupError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
