import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from safe_io import SafeWriteError, atomic_write_text, ensure_private_directory, open_private_file


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

    @unittest.skipIf(os.name == "nt", "La propiedad POSIX no se valida en Windows.")
    def test_private_directory_must_belong_to_effective_user(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "private"
            directory.mkdir(mode=0o700)
            other_uid = os.geteuid() + 1
            with patch("safe_io.os.geteuid", return_value=other_uid):
                with self.assertRaisesRegex(SafeWriteError, "usuario efectivo"):
                    ensure_private_directory(directory)

    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_private_directory_rejects_group_writable_parent(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "group-writable"
            parent.mkdir(mode=0o770)
            parent.chmod(0o770)
            directory = parent / "private"
            directory.mkdir(mode=0o700)
            with self.assertRaisesRegex(SafeWriteError, "directorio padre"):
                ensure_private_directory(directory)

    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_private_directory_accepts_root_owned_sticky_parent(self):
        parent = Path(tempfile.gettempdir())
        parent_info = parent.stat()
        if (
            parent_info.st_uid != 0
            or not (parent_info.st_mode & stat.S_ISVTX)
        ):
            self.skipTest("el directorio temporal no es root-owned sticky")
        with tempfile.TemporaryDirectory(dir=parent) as temp:
            directory = Path(temp)
            self.assertEqual(
                ensure_private_directory(directory, create=False), directory
            )
            self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)

    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_private_directory_rejects_world_writable_parent_without_sticky_bit(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "world-writable"
            parent.mkdir(mode=0o700)
            parent.chmod(0o777)
            directory = parent / "private"
            directory.mkdir(mode=0o700)
            with self.assertRaisesRegex(SafeWriteError, "directorio padre"):
                ensure_private_directory(directory)

    def test_open_private_file_appends_and_reads_with_private_permissions(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "data" / "events.jsonl"
            with open_private_file(path, "a") as stream:
                stream.write('{"event":1}\\n')
            with open_private_file(path, "r") as stream:
                self.assertEqual(stream.read(), '{"event":1}\\n')
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO solo disponible en POSIX.")
    def test_open_private_file_rejects_fifo_before_open(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "data" / "stream.fifo"
            path.parent.mkdir(mode=0o700)
            os.mkfifo(path, 0o600)
            with self.assertRaisesRegex(SafeWriteError, "archivo privado debe ser regular"):
                with open_private_file(path, "r"):
                    pass

    def test_open_private_file_rejects_symlink_and_hard_link(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "target.jsonl"
            target.write_text('{"secret":"private"}\\n', encoding="utf-8")
            symlink = root / "symlink.jsonl"
            hardlink = root / "hardlink.jsonl"
            try:
                symlink.symlink_to(target)
                os.link(target, hardlink)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks or hard links unavailable")
            with self.assertRaises(SafeWriteError):
                with open_private_file(symlink, "r"):
                    pass
            if os.name == "posix":
                with self.assertRaisesRegex(SafeWriteError, "enlaces duros"):
                    with open_private_file(hardlink, "r"):
                        pass

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


    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_atomic_write_rejects_group_writable_parent(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "shared"
            parent.mkdir(mode=0o700)
            parent.chmod(0o770)
            with self.assertRaisesRegex(SafeWriteError, "modificables por terceros"):
                atomic_write_text(parent / "private.json", "{}")
            self.assertFalse((parent / "private.json").exists())

    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_atomic_write_creates_private_parent_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "new" / "nested" / "report.json"
            atomic_write_text(destination, "{}", create_parents=True)
            for directory in (destination.parent, destination.parent.parent):
                self.assertEqual(stat.S_IMODE(directory.stat().st_mode) & 0o077, 0)

    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_atomic_write_accepts_root_owned_sticky_ancestor(self):
        parent = Path(tempfile.gettempdir())
        info = parent.stat()
        if info.st_uid != 0 or not (info.st_mode & stat.S_ISVTX):
            self.skipTest("el directorio temporal no es root-owned sticky")
        with tempfile.TemporaryDirectory(dir=parent) as temp:
            destination = Path(temp) / "private.json"
            atomic_write_text(destination, "{}")
            self.assertEqual(destination.read_text(encoding="utf-8"), "{}")

if __name__ == "__main__":
    unittest.main()
