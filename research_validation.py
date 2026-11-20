#!/usr/bin/env python3
"""Auditoría de trazabilidad y madurez de la investigación de CYBER_AI.

La asociación temática entre dominio y fuente nunca se interpreta como prueba
de que una fuente respalde una afirmación. La herramienta no aprueba claims
automáticamente ni transforma metadatos en lectura integral.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT / "knowledge" / "research"
WORKLIST = RESEARCH / "VALIDATION_WORKLIST_192.json"
CLAIMS = RESEARCH / "CLAIM_EVIDENCE_REGISTER.json"
SOURCE_REGISTER = RESEARCH / "field_studies" / "SOURCE_REGISTER_2026-11-18.json"
DOMAIN_MAP = RESEARCH / "field_studies" / "DOMAIN_SOURCE_MAP.json"
GAP_REGISTER = RESEARCH / "ADVANCED_GAP_REGISTER.json"
CLAIM_STATUSES = {"candidate", "needs_review", "supported", "contradicted", "inconclusive"}
EVIDENCE_TYPES = {"primary_document", "secondary_study", "experiment", "dataset", "expert_review"}
FULL_TEXT_MARKERS = {"full_text_reviewed", "experimentally_validated", "independently_reproduced"}


def _load(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def _parse_date(value):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate_claim_record(claim, source_by_id, task_ids):
    """Devuelve errores; no hace inferencia semántica sobre si la cita respalda."""
    errors = []
    if not isinstance(claim, dict):
        return ["claim_not_object"]
    required = ("claim_id", "task_id", "claim_text", "source_ids", "locator",
                "evidence_excerpt", "evidence_type", "status", "reviewer", "reviewed_at")
    for field in required:
        if claim.get(field) in (None, "", []):
            errors.append("missing_" + field)
    if claim.get("task_id") and claim["task_id"] not in task_ids:
        errors.append("unknown_task_id")
    status = claim.get("status")
    if status not in CLAIM_STATUSES:
        errors.append("invalid_status")
    if claim.get("evidence_type") not in EVIDENCE_TYPES:
        errors.append("invalid_evidence_type")
    source_ids = claim.get("source_ids")
    if not isinstance(source_ids, list) or not source_ids:
        errors.append("source_ids_must_be_nonempty_list")
        source_ids = []
    for source_id in source_ids:
        if source_id not in source_by_id:
            errors.append("unknown_source:" + str(source_id))
    if claim.get("locator") and len(str(claim["locator"]).strip()) < 3:
        errors.append("locator_too_short")
    if claim.get("evidence_excerpt") and len(str(claim["evidence_excerpt"]).strip()) < 20:
        errors.append("evidence_excerpt_too_short")
    reviewed_at = _parse_date(claim.get("reviewed_at"))
    if claim.get("reviewed_at") and reviewed_at is None:
        errors.append("invalid_reviewed_at")
    elif reviewed_at and reviewed_at > datetime.now(timezone.utc):
        errors.append("reviewed_at_in_future")

    if status in {"supported", "contradicted"}:
        if claim.get("evidence_type") == "experiment":
            refs = claim.get("evidence_refs")
            if not isinstance(refs, list) or not refs:
                errors.append("experimental_claim_requires_evidence_refs")
        else:
            if not source_ids or any(
                source_by_id.get(sid, {}).get("verification_status") not in FULL_TEXT_MARKERS
                for sid in source_ids
            ):
                errors.append("claim_source_not_full_text_reviewed")
            if not claim.get("reviewer") or not reviewed_at:
                errors.append("reviewed_claim_requires_reviewer_and_date")
    return errors


def audit_research_assets(worklist=None, claims=None, source_register=None,
                          domain_map=None, gap_register=None):
    worklist = worklist or _load(WORKLIST)
    claims = claims or _load(CLAIMS)
    source_register = source_register or _load(SOURCE_REGISTER)
    domain_map = domain_map or _load(DOMAIN_MAP)
    gap_register = gap_register or _load(GAP_REGISTER)

    errors = []
    sources = source_register.get("sources", [])
    source_by_id = {s.get("id"): s for s in sources if isinstance(s, dict)}
    if len(source_by_id) != len(sources):
        errors.append("duplicate_or_invalid_source_ids")
    tasks = worklist.get("tasks", [])
    task_ids = {t.get("task_id") for t in tasks if isinstance(t, dict)}
    if len(task_ids) != len(tasks):
        errors.append("duplicate_or_invalid_task_ids")

    expected_domains = {d.get("domain_id") for d in gap_register.get("domains", [])}
    mapped_domains = {d.get("area_id"): d for d in domain_map.get("areas", [])}
    if expected_domains != set(mapped_domains):
        errors.append("domain_source_map_mismatch")
    if worklist.get("counts", {}).get("domains") != len(expected_domains):
        errors.append("worklist_domain_count_mismatch")
    if worklist.get("counts", {}).get("tasks") != len(tasks):
        errors.append("worklist_task_count_mismatch")

    expected_task_keys = set()
    unmapped_topics = []
    missing_sources = []
    for domain in gap_register.get("domains", []):
        domain_id = domain.get("domain_id")
        mapped = mapped_domains.get(domain_id, {}).get("source_ids", [])
        for index, topic in enumerate(domain.get("developed_topics", []), 1):
            task_id = f"{domain_id}-{index:02d}"
            expected_task_keys.add(task_id)
            row = next((t for t in tasks if t.get("task_id") == task_id), None)
            if row is None:
                errors.append("missing_task:" + task_id)
                continue
            if row.get("topic") != topic.get("topic") or row.get("anchor") != topic.get("anchor"):
                errors.append("task_topic_mismatch:" + task_id)
            if not row.get("candidate_source_ids"):
                unmapped_topics.append(task_id)
            for source_id in row.get("candidate_source_ids", []):
                if source_id not in source_by_id:
                    missing_sources.append({"task_id": task_id, "source_id": source_id})
                if source_id not in mapped:
                    errors.append("source_not_in_domain_map:" + task_id + ":" + source_id)
    if expected_task_keys != task_ids:
        errors.append("worklist_does_not_match_advanced_gap_register")

    claim_rows = claims.get("claims", [])
    claim_ids = [c.get("claim_id") for c in claim_rows if isinstance(c, dict)]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("duplicate_claim_ids")
    claim_errors = []
    for claim in claim_rows:
        problems = validate_claim_record(claim, source_by_id, task_ids)
        if problems:
            claim_errors.append({"claim_id": claim.get("claim_id", "<unknown>"),
                                 "errors": problems})

    source_status_counts = {}
    full_text_count = 0
    for source in sources:
        status = source.get("verification_status", "unrecorded")
        source_status_counts[status] = source_status_counts.get(status, 0) + 1
        if status in FULL_TEXT_MARKERS:
            full_text_count += 1

    supported = sum(c.get("status") == "supported" and not validate_claim_record(c, source_by_id, task_ids)
                    for c in claim_rows if isinstance(c, dict))
    contradicted = sum(c.get("status") == "contradicted" and not validate_claim_record(c, source_by_id, task_ids)
                       for c in claim_rows if isinstance(c, dict))
    structurally_valid = not errors and not claim_errors and not unmapped_topics and not missing_sources
    return {
        "schema_version": "1.0.0",
        "status": "structurally_valid_needs_research" if structurally_valid else "invalid",
        "structurally_valid": structurally_valid,
        "counts": {
            "domains": len(expected_domains), "tasks": len(tasks),
            "sources": len(sources), "claims": len(claim_rows),
            "claims_supported": supported, "claims_contradicted": contradicted,
            "sources_full_text_reviewed": full_text_count,
            "topics_without_candidate_sources": len(unmapped_topics),
        },
        "source_status_counts": source_status_counts,
        "unmapped_topics": unmapped_topics,
        "missing_sources": missing_sources,
        "structural_errors": errors,
        "claim_errors": claim_errors,
        "limitations": [
            "El mapeo dominio-fuente solo identifica fuentes candidatas.",
            "La herramienta no evalúa semánticamente si una cita respalda una afirmación.",
            "Los estados de página/metadatos revisados no equivalen a lectura integral.",
            "La validación experimental requiere artefactos y resultados reales.",
            "La revisión independiente requiere identidad verificable del revisor y evidencia."
        ]
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emitir informe JSON.")
    parser.add_argument("--strict", action="store_true",
                        help="Fallar si hay afirmaciones pendientes o ninguna afirmación validada.")
    args = parser.parse_args(argv)
    try:
        report = audit_research_assets()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Error al auditar la biblioteca: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        counts = report["counts"]
        print("Auditoría de validación de investigación CYBER_AI")
        print(f"Estado: {report['status']}")
        print(f"Dominios/módulos/fuentes: {counts['domains']}/{counts['tasks']}/{counts['sources']}")
        print(f"Afirmaciones: {counts['claims']} (respaldadas: {counts['claims_supported']}; contradichas: {counts['claims_contradicted']})")
        print(f"Fuentes con lectura integral registrada: {counts['sources_full_text_reviewed']}")
        print(f"Integridad estructural: {'OK' if report['structurally_valid'] else 'ERROR'}")
        for issue in report["structural_errors"] + report["unmapped_topics"]:
            print(f"- {issue}")
        for item in report["claim_errors"]:
            print(f"- {item['claim_id']}: {', '.join(item['errors'])}")
    if not report["structurally_valid"]:
        return 2
    if args.strict and (report["claim_errors"] or report["counts"]["claims_supported"] == 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
