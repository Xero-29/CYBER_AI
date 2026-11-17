"""Auditoría estructural de profundidad de la biblioteca; no certifica veracidad técnica."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = {
    "scope": ("## Propósito y límites",),
    "architecture": ("## Arquitectura", "## Superficie", "## Fuentes y riesgos"),
    "competencies": ("## Competencias",),
    "controls": ("## Controles",),
    "methodology": ("## Metodología",),
    "lab": ("## Laboratorio",),
    "evaluation": ("## Evaluación", "## Criterios de evaluación"),
    "agent_policy": ("## Instrucciones para agentes IA",),
}
DEEP = {
    "threat_model": ("## Modelo de amenazas", "## Amenazas", "## Arquitectura y riesgos", "## Superficie y amenazas"),
    "detection": ("## Detección", "## Telemetría", "## Monitorización", "## Monitoreo"),
    "incident_response": ("## Respuesta", "## Investigación", "## Recuperación"),
    "case_studies": ("## Casos", "## Caso práctico", "## Escenarios"),
    "references": ("## Referencias", "## Marcos y herramientas", "## Fuentes"),
}

def has_heading(content: str, alternatives: tuple[str, ...]) -> bool:
    return any(re.search(r"(?im)^" + re.escape(item) + r"(?:\s|$)", content) for item in alternatives)

def audit_library(root: Path = ROOT) -> dict:
    try:
        manifest = json.loads((root / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
        curriculum = json.loads((root / "knowledge/curricula/domain_curriculum.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "area_count": 0, "areas": []}
    ma, ca = manifest.get("areas", []), curriculum.get("areas", [])
    mids, cids = [x.get("id") for x in ma], [x.get("id") for x in ca]
    errors = []
    if len(mids) != len(set(mids)): errors.append("IDs duplicados en manifiesto")
    if set(mids) != set(cids): errors.append("Currículo y manifiesto no coinciden")
    by_id = {x.get("id"): x for x in ca}
    results = []
    for area in ma:
        aid, entry = area.get("id", "?"), by_id.get(area.get("id"))
        item_errors = []
        content = ""
        if not entry:
            item_errors.append("sin currículo")
        else:
            for key in ("scope","learning_levels","deep_topics","required_artifacts","lab_blueprint","evaluation","reference_policy","maturity"):
                if not entry.get(key): item_errors.append("currículo sin " + key)
            if len(entry.get("deep_topics", [])) < 5: item_errors.append("menos de cinco temas técnicos")
            if len(entry.get("required_artifacts", [])) < 6: item_errors.append("artefactos insuficientes")
        try: content = (root / area.get("path", "")).read_text(encoding="utf-8")
        except OSError: item_errors.append("pack inexistente o ilegible")
        base = {k: has_heading(content,v) for k,v in BASE.items()}
        deep = {k: has_heading(content,v) for k,v in DEEP.items()}
        missing = [k for k,v in base.items() if not v]
        missing_deep = [k for k,v in deep.items() if not v]
        if missing: item_errors.append("secciones base ausentes: " + ", ".join(missing))
        results.append({"id":aid,"name":area.get("name"),"base_complete":not item_errors,"deep_section_coverage":sum(deep.values()),"deep_section_total":len(DEEP),"missing_deep_sections":missing_deep,"errors":item_errors,"curriculum_maturity":entry.get("maturity") if entry else "missing"})
    base_complete=sum(x["base_complete"] for x in results)
    deep_complete=sum(x["deep_section_coverage"] == len(DEEP) for x in results)
    return {"ok":not errors and base_complete == len(results),"errors":errors,"area_count":len(results),"base_complete":base_complete,"deep_complete":deep_complete,"deep_section_checks":len(results)*len(DEEP),"deep_section_present":sum(x["deep_section_coverage"] for x in results),"curriculum_defined":len(cids),"areas":results,"limitations":["Mide estructura, no exactitud ni profundidad semántica.","No valida licencias, vigencia ni calidad de fuentes.","No prueba ejecución de laboratorios.","No certifica competencia de agentes o herramientas."]}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json",action="store_true")
    parser.add_argument("--require-deep",action="store_true")
    args=parser.parse_args()
    report=audit_library()
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print(f"Áreas auditadas: {report['area_count']}")
        print(f"Currículos definidos: {report.get('curriculum_defined',0)}")
        print(f"Secciones base completas: {report.get('base_complete',0)}/{report['area_count']}")
        print(f"Secciones profundas completas: {report.get('deep_complete',0)}/{report['area_count']}")
        print(f"Comprobaciones profundas: {report.get('deep_section_present',0)}/{report.get('deep_section_checks',0)}")
        for item in report.get("areas",[]):
            if item["errors"] or item["missing_deep_sections"]: print(f"- {item['id']}: {item['errors']}; faltan={item['missing_deep_sections']}")
        for item in report.get("limitations",[]): print("LIMITACIÓN: "+item)
    if not report["ok"]: return 1
    if args.require_deep and report.get("deep_complete") != report.get("area_count"): return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
