import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sandbox_runner
import tool_adapters
from tool_adapters import ToolExecutionError


class SandboxRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "sample.py").write_text("print('safe')", encoding="utf-8")
        self.root_patch = patch.object(sandbox_runner, "PROJECT_ROOT", self.root)
        self.root_patch.start()
        self.adapter_root_patch = patch.object(tool_adapters, "PROJECT_ROOT", self.root)
        self.adapter_root_patch.start()

    def tearDown(self):
        self.adapter_root_patch.stop()
        self.root_patch.stop()
        self.temp.cleanup()

    def test_docker_command_enforces_isolation_flags_and_read_only_source(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        command = sandbox_runner.build_docker_command(
            "ruff", "sample.py", evidence, image="sandbox:test", timeout=60
        )
        joined = " ".join(command)
        for flag in (
            "--network=none", "--read-only", "--cap-drop=ALL",
            "--security-opt=no-new-privileges:true", "--pids-limit=128",
            "--memory=1g", "--cpus=2",
        ):
            self.assertIn(flag, command)
        user_flag = next(item for item in command if item.startswith("--user="))
        self.assertNotEqual(user_flag, "--user=0:0")
        self.assertTrue(user_flag.startswith("--user="))
        self.assertIn("readonly", joined)
        self.assertIn("dst=/evidence", joined)
        self.assertNotIn("--privileged", command)
        self.assertNotIn("/var/run/docker.sock", joined)

    def test_network_tool_is_denied(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        with self.assertRaises(ToolExecutionError):
            sandbox_runner.build_docker_command("pip_audit", "sample.py", evidence)

    def test_invalid_timeout_is_denied(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        with self.assertRaises(ToolExecutionError):
            sandbox_runner.build_docker_command("ruff", "sample.py", evidence, timeout=999)

    def test_target_outside_repo_is_denied(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        with tempfile.TemporaryDirectory() as outside:
            with self.assertRaises(ToolExecutionError):
                sandbox_runner.build_docker_command("ruff", outside, evidence)


if __name__ == "__main__":
    unittest.main()
