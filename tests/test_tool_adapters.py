import io
import json
import os
import stat
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
        provenance = {"resolved_path": "/usr/bin/ruff", "sha256": "a" * 64}
        with patch.object(tool_adapters, "_hash_binary", return_value=provenance):
            evidence = run_local_tool("ruff", "sample.py")
        command = popen.call_args.args[0]
        self.assertEqual(command[:3], ["/usr/bin/ruff", "check", "--no-cache"])
        self.assertIn("--output-format=json", command)
        self.assertFalse(popen.call_args.kwargs["shell"])
        self.assertEqual(evidence["status"], "completed")
        self.assertEqual(evidence["tool_version"], "ruff 0.14.5")
        self.assertEqual(evidence["parsed_json"], [])
        self.assertEqual(evidence["network_access"], "not_enforced")
        self.assertFalse(evidence["network_isolation_enforced"])
        self.assertEqual(len(evidence["target_sha256"]), 64)
        self.assertEqual(evidence["tool_binary_sha256"], "a" * 64)
        self.assertEqual(evidence["tool_binary_sha256_after"], "a" * 64)
        self.assertFalse(evidence["tool_binary_modified"])

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/ruff")
    @patch("tool_adapters.subprocess.run")
    def test_binary_replacement_during_execution_invalidates_evidence(self, version_run, which, popen):
        version_run.return_value = subprocess.CompletedProcess(["ruff", "--version"], 0, stdout="ruff 0.14.5", stderr="")
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
                tool_adapters.subprocess, "run",
                return_value=subprocess.CompletedProcess(
                    ["ruff", "--version"], 0, stdout="ruff 0.14.5\\n", stderr=""
                ),
            ),
            patch.object(tool_adapters.subprocess, "Popen", side_effect=start_process),
        ):
            evidence = run_local_tool("ruff", "sample.py")
        self.assertEqual(evidence["status"], "integrity_error")
        self.assertTrue(evidence["target_modified"])
        self.assertFalse(evidence["tool_reported_success"])
        self.assertEqual(evidence["return_code"], 0)

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

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/bandit")
    @patch("tool_adapters.subprocess.run")
    def test_timeout_is_recorded(self, version_run, which, popen):
        version_run.return_value = subprocess.CompletedProcess(["bandit", "--version"], 0, stdout="Bandit 1.8.6", stderr="")
        popen.return_value = FakeProcess(timeout=True)
        provenance = {"resolved_path": "/usr/bin/bandit", "sha256": "b" * 64}
        with patch.object(tool_adapters, "_hash_binary", return_value=provenance):
            evidence = run_local_tool("bandit", "sample.py", timeout=1)
        self.assertEqual(evidence["status"], "timeout")
        self.assertIsNone(evidence["return_code"])

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
        with self.assertRaisesRegex(ToolExecutionError, "enlace simbólico"):
            write_evidence({"tool": "ruff"}, link)
        with self.assertRaisesRegex(ToolExecutionError, "Identificador"):
            write_evidence({"tool": "../escape"}, "reports/unsafe")



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


    def test_yara_is_delegated_to_docker_isolation_runner(self):
        with patch("isolated_tool_runner.run_isolated_tool", return_value={"status": "completed"}) as runner:
            result = run_local_tool("yara", "sample.py", config_path="rules.yar")
        self.assertEqual(result["status"], "completed")
        runner.assert_called_once()
        self.assertEqual(runner.call_args.args, ("yara", "sample.py"))

    def test_tshark_is_delegated_to_docker_isolation_runner(self):
        capture = self.root / "sample.pcap"
        capture.write_bytes(b"pcap")
        with patch("isolated_tool_runner.run_isolated_tool", return_value={"status": "completed"}) as runner:
            result = run_local_tool("tshark", "sample.pcap")
        self.assertEqual(result["status"], "completed")
        runner.assert_called_once()
        self.assertEqual(runner.call_args.args, ("tshark", "sample.pcap"))

    def test_osv_scanner_uses_offline_json_mode(self):
        command = tool_adapters._build_command(
            "osv_scanner", "/usr/bin/osv-scanner", self.root
        )
        self.assertEqual(
            command,
            [
                "/usr/bin/osv-scanner", "--offline", "scan", "source",
                "-r", str(self.root), "--format", "json",
            ],
        )
        self.assertTrue(tool_adapters.TOOL_SPECS["osv_scanner"]["offline_only"])
        self.assertTrue(tool_adapters.TOOL_SPECS["osv_scanner"]["local_database_required"])

    def test_grype_uses_local_directory_json_mode(self):
        command = tool_adapters._build_command(
            "grype", "/usr/bin/grype", self.root
        )
        self.assertEqual(command, ["/usr/bin/grype", str(self.root), "-o", "json"])
        self.assertTrue(tool_adapters.TOOL_SPECS["grype"]["local_database_required"])

    def test_gitleaks_redacts_all_secret_values(self):
        command = tool_adapters._build_command(
            "gitleaks", "/usr/bin/gitleaks", self.root
        )
        self.assertIn("--redact=100", command)
        self.assertIn("--report-format", command)
        self.assertIn("json", command)
        with self.assertRaisesRegex(ToolExecutionError, "directorio"):
            tool_adapters._build_command(
                "gitleaks", "/usr/bin/gitleaks", self.root / "sample.py"
            )

    def test_zeek_accepts_only_offline_capture_files(self):
        capture = self.root / "trace.pcapng"
        capture.write_bytes(b"pcap")
        command = tool_adapters._build_command(
            "zeek", "/usr/bin/zeek", capture
        )
        self.assertEqual(
            command,
            ["/usr/bin/zeek", "-r", str(capture), "LogAscii::use_json=T"],
        )
        with self.assertRaisesRegex(ToolExecutionError, "PCAP"):
            tool_adapters._build_command(
                "zeek", "/usr/bin/zeek", self.root / "sample.py"
            )

    def test_volatility_requires_allowlisted_plugin_and_offline_mode(self):
        command = tool_adapters._build_command(
            "volatility3", "/usr/bin/vol", self.root / "sample.py",
            plugin="windows.info",
        )
        self.assertEqual(
            command,
            ["/usr/bin/vol", "--offline", "-f", str(self.root / "sample.py"), "windows.info"],
        )
        with self.assertRaisesRegex(ToolExecutionError, "allowlist"):
            tool_adapters._build_command(
                "volatility3", "/usr/bin/vol", self.root / "sample.py",
                plugin="malicious.plugin",
            )

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/osv-scanner")
    @patch("tool_adapters.subprocess.run")
    def test_osv_execution_records_offline_configuration(self, version_run, which, popen):
        version_run.return_value = subprocess.CompletedProcess(
            ["osv-scanner", "--version"], 0, stdout="osv-scanner 2.0", stderr=""
        )
        process = FakeProcess(stdout=b'{"results":[]}')
        popen.return_value = process
        provenance = {"resolved_path": "/usr/bin/osv-scanner", "sha256": "a" * 64}
        with (
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters, "verify_tool_allowed", return_value={"allowed": True}),
        ):
            evidence = run_local_tool("osv_scanner", ".")
        self.assertEqual(evidence["status"], "completed")
        self.assertTrue(evidence["tool_reported_success"])
        self.assertEqual(evidence["network_access"], "disabled_by_tool_offline_mode")
        self.assertFalse(evidence["network_isolation_enforced"])
        self.assertIn("--offline", evidence["command"])
        self.assertEqual(evidence["parsed_json"], {"results": []})

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/gitleaks")
    @patch("tool_adapters.subprocess.run")
    def test_gitleaks_findings_exit_code_is_not_misreported_as_execution_failure(
        self, version_run, which, popen
    ):
        version_run.return_value = subprocess.CompletedProcess(
            ["gitleaks", "version"], 0, stdout="gitleaks 8.0", stderr=""
        )
        process = FakeProcess(stdout=b'[{"RuleID":"test"}]')
        process.wait = Mock(return_value=1)
        popen.return_value = process
        provenance = {"resolved_path": "/usr/bin/gitleaks", "sha256": "b" * 64}
        with (
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters, "verify_tool_allowed", return_value={"allowed": True}),
        ):
            evidence = run_local_tool("gitleaks", ".")
        self.assertEqual(evidence["return_code"], 1)
        self.assertTrue(evidence["tool_reported_success"])
        self.assertTrue(evidence["findings_present"])

    @patch("tool_adapters.subprocess.Popen")
    @patch("tool_adapters.shutil.which", return_value="/usr/bin/zeek")
    @patch("tool_adapters.subprocess.run")
    def test_zeek_collects_json_logs_in_temporary_workspace(self, version_run, which, popen):
        capture = self.root / "trace.pcap"
        capture.write_bytes(b"pcap")
        version_run.return_value = subprocess.CompletedProcess(
            ["zeek", "--version"], 0, stdout="zeek 7.0", stderr=""
        )
        def start_process(command, **kwargs):
            Path(kwargs["cwd"], "conn.log").write_text(
                '{"id.orig_h":"192.0.2.1"}\n', encoding="utf-8"
            )
            return FakeProcess()
        popen.side_effect = start_process
        provenance = {"resolved_path": "/usr/bin/zeek", "sha256": "c" * 64}
        with (
            patch.object(tool_adapters, "_hash_binary", return_value=provenance),
            patch.object(tool_adapters, "verify_tool_allowed", return_value={"allowed": True}),
        ):
            evidence = run_local_tool("zeek", "trace.pcap")
        self.assertEqual(evidence["status"], "completed")
        self.assertEqual(
            evidence["parsed_json"]["logs"]["conn.log"][0]["id.orig_h"],
            "192.0.2.1",
        )

if __name__ == "__main__":
    unittest.main()
