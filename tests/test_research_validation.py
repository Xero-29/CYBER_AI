import unittest
from research_validation import audit_research_assets, validate_claim_record


class ResearchValidationTests(unittest.TestCase):
    def setUp(self):
        self.sources = {
            "nist": {"id": "nist", "verification_status": "official_scope_reviewed"},
            "paper": {"id": "paper", "verification_status": "full_text_reviewed"},
        }
        self.tasks = {"network-01"}

    def valid_claim(self, **overrides):
        claim = {
            "claim_id": "claim-1", "task_id": "network-01",
            "claim_text": "La afirmación técnica bajo evaluación.",
            "source_ids": ["paper"], "locator": "p. 12, sección 3.1",
            "evidence_excerpt": "Texto de evidencia suficientemente extenso para revisión.",
            "evidence_type": "primary_document", "status": "supported",
            "reviewer": "reviewer@example.invalid",
            "reviewed_at": "2026-11-18T12:00:00Z"
        }
        claim.update(overrides)
        return claim

    def test_supported_claim_requires_full_text_review(self):
        errors = validate_claim_record(
            self.valid_claim(source_ids=["nist"]), self.sources, self.tasks
        )
        self.assertIn("claim_source_not_full_text_reviewed", errors)

    def test_supported_claim_requires_exact_locator_and_excerpt(self):
        claim = self.valid_claim(locator="", evidence_excerpt="")
        errors = validate_claim_record(claim, self.sources, self.tasks)
        self.assertIn("missing_locator", errors)
        self.assertIn("missing_evidence_excerpt", errors)

    def test_claim_cannot_reference_unknown_task_or_source(self):
        errors = validate_claim_record(
            self.valid_claim(task_id="unknown", source_ids=["ghost"]),
            self.sources, self.tasks
        )
        self.assertIn("unknown_task_id", errors)
        self.assertIn("unknown_source:ghost", errors)

    def test_experimental_claim_requires_evidence_artifact(self):
        errors = validate_claim_record(
            self.valid_claim(evidence_type="experiment", evidence_refs=[]),
            self.sources, self.tasks
        )
        self.assertIn("experimental_claim_requires_evidence_refs", errors)

    def test_inconclusive_claim_does_not_require_approval(self):
        errors = validate_claim_record(
            self.valid_claim(status="inconclusive", source_ids=["nist"]),
            self.sources, self.tasks
        )
        self.assertEqual(errors, [])

    def test_repository_worklist_is_exactly_192_and_structurally_sound(self):
        report = audit_research_assets()
        self.assertTrue(report["structurally_valid"], report["structural_errors"])
        self.assertEqual(report["counts"]["domains"], 48)
        self.assertEqual(report["counts"]["tasks"], 192)
        self.assertEqual(report["counts"]["sources"], 95)
        self.assertEqual(report["counts"]["claims"], 0)
        self.assertEqual(report["counts"]["claims_supported"], 0)
        self.assertEqual(report["counts"]["sources_full_text_reviewed"], 0)

    def test_no_topic_is_mistaken_for_validated_claim(self):
        report = audit_research_assets()
        self.assertEqual(report["status"], "structurally_valid_needs_research")
        self.assertGreater(report["counts"]["tasks"], 0)
        self.assertEqual(report["counts"]["claims_supported"], 0)


if __name__ == "__main__":
    unittest.main()
