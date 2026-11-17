import subprocess
import sys
import unittest
from unittest.mock import patch, call
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

    @patch("cyber_ai.subprocess.run")
    def test_ask_routes_to_director_with_complete_task(self, run):
        run.return_value.returncode = 0
        with patch.object(sys, "argv", [
            "cyber_ai.py", "--ask", "auditoría web de mi aplicación"
        ]):
            from cyber_ai import main
            self.assertEqual(main(), 0)
        command = run.call_args.args[0]
        self.assertTrue(command[1].endswith("director.py"))
        self.assertEqual(command[2], "auditoría web de mi aplicación")
        self.assertEqual(run.call_args.kwargs["check"], False)

    @patch("cyber_ai.subprocess.run")
    def test_ask_can_disable_knowledge_explicitly(self, run):
        run.return_value.returncode = 0
        with patch.object(sys, "argv", [
            "cyber_ai.py", "--ask", "consulta simple", "--no-knowledge"
        ]):
            from cyber_ai import main
            self.assertEqual(main(), 0)
        self.assertIn("--no-knowledge", run.call_args.args[0])

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
