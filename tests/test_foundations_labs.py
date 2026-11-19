import unittest
from knowledge.deep_modules.foundations.labs.runner import (
    lab01_authorization, lab02_asset_reconciliation, lab03_threat_model,
    lab04_identity, lab05_crypto_integrity, lab06_event_reconstruction,
    lab07_assurance, run_all,
)

class FoundationsLabTests(unittest.TestCase):
    def test_01_revocation_invalidates_cached_authorization(self):
        r=lab01_authorization(); self.assertTrue(r["initial_allow"])
        self.assertTrue(r["revoked_access_denied"]); self.assertTrue(r["unknown_action_denied"])
    def test_02_stable_asset_id_reduces_false_merges(self):
        r=lab02_asset_reconciliation(); self.assertEqual(r["records"],500)
        self.assertEqual(r["stable_resource_id"]["fp"],0)
        self.assertGreater(r["hostname_baseline"]["fp"],0)
        self.assertEqual(r,lab02_asset_reconciliation())
    def test_03_threat_model_covers_required_paths(self):
        r=lab03_threat_model(); self.assertEqual(r["paths_found"],r["required_paths"])
        self.assertIn("not proof of exploitability",r["warning"])
    def test_04_identity_rejects_invalid_claims(self):
        r=lab04_identity(); self.assertTrue(r["all_expected"]); self.assertEqual(r["negative_cases"],5)
    def test_05_hmac_detects_tampering_and_key_change(self):
        r=lab05_crypto_integrity(); self.assertTrue(r["tamper_rejected"])
        self.assertTrue(r["new_key_verified"]); self.assertIn("no confidentiality",r["scope"])
    def test_06_timeline_is_sorted_and_deduplicated(self):
        r=lab06_event_reconstruction(); self.assertTrue(r["chronological"])
        self.assertEqual(r["duplicate_events_removed"],1); self.assertEqual(r["missing_event_ids"],[])
    def test_07_stale_or_missing_evidence_does_not_close_control(self):
        r=lab07_assurance(); self.assertEqual(r["validly_closed"],["C1"])
        self.assertEqual(set(r["unsubstantiated_not_closed"]),{"C2","C3","C4"})
    def test_full_suite(self):
        r=run_all(); self.assertTrue(r["synthetic_only"]); self.assertTrue(r["all_checks_passed"])

if __name__=="__main__": unittest.main()
