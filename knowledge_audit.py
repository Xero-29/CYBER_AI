#!/usr/bin/env python3
"""Auditoría de solo lectura de archivos y biblioteca de CYBER_AI."""

import argparse
import hashlib
import json
import os
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "data/knowledge_sources/download_manifest.json"
DATABASE = ROOT / "data/knowledge_library.sqlite3"
REPORT_DIR = ROOT / "data/knowledge_sources/audit_reports"
AUDIT_EXTENSIONS = {".pdf", ".html", ".htm", ".txt", ".md"}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_manifest_path(root, relative):
    """Resolve a manifest path without accepting traversal or symlinks."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("La ruta debe ser un texto POSIX relativo.")
    candidate = PurePosixPath(relative)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise ValueError("La ruta absoluta o con traversal está prohibida.")
    root = Path(root).resolve()
    path = root.joinpath(*candidate.parts)
    cursor = root
    for part in candidate.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("No se permiten symlinks en rutas del manifiesto.")
    try:
        path.resolve(strict=False).relative_to(root)
    except ValueError as error:
        raise ValueError("La ruta sale del directorio del proyecto.") from error
    return path


def audit_files(manifest_path=MANIFEST, root=ROOT):
    result = {
        "manifest_missing": [],
        "manifest_errors": [],
        "size_mismatch": [],
        "hash_mismatch": [],
        "temporary_files": [],
        "unregistered_files": [],
        "unsafe_paths": [],
        "duplicate_files": [],
        "checked_files": 0,
    }
    root = Path(root).resolve()
    manifest_path = Path(manifest_path)
    try:
        if manifest_path.is_symlink():
            raise ValueError("El manifiesto no puede ser symlink.")
        manifest_path.resolve(strict=True).relative_to(root)
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result["manifest_errors"].append("No existe download_manifest.json.")
        return result
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        result["manifest_errors"].append(f"Manifiesto no válido: {error}")
        return result

    resources = data.get("resources") if isinstance(data, dict) else None
    if not isinstance(resources, dict):
        result["manifest_errors"].append("resources debe ser un objeto JSON.")
        return result

    registered = set()
    for name, item in resources.items():
        if not isinstance(item, dict):
            result["manifest_errors"].append(
                f"El recurso {name!r} no es un objeto."
            )
            continue
        relative = item.get("file")
        if not relative:
            result["manifest_missing"].append({
                "resource": name, "reason": "No tiene ruta registrada",
            })
            continue
        try:
            path = _safe_manifest_path(root, relative)
        except ValueError as error:
            result["unsafe_paths"].append({
                "resource": name, "path": str(relative), "reason": str(error),
            })
            continue

        registered.add(path.resolve(strict=False))
        if not path.is_file():
            result["manifest_missing"].append({
                "resource": name, "path": str(relative),
            })
            continue

        result["checked_files"] += 1
        actual_size = path.stat().st_size
        expected_size = item.get("bytes")
        if expected_size is not None and (
            isinstance(expected_size, bool)
            or not isinstance(expected_size, int)
            or actual_size != expected_size
        ):
            result["size_mismatch"].append({
                "resource": name, "expected": expected_size,
                "actual": actual_size,
            })

        expected_hash = item.get("sha256")
        if expected_hash is not None:
            if not isinstance(expected_hash, str) or len(expected_hash) != 64:
                result["manifest_errors"].append(
                    f"SHA-256 inválido para el recurso {name!r}."
                )
            else:
                actual_hash = sha256_file(path)
                if actual_hash != expected_hash.lower():
                    result["hash_mismatch"].append({
                        "resource": name, "expected": expected_hash,
                        "actual": actual_hash,
                    })

    scan_roots = [
        root / "data/knowledge_sources",
        root / "data/knowledge_base",
    ]
    hashes = defaultdict(list)
    for folder in scan_roots:
        if not folder.exists():
            continue
        for current, dirs, files in os.walk(folder, followlinks=False):
            current_path = Path(current)
            for dirname in list(dirs):
                child = current_path / dirname
                if child.is_symlink():
                    result["unsafe_paths"].append({
                        "path": str(child), "reason": "Directorio symlink omitido.",
                    })
                    dirs.remove(dirname)
            for filename in files:
                path = current_path / filename
                if path.is_symlink():
                    result["unsafe_paths"].append({
                        "path": str(path), "reason": "Archivo symlink omitido.",
                    })
                    continue
                if path.name.endswith(".part"):
                    result["temporary_files"].append(str(path))
                    continue
                if path.suffix.lower() not in AUDIT_EXTENSIONS:
                    continue
                resolved = path.resolve()
                if resolved not in registered:
                    result["unregistered_files"].append(str(path))
                hashes[sha256_file(path)].append(str(path))

    result["duplicate_files"] = [
        {"sha256": digest, "files": paths}
        for digest, paths in hashes.items() if len(paths) > 1
    ]
    return result


def audit_database(database_path=DATABASE):
    database_path = Path(database_path)
    if not database_path.is_file() or database_path.is_symlink():
        return {"error": "No existe la base de datos o no es un archivo regular."}

    db = None
    try:
        db = sqlite3.connect(
            database_path.resolve().as_uri() + "?mode=ro",
            uri=True, timeout=5,
        )
        result = {}
        result["chunks"] = db.execute(
            "SELECT COUNT(*) FROM knowledge_chunks"
        ).fetchone()[0]
        result["documents"] = db.execute(
            "SELECT COUNT(DISTINCT document_id) FROM knowledge_chunks"
        ).fetchone()[0]
        result["duplicate_content"] = db.execute("""
            SELECT content_sha256, COUNT(*)
            FROM knowledge_chunks
            GROUP BY content_sha256
            HAVING COUNT(*) > 1
        """).fetchall()
        result["duplicate_positions"] = db.execute("""
            SELECT document_id, chunk_index, COUNT(*)
            FROM knowledge_chunks
            GROUP BY document_id, chunk_index
            HAVING COUNT(*) > 1
        """).fetchall()
        return result
    except sqlite3.Error as error:
        return {"error": f"No se pudo auditar la base de datos en modo lectura: {error}"}
    finally:
        if db is not None:
            db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Ejecuta la auditoría de solo lectura.",
    )
    args = parser.parse_args()
    if not args.check:
        parser.error("Por seguridad, utiliza --check.")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY",
        "files": audit_files(),
        "database": audit_database(),
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output = REPORT_DIR / (
        "audit_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + ".json"
    )
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    print("========== AUDITORÍA CYBER_AI ==========")
    print("Modo: SOLO LECTURA")
    print("Archivos comprobados:", report["files"]["checked_files"])
    for key, value in report["files"].items():
        if isinstance(value, list):
            print(f"{key}: {len(value)}")
    print("Fragmentos SQLite:", report["database"].get("chunks"))
    print("Documentos SQLite:", report["database"].get("documents"))
    print("Contenido duplicado SQLite:",
          len(report["database"].get("duplicate_content", [])))
    print("Posiciones duplicadas SQLite:",
          len(report["database"].get("duplicate_positions", [])))
    print("Informe:", output.relative_to(ROOT))
    print("No se eliminó ni modificó ningún documento.")


if __name__ == "__main__":
    main()
