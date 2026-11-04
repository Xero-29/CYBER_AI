import subprocess
import sys
import unittest
from pathlib import Path


class EntryPointTests(unittest.TestCase):
    def test_self_test(self):
        result = subprocess.run(
            [sys.executable, "cyber_ai.py", "--self-test"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("correcta", result.stdout)

    def test_missing_report_returns_error(self):
        result = subprocess.run(
            [sys.executable, "cyber_ai.py", "--report", "archivo_inexistente.txt"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
