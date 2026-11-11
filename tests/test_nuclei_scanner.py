import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from nuclei_scanner import scan_target, validate_target


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
    def test_scan_requires_explicit_authorization(self):
        result = scan_target("http://127.0.0.1:8765")
        self.assertEqual(result["status"], "authorization_required")
        self.assertEqual(result["findings"], [])

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
            result = scan_target("http://127.0.0.1:8765", authorized=True)

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
                    with patch("nuclei_scanner.Path.home", return_value=root):
                        with patch("nuclei_scanner.time.sleep"):
                            result = scan_target("http://127.0.0.1:8765")

            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["findings_count"], 1)
            self.assertEqual(result["findings"][0]["template-id"], "test-template")

    def test_process_start_error_is_reported(self):
        with patch("nuclei_scanner.shutil.which", return_value="/usr/bin/nuclei"):
            with patch(
                "nuclei_scanner.subprocess.Popen",
                side_effect=OSError("No se pudo iniciar"),
            ):
                result = scan_target("http://127.0.0.1:8765")

        self.assertEqual(result["status"], "error")
        self.assertIn("No se pudo iniciar", result["error"])


if __name__ == "__main__":
    unittest.main()
