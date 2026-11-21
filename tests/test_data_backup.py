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

    def test_manifest_duplicate_json_keys_are_rejected(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        (snapshot / "manifest.json").write_text(
            '{"schema":"cyber-ai-data-backup-v1",'
            '"schema":"cyber-ai-data-backup-v1",'
            '"files":[],"encrypted":false,"requires_quiesced_writers":true}',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(BackupError, "claves JSON duplicadas"):
            verify_backup(snapshot)

    def test_excessive_manifest_nesting_is_reported_as_backup_error(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        (snapshot / "manifest.json").write_text(
            '{"a":' * 2000 + "0" + "}" * 2000, encoding="utf-8"
        )
        with self.assertRaisesRegex(BackupError, "profundidad JSON"):
            verify_backup(snapshot)

    def test_manifest_depth_scanner_ignores_delimiters_inside_strings(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["description"] = '[]{}"\\\\' * 256
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
        )
        self.assertTrue(verify_backup(snapshot)["valid"])

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

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO solo está disponible en POSIX.")
    def test_rejects_fifo_sources_instead_of_blocking_on_copy(self):
        fifo = self.data / "named-pipe"
        os.mkfifo(fifo)
        snapshot = self.root / "fifo-backup"
        with self.assertRaisesRegex(BackupError, "archivos regulares"):
            create_backup(self.data, snapshot)
        self.assertFalse(snapshot.exists())
        self.assertEqual(list(self.root.glob(".fifo-backup.tmp-*")), [])

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


    def test_restore_rejects_manifest_symlink_swap_after_verification(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        manifest_path = snapshot / "manifest.json"
        outside = self.root / "outside-manifest.json"
        outside.write_text("not a backup manifest", encoding="utf-8")
        real_open = os.open
        manifest_opens = {"count": 0}

        def swap_on_restore(path, flags, *args, **kwargs):
            if Path(path) == manifest_path:
                manifest_opens["count"] += 1
                if manifest_opens["count"] == 2:
                    manifest_path.unlink()
                    manifest_path.symlink_to(outside)
            return real_open(path, flags, *args, **kwargs)

        with patch("data_backup.os.open", side_effect=swap_on_restore):
            with self.assertRaises(BackupError):
                restore_backup(
                    snapshot, self.data, confirm_quiesced=True, confirm_replace=True
                )
        self.assertEqual(
            (self.data / "events.jsonl").read_text(encoding="utf-8"),
            '{"event":"test"}\n',
        )
        self.assertEqual(outside.read_text(encoding="utf-8"), "not a backup manifest")

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
        original_copy = __import__("data_backup")._copy_regular_file

        def mutate_before_copy(source, target):
            if Path(source) == snapshot / "events.jsonl":
                Path(source).write_text("tampered", encoding="utf-8")
            return original_copy(source, target)

        with patch("data_backup._copy_regular_file", side_effect=mutate_before_copy):
            with self.assertRaisesRegex(BackupError, "cambió durante la restauración"):
                restore_backup(
                    snapshot, self.data, confirm_quiesced=True, confirm_replace=True
                )
        self.assertEqual(
            (self.data / "events.jsonl").read_text(encoding="utf-8"),
            '{"event":"test"}\n',
        )


    @unittest.skipUnless(os.name == "posix", "Los enlaces duros se validan en POSIX.")
    def test_rejects_hard_link_file_inside_backup(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        target = snapshot / "events.jsonl"
        os.link(target, self.root / "outside-hard-link")
        with self.assertRaisesRegex(BackupError, "enlaces duros"):
            verify_backup(snapshot)

    def test_rejects_symlink_swap_between_inspection_and_open(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        target = snapshot / "events.jsonl"
        outside = self.root / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        real_open = os.open
        swapped = {"value": False}

        def swap_then_open(path, flags, *args, **kwargs):
            if Path(path) == target and not swapped["value"]:
                swapped["value"] = True
                target.unlink()
                target.symlink_to(outside)
            return real_open(path, flags, *args, **kwargs)

        with patch("data_backup.os.open", side_effect=swap_then_open):
            with self.assertRaises(BackupError):
                verify_backup(snapshot)
        self.assertEqual(outside.read_text(encoding="utf-8"), "outside")

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

    def _symlink_directory(self, link, target):
        try:
            link.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Los symlinks de directorio no están disponibles.")

    def test_backup_rejects_symlinked_data_ancestor(self):
        link = self.root / "data-link"
        self._symlink_directory(link, self.root)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            create_backup(link / "data", self.root / "backup")

    def test_backup_rejects_symlinked_destination_parent(self):
        real_parent = self.root / "real-backups"
        real_parent.mkdir()
        link = self.root / "backup-link"
        self._symlink_directory(link, real_parent)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            create_backup(self.data, link / "backup")
        self.assertFalse((real_parent / "backup").exists())

    def test_verify_rejects_symlinked_snapshot_ancestor(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        link = self.root / "snapshot-link"
        self._symlink_directory(link, self.root)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            verify_backup(link / "backup")

    def test_restore_rejects_symlinked_destination_parent(self):
        snapshot = self.root / "backup"
        create_backup(self.data, snapshot)
        real_parent = self.root / "restore-parent"
        real_parent.mkdir()
        link = self.root / "restore-link"
        self._symlink_directory(link, real_parent)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            restore_backup(
                snapshot, link / "data", confirm_quiesced=True
            )
        self.assertFalse((real_parent / "data").exists())

    @unittest.skipUnless(os.name == "posix", "Los permisos POSIX se prueban en POSIX.")
    def test_backup_rejects_untrusted_writable_destination_parent(self):
        parent = self.root / "world-writable"
        parent.mkdir()
        original_mode = parent.stat().st_mode & 0o777
        try:
            parent.chmod(0o777)
            with self.assertRaisesRegex(BackupError, "modificables por terceros"):
                create_backup(self.data, parent / "backup")
            self.assertFalse((parent / "backup").exists())
        finally:
            parent.chmod(original_mode)


if __name__ == "__main__":
    unittest.main()
