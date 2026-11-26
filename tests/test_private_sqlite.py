import os
import stat
import tempfile
import unittest
from pathlib import Path

from private_sqlite import connect_private_sqlite
from safe_io import SafeWriteError


class PrivateSQLiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cyber-ai-private-sqlite-")
        self.root = Path(self.temp.name)
        self.database = self.root / "private.sqlite3"

    def tearDown(self):
        self.temp.cleanup()

    def test_creates_working_database_with_private_posix_permissions(self):
        connection = connect_private_sqlite(self.database)
        try:
            self.assertEqual(connection.execute("PRAGMA trusted_schema").fetchone()[0], 0)
            self.assertEqual(connection.execute("PRAGMA secure_delete").fetchone()[0], 1)
            self.assertEqual(connection.execute("PRAGMA foreign_keys").fetchone()[0], 1)
            connection.execute("CREATE TABLE sample (value TEXT NOT NULL)")
            connection.execute("INSERT INTO sample(value) VALUES (?)", ("ok",))
            self.assertEqual(
                connection.execute("SELECT value FROM sample").fetchone()[0],
                "ok",
            )
        finally:
            connection.close()

        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.root.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(self.database.stat().st_mode), 0o600)

    @unittest.skipUnless(os.name == "posix", "POSIX file permissions required")
    def test_existing_permissive_database_is_restricted(self):
        self.database.write_bytes(b"")
        os.chmod(self.database, 0o644)
        connection = connect_private_sqlite(self.database)
        connection.close()
        self.assertEqual(stat.S_IMODE(self.database.stat().st_mode), 0o600)

    def test_symlink_database_is_rejected(self):
        target = self.root / "outside.sqlite3"
        target.write_text("must remain unchanged", encoding="utf-8")
        try:
            self.database.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaises(SafeWriteError):
            connect_private_sqlite(self.database)
        self.assertEqual(target.read_text(encoding="utf-8"), "must remain unchanged")

    @unittest.skipUnless(os.name == "posix", "POSIX hardlink checks required")
    def test_hardlinked_database_is_rejected(self):
        target = self.root / "outside.sqlite3"
        target.write_bytes(b"")
        os.link(target, self.database)
        with self.assertRaisesRegex(SafeWriteError, "enlaces duros"):
            connect_private_sqlite(self.database)

    def test_symlink_sidecar_is_rejected(self):
        connection = connect_private_sqlite(self.database)
        connection.close()
        target = self.root / "outside-journal"
        target.write_text("do not follow", encoding="utf-8")
        sidecar = Path(f"{self.database}-wal")
        try:
            sidecar.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaises(SafeWriteError):
            connect_private_sqlite(self.database)
        self.assertEqual(target.read_text(encoding="utf-8"), "do not follow")

    def test_symlink_parent_directory_is_rejected(self):
        real = self.root / "real"
        real.mkdir()
        linked = self.root / "linked"
        try:
            linked.symlink_to(real, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks unavailable")
        with self.assertRaises(SafeWriteError):
            connect_private_sqlite(linked / "private.sqlite3")


if __name__ == "__main__":
    unittest.main()
