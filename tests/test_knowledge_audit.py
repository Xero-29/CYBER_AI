import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from knowledge_audit import audit_database, audit_files


class KnowledgeAuditSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source_dir = self.root / "data" / "knowledge_sources"
        self.source_dir.mkdir(parents=True)
        self.manifest = self.source_dir / "download_manifest.json"

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self, resources):
        self.manifest.write_text(
            json.dumps({"resources": resources}), encoding="utf-8"
        )

    def test_valid_manifest_file_is_verified(self):
        source = self.source_dir / "sample.txt"
        source.write_text("contenido", encoding="utf-8")
        raw = source.read_bytes()
        self.write_manifest({
            "sample": {
                "file": "data/knowledge_sources/sample.txt",
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        })
        report = audit_files(self.manifest, self.root)
        self.assertEqual(report["checked_files"], 1)
        self.assertEqual(report["hash_mismatch"], [])
        self.assertEqual(report["unsafe_paths"], [])

    def test_manifest_traversal_is_rejected(self):
        outside = self.root.parent / "outside-knowledge-audit.txt"
        outside.write_text("must not be read", encoding="utf-8")
        try:
            self.write_manifest({
                "escape": {"file": "../outside-knowledge-audit.txt"}
            })
            report = audit_files(self.manifest, self.root)
            self.assertEqual(report["checked_files"], 0)
            self.assertTrue(any(item.get("resource") == "linked" for item in report["unsafe_paths"]))
        finally:
            outside.unlink(missing_ok=True)

    def test_manifest_symlink_is_rejected(self):
        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        link = self.source_dir / "linked.txt"
        try:
            link.symlink_to(outside)
            self.write_manifest({
                "linked": {"file": "data/knowledge_sources/linked.txt"}
            })
            report = audit_files(self.manifest, self.root)
            self.assertEqual(report["checked_files"], 0)
            self.assertEqual(len(report["unsafe_paths"]), 1)
        finally:
            link.unlink(missing_ok=True)

    def test_missing_or_invalid_manifest_is_reported_not_raised(self):
        report = audit_files(self.manifest, self.root)
        self.assertTrue(report["manifest_errors"])
        self.manifest.write_text("not-json", encoding="utf-8")
        report = audit_files(self.manifest, self.root)
        self.assertTrue(report["manifest_errors"])

    def test_database_audit_uses_read_only_connection(self):
        database = self.root / "library.sqlite3"
        with sqlite3.connect(database) as db:
            db.execute("""
                CREATE TABLE knowledge_chunks(
                    document_id TEXT, chunk_index INTEGER,
                    content_sha256 TEXT
                )
            """)
            db.execute(
                "INSERT INTO knowledge_chunks VALUES('doc', 0, 'hash')"
            )
        report = audit_database(database)
        self.assertEqual(report["chunks"], 1)
        with sqlite3.connect(database) as db:
            self.assertEqual(
                db.execute("SELECT COUNT(*) FROM knowledge_chunks").fetchone()[0],
                1,
            )

    def test_symlinked_scan_root_is_not_followed(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "private.txt").write_text("not part of the project")
        data_dir = self.root / "data"
        data_dir.mkdir(exist_ok=True)
        link = data_dir / "knowledge_base"
        try:
            link.symlink_to(outside, target_is_directory=True)
            self.write_manifest({})
            report = audit_files(self.manifest, self.root)
            self.assertTrue(any(
                item["path"] == str(link) for item in report["unsafe_paths"]
            ))
            self.assertEqual(report["unregistered_files"], [])
        finally:
            link.unlink(missing_ok=True)

    def test_invalid_database_schema_returns_diagnostic(self):
        database = self.root / "empty.sqlite3"
        sqlite3.connect(database).close()
        report = audit_database(database)
        self.assertIn("error", report)


if __name__ == "__main__":
    unittest.main()
