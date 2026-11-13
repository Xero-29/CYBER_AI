import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

import tool_adapters
from tool_adapters import ToolExecutionError, run_local_tool, write_evidence


class FakeProcess:
    pid = 99999999

    def __init__(self, stdout=b"[]", stderr=b"", timeout=False):
        self.stdout = io.BytesIO(stdout)
        self.stderr = io.BytesIO(stderr)
        self.timeout = timeout
        self.wait_calls = 0

    def wait(self, timeout=None):
        self.wait_calls += 1
        if self.timeout and self.wait_calls == 1:
            raise subprocess.TimeoutExpired(["fake"], timeout)
        return 0

    def kill(self):
        return None


class ToolAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "sample.py").write_text("print('safe')\n", encoding="utf-8")
        self.root_patch = patch.object(tool_adapters, "PROJECT_ROOT", self.root)
        self.root_patch.start()

    def tearDown(self):
        self.root_patch.stop()
        self.temp.cleanup()

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/ruff")
    @patch("tool_adapters.subprocess.run")
    def test_ruff_uses_argument_vector_and_returns_structured_evidence(self, version_run, which, popen):
        version_run.return_value = subprocess.CompletedProcess(["ruff", "--version"], 0, stdout="ruff 0.14.5\n", stderr="")
        process = FakeProcess()
        popen.return_value = process
        evidence = run_local_tool("ruff", "sample.py")
        command = popen.call_args.args[0]
        self.assertEqual(command[:3], ["/usr/bin/ruff", "check", "--no-cache"])
        self.assertIn("--output-format=json", command)
        self.assertFalse(popen.call_args.kwargs["shell"])
        self.assertEqual(evidence["status"], "completed")
        self.assertEqual(evidence["tool_version"], "ruff 0.14.5")
        self.assertEqual(evidence["parsed_json"], [])
        self.assertFalse(evidence["network_access"])
        self.assertEqual(len(evidence["target_sha256"]), 64)

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/semgrep")
    def test_semgrep_requires_local_config(self, which, popen):
        with self.assertRaisesRegex(ToolExecutionError, "configuración local"):
            run_local_tool("semgrep", "sample.py")
        popen.assert_not_called()

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/pip-audit")
    def test_pip_audit_is_denied_without_network_policy(self, which, popen):
        with self.assertRaisesRegex(ToolExecutionError, "requiere consultar"):
            run_local_tool("pip_audit", "sample.py")
        popen.assert_not_called()

    def test_paths_outside_repository_are_denied(self):
        with tempfile.TemporaryDirectory() as outside:
            with self.assertRaises(ToolExecutionError):
                run_local_tool("ruff", outside)

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/bandit")
    def test_timeout_is_recorded(self, which, popen):
        popen.return_value = FakeProcess(timeout=True)
        evidence = run_local_tool("bandit", "sample.py", timeout=1)
        self.assertEqual(evidence["status"], "timeout")
        self.assertIsNone(evidence["return_code"])

    def test_evidence_is_written_inside_repository(self):
        evidence = {"tool": "ruff", "status": "completed"}
        path = write_evidence(evidence)
        self.assertTrue(path.is_file())
        self.assertEqual(json.loads(path.read_text())["tool"], "ruff")
        self.assertTrue(path.resolve().is_relative_to(self.root))


if __name__ == "__main__":
    unittest.main()
