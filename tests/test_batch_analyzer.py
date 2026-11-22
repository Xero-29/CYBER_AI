import os
import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from batch_analyzer import process_directory


class BatchAnalyzerTests(unittest.TestCase):
    def test_processes_text_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            incoming = root / "incoming"
            incoming.mkdir()
            (incoming / "finding.txt").write_text(
                "Posible fallo de validación", encoding="utf-8"
            )

            old_cwd = os.getcwd()
            try:
                os.chdir(root)
                secret = "report-output-secret"
                with patch(
                    "batch_analyzer.analyze_report",
                    return_value={"classification": "pending_validation", "api_key": secret},
                ), patch(
                    "batch_analyzer.enrich_analysis",
                    side_effect=lambda value: value,
                ), patch(
                    "batch_analyzer.register_report",
                    return_value={"duplicate": False},
                ):
                    results = process_directory(incoming)

                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["classification"], "pending_validation")
                output = Path(results[0]["output"])
                self.assertTrue(output.is_file())
                self.assertNotIn(secret, output.read_text(encoding="utf-8"))
                self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["api_key"], "[REDACTED]")
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
                    self.assertEqual(stat.S_IMODE(output.parent.stat().st_mode), 0o700)
            finally:
                os.chdir(old_cwd)

    def test_rejects_missing_directory(self):
        with self.assertRaises(NotADirectoryError):
            process_directory("directorio_inexistente_cyber_ai")


if __name__ == "__main__":
    unittest.main()
