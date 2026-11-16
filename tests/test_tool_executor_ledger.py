import contextlib
import io
import unittest
from unittest.mock import patch

import tool_executor


class FakeLedger:
    def __init__(self, fail_terminal=False):
        self.statuses = []
        self.fail_terminal = fail_terminal

    def append(self, **event):
        self.statuses.append(event["status"])
        if event["status"] == "started":
            return {"event_id": "start-1"}
        if self.fail_terminal:
            raise OSError("ledger unavailable")
        return {"event_id": "terminal-1", "status": event["status"]}


class ToolExecutorLedgerTests(unittest.TestCase):
    def invoke(self, ledger, runner):
        output = io.StringIO()
        with patch.object(tool_executor, "ExecutionLedger", return_value=ledger), \
             patch.object(tool_executor, "run_local_tool", side_effect=runner), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            result = tool_executor.main([
                "--tool", "ruff", "--target", "tests/fixtures/sample.py", "--execute",
                "--require-ledger",
            ])
        return result, output.getvalue()

    def test_unexpected_adapter_exception_closes_started_event(self):
        ledger = FakeLedger()
        result, output = self.invoke(ledger, RuntimeError("unexpected adapter failure"))
        self.assertEqual(result, 1)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        self.assertIn("RuntimeError", output)
        self.assertIn("terminal-1", output)

    def test_adapter_denial_is_recorded_as_terminal_denied(self):
        ledger = FakeLedger()
        result, output = self.invoke(ledger, tool_executor.ToolExecutionError("blocked"))
        self.assertEqual(result, 2)
        self.assertEqual(ledger.statuses, ["started", "denied"])
        self.assertIn("blocked", output)

    def test_required_ledger_failure_returns_nonzero_after_execution(self):
        ledger = FakeLedger(fail_terminal=True)
        result, output = self.invoke(ledger, RuntimeError("unexpected adapter failure"))
        self.assertEqual(result, 3)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        self.assertIn("ledger_error", output)


if __name__ == "__main__":
    unittest.main()
