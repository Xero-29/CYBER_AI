"""Pruebas del registro persistente de recursos."""

import tempfile
import unittest
from pathlib import Path

import knowledge_library as library
import knowledge_registry as registry


class TestKnowledgeRegistry(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = library.DB_PATH
        library.DB_PATH = Path(self.temp_dir.name) / "registry.sqlite3"

    def tearDown(self):
        library.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def register(self, path, digest):
        return registry.register_resource(
            path,
            sha256=digest,
            file_size=100,
            resource_type="pdf",
            title="Documento de prueba",
        )

    def test_new_resource_creates_first_version(self):
        result = self.register(
            Path(self.temp_dir.name) / "guide.pdf",
            "a" * 64,
        )

        self.assertEqual(result["status"], "new")
        self.assertTrue(result["version_created"])
        self.assertEqual(len(registry.resource_inventory()), 1)

    def test_same_file_does_not_duplicate_version(self):
        path = Path(self.temp_dir.name) / "guide.pdf"

        first = self.register(path, "b" * 64)
        second = self.register(path, "b" * 64)

        self.assertEqual(first["resource_id"], second["resource_id"])
        self.assertEqual(second["status"], "unchanged")
        self.assertFalse(second["version_created"])
        self.assertEqual(registry.resource_inventory()[0]["versions"], 1)

    def test_changed_hash_creates_new_version(self):
        path = Path(self.temp_dir.name) / "guide.pdf"

        first = self.register(path, "c" * 64)
        second = self.register(path, "d" * 64)

        self.assertEqual(first["resource_id"], second["resource_id"])
        self.assertEqual(second["status"], "modified")
        self.assertTrue(second["version_created"])
        self.assertEqual(registry.resource_inventory()[0]["versions"], 2)

    def test_invalid_hash_is_rejected(self):
        with self.assertRaises(ValueError):
            self.register(
                Path(self.temp_dir.name) / "guide.pdf",
                "hash-invalido",
            )


    def test_classification_update_creates_history(self):
        result = self.register(
            Path(self.temp_dir.name) / "guide.pdf",
            "e" * 64,
        )

        changed = registry.update_resource_classification(
            result["resource_id"],
            area_id="area_06",
            domain_id="virtualization_security",
            topic_id="hypervisor_security",
            subtopic_id="server_hypervisor_protection",
            classification_status="provisional",
            reason="Prueba de clasificación",
        )

        self.assertTrue(changed)

        with registry.connect() as db:
            resource = db.execute(
                "SELECT * FROM knowledge_resources WHERE resource_id = ?",
                (result["resource_id"],),
            ).fetchone()
            history = db.execute(
                "SELECT * FROM knowledge_classification_history "
                "WHERE resource_id = ?",
                (result["resource_id"],),
            ).fetchall()

        self.assertEqual(resource["area_id"], "area_06")
        self.assertEqual(resource["classification_status"], "provisional")
        self.assertEqual(len(history), 1)
        self.assertIn("area_06", history[0]["new_classification"])
        self.assertIn("pending", history[0]["previous_classification"])

    def test_invalid_classification_status_is_rejected(self):
        result = self.register(
            Path(self.temp_dir.name) / "guide.pdf",
            "f" * 64,
        )

        with self.assertRaises(ValueError):
            registry.update_resource_classification(
                result["resource_id"],
                area_id="area_06",
                domain_id="domain",
                topic_id="topic",
                subtopic_id="subtopic",
                classification_status="approved",
            )

    def test_missing_resource_is_rejected(self):
        with self.assertRaises(ValueError):
            registry.update_resource_classification(
                "resource-inexistente",
                area_id="area_06",
                domain_id="domain",
                topic_id="topic",
                subtopic_id="subtopic",
            )

    def test_same_classification_does_not_create_history(self):
        result = self.register(
            Path(self.temp_dir.name) / "guide.pdf",
            "1" * 64,
        )

        classification = {
            "area_id": "area_06",
            "domain_id": "domain",
            "topic_id": "topic",
            "subtopic_id": "subtopic",
            "classification_status": "provisional",
        }

        self.assertTrue(registry.update_resource_classification(
            result["resource_id"], **classification
        ))

        self.assertFalse(registry.update_resource_classification(
            result["resource_id"], **classification
        ))

        with registry.connect() as db:
            count = db.execute(
                "SELECT COUNT(*) FROM knowledge_classification_history"
            ).fetchone()[0]

        self.assertEqual(count, 1)



    def test_classification_preserves_versions_and_chunks(self):
        result = self.register(
            Path(self.temp_dir.name) / "integrity.pdf",
            "2" * 64,
        )

        with registry.connect() as db:
            db.execute("""
                UPDATE knowledge_resource_versions
                SET license = 'CC-BY-4.0',
                    license_url = 'https://example.org/license',
                    license_status = 'verified',
                    provenance_uri = 'https://example.org/source',
                    provenance_evidence = 'Prueba de procedencia'
                WHERE version_id = ?
            """, (result["version_id"],))

            db.execute("""
                INSERT INTO knowledge_chunks (
                    id, document_id, chunk_index, title, source,
                    category, tags_json, visibility, content_z,
                    content_sha256, original_bytes, compressed_bytes,
                    embedding_json, embedding_model,
                    embedding_dimensions, created_at, license
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "chunk-integrity", "document-integrity", 0,
                "Fragmento de prueba", "integrity.pdf",
                "test", "[]", "shared", b"contenido",
                "a" * 64, 9, 9, "[0.1, 0.2]", "test-model",
                2, registry.utc_now(), "CC-BY-4.0",
            ))

        with registry.connect() as db:
            version_before = dict(db.execute(
                "SELECT * FROM knowledge_resource_versions WHERE version_id = ?",
                (result["version_id"],),
            ).fetchone())
            chunk_before = dict(db.execute(
                "SELECT * FROM knowledge_chunks WHERE id = ?",
                ("chunk-integrity",),
            ).fetchone())

        self.assertTrue(registry.update_resource_classification(
            result["resource_id"],
            area_id="area_19",
            domain_id="firmware_security",
            topic_id="bios_security",
            subtopic_id="firmware_protection",
            classification_status="provisional",
        ))

        with registry.connect() as db:
            version_after = dict(db.execute(
                "SELECT * FROM knowledge_resource_versions WHERE version_id = ?",
                (result["version_id"],),
            ).fetchone())
            chunk_after = dict(db.execute(
                "SELECT * FROM knowledge_chunks WHERE id = ?",
                ("chunk-integrity",),
            ).fetchone())

        self.assertEqual(version_before, version_after)
        self.assertEqual(chunk_before, chunk_after)

if __name__ == "__main__":
    unittest.main()
