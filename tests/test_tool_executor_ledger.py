import contextlib
import io
import json
import tempfile
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
        with tempfile.NamedTemporaryFile() as artifact:
            with (
                patch.object(tool_executor, "ExecutionLedger", return_value=ledger),
                patch.object(tool_executor, "run_local_tool") as mocked_runner,
                patch.object(tool_executor, "write_evidence", return_value=artifact.name),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                if isinstance(runner, dict):
                    mocked_runner.return_value = runner
                else:
                    mocked_runner.side_effect = runner
                result = tool_executor.main([
                    "--tool", "ruff", "--target", "tests/fixtures/sample.py", "--execute",
                    "--require-ledger",
                ])
        return result, output.getvalue()

    def test_ledger_initialization_failure_blocks_execution_by_default(self):
        error = io.StringIO()
        with patch.object(
            tool_executor, "ExecutionLedger", side_effect=OSError("ledger unavailable")
        ), patch.object(tool_executor, "run_local_tool") as runner, \
             contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(error):
            result = tool_executor.main([
                "--tool", "ruff", "--target", "tests/fixtures/sample.py", "--execute",
            ])
        self.assertEqual(result, 3)
        runner.assert_not_called()
        self.assertIn("no se pudo registrar el inicio", error.getvalue())
        self.assertNotIn("ledger unavailable", error.getvalue())

    def test_unlogged_execution_requires_explicit_override(self):
        output = io.StringIO()
        with patch.object(
            tool_executor, "ExecutionLedger", side_effect=OSError("ledger unavailable")
        ), patch.object(
            tool_executor, "run_local_tool",
            side_effect=tool_executor.ToolExecutionError("blocked for test"),
        ) as runner, contextlib.redirect_stdout(output), \
             contextlib.redirect_stderr(io.StringIO()):
            result = tool_executor.main([
                "--tool", "ruff", "--target", "tests/fixtures/sample.py", "--execute",
                "--allow-unlogged-execution",
            ])
        self.assertEqual(result, 2)
        runner.assert_called_once()
        self.assertIn("blocked for test", output.getvalue())

    def test_unexpected_adapter_exception_closes_started_event(self):
        ledger = FakeLedger()
        result, output = self.invoke(
            ledger, RuntimeError("unexpected adapter failure token=secret-value")
        )
        self.assertEqual(result, 1)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        self.assertIn("RuntimeError", output)
        self.assertIn("unexpected_adapter_error", output)
        self.assertNotIn("secret-value", output)
        self.assertNotIn("unexpected adapter failure", output)
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
            "target_modified": False,
            "target_sha256": "c" * 64,
            "target_sha256_after": "c" * 64,
            "output_truncated": False,
            "output_limit_exceeded": False,
            "output_limit_termination_failed": False,
        }
        result, output = self.invoke(ledger, evidence)
        self.assertEqual(result, 1)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        terminal = ledger.events[-1]
        self.assertEqual(terminal["status"], "failed")
        self.assertTrue(terminal["validator_results"][0]["passed"])
        self.assertFalse(terminal["validator_results"][1]["passed"])
        self.assertTrue(terminal["validator_results"][2]["passed"])

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
            "output_truncated": False,
            "output_limit_exceeded": False,
            "output_limit_termination_failed": False,
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

    def test_truncated_output_is_failed_and_recorded_as_incomplete(self):
        ledger = FakeLedger()
        evidence = {
            "status": "completed",
            "tool": "ruff",
            "target": "tests/fixtures/sample.py",
            "return_code": 0,
            "output_capture_complete": True,
            "output_truncated": True,
            "output_limit_exceeded": False,
            "output_limit_termination_failed": False,
            "tool_reported_success": True,
        }
        result, output = self.invoke(ledger, evidence)
        self.assertEqual(result, 1)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        terminal = ledger.events[-1]
        self.assertEqual(terminal["status"], "failed")
        validators = {
            item["name"]: item["passed"]
            for item in terminal["validator_results"]
        }
        self.assertTrue(validators["process_exit"])
        self.assertFalse(validators["output_completeness"])
        rendered = json.loads(output)
        self.assertEqual(rendered["status"], "output_incomplete")
        self.assertFalse(rendered["tool_reported_success"])

    def test_incomplete_stream_capture_cannot_be_successful(self):
        ledger = FakeLedger()
        evidence = {
            "status": "completed",
            "tool": "ruff",
            "target": "tests/fixtures/sample.py",
            "return_code": 0,
            "output_capture_complete": False,
            "output_truncated": False,
            "output_limit_exceeded": False,
            "output_limit_termination_failed": False,
            "tool_reported_success": True,
        }
        result, output = self.invoke(ledger, evidence)
        self.assertEqual(result, 1)
        rendered = json.loads(output)
        self.assertEqual(rendered["status"], "output_incomplete")
        self.assertFalse(rendered["tool_reported_success"])
        terminal = ledger.events[-1]
        validators = {item["name"]: item["passed"] for item in terminal["validator_results"]}
        self.assertFalse(validators["output_completeness"])

    def test_missing_output_completeness_metadata_cannot_be_successful(self):
        ledger = FakeLedger()
        evidence = {
            "status": "completed",
            "tool": "ruff",
            "target": "tests/fixtures/sample.py",
            "return_code": 0,
            "tool_reported_success": True,
        }
        result, output = self.invoke(ledger, evidence)
        self.assertEqual(result, 1)
        self.assertEqual(ledger.statuses, ["started", "failed"])
        rendered = json.loads(output)
        self.assertEqual(rendered["status"], "output_integrity_unknown")
        self.assertFalse(rendered["tool_reported_success"])
        terminal = ledger.events[-1]
        validators = {
            item["name"]: item["passed"]
            for item in terminal["validator_results"]
        }
        self.assertFalse(validators["output_completeness"])

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
        self.assertIn("ledger_error_type", output)
        self.assertNotIn("ledger unavailable", output)

    def test_duration_uses_adapter_measurement_and_validates_fallback(self):
        self.assertEqual(tool_executor._duration_ms({"elapsed_seconds": 0.25}, 10.0), 250)
        self.assertEqual(tool_executor._duration_ms({"elapsed_seconds": 0}, 10.0), 0)

        invalid_values = [
            True, -1, float("nan"), float("inf"), "0.25", None,
            10**1000, 1e308,
        ]
        for value in invalid_values:
            with self.subTest(value=value), patch.object(
                tool_executor.time, "monotonic", return_value=10.5
            ):
                self.assertEqual(
                    tool_executor._duration_ms({"elapsed_seconds": value}, 10.0), 500
                )


if __name__ == "__main__":
    unittest.main()
