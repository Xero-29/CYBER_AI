import json
import os
import tempfile
import unittest
from pathlib import Path
import signal
from unittest.mock import patch

from nuclei_scanner import scan_target, validate_target, _terminate_process_tree
from execution_ledger import ExecutionLedger
from binary_integrity import BinaryIntegrityError


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
        self.ledger_env = patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(self.ledger_path)})
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

            provenance = {
                "resolved_path": "/usr/bin/nuclei",
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.hash_executable", return_value=provenance):
                        with patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen):
                            with patch("nuclei_scanner.Path.home", return_value=root):
                                with patch("nuclei_scanner.time.sleep"):
                                    result = scan_target("http://127.0.0.1:8765", authorized=True, authorization_id="test-grant")

            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["findings_count"], 1)
            self.assertEqual(result["findings"][0]["template-id"], "test-template")
            events = ExecutionLedger(self.ledger_path).history(namespace="security-scans")
            self.assertEqual(events[0]["status"], "completed")
            self.assertEqual(events[1]["status"], "started")
            self.assertEqual(events[0]["metadata"]["start_event_id"], events[1]["event_id"])

    def test_require_ledger_blocks_scan_when_start_cannot_be_recorded(self):
        provenance = {
            "resolved_path": "/usr/bin/nuclei",
            "sha256": "a" * 64,
            "allowlist": {"enforced": True, "status": "approved"},
        }
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"), \
             patch("nuclei_scanner.require_approved_executable", return_value=provenance), \
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
        provenance = {
            "resolved_path": "/usr/bin/nuclei",
            "sha256": "a" * 64,
            "allowlist": {"enforced": True, "status": "approved"},
        }
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
            with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                with patch(
                    "nuclei_scanner.subprocess.Popen",
                    side_effect=OSError("No se pudo iniciar"),
                ):
                    result = scan_target("http://127.0.0.1:8765", authorized=True, authorization_id="test-grant")

        self.assertEqual(result["status"], "error")
        self.assertIn("No se pudo iniciar", result["error"])



    def test_unapproved_nuclei_binary_is_blocked_before_process_start(self):
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
            with patch(
                "nuclei_scanner.require_approved_executable",
                side_effect=BinaryIntegrityError("allowlist missing"),
            ):
                with patch("nuclei_scanner.subprocess.Popen") as popen:
                    result = scan_target(
                        "http://127.0.0.1:8765",
                        authorized=True,
                        authorization_id="test-grant",
                    )
        self.assertEqual(result["status"], "binary_denied")
        popen.assert_not_called()

    def test_binary_replacement_discards_scan_findings(self):
        finding = {"template-id": "untrusted", "matched-at": "http://127.0.0.1:8765"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            provenance = {
                "resolved_path": "/usr/bin/nuclei",
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            fake_process = FakeProcess(stdout_lines=["Nuclei iniciado\n"])

            def fake_popen(command, **kwargs):
                output_index = command.index("-o") + 1
                Path(command[output_index]).write_text(json.dumps(finding) + "\n", encoding="utf-8")
                return fake_process

            with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.hash_executable", return_value={
                        "resolved_path": "/usr/bin/nuclei", "sha256": "b" * 64,
                    }):
                        with patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen):
                            with patch("nuclei_scanner.Path.home", return_value=root):
                                with patch("nuclei_scanner.time.sleep"):
                                    result = scan_target(
                                        "http://127.0.0.1:8765",
                                        authorized=True,
                                        authorization_id="test-grant",
                                    )
            self.assertEqual(result["status"], "integrity_error")
            self.assertTrue(result["tool_binary_modified"])
            self.assertEqual(result["discarded_findings_count"], 1)
            self.assertEqual(result["findings"], [])


    def test_validate_target_rejects_control_characters_and_non_strings(self):
        for target in ("https://8.8.8.8\\n", None, 123):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    validate_target(target)

    def test_scan_rejects_out_of_range_timeout(self):
        with self.assertRaisesRegex(ValueError, "timeout"):
            scan_target(
                "http://127.0.0.1:8765",
                authorized=True,
                authorization_id="test-grant",
                timeout=0,
            )

if __name__ == "__main__":
    unittest.main()
