import unittest

from scan_result_validator import validate_scan_result


class ScanResultValidatorTests(unittest.TestCase):
    def valid_result(self):
        return {
            "target": "https://203.0.113.10",
            "status": "completed",
            "return_code": 0,
            "authorization": {"authorization_id": "grant-1"},
            "findings_count": 1,
            "findings": [{"matched-at": "https://203.0.113.10/login"}],
        }

    def test_accepts_completed_findings_within_authorized_origin(self):
        result = validate_scan_result(self.valid_result())
        self.assertEqual(result["status"], "valid_structure")
        self.assertTrue(result["findings_eligible"])

    def test_rejects_finding_outside_authorized_origin(self):
        data = self.valid_result()
        data["findings"][0]["matched-at"] = "https://attacker.example/login"
        result = validate_scan_result(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("finding_0_outside_authorized_origin", result["errors"])
        self.assertFalse(result["findings_eligible"])

    def test_rejects_count_mismatch(self):
        data = self.valid_result()
        data["findings_count"] = 2
        result = validate_scan_result(data)
        self.assertIn("findings_count_mismatch", result["errors"])

    def test_rejects_missing_authorization_evidence(self):
        data = self.valid_result()
        data.pop("authorization")
        result = validate_scan_result(data)
        self.assertIn("authorization_evidence_missing", result["errors"])

    def test_rejects_non_completed_scan(self):
        data = self.valid_result()
        data["status"] = "timeout"
        result = validate_scan_result(data)
        self.assertIn("scan_not_completed", result["errors"])

    def test_rejects_malformed_jsonl_output(self):
        data = self.valid_result()
        data["malformed_findings_lines"] = 1
        result = validate_scan_result(data)
        self.assertIn("malformed_findings_output", result["errors"])


if __name__ == "__main__":
    unittest.main()
