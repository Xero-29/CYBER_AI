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
        self.assertFalse(evidence["network_access"])
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

    def test_evidence_is_written_inside_repository(self):
        evidence = {"tool": "ruff", "status": "completed"}
        path = write_evidence(evidence)
        self.assertTrue(path.is_file())
        self.assertEqual(json.loads(path.read_text())["tool"], "ruff")
        self.assertTrue(path.resolve().is_relative_to(self.root))



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
