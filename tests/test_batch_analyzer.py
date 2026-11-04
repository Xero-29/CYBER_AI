import os
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
                with patch(
                    "batch_analyzer.enrich_analysis",
                    side_effect=lambda value: value,
                ), patch(
                    "batch_analyzer.register_report",
                    return_value={"duplicate": False},
                ):
                    results = process_directory(incoming)

                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["classification"], "pending_validation")
                self.assertTrue(Path(results[0]["output"]).is_file())
            finally:
                os.chdir(old_cwd)

    def test_rejects_missing_directory(self):
        with self.assertRaises(NotADirectoryError):
            process_directory("directorio_inexistente_cyber_ai")


if __name__ == "__main__":
    unittest.main()
