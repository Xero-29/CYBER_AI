import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from binary_integrity import (
    BinaryIntegrityError,
    build_minimal_environment,
    hash_executable,
    require_approved_executable,
)
from tool_allowlist import ToolAllowlistError


class BinaryIntegrityTests(unittest.TestCase):
    def test_hashes_regular_file_deterministically(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "tool"
            executable.write_bytes(b"test executable\n")
            first = hash_executable(executable)
            second = hash_executable(executable)
            self.assertEqual(first, second)
            self.assertEqual(len(first["sha256"]), 64)
            self.assertEqual(first["resolved_path"], str(executable.resolve()))

    def test_rejects_non_regular_file(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(BinaryIntegrityError):
                hash_executable(temp)

    def test_rejects_empty_file(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "empty"
            executable.touch()
            with self.assertRaises(BinaryIntegrityError):
                hash_executable(executable)

    def test_rejects_oversized_file(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "large"
            executable.write_bytes(b"x" * 16)
            with patch("binary_integrity.MAX_EXECUTABLE_BYTES", 8):
                with self.assertRaises(BinaryIntegrityError):
                    hash_executable(executable)

    def test_detects_path_replacement_after_open(self):
        if os.name != "posix":
            self.skipTest("La sustitución de archivo abierto se prueba en POSIX.")
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "tool"
            executable.write_bytes(b"original")
            real_open = os.open

            def replace_after_open(path, flags):
                descriptor = real_open(path, flags)
                executable.unlink()
                executable.write_bytes(b"replacement")
                return descriptor

            with patch("binary_integrity.os.open", side_effect=replace_after_open):
                with self.assertRaises(BinaryIntegrityError):
                    hash_executable(executable)

    def test_accepts_symlink_only_by_hashing_resolved_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "real-tool"
            target.write_bytes(b"tool")
            link = root / "tool"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            result = hash_executable(link)
            self.assertEqual(result["resolved_path"], str(target.resolve()))



    def test_active_scanner_requires_signed_allowlist(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "nuclei"
            executable.write_bytes(b"nuclei")
            with patch("binary_integrity.verify_tool_allowed", return_value={
                "enforced": True, "status": "approved", "sha256": "a" * 64,
            }):
                result = require_approved_executable(executable, "nuclei")
            self.assertTrue(result["allowlist"]["enforced"])

            with patch("binary_integrity.verify_tool_allowed", return_value={
                "enforced": False, "status": "not_configured",
            }):
                with self.assertRaisesRegex(BinaryIntegrityError, "allowlist firmada"):
                    require_approved_executable(executable, "nuclei")

    def test_active_scanner_rejects_unapproved_binary(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "nuclei"
            executable.write_bytes(b"nuclei")
            with patch("binary_integrity.verify_tool_allowed", side_effect=ToolAllowlistError("denied")):
                with self.assertRaises(BinaryIntegrityError):
                    require_approved_executable(executable, "nuclei")


    def test_minimal_environment_excludes_application_secrets_and_proxy_settings(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / "nuclei"
            executable.write_bytes(b"nuclei-test-binary")
            with patch.dict(os.environ, {
                "OPENAI_API_KEY": "must-not-be-forwarded",
                "AWS_SECRET_ACCESS_KEY": "must-not-be-forwarded",
                "HTTPS_PROXY": "http://proxy.invalid",
                "PATH": "/attacker/path",
                "LANG": "C.UTF-8",
            }):
                env = build_minimal_environment(temp, str(executable))
        self.assertEqual(env["HOME"], str(Path(temp).resolve()))
        self.assertEqual(env["TMPDIR"], env["HOME"])
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", env)
        self.assertNotIn("HTTPS_PROXY", env)
        self.assertNotIn("/attacker/path", env["PATH"])
        self.assertIn("/usr/bin", env["PATH"])
        self.assertEqual(env["LANG"], "C.UTF-8")

if __name__ == "__main__":
    unittest.main()
