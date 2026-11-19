import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sandbox_runner
import tool_adapters
from tool_adapters import ToolExecutionError
from sandbox_runner import SANDBOX_TOOLS


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
        user_flags = [item for item in command if item.startswith("--user=")]
        if os.name == "nt":
            self.assertEqual(user_flags, [])
        else:
            self.assertEqual(len(user_flags), 1)
            self.assertNotEqual(user_flags[0], "--user=0:0")
        self.assertIn("--pull=never", command)
        self.assertIn("readonly", joined)
        self.assertIn("dst=/evidence", joined)
        self.assertIn("CYBER_AI_LEDGER_PATH=/evidence/execution_ledger.sqlite3", command)
        self.assertIn("--require-ledger", command)
        self.assertNotIn("--privileged", command)
        self.assertNotIn("/var/run/docker.sock", joined)

    @unittest.skipIf(os.name == "nt", "El UID de host solo existe en POSIX.")
    def test_root_host_is_rejected_instead_of_running_container_as_root(self):
        evidence = self.root.parent / (self.root.name + "-root-evidence")
        with patch.object(sandbox_runner.os, "getuid", return_value=0), \
             patch.object(sandbox_runner.os, "getgid", return_value=0):
            with self.assertRaisesRegex(ToolExecutionError, "host root"):
                sandbox_runner.build_docker_command("ruff", "sample.py", evidence)

    def test_windows_uses_non_root_image_user_without_posix_uid_calls(self):
        with patch.object(sandbox_runner.os, "getuid", side_effect=AssertionError("getuid called")), \
             patch.object(sandbox_runner.os, "getgid", side_effect=AssertionError("getgid called")):
            self.assertEqual(sandbox_runner._docker_user_args("nt"), [])

        evidence = self.root.parent / (self.root.name + "-windows-evidence")
        with patch.object(sandbox_runner, "_docker_user_args", return_value=[]):
            command = sandbox_runner.build_docker_command("ruff", "sample.py", evidence)
        self.assertFalse(any(item.startswith("--user=") for item in command))
        self.assertIn("--pull=never", command)

    def test_evidence_mount_is_created_with_private_permissions(self):
        evidence = self.root.parent / (self.root.name + "-private-evidence")
        sandbox_runner.build_docker_command("ruff", "sample.py", evidence)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(evidence.stat().st_mode), 0o700)

    @unittest.skipIf(os.name == "nt", "Los bits POSIX no representan ACL de Windows.")
    def test_existing_public_evidence_mount_is_rejected(self):
        evidence = self.root.parent / (self.root.name + "-public-evidence")
        evidence.mkdir(mode=0o755)
        evidence.chmod(0o755)
        with self.assertRaisesRegex(ToolExecutionError, "privada"):
            sandbox_runner.build_docker_command("ruff", "sample.py", evidence)

    def test_only_tools_bundled_in_image_are_allowed(self):
        self.assertEqual(SANDBOX_TOOLS, frozenset({"ruff", "bandit"}))
        evidence = self.root.parent / (self.root.name + "-evidence")
        for tool in ("semgrep", "syft", "trivy"):
            with self.subTest(tool=tool):
                with self.assertRaises(ToolExecutionError):
                    sandbox_runner.build_docker_command(tool, "sample.py", evidence)

    def test_allowlist_matches_tools_installed_in_image(self):
        sandbox_dir = Path(sandbox_runner.__file__).parent / "sandbox"
        dockerfile = sandbox_dir / "Dockerfile"
        lockfile = sandbox_dir / "requirements.lock"
        docker_content = dockerfile.read_text(encoding="utf-8")
        lock_content = lockfile.read_text(encoding="utf-8")

        self.assertIn("COPY sandbox/requirements.lock", docker_content)
        self.assertIn("--require-hashes", docker_content)
        self.assertIn("ruff==0.14.5", lock_content)
        self.assertIn("bandit==1.8.6", lock_content)
        self.assertIn(
            "python:3.12-slim-bookworm@sha256:"
            "0f086103b026048cc50cb5da25ec435c023c5241a83fc44daea593377abc61c4",
            docker_content,
        )
        self.assertEqual(SANDBOX_TOOLS, frozenset({"ruff", "bandit"}))

    def test_host_timeout_bounds_docker_process(self):
        with patch.object(sandbox_runner.shutil, "which", return_value="/usr/bin/docker"), \
             patch.object(
                 sandbox_runner, "build_docker_command",
                 return_value=["docker", "run", "--name", "cyber-ai-sandbox-" + "a" * 32],
             ), \
             patch.object(
                 sandbox_runner.subprocess, "run",
                 side_effect=[
                     subprocess.TimeoutExpired(["docker", "run"], 180),
                     subprocess.CompletedProcess(["docker", "kill"], 0),
                     subprocess.CompletedProcess(["docker", "rm"], 0),
                 ],
             ) as run:
            result = sandbox_runner.main([
                "--tool", "ruff", "--target", "sample.py", "--execute",
            ])
        self.assertEqual(result, 124)
        self.assertEqual(run.call_args_list[0].kwargs["timeout"], 180)
        container_name = run.call_args_list[1].args[0][2]
        self.assertRegex(container_name, r"^cyber-ai-sandbox-[0-9a-f]{32}$")
        self.assertEqual(run.call_args_list[2].args[0], ["docker", "rm", "--force", container_name])
        self.assertEqual(run.call_count, 3)

    def test_evidence_path_rejects_mount_delimiters(self):
        evidence = self.root.parent / (self.root.name + ",bad")
        with self.assertRaises(ToolExecutionError):
            sandbox_runner.build_docker_command(
                "ruff", "sample.py", evidence, image="sandbox:test"
            )

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
