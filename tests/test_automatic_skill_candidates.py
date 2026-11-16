import unittest
from unittest.mock import patch

import skillbook
import team_orchestrator


class AutomaticSkillCandidateTests(unittest.TestCase):
    def test_two_supervised_successes_create_candidate_not_active_skill(self):
        events = [
            {"event_id": "run-1", "task_fingerprint": "a" * 64, "status": "completed",
             "tool": "team_orchestrator", "created_at": "2026-04-01T00:00:00Z",
             "metadata": {"objective_supervision": True}},
            {"event_id": "run-2", "task_fingerprint": "a" * 64, "status": "completed",
             "tool": "team_orchestrator", "created_at": "2026-04-02T00:00:00Z",
             "metadata": {"objective_supervision": True}},
        ]
        class FakeLedger:
            def verify(self): return {"valid": True}
            def history(self, **kwargs): return events
        report = {
            "status": "completed", "workflow": "security_review",
            "objective_contract": {"acceptance_criteria": ["validar hallazgos"]},
            "steps": [
                {"agent": "NEXO", "objective": "inventariar activos"},
                {"agent": "VERITAS", "objective": "revisar evidencia"},
            ],
        }
        workflow = {
            "description": "Revisión defensiva supervisada",
            "steps": [{"agent": "NEXO", "tools": ["ruff"]}],
            "acceptance_criteria": ["validar hallazgos"],
        }
        with patch.object(team_orchestrator, "ExecutionLedger", return_value=FakeLedger()), \
             patch.object(skillbook, "propose_skill_from_ledger",
                          return_value={"status": "candidate"}) as propose:
            result = team_orchestrator._auto_propose_skill_candidate(
                report, workflow, "auditoría defensiva", "shared", "run-2"
            )
        self.assertEqual(result["status"], "candidate")
        kwargs = propose.call_args.kwargs
        self.assertEqual(kwargs["event_ids"], ["run-1", "run-2"])
        self.assertEqual(kwargs["source_urls"], [])
        self.assertEqual(kwargs["tools"], ["ruff"])

    def test_failed_or_unsupervised_history_never_proposes(self):
        events = [
            {"event_id": "run-1", "task_fingerprint": "b" * 64, "status": "completed",
             "tool": "team_orchestrator", "created_at": "2026-05-01T00:00:00Z",
             "metadata": {"objective_supervision": True}},
            {"event_id": "run-2", "task_fingerprint": "b" * 64, "status": "failed",
             "tool": "team_orchestrator", "created_at": "2026-05-02T00:00:00Z",
             "metadata": {"objective_supervision": True}},
        ]
        class FakeLedger:
            def verify(self): return {"valid": True}
            def history(self, **kwargs): return events
        report = {"status": "completed", "objective_contract": {"criteria": ["ok"]},
                  "steps": [{"agent": "A", "objective": "one"},
                            {"agent": "B", "objective": "two"}]}
        with patch.object(team_orchestrator, "ExecutionLedger", return_value=FakeLedger()), \
             patch.object(skillbook, "propose_skill_from_ledger") as propose:
            result = team_orchestrator._auto_propose_skill_candidate(
                report, {"steps": []}, "task", "shared", "run-2"
            )
        self.assertIsNone(result)
        propose.assert_not_called()


if __name__ == "__main__":
    unittest.main()
