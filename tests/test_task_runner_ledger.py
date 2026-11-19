import json
import hashlib
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

    def test_execute_blocks_when_ledger_cannot_start_by_default(self):
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as home:
            nuclei_executable = Path(workspace) / "nuclei"
            nuclei_executable.write_bytes(b"fake nuclei binary")
            provenance = {
                "resolved_path": str(nuclei_executable),
                "sha256": hashlib.sha256(nuclei_executable.read_bytes()).hexdigest(),
                "allowlist": {"enforced": True, "status": "approved"},
            }
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
                    patch.object(task_runner.shutil, "which", return_value=str(nuclei_executable)),
                    patch.object(task_runner, "require_approved_executable", return_value=provenance),
                    patch.object(task_runner, "ExecutionLedger", side_effect=OSError("ledger offline")),
                    patch.object(task_runner, "run_bounded_process") as scanner,
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
            nuclei_executable = Path(workspace) / "nuclei"
            nuclei_executable.write_bytes(b"fake nuclei binary")
            provenance = {
                "resolved_path": str(nuclei_executable),
                "sha256": hashlib.sha256(nuclei_executable.read_bytes()).hexdigest(),
                "allowlist": {"enforced": True, "status": "approved"},
            }
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
                    patch.object(task_runner.shutil, "which", return_value=str(nuclei_executable)),
                    patch.object(task_runner, "require_approved_executable", return_value=provenance),
                    patch.object(task_runner, "ExecutionLedger", side_effect=OSError("ledger offline")),
                    patch.object(
                        task_runner, "run_bounded_process",
                        return_value={
                            "returncode": 0, "stdout": "", "stderr": "",
                            "timed_out": False, "output_truncated": False,
                            "process_tree_isolation_enforced": True,
                        },
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

    def test_process_isolation_error_is_reported_as_required(self):
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as home:
            nuclei_executable = Path(workspace) / "nuclei"
            nuclei_executable.write_bytes(b"fake nuclei binary")
            provenance = {
                "resolved_path": str(nuclei_executable),
                "sha256": hashlib.sha256(nuclei_executable.read_bytes()).hexdigest(),
                "allowlist": {"enforced": True, "status": "approved"},
            }
            template = Path(home) / "nuclei-templates/http/technologies/tech-detect.yaml"
            template.parent.mkdir(parents=True)
            template.write_text("id: test\n", encoding="utf-8")
            ledger = unittest.mock.Mock()
            ledger.append.side_effect = [{"event_id": "start"}, {"event_id": "terminal"}]
            old_cwd = os.getcwd()
            try:
                os.chdir(workspace)
                with (
                    patch.object(Path, "home", return_value=Path(home)),
                    patch.object(task_runner, "select_capabilities", return_value=[{"path": str(template)}]),
                    patch.object(task_runner, "authorize_target", return_value={"authorization_id": "grant"}),
                    patch.object(task_runner.shutil, "which", return_value=str(nuclei_executable)),
                    patch.object(task_runner, "require_approved_executable", return_value=provenance),
                    patch.object(task_runner, "ExecutionLedger", return_value=ledger),
                    patch.object(
                        task_runner, "run_bounded_process",
                        side_effect=task_runner.ProcessIsolationError("Job Object required"),
                    ),
                    patch.object(sys, "argv", [
                        "task_runner.py", "--task", "inspect web headers",
                        "--target", "https://203.0.113.10", "--execute",
                        "--confirm-authorized", "--authorization-id", "grant",
                    ]),
                ):
                    result = task_runner.main()
                self.assertEqual(result, 1)
                report_files = sorted((Path(workspace) / "reports").glob("task_scan_*_report.json"))
                self.assertEqual(len(report_files), 1)
                report = json.loads(report_files[0].read_text(encoding="utf-8"))
                self.assertEqual(report["status"], "isolation_required")
                self.assertEqual(report["error_type"], "ProcessIsolationError")
                self.assertEqual(report["reason"], "process_isolation_unavailable")
                self.assertTrue(report["report_persisted"])
                self.assertNotIn("error", report)
            finally:
                os.chdir(old_cwd)

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
                nuclei_executable = Path(workspace) / "nuclei"
                nuclei_executable.write_bytes(b"fake nuclei binary")
                provenance = {
                    "resolved_path": str(nuclei_executable),
                    "sha256": hashlib.sha256(nuclei_executable.read_bytes()).hexdigest(),
                    "allowlist": {"enforced": True, "status": "approved"},
                }
                template = Path(home) / "nuclei-templates/http/technologies/tech-detect.yaml"
                template.parent.mkdir(parents=True)
                template.write_text("id: test\n", encoding="utf-8")
                with (
                    patch.object(Path, "home", return_value=Path(home)),
                    patch.object(task_runner, "select_capabilities", return_value=[{"path": str(template)}]),
                    patch.object(task_runner, "authorize_target", return_value={"authorization_id": "grant"}),
                    patch.object(task_runner.shutil, "which", return_value=str(nuclei_executable)),
                    patch.object(task_runner, "require_approved_executable", return_value=provenance),
                    patch.object(task_runner, "run_bounded_process", side_effect=RuntimeError("scanner crashed token=secret-value")),
                    patch.object(task_runner, "ExecutionLedger", return_value=ledger),
                    patch.object(sys, "argv", [
                        "task_runner.py", "--task", "inspect web headers",
                        "--target", "https://203.0.113.10", "--execute",
                        "--confirm-authorized", "--authorization-id", "grant",
                    ]),
                ):
                    result = task_runner.main()
                report_files = sorted((Path(workspace) / "reports").glob("task_scan_*_report.json"))
                self.assertEqual(len(report_files), 1)
                report = json.loads(report_files[0].read_text(encoding="utf-8"))
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result, 1)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["error_type"], "RuntimeError")
        self.assertEqual(report["reason"], "execution_failed")
        self.assertTrue(report["report_persisted"])
        self.assertNotIn("error", report)
        self.assertNotIn("secret-value", json.dumps(report))
        self.assertEqual(
            [call.kwargs["status"] for call in ledger.append.call_args_list],
            ["started", "failed"],
        )


if __name__ == "__main__":
    unittest.main()
