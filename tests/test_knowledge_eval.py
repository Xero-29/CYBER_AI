import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import knowledge_eval


class KnowledgeEvaluationTests(unittest.TestCase):
    def test_loads_jsonl_and_rejects_invalid_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.jsonl"
            path.write_text(json.dumps({
                "id": "one", "query": "consulta",
                "relevant_categories": ["cybersecurity:api"],
            }) + "\n", encoding="utf-8")
            self.assertEqual(len(knowledge_eval.load_dataset(path)), 1)
            path.write_text(json.dumps({
                "id": "invalid", "query": "",
                "relevant_categories": ["cybersecurity:api"],
            }) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "query inválida"):
                knowledge_eval.load_dataset(path)

    def test_rejects_duplicate_case_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.jsonl"
            row = {"id": "same", "query": "api", "relevant_categories": ["api"]}
            path.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicado"):
                knowledge_eval.load_dataset(path)

    def test_rejects_duplicates_after_normalization(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.jsonl"
            first = {
                "id": "case", "query": "api",
                "relevant_categories": ["cybersecurity:api"],
            }
            second = {
                "id": " case ", "query": "api",
                "relevant_categories": ["cybersecurity:api"],
            }
            path.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicado"):
                knowledge_eval.load_dataset(path)

    def test_rejects_symlink_dataset(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.jsonl"
            link = Path(temp) / "link.jsonl"
            path.write_text(json.dumps({
                "id": "one", "query": "api",
                "relevant_categories": ["api"],
            }) + "\n", encoding="utf-8")
            link.symlink_to(path)
            with self.assertRaisesRegex(ValueError, "symlink"):
                knowledge_eval.load_dataset(link)

    def test_rejects_unknown_dataset_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.jsonl"
            path.write_text(json.dumps({
                "id": "one", "query": "api",
                "relevant_categories": ["api"], "untrusted": True,
            }) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exactamente"):
                knowledge_eval.load_dataset(path)

    def test_rejects_oversized_dataset(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.jsonl"
            path.write_bytes(b" " * (knowledge_eval.MAX_DATASET_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "2 MiB"):
                knowledge_eval.load_dataset(path)

    def test_metrics_measure_hits_and_ranking(self):
        cases = [
            {"id": "one", "query": "api", "relevant_categories": ["api"]},
            {"id": "two", "query": "soc", "relevant_categories": ["soc"]},
        ]
        embed = Mock(return_value={
            "embedding": [1.0, 0.0], "embedding_space": "test-space",
        })
        search = Mock(side_effect=[
            [{"category": "other"}, {"category": "api"}],
            [{"category": "other"}],
        ])
        result = knowledge_eval.evaluate(cases, 2, embed=embed, search=search)
        self.assertEqual(result["queries"], 2)
        self.assertEqual(search.call_args.kwargs["query_text"], "soc")
        self.assertEqual(result["recall_at_k"], 0.5)
        self.assertEqual(result["precision_at_k"], 0.25)
        self.assertEqual(result["mrr_at_k"], 0.25)
        self.assertEqual(result["no_hit_queries"], 1)

    def test_evaluate_validates_in_memory_cases_before_provider_call(self):
        embed = Mock()
        search = Mock()
        invalid = [{
            "id": "case", "query": "api",
            "relevant_categories": ["api"], "unexpected": True,
        }]
        with self.assertRaisesRegex(ValueError, "exactamente"):
            knowledge_eval.evaluate(invalid, 1, embed=embed, search=search)
        embed.assert_not_called()
        search.assert_not_called()

    def test_evaluate_rejects_non_finite_embedding_before_search(self):
        cases = [{
            "id": "case", "query": "api",
            "relevant_categories": ["api"],
        }]
        for invalid_value in (float("nan"), float("inf"), 10 ** 1000, True):
            with self.subTest(value_type=type(invalid_value).__name__):
                embed = Mock(return_value={
                    "embedding": [invalid_value], "embedding_space": "test-space",
                })
                search = Mock()
                with self.assertRaisesRegex(ValueError, "vector o espacio"):
                    knowledge_eval.evaluate(cases, 1, embed=embed, search=search)
                search.assert_not_called()

    def test_evaluate_rejects_malformed_search_results(self):
        cases = [{
            "id": "case", "query": "api",
            "relevant_categories": ["api"],
        }]
        embed = Mock(return_value={
            "embedding": [1.0], "embedding_space": "test-space",
        })
        search = Mock(return_value={"category": "api"})
        with self.assertRaisesRegex(ValueError, "lista de resultados"):
            knowledge_eval.evaluate(cases, 1, embed=embed, search=search)

    def test_default_domain_dataset_covers_all_48_manifest_areas(self):
        manifest = json.loads((knowledge_eval.ROOT / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
        cases = knowledge_eval.load_dataset(knowledge_eval.DEFAULT_DATASET)
        expected = {f"cybersecurity:{area['id']}" for area in manifest["areas"]}
        actual = {category for case in cases for category in case["relevant_categories"]}
        self.assertEqual(len(cases), 48)
        self.assertEqual(actual, expected)
        self.assertEqual(len({case["id"] for case in cases}), 48)

    def test_invalid_top_k_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "top_k"):
            knowledge_eval.evaluate([{}], 0)


if __name__ == "__main__":
    unittest.main()
