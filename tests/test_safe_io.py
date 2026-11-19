import os
import stat
import tempfile
import unittest
from pathlib import Path

from safe_io import SafeWriteError, atomic_write_text, ensure_private_directory


class SafeIoTests(unittest.TestCase):
    def test_atomic_write_creates_and_replaces_regular_file(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "manifest.json"
            atomic_write_text(destination, "first")
            atomic_write_text(destination, "second")
            self.assertEqual(destination.read_text(encoding="utf-8"), "second")
            leftovers = [item for item in Path(temp).iterdir() if item != destination]
            self.assertEqual(leftovers, [])
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o600)

    def test_symlink_destination_is_rejected_without_touching_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "protected.txt"
            target.write_text("original", encoding="utf-8")
            link = root / "output.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(SafeWriteError):
                atomic_write_text(link, "replacement")
            self.assertEqual(target.read_text(encoding="utf-8"), "original")

    def test_symlink_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "real"
            real.mkdir()
            link = root / "linked"
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(SafeWriteError):
                atomic_write_text(link / "manifest.json", "{}")

    def test_parent_creation_does_not_follow_symlink_components(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "real"
            real.mkdir()
            link = root / "linked"
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(SafeWriteError):
                atomic_write_text(
                    link / "new" / "manifest.json", "{}", create_parents=True
                )
            self.assertFalse((real / "new").exists())

    def test_parent_creation_is_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "new" / "nested" / "report.json"
            with self.assertRaises(SafeWriteError):
                atomic_write_text(destination, "{}")
            atomic_write_text(destination, "{}", create_parents=True)
            self.assertEqual(destination.read_text(encoding="utf-8"), "{}")

    def test_non_regular_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "directory"
            destination.mkdir()
            with self.assertRaises(SafeWriteError):
                atomic_write_text(destination, "no")



    def test_private_directory_is_created_and_restricted(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "reports" / "private"
            result = ensure_private_directory(directory)
            self.assertEqual(result, directory)
            self.assertTrue(directory.is_dir())
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)

    def test_private_directory_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "real"
            real.mkdir()
            link = root / "linked"
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(SafeWriteError):
                ensure_private_directory(link)

if __name__ == "__main__":
    unittest.main()
