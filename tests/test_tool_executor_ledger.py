import contextlib
import io
import json
import unittest
from unittest.mock import patch

import tool_executor


class FakeLedger:
    def __init__(self, fail_terminal=False):
        self.statuses = []
        self.events = []
        self.fail_terminal = fail_terminal

    def append(self, **event):
        self.events.append(event)
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

    def test_binary_integrity_error_is_failed_and_validators_fail(self):
        ledger = FakeLedger()
        evidence = {
            "status": "integrity_error",
            "tool": "ruff",
            "target": "tests/fixtures/sample.py",
            "return_code": 0,
            "tool_binary_modified": True,
            "tool_binary_sha256": "a" * 64,
            "tool_binary_sha256_after": "b" * 64,
        }
        result, output = self.invoke(ledger, evidence)
        self.assertEqual(result, 1)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        terminal = ledger.events[-1]
        self.assertEqual(terminal["status"], "failed")
        self.assertFalse(terminal["validator_results"][0]["passed"])
        self.assertFalse(terminal["validator_results"][1]["passed"])

    def test_target_integrity_error_is_failed_and_validators_are_independent(self):
        ledger = FakeLedger()
        evidence = {
            "status": "integrity_error",
            "tool": "ruff",
            "target": "tests/fixtures/sample.py",
            "return_code": 0,
            "tool_binary_modified": False,
            "tool_binary_sha256": "a" * 64,
            "tool_binary_sha256_after": "a" * 64,
            "target_modified": True,
            "target_sha256": "b" * 64,
            "target_sha256_after": "c" * 64,
        }
        result, output = self.invoke(ledger, evidence)
        self.assertEqual(result, 1)
        terminal = ledger.events[-1]
        self.assertEqual(terminal["status"], "failed")
        validators = {item["name"]: item["passed"] for item in terminal["validator_results"]}
        self.assertTrue(validators["process_exit"])
        self.assertTrue(validators["tool_binary_integrity"])
        self.assertFalse(validators["target_integrity"])
        self.assertEqual(
            terminal["metadata"]["target_sha256_after"], "c" * 64
        )

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

    def test_duration_uses_adapter_measurement_and_validates_fallback(self):
        self.assertEqual(tool_executor._duration_ms({"elapsed_seconds": 0.25}, 10.0), 250)
        self.assertEqual(tool_executor._duration_ms({"elapsed_seconds": 0}, 10.0), 0)

        invalid_values = [True, -1, float("nan"), float("inf"), "0.25", None]
        for value in invalid_values:
            with self.subTest(value=value), patch.object(
                tool_executor.time, "monotonic", return_value=10.5
            ):
                self.assertEqual(
                    tool_executor._duration_ms({"elapsed_seconds": value}, 10.0), 500
                )


if __name__ == "__main__":
    unittest.main()
