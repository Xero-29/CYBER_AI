#!/usr/bin/env python3
"""Evalúa la recuperación semántica con un conjunto JSONL versionado."""
import argparse
import json
import math
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

from knowledge_embeddings import generate_embedding
from knowledge_library import search_knowledge_hybrid

MAX_DATASET_BYTES = 2 * 1024 * 1024
MAX_CASES = 5000
MAX_LINE_BYTES = 64 * 1024

ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "knowledge" / "evaluation" / "domain_queries.jsonl"


def load_dataset(path):
    source = Path(path)
    if source.is_symlink():
        raise ValueError("El dataset debe ser un archivo regular, no un symlink.")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    try:
        descriptor = os.open(source, flags)
    except OSError as error:
        raise ValueError("No se pudo abrir el dataset como archivo regular.") from error

    cases = []
    seen_ids = set()
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("El dataset debe ser un archivo regular, no un symlink.")
        if before.st_size > MAX_DATASET_BYTES:
            raise ValueError("El dataset supera 2 MiB.")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            total_bytes = 0
            for line_number, raw in enumerate(stream, 1):
                total_bytes += len(raw)
                if total_bytes > MAX_DATASET_BYTES:
                    raise ValueError("El dataset supera 2 MiB.")
                if len(raw) > MAX_LINE_BYTES:
                    raise ValueError(f"Línea {line_number} supera 64 KiB.")
                if not raw.strip():
                    continue
                try:
                    item = json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    raise ValueError(f"JSONL inválido en línea {line_number}.") from error
                if not isinstance(item, dict) or set(item) != {
                    "id", "query", "relevant_categories"
                }:
                    raise ValueError(
                        f"Línea {line_number}: se requieren exactamente id, query y relevant_categories."
                    )
                case_id, query, expected = (
                    item["id"], item["query"], item["relevant_categories"]
                )
                if not isinstance(case_id, str) or not case_id.strip() or case_id.strip() in seen_ids:
                    raise ValueError(f"ID ausente o duplicado en línea {line_number}.")
                if not isinstance(query, str) or not query.strip():
                    raise ValueError(f"query inválida en línea {line_number}.")
                if (
                    not isinstance(expected, list) or not expected
                    or any(not isinstance(value, str) or not value.strip() for value in expected)
                    or len({value.strip() for value in expected}) != len(expected)
                ):
                    raise ValueError(f"relevant_categories inválida en línea {line_number}.")
                normalized_case = {
                    "id": case_id.strip(),
                    "query": query.strip(),
                    "relevant_categories": [value.strip() for value in expected],
                }
                try:
                    json.dumps(
                        normalized_case, ensure_ascii=False, separators=(",", ":")
                    ).encode("utf-8")
                except UnicodeEncodeError as error:
                    raise ValueError(
                        f"Línea {line_number} contiene Unicode inválido."
                    ) from error
                seen_ids.add(case_id.strip())
                cases.append(normalized_case)
                if len(cases) > MAX_CASES:
                    raise ValueError("El dataset supera 5000 casos.")
            after = os.fstat(stream.fileno())
            identity_before = (
                before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns,
            )
            identity_after = (
                after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns, after.st_ctime_ns,
            )
            if identity_before != identity_after:
                raise ValueError("El dataset cambió durante su lectura.")
    finally:
        if descriptor is not None:
            os.close(descriptor)

    if not cases:
        raise ValueError("El conjunto de evaluación está vacío.")
    return cases


def _normalize_cases(cases):
    """Validate and normalize in-memory datasets using the same strict schema."""
    if not isinstance(cases, list) or not cases:
        raise ValueError("dataset debe ser una lista no vacía.")
    if len(cases) > MAX_CASES:
        raise ValueError("El dataset supera 5000 casos.")
    normalized = []
    seen_ids = set()
    total_bytes = 0
    for index, item in enumerate(cases, 1):
        if not isinstance(item, dict) or set(item) != {
            "id", "query", "relevant_categories"
        }:
            raise ValueError(
                f"Caso {index}: se requieren exactamente id, query y relevant_categories."
            )
        case_id, query, expected = (
            item["id"], item["query"], item["relevant_categories"]
        )
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError(f"ID inválido en caso {index}.")
        normalized_id = case_id.strip()
        if normalized_id in seen_ids:
            raise ValueError(f"ID duplicado en caso {index}.")
        if not isinstance(query, str) or not query.strip():
            raise ValueError(f"query inválida en caso {index}.")
        if (
            not isinstance(expected, list) or not expected
            or any(not isinstance(value, str) or not value.strip() for value in expected)
            or len({value.strip() for value in expected}) != len(expected)
        ):
            raise ValueError(f"relevant_categories inválida en caso {index}.")
        normalized_case = {
            "id": normalized_id,
            "query": query.strip(),
            "relevant_categories": [value.strip() for value in expected],
        }
        try:
            encoded_case = json.dumps(
                normalized_case, ensure_ascii=False, separators=(",", ":")
            ).encode("utf-8")
        except UnicodeEncodeError as error:
            raise ValueError(f"El caso {index} contiene Unicode inválido.") from error
        line_bytes = len(encoded_case) + 1
        if line_bytes > MAX_LINE_BYTES:
            raise ValueError(f"Caso {index} supera 64 KiB.")
        total_bytes += line_bytes
        if total_bytes > MAX_DATASET_BYTES:
            raise ValueError("El dataset supera 2 MiB.")
        seen_ids.add(normalized_id)
        normalized.append(normalized_case)
    return normalized


def _is_finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def evaluate(dataset, top_k=5, *, embed=generate_embedding, search=search_knowledge_hybrid):
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 50:
        raise ValueError("top_k debe estar entre 1 y 50.")
    cases = (
        load_dataset(dataset)
        if isinstance(dataset, (str, Path))
        else _normalize_cases(dataset)
    )
    details = []
    recalls, precisions, reciprocal_ranks = [], [], []
    for case in cases:
        vector = embed(case["query"], agent_name="ECO")
        if not isinstance(vector, dict):
            raise ValueError("El proveedor de embeddings devolvió una respuesta inválida.")
        embedding = vector.get("embedding")
        embedding_space = vector.get("embedding_space")
        if (
            not isinstance(embedding, (list, tuple))
            or not embedding
            or len(embedding) > 65536
            or any(
                not _is_finite_number(value)
                for value in embedding
            )
            or not isinstance(embedding_space, str)
            or not embedding_space.strip()
        ):
            raise ValueError("El proveedor devolvió un vector o espacio de embeddings inválido.")
        results = search(
            query_text=case["query"],
            query_embedding=embedding,
            embedding_model=embedding_space,
            top_k=top_k,
        )
        if not isinstance(results, list):
            raise ValueError("La búsqueda devolvió una lista de resultados inválida.")
        results = results[:top_k]
        for result in results:
            if not isinstance(result, dict):
                raise ValueError("La búsqueda devolvió un resultado inválido.")
            category = result.get("category")
            if category is not None and not isinstance(category, str):
                raise ValueError("La categoría recuperada debe ser texto.")
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
