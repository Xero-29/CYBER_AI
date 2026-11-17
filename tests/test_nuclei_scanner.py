import json
import os
import tempfile
import unittest
from pathlib import Path
import signal
from unittest.mock import patch

from nuclei_scanner import scan_target, validate_target, _terminate_process_tree
from execution_ledger import ExecutionLedger


class FakeProcess:
    def __init__(self, returncode=0, stdout_lines=()):
        self.returncode = returncode
        self.stdout = iter(stdout_lines)

    def poll(self):
        return self.returncode

    def wait(self):
        return self.returncode

    def kill(self):
        self.returncode = -9


class NucleiScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.ledger_path = Path(self.temp.name) / "ledger.sqlite3"
        self.templates = Path(self.temp.name) / "templates"
        self.templates.mkdir()
        (self.templates / "test-template.yaml").write_text("id: test\\n", encoding="utf-8")
        self.ledger_env = patch.dict(os.environ, {
            "CYBER_AI_LEDGER_PATH": str(self.ledger_path),
            "CYBER_AI_NUCLEI_TEMPLATES": str(self.templates),
        })
        self.ledger_env.start()
        self.authorization = patch(
            "nuclei_scanner.authorize_target",
            return_value={"authorization_id": "test-grant"},
        )
        self.authorization.start()

    def tearDown(self):
        self.authorization.stop()
        self.ledger_env.stop()
        self.temp.cleanup()

    def test_scan_requires_explicit_authorization(self):
        result = scan_target("http://127.0.0.1:8765")
        self.assertEqual(result["status"], "authorization_required")
        self.assertEqual(result["findings"], [])

    def test_confirmation_flag_without_grant_id_is_not_authorization(self):
        result = scan_target(
            "http://127.0.0.1:8765",
            authorized=True,
        )
        self.assertEqual(result["status"], "authorization_required")

    def test_validate_target_accepts_local_http_url(self):
        self.assertEqual(
            validate_target("http://127.0.0.1:8765"),
            "http://127.0.0.1:8765",
        )

    def test_validate_target_rejects_invalid_scheme(self):
        with self.assertRaises(ValueError):
            validate_target("ftp://127.0.0.1")

    def test_validate_target_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            validate_target("https://user:password@example.com")

    def test_missing_nuclei_returns_error(self):
        with patch("nuclei_scanner.shutil.which", return_value=None):
            result = scan_target("http://127.0.0.1:8765", authorized=True, authorization_id="test-grant")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["findings"], [])
        self.assertIn("PATH", result["error"])

    def test_successful_scan_reads_jsonl_findings(self):
        finding = {
            "template-id": "test-template",
            "info": {"name": "Test", "severity": "info"},
            "matched-at": "http://127.0.0.1:8765",
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_process = FakeProcess(stdout_lines=["Nuclei iniciado\n"])

            def fake_popen(command, **kwargs):
                output_index = command.index("-o") + 1
                Path(command[output_index]).write_text(
                    json.dumps(finding) + "\n",
                    encoding="utf-8",
                )
                return fake_process

            with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
                with patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen):
                    with patch("nuclei_scanner.time.sleep"):
                        result = scan_target("http://127.0.0.1:8765", authorized=True, authorization_id="test-grant")

            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["findings_count"], 1)
            self.assertEqual(result["findings"][0]["template-id"], "test-template")
            self.assertEqual(result["independent_evidence_validation"]["status"], "valid_structure")
            self.assertTrue(result["ledger_event_id"])
            events = ExecutionLedger(self.ledger_path).history(namespace="security-scans")
            self.assertEqual(events[0]["status"], "completed")
            self.assertEqual(events[1]["status"], "started")
            self.assertEqual(events[0]["metadata"]["start_event_id"], events[1]["event_id"])

    def test_require_ledger_blocks_scan_when_start_cannot_be_recorded(self):
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"), \
             patch("nuclei_scanner.ExecutionLedger") as ledger:
            ledger.return_value.append.side_effect = OSError("ledger offline")
            result = scan_target(
                "http://127.0.0.1:8765", authorized=True,
                authorization_id="test-grant", require_ledger=True,
            )
        self.assertEqual(result["status"], "ledger_error")

    def test_timeout_termination_kills_process_group_on_posix(self):
        process = FakeProcess()
        process.pid = 4321
        with patch("nuclei_scanner.os.name", "posix"), patch(
            "nuclei_scanner.os.killpg"
        ) as killpg:
            _terminate_process_tree(process)
        killpg.assert_called_once_with(4321, signal.SIGKILL)

    def test_timeout_termination_falls_back_to_process_kill(self):
        process = FakeProcess()
        with patch("nuclei_scanner.os.name", "nt"):
            _terminate_process_tree(process)
        self.assertEqual(process.returncode, -9)

    def test_process_start_error_is_reported(self):
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
            with patch(
                "nuclei_scanner.subprocess.Popen",
                side_effect=OSError("No se pudo iniciar"),
            ):
                result = scan_target("http://127.0.0.1:8765", authorized=True, authorization_id="test-grant")

        self.assertEqual(result["status"], "error")
        self.assertIn("No se pudo iniciar", result["error"])

    def test_scan_rejects_invalid_rate_limits(self):
        with self.assertRaises(ValueError):
            scan_target("http://127.0.0.1:8765", rate_limit=0)
        with self.assertRaises(ValueError):
            scan_target("http://127.0.0.1:8765", concurrency=11)

    def test_missing_template_directory_is_reported_before_execution(self):
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
            result = scan_target(
                "http://127.0.0.1:8765", authorized=True,
                authorization_id="test-grant", templates_path="/missing/templates",
            )
        self.assertEqual(result["status"], "error")
        self.assertIn("plantillas", result["error"].lower())

    def test_nuclei_command_uses_full_template_directory_and_safe_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_file = Path(tmp) / "unused"
            captured = {}
            def fake_popen(command, **kwargs):
                captured["command"] = command
                output = Path(command[command.index("-o") + 1])
                output.write_text("", encoding="utf-8")
                return FakeProcess()
            with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"), \
                 patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen), \
                 patch("nuclei_scanner.time.sleep"):
                result = scan_target(
                    "http://127.0.0.1:8765", authorized=True,
                    authorization_id="test-grant", rate_limit=3, concurrency=1,
                )
            command = captured["command"]
            self.assertIn(str(self.templates.resolve()), command)
            self.assertIn("-disable-unsigned-templates", command)
            self.assertIn("-no-stdin", command)
            self.assertEqual(command[command.index("-type") + 1], "http")
            self.assertIn("dos,intrusive,fuzz,code,headless", command)
            self.assertEqual(result["rate_limit"], 3)
            self.assertEqual(result["concurrency"], 1)


if __name__ == "__main__":
    unittest.main()
