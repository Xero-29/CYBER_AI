#!/usr/bin/env python3
"""Evalúa la recuperación semántica con un conjunto JSONL versionado."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from knowledge_embeddings import generate_embedding
from knowledge_library import search_knowledge

ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "knowledge" / "evaluation" / "smoke_queries.jsonl"


def load_dataset(path):
    cases = []
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"JSONL inválido en línea {line_number}.") from error
            query = item.get("query") if isinstance(item, dict) else None
            expected = item.get("relevant_categories") if isinstance(item, dict) else None
            if not isinstance(query, str) or not query.strip():
                raise ValueError(f"query inválida en línea {line_number}.")
            if (
                not isinstance(expected, list) or not expected
                or any(not isinstance(value, str) or not value.strip() for value in expected)
            ):
                raise ValueError(f"relevant_categories inválida en línea {line_number}.")
            cases.append({
                "id": str(item.get("id", line_number)),
                "query": query.strip(),
                "relevant_categories": sorted(set(value.strip() for value in expected)),
            })
    if not cases:
        raise ValueError("El conjunto de evaluación está vacío.")
    return cases


def evaluate(dataset, top_k=5, *, embed=generate_embedding, search=search_knowledge):
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 50:
        raise ValueError("top_k debe estar entre 1 y 50.")
    cases = load_dataset(dataset) if isinstance(dataset, (str, Path)) else dataset
    if not isinstance(cases, list) or not cases:
        raise ValueError("dataset debe ser una lista no vacía.")
    details = []
    recalls, precisions, reciprocal_ranks = [], [], []
    for case in cases:
        vector = embed(case["query"], agent_name="ECO")
        results = search(
            query_embedding=vector["embedding"],
            embedding_model=vector["embedding_space"],
            top_k=top_k,
        )
        expected = set(case["relevant_categories"])
        retrieved = [item for item in results if item.get("category") in expected]
        found_categories = {item.get("category") for item in retrieved}
        recall = len(found_categories) / len(expected)
        precision = len(retrieved) / top_k
        first_rank = next(
            (index for index, item in enumerate(results, 1)
             if item.get("category") in expected),
            None,
        )
        reciprocal = 1 / first_rank if first_rank else 0.0
        recalls.append(recall)
        precisions.append(precision)
        reciprocal_ranks.append(reciprocal)
        details.append({
            "id": case.get("id"),
            "query": case["query"],
            "expected_categories": sorted(expected),
            "retrieved_categories": [item.get("category") for item in results],
            "recall_at_k": round(recall, 4),
            "precision_at_k": round(precision, 4),
            "reciprocal_rank": round(reciprocal, 4),
            "hit": first_rank is not None,
        })
    count = len(details)
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "top_k": top_k,
        "queries": count,
        "recall_at_k": round(sum(recalls) / count, 4),
        "precision_at_k": round(sum(precisions) / count, 4),
        "mrr_at_k": round(sum(reciprocal_ranks) / count, 4),
        "no_hit_queries": sum(not item["hit"] for item in details),
        "results": details,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", help="Ruta JSON para conservar el informe.")
    args = parser.parse_args()
    report = evaluate(args.dataset, args.top_k)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered + "\n", encoding="utf-8")
        print(f"Informe: {destination}")
    print(
        f"Consultas: {report['queries']} | Recall@{args.top_k}: "
        f"{report['recall_at_k']:.3f} | Precision@{args.top_k}: "
        f"{report['precision_at_k']:.3f} | MRR@{args.top_k}: "
        f"{report['mrr_at_k']:.3f} | Sin resultados relevantes: "
        f"{report['no_hit_queries']}"
    )


if __name__ == "__main__":
    main()
