import json
import unittest
from pathlib import Path

from knowledge_depth_audit import audit_depth, parse_gap_document


class KnowledgeDepthAuditTests(unittest.TestCase):
    def test_parser_reads_domain_topic_and_section_structure(self):
        content = """# sample_domain

## 1. Topic one

### Purpose
Specific content for the first topic.

### Evidence
Evidence for the first topic.

## 2. Topic two

### Purpose
Different content for the second topic.

### Evidence
Evidence for the second topic.
"""
        parsed = parse_gap_document(content)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(len(parsed[0]["topics"]), 2)
        self.assertIn("Purpose", parsed[0]["topics"][0]["sections"])

    def test_reused_boilerplate_is_reported_and_not_promoted(self):
        report = audit_depth(Path(__file__).resolve().parents[1])
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(report["domain_count"], 48)
        self.assertEqual(report["topic_count"], 192)
        self.assertEqual(report["section_block_count"], 192 * 7)
        self.assertGreater(report["exact_duplicate_section_pairs"], 0)
        self.assertGreater(report["cross_domain_duplicate_section_pairs"], 0)
        self.assertEqual(report["supported_claim_count"], 0)
        self.assertEqual(report["experimental_not_assessed_count"], 192)
        self.assertEqual(report["independent_review_not_started_count"], 192)
        self.assertEqual(report["expert_eligible_count"], 0)
        architecture = report["per_section"]["Arquitectura y modelo de amenazas"]
        self.assertEqual(architecture["max_reuse"], 192)

    def test_word_count_or_structure_does_not_promote_expert_status(self):
        report = audit_depth(Path(__file__).resolve().parents[1])
        self.assertNotEqual(report["status"], "expert_validated")
        self.assertEqual(report["expert_eligible_count"], 0)


if __name__ == "__main__":
    unittest.main()
