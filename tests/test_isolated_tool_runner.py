import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from isolated_tool_runner import run_isolated_tool


class FakeProcess:
    pid = 1234
    def __init__(self):
        self.stdout = io.BytesIO(b"sample output")
        self.stderr = io.BytesIO(b"")
    def wait(self, timeout=None):
        return 0
    def kill(self):
        return None


class IsolatedToolRunnerTests(unittest.TestCase):
    def test_yara_runs_in_networkless_readonly_container(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "sample.bin"
            target.write_bytes(b"sample")
            rules = root / "rules.yar"
            rules.write_text("rule sample { condition: true }", encoding="utf-8")
            with patch("isolated_tool_runner.shutil.which", return_value="/usr/bin/docker"), \
                 patch("isolated_tool_runner.subprocess.run", return_value=subprocess.CompletedProcess(
                     ["docker"], 0, stdout="sha256:" + "a" * 64, stderr=""
                 )), \
                 patch("isolated_tool_runner.verify_tool_allowed", return_value={"enforced": True}), \
                 patch("isolated_tool_runner.subprocess.Popen", return_value=FakeProcess()) as popen:
                evidence = run_isolated_tool(
                    "yara", str(target), config_path=str(rules), allow_external=True
                )
            command = popen.call_args.args[0]
            self.assertIn("--network=none", command)
            self.assertIn("--read-only", command)
            self.assertIn("--cap-drop=ALL", command)
            self.assertIn("--security-opt=no-new-privileges", command)
            self.assertIn("--pids-limit=64", command)
            self.assertFalse(any("docker.sock" in arg for arg in command))
            self.assertTrue(any(arg.endswith(",readonly") for arg in command))
            self.assertTrue(evidence["network_isolation_enforced"])
            self.assertEqual(evidence["status"], "completed")
            self.assertEqual(evidence["tool_binary_sha256"], "a" * 64)

    def test_unknown_tools_are_rejected(self):
        with self.assertRaises(Exception):
            run_isolated_tool("shell", "/tmp", allow_external=True)


if __name__ == "__main__":
    unittest.main()
