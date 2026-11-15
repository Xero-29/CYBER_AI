import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import knowledge_bootstrap as bootstrap


class KnowledgeBootstrapTests(unittest.TestCase):
    def _setup(self, root, path="knowledge/packs/x.md"):
        pack = root / path
        pack.parent.mkdir(parents=True, exist_ok=True)
        pack.write_text("# X\nContenido", encoding="utf-8")
        manifest = root / "knowledge/packs/manifest.json"
        manifest.write_text(json.dumps({"area_count": 1, "areas": [
            {"id": "x", "name": "X", "path": path}
        ]}), encoding="utf-8")
        return pack, manifest

    def test_dry_run_checks_hashes_without_importing_ia(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, manifest = self._setup(root)
            with patch.object(bootstrap, "PROJECT", root), patch.object(bootstrap, "MANIFEST", manifest):
                result = bootstrap.bootstrap(dry_run=True)
            self.assertTrue(result["dry_run"])
            self.assertEqual(result["selected"], 1)
            self.assertEqual(result["ingested"], [])
            self.assertEqual(len(result["items"][0]["sha256"]), 64)

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"area_count": 1, "areas": [
                {"id": "bad", "path": "../outside.md"}
            ]}), encoding="utf-8")
            with patch.object(bootstrap, "PROJECT", root), patch.object(bootstrap, "MANIFEST", manifest):
                with self.assertRaisesRegex(ValueError, "Ruta no permitida"):
                    bootstrap.load_packs()

    def test_rejects_symlinked_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root.parent / "cyber-ai-symlink-test.md"
            outside.write_text("outside", encoding="utf-8")
            pack_dir = root / "knowledge/packs"
            pack_dir.mkdir(parents=True)
            (pack_dir / "link.md").symlink_to(outside)
            manifest = pack_dir / "manifest.json"
            manifest.write_text(json.dumps({"area_count": 1, "areas": [
                {"id": "link", "path": "knowledge/packs/link.md"}
            ]}), encoding="utf-8")
            with patch.object(bootstrap, "PROJECT", root), patch.object(bootstrap, "MANIFEST", manifest):
                with self.assertRaisesRegex(ValueError, "symlinks"):
                    bootstrap.load_packs()
            outside.unlink(missing_ok=True)

    def test_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, manifest = self._setup(root)
            manifest.write_text(json.dumps({"area_count": 2, "areas": [
                {"id": "x", "path": "knowledge/packs/x.md"},
                {"id": "x", "path": "knowledge/packs/x.md"}
            ]}), encoding="utf-8")
            with patch.object(bootstrap, "PROJECT", root), patch.object(bootstrap, "MANIFEST", manifest):
                with self.assertRaisesRegex(ValueError, "duplicadas"):
                    bootstrap.load_packs()

    def test_failed_ingestion_is_recorded_as_failed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._setup(root)
            with patch.object(bootstrap, "PROJECT", root), \
                 patch.object(bootstrap, "MANIFEST", root / "knowledge/packs/manifest.json"), \
                 patch("knowledge_registry.resource_inventory", return_value=[]), \
                 patch("knowledge_registry.register_resource", return_value={"resource_id": "r"}), \
                 patch("knowledge_registry.update_resource_classification"), \
                 patch("knowledge_registry.update_resource_processing_status") as status, \
                 patch("knowledge_ingest.ingest_document", side_effect=RuntimeError("embedding offline")):
                result = bootstrap.bootstrap()
            self.assertEqual(result["failed_count"], 1)
            self.assertIn("embedding offline", result["failed"][0]["error"])
            self.assertEqual([x.args[1] for x in status.call_args_list], ["processing", "failed"])


if __name__ == "__main__":
    unittest.main()
