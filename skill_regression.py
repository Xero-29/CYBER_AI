#!/usr/bin/env python3
"""Benchmark determinista de recuperación de Skills sin alterar sus contadores de uso."""
import argparse
import json
import math
import sys
from pathlib import Path

import skillbook

MAX_DATASET_BYTES = 2 * 1024 * 1024
MAX_CASES = 5000
MAX_LINE_BYTES = 64 * 1024


class SkillRegressionError(ValueError):
    """Dataset o umbral de regresión inválido."""


def load_dataset(path):
    source = Path(path)
    if source.is_symlink() or not source.is_file():
        raise SkillRegressionError("El dataset debe ser un archivo regular, no un symlink.")
    if source.stat().st_size > MAX_DATASET_BYTES:
        raise SkillRegressionError("El dataset supera 2 MiB.")
    cases = []
    seen = set()
    with source.open("rb") as stream:
        for line_number, raw in enumerate(stream, 1):
            if len(raw) > MAX_LINE_BYTES:
                raise SkillRegressionError(f"Línea {line_number} supera 64 KiB.")
            if not raw.strip():
                continue
            try:
                item = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise SkillRegressionError(f"JSON inválido en línea {line_number}.") from error
            if not isinstance(item, dict) or set(item) != {"id", "query", "relevant_skill_ids"}:
                raise SkillRegressionError(
                    f"Línea {line_number}: se requieren exactamente id, query y relevant_skill_ids."
                )
            case_id, query, relevant = item["id"], item["query"], item["relevant_skill_ids"]
            if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
                raise SkillRegressionError(f"ID ausente o duplicado en línea {line_number}.")
            if not isinstance(query, str) or not query.strip():
                raise SkillRegressionError(f"Consulta vacía en línea {line_number}.")
            if (
                not isinstance(relevant, list) or not relevant
                or any(not isinstance(value, str) or not value.strip() for value in relevant)
                or len(set(relevant)) != len(relevant)
            ):
                raise SkillRegressionError(
                    f"relevant_skill_ids debe ser una lista no vacía y sin duplicados (línea {line_number})."
                )
            seen.add(case_id)
            cases.append({
                "id": case_id, "query": query.strip(),
                "relevant_skill_ids": relevant,
            })
            if len(cases) > MAX_CASES:
                raise SkillRegressionError("El dataset supera 5000 casos.")
    if not cases:
        raise SkillRegressionError("El dataset no contiene casos.")
    return cases


def evaluate(dataset, *, top_k=5):
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 5:
        raise SkillRegressionError("top_k debe estar entre 1 y 5.")
    cases = load_dataset(dataset)
    expected_ids = sorted({
        skill_id for case in cases for skill_id in case["relevant_skill_ids"]
    })
    history = {}
    for skill_id in expected_ids:
        result = skillbook.verify_skill_history(skill_id)
        if not result.get("valid") or result.get("status") != "active":
            raise SkillRegressionError(
                f"Skill relevante ausente, inactiva o con historial inválido: {skill_id}."
            )
        history[skill_id] = result["current_version"]

    results = []
    reciprocal_ranks = []
    precisions = []
    recalls = []
    for case in cases:
        matches = skillbook.search_skills(
            case["query"], limit=top_k, record_usage=False
        )
        returned = [item["skill_id"] for item in matches]
        relevant = set(case["relevant_skill_ids"])
        hits = [index for index, skill_id in enumerate(returned, 1) if skill_id in relevant]
        recall = len(set(returned) & relevant) / len(relevant)
        precision = len(hits) / top_k
        reciprocal_rank = 1 / hits[0] if hits else 0.0
        recalls.append(recall)
        precisions.append(precision)
        reciprocal_ranks.append(reciprocal_rank)
        results.append({
            "id": case["id"], "returned_skill_ids": returned,
            "relevant_found": sorted(set(returned) & relevant),
            "recall": round(recall, 6), "precision_at_k": round(precision, 6),
            "reciprocal_rank": round(reciprocal_rank, 6),
            "passed": bool(hits),
        })
    count = len(cases)
    return {
        "schema": "cyber-ai-skill-regression-v1",
        "cases": count,
        "top_k": top_k,
        "skill_versions": history,
        "metrics": {
            "recall_at_k": round(sum(recalls) / count, 6),
            "precision_at_k": round(sum(precisions) / count, 6),
            "mrr_at_k": round(sum(reciprocal_ranks) / count, 6),
            "hit_rate_at_k": round(sum(bool(x) for x in reciprocal_ranks) / count, 6),
        },
        "case_results": results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--min-recall", type=float, default=0.80)
    parser.add_argument("--min-mrr", type=float, default=0.70)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        for name, value in (("min-recall", args.min_recall), ("min-mrr", args.min_mrr)):
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise SkillRegressionError(f"--{name} debe estar entre 0 y 1.")
        report = evaluate(args.dataset, top_k=args.top_k)
        report["thresholds"] = {
            "min_recall_at_k": args.min_recall, "min_mrr_at_k": args.min_mrr,
        }
        passed = (
            report["metrics"]["recall_at_k"] >= args.min_recall
            and report["metrics"]["mrr_at_k"] >= args.min_mrr
        )
        report["passed"] = passed
        serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            if args.output.is_symlink():
                raise SkillRegressionError("No se permite escribir el informe sobre un symlink.")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.output.with_name(args.output.name + ".tmp")
            if temporary.is_symlink():
                raise SkillRegressionError("El temporal de salida no puede ser un symlink.")
            temporary.write_text(serialized, encoding="utf-8")
            temporary.replace(args.output)
        else:
            print(serialized, end="")
        return 0 if passed else 1
    except (OSError, SkillRegressionError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
