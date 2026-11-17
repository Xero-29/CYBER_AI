"""Auditoría estructural de agendas de investigación; no certifica resultados científicos."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_HEADINGS = (
    "# Agenda de investigación:",
    "## Pregunta central",
    "##",
)
REQUIRED_TERMS = (
    "hipótesis",
    "método",
    "métricas",
    "entregable",
    "madurez",
)


def audit_research_library(root: Path = ROOT) -> dict:
    errors: list[str] = []
    try:
        manifest = json.loads((root / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
        curriculum = json.loads((root / "knowledge/curricula/domain_curriculum.json").read_text(encoding="utf-8"))
        registry = json.loads((root / "knowledge/research/source_registry.json").read_text(encoding="utf-8"))
        protocol = (root / "knowledge/research/RESEARCH_PROTOCOL.md").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "area_count": 0, "agenda_count": 0}

    manifest_areas = manifest.get("areas", [])
    curriculum_areas = curriculum.get("areas", [])
    manifest_ids = [x.get("id") for x in manifest_areas]
    curriculum_ids = [x.get("id") for x in curriculum_areas]
    if len(manifest_ids) != len(set(manifest_ids)):
        errors.append("IDs duplicados en manifiesto")
    if set(manifest_ids) != set(curriculum_ids):
        errors.append("Manifiesto y currículo no coinciden")

    results = []
    for area in manifest_areas:
        area_id = area.get("id", "?")
        path = root / "knowledge/deep_modules" / area_id / "RESEARCH_AGENDA.md"
        item_errors = []
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            content = ""
            item_errors.append("agenda inexistente o ilegible")
        if content and not content.startswith("# Agenda de investigación:"):
            item_errors.append("título de agenda inválido")
        lowered = content.casefold()
        for term in REQUIRED_TERMS:
            if term not in lowered:
                item_errors.append("falta concepto requerido: " + term)
        if "research_agenda_defined" not in content:
            item_errors.append("no declara madurez de agenda")
        if "M5" not in content or "reproducción" not in lowered:
            item_errors.append("no define umbral de revisión/reproducción")
        results.append({"id": area_id, "exists": not any("inexistente" in e for e in item_errors), "structurally_complete": not item_errors, "errors": item_errors})

    sources = registry.get("sources", [])
    source_errors = []
    source_ids = [s.get("id") for s in sources]
    if len(source_ids) != len(set(source_ids)):
        source_errors.append("IDs duplicados en registro de fuentes")
    for source in sources:
        for key in ("id", "title", "publisher", "url", "verification_status", "review_note"):
            if not source.get(key):
                source_errors.append(f"fuente sin {key}: {source.get('id', '?')}")
    if "reproducción" not in protocol.casefold() or "amenazas a la validez" not in protocol.casefold():
        errors.append("protocolo de investigación incompleto")
    agenda_count = sum(x["exists"] for x in results)
    complete_count = sum(x["structurally_complete"] for x in results)
    return {
        "ok": not errors and not source_errors and complete_count == len(manifest_areas),
        "area_count": len(manifest_areas),
        "agenda_count": agenda_count,
        "structurally_complete_agendas": complete_count,
        "source_count": len(sources),
        "source_metadata_reviewed": sum("metadata_verified" in s.get("verification_status", "") for s in sources),
        "errors": errors + source_errors,
        "areas": results,
        "limitations": [
            "La auditoría comprueba estructura y metadatos, no calidad semántica ni resultados científicos.",
            "No demuestra que se haya ejecutado una revisión sistemática, experimento o reproducción.",
            "Los metadatos oficiales revisados no equivalen a lectura y verificación integral del documento.",
            "No asigna madurez M4/M5 ni certifica competencia de investigadores o agentes."
        ]
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
        print(f"Agendas existentes: {report['agenda_count']}/{report['area_count']}")
        print(f"Agendas estructuralmente completas: {report['structurally_complete_agendas']}/{report['area_count']}")
        print(f"Fuentes registradas: {report['source_count']} (metadatos oficiales revisados: {report['source_metadata_reviewed']})")
        for error in report["errors"]:
            print("ERROR:", error)
        for limitation in report["limitations"]:
            print("LIMITACIÓN:", limitation)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
