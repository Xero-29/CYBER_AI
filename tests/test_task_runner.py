import hashlib
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import task_runner
from execution_policy import AuthorizationError


class TaskRunnerLedgerTests(unittest.TestCase):
    def test_timeout_is_recorded(self):
        report = {"status": "timeout", "findings": []}
        with patch.object(task_runner, "ExecutionLedger") as ledger:
            task_runner._record_task_scan("web headers", "http://127.0.0.1", report, 0.0, "auth-1")
        ledger.return_value.append.assert_called_once()
        args = ledger.return_value.append.call_args.kwargs
        self.assertEqual(args["status"], "timeout")
        self.assertEqual(args["tool"], "nuclei_task_runner")
        self.assertEqual(args["namespace"], "security-scans")

    def test_missing_confirmation_is_classified_as_denied(self):
        report = {"status": "authorization_denied", "reason": "missing_operator_confirmation"}
        with patch.object(task_runner, "ExecutionLedger") as ledger:
            task_runner._record_task_scan("web headers", "http://127.0.0.1", report, 0.0)
        self.assertEqual(ledger.return_value.append.call_args.kwargs["status"], "denied")

    def test_authorization_denial_is_recorded(self):
        report = {"status": "authorization_denied", "findings": []}
        with patch.object(task_runner, "ExecutionLedger") as ledger:
            task_runner._record_task_scan("web headers", "http://127.0.0.1", report, 0.0)
        self.assertEqual(ledger.return_value.append.call_args.kwargs["status"], "denied")

    def test_prelaunch_revalidation_uses_exact_target_action_and_grant(self):
        target = "https://198.51.100.25"
        with patch("task_runner.authorize_target", return_value={"authorization_id": "auth-7"}) as authorize:
            grant = task_runner._revalidate_target_authorization(target, "auth-7")
        self.assertEqual(grant["authorization_id"], "auth-7")
        authorize.assert_called_once_with(target, "nuclei_scan", "auth-7")

    def test_safe_task_label_redacts_credentials_and_rejects_controls(self):
        self.assertEqual(
            task_runner._safe_task_label("audit token=secret-value"),
            "audit token=[REDACTED]",
        )
        with self.assertRaises(ValueError):
            task_runner._safe_task_label("audit\\nsecond-line")

    def test_query_secret_is_rejected_before_cli_output_or_ledger(self):
        secret = "never-print-this-query-secret"
        argv = [
            "task_runner.py", "--task", "web headers",
            "--target", f"https://198.51.100.25/?token={secret}",
        ]
        output = io.StringIO()
        with patch.object(sys, "argv", argv):
            with redirect_stdout(output), redirect_stderr(output):
                with self.assertRaises(SystemExit):
                    task_runner.main()
        self.assertNotIn(secret, output.getvalue())

    def test_prelaunch_revalidation_propagates_revocation(self):
        with patch(
            "task_runner.authorize_target",
            side_effect=AuthorizationError("expired"),
        ):
            with self.assertRaises(AuthorizationError):
                task_runner._revalidate_target_authorization(
                    "https://198.51.100.25", "auth-7"
                )



class TaskRunnerTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "nuclei-templates"
        self.template = self.root / "http" / "technologies" / "tech-detect.yaml"
        self.template.parent.mkdir(parents=True)
        self.template.write_text("id: tech-detect\\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_only_regular_templates_inside_root(self):
        self.assertEqual(task_runner._safe_template_path(self.template, self.root), self.template.resolve())

    def test_rejects_template_outside_root(self):
        outside = Path(self.temp.name) / "outside.yaml"
        outside.write_text("id: outside\\n", encoding="utf-8")
        self.assertIsNone(task_runner._safe_template_path(outside, self.root))

    def test_rejects_symlink_template(self):
        link = self.template.parent / "linked.yaml"
        try:
            link.symlink_to(self.template)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.assertIsNone(task_runner._safe_template_path(link, self.root))

    def test_rejects_oversized_template(self):
        self.template.write_bytes(b"x" * (2 * 1024 * 1024 + 1))
        self.assertIsNone(task_runner._safe_template_path(self.template, self.root))

    def test_template_hash_evidence_changes_when_content_changes(self):
        selected = [{"path": str(self.template)}]
        before = task_runner._hash_selected_templates(selected, self.root)
        self.template.write_text("id: changed\\n", encoding="utf-8")
        after = task_runner._hash_selected_templates(selected, self.root)
        self.assertEqual(before[0]["path"], after[0]["path"])
        self.assertNotEqual(before[0]["sha256"], after[0]["sha256"])
        self.assertEqual(before[0]["sha256"], hashlib.sha256(b"id: tech-detect\\n").hexdigest())


if __name__ == "__main__":
    unittest.main()
