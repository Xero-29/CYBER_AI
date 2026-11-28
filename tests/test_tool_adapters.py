import io
import json
import os
import signal
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

import tool_adapters
from process_isolation import ProcessIsolationError
from tool_adapters import ToolExecutionError, run_local_tool, write_evidence


class FakeProcess:
    pid = 99999999

    def __init__(self, stdout=b"[]", stderr=b"", timeout=False):
        self.stdout = io.BytesIO(stdout)
        self.stderr = io.BytesIO(stderr)
        self.timeout = timeout
        self.wait_calls = 0
        self.killed = False

    def wait(self, timeout=None):
        self.wait_calls += 1
        if self.timeout and self.wait_calls == 1:
            raise subprocess.TimeoutExpired(["fake"], timeout)
        return 0

    def kill(self):
        self.killed = True


def _version_result(
    stdout="ruff 0.14.5\n",
    *,
    returncode=0,
    timed_out=False,
    output_truncated=False,
    output_capture_complete=True,
    process_group=True,
):
    return {
        "returncode": returncode,
        "stdout": stdout,
        "stderr": "",
        "timed_out": timed_out,
        "output_truncated": output_truncated,
        "output_capture_complete": output_capture_complete,
        "process_group_isolation_enforced": process_group,
        "process_tree_isolation_enforced": False,
    }


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
    @patch("tool_adapters.run_bounded_process")
    def test_ruff_uses_argument_vector_and_returns_structured_evidence(self, version_run, which, popen):
        version_run.return_value = _version_result("ruff 0.14.5\n")
        process = FakeProcess()
        popen.return_value = process
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}
        with patch.object(tool_adapters, "_hash_binary", return_value=provenance):
            evidence = run_local_tool("ruff", "sample.py")
        command = popen.call_args.args[0]
        self.assertEqual(command[:3], ["/usr/bin/ruff", "check", "--no-cache"])
        self.assertIn("--output-format=json", command)
        self.assertFalse(popen.call_args.kwargs["shell"])
        self.assertEqual(
            popen.call_args.kwargs["cwd"], popen.call_args.kwargs["env"]["HOME"]
        )
        self.assertEqual(evidence["status"], "completed")
        self.assertTrue(evidence["output_capture_complete"])
        self.assertEqual(evidence["tool_version"], "ruff 0.14.5")
        self.assertEqual(version_run.call_args.kwargs["timeout"], 5)
        self.assertEqual(version_run.call_args.kwargs["max_output_bytes"], 8192)
        self.assertEqual(evidence["parsed_json"], [])
        self.assertEqual(evidence["network_access"], "not_enforced")
        self.assertFalse(evidence["network_isolation_enforced"])
        self.assertEqual(len(evidence["target_sha256"]), 64)
        self.assertEqual(evidence["tool_binary_sha256"], "a" * 64)
        self.assertEqual(evidence["tool_binary_sha256_after"], "a" * 64)
        self.assertFalse(evidence["tool_binary_modified"])
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_non_posix_output_limit_fallback_is_not_claimed_as_tree_isolation(self):
        process = FakeProcess()
        terminated = tool_adapters._terminate_process_tree(process, posix=False)
        self.assertFalse(terminated)
        self.assertTrue(process.killed)

    def test_truncated_output_is_incomplete_even_when_tool_exits_zero(self):
        process = FakeProcess(stdout=b"x" * (tool_adapters.MAX_OUTPUT_BYTES + 1))
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}
        with (
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters.shutil, "which", return_value="/usr/bin/ruff"),
            patch.object(
                tool_adapters, "run_bounded_process",
                return_value=_version_result("ruff 0.14.5"),
            ),
            patch.object(tool_adapters.subprocess, "Popen", return_value=process),
        ):
            evidence = run_local_tool("ruff", "sample.py")
        self.assertEqual(evidence["return_code"], 0)
        self.assertEqual(evidence["status"], "output_truncated")
        self.assertTrue(evidence["output_truncated"])
        self.assertFalse(evidence["output_limit_exceeded"])
        self.assertTrue(evidence["output_capture_complete"])
        self.assertFalse(evidence["tool_reported_success"])

    def test_stream_read_failures_and_invalid_chunks_fail_closed(self):
        class FailingStream:
            def __init__(self, *, error=None, value=None):
                self.closed = False
                self.error = error
                self.value = value

            def read(self, _size):
                if self.error is not None:
                    raise self.error
                return self.value

            def close(self):
                self.closed = True

        class FailingProcess(FakeProcess):
            def __init__(self, stream):
                self.stdout = stream
                self.stderr = io.BytesIO(b"")
                self.timeout = False
                self.wait_calls = 0
                self.killed = False

        broken_streams = (
            FailingStream(error=OSError("synthetic read failure")),
            FailingStream(error=RuntimeError("synthetic wrapper failure")),
            FailingStream(value="not-bytes"),
        )
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}
        for stream in broken_streams:
            with self.subTest(stream=type(stream.error).__name__ if stream.error else "invalid-chunk"):
                with (
                    patch.object(tool_adapters, "_hash_binary", return_value=provenance),
                    patch.object(tool_adapters.shutil, "which", return_value="/usr/bin/ruff"),
                    patch.object(
                        tool_adapters, "run_bounded_process",
                        return_value=_version_result("ruff 0.14.5"),
                    ),
                    patch.object(
                        tool_adapters.subprocess, "Popen",
                        return_value=FailingProcess(stream),
                    ),
                ):
                    with self.assertRaisesRegex(ProcessIsolationError, "capturar íntegramente"):
                        run_local_tool("ruff", "sample.py")


    def test_excessive_total_output_terminates_the_process_group(self):
        process = FakeProcess(
            stdout=b"x" * (tool_adapters.MAX_TOTAL_OUTPUT_BYTES + 1)
        )
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}
        with (
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters.shutil, "which", return_value="/usr/bin/ruff"),
            patch.object(
                tool_adapters, "run_bounded_process",
                return_value=_version_result("ruff 0.14.5"),
            ),
            patch.object(tool_adapters.subprocess, "Popen", return_value=process),
            patch.object(tool_adapters.os, "killpg") as killpg,
        ):
            evidence = run_local_tool("ruff", "sample.py")
        killpg.assert_called_once_with(process.pid, signal.SIGKILL)
        self.assertEqual(evidence["status"], "output_limit_exceeded")
        self.assertTrue(evidence["output_truncated"])
        self.assertTrue(evidence["output_limit_exceeded"])
        self.assertFalse(evidence["output_capture_complete"])
        self.assertFalse(evidence["tool_reported_success"])
        self.assertFalse(evidence["output_limit_termination_failed"])

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/ruff")
    @patch("tool_adapters.run_bounded_process")
    def test_host_tool_uses_ephemeral_home_and_does_not_forward_secrets(
        self, version_run, which, popen
    ):
        version_run.return_value = _version_result("ruff 0.14.5\n")
        popen.return_value = FakeProcess()
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}
        with (
            patch.dict(os.environ, {
                "HOME": "/home/private-user",
                "AWS_SECRET_ACCESS_KEY": "must-not-be-forwarded",
                "OPENAI_API_KEY": "must-not-be-forwarded",
            }),
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
        ):
            run_local_tool("ruff", "sample.py")

        process_env = popen.call_args.kwargs["env"]
        version_env = version_run.call_args.kwargs["env"]
        self.assertNotEqual(process_env["HOME"], "/home/private-user")
        self.assertEqual(process_env["HOME"], process_env["TMPDIR"])
        self.assertEqual(process_env, version_env)
        self.assertEqual(version_run.call_args.kwargs["cwd"], version_env["HOME"])
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", process_env)
        self.assertNotIn("OPENAI_API_KEY", process_env)
        self.assertNotIn("/home/private-user", process_env["PATH"])
        self.assertIn("/usr/bin", process_env["PATH"])
        self.assertTrue(all(process_env["PATH"].split(os.pathsep)))
        self.assertFalse(Path(process_env["HOME"]).exists())

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/ruff")
    @patch("tool_adapters.run_bounded_process")
    def test_binary_replacement_during_execution_invalidates_evidence(self, version_run, which, popen):
        version_run.return_value = _version_result("ruff 0.14.5")
        popen.return_value = FakeProcess()
        hashes = [
            {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64},
            {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64},
            {"resolved_path": "/usr/bin/ruff", "sha256": "c" * 64},
        ]
        with patch.object(tool_adapters, "_hash_binary", side_effect=hashes):
            evidence = run_local_tool("ruff", "sample.py")
        self.assertEqual(evidence["status"], "integrity_error")
        self.assertTrue(evidence["tool_binary_modified"])
        self.assertFalse(evidence["tool_reported_success"])

    def test_target_mutation_during_execution_invalidates_success(self):
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}

        def start_process(*args, **kwargs):
            (self.root / "sample.py").write_text("print('changed')\\n", encoding="utf-8")
            return FakeProcess()

        with (
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters.shutil, "which", return_value="/usr/bin/ruff"),
            patch.object(
                tool_adapters, "run_bounded_process",
                return_value=_version_result("ruff 0.14.5\\n"),
            ),
            patch.object(tool_adapters.subprocess, "Popen", side_effect=start_process),
        ):
            evidence = run_local_tool("ruff", "sample.py")
        self.assertEqual(evidence["status"], "integrity_error")
        self.assertTrue(evidence["target_modified"])
        self.assertFalse(evidence["tool_reported_success"])
        self.assertEqual(evidence["return_code"], 0)

    def test_version_probe_fails_closed_on_timeout_truncation_or_missing_group(self):
        for result in (
            _version_result(timed_out=True),
            _version_result(output_truncated=True),
            _version_result(output_capture_complete=False),
            _version_result(process_group=False),
        ):
            with self.subTest(result=result):
                with patch.object(tool_adapters, "run_bounded_process", return_value=result) as runner:
                    self.assertEqual(
                        tool_adapters._probe_tool_version(
                            "/usr/bin/ruff", "ruff", {"HOME": "/tmp/cyber-probe"}
                        ),
                        "unknown",
                    )
                self.assertEqual(runner.call_args.kwargs["timeout"], 5)
                self.assertEqual(runner.call_args.kwargs["max_output_bytes"], 8192)
                self.assertEqual(runner.call_args.kwargs["cwd"], "/tmp/cyber-probe")

        with patch.object(tool_adapters, "run_bounded_process") as runner:
            self.assertEqual(
                tool_adapters._probe_tool_version("/usr/bin/ruff", "ruff", {}),
                "unknown",
            )
        runner.assert_not_called()

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/semgrep")
    def test_semgrep_requires_local_config(self, which, popen):
        provenance = {"resolved_path": "/usr/bin/semgrep", "sha256": "d" * 64}
        with patch.object(tool_adapters, "_hash_binary", return_value=provenance):
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

    def test_relative_target_is_resolved_from_project_root(self):
        with patch("tool_adapters.os.getcwd", return_value=str(self.root.parent)):
            self.assertEqual(
                tool_adapters._confined_path("sample.py"),
                self.root / "sample.py",
            )

    def test_confined_path_rejects_symlinked_ancestor(self):
        real_parent = self.root / "real-target"
        real_parent.mkdir()
        (real_parent / "sample.py").write_text("print('safe')\\n", encoding="utf-8")
        linked_parent = self.root / "linked-target"
        try:
            linked_parent.symlink_to(real_parent, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(ToolExecutionError, "enlaces simbólicos"):
            tool_adapters._confined_path(linked_parent / "sample.py")

    def test_confined_path_rejects_hardlinked_target_file(self):
        with tempfile.TemporaryDirectory() as outside:
            secret = Path(outside) / "secret.py"
            secret.write_text("private material\\n", encoding="utf-8")
            linked_target = self.root / "linked-secret.py"
            try:
                os.link(secret, linked_target)
            except OSError:
                self.skipTest("hardlinks unavailable")
            with self.assertRaisesRegex(ToolExecutionError, "enlaces duros"):
                tool_adapters._confined_path(linked_target)

    def test_hash_target_bounds_total_directory_entries(self):
        target = self.root / "bounded-tree"
        nested = target / "nested"
        nested.mkdir(parents=True)
        (nested / "sample.py").write_text("print('safe')\\n", encoding="utf-8")
        with patch.object(tool_adapters, "MAX_TARGET_ENTRIES", 1):
            with self.assertRaisesRegex(ToolExecutionError, "límite total de entradas"):
                tool_adapters._hash_target(target)

    def test_hash_target_detects_root_directory_replacement_during_scan(self):
        target = self.root / "root-swap"
        replacement = self.root / "replacement"
        moved = self.root / "root-swap-original"
        target.mkdir()
        replacement.mkdir()
        real_scandir = os.scandir

        def replace_root_before_scan(root):
            if Path(root) == target:
                target.rename(moved)
                replacement.rename(target)
            return real_scandir(root)

        with patch.object(tool_adapters.os, "scandir", side_effect=replace_root_before_scan):
            with self.assertRaisesRegex(ToolExecutionError, "cambió durante el cálculo"):
                tool_adapters._hash_target(target)

    def test_hash_target_fails_closed_when_directory_scan_is_incomplete(self):
        target = self.root / "unreadable-tree"
        target.mkdir()
        real_scandir = os.scandir

        def fail_target_scan(root):
            if Path(root) == target:
                raise PermissionError("synthetic enumeration failure")
            return real_scandir(root)

        with patch.object(tool_adapters.os, "scandir", side_effect=fail_target_scan):
            with self.assertRaisesRegex(ToolExecutionError, "enumerar el objetivo"):
                tool_adapters._hash_target(target)

    def test_hash_target_rejects_nested_hardlinked_file(self):
        target_dir = self.root / "tree"
        target_dir.mkdir()
        with tempfile.TemporaryDirectory() as outside:
            secret = Path(outside) / "secret.py"
            secret.write_text("private material\\n", encoding="utf-8")
            try:
                os.link(secret, target_dir / "linked-secret.py")
            except OSError:
                self.skipTest("hardlinks unavailable")
            self.assertEqual(tool_adapters._confined_path(target_dir), target_dir)
            with self.assertRaisesRegex(ToolExecutionError, "enlaces duros"):
                tool_adapters._hash_target(target_dir)

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/bandit")
    @patch("tool_adapters.run_bounded_process")
    def test_timeout_is_recorded(self, version_run, which, popen):
        version_run.return_value = _version_result("Bandit 1.8.6")
        process = FakeProcess(timeout=True)
        popen.return_value = process
        provenance = {"resolved_path": "/usr/bin/bandit", "sha256": "b" * 64}
        with patch.object(tool_adapters, "_hash_binary", return_value=provenance):
            evidence = run_local_tool("bandit", "sample.py", timeout=1)
        self.assertEqual(evidence["status"], "timeout")
        self.assertIsNone(evidence["return_code"])
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_evidence_is_written_inside_repository_with_private_permissions(self):
        evidence = {"tool": "ruff", "status": "completed"}
        path = write_evidence(evidence)
        self.assertTrue(path.is_file())
        self.assertEqual(json.loads(path.read_text())["tool"], "ruff")
        self.assertTrue(path.resolve().is_relative_to(self.root))
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

    def test_evidence_publication_failure_removes_temporary_file(self):
        with patch.object(tool_adapters.os, "replace", side_effect=OSError("publish failed")):
            with self.assertRaisesRegex(ToolExecutionError, "evidencia protegida"):
                write_evidence({"tool": "ruff", "status": "completed"})
        evidence_dir = self.root / "reports" / "tool_evidence"
        self.assertTrue(evidence_dir.is_dir())
        self.assertEqual(list(evidence_dir.iterdir()), [])

    def test_evidence_rejects_symlink_destination_and_unsafe_tool_name(self):
        outside = self.root / "outside"
        outside.mkdir()
        link = self.root / "linked-evidence"
        link.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ToolExecutionError, "enlaces simbólicos"):
            write_evidence({"tool": "ruff"}, link)
        with self.assertRaisesRegex(ToolExecutionError, "Identificador"):
            write_evidence({"tool": "../escape"}, "reports/unsafe")

    def test_evidence_rejects_symlinked_parent_before_creating_children(self):
        outside = self.root / "outside"
        outside.mkdir()
        link = self.root / "linked-parent"
        link.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ToolExecutionError, "enlaces simbólicos"):
            write_evidence({"tool": "ruff"}, link / "new" / "evidence")
        self.assertFalse((outside / "new").exists())

    def test_evidence_rejects_external_path_before_creating_directory(self):
        with tempfile.TemporaryDirectory() as outside:
            destination = Path(outside) / "new-evidence"
            with self.assertRaisesRegex(ToolExecutionError, "dentro del repositorio"):
                write_evidence({"tool": "ruff"}, destination)
            self.assertFalse(destination.exists())

    def test_external_evidence_override_requires_an_explicit_boolean(self):
        with tempfile.TemporaryDirectory() as outside:
            destination = Path(outside) / "new-evidence"
            for value in ("false", 1, None):
                with self.subTest(value=value):
                    with self.assertRaisesRegex(ToolExecutionError, "booleano explícito"):
                        write_evidence(
                            {"tool": "ruff", "status": "completed"},
                            destination,
                            allow_external=value,
                        )
            self.assertFalse(destination.exists())

    def test_evidence_cannot_chmod_repository_root(self):
        original_mode = stat.S_IMODE(self.root.stat().st_mode)
        with self.assertRaisesRegex(ToolExecutionError, "raíz del repositorio"):
            write_evidence({"tool": "ruff"}, self.root)
        self.assertEqual(stat.S_IMODE(self.root.stat().st_mode), original_mode)

    @unittest.skipUnless(os.name == "posix", "Los permisos POSIX se prueban en POSIX.")
    def test_evidence_refuses_to_chmod_existing_shared_directory(self):
        shared = self.root / "shared"
        shared.mkdir()
        shared.chmod(0o755)
        with self.assertRaisesRegex(ToolExecutionError, "modo privado 0700"):
            write_evidence({"tool": "ruff"}, shared)
        self.assertEqual(stat.S_IMODE(shared.stat().st_mode), 0o755)



    def test_checkov_builds_local_json_command(self):
        target = self.root / "iac"
        target.mkdir()
        command = tool_adapters._build_command("checkov", "/usr/bin/checkov", target)
        self.assertEqual(command, ["/usr/bin/checkov", "-d", str(target), "--output", "json", "--quiet"])

    def test_detect_secrets_requires_repository_directory(self):
        with self.assertRaisesRegex(ToolExecutionError, "directorio"):
            tool_adapters._build_command("detect_secrets", "/usr/bin/detect-secrets", self.root / "sample.py")

    def test_shellcheck_selects_only_shell_files(self):
        target = self.root / "scripts"
        target.mkdir()
        shell = target / "check.sh"
        shell.write_text("echo ok\n", encoding="utf-8")
        (target / "ignore.py").write_text("print('x')\n", encoding="utf-8")
        command = tool_adapters._build_command("shellcheck", "/usr/bin/shellcheck", target)
        self.assertIn(str(shell), command)
        self.assertNotIn(str(target / "ignore.py"), command)

    def test_shellcheck_file_discovery_enforces_total_entry_limit(self):
        target = self.root / "many-scripts"
        target.mkdir()
        for index in range(3):
            (target / f"script-{index}.sh").write_text("echo ok\\n", encoding="utf-8")
        with patch.object(tool_adapters, "MAX_TARGET_ENTRIES", 2):
            with self.assertRaisesRegex(ToolExecutionError, "límite total de entradas"):
                tool_adapters._build_command("shellcheck", "/usr/bin/shellcheck", target)

    def test_shellcheck_file_discovery_rejects_symlinked_directories(self):
        target = self.root / "scripts-with-link"
        external = self.root / "external-scripts"
        target.mkdir()
        external.mkdir()
        (external / "hidden.sh").write_text("echo hidden\\n", encoding="utf-8")
        link = target / "linked"
        try:
            link.symlink_to(external, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(ToolExecutionError, "enlaces simbólicos"):
            tool_adapters._build_command("shellcheck", "/usr/bin/shellcheck", target)

    def test_shellcheck_command_preparation_rejects_target_mutation_before_launch(self):
        target = self.root / "scripts"
        target.mkdir()
        (target / "check.sh").write_text("echo ok\\n", encoding="utf-8")
        provenance = {"resolved_path": "/usr/bin/shellcheck", "sha256": "a" * 64}
        with (
            patch.object(tool_adapters.shutil, "which", return_value="/usr/bin/shellcheck"),
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters, "verify_tool_allowed", return_value={"approved": True}),
            patch.object(tool_adapters, "_probe_tool_version", return_value="shellcheck 0.10.0"),
            patch.object(tool_adapters, "_hash_target", side_effect=["a" * 64, "b" * 64]),
            patch.object(tool_adapters.subprocess, "Popen") as popen,
        ):
            with self.assertRaisesRegex(ToolExecutionError, "cambió mientras se preparaba"):
                run_local_tool("shellcheck", "scripts")
        popen.assert_not_called()

    def test_actionlint_selects_workflow_files(self):
        target = self.root / "workflows"
        target.mkdir()
        workflow = target / "ci.yml"
        workflow.write_text("name: ci\n", encoding="utf-8")
        command = tool_adapters._build_command("actionlint", "/usr/bin/actionlint", target)
        self.assertEqual(command, ["/usr/bin/actionlint", "-oneline", str(workflow)])

    def test_yara_requires_local_rules(self):
        with self.assertRaisesRegex(ToolExecutionError, "reglas local"):
            tool_adapters._build_command("yara", "/usr/bin/yara", self.root / "sample.py")
        rules = self.root / "rules.yar"
        rules.write_text("rule test { condition: true }\n", encoding="utf-8")
        command = tool_adapters._build_command("yara", "/usr/bin/yara", self.root / "sample.py", config_path=rules)
        self.assertEqual(command, ["/usr/bin/yara", "-r", str(rules), str(self.root / "sample.py")])

    def test_tshark_requires_pcap_file(self):
        with self.assertRaisesRegex(ToolExecutionError, "PCAP"):
            tool_adapters._build_command("tshark", "/usr/bin/tshark", self.root / "sample.py")
        capture = self.root / "trace.pcap"
        capture.write_bytes(b"pcap")
        command = tool_adapters._build_command("tshark", "/usr/bin/tshark", capture)
        self.assertEqual(command, ["/usr/bin/tshark", "-r", str(capture), "-T", "json"])


    @patch("tool_adapters.shutil.which")
    def test_windows_requires_job_object_before_host_execution(self, which):
        with patch("tool_adapters.os.name", "nt"):
            with self.assertRaisesRegex(ToolExecutionError, "Job Object"):
                run_local_tool("ruff", "sample.py")
        which.assert_not_called()

    @patch("tool_adapters.shutil.which")
    def test_yara_requires_isolation_before_host_execution(self, which):
        with self.assertRaisesRegex(ToolExecutionError, "sandbox aislado"):
            run_local_tool("yara", "sample.py", config_path="sample.py")
        which.assert_not_called()

    @patch("tool_adapters.shutil.which")
    def test_tshark_requires_isolation_before_host_execution(self, which):
        capture = self.root / "sample.pcap"
        capture.write_bytes(b"pcap")
        with self.assertRaisesRegex(ToolExecutionError, "sandbox aislado"):
            run_local_tool("tshark", "sample.pcap")
        which.assert_not_called()

if __name__ == "__main__":
    unittest.main()
