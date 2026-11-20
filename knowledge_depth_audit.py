from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOC = Path("knowledge/research/ADVANCED_GAP_DEVELOPMENT.md")
WORKLIST = Path("knowledge/research/VALIDATION_WORKLIST_192.json")
CLAIMS = Path("knowledge/research/CLAIM_EVIDENCE_REGISTER.json")
REGISTER = Path("knowledge/research/ADVANCED_GAP_REGISTER.json")


def _normalise(value: str) -> str:
    tokens = re.findall(r"[a-z0-9áéíóúñ_]{3,}", value.casefold())
    return " ".join(tokens)


def parse_gap_document(content: str) -> list[dict]:
    domains: list[dict] = []
    domain = None
    topic = None
    section = None
    section_lines: list[str] = []

    def flush_section() -> None:
        nonlocal section_lines
        if domain is not None and topic is not None and section:
            text = " ".join(section_lines).strip()
            if text:
                topic["sections"][section] = text
        section_lines = []

    def flush_topic() -> None:
        nonlocal topic, section
        flush_section()
        if domain is not None and topic is not None:
            domain["topics"].append(topic)
        topic = None
        section = None

    for line in content.splitlines():
        match = re.fullmatch(r"# ([a-z0-9_]+)\s*", line)
        if match:
            flush_topic()
            domain = {"domain_id": match.group(1), "topics": []}
            domains.append(domain)
            continue

        match = re.match(r"## \d+\.\s+(.+)$", line)
        if match:
            flush_topic()
            topic = {"title": match.group(1).strip(), "sections": {}}
            continue

        match = re.match(r"###\s+(.+)$", line)
        if match:
            flush_section()
            section = match.group(1).strip()
            continue

        if topic is not None and section is not None:
            section_lines.append(line)

    flush_topic()
    return domains


def audit_depth(root: Path = ROOT) -> dict:
    try:
        document = (root / DOC).read_text(encoding="utf-8")
        worklist = json.loads((root / WORKLIST).read_text(encoding="utf-8"))
        claims = json.loads((root / CLAIMS).read_text(encoding="utf-8"))
        register = json.loads((root / REGISTER).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "expert_eligible_count": 0}

    domains = parse_gap_document(document)
    topic_records = []
    section_entries: dict[str, list[dict]] = defaultdict(list)
    errors = []

    for domain in domains:
        for topic in domain["topics"]:
            record = {
                "domain_id": domain["domain_id"],
                "topic": topic["title"],
                "sections": topic["sections"],
            }
            topic_records.append(record)
            for heading, text in topic["sections"].items():
                normalised = _normalise(text)
                if normalised:
                    section_entries[heading].append({
                        "domain_id": domain["domain_id"],
                        "topic": topic["title"],
                        "normalised": normalised,
                    })

    per_section = {}
    exact_duplicate_pairs = 0
    cross_domain_duplicate_pairs = 0
    reused_section_blocks = 0
    unique_variants_total = 0

    for heading, entries in sorted(section_entries.items()):
        groups: dict[str, list[dict]] = defaultdict(list)
        for entry in entries:
            groups[entry["normalised"]].append(entry)

        heading_pairs = 0
        heading_cross_domain_pairs = 0
        heading_reused_blocks = 0
        for group in groups.values():
            count = len(group)
            if count > 1:
                heading_pairs += count * (count - 1) // 2
                heading_reused_blocks += count
                by_domain = Counter(item["domain_id"] for item in group)
                within_domain_pairs = sum(n * (n - 1) // 2 for n in by_domain.values())
                heading_cross_domain_pairs += count * (count - 1) // 2 - within_domain_pairs

        unique_variants = len(groups)
        unique_variants_total += unique_variants
        exact_duplicate_pairs += heading_pairs
        cross_domain_duplicate_pairs += heading_cross_domain_pairs
        reused_section_blocks += heading_reused_blocks
        per_section[heading] = {
            "section_blocks": len(entries),
            "unique_variants": unique_variants,
            "reused_blocks": heading_reused_blocks,
            "exact_duplicate_pairs": heading_pairs,
            "cross_domain_duplicate_pairs": heading_cross_domain_pairs,
            "max_reuse": max((len(group) for group in groups.values()), default=0),
        }

    tasks = worklist.get("tasks", [])
    claim_items = claims.get("claims", [])
    supported_claims = [
        claim for claim in claim_items
        if claim.get("status") == "supported"
    ]
    experiments_not_assessed = sum(
        task.get("experimental_status") == "not_assessed" for task in tasks
    )
    independent_not_started = sum(
        task.get("independent_review_status") == "not_started" for task in tasks
    )
    full_text_pending = sum(
        task.get("source_review_status") != "full_text_reviewed" for task in tasks
    )

    expected_topics = sum(
        len(domain.get("developed_topics", []))
        for domain in register.get("domains", [])
    )
    parsed_topics = len(topic_records)
    section_blocks = sum(len(item["sections"]) for item in topic_records)
    if len(domains) != 48:
        errors.append(f"expected 48 domains, found {len(domains)}")
    if parsed_topics != 192 or expected_topics != 192:
        errors.append(
            f"expected 192 topics, parsed {parsed_topics}, register {expected_topics}"
        )
    if section_blocks != 192 * 7:
        errors.append(f"expected 1344 section blocks, found {section_blocks}")
    if len(tasks) != 192:
        errors.append(f"expected 192 validation tasks, found {len(tasks)}")

    # A gap is not expert-eligible merely because it has headings or word count.
    # Promotion requires validated claims, reviewed sources, assessed experiments,
    # and independent review; none can be inferred from the draft register.
    expert_eligible = 0
    return {
        "ok": not errors,
        "errors": errors,
        "status": (
            "initial_drafts_with_reused_boilerplate_not_expert_validated"
            if exact_duplicate_pairs
            else "initial_drafts_not_expert_validated"
        ),
        "domain_count": len(domains),
        "topic_count": parsed_topics,
        "validation_task_count": len(tasks),
        "section_block_count": section_blocks,
        "unique_section_variants_total": unique_variants_total,
        "reused_section_blocks": reused_section_blocks,
        "exact_duplicate_section_pairs": exact_duplicate_pairs,
        "cross_domain_duplicate_section_pairs": cross_domain_duplicate_pairs,
        "per_section": per_section,
        "supported_claim_count": len(supported_claims),
        "experimental_not_assessed_count": experiments_not_assessed,
        "independent_review_not_started_count": independent_not_started,
        "full_text_review_pending_count": full_text_pending,
        "expert_eligible_count": expert_eligible,
        "policy": (
            "Structural presence and word count are not expert evidence. "
            "Promotion requires claim-to-source traceability, full-text review, "
            "appropriate experiments, and independent review."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita la especificidad y la evidencia de las 192 brechas avanzadas."
    )
    parser.add_argument("--output", type=Path, help="Ruta opcional para guardar el informe JSON.")
    parser.add_argument(
        "--require-expert",
        action="store_true",
        help="Falla si las 192 brechas no cumplen criterios de aceptación experta.",
    )
    args = parser.parse_args()
    report = audit_depth()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print("Auditoría de profundidad de las 192 brechas")
    print(f"Dominios/temas/tareas: {report.get('domain_count', 0)}/{report.get('topic_count', 0)}/{report.get('validation_task_count', 0)}")
    print(f"Bloques de sección: {report.get('section_block_count', 0)}")
    print(f"Variantes únicas por sección: {report.get('unique_section_variants_total', 0)}")
    print(f"Bloques reutilizados: {report.get('reused_section_blocks', 0)}")
    print(f"Pares de duplicación exacta: {report.get('exact_duplicate_section_pairs', 0)}")
    print(f"Pares duplicados entre dominios: {report.get('cross_domain_duplicate_section_pairs', 0)}")
    print(f"Claims respaldados: {report.get('supported_claim_count', 0)}")
    print(f"Experimentos no evaluados: {report.get('experimental_not_assessed_count', 0)}")
    print(f"Revisiones independientes no iniciadas: {report.get('independent_review_not_started_count', 0)}")
    print(f"Fuentes pendientes de lectura integral: {report.get('full_text_review_pending_count', 0)}")
    print(f"Brechas elegibles como expertas: {report.get('expert_eligible_count', 0)}")
    print(f"Estado: {report.get('status', 'error')}")
    for heading, metrics in report.get("per_section", {}).items():
        print(
            f"- {heading}: {metrics['unique_variants']} variantes, "
            f"máxima reutilización {metrics['max_reuse']}, "
            f"pares duplicados {metrics['exact_duplicate_pairs']}"
        )
    for error in report.get("errors", []):
        print(f"ERROR: {error}", file=sys.stderr)

    if not report.get("ok"):
        return 1
    if args.require_expert and report.get("expert_eligible_count") != 192:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
