import io
import json
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import team_orchestrator


class TeamOrchestratorReportSecurityTests(unittest.TestCase):
    def test_report_redacts_secrets_and_uses_private_atomic_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "team_runs" / "report.json"
            secret = "team-report-secret"
            team_orchestrator.save_report(path, {
                "task": f"password={secret}",
                "api_key": secret,
                "nested": {"token": secret},
            })
            rendered = path.read_text(encoding="utf-8")
            report = json.loads(rendered)
            self.assertNotIn(secret, rendered)
            self.assertEqual(report["api_key"], "[REDACTED]")
            self.assertEqual(report["nested"]["token"], "[REDACTED]")
            self.assertIn("password=[REDACTED]", report["task"])
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

    def test_report_size_is_bounded_before_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "team_runs" / "report.json"
            with patch.object(team_orchestrator, "MAX_REPORT_BYTES", 32):
                with self.assertRaisesRegex(ValueError, "16 MiB"):
                    team_orchestrator.save_report(path, {"data": "x" * 100})
            self.assertFalse(path.exists())



    def test_cli_redacts_provider_errors_before_printing(self):
        secret = "team-provider-secret"
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            workflow_file = Path(directory) / "workflows.json"
            workflow_file.write_text(
                json.dumps({"default_workflow": "test"}),
                encoding="utf-8",
            )
            with patch.object(team_orchestrator, "WORKFLOW_FILE", workflow_file), \\
                 patch.object(
                     team_orchestrator, "execute_workflow",
                     side_effect=RuntimeError(f"falló el proveedor: token={secret}"),
                 ), redirect_stderr(output):
                result = team_orchestrator.main(["--workflow", "test", "tarea"])
        self.assertEqual(result, 1)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())

if __name__ == "__main__":
    unittest.main()
