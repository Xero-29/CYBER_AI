import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from binary_integrity import BinaryIntegrityError, hash_executable


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


if __name__ == "__main__":
    unittest.main()
