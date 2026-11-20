#!/usr/bin/env python3
"""Valida e indexa de forma reanudable los paquetes, estudios, dossiers y Skills candidatas."""
import argparse
import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
MANIFEST = PROJECT / "knowledge" / "packs" / "manifest.json"


@contextmanager
def exclusive_file_lock(lock, *, windows=None, windows_api=None):
    """Bloqueo exclusivo portable: flock en POSIX y byte-range lock en Windows."""
    windows = os.name == "nt" if windows is None else windows
    if windows:
        if windows_api is None:
            import msvcrt as windows_api
        lock.seek(0, os.SEEK_END)
        if lock.tell() == 0:
            lock.write(bytes(1))
            lock.flush()
        lock.seek(0)
        windows_api.locking(lock.fileno(), windows_api.LK_LOCK, 1)
        try:
            yield
        finally:
            lock.seek(0)
            windows_api.locking(lock.fileno(), windows_api.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _resolve_document(relative, root):
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("Ruta de documento inválida.")
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
    return path


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
    documents = []
    for item in areas:
        if area_id and item["id"] != area_id:
            continue
        area_name = item.get("name", item["id"])
        candidates = [
            ("pack", item.get("path"), area_name, "baseline", "methodology"),
            ("technical_compendium", item.get("technical_compendium_path"), f"{area_name} — compendio técnico", "technical", "compendium"),
            ("research_agenda", item.get("research_agenda_path"), f"{area_name} — agenda de investigación", "research", "agenda"),
            ("literature_review", item.get("literature_review_path"), f"{area_name} — revisión bibliográfica", "research", "literature_review"),
            ("deep_sections", item.get("deep_sections_path"),
             f"{area_name} — desarrollo profundo", "research", "deep_sections"),
            ("research_study", item.get("research_study_path"),
             f"{area_name} — investigación técnica", "research", "field_study"),
        ]
        for kind, relative, title, topic_id, subtopic_id in candidates:
            if relative is None:
                continue
            documents.append({
                "id": item["id"], "area_id": item["id"], "kind": kind,
                "relative": relative, "title": title,
                "topic_id": topic_id, "subtopic_id": subtopic_id,
            })

    skill_candidates = data.get("skill_candidates", [])
    if not isinstance(skill_candidates, list):
        raise ValueError("skill_candidates debe ser una lista.")
    skill_ids = set()
    for skill in skill_candidates:
        if not isinstance(skill, dict):
            raise ValueError("Cada Skill candidata debe ser un objeto.")
        skill_id = skill.get("id")
        skill_area = skill.get("area_id", "foundations")
        if not isinstance(skill_id, str) or not skill_id.strip() or skill_id in skill_ids:
            raise ValueError("ID de Skill candidata inválido o duplicado.")
        skill_ids.add(skill_id)
        if skill_area not in ids:
            raise ValueError(f"Área inválida para Skill candidata: {skill_area}")
        if area_id and skill_area != area_id:
            continue
        documents.append({
            "id": skill_id, "area_id": skill_area, "kind": "skill_candidate",
            "relative": skill.get("path"), "title": skill.get("name", skill_id),
            "topic_id": skill.get("topic_id", "skills"),
            "subtopic_id": skill.get("subtopic_id", "candidate_spec"),
        })

    supplemental_documents = data.get("supplemental_documents", [])
    if not isinstance(supplemental_documents, list):
        raise ValueError("supplemental_documents debe ser una lista.")
    supplemental_ids = set()
    for document in supplemental_documents:
        if not isinstance(document, dict):
            raise ValueError("Cada documento suplementario debe ser un objeto.")
        document_id = document.get("id")
        document_area = document.get("area_id", "foundations")
        if not isinstance(document_id, str) or not document_id.strip() or document_id in supplemental_ids:
            raise ValueError("ID de documento suplementario inválido o duplicado.")
        supplemental_ids.add(document_id)
        if document_area not in ids:
            raise ValueError(f"Área inválida para documento suplementario: {document_area}")
        if area_id and document_area != area_id:
            continue
        documents.append({
            "id": document_id, "area_id": document_area,
            "kind": "supplemental_document", "relative": document.get("path"),
            "title": document.get("name", document_id),
            "topic_id": document.get("topic_id", "supplemental"),
            "subtopic_id": document.get("subtopic_id", "reference"),
        })

    packs = []
    for item in documents:
        path = _resolve_document(item["relative"], root)
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        stable_id = "offline-" + hashlib.sha256(
            (Path(item["relative"]).as_posix() + ":" + digest).encode("utf-8")
        ).hexdigest()
        packs.append({
            "id": item["id"], "area_id": item["area_id"], "name": item["title"],
            "document_kind": item["kind"], "topic_id": item["topic_id"],
            "subtopic_id": item["subtopic_id"], "path": path,
            "relative": path.relative_to(root).as_posix(),
            "sha256": digest, "document_id": stable_id, "size": len(raw),
            "visibility": "shared", "tenant_id": None,
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
    resource_types = {
        "pack": "knowledge_pack",
        "deep_sections": "knowledge_deep_sections",
        "research_study": "knowledge_research_study",
        "technical_compendium": "knowledge_technical_compendium",
        "research_agenda": "knowledge_research_agenda",
        "literature_review": "knowledge_literature_review",
        "supplemental_document": "knowledge_supplemental_document",
        "skill_candidate": "knowledge_skill_candidate",
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
                skipped.append(
                    pack["id"] if pack["document_kind"] == "pack"
                    else f"{pack['id']}:{pack['document_kind']}"
                )
                continue
            registered = register_resource(
                pack["path"], sha256=pack["sha256"], file_size=pack["size"],
                resource_type=resource_types[pack["document_kind"]],
                title=pack["name"], publisher="CYBER_AI",
                canonical_uri=f"repo://{pack['relative']}",
            )
            resource_id = registered["resource_id"]
            update_resource_classification(
                resource_id, area_id=pack["area_id"], domain_id=pack["area_id"],
                topic_id=pack.get("topic_id", "baseline"),
                subtopic_id=pack.get("subtopic_id", "methodology"),
                classification_status="provisional",
                reason=(
                    "Especificación candidata de Skill indexada como conocimiento no activo."
                    if pack["document_kind"] == "skill_candidate"
                    else "Documento propio offline indexado desde el manifiesto versionado."
                ),
            )
            update_resource_processing_status(resource_id, "processing")
            tags = ["cyber_ai", "offline_knowledge", pack["area_id"], pack["document_kind"]]
            result = ingest_document(
                pack["path"], title=pack["name"],
                category=f"cybersecurity:{pack['area_id']}", source=pack["relative"],
                license="UNSPECIFIED", visibility="shared", tags=tags,
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
                "area": pack["area_id"], "kind": pack.get("document_kind", "pack"),
                "document_id": result["document_id"], "chunks": result["chunks"],
                "sha256": pack["sha256"],
                "already_present": bool(result.get("already_present", False)),
            })
        except Exception as error:
            if resource_id:
                try:
                    update_resource_processing_status(resource_id, "failed")
                except Exception:
                    pass
            failed.append({"area": pack["area_id"], "kind": pack.get("document_kind"), "error": str(error)[:500]})
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
    with lock_path.open("a+b") as lock:
        with exclusive_file_lock(lock):
            return _bootstrap_locked(packs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area", help="Indexar una sola especialidad.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validar rutas y hashes sin IA ni escrituras.")
    parser.add_argument("--rebuild-text-index", action="store_true",
                        help="Reconstruir el índice FTS5 sin generar embeddings.")
    args = parser.parse_args()
    if args.rebuild_text_index:
        from knowledge_library import rebuild_fts_index
        print(json.dumps(rebuild_fts_index(), ensure_ascii=False, indent=2))
        return 0
    result = bootstrap(area_id=args.area, dry_run=args.dry_run)
    print(json.dumps({
        "dry_run": result["dry_run"], "selected": result["selected"],
        "ingested": result.get("ingested_count", len(result["ingested"])),
        "skipped": result.get("skipped_count", len(result["skipped"])),
        "failed": result.get("failed_count", len(result["failed"])),
        "errors": result["failed"],
    }, ensure_ascii=False, indent=2))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
