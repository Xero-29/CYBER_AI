import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tool_executor

from tool_executor import _terminal_status


class ToolExecutorTests(unittest.TestCase):
    def test_finding_exit_code_can_represent_a_successful_scan(self):
        self.assertEqual(
            _terminal_status({
                "status": "completed",
                "return_code": 1,
                "tool_reported_success": True,
                "findings_present": True,
            }),
            "completed",
        )

    def test_unaccepted_exit_code_remains_a_failed_execution(self):
        self.assertEqual(
            _terminal_status({
                "status": "completed",
                "return_code": 2,
                "tool_reported_success": False,
            }),
            "failed",
        )

    def test_cli_requires_and_passes_explicit_network_authorization(self):
        with tempfile.TemporaryDirectory() as temp:
            artifact = Path(temp) / "evidence.json"
            artifact.write_text("{}", encoding="utf-8")

            class FakeLedger:
                def __init__(self):
                    self.events = []

                def append(self, **kwargs):
                    event = {
                        "event_id": f"event-{len(self.events) + 1}",
                        **{key: value for key, value in kwargs.items() if key != "evidence"},
                    }
                    self.events.append(event)
                    return {"event_id": event["event_id"]}

            ledger = FakeLedger()
            evidence = {
                "status": "completed",
                "tool": "nmap",
                "tool_reported_success": True,
                "return_code": 0,
                "target_type": "network",
                "scope_validated": True,
                "authorization_scope": "192.0.2.10/32",
                "scope_allowlist_sha256": "a" * 64,
                "tool_binary_modified": False,
                "tool_binary_sha256": "b" * 64,
                "tool_binary_sha256_after": "b" * 64,
                "target_modified": None,
            }
            with (
                patch.object(tool_executor, "ExecutionLedger", return_value=ledger),
                patch.object(tool_executor, "run_local_tool", return_value=evidence) as runner,
                patch.object(tool_executor, "write_evidence", return_value=artifact),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                result = tool_executor.main([
                    "--tool", "nmap", "--target", "192.0.2.10",
                    "--authorized-network", "--execute",
                ])
            self.assertEqual(result, 0)
            self.assertTrue(runner.call_args.kwargs["allow_network"])
            terminal = ledger.events[-1]
            self.assertTrue(terminal["validator_results"][0]["passed"])
            self.assertTrue(terminal["validator_results"][2]["passed"])

    def test_timeout_and_denied_statuses_are_preserved(self):
        self.assertEqual(_terminal_status({"status": "timeout"}), "timeout")
        self.assertEqual(_terminal_status({"status": "denied"}), "denied")


if __name__ == "__main__":
    unittest.main()
