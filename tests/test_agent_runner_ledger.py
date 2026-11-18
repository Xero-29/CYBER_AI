import unittest
from types import SimpleNamespace
from unittest.mock import patch

import agent_runner


class FakeLedger:
    def __init__(self, finalized=False):
        self.finalized = finalized
        self.appended = []

    def history(self, *, namespace, limit):
        events = [{
            "sequence": 1,
            "event_id": "start-1",
            "namespace": namespace,
            "task": "[REDACTED PROMPT]",
            "status": "started",
            "tool": "agent_runner",
            "metadata": {"task_id": "task-123"},
        }]
        events.append({
            "sequence": 2,
            "event_id": "start-other",
            "namespace": namespace,
            "task": "[REDACTED PROMPT]",
            "status": "started",
            "tool": "agent_runner",
            "metadata": {"task_id": "other-task"},
        })
        if self.finalized:
            events.append({
                "sequence": 2,
                "event_id": "end-1",
                "namespace": namespace,
                "task": "task under test",
                "status": "failed",
                "tool": "agent_runner",
                "metadata": {"start_event_id": "start-1"},
            })
        return events

    def append(self, **event):
        self.appended.append(event)
        return {"event_id": "end-2", "status": event["status"]}


class AgentRunnerLedgerGuardTests(unittest.TestCase):
    def invoke(self, ledger):
        with (
            patch.object(agent_runner, "_run_agent_impl", side_effect=RuntimeError("provider failed")),
            patch.object(agent_runner, "load_config", return_value={}),
            patch.object(agent_runner, "resolve_agent", return_value=("agent", {"memory": {"namespace": "ns"}})),
            patch.object(agent_runner, "ExecutionLedger", return_value=ledger),
            patch.object(agent_runner.uuid, "uuid4", return_value=SimpleNamespace(hex="task-123")),
        ):
            with self.assertRaisesRegex(RuntimeError, "provider failed"):
                agent_runner.run_agent("agent", "task under test")

    def test_agent_ledger_is_required_by_default_with_explicit_override(self):
        self.assertTrue(agent_runner._ledger_required({}))
        self.assertFalse(agent_runner._ledger_required({
            "CYBER_AI_ALLOW_UNLOGGED_EXECUTION": "1"
        }))
        self.assertTrue(agent_runner._ledger_required({
            "CYBER_AI_ALLOW_UNLOGGED_EXECUTION": "1",
            "CYBER_AI_LEDGER_REQUIRED": "1",
        }))

    def test_ledger_failure_is_fatal_by_default(self):
        with (
            patch.object(agent_runner, "_run_agent_impl", side_effect=RuntimeError("provider failed")),
            patch.object(agent_runner, "load_config", return_value={}),
            patch.object(agent_runner, "resolve_agent", return_value=("agent", {"memory": {"namespace": "ns"}})),
            patch.object(agent_runner, "ExecutionLedger", side_effect=OSError("ledger offline")),
            patch.dict("os.environ", {}, clear=True),
        ):
            with self.assertRaisesRegex(RuntimeError, "no se pudo cerrar su evento"):
                agent_runner.run_agent("agent", "task under test")

    def test_explicit_unlogged_override_preserves_original_agent_error(self):
        with (
            patch.object(agent_runner, "_run_agent_impl", side_effect=RuntimeError("provider failed")),
            patch.object(agent_runner, "load_config", return_value={}),
            patch.object(agent_runner, "resolve_agent", return_value=("agent", {"memory": {"namespace": "ns"}})),
            patch.object(agent_runner, "ExecutionLedger", side_effect=OSError("ledger offline")),
            patch.dict("os.environ", {"CYBER_AI_ALLOW_UNLOGGED_EXECUTION": "1"}, clear=True),
        ):
            with self.assertRaisesRegex(RuntimeError, "provider failed"):
                agent_runner.run_agent("agent", "task under test")

    def test_uncaught_failure_appends_terminal_event(self):
        ledger = FakeLedger()
        self.invoke(ledger)
        self.assertEqual(len(ledger.appended), 1)
        self.assertEqual(ledger.appended[0]["status"], "failed")
        self.assertEqual(ledger.appended[0]["metadata"]["start_event_id"], "start-1")

    def test_does_not_duplicate_existing_terminal_event(self):
        ledger = FakeLedger(finalized=True)
        self.invoke(ledger)
        self.assertEqual(ledger.appended, [])


if __name__ == "__main__":
    unittest.main()
