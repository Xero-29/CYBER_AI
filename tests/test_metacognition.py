import json
import tempfile
import unittest
from pathlib import Path

from metacognition import (
    extract_json_object, validate_assessment, run_cycle, load_competency_map,
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
                               model_call=model, publisher=lambda report, task_id: {"indexed": True}, state_path=Path(tmp) / "state.json",
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
                state_path=state_path, log_path=log_path)
            state = load_competency_map(state_path)
        self.assertEqual(result["status"], "knowledge_acquired_needs_task_execution")
        self.assertEqual(state["competencies"]["tcp congestion control"]["status"], "known")
        self.assertNotEqual(state["competencies"]["tcp congestion control"]["status"], "mastered")

    def test_researcher_backend_is_replaceable(self):
        seen = []
        backend = ModelBackend("local", "small-model", lambda prompt: seen.append(prompt) or "informe")
        result = ResearcherAgent(backend).investigate("Analizar DNS", {"gaps": ["DNSSEC"]})
        self.assertEqual(result["status"], "pending_independent_verification")
        self.assertFalse(result["self_verified"])
        self.assertTrue(seen)


if __name__ == "__main__":
    unittest.main()
