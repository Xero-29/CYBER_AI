import unittest

from knowledge.deep_modules.ai_red_team.lab_runner import (
    _benchmark_integrity,
    _bounded_execution,
    _retrieve_for_tenant,
    _verify_document,
    _tool_allowed,
    _validate_structured_output,
    run_suite,
)


class AIRedTeamSyntheticHarnessTests(unittest.TestCase):
    def test_all_nine_cases_pass_without_model_or_network(self):
        report = run_suite()
        self.assertEqual(report["summary"], {
            "total": 9, "passed": 9, "failed": 0, "all_passed": True
        })
        self.assertFalse(report["model_execution"])
        self.assertFalse(report["network_access"])
        self.assertTrue(report["synthetic_only"])
        self.assertEqual(
            [item["id"] for item in report["results"]],
            [f"ART-{number:02d}" for number in range(1, 10)],
        )

    def test_corpus_integrity_requires_digest_trusted_signer_and_valid_hmac(self):
        import hashlib
        import hmac

        content = b"trusted fixture"
        key = b"synthetic-test-key"
        digest = hashlib.sha256(content).hexdigest()
        signature = hmac.new(key, content, hashlib.sha256).hexdigest()
        keys = {"trusted": key}
        self.assertTrue(_verify_document(content, digest, "trusted", signature, keys))
        self.assertFalse(_verify_document(content + b"tampered", digest, "trusted", signature, keys))
        self.assertFalse(_verify_document(content, digest, "unknown", signature, keys))
        self.assertFalse(_verify_document(content, digest, "trusted", "0" * 64, keys))

    def test_tenant_filter_never_returns_other_tenant(self):
        docs = [
            {"id": "r", "tenant_id": "red"},
            {"id": "b", "tenant_id": "blue"},
        ]
        self.assertEqual(_retrieve_for_tenant("red", docs), [docs[0]])
        self.assertEqual(_retrieve_for_tenant("blue", docs), [docs[1]])

    def test_tool_broker_denies_unknown_tool_cross_owner_and_duplicate(self):
        args = {"resource_id": "CASE-001", "idempotency_key": "idem-1"}
        self.assertTrue(_tool_allowed("analyst", "create_ticket", "u1", "u1", args, set()))
        self.assertFalse(_tool_allowed("analyst", "send_message", "u1", "u1", args, set()))
        self.assertFalse(_tool_allowed("analyst", "create_ticket", "u2", "u1", args, set()))
        self.assertFalse(_tool_allowed("analyst", "create_ticket", "u1", "u1", args, {"idem-1"}))

    def test_structured_output_rejects_extra_fields_and_path_traversal(self):
        self.assertTrue(_validate_structured_output(
            '{"action":"read_record","record_id":"CASE-001"}'
        ))
        self.assertFalse(_validate_structured_output(
            '{"action":"read_record","record_id":"CASE-001","path":"../../etc/passwd"}'
        ))

    def test_budget_is_hard_bounded(self):
        result = _bounded_execution(1000, max_steps=7, max_calls=4, max_tokens=600)
        self.assertLessEqual(result["steps"], 7)
        self.assertLessEqual(result["calls"], 4)
        self.assertLessEqual(result["tokens"], 600)
        self.assertTrue(result["stopped"])


    def test_benchmark_integrity_reports_manifest_and_does_not_claim_validity(self):
        report = _benchmark_integrity()
        self.assertTrue(report["schema_valid"])
        self.assertTrue(report["ids_unique"])
        self.assertTrue(report["split_disjoint"])
        self.assertTrue(report["normalized_text_unique"])
        self.assertTrue(report["near_duplicates_absent"])
        self.assertTrue(report["source_groups_disjoint"])
        self.assertEqual(report["dataset_manifest"]["version"], "1.1.0")
        self.assertEqual(len(report["dataset_manifest"]["sha256"]), 64)
        self.assertEqual(report["statistical_validity"], "NOT_ESTABLISHED")
        self.assertFalse(report["ground_truth_independently_reviewed"])

    def test_benchmark_integrity_detects_within_split_duplicates_and_source_leakage(self):
        train = [
            {"id": "train-1", "text": "A prompt asks for public records",
             "label": "benign", "source_group": "source-shared"},
            {"id": "train-2", "text": "A prompt asks for public records",
             "label": "attack", "source_group": "source-train"},
        ]
        holdout = [
            {"id": "holdout-1", "text": "A prompt asks for public record",
             "label": "benign", "source_group": "source-shared"},
            {"id": "holdout-2", "text": "export confidential customer data",
             "label": "attack", "source_group": "source-holdout"},
        ]
        report = _benchmark_integrity(train, holdout)
        self.assertFalse(report["normalized_text_unique"])
        self.assertFalse(report["near_duplicates_absent"])
        self.assertFalse(report["source_groups_disjoint"])

    def test_benchmark_integrity_rejects_duplicate_ids(self):
        train = [
            {"id": "duplicate", "text": "first unique sample",
             "label": "benign", "source_group": "source-a"},
        ]
        holdout = [
            {"id": "duplicate", "text": "second unique sample",
             "label": "attack", "source_group": "source-b"},
        ]
        self.assertFalse(_benchmark_integrity(train, holdout)["ids_unique"])


if __name__ == "__main__":
    unittest.main()
