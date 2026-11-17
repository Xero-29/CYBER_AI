"""Auditoría estructural y de trazabilidad de la biblioteca de investigación.

No certifica exactitud semántica, lectura integral, resultados científicos ni madurez M3-M5.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
REQUIRED_AGENDA_CONCEPTS = {
    "hipótesis": ("hipótesis",),
    "método": ("método", "metodología", "diseño de investigación", "diseño experimental", "diseño y análisis", "protocolo"),
    "métricas": ("métricas", "indicadores"),
    "entregable": ("entregable", "entregables", "artefacto", "artefactos", "producto", "productos", "publicación"),
    "madurez": ("madurez", "estado", "umbral"),
}
REQUIRED_DOSSIER_MARKERS = (
    "## pregunta",
    "## síntesis",
    "## brechas",
    "## identificadores del registro de fuentes",
)
SOURCE_ID_PATTERN = re.compile(r"^- `([A-Za-z0-9.-]+)`$", re.MULTILINE)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def audit_research_library(root: Path = ROOT) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = json.loads(_read_text(root / "knowledge/packs/manifest.json"))
        curriculum = json.loads(_read_text(root / "knowledge/curricula/domain_curriculum.json"))
        registry = json.loads(_read_text(root / "knowledge/research/source_registry.json"))
        protocol = _read_text(root / "knowledge/research/RESEARCH_PROTOCOL.md")
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "ok": False, "errors": [str(exc)], "warnings": [],
            "area_count": 0, "agenda_count": 0, "literature_review_count": 0,
        }

    manifest_areas = manifest.get("areas", [])
    curriculum_areas = curriculum.get("areas", [])
    manifest_ids = [x.get("id") for x in manifest_areas]
    curriculum_ids = [x.get("id") for x in curriculum_areas]
    if len(manifest_ids) != len(set(manifest_ids)):
        errors.append("IDs duplicados en manifiesto")
    if set(manifest_ids) != set(curriculum_ids):
        errors.append("Manifiesto y currículo no coinciden")

    sources = registry.get("sources", [])
    source_ids = [s.get("id") for s in sources]
    source_errors: list[str] = []
    if len(source_ids) != len(set(source_ids)):
        source_errors.append("IDs duplicados en registro de fuentes")
    for source in sources:
        sid = source.get("id", "?")
        for key in ("id", "title", "publisher", "url", "verification_status", "review_note"):
            if not source.get(key):
                source_errors.append(f"fuente sin {key}: {sid}")
        parsed = urlparse(source.get("url", ""))
        if parsed.scheme != "https" or not parsed.netloc:
            source_errors.append(f"URL no canónica HTTPS: {sid}")
        if not isinstance(source.get("domains"), list) or not source.get("domains"):
            source_errors.append(f"fuente sin dominios asociados: {sid}")
    known_source_ids = set(source_ids)

    area_results = []
    agenda_count = 0
    agenda_complete_count = 0
    dossier_count = 0
    dossier_complete_count = 0
    referenced_ids: set[str] = set()

    for area in manifest_areas:
        area_id = area.get("id", "?")
        base = root / "knowledge/deep_modules" / area_id
        agenda_errors: list[str] = []
        dossier_errors: list[str] = []
        agenda_path = base / "RESEARCH_AGENDA.md"
        dossier_path = base / "LITERATURE_REVIEW.md"

        try:
            agenda = _read_text(agenda_path)
            agenda_count += 1
        except OSError:
            agenda = ""
            agenda_errors.append("agenda inexistente o ilegible")
        if agenda and not agenda.startswith("# Agenda de investigación:"):
            agenda_errors.append("título de agenda inválido")
        agenda_lower = agenda.casefold()
        for concept, alternatives in REQUIRED_AGENDA_CONCEPTS.items():
            if not any(term in agenda_lower for term in alternatives):
                agenda_errors.append("falta concepto requerido en agenda: " + concept)
        if "research_agenda_defined" not in agenda:
            agenda_errors.append("no declara madurez de agenda")
        if "M5" not in agenda or "reproducción" not in agenda_lower:
            agenda_errors.append("no define umbral de revisión/reproducción")
        if not agenda_errors:
            agenda_complete_count += 1

        try:
            dossier = _read_text(dossier_path)
            dossier_count += 1
        except OSError:
            dossier = ""
        if dossier:
            lowered = dossier.casefold()
            for marker in REQUIRED_DOSSIER_MARKERS:
                if marker not in lowered:
                    dossier_errors.append("falta sección de revisión: " + marker)
            if "corte:" not in lowered or "madurez:" not in lowered:
                dossier_errors.append("falta fecha de corte o madurez explícita")
            if "no m3/m4" not in lowered and "no m4" not in lowered and "no m3" not in lowered:
                dossier_errors.append("no declara límite de madurez empírica")
            ids = SOURCE_ID_PATTERN.findall(dossier)
            if not ids:
                dossier_errors.append("no enlaza IDs del registro de fuentes")
            for sid in ids:
                referenced_ids.add(sid)
                if sid not in known_source_ids:
                    dossier_errors.append("ID de fuente no registrado: " + sid)
            if not dossier_errors:
                dossier_complete_count += 1
            else:
                errors.append(f"{area_id}: " + "; ".join(dossier_errors))

        area_results.append({
            "id": area_id,
            "agenda_exists": bool(agenda),
            "agenda_structurally_complete": not agenda_errors,
            "agenda_errors": agenda_errors,
            "literature_review_exists": bool(dossier),
            "literature_review_traceable": bool(dossier) and not dossier_errors,
            "literature_review_errors": dossier_errors,
        })

    if "reproducción" not in protocol.casefold() or "amenazas a la validez" not in protocol.casefold():
        errors.append("protocolo de investigación incompleto")
    unknown_references = sorted(referenced_ids - known_source_ids)
    if unknown_references:
        source_errors.append("referencias a IDs inexistentes: " + ", ".join(unknown_references))

    missing_dossiers = len(manifest_areas) - dossier_count
    if missing_dossiers:
        warnings.append(
            f"Revisiones bibliográficas presentes: {dossier_count}/{len(manifest_areas)}; "
            "las áreas restantes conservan agenda, no revisión de literatura ejecutada."
        )
    if dossier_complete_count != dossier_count:
        warnings.append("Hay revisiones bibliográficas con trazabilidad o estructura incompleta.")
    if not referenced_ids:
        warnings.append("Ningún dossier enlaza fuentes del registro.")

    # Distinguimos metadatos de catálogo de páginas/documentos inspeccionados.
    reviewed_statuses = {
        "official_project_page_reviewed", "official_risk_page_reviewed",
        "official_metadata_and_abstract_reviewed", "official_pdf_sections_inspected",
        "official_draft_metadata_reviewed", "official_draft_metadata_and_announcement_reviewed",
        "official_specification_pages_reviewed",
        "official_data_repository_reviewed", "official_release_notes_reviewed",
        "official_version_history_reviewed", "official_model_documentation_reviewed",
        "official_methodology_page_reviewed", "official_standard_metadata_reviewed",
    }
    source_reviewed_count = sum(s.get("verification_status") in reviewed_statuses for s in sources)
    source_metadata_only_count = sum(s.get("verification_status") == "official_metadata_verified" for s in sources)
    source_catalog_only_count = sum(
        "catalog" in s.get("verification_status", "") or "registered" in s.get("verification_status", "")
        for s in sources
    )

    core_ok = not errors and not source_errors and agenda_complete_count == len(manifest_areas)
    return {
        "ok": core_ok,
        "coverage_complete": (
            dossier_count == len(manifest_areas)
            and dossier_complete_count == len(manifest_areas)
        ),
        "area_count": len(manifest_areas),
        "agenda_count": agenda_count,
        "structurally_complete_agendas": agenda_complete_count,
        "literature_review_count": dossier_count,
        "traceable_literature_reviews": dossier_complete_count,
        "source_count": len(sources),
        "source_pages_or_documents_reviewed": source_reviewed_count,
        "source_metadata_only_count": source_metadata_only_count,
        "catalog_references_registered_not_content_reviewed": source_catalog_only_count,
        "unique_source_ids_referenced_by_dossiers": len(referenced_ids),
        "errors": errors + source_errors,
        "warnings": warnings,
        "areas": area_results,
        "limitations": [
            "La auditoría comprueba estructura y trazabilidad de IDs, no exactitud semántica ni exhaustividad bibliográfica.",
            "Una página oficial revisada no equivale a lectura integral del estándar o documento.",
            "No demuestra que se haya ejecutado una revisión sistemática, experimento o reproducción.",
            "No asigna madurez M3/M4/M5 ni certifica competencia de investigadores o agentes.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit_research_library()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Áreas: {report['area_count']}")
        print(f"Agendas completas: {report['structurally_complete_agendas']}/{report['area_count']}")
        print(f"Revisiones bibliográficas: {report['traceable_literature_reviews']}/{report['area_count']}")
        print(f"Fuentes registradas: {report['source_count']}")
        print(f"Solo metadatos revisados: {report['source_metadata_only_count']}")
        print(f"Páginas/documentos revisados: {report['source_pages_or_documents_reviewed']}")
        print(f"Referencias de catálogo sin revisión de contenido: {report['catalog_references_registered_not_content_reviewed']}")
        for item in report["errors"]:
            print("ERROR:", item)
        for item in report["warnings"]:
            print("PENDIENTE:", item)
        for item in report["limitations"]:
            print("LÍMITE:", item)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
