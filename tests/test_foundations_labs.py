import unittest
from knowledge.deep_modules.foundations.labs.runner import (
    lab01_authorization, lab02_asset_reconciliation, lab03_threat_model,
    lab04_identity, lab05_crypto_integrity, lab06_event_reconstruction,
    lab07_assurance, lab08_safety_security_tradeoff, lab09_privacy_confidentiality_gap,
    lab10_resilience_recovery_trust, lab11_common_cause_redundancy, lab12_integrity_vs_truth,
    run_all, encode_hs256_jwt, validate_hs256_jwt,
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
    def test_04_signed_jwt_rejects_invalid_tokens(self):
        r=lab04_identity(); self.assertTrue(r["all_expected"])
        self.assertEqual(r["negative_cases"],10)
        self.assertTrue(r["signature_verified"])
        self.assertFalse(r["outcomes"]["wrong_signature"])
        self.assertFalse(r["outcomes"]["alg_none_rejected"])
        self.assertFalse(r["outcomes"]["unsupported_header_parameter"])
    def test_05_hmac_detects_tampering_and_key_change(self):
        r=lab05_crypto_integrity(); self.assertTrue(r["tamper_rejected"])
        self.assertTrue(r["new_key_verified"]); self.assertIn("no confidentiality",r["scope"])
    def test_06_hmac_audit_chain_detects_tampering_and_reordering(self):
        r=lab06_event_reconstruction(); self.assertTrue(r["chronological"])
        self.assertEqual(r["duplicate_events_removed"],1); self.assertEqual(r["missing_event_ids"],[])
        self.assertTrue(r["hmac_chain_valid"]); self.assertTrue(r["tampering_detected"])
        self.assertTrue(r["reordering_detected"])
    def test_07_assurance_requires_fresh_scoped_evidence(self):
        r=lab07_assurance(); self.assertEqual(r["validly_closed"],["C1"])
        self.assertEqual(set(r["unsubstantiated_not_closed"]),{"C2","C3","C4"})
        self.assertEqual(r["false_closures_prevented"],3)
    def test_10_safety_security_tradeoff_is_explicit(self):
        r=lab08_safety_security_tradeoff(); self.assertTrue(r["joint_requirement_met"])
        self.assertIn("not a hazard analysis",r["warning"])
    def test_11_privacy_is_not_confidentiality(self):
        r=lab09_privacy_confidentiality_gap(); self.assertTrue(r["confidentiality_protected"])
        self.assertTrue(r["privacy_risk_detected"]); self.assertTrue(r["privacy_risk_mitigated_after_design_change"])
    def test_12_recovery_must_restore_trust(self):
        r=lab10_resilience_recovery_trust(); self.assertTrue(r["service_available_after_restore"])
        self.assertFalse(r["trust_restored_before_controls"]); self.assertTrue(r["trust_restored_after_controls"])
    def test_13_common_cause_defeats_nominal_redundancy(self):
        r=lab11_common_cause_redundancy(); self.assertTrue(r["common_cause_detected"])
        self.assertTrue(r["degraded_service_available"])
    def test_14_integrity_does_not_prove_truth(self):
        r=lab12_integrity_vs_truth(); self.assertTrue(r["integrity_and_authenticity"])
        self.assertFalse(r["semantic_validity_before_review"])
        self.assertTrue(r["semantic_validity_after_calibration_and_crosscheck"])
    def test_08_full_suite(self):
        r=run_all(); self.assertTrue(r["synthetic_only"]); self.assertTrue(r["all_checks_passed"])
    def test_09_jwt_rejects_duplicate_json_members(self):
        key=b"foundations-lab-hs256-key-32-bytes!"
        token=encode_hs256_jwt({"iss":"issuer","aud":"api","exp":2000,"scope":"read","jti":"j1"},key)
        head,_,_=token.split(".")
        import base64, hmac, hashlib
        duplicate_payload=base64.urlsafe_b64encode(b'{"iss":"issuer","iss":"evil","aud":"api","exp":2000,"scope":"read","jti":"j1"}').rstrip(b"=").decode()
        signed=f"{head}.{duplicate_payload}"
        signature=base64.urlsafe_b64encode(hmac.new(key,signed.encode(),hashlib.sha256).digest()).rstrip(b"=").decode()
        self.assertFalse(validate_hs256_jwt(f"{signed}.{signature}",key=key,issuer="issuer",audience="api",now=1000,required_scope="read",revoked=set()))

if __name__=="__main__": unittest.main()
