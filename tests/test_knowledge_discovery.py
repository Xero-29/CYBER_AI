"""Pruebas del motor de descubrimiento de recursos."""

import tempfile
import unittest
from pathlib import Path

import knowledge_library as library
import knowledge_discovery as discovery
import knowledge_registry as registry


class TestKnowledgeDiscovery(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = library.DB_PATH
        library.DB_PATH = Path(self.temp_dir.name) / "discovery.sqlite3"

        self.root = Path(self.temp_dir.name) / "sources"
        self.root.mkdir()

    def tearDown(self):
        library.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_discovers_supported_files(self):
        (self.root / "guide.pdf").write_bytes(b"%PDF-test")
        (self.root / "data.json").write_text('{"ok": true}')
        (self.root / "notes.txt").write_text("Texto de prueba")

        result = discovery.discover_resources(
            [self.root],
            area_id="area_02",
        )

        self.assertEqual(result["discovered"], 3)
        self.assertEqual(result["new"], 3)
        self.assertEqual(result["errors"], [])

        inventory = registry.resource_inventory()
        self.assertEqual(len(inventory), 3)
        self.assertTrue(
            all(item["area_id"] == "area_02" for item in inventory)
        )

    def test_unchanged_files_are_not_duplicated(self):
        file_path = self.root / "guide.pdf"
        file_path.write_bytes(b"%PDF-test")

        first = discovery.discover_resources([self.root])
        second = discovery.discover_resources([self.root])

        self.assertEqual(first["new"], 1)
        self.assertEqual(second["unchanged"], 1)
        self.assertEqual(len(registry.resource_inventory()), 1)
        self.assertEqual(registry.resource_inventory()[0]["versions"], 1)

    def test_modified_file_creates_version(self):
        file_path = self.root / "guide.pdf"
        file_path.write_bytes(b"%PDF-original")

        discovery.discover_resources([self.root])

        file_path.write_bytes(b"%PDF-modificado")
        result = discovery.discover_resources([self.root])

        self.assertEqual(result["modified"], 1)
        self.assertEqual(registry.resource_inventory()[0]["versions"], 2)

    def test_unsupported_files_are_skipped(self):
        (self.root / "program.exe").write_bytes(b"no procesar")

        result = discovery.discover_resources([self.root])

        self.assertEqual(result["discovered"], 0)
        self.assertEqual(result["skipped"], 1)
        self.assertEqual(result["errors"], [])

    def test_compressed_csv_is_detected(self):
        file_path = self.root / "scores.csv.gz"
        file_path.write_bytes(b"contenido comprimido de prueba")

        result = discovery.discover_resources([self.root])

        self.assertEqual(result["new"], 1)
        self.assertEqual(result["resources"][0]["type"], "csv_gz")


if __name__ == "__main__":
    unittest.main()
