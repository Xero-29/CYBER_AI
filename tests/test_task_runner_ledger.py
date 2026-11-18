import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import task_runner


class TaskRunnerLedgerTests(unittest.TestCase):
    def test_records_started_and_terminal_status_mapping(self):
        ledger = unittest.mock.Mock()
        ledger.append.return_value = {"event_id": "terminal"}
        with patch.object(task_runner, "ExecutionLedger", return_value=ledger):
            result = task_runner._record_task_scan(
                "audit", "https://example.test", {"status": "timeout"},
                0.0, "auth-1", "start-1",
            )
        self.assertEqual(result["event_id"], "terminal")
        args = ledger.append.call_args.kwargs
        self.assertEqual(args["status"], "timeout")
        self.assertEqual(args["metadata"]["start_event_id"], "start-1")
        self.assertEqual(args["metadata"]["authorization_id"], "auth-1")

    def test_ledger_failure_is_reported_to_fail_closed_caller(self):
        with patch.object(task_runner, "ExecutionLedger", side_effect=OSError("offline")):
            result = task_runner._record_task_scan(
                "audit", "https://example.test", {"status": "completed"}, 0.0
            )
        self.assertIsNone(result)

    def test_unexpected_scanner_exception_is_recorded_as_failed(self):
        ledger = unittest.mock.Mock()
        ledger.append.side_effect = [
            {"event_id": "start-task-1"},
            {"event_id": "terminal-task-1", "status": "failed"},
        ]
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as home:
            old_cwd = os.getcwd()
            try:
                os.chdir(workspace)
                template = Path(home) / "nuclei-templates/http/technologies/tech-detect.yaml"
                template.parent.mkdir(parents=True)
                template.write_text("id: test\n", encoding="utf-8")
                with (
                    patch.object(Path, "home", return_value=Path(home)),
                    patch.object(task_runner, "select_capabilities", return_value=[{"path": str(template)}]),
                    patch.object(task_runner, "authorize_target", return_value={"authorization_id": "grant"}),
                    patch.object(task_runner.shutil, "which", return_value="/usr/bin/nuclei"),
                    patch.object(task_runner.subprocess, "run", side_effect=RuntimeError("scanner crashed")),
                    patch.object(task_runner, "ExecutionLedger", return_value=ledger),
                    patch.object(sys, "argv", [
                        "task_runner.py", "--task", "inspect web headers",
                        "--target", "https://203.0.113.10", "--execute",
                        "--confirm-authorized", "--authorization-id", "grant",
                    ]),
                ):
                    result = task_runner.main()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result, 1)
        self.assertEqual(
            [call.kwargs["status"] for call in ledger.append.call_args_list],
            ["started", "failed"],
        )


    def test_execute_blocks_when_ledger_cannot_start_by_default(self):
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as home:
            template = Path(home) / "nuclei-templates/http/technologies/tech-detect.yaml"
            template.parent.mkdir(parents=True)
            template.write_text("id: test\n", encoding="utf-8")
            old_cwd = os.getcwd()
            try:
                os.chdir(workspace)
                with (
                    patch.object(Path, "home", return_value=Path(home)),
                    patch.object(task_runner, "select_capabilities", return_value=[{"path": str(template)}]),
                    patch.object(task_runner, "authorize_target", return_value={"authorization_id": "grant"}),
                    patch.object(task_runner.shutil, "which", return_value="/usr/bin/nuclei"),
                    patch.object(task_runner, "ExecutionLedger", side_effect=OSError("ledger offline")),
                    patch.object(task_runner.subprocess, "run") as scanner,
                    patch.object(sys, "argv", [
                        "task_runner.py", "--task", "inspect web headers",
                        "--target", "https://203.0.113.10", "--execute",
                        "--confirm-authorized", "--authorization-id", "grant",
                    ]),
                ):
                    result = task_runner.main()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result, 3)
        scanner.assert_not_called()

    def test_unlogged_scan_requires_explicit_override(self):
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as home:
            template = Path(home) / "nuclei-templates/http/technologies/tech-detect.yaml"
            template.parent.mkdir(parents=True)
            template.write_text("id: test\n", encoding="utf-8")
            old_cwd = os.getcwd()
            try:
                os.chdir(workspace)
                with (
                    patch.object(Path, "home", return_value=Path(home)),
                    patch.object(task_runner, "select_capabilities", return_value=[{"path": str(template)}]),
                    patch.object(task_runner, "authorize_target", return_value={"authorization_id": "grant"}),
                    patch.object(task_runner.shutil, "which", return_value="/usr/bin/nuclei"),
                    patch.object(task_runner, "ExecutionLedger", side_effect=OSError("ledger offline")),
                    patch.object(
                        task_runner.subprocess, "run",
                        return_value=unittest.mock.Mock(returncode=0, stdout="", stderr=""),
                    ) as scanner,
                    patch.object(sys, "argv", [
                        "task_runner.py", "--task", "inspect web headers",
                        "--target", "https://203.0.113.10", "--execute",
                        "--confirm-authorized", "--authorization-id", "grant",
                        "--allow-unlogged-execution",
                    ]),
                ):
                    result = task_runner.main()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result, 0)
        scanner.assert_called_once()

if __name__ == "__main__":
    unittest.main()
