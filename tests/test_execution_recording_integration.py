import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tool_executor


class ToolExecutorLedgerIntegrationTests(unittest.TestCase):
    def test_successful_execution_is_appended_to_ledger(self):
        evidence = {
            "tool": "ruff", "status": "completed", "return_code": 0,
            "elapsed_seconds": 0.25, "tool_version": "1.0",
            "target": "sample.py", "target_sha256": "a" * 64,
            "target_modified": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            def write_artifact(payload, **kwargs):
                output.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                return output
            with patch.object(tool_executor, "run_local_tool", return_value=evidence), \
                 patch.object(tool_executor, "write_evidence", side_effect=write_artifact), \
                 patch.object(tool_executor, "ExecutionLedger") as ledger, \
                 patch("builtins.print"):
                ledger.return_value.append.return_value = {"sequence": 1, "event_id": "test", "status": "completed"}
                result = tool_executor.main(["--tool", "ruff", "--target", "sample.py", "--execute"])
                artifact_digest = hashlib.sha256(output.read_bytes()).hexdigest()
        self.assertEqual(result, 0)
        ledger.return_value.append.assert_called_once()
        args = ledger.return_value.append.call_args.kwargs
        self.assertEqual(args["status"], "completed")
        self.assertEqual(args["tool"], "ruff")
        self.assertEqual(args["duration_ms"], 250)
        self.assertEqual(args["metadata"]["evidence_artifact_sha256"], artifact_digest)

    def test_dry_run_does_not_create_ledger_event(self):
        with patch.object(tool_executor, "ExecutionLedger") as ledger, \
             patch("builtins.print"):
            result = tool_executor.main(["--tool", "ruff", "--target", "sample.py"])
        self.assertEqual(result, 0)
        ledger.assert_not_called()


if __name__ == "__main__":
    unittest.main()
