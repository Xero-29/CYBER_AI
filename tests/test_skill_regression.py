import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import skill_regression


class SkillRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dataset = Path(self.temp.name) / "queries.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def write_dataset(self, rows):
        self.dataset.write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )

    def test_metrics_and_skill_history_validation(self):
        self.write_dataset([
            {"id": "case-1", "query": "auditoria cabeceras HTTP", "relevant_skill_ids": ["skill-a"]},
            {"id": "case-2", "query": "revision TLS certificados", "relevant_skill_ids": ["skill-b"]},
        ])
        def search(query, limit, record_usage):
            self.assertFalse(record_usage)
            return [{"skill_id": "skill-a" if "HTTP" in query else "skill-b"}]
        with patch.object(skill_regression.skillbook, "verify_skill_history",
                          side_effect=lambda skill_id: {"valid": True, "status": "active", "current_version": 2}), \
             patch.object(skill_regression.skillbook, "search_skills", side_effect=search):
            report = skill_regression.evaluate(self.dataset, top_k=1)
        self.assertEqual(report["metrics"]["recall_at_k"], 1.0)
        self.assertEqual(report["metrics"]["precision_at_k"], 1.0)
        self.assertEqual(report["metrics"]["mrr_at_k"], 1.0)
        self.assertEqual(report["skill_versions"], {"skill-a": 2, "skill-b": 2})

    def test_invalid_history_fails_closed(self):
        self.write_dataset([
            {"id": "case-1", "query": "auditoria cabeceras HTTP", "relevant_skill_ids": ["skill-a"]}
        ])
        with patch.object(skill_regression.skillbook, "verify_skill_history",
                          return_value={"valid": False, "reason": "history_hash_chain"}):
            with self.assertRaises(skill_regression.SkillRegressionError):
                skill_regression.evaluate(self.dataset)

    def test_duplicate_case_id_is_rejected(self):
        self.write_dataset([
            {"id": "same", "query": "one", "relevant_skill_ids": ["skill-a"]},
            {"id": "same", "query": "two", "relevant_skill_ids": ["skill-a"]},
        ])
        with self.assertRaises(skill_regression.SkillRegressionError):
            skill_regression.load_dataset(self.dataset)

    def test_symlink_dataset_is_rejected(self):
        link = Path(self.temp.name) / "link.jsonl"
        link.symlink_to(self.dataset)
        with self.assertRaises(skill_regression.SkillRegressionError):
            skill_regression.load_dataset(link)

    def test_invalid_threshold_is_rejected(self):
        self.write_dataset([
            {"id": "case-1", "query": "query", "relevant_skill_ids": ["skill-a"]}
        ])
        with patch.object(skill_regression.skillbook, "verify_skill_history",
                          return_value={"valid": True, "status": "active", "current_version": 1}), \
             patch.object(skill_regression.skillbook, "search_skills", return_value=[]):
            report = skill_regression.evaluate(self.dataset)
        self.assertEqual(report["metrics"]["hit_rate_at_k"], 0.0)


if __name__ == "__main__":
    unittest.main()
