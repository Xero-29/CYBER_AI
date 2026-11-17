import unittest
from datetime import datetime, timezone

from knowledge_provenance import audit_catalog


class KnowledgeProvenanceTests(unittest.TestCase):
    NOW = datetime(2026, 11, 16, tzinfo=timezone.utc)

    def resource(self, **overrides):
        item = {
            "id": "nist-sp", "url": "https://csrc.nist.gov/publications/sp",
            "publisher": "csrc.nist.gov", "license_status": "approved",
            "license_evidence": "Reviewed license terms",
            "verified_for_download": True, "download": True,
            "last_reviewed_at": "2026-10-01T00:00:00Z",
            "review_interval_days": 90,
        }
        item.update(overrides)
        return item

    def test_approved_recent_source_is_ready(self):
        report = audit_catalog({"resources": [self.resource()]}, now=self.NOW)
        self.assertEqual(report["status"], "ready")
        self.assertEqual(report["reviewed"], 1)

    def test_pending_license_is_not_counted_as_reviewed(self):
        report = audit_catalog({"resources": [self.resource(
            license_status="pending", verified_for_download=False,
            download=False, license_evidence=None,
        )]}, now=self.NOW)
        self.assertEqual(report["status"], "needs_review")
        self.assertEqual(report["reviewed"], 0)

    def test_expired_review_is_reported_stale(self):
        report = audit_catalog({"resources": [self.resource(
            last_reviewed_at="2025-01-01T00:00:00Z",
            review_interval_days=30,
        )]}, now=self.NOW)
        self.assertEqual(report["stale"], 1)
        self.assertEqual(report["status"], "needs_review")

    def test_download_gate_requires_approved_license_evidence(self):
        report = audit_catalog({"resources": [self.resource(
            license_status="pending", license_evidence=None,
        )]}, now=self.NOW)
        self.assertGreater(report["errors"], 0)
        self.assertIn("unsafe_download_gate", {x["code"] for x in report["issues"]})

    def test_rejects_naive_and_future_review_dates(self):
        for value in ("2026-11-01", "2027-01-01T00:00:00Z"):
            with self.subTest(value=value):
                report = audit_catalog({"resources": [self.resource(
                    last_reviewed_at=value,
                )]}, now=self.NOW)
                self.assertGreater(report["errors"], 0)

    def test_duplicate_ids_are_rejected(self):
        report = audit_catalog({"resources": [self.resource(), self.resource()]}, now=self.NOW)
        self.assertIn("duplicate_id", {x["code"] for x in report["issues"]})

    def test_strict_mode_fails_when_sources_need_review(self):
        report = audit_catalog({"resources": [self.resource(
            license_status="pending", verified_for_download=False,
            download=False, license_evidence=None,
        )]}, now=self.NOW, require_reviewed=True)
        self.assertGreater(report["errors"], 0)

    def test_missing_resources_is_invalid(self):
        self.assertEqual(audit_catalog({})["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
