import os
import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from batch_analyzer import process_directory, process_file


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


    def test_process_file_rejects_symlink_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "outside.txt"
            target.write_text("secret external report", encoding="utf-8")
            link = root / "linked.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with patch("batch_analyzer.ensure_private_directory") as ensure_output:
                with self.assertRaises(ValueError):
                    process_file(link)
                ensure_output.assert_not_called()

    def test_process_directory_rejects_symlink_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "real"
            real.mkdir()
            link = root / "linked"
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(NotADirectoryError):
                process_directory(link)

if __name__ == "__main__":
    unittest.main()
