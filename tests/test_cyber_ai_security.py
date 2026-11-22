import json
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import cyber_ai


class CyberAiOutputSecurityTests(unittest.TestCase):
    def test_report_output_is_private_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            old_cwd = os.getcwd()
            try:
                os.chdir(directory)
                source = Path("finding.txt")
                source.write_text("Informe de prueba", encoding="utf-8")
                secret = "cyber-ai-report-secret"
                with patch.object(
                    cyber_ai,
                    "analyze_report",
                    return_value={
                        "classification": "pending_validation",
                        "cve_references": [],
                        "api_key": secret,
                    },
                ), patch.object(
                    cyber_ai, "enrich_analysis", side_effect=lambda value: value
                ), patch.object(
                    cyber_ai, "register_report", return_value={"duplicate": False}
                ):
                    self.assertEqual(cyber_ai.process_one(source), 0)

                outputs = list(Path("reports").glob("*_analysis.json"))
                self.assertEqual(len(outputs), 1)
                rendered = outputs[0].read_text(encoding="utf-8")
                self.assertNotIn(secret, rendered)
                self.assertEqual(json.loads(rendered)["api_key"], "[REDACTED]")
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(outputs[0].stat().st_mode), 0o600)
                    self.assertEqual(stat.S_IMODE(outputs[0].parent.stat().st_mode), 0o700)
            finally:
                os.chdir(old_cwd)

    def test_scan_summary_redacts_untrusted_finding_text(self):
        secret = "scan-output-secret"
        summary = {
            "target": f"https://example.test/?token={secret}",
            "scan_status": "completed",
            "raw_findings_count": 1,
            "grouped_findings_count": 1,
            "severity_counts": {"info": 1},
            "findings": [{
                "name": f"token={secret}",
                "severity": "info",
                "template_id": "test",
                "matcher_name": "matcher",
                "count": 1,
                "matched_urls": [f"https://example.test/path?token={secret}"],
                "description": f"password={secret}",
                "potential_risk": "No confirmado",
                "manual_validation": "Revisar",
                "recommendation": "Validar",
            }],
        }
        output = StringIO()
        with redirect_stdout(output):
            cyber_ai.print_scan_summary(summary)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())


    def test_process_one_rejects_symlink_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "outside.txt"
            target.write_text("token=must-not-be-read", encoding="utf-8")
            link = root / "linked.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            old_cwd = os.getcwd()
            try:
                os.chdir(root)
                output = StringIO()
                from contextlib import redirect_stderr
                with redirect_stderr(output):
                    result = cyber_ai.process_one(link)
                self.assertEqual(result, 2)
                self.assertNotIn("must-not-be-read", output.getvalue())
                self.assertFalse((root / "reports").exists())
            finally:
                os.chdir(old_cwd)

if __name__ == "__main__":
    unittest.main()
