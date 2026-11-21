import json
import tempfile
import unittest
from pathlib import Path

from metacognition import (
    extract_json_object, validate_assessment, validate_verification, run_cycle,
    load_competency_map, append_event, MetacognitionError,
)
from researcher_agent import ModelBackend, ResearcherAgent


class MetacognitionTests(unittest.TestCase):
    def test_extract_json_from_wrapped_response(self):
        self.assertEqual(extract_json_object('respuesta: {"ok": true} fin'), {"ok": True})

    def test_invalid_confidence_rejected(self):
        with self.assertRaises(ValueError):
            validate_assessment({"knowledge_sufficient": True, "confidence": 1.5, "gaps": []})

    def test_critical_gap_overrides_claimed_sufficiency(self):
        value = validate_assessment({
            "knowledge_sufficient": True, "confidence": 0.9,
            "gaps": [{"topic": "criptografía", "priority": 5, "prerequisites": []}],
        })
        self.assertFalse(value["knowledge_sufficient"])

    def test_sufficient_knowledge_skips_research(self):
        calls = []
        def model(agent, prompt):
            calls.append(agent)
            return json.dumps({
                "knowledge_sufficient": True, "confidence": 0.92,
                "known_topics": ["redes"], "gaps": [], "uncertainties": [],
            })
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cycle("Explicar TCP", principal="MAIN", researcher="R", verifier="V",
                               model_call=model, publisher=lambda report, task_id: {"indexed": True}, source_researcher=lambda task, assessment: {
                                   "status": "ok", "verified_sources": 1,
                                   "report": "test evidence from a reviewed source",
                               }, state_path=Path(tmp) / "state.json",
                               log_path=Path(tmp) / "events.jsonl")
        self.assertEqual(result["status"], "sufficient")
        self.assertEqual(calls, ["MAIN"])

    def test_research_must_be_independently_verified_and_reassessed(self):
        calls = []
        def model(agent, prompt):
            calls.append(agent)
            if agent == "MAIN" and len([x for x in calls if x == "MAIN"]) == 1:
                return json.dumps({"knowledge_sufficient": False, "confidence": 0.3,
                    "gaps": [{"topic": "TCP congestion control", "why": "missing",
                              "prerequisites": ["TCP"], "priority": 4}]})
            if agent == "RESEARCHER":
                return "Informe con fuentes identificadas y limitaciones."
            if agent == "VERIFIER":
                return json.dumps({"approved": True, "score": 85,
                                   "evidence_quality": "good", "gaps_remaining": [], "reasons": []})
            return json.dumps({"knowledge_sufficient": True, "confidence": 0.8, "gaps": []})
        with tempfile.TemporaryDirectory() as tmp:
            state_path, log_path = Path(tmp) / "state.json", Path(tmp) / "events.jsonl"
            result = run_cycle("Explicar control de congestión", principal="MAIN",
                researcher="RESEARCHER", verifier="VERIFIER", model_call=model,
                publisher=lambda report, task_id: {"indexed": True},
                source_researcher=lambda task, assessment: {
                    "status": "ok", "verified_sources": 1,
                    "report": "test evidence from a reviewed source",
                },
                state_path=state_path, log_path=log_path)
            state = load_competency_map(state_path)
        self.assertEqual(result["status"], "knowledge_acquired_needs_task_execution")
        self.assertEqual(state["competencies"]["tcp congestion control"]["status"], "known")
        self.assertNotEqual(state["competencies"]["tcp congestion control"]["status"], "mastered")

    def test_index_failure_blocks_claim_of_ready_knowledge(self):
        calls = []
        def model(agent, prompt):
            calls.append(agent)
            if agent == "MAIN" and calls.count("MAIN") == 1:
                return json.dumps({"knowledge_sufficient": False, "confidence": 0.2,
                    "gaps": [{"topic": "DNSSEC", "why": "missing",
                              "prerequisites": ["DNS"], "priority": 4}]})
            if agent == "RESEARCHER":
                return "Informe con fuentes."
            if agent == "VERIFIER":
                return json.dumps({"approved": True, "score": 90, "evidence_quality": "good",
                                   "gaps_remaining": [], "reasons": []})
            return json.dumps({"knowledge_sufficient": True, "confidence": 0.9, "gaps": []})
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cycle(
                "Diseñar validación DNSSEC", principal="MAIN",
                researcher="RESEARCHER", verifier="VERIFIER", model_call=model,
                publisher=lambda report, task_id: {"indexed": False},
                source_researcher=lambda task, assessment: {
                    "status": "ok", "verified_sources": 1,
                    "report": "fuentes revisadas y verificadas",
                },
                state_path=Path(tmp) / "state.json",
                log_path=Path(tmp) / "events.jsonl",
            )
        self.assertEqual(result["status"], "knowledge_acquired_not_indexed")

    def test_low_confidence_cannot_claim_sufficiency(self):
        result = validate_assessment({
            "knowledge_sufficient": True, "confidence": 0.4, "gaps": [],
        })
        self.assertFalse(result["knowledge_sufficient"])

    def test_researcher_backend_is_replaceable(self):
        seen = []
        backend = ModelBackend("local", "small-model", lambda prompt: seen.append(prompt) or "informe")
        result = ResearcherAgent(backend).investigate("Analizar DNS", {"gaps": ["DNSSEC"]})
        self.assertEqual(result["status"], "pending_independent_verification")
        self.assertFalse(result["self_verified"])
        self.assertTrue(seen)

    
    def test_source_evidence_failure_blocks_researcher(self):
        calls = []
        def model(agent, prompt):
            calls.append(agent)
            return json.dumps({
                "knowledge_sufficient": False, "confidence": 0.2,
                "gaps": [{"topic": "DNSSEC", "why": "missing",
                          "prerequisites": ["DNS"], "priority": 4}],
            })
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cycle(
                "Investigar DNSSEC", principal="MAIN", researcher="RESEARCHER",
                verifier="VERIFIER", model_call=model,
                source_researcher=lambda task, assessment: {
                    "status": "unavailable", "verified_sources": 0, "report": "",
                },
                state_path=Path(tmp) / "state.json",
                log_path=Path(tmp) / "events.jsonl",
            )
        self.assertEqual(result["status"], "source_evidence_unavailable")
        self.assertEqual(calls, ["MAIN"])

    def test_verifier_cannot_approve_low_score_or_remaining_gaps(self):
        low = validate_verification({
            "approved": True, "score": 74, "evidence_quality": "good",
            "gaps_remaining": [], "reasons": [],
        })
        incomplete = validate_verification({
            "approved": True, "score": 95, "evidence_quality": "excellent",
            "gaps_remaining": ["DNSSEC validation"], "reasons": [],
        })
        self.assertFalse(low["approved"])
        self.assertFalse(incomplete["approved"])

    def test_assessment_rejects_non_text_prerequisites(self):
        with self.assertRaises(ValueError):
            validate_assessment({
                "knowledge_sufficient": False, "confidence": 0.2,
                "gaps": [{"topic": "DNSSEC", "priority": 4, "prerequisites": [42]}],
            })

    def test_state_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target.json"
            target.write_text(json.dumps({
                "schema_version": 1, "competencies": {}, "updated_at": None,
            }), encoding="utf-8")
            link = root / "state.json"
            link.symlink_to(target)
            with self.assertRaises(MetacognitionError):
                load_competency_map(link)

    def test_research_log_is_private_and_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "events.jsonl"
            secret = "sk-proj-abcdefghijklmnopqrstuvwxyz012345"
            append_event({"status": "test", "api_key": secret}, log)
            stored = log.read_text(encoding="utf-8")
            self.assertNotIn(secret, stored)
            self.assertEqual(log.stat().st_mode & 0o777, 0o600)
            self.assertEqual(root.stat().st_mode & 0o777, 0o700)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            extract_json_object('{"knowledge_sufficient": false, "knowledge_sufficient": true}')


if __name__ == "__main__":
    unittest.main()
