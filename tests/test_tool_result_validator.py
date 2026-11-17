import unittest

from tool_result_validator import validate_tool_evidence


class ToolResultValidatorTests(unittest.TestCase):
    def setUp(self):
        self.evidence = {
            "status": "completed", "return_code": 0,
            "tool_reported_success": True, "target_modified": False,
            "tool_binary_modified": False, "target_sha256": "a" * 64,
            "target_sha256_after": "a" * 64,
            "tool_binary_sha256": "b" * 64,
            "tool_binary_sha256_after": "b" * 64,
            "tool_allowlist": {"enforced": True},
            "output_truncated": False,
        }

    def test_accepts_integrity_preserved_allowlisted_execution(self):
        result = validate_tool_evidence(self.evidence)
        self.assertEqual(result["status"], "valid_integrity")
        self.assertTrue(result["findings_eligible"])

    def test_rejects_changed_target(self):
        changed = dict(self.evidence, target_modified=True)
        result = validate_tool_evidence(changed)
        self.assertEqual(result["status"], "rejected")
        self.assertFalse(result["findings_eligible"])
        self.assertIn("target_integrity_not_preserved", result["errors"])

    def test_rejects_missing_allowlist_and_truncated_output(self):
        changed = dict(self.evidence, tool_allowlist={"enforced": False}, output_truncated=True)
        result = validate_tool_evidence(changed)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("signed_allowlist_not_enforced", result["errors"])
        self.assertIn("output_truncated_or_unknown", result["errors"])

    def test_rejects_invalid_hash(self):
        changed = dict(self.evidence, target_sha256="invalid")
        result = validate_tool_evidence(changed)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("target_sha256_invalid", result["errors"])


if __name__ == "__main__":
    unittest.main()
