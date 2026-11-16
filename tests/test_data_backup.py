import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from data_backup import BackupError, create_backup, restore_backup, verify_backup


class DataBackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data = self.root / "data"
        self.data.mkdir()
        with sqlite3.connect(self.data / "memory.sqlite3") as db:
            db.execute("CREATE TABLE notes(value TEXT)")
            db.execute("INSERT INTO notes VALUES('verified')")
        (self.data / "events.jsonl").write_text('{"event":"test"}\n', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_backup_verify_and_restore_preserves_sqlite_and_files(self):
        snapshot = self.root / "backup"
        result = create_backup(self.data, snapshot)
        self.assertFalse(result["encrypted"])
        self.assertTrue(verify_backup(snapshot)["valid"])
        with sqlite3.connect(self.data / "memory.sqlite3") as db:
            db.execute("UPDATE notes SET value='changed'")
        restored = restore_backup(
            snapshot, self.data, confirm_quiesced=True, confirm_replace=True
        )
        self.assertTrue(restored["restored"])
        with sqlite3.connect(self.data / "memory.sqlite3") as db:
            self.assertEqual(db.execute("SELECT value FROM notes").fetchone()[0], "verified")
        self.assertEqual((self.data / "events.jsonl").read_text(encoding="utf-8"), '{"event":"test"}\n')
        self.assertTrue(Path(restored["previous_data_preserved_at"]).is_dir())

    def test_detects_modified_backup_file(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        (snapshot / "events.jsonl").write_text("tampered", encoding="utf-8")
        with self.assertRaises(BackupError):
            verify_backup(snapshot)

    def test_refuses_symlinks_in_data(self):
        (self.data / "outside").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(BackupError):
            create_backup(self.data, self.root / "backup")

    def test_restore_requires_explicit_quiescence_and_replace(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        with self.assertRaises(BackupError):
            restore_backup(snapshot, self.data)
        with self.assertRaises(BackupError):
            restore_backup(snapshot, self.data, confirm_quiesced=True)


if __name__ == "__main__":
    unittest.main()
