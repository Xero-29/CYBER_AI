import json
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
from tool_allowlist import sign_tool_allowlist
from sandbox_runner import SANDBOX_TOOLS


class SandboxRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "sample.py").write_text("print('safe')", encoding="utf-8")
        for module in sandbox_runner.RUNTIME_MODULES:
            (self.root / module).write_text("# test runtime module\\n", encoding="utf-8")
        self.root_patch = patch.object(sandbox_runner, "PROJECT_ROOT", self.root)
        self.root_patch.start()
        self.adapter_root_patch = patch.object(tool_adapters, "PROJECT_ROOT", self.root)
        self.adapter_root_patch.start()
        self.runtime_temp = tempfile.TemporaryDirectory()
        self.runtime_dir = sandbox_runner.prepare_runtime_bundle(self.runtime_temp.name)
        self.allowlist_temp = tempfile.TemporaryDirectory()
        self.allowlist_path = Path(self.allowlist_temp.name) / "tools.json"
        self.allowlist_key = "unit-test-hmac-key-" + "x" * 48
        manifest = sign_tool_allowlist(
            {"ruff": {"sha256": "a" * 64}},
            self.allowlist_key.encode("utf-8"),
        )
        self.allowlist_path.write_text(
            json.dumps(manifest, sort_keys=True), encoding="utf-8"
        )
        if os.name == "posix":
            self.allowlist_path.chmod(0o600)
        self.allowlist_env_patch = patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": str(self.allowlist_path),
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": self.allowlist_key,
        })
        self.allowlist_env_patch.start()

    def build_command(self, *args, **kwargs):
        kwargs["runtime_dir"] = self.runtime_dir
        return sandbox_runner.build_docker_command(*args, **kwargs)

    def tearDown(self):
        self.allowlist_env_patch.stop()
        self.allowlist_temp.cleanup()
        self.runtime_temp.cleanup()
        self.adapter_root_patch.stop()
        self.root_patch.stop()
        self.temp.cleanup()

    def test_docker_command_enforces_isolation_flags_and_read_only_source(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        command = self.build_command(
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
        runtime_mount = (
            f"type=bind,src={self.runtime_dir},dst=/workspace,readonly"
        )
        target_mount = (
            f"type=bind,src={(self.root / 'sample.py').resolve()},"
            "dst=/workspace/target,readonly"
        )
        self.assertIn(runtime_mount, command)
        self.assertIn(target_mount, command)
        self.assertNotIn(
            f"type=bind,src={self.root.resolve()},dst=/workspace,readonly",
            joined,
        )
        self.assertIn("CYBER_AI_LEDGER_PATH=/evidence/execution_ledger.sqlite3", command)
        self.assertIn("--require-ledger", command)
        self.assertNotIn("--privileged", command)
        self.assertNotIn("/var/run/docker.sock", joined)

    def test_runtime_bundle_contains_only_minimal_modules_and_no_target_data(self):
        self.assertEqual(
            {item.name for item in self.runtime_dir.iterdir()},
            set(sandbox_runner.RUNTIME_MODULES),
        )
        self.assertNotIn("sample.py", {item.name for item in self.runtime_dir.iterdir()})
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.runtime_dir.stat().st_mode), 0o555)
            for name in sandbox_runner.RUNTIME_MODULES:
                self.assertEqual(
                    stat.S_IMODE((self.runtime_dir / name).stat().st_mode),
                    0o444,
                )

    def test_target_mount_rejects_docker_delimiters(self):
        bad_target = self.root / "bad,target.py"
        bad_target.write_text("print('bad')", encoding="utf-8")
        evidence = self.root.parent / (self.root.name + "-bad-target-evidence")
        with self.assertRaisesRegex(ToolExecutionError, "delimitadores"):
            self.build_command("ruff", "bad,target.py", evidence)

    def test_signed_allowlist_is_read_only_mounted_and_key_is_not_in_argv(self):
        evidence = self.root.parent / (self.root.name + "-signed-evidence")
        command = self.build_command(
            "ruff", "sample.py", evidence, image="sandbox:test"
        )
        allowlist_mount = (
            f"type=bind,src={self.allowlist_path.resolve()},"
            "dst=/run/cyber-ai-tool-allowlist.json,readonly"
        )
        self.assertIn(allowlist_mount, command)
        self.assertIn(
            "CYBER_AI_TOOL_ALLOWLIST_PATH=/run/cyber-ai-tool-allowlist.json",
            command,
        )
        self.assertIn("CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY", command)
        self.assertIn("CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1", command)
        self.assertNotIn(self.allowlist_key, command)

    def test_missing_signed_allowlist_blocks_sandbox_command(self):
        evidence = self.root.parent / (self.root.name + "-missing-allowlist")
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": "",
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": "",
        }):
            with self.assertRaisesRegex(ToolExecutionError, "allowlist HMAC"):
                self.build_command("ruff", "sample.py", evidence)

    def test_invalid_signature_blocks_sandbox_command(self):
        evidence = self.root.parent / (self.root.name + "-invalid-allowlist")
        self.allowlist_path.write_text('{"schema_version":1}', encoding="utf-8")
        if os.name == "posix":
            self.allowlist_path.chmod(0o600)
        with self.assertRaisesRegex(ToolExecutionError, "allowlist HMAC"):
            self.build_command("ruff", "sample.py", evidence)

    def test_allowlist_cannot_authorize_extra_tools(self):
        evidence = self.root.parent / (self.root.name + "-extra-tool-allowlist")
        manifest = sign_tool_allowlist(
            {
                "ruff": {"sha256": "a" * 64},
                "bandit": {"sha256": "b" * 64},
            },
            self.allowlist_key.encode("utf-8"),
        )
        self.allowlist_path.write_text(
            json.dumps(manifest, sort_keys=True), encoding="utf-8"
        )
        if os.name == "posix":
            self.allowlist_path.chmod(0o600)
        with self.assertRaisesRegex(ToolExecutionError, "exclusivamente"):
            self.build_command("ruff", "sample.py", evidence)

    @unittest.skipIf(os.name == "nt", "El UID de host solo existe en POSIX.")
    def test_root_host_is_rejected_instead_of_running_container_as_root(self):
        evidence = self.root.parent / (self.root.name + "-root-evidence")
        with patch.object(sandbox_runner.os, "getuid", return_value=0), \
             patch.object(sandbox_runner.os, "getgid", return_value=0):
            with self.assertRaisesRegex(ToolExecutionError, "host root"):
                self.build_command("ruff", "sample.py", evidence)

    def test_windows_uses_non_root_image_user_without_posix_uid_calls(self):
        with patch.object(sandbox_runner.os, "getuid", side_effect=AssertionError("getuid called")), \
             patch.object(sandbox_runner.os, "getgid", side_effect=AssertionError("getgid called")):
            self.assertEqual(sandbox_runner._docker_user_args("nt"), [])

        evidence = self.root.parent / (self.root.name + "-windows-evidence")
        with patch.object(sandbox_runner, "_docker_user_args", return_value=[]):
            command = self.build_command("ruff", "sample.py", evidence)
        self.assertFalse(any(item.startswith("--user=") for item in command))
        self.assertIn("--pull=never", command)

    def test_evidence_mount_is_created_with_private_permissions(self):
        evidence_root = self.root.parent / (self.root.name + "-private-evidence")
        command = self.build_command("ruff", "sample.py", evidence_root)
        mount = next(
            item for item in command
            if item.startswith("type=bind,src=") and ",dst=/evidence" in item
        )
        mounted = Path(mount.split("src=", 1)[1].split(",dst=", 1)[0])
        self.assertEqual(mounted.parent, evidence_root.resolve())
        self.assertTrue(mounted.name.startswith("run-"))
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(evidence_root.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(mounted.stat().st_mode), 0o700)

    def test_evidence_mount_does_not_expose_previous_reports(self):
        evidence_root = self.root.parent / (self.root.name + "-history-evidence")
        evidence_root.mkdir(mode=0o700)
        previous = evidence_root / "previous-secret.json"
        previous.write_text("must not be mounted", encoding="utf-8")
        command = self.build_command("ruff", "sample.py", evidence_root)
        mount = next(
            item for item in command
            if item.startswith("type=bind,src=") and ",dst=/evidence" in item
        )
        mounted = Path(mount.split("src=", 1)[1].split(",dst=", 1)[0])
        self.assertNotEqual(mounted, evidence_root.resolve())
        self.assertFalse((mounted / previous.name).exists())
        self.assertEqual(previous.read_text(encoding="utf-8"), "must not be mounted")

    def test_evidence_parent_of_repository_is_rejected(self):
        with self.assertRaisesRegex(ToolExecutionError, "solaparse con el repositorio"):
            self.build_command("ruff", "sample.py", self.root.parent)

    @unittest.skipIf(os.name == "nt", "Los bits POSIX no representan ACL de Windows.")
    def test_existing_public_evidence_mount_is_rejected(self):
        evidence = self.root.parent / (self.root.name + "-public-evidence")
        evidence.mkdir(mode=0o755)
        evidence.chmod(0o755)
        with self.assertRaisesRegex(ToolExecutionError, "privada"):
            self.build_command("ruff", "sample.py", evidence)

    def test_only_tools_bundled_in_image_are_allowed(self):
        self.assertEqual(SANDBOX_TOOLS, frozenset({"ruff", "bandit"}))
        evidence = self.root.parent / (self.root.name + "-evidence")
        for tool in ("semgrep", "syft", "trivy"):
            with self.subTest(tool=tool):
                with self.assertRaises(ToolExecutionError):
                    self.build_command(tool, "sample.py", evidence)

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
                 return_value=[
                     "docker", "run", "--name", "cyber-ai-sandbox-" + "a" * 32,
                     "--mount", "type=bind,src=/tmp/evidence/run-" + "b" * 32 + ",dst=/evidence",
                 ],
             ), \
             patch.object(
                 sandbox_runner.subprocess, "run",
                 side_effect=[
                     subprocess.TimeoutExpired(["docker", "run"], 180),
                     subprocess.CompletedProcess(["docker", "kill"], 0),
                     subprocess.CompletedProcess(["docker", "rm"], 0),
                 ],
             ) as run:
            evidence_root = self.root.parent / (self.root.name + "-main-evidence")
            result = sandbox_runner.main([
                "--tool", "ruff", "--target", "sample.py",
                "--evidence-dir", str(evidence_root), "--execute",
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
            self.build_command(
                "ruff", "sample.py", evidence, image="sandbox:test"
            )

    def test_network_tool_is_denied(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        with self.assertRaises(ToolExecutionError):
            self.build_command("pip_audit", "sample.py", evidence)

    def test_invalid_timeout_is_denied(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        with self.assertRaises(ToolExecutionError):
            self.build_command("ruff", "sample.py", evidence, timeout=999)

    def test_target_outside_repo_is_denied(self):
        evidence = self.root.parent / (self.root.name + "-evidence")
        with tempfile.TemporaryDirectory() as outside:
            with self.assertRaises(ToolExecutionError):
                self.build_command("ruff", outside, evidence)



    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_evidence_mount_rejects_group_writable_ancestor(self):
        parent = self.root / "shared"
        parent.mkdir(mode=0o700)
        parent.chmod(0o770)
        evidence = parent / "private"
        with self.assertRaisesRegex(ToolExecutionError, "ruta de evidencias"):
            self.build_command("ruff", "sample.py", evidence)
        self.assertFalse(evidence.exists())

    def test_evidence_mount_rejects_symlinked_ancestor(self):
        real = self.root / "real-evidence-parent"
        real.mkdir()
        linked = self.root / "linked-evidence-parent"
        try:
            linked.symlink_to(real, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        evidence = linked / "private"
        with self.assertRaisesRegex(ToolExecutionError, "ruta de evidencias"):
            self.build_command("ruff", "sample.py", evidence)
        self.assertFalse((real / "private").exists())

if __name__ == "__main__":
    unittest.main()
