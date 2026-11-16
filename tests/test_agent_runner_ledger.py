import unittest
from datetime import datetime, timezone
from unittest.mock import patch

import agent_runner


class FakeLedger:
    def __init__(self, finalized=False):
        self.finalized = finalized
        self.appended = []

    def history(self, *, namespace, limit):
        created_at = datetime.now(timezone.utc).isoformat()
        events = [{
            "sequence": 1,
            "event_id": "start-1",
            "created_at": created_at,
            "namespace": namespace,
            "task": "task under test",
            "status": "started",
            "tool": "agent_runner",
            "metadata": {},
        }]
        if self.finalized:
            events.append({
                "sequence": 2,
                "event_id": "end-1",
                "created_at": created_at,
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
        with patch.object(agent_runner, "_run_agent_impl", side_effect=RuntimeError("provider failed")), \
             patch.object(agent_runner, "load_config", return_value={}), \
             patch.object(agent_runner, "resolve_agent", return_value=("agent", {"memory": {"namespace": "ns"}})), \
             patch.object(agent_runner, "ExecutionLedger", return_value=ledger):
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
