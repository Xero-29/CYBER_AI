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
            path.write_text('{"query":""}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "query inválida"):
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
        self.assertEqual(result["recall_at_k"], 0.5)
        self.assertEqual(result["precision_at_k"], 0.25)
        self.assertEqual(result["mrr_at_k"], 0.25)
        self.assertEqual(result["no_hit_queries"], 1)

    def test_invalid_top_k_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "top_k"):
            knowledge_eval.evaluate([{}], 0)


if __name__ == "__main__":
    unittest.main()
