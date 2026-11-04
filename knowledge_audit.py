#!/usr/bin/env python3
"""Auditoría de solo lectura de archivos y biblioteca de CYBER_AI."""

import argparse
import hashlib
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "data/knowledge_sources/download_manifest.json"
DATABASE = ROOT / "data/knowledge_library.sqlite3"
REPORT_DIR = ROOT / "data/knowledge_sources/audit_reports"


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit_files():
    result = {
        "manifest_missing": [],
        "size_mismatch": [],
        "hash_mismatch": [],
        "temporary_files": [],
        "unregistered_files": [],
        "duplicate_files": [],
        "checked_files": 0,
    }

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    resources = data.get("resources", {})
    registered = set()

    for name, item in resources.items():
        relative = item.get("file")
        if not relative:
            result["manifest_missing"].append({
                "resource": name,
                "reason": "No tiene ruta registrada",
            })
            continue

        path = (ROOT / relative).resolve()
        registered.add(path)

        if not path.is_file():
            result["manifest_missing"].append({
                "resource": name,
                "path": str(path),
            })
            continue

        result["checked_files"] += 1
        actual_size = path.stat().st_size

        if actual_size != item.get("bytes"):
            result["size_mismatch"].append({
                "resource": name,
                "expected": item.get("bytes"),
                "actual": actual_size,
            })

        expected_hash = item.get("sha256")
        if expected_hash:
            actual_hash = sha256_file(path)
            if actual_hash != expected_hash:
                result["hash_mismatch"].append({
                    "resource": name,
                    "expected": expected_hash,
                    "actual": actual_hash,
                })

    scan_roots = [
        ROOT / "data/knowledge_sources",
        ROOT / "data/knowledge_base",
    ]

    hashes = defaultdict(list)

    for folder in scan_roots:
        if not folder.exists():
            continue

        for path in folder.rglob("*"):
            if not path.is_file():
                continue

            resolved = path.resolve()

            if path.name.endswith(".part"):
                result["temporary_files"].append(str(path))
                continue

            if path.suffix.lower() not in {
                ".pdf", ".html", ".htm", ".txt", ".md"
            }:
                continue

            if resolved not in registered:
                result["unregistered_files"].append(str(path))

            hashes[sha256_file(path)].append(str(path))

    result["duplicate_files"] = [
        {"sha256": digest, "files": paths}
        for digest, paths in hashes.items()
        if len(paths) > 1
    ]

    return result


def audit_database():
    if not DATABASE.is_file():
        return {"error": "No existe la base de datos."}

    db = sqlite3.connect(DATABASE)
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

    db.close()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
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
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("========== AUDITORÍA CYBER_AI ==========")
    print("Modo: SOLO LECTURA")
    print("Archivos comprobados:", report["files"]["checked_files"])

    for key, value in report["files"].items():
        if isinstance(value, list):
            print(f"{key}: {len(value)}")

    print("Fragmentos SQLite:", report["database"].get("chunks"))
    print("Documentos SQLite:", report["database"].get("documents"))
    print(
        "Contenido duplicado SQLite:",
        len(report["database"].get("duplicate_content", [])),
    )
    print(
        "Posiciones duplicadas SQLite:",
        len(report["database"].get("duplicate_positions", [])),
    )
    print("Informe:", output.relative_to(ROOT))
    print("No se eliminó ni modificó ningún documento.")


if __name__ == "__main__":
    main()
