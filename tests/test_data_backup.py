import io
import json
import os
import shutil
import sqlite3
import stat
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import data_backup
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


    def create_unsigned_backup(self, destination, *, data_dir=None):
        return create_backup(
            data_dir or self.data, destination, allow_unsigned=True
        )

    def verify_unsigned_backup(self, snapshot):
        return verify_backup(snapshot, require_signature=False)

    def restore_unsigned_backup(self, *args, **kwargs):
        kwargs.setdefault("require_signature", False)
        return restore_backup(*args, **kwargs)


    def test_backup_verify_and_restore_preserves_sqlite_and_files(self):
        snapshot = self.root / "backup"
        source_mode = stat.S_IMODE((self.data / "memory.sqlite3").stat().st_mode)
        result = self.create_unsigned_backup(snapshot)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE((snapshot / "memory.sqlite3").stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE((self.data / "memory.sqlite3").stat().st_mode), source_mode)
        self.assertFalse(result["encrypted"])
        self.assertTrue(self.verify_unsigned_backup(snapshot)["valid"])
        with sqlite3.connect(self.data / "memory.sqlite3") as db:
            db.execute("UPDATE notes SET value='changed'")
        restored = self.restore_unsigned_backup(
            snapshot, self.data, confirm_quiesced=True, confirm_replace=True
        )
        self.assertTrue(restored["restored"])
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE((self.data / "memory.sqlite3").stat().st_mode), 0o600)
        with sqlite3.connect(self.data / "memory.sqlite3") as db:
            self.assertEqual(db.execute("SELECT value FROM notes").fetchone()[0], "verified")
        self.assertEqual((self.data / "events.jsonl").read_text(encoding="utf-8"), '{"event":"test"}\n')
        self.assertTrue(Path(restored["previous_data_preserved_at"]).is_dir())

    def test_rejects_oversized_manifest_before_json_parsing(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        manifest_path = snapshot / "manifest.json"
        with patch("data_backup.MAX_MANIFEST_BYTES", 32):
            manifest_path.write_bytes(b" " * 33)
            with self.assertRaisesRegex(BackupError, "16 MiB"):
                self.verify_unsigned_backup(snapshot)

    def test_manifest_duplicate_json_keys_are_rejected(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        (snapshot / "manifest.json").write_text(
            '{"schema":"cyber-ai-data-backup-v1",'
            '"schema":"cyber-ai-data-backup-v1",'
            '"files":[],"encrypted":false,"requires_quiesced_writers":true}',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(BackupError, "claves JSON duplicadas"):
            self.verify_unsigned_backup(snapshot)

    def test_manifest_rejects_non_finite_and_out_of_range_numbers(self):
        with patch.dict(os.environ, {}, clear=True):
            for number in ("NaN", "Infinity", "1e999", "-1e-999"):
                with self.subTest(number=number), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    data = root / "data"
                    data.mkdir()
                    (data / "sample.txt").write_text("safe", encoding="utf-8")
                    snapshot = root / "backup"
                    self.create_unsigned_backup(snapshot, data_dir=data)
                    manifest_path = snapshot / "manifest.json"
                    manifest_text = manifest_path.read_text(encoding="utf-8").rstrip()
                    manifest_path.write_text(
                        manifest_text[:-1] + ', "untrusted_score": ' + number + '}',
                        encoding="utf-8",
                    )
                    with self.assertRaises(BackupError):
                        self.verify_unsigned_backup(snapshot)

    def test_manifest_accepts_finite_exponent_values(self):
        with patch.dict(os.environ, {}, clear=True):
            snapshot = self.root / "finite-number-backup"
            self.create_unsigned_backup(snapshot, data_dir=self.data)
            manifest_path = snapshot / "manifest.json"
            manifest_text = manifest_path.read_text(encoding="utf-8").rstrip()
            manifest_path.write_text(
                manifest_text[:-1] + ', "untrusted_score": -1.25e2}',
                encoding="utf-8",
            )
            self.assertTrue(self.verify_unsigned_backup(snapshot)["valid"])

    def test_excessive_manifest_nesting_is_reported_as_backup_error(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        (snapshot / "manifest.json").write_text(
            '{"a":' * 2000 + "0" + "}" * 2000, encoding="utf-8"
        )
        with self.assertRaisesRegex(BackupError, "profundidad JSON"):
            self.verify_unsigned_backup(snapshot)

    def test_manifest_depth_scanner_ignores_delimiters_inside_strings(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["description"] = '[]{}"\\\\' * 256
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
        )
        self.assertTrue(self.verify_unsigned_backup(snapshot)["valid"])

    def test_backup_and_verifier_enforce_file_count_limit(self):
        snapshot = self.root / "backup"
        with patch("data_backup.MAX_BACKUP_FILES", 1):
            with self.assertRaisesRegex(BackupError, "límite de archivos"):
                self.create_unsigned_backup(snapshot, data_dir=self.data)
            self.assertFalse(snapshot.exists())

        snapshot = self.root / "valid-backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        with patch("data_backup.MAX_BACKUP_FILES", 1):
            with self.assertRaisesRegex(BackupError, "límite de archivos"):
                self.verify_unsigned_backup(snapshot)

    def test_detects_modified_backup_file(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        (snapshot / "events.jsonl").write_text("tampered", encoding="utf-8")
        with self.assertRaises(BackupError):
            self.verify_unsigned_backup(snapshot)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO solo está disponible en POSIX.")
    def test_rejects_fifo_sources_instead_of_blocking_on_copy(self):
        fifo = self.data / "named-pipe"
        os.mkfifo(fifo)
        snapshot = self.root / "fifo-backup"
        with self.assertRaisesRegex(BackupError, "archivos regulares"):
            self.create_unsigned_backup(snapshot, data_dir=self.data)
        self.assertFalse(snapshot.exists())
        self.assertEqual(list(self.root.glob(".fifo-backup.tmp-*")), [])

    def test_refuses_symlinks_in_data(self):
        (self.data / "outside").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(BackupError):
            self.create_unsigned_backup(self.root / "backup")

    def test_restore_requires_explicit_quiescence_and_replace(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        with self.assertRaises(BackupError):
            self.restore_unsigned_backup(snapshot, self.data)
        with self.assertRaises(BackupError):
            self.restore_unsigned_backup(snapshot, self.data, confirm_quiesced=True)


    def test_rejects_malformed_manifest_metadata(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["size"] = True
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(BackupError):
            self.verify_unsigned_backup(snapshot)

    def test_rejects_unlisted_files_and_reserved_manifest_path(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        (snapshot / "injected.txt").write_text("untracked", encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "no coincide"):
            self.verify_unsigned_backup(snapshot)

        (snapshot / "injected.txt").unlink()
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"].append({
            "path": "manifest.json", "kind": "file_copy_quiesced",
            "size": manifest_path.stat().st_size, "sha256": "0" * 64,
        })
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(BackupError):
            self.verify_unsigned_backup(snapshot)

    def test_rejects_noncanonical_and_conflicting_paths(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["path"] = "./" + manifest["files"][0]["path"]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(BackupError):
            self.verify_unsigned_backup(snapshot)

    def test_rejects_symlink_inside_backup(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        (snapshot / "escape").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(BackupError):
            self.verify_unsigned_backup(snapshot)


    def test_restore_rejects_manifest_symlink_swap_after_verification(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
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
                self.restore_unsigned_backup(
                    snapshot, self.data, confirm_quiesced=True, confirm_replace=True
                )
        self.assertEqual(
            (self.data / "events.jsonl").read_text(encoding="utf-8"),
            '{"event":"test"}\n',
        )
        self.assertEqual(outside.read_text(encoding="utf-8"), "not a backup manifest")

    def test_restore_creates_missing_parent_and_rejects_overlap(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        destination = self.root / "new" / "nested" / "data"
        result = self.restore_unsigned_backup(snapshot, destination, confirm_quiesced=True)
        self.assertTrue(result["restored"])
        with sqlite3.connect(destination / "memory.sqlite3") as db:
            self.assertEqual(db.execute("SELECT value FROM notes").fetchone()[0], "verified")
        with self.assertRaises(BackupError):
            self.restore_unsigned_backup(snapshot, snapshot / "inside", confirm_quiesced=True)

    def test_hmac_signature_is_verified_and_required_when_requested(self):
        key = "backup-signing-key-with-at-least-32-bytes"
        snapshot = self.root / "signed-backup"
        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": key}):
            result = self.create_unsigned_backup(snapshot, data_dir=self.data)
            self.assertTrue(result["signed"])
            self.assertTrue(verify_backup(snapshot, require_signature=True)["signed"])

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(BackupError, "falta CYBER_AI_BACKUP_HMAC_KEY"):
                self.verify_unsigned_backup(snapshot)

        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": "different-key-with-at-least-32-bytes"}):
            with self.assertRaisesRegex(BackupError, "firma HMAC"):
                self.verify_unsigned_backup(snapshot)

    def test_unsigned_backup_is_rejected_when_signature_is_required(self):
        snapshot = self.root / "unsigned-backup"
        with patch.dict(os.environ, {}, clear=True):
            result = self.create_unsigned_backup(snapshot, data_dir=self.data)
            self.assertFalse(result["signed"])
            with self.assertRaisesRegex(BackupError, "no tiene firma"):
                verify_backup(snapshot, require_signature=True)

    def test_short_hmac_key_is_rejected_before_backup_creation(self):
        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": "too-short"}):
            with self.assertRaisesRegex(BackupError, "al menos 32 bytes"):
                self.create_unsigned_backup(self.root / "invalid-backup")

    def test_restore_detects_source_changes_after_verification(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        original_copy = __import__("data_backup")._copy_regular_file

        def mutate_before_copy(source, target):
            if Path(source) == snapshot / "events.jsonl":
                Path(source).write_text("tampered", encoding="utf-8")
            return original_copy(source, target)

        with patch("data_backup._copy_regular_file", side_effect=mutate_before_copy):
            with self.assertRaisesRegex(BackupError, "cambió durante la restauración"):
                self.restore_unsigned_backup(
                    snapshot, self.data, confirm_quiesced=True, confirm_replace=True
                )
        self.assertEqual(
            (self.data / "events.jsonl").read_text(encoding="utf-8"),
            '{"event":"test"}\n',
        )


    @unittest.skipUnless(os.name == "posix", "Los enlaces duros se validan en POSIX.")
    def test_rejects_hard_link_file_inside_backup(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        target = snapshot / "events.jsonl"
        os.link(target, self.root / "outside-hard-link")
        with self.assertRaisesRegex(BackupError, "enlaces duros"):
            self.verify_unsigned_backup(snapshot)

    def test_rejects_symlink_swap_between_inspection_and_open(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
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
                self.verify_unsigned_backup(snapshot)
        self.assertEqual(outside.read_text(encoding="utf-8"), "outside")

    def test_rejects_symlink_file_inside_backup(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        target = snapshot / "events.jsonl"
        target.unlink()
        target.symlink_to(self.root / "outside.txt")
        (self.root / "outside.txt").write_text("outside", encoding="utf-8")
        with self.assertRaises(BackupError):
            self.verify_unsigned_backup(snapshot)

    def test_rejects_parent_traversal_in_manifest(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["path"] = "../outside"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "Ruta insegura"):
            self.verify_unsigned_backup(snapshot)

    def test_signed_manifest_tampering_is_detected(self):
        key = "backup-signing-key-with-at-least-32-bytes"
        snapshot = self.root / "signed-backup"
        with patch.dict(os.environ, {"CYBER_AI_BACKUP_HMAC_KEY": key}):
            self.create_unsigned_backup(snapshot, data_dir=self.data)
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
                self.create_unsigned_backup(destination)
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
            self.create_unsigned_backup(self.root / "backup", data_dir=link / "data")

    def test_backup_rejects_symlinked_destination_parent(self):
        real_parent = self.root / "real-backups"
        real_parent.mkdir()
        link = self.root / "backup-link"
        self._symlink_directory(link, real_parent)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            self.create_unsigned_backup(link / "backup")
        self.assertFalse((real_parent / "backup").exists())

    def test_verify_rejects_symlinked_snapshot_ancestor(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        link = self.root / "snapshot-link"
        self._symlink_directory(link, self.root)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            self.verify_unsigned_backup(link / "backup")

    def test_restore_rejects_symlinked_destination_parent(self):
        snapshot = self.root / "backup"
        self.create_unsigned_backup(snapshot, data_dir=self.data)
        real_parent = self.root / "restore-parent"
        real_parent.mkdir()
        link = self.root / "restore-link"
        self._symlink_directory(link, real_parent)
        with self.assertRaisesRegex(BackupError, "symlinks"):
            self.restore_unsigned_backup(
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
                self.create_unsigned_backup(parent / "backup")
            self.assertFalse((parent / "backup").exists())
        finally:
            parent.chmod(original_mode)


    def test_cli_redacts_secrets_from_errors(self):
        secret = "backup-provider-secret"
        output = io.StringIO()
        with patch(
            "data_backup.verify_backup",
            side_effect=BackupError(f"Ruta insegura en manifiesto: token={secret}"),
        ), redirect_stderr(output):
            result = data_backup.main([
                "verify", "--snapshot", str(self.root / "snapshot")
            ])
        self.assertEqual(result, 2)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())

    def test_cli_redacts_secret_like_values_in_success_output(self):
        secret = "backup-path-secret"
        output = io.StringIO()
        with patch(
            "data_backup.create_backup",
            return_value={"destination": f"/tmp/api_key={secret}", "files": 1},
        ), patch("sys.stdout", output):
            result = data_backup.main([
                "--data-dir", str(self.data), "backup",
                "--destination", str(self.root / "snapshot"),
                "--confirm-quiesced", "--allow-unsigned",
            ])
        self.assertEqual(result, 0)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("[REDACTED]", output.getvalue())

    def test_backup_api_requires_signing_key_unless_unsigned_is_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(BackupError, "CYBER_AI_BACKUP_HMAC_KEY"):
                create_backup(self.data, self.root / "strict-backup")
            result = create_backup(
                self.data, self.root / "explicit-unsigned", allow_unsigned=True
            )
        self.assertFalse(result["signed"])

    def test_cli_requires_signature_and_explicit_unsigned_override(self):
        snapshot = self.root / "snapshot"
        output = io.StringIO()
        with patch("data_backup.verify_backup", return_value={"valid": True}) as verify, patch(
            "sys.stdout", output
        ):
            result = data_backup.main([
                "--data-dir", str(self.data), "verify", "--snapshot", str(snapshot)
            ])
        self.assertEqual(result, 0)
        verify.assert_called_once_with(snapshot, require_signature=True)

        with patch("data_backup.verify_backup", return_value={"valid": True}) as verify, patch(
            "sys.stdout", io.StringIO()
        ):
            result = data_backup.main([
                "--data-dir", str(self.data), "verify", "--snapshot", str(snapshot),
                "--allow-unsigned",
            ])
        self.assertEqual(result, 0)
        verify.assert_called_once_with(snapshot, require_signature=False)

    def test_cli_requires_signing_key_for_backup_unless_explicitly_unsigned(self):
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch(
            "data_backup.create_backup"
        ) as create, redirect_stderr(output):
            result = data_backup.main([
                "--data-dir", str(self.data), "backup",
                "--destination", str(self.root / "backup"),
                "--confirm-quiesced",
            ])
        self.assertEqual(result, 2)
        create.assert_not_called()
        self.assertIn("CYBER_AI_BACKUP_HMAC_KEY", output.getvalue())

    def test_backup_and_restore_security_overrides_require_real_booleans(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(BackupError, "booleano explícito"):
                create_backup(
                    self.data, self.root / "truthy-unsigned", allow_unsigned="true"
                )

        snapshot = self.root / "unsigned-flags"
        self.create_unsigned_backup(snapshot)
        with self.assertRaisesRegex(BackupError, "booleano explícito"):
            verify_backup(snapshot, require_signature=0)
        with self.assertRaisesRegex(BackupError, "booleanos explícitos"):
            restore_backup(
                snapshot,
                self.data,
                confirm_quiesced=True,
                confirm_replace="false",
                require_signature=False,
            )
        with self.assertRaisesRegex(BackupError, "booleanos explícitos"):
            restore_backup(
                snapshot,
                self.data,
                confirm_quiesced=True,
                confirm_replace=True,
                require_signature=0,
            )
        self.assertEqual(
            (self.data / "events.jsonl").read_text(encoding="utf-8"),
            '{"event":"test"}\n',
        )

    def test_restore_api_requires_signature_by_default(self):
        snapshot = self.root / "unsigned-restore"
        self.create_unsigned_backup(snapshot)
        with self.assertRaisesRegex(BackupError, "no tiene firma"):
            restore_backup(
                snapshot, self.data, confirm_quiesced=True, confirm_replace=True
            )

    def test_restore_cli_requires_signature_by_default(self):
        snapshot = self.root / "snapshot"
        with patch(
            "data_backup.restore_backup", return_value={"restored": True}
        ) as restore, patch("sys.stdout", io.StringIO()):
            result = data_backup.main([
                "--data-dir", str(self.data), "restore",
                "--snapshot", str(snapshot),
                "--confirm-quiesced", "--confirm-replace",
            ])
        self.assertEqual(result, 0)
        restore.assert_called_once_with(
            snapshot,
            self.data,
            confirm_quiesced=True,
            confirm_replace=True,
            require_signature=True,
        )

if __name__ == "__main__":
    unittest.main()
