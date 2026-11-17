import os
import unittest
from unittest.mock import patch
from pathlib import Path

from tool_adapters import ToolExecutionError
from tool_execution_pipeline import execute_tool_plan


class ToolExecutionPipelineTests(unittest.TestCase):
    def setUp(self):
        self.plan = {
            "task": "review source",
            "tool_candidates": [{
                "id": "ruff", "adapter_supported": True,
                "risk": "local", "available": True,
            }],
        }

    def test_requires_explicit_operator_confirmation(self):
        with self.assertRaises(ToolExecutionError):
            execute_tool_plan(self.plan, "tests", confirmed=False)

    def test_requires_signed_allowlist_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ToolExecutionError):
                execute_tool_plan(self.plan, "tests", confirmed=True)

    def test_rejects_parent_directory_target(self):
        with self.assertRaises(ToolExecutionError):
            execute_tool_plan(self.plan, "../outside", confirmed=True)

    @patch("tool_execution_pipeline.ExecutionLedger")
    @patch("tool_execution_pipeline.write_evidence", return_value=Path("reports/evidence.json"))
    @patch("tool_execution_pipeline.run_local_tool")
    def test_returns_structured_evidence_and_ledger_reference(
        self, run_tool, write_evidence, ledger
    ):
        run_tool.return_value = {
            "tool": "ruff", "status": "completed",
            "tool_version": "ruff test", "duration_ms": 12,
            "target_sha256": "a" * 64, "tool_binary_sha256": "b" * 64,
            "findings_count": 0,
        }
        ledger.return_value.append.return_value = {"event_id": "event-123"}
        env = {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": "/tmp/allowlist.json",
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": "k" * 64,
        }
        with patch.dict(os.environ, env, clear=True):
            result = execute_tool_plan(self.plan, "tests", confirmed=True)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["results"][0]["tool"], "ruff")
        self.assertEqual(result["results"][0]["ledger_event_id"], "event-123")
        self.assertEqual(run_tool.call_args.args, ("ruff", "tests"))
        self.assertEqual(os.environ.get("CYBER_AI_TOOL_ALLOWLIST_REQUIRED"), None)


if __name__ == "__main__":
    unittest.main()
