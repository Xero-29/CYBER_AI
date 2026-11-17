"""Evidence-aware global coverage audit; structure is not semantic validation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VALID_STATUSES = {"not_assessed", "in_progress", "partially_validated", "validated", "not_applicable"}


def _load(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def audit(root: Path = ROOT) -> dict:
    errors, warnings = [], []
    try:
        matrix = _load(root, "knowledge/research/global_coverage_matrix.json")
        manifest = _load(root, "knowledge/packs/manifest.json")
        curriculum = _load(root, "knowledge/curricula/domain_curriculum.json")
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "area_count": 0, "reference_count": 0}
    manifest_ids = [x.get("id") for x in manifest.get("areas", [])]
    curriculum_by_id = {x.get("id"): x for x in curriculum.get("areas", [])}
    area_rows = matrix.get("areas", [])
    area_ids = [x.get("id") for x in area_rows]
    refs = matrix.get("references", [])
    ref_ids = [x.get("id") for x in refs]
    if len(manifest_ids) != len(set(manifest_ids)): errors.append("IDs duplicados en manifiesto")
    if len(area_ids) != len(set(area_ids)): errors.append("IDs duplicados en matriz")
    if len(ref_ids) != len(set(ref_ids)): errors.append("IDs duplicados en referencias")
    if set(manifest_ids) != set(area_ids): errors.append("La matriz no coincide exactamente con el manifiesto")
    if set(manifest_ids) != set(curriculum_by_id): errors.append("El currículo no coincide exactamente con el manifiesto")
    known_refs = set(ref_ids)
    for ref in refs:
        for key in ("id", "title", "publisher", "type", "scope", "domains", "verification_status"):
            if not ref.get(key): errors.append(f"Referencia sin {key}: {ref.get('id', '?')}")
        unknown = set(ref.get("domains", [])) - set(manifest_ids)
        if unknown: errors.append(f"{ref.get('id')}: dominios inexistentes {sorted(unknown)}")
    reference_domains = {item["id"]: set(item.get("domains", [])) for item in refs}
    rows = []
    topic_total = artifact_total = topic_assessed = artifact_assessed = gates_assessed = 0
    validated_specialties = 0
    for area in area_rows:
        aid, links = area.get("id", "?"), area.get("reference_ids", [])
        unknown = sorted(set(links) - known_refs)
        if unknown: errors.append(f"{aid}: referencias inexistentes {unknown}")
        inconsistent = sorted(ref_id for ref_id in links if ref_id in reference_domains and aid not in reference_domains[ref_id])
        if inconsistent: errors.append(f"{aid}: mapeo inverso ausente en referencias {inconsistent}")
        if len(links) != len(set(links)): errors.append(f"{aid}: referencias duplicadas")
        if not links: warnings.append(f"{aid}: sin referencias asociadas")
        curriculum_topics = (curriculum_by_id.get(aid) or {}).get("deep_topics", [])
        curriculum_artifacts = (curriculum_by_id.get(aid) or {}).get("required_artifacts", [])
        topics, artifacts, gates = area.get("topic_requirements", []), area.get("artifact_requirements", []), area.get("validation_gates", [])
        topic_names = [x.get("topic") for x in topics]
        artifact_names = [x.get("artifact") for x in artifacts]
        if topic_names != curriculum_topics: errors.append(f"{aid}: requisitos temáticos no coinciden con currículo")
        if artifact_names != curriculum_artifacts: errors.append(f"{aid}: artefactos requeridos no coinciden con currículo")
        for kind, items in (("tema", topics), ("artefacto", artifacts), ("puerta", gates)):
            for item in items:
                status = item.get("status")
                if status not in VALID_STATUSES: errors.append(f"{aid}: estado inválido en {kind}: {status}")
                if status == "validated" and (not item.get("evidence_refs") or not item.get("reviewer") or not item.get("reviewed_at")):
                    errors.append(f"{aid}: {kind} validado sin evidencia/revisor/fecha")
                if status == "validated" and not item.get("evidence_refs"): continue
        topic_total += len(topics); artifact_total += len(artifacts)
        topic_assessed += sum(x.get("status") in {"partially_validated","validated","not_applicable"} for x in topics)
        artifact_assessed += sum(x.get("status") in {"partially_validated","validated","not_applicable"} for x in artifacts)
        gates_assessed += sum(x.get("status") in {"partially_validated","validated","not_applicable"} for x in gates)
        if area.get("specialty_readiness") == "validated": validated_specialties += 1
        rows.append({"id":aid,"reference_count":len(links),"references_exist":not unknown,
          "topic_count":len(topics),"topics_assessed":sum(x.get("status") in {"partially_validated","validated","not_applicable"} for x in topics),
          "artifact_count":len(artifacts),"artifacts_assessed":sum(x.get("status") in {"partially_validated","validated","not_applicable"} for x in artifacts),
          "validation_gates":len(gates),"validation_gates_assessed":sum(x.get("status") in {"partially_validated","validated","not_applicable"} for x in gates),
          "specialty_readiness":area.get("specialty_readiness"),
          "coverage_status":area.get("coverage_status"),"content_depth_status":area.get("content_depth_status"),
          "known_gaps":area.get("known_gaps",[])})
    mapped = sum(x["reference_count"] > 0 for x in rows)
    return {"ok":not errors,"errors":errors,"warnings":warnings,"area_count":len(rows),
      "areas_with_reference_mapping":mapped,"areas_without_reference_mapping":len(rows)-mapped,
      "reference_count":len(refs),"cross_cutting_gap_count":len(matrix.get("cross_cutting_gaps",[])),
      "topic_requirement_count":topic_total,"topics_assessed":topic_assessed,
      "artifact_requirement_count":artifact_total,"artifacts_assessed":artifact_assessed,
      "validation_gate_count":sum(len(x.get("validation_gates",[])) for x in area_rows),
      "validation_gates_assessed":gates_assessed,"validated_specialties":validated_specialties,
      "content_depth_assessed":0,"exhaustive_coverage_claim":False,"areas":rows,
      "limitations":["The curated reference set is not an exhaustive census.",
        "Curriculum-derived requirements are a bounded checklist, not proof that the domain universe is complete.",
        "Assessment status requires evidence, reviewer and date; structure alone never validates content.",
        "Full-text review, legal applicability, operational tool behavior and lab execution require separate evidence.",
        "No total coverage percentage is calculated without a complete weighted universe."]}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    report=audit()
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print(f"Áreas auditadas: {report['area_count']}")
        print(f"Áreas con referencias asociadas: {report['areas_with_reference_mapping']}")
        print(f"Familias de referencia: {report['reference_count']}")
        print(f"Requisitos temáticos: {report['topic_requirement_count']} ({report['topics_assessed']} evaluados)")
        print(f"Artefactos: {report['artifact_requirement_count']} ({report['artifacts_assessed']} evaluados)")
        print(f"Puertas de validación: {report['validation_gate_count']} ({report['validation_gates_assessed']} evaluadas)")
        print(f"Especialidades validadas: {report['validated_specialties']}")
        print("Cobertura exhaustiva demostrada: no")
        for error in report["errors"]: print("ERROR:",error)
    return 0 if report["ok"] else 1


if __name__=="__main__": raise SystemExit(main())
