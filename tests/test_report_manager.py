import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from report_manager import fingerprint, register_report


class ReportManagerTests(unittest.TestCase):
    def test_normalized_text_has_same_fingerprint(self):
        self.assertEqual(fingerprint("Hola   mundo"), fingerprint(" hola mundo "))

    def test_registers_and_detects_exact_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("report_manager.REPORTS_DIR", root / "reports"), \
                 patch("report_manager.DATA_DIR", root / "data"), \
                 patch("report_manager.INDEX_FILE", root / "data" / "index.json"):
                first = register_report("prueba", root / "reports" / "uno.json")
                second = register_report("prueba", root / "reports" / "dos.json")
        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])


if __name__ == "__main__":
    unittest.main()
