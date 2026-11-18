import json
import os
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_rejects_oversized_manifest_before_json_parsing(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        manifest_path = snapshot / "manifest.json"
        with patch("data_backup.MAX_MANIFEST_BYTES", 32):
            manifest_path.write_bytes(b" " * 33)
            with self.assertRaisesRegex(BackupError, "16 MiB"):
                verify_backup(snapshot)

    def test_backup_and_verifier_enforce_file_count_limit(self):
        snapshot = self.root / "backup"
        with patch("data_backup.MAX_BACKUP_FILES", 1):
            with self.assertRaisesRegex(BackupError, "límite de archivos"):
                create_backup(self.data, snapshot)
            self.assertFalse(snapshot.exists())

        snapshot = self.root / "valid-backup"
        create_backup(self.data, snapshot)
        with patch("data_backup.MAX_BACKUP_FILES", 1):
            with self.assertRaisesRegex(BackupError, "límite de archivos"):
                verify_backup(snapshot)

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


    def test_rejects_malformed_manifest_metadata(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["size"] = True
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(BackupError):
            verify_backup(snapshot)

    def test_rejects_unlisted_files_and_reserved_manifest_path(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        (snapshot / "injected.txt").write_text("untracked", encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "no coincide"):
            verify_backup(snapshot)

        (snapshot / "injected.txt").unlink()
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"].append({
            "path": "manifest.json", "kind": "file_copy_quiesced",
            "size": manifest_path.stat().st_size, "sha256": "0" * 64,
        })
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(BackupError):
            verify_backup(snapshot)

    def test_rejects_noncanonical_and_conflicting_paths(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["path"] = "./" + manifest["files"][0]["path"]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(BackupError):
            verify_backup(snapshot)

    def test_rejects_symlink_inside_backup(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        (snapshot / "escape").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(BackupError):
            verify_backup(snapshot)


    def test_restore_creates_missing_parent_and_rejects_overlap(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        destination = self.root / "new" / "nested" / "data"
        result = restore_backup(snapshot, destination, confirm_quiesced=True)
        self.assertTrue(result["restored"])
        with sqlite3.connect(destination / "memory.sqlite3") as db:
            self.assertEqual(db.execute("SELECT value FROM notes").fetchone()[0], "verified")
        with self.assertRaises(BackupError):
            restore_backup(snapshot, snapshot / "inside", confirm_quiesced=True)

    def test_hmac_signature_is_verified_and_required_when_requested(self):
        key = "backup-signing-key-with-at-least-32-bytes"
        snapshot = self.root / "signed-backup"
        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": key}):
            result = create_backup(self.data, snapshot)
            self.assertTrue(result["signed"])
            self.assertTrue(verify_backup(snapshot, require_signature=True)["signed"])

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(BackupError, "falta CYBER_AI_BACKUP_HMAC_KEY"):
                verify_backup(snapshot)

        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": "different-key-with-at-least-32-bytes"}):
            with self.assertRaisesRegex(BackupError, "firma HMAC"):
                verify_backup(snapshot)

    def test_unsigned_backup_is_rejected_when_signature_is_required(self):
        snapshot = self.root / "unsigned-backup"
        with patch.dict(os.environ, {}, clear=True):
            result = create_backup(self.data, snapshot)
            self.assertFalse(result["signed"])
            with self.assertRaisesRegex(BackupError, "no tiene firma"):
                verify_backup(snapshot, require_signature=True)

    def test_short_hmac_key_is_rejected_before_backup_creation(self):
        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": "too-short"}):
            with self.assertRaisesRegex(BackupError, "al menos 32 bytes"):
                create_backup(self.data, self.root / "invalid-backup")

    def test_restore_detects_source_changes_after_verification(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        original_copy = shutil.copy2

        def mutate_before_copy(source, target):
            if Path(source) == snapshot / "events.jsonl":
                Path(source).write_text("tampered", encoding="utf-8")
            return original_copy(source, target)

        with patch("data_backup.shutil.copy2", side_effect=mutate_before_copy):
            with self.assertRaisesRegex(BackupError, "cambió durante la restauración"):
                restore_backup(
                    snapshot, self.data, confirm_quiesced=True, confirm_replace=True
                )
        self.assertEqual(
            (self.data / "events.jsonl").read_text(encoding="utf-8"),
            '{"event":"test"}\n',
        )


    def test_rejects_symlink_file_inside_backup(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        target = snapshot / "events.jsonl"
        target.unlink()
        target.symlink_to(self.root / "outside.txt")
        (self.root / "outside.txt").write_text("outside", encoding="utf-8")
        with self.assertRaises(BackupError):
            verify_backup(snapshot)

    def test_rejects_parent_traversal_in_manifest(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["path"] = "../outside"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "Ruta insegura"):
            verify_backup(snapshot)

    def test_signed_manifest_tampering_is_detected(self):
        key = "backup-signing-key-with-at-least-32-bytes"
        snapshot = self.root / "signed-backup"
        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": key}):
            create_backup(self.data, snapshot)
            manifest_path = snapshot / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["created_at"] = "2000-01-01T00:00:00+00:00"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(BackupError, "HMAC"):
                verify_backup(snapshot, require_signature=True)

    def test_failed_atomic_publish_cleans_staging_directory(self):
        destination = self.root / "backup"
        with patch("data_backup.os.replace", side_effect=OSError("simulated publish failure")):
            with self.assertRaisesRegex(OSError, "simulated publish failure"):
                create_backup(self.data, destination)
        self.assertFalse(destination.exists())
        self.assertEqual(list(self.root.glob(".backup.tmp-*")), [])

if __name__ == "__main__":
    unittest.main()
