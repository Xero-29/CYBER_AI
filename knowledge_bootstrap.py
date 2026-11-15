#!/usr/bin/env python3
"""Indexa los paquetes de conocimiento offline en la biblioteca SQLite."""

import argparse
import hashlib
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
MANIFEST = PROJECT / "knowledge" / "packs" / "manifest.json"


def load_packs(area_id=None):
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    areas = data.get("areas")
    if not isinstance(areas, list) or data.get("area_count") != len(areas):
        raise ValueError("Manifiesto de paquetes inválido.")
    ids = [item.get("id") for item in areas]
    if any(not isinstance(value, str) or not value.strip() for value in ids):
        raise ValueError("Identificador de área inválido.")
    if len(ids) != len(set(ids)):
        raise ValueError("Hay áreas duplicadas en el manifiesto.")
    if area_id and area_id not in ids:
        raise ValueError(f"Área desconocida: {area_id}")

    root = PROJECT.resolve()
    packs = []
    for item in areas:
        if area_id and item["id"] != area_id:
            continue
        relative = item.get("path")
        if not isinstance(relative, str) or not relative.strip():
            raise ValueError(f"Ruta inválida: {item['id']}")
        raw_path = PROJECT / relative
        if raw_path.is_symlink():
            raise ValueError(f"No se permiten symlinks: {relative}")
        path = raw_path.resolve()
        if root not in path.parents or not path.is_file():
            raise ValueError(f"Ruta fuera del proyecto o inexistente: {relative}")
        content = path.read_bytes()
        packs.append({
            "id": item["id"], "name": item.get("name", item["id"]),
            "path": path, "relative": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(content).hexdigest(), "size": len(content),
        })
    return packs


def bootstrap(area_id=None, dry_run=False):
    packs = load_packs(area_id)
    if dry_run:
        return {"dry_run": True, "selected": len(packs), "items": packs,
                "ingested_count": 0, "skipped_count": 0}

    from knowledge_ingest import ingest_document
    from knowledge_registry import register_resource, resource_inventory, update_resource_classification

    existing = {
        str(Path(item["source_path"]).resolve()): item
        for item in resource_inventory()
    }
    ingested, skipped = [], []
    for pack in packs:
        previous = existing.get(str(pack["path"]))
        if previous and previous.get("current_sha256") == pack["sha256"]:
            skipped.append(pack["id"])
            continue
        result = ingest_document(
            pack["path"], title=pack["name"],
            category=f"cybersecurity:{pack['id']}", source=pack["relative"],
            license="UNSPECIFIED", visibility="shared",
            tags=["cyber_ai", "offline_pack", pack["id"]],
        )
        registered = register_resource(
            pack["path"], sha256=pack["sha256"], file_size=pack["size"],
            resource_type="knowledge_pack", title=pack["name"],
            publisher="CYBER_AI", canonical_uri=f"repo://{pack['relative']}",
        )
        update_resource_classification(
            registered["resource_id"], area_id=pack["id"],
            domain_id=pack["id"], topic_id="baseline",
            subtopic_id="methodology", classification_status="provisional",
            reason="Paquete propio offline indexado desde el manifiesto versionado.",
        )
        ingested.append({"area": pack["id"], "chunks": result["chunks"],
                         "document_id": result["document_id"], "sha256": pack["sha256"]})
    return {"dry_run": False, "selected": len(packs), "ingested": ingested,
            "skipped": skipped, "ingested_count": len(ingested),
            "skipped_count": len(skipped)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area", help="Indexar una sola especialidad.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validar rutas y hashes sin IA ni escrituras.")
    args = parser.parse_args()
    result = bootstrap(args.area, args.dry_run)
    if args.dry_run:
        print(f"Simulación: {result['selected']} paquetes validados; sin escrituras.")
        for item in result["items"]:
            print(f"{item['id']}: {item['size']} bytes, SHA-256 {item['sha256']}")
    else:
        print(f"Indexados: {result['ingested_count']}; sin cambios: {result['skipped_count']}.")


if __name__ == "__main__":
    main()
