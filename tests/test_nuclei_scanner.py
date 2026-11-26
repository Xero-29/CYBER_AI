import io
import json
import os
import tempfile
import threading
import unittest
from pathlib import Path
import signal
from unittest.mock import patch

from nuclei_scanner import (
    scan_target,
    validate_target,
    _close_process_output,
    _inspect_output_file,
    _iter_output_chunks,
    _sanitize_console_text,
    _terminate_process_tree,
    MAX_SCAN_OUTPUT_BYTES,
)
from execution_ledger import ExecutionLedger
from binary_integrity import BinaryIntegrityError
from execution_policy import AuthorizationError
from template_integrity import TemplateIntegrityError


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
        self.template_allowlist = patch(
            "nuclei_scanner.verify_approved_templates",
            return_value={"enforced": True, "approved_template_ids": ["test-template"]},
        )
        self.template_allowlist.start()

    def tearDown(self):
        self.template_allowlist.stop()
        self.authorization.stop()
        self.ledger_env.stop()
        self.temp.cleanup()

    @staticmethod
    def _create_templates(home):
        root = Path(home) / "nuclei-templates"
        paths = [
            root / "http/technologies/bulma-detect.yaml",
            root / "http/misconfiguration/http-missing-security-headers.yaml",
        ]
        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("id: test-template\ninfo:\n  name: test\n  severity: info\n", encoding="utf-8")
        return paths

    def test_scan_fails_closed_without_windows_job_object(self):
        with patch("nuclei_scanner.authorize_target", return_value={"authorization_id": "grant"}):
            with patch("nuclei_scanner.os.name", "nt"):
                with patch("nuclei_scanner.ExecutionLedger") as ledger:
                    ledger.return_value.append.return_value = {"event_id": "terminal"}
                    with patch("nuclei_scanner.shutil.which") as which:
                        result = scan_target(
                            "http://127.0.0.1:8765",
                            authorized=True,
                            authorization_id="test-grant",
                        )
        self.assertEqual(result["status"], "isolation_required")
        which.assert_not_called()

    def test_grant_revoked_during_preflight_blocks_process_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(root)
            reports = root / "reports"
            reports.mkdir()
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            with (
                patch(
                    "nuclei_scanner.authorize_target",
                    side_effect=[
                        {"authorization_id": "test-grant"},
                        AuthorizationError("revoked"),
                    ],
                ) as authorize,
                patch("nuclei_scanner.shutil.which", return_value=str(executable)),
                patch("nuclei_scanner.require_approved_executable", return_value=provenance),
                patch("nuclei_scanner.Path.home", return_value=root),
                patch("nuclei_scanner.ensure_private_directory", return_value=reports),
                patch("nuclei_scanner._record_scan_start", return_value="start-event"),
                patch(
                    "nuclei_scanner._finalize_scan",
                    side_effect=lambda target, result, *args, **kwargs: result,
                ),
                patch("nuclei_scanner.subprocess.Popen") as popen,
            ):
                result = scan_target(
                    "http://127.0.0.1:8765",
                    authorized=True,
                    authorization_id="test-grant",
                    require_ledger=False,
                )
            self.assertEqual(result["status"], "authorization_denied")
            self.assertEqual(
                result["reason"], "authorization_revoked_or_expired_before_launch"
            )
            self.assertEqual(authorize.call_count, 2)
            popen.assert_not_called()

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

    def test_validate_target_rejects_query_and_sensitive_path_values(self):
        for target in (
            "https://8.8.8.8/?token=secret-value",
            "https://8.8.8.8/token=secret-value",
        ):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    validate_target(target)

    def test_validate_target_rejects_dns_names_before_logging(self):
        with self.assertRaises(ValueError):
            validate_target("https://example.com")

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
            "api_key": "nuclei-finding-secret",
            "extracted-results": ["password=extracted-secret"],
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(root)
            fake_process = FakeProcess(stdout_lines=["Nuclei iniciado token=scanner-message-secret\n"])

            def fake_popen(command, **kwargs):
                output_index = command.index("-o") + 1
                Path(command[output_index]).write_text(
                    json.dumps(finding) + "\n",
                    encoding="utf-8",
                )
                return fake_process

            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            with patch("nuclei_scanner.shutil.which", return_value=str(executable)):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.hash_executable", return_value=provenance):
                        with patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen):
                            with patch("nuclei_scanner.Path.home", return_value=root):
                                with patch("nuclei_scanner.time.sleep"):
                                    result = scan_target("http://127.0.0.1:8765", authorized=True, authorization_id="test-grant")

            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["findings_count"], 1)
            self.assertEqual(result["findings"][0]["template-id"], "test-template")
            self.assertEqual(result["findings"][0]["api_key"], "[REDACTED]")
            serialized = json.dumps(result, ensure_ascii=False)
            for secret in (
                "nuclei-finding-secret", "extracted-secret", "scanner-message-secret"
            ):
                self.assertNotIn(secret, serialized)
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
        process.returncode = None
        with patch("nuclei_scanner.os.name", "nt"):
            _terminate_process_tree(process)
        self.assertEqual(process.returncode, -9)

    def test_output_file_monitor_enforces_size_and_regular_file_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nuclei.jsonl"
            output.write_bytes(b"x" * (MAX_SCAN_OUTPUT_BYTES + 1))
            self.assertEqual(_inspect_output_file(output), "over_limit")
            output.unlink()
            output.mkdir()
            self.assertEqual(_inspect_output_file(output), "invalid")

    def test_output_file_monitor_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside.jsonl"
            outside.write_text("{}", encoding="utf-8")
            link = root / "nuclei.jsonl"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            self.assertEqual(_inspect_output_file(link), "invalid")

    def test_output_chunks_are_bounded(self):
        stream = io.StringIO("x" * 5000 + "\n")
        chunks = list(_iter_output_chunks(stream, max_chars=2001))
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 2001 for chunk in chunks))

    def test_console_output_escapes_terminal_control_and_bidi_characters(self):
        untrusted = "safe\\x1b]52;c;clipboard\\x07\\u202e"
        self.assertEqual(
            _sanitize_console_text(untrusted),
            "safe\\\\u001b]52;c;clipboard\\\\u0007\\\\u202e",
        )

    def test_output_reader_is_closed_after_drain(self):
        process = FakeProcess()
        process.stdout = io.StringIO("scanner output\n")
        reader = threading.Thread(target=lambda: list(process.stdout), daemon=True)
        reader.start()
        _close_process_output(process, reader)
        self.assertTrue(process.stdout.closed)

    def test_stuck_output_reader_triggers_process_tree_cleanup(self):
        released = threading.Event()

        class BlockingStream:
            def readline(self, _size):
                released.wait(timeout=1)
                return ""

            def close(self):
                released.set()

        process = FakeProcess()
        process.pid = 1234
        process.stdout = BlockingStream()
        reader = threading.Thread(target=lambda: list(_iter_output_chunks(process.stdout)), daemon=True)
        reader.start()
        with patch("nuclei_scanner._terminate_process_tree") as terminate:
            _close_process_output(process, reader, join_timeout=0.01)
        terminate.assert_called_once_with(process)
        self.assertFalse(reader.is_alive())

    def test_process_start_error_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(root)
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            with patch("nuclei_scanner.shutil.which", return_value=str(executable)):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.Path.home", return_value=root):
                        with patch(
                            "nuclei_scanner.subprocess.Popen",
                            side_effect=OSError("No se pudo iniciar"),
                        ):
                            result = scan_target(
                                "http://127.0.0.1:8765",
                                authorized=True,
                                authorization_id="test-grant",
                            )

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error_type"], "OSError")
        self.assertEqual(result["reason"], "scanner_io_error")
        self.assertNotIn("error", result)



    def test_unexpected_scanner_exception_closes_ledger_without_leaking_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            home = root / "home"
            home.mkdir()
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(home)
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            old_cwd = os.getcwd()
            try:
                os.chdir(workspace)
                with (
                    patch("nuclei_scanner.shutil.which", return_value=str(executable)),
                    patch("nuclei_scanner.require_approved_executable", return_value=provenance),
                    patch("nuclei_scanner.Path.home", return_value=home),
                    patch(
                        "nuclei_scanner.subprocess.Popen",
                        side_effect=RuntimeError("scanner failed token=secret-value"),
                    ),
                    patch("nuclei_scanner.ExecutionLedger") as ledger,
                ):
                    ledger.return_value.append.side_effect = [
                        {"event_id": "start"},
                        {"event_id": "terminal"},
                    ]
                    result = scan_target(
                        "http://127.0.0.1:8765",
                        authorized=True,
                        authorization_id="test-grant",
                        require_ledger=True,
                    )
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error_type"], "RuntimeError")
        self.assertEqual(result["reason"], "scanner_execution_failed")
        self.assertNotIn("error", result)
        self.assertNotIn("secret-value", json.dumps(result))
        calls = ledger.return_value.append.call_args_list
        self.assertEqual([call.kwargs["status"] for call in calls], ["started", "failed"])
        self.assertEqual(calls[1].kwargs["metadata"]["start_event_id"], "start")

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
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(root)
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            fake_process = FakeProcess(stdout_lines=["Nuclei iniciado\n"])

            def fake_popen(command, **kwargs):
                output_index = command.index("-o") + 1
                Path(command[output_index]).write_text(json.dumps(finding) + "\n", encoding="utf-8")
                return fake_process

            with patch("nuclei_scanner.shutil.which", return_value=str(executable)):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.hash_executable", return_value={
                        "resolved_path": str(executable), "sha256": "b" * 64,
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




    def test_missing_or_unsafe_template_blocks_process_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            with patch("nuclei_scanner.shutil.which", return_value=str(executable)):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.Path.home", return_value=root):
                        with patch("nuclei_scanner.subprocess.Popen") as popen:
                            result = scan_target(
                                "http://127.0.0.1:8765",
                                authorized=True,
                                authorization_id="test-grant",
                            )
            self.assertEqual(result["status"], "template_denied")
            popen.assert_not_called()

    def test_unapproved_template_blocks_process_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(root)
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            with (
                patch("nuclei_scanner.shutil.which", return_value=str(executable)),
                patch("nuclei_scanner.require_approved_executable", return_value=provenance),
                patch("nuclei_scanner.Path.home", return_value=root),
                patch(
                    "nuclei_scanner.verify_approved_templates",
                    side_effect=TemplateIntegrityError("template not approved"),
                ),
                patch("nuclei_scanner.subprocess.Popen") as popen,
            ):
                result = scan_target(
                    "http://127.0.0.1:8765",
                    authorized=True,
                    authorization_id="test-grant",
                )
        self.assertEqual(result["status"], "template_denied")
        popen.assert_not_called()

    def test_template_replacement_discards_scan_findings(self):
        finding = {"template-id": "untrusted", "matched-at": "http://127.0.0.1:8765"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            templates = self._create_templates(root)
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            fake_process = FakeProcess(stdout_lines=["Nuclei iniciado\n"])

            def fake_popen(command, **kwargs):
                output_index = command.index("-o") + 1
                Path(command[output_index]).write_text(json.dumps(finding) + "\n", encoding="utf-8")
                templates[0].write_text("id: modified-template\n", encoding="utf-8")
                return fake_process

            with patch("nuclei_scanner.shutil.which", return_value=str(executable)):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.hash_executable", return_value=provenance):
                        with patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen):
                            with patch("nuclei_scanner.Path.home", return_value=root):
                                with patch("nuclei_scanner.time.sleep"):
                                    result = scan_target(
                                        "http://127.0.0.1:8765",
                                        authorized=True,
                                        authorization_id="test-grant",
                                    )
            self.assertEqual(result["status"], "integrity_error")
            self.assertTrue(result["templates_modified"])
            self.assertEqual(result["discarded_findings_count"], 1)
            self.assertEqual(result["findings"], [])

    def test_malformed_jsonl_is_rejected_as_invalid_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            self._create_templates(root)
            provenance = {
                "resolved_path": str(executable),
                "sha256": "a" * 64,
                "allowlist": {"enforced": True, "status": "approved"},
            }
            fake_process = FakeProcess(stdout_lines=["Nuclei iniciado\n"])

            def fake_popen(command, **kwargs):
                output_index = command.index("-o") + 1
                Path(command[output_index]).write_text("not-json\n", encoding="utf-8")
                return fake_process

            with patch("nuclei_scanner.shutil.which", return_value=str(executable)):
                with patch("nuclei_scanner.require_approved_executable", return_value=provenance):
                    with patch("nuclei_scanner.hash_executable", return_value=provenance):
                        with patch("nuclei_scanner.subprocess.Popen", side_effect=fake_popen):
                            with patch("nuclei_scanner.Path.home", return_value=root):
                                with patch("nuclei_scanner.time.sleep"):
                                    result = scan_target(
                                        "http://127.0.0.1:8765",
                                        authorized=True,
                                        authorization_id="test-grant",
                                    )
            self.assertEqual(result["status"], "evidence_invalid")
            self.assertEqual(result["findings"], [])

    def test_validate_target_rejects_control_characters_and_non_strings(self):
        for target in ("https://8.8.8.8\n", None, 123):
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
