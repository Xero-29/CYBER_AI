#!/usr/bin/env python3
"""Valida e indexa de forma reanudable los paquetes offline de CYBER_AI."""
import argparse
import fcntl
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
    ids = []
    for item in areas:
        if not isinstance(item, dict):
            raise ValueError("Cada área debe ser un objeto.")
        value = item.get("id")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Identificador de área inválido.")
        ids.append(value)
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
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError(f"Ruta no permitida: {relative}")
        current = PROJECT
        for part in rel.parts:
            if part in {"", "."}:
                continue
            current = current / part
            if current.is_symlink():
                raise ValueError(f"No se permiten symlinks: {relative}")
        path = (PROJECT / rel).resolve()
        if root not in path.parents or not path.is_file():
            raise ValueError(f"Ruta fuera del proyecto o inexistente: {relative}")
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        stable_id = "offline-" + hashlib.sha256(
            (rel.as_posix() + ":" + digest).encode("utf-8")
        ).hexdigest()
        packs.append({
            "id": item["id"], "name": item.get("name", item["id"]),
            "path": path, "relative": path.relative_to(root).as_posix(),
            "sha256": digest, "document_id": stable_id, "size": len(raw),
        })
    return packs


def _bootstrap_locked(packs, dry_run=False):
    if dry_run:
        return {"dry_run": True, "selected": len(packs), "items": packs,
                "ingested": [], "skipped": [], "failed": []}
    from knowledge_embeddings import expected_embedding_space
    embedding_model = expected_embedding_space("ECO")
    from knowledge_ingest import ingest_document
    from knowledge_library import document_chunk_count
    from knowledge_registry import (
        register_resource, resource_inventory, update_resource_classification,
        update_resource_processing_status,
    )
    existing = {
        str(Path(row["source_path"]).resolve()): row
        for row in resource_inventory()
    }
    ingested, skipped, failed = [], [], []
    for pack in packs:
        resource_id = None
        try:
            previous = existing.get(str(pack["path"]))
            if (previous and previous.get("current_sha256") == pack["sha256"]
                    and previous.get("processing_status") == "completed"
                    and document_chunk_count(
                pack["document_id"], embedding_model,
                visibility=pack["visibility"], tenant_id=pack["tenant_id"],
            ) > 0):
                skipped.append(pack["id"])
                continue
            registered = register_resource(
                pack["path"], sha256=pack["sha256"], file_size=pack["size"],
                resource_type="knowledge_pack", title=pack["name"],
                publisher="CYBER_AI", canonical_uri=f"repo://{pack['relative']}",
            )
            resource_id = registered["resource_id"]
            update_resource_classification(
                resource_id, area_id=pack["id"], domain_id=pack["id"],
                topic_id="baseline", subtopic_id="methodology",
                classification_status="provisional",
                reason="Paquete propio offline indexado desde el manifiesto versionado.",
            )
            update_resource_processing_status(resource_id, "processing")
            result = ingest_document(
                pack["path"], title=pack["name"],
                category=f"cybersecurity:{pack['id']}", source=pack["relative"],
                license="UNSPECIFIED", visibility="shared",
                tags=["cyber_ai", "offline_pack", pack["id"]],
                document_id=pack["document_id"],
                expected_embedding_model=embedding_model,
            )
            if result["chunks"] < 1 or document_chunk_count(
                pack["document_id"], embedding_model,
                visibility=pack["visibility"], tenant_id=pack["tenant_id"],
            ) < 1:
                raise RuntimeError("La ingestión no publicó fragmentos verificables.")
            update_resource_processing_status(resource_id, "completed")
            ingested.append({
                "area": pack["id"], "document_id": result["document_id"],
                "chunks": result["chunks"], "sha256": pack["sha256"],
                "already_present": bool(result.get("already_present", False)),
            })
        except Exception as error:
            if resource_id:
                try:
                    update_resource_processing_status(resource_id, "failed")
                except Exception:
                    pass
            failed.append({"area": pack["id"], "error": str(error)[:500]})
    return {
        "dry_run": False, "selected": len(packs), "ingested": ingested,
        "skipped": skipped, "failed": failed,
        "ingested_count": len(ingested), "skipped_count": len(skipped),
        "failed_count": len(failed),
    }


def bootstrap(area_id=None, dry_run=False):
    packs = load_packs(area_id)
    if dry_run:
        return _bootstrap_locked(packs, dry_run=True)
    lock_path = PROJECT / "data" / "knowledge_bootstrap.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            return _bootstrap_locked(packs)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area", help="Indexar una sola especialidad.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validar rutas y hashes sin IA ni escrituras.")
    parser.add_argument("--rebuild-text-index", action="store_true",
                        help="Reconstruir el índice FTS5 sin generar embeddings.")
    args = parser.parse_args()
    if args.rebuild_text_index:
        from knowledge_library import rebuild_text_index
        result = rebuild_text_index()
        print(f"Índice textual disponible: {result['available']}; fragmentos: {result['indexed']}.")
        return
    result = bootstrap(args.area, args.dry_run)
    if args.dry_run:
        print(f"Validación: {result['selected']} paquetes; sin IA ni escrituras.")
        for item in result["items"]:
            print(f"{item['id']}: {item['size']} bytes SHA-256 {item['sha256']}")
    else:
        print(f"Indexados: {result['ingested_count']}; sin cambios: "
              f"{result['skipped_count']}; fallidos: {result['failed_count']}.")
        for item in result["failed"]:
            print(f"ERROR {item['area']}: {item['error']}")


if __name__ == "__main__":
    main()
