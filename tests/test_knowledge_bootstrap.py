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
            self.assertEqual(result["items"][0]["visibility"], "shared")
            self.assertIsNone(result["items"][0]["tenant_id"])

    def test_windows_lock_uses_byte_range_and_releases(self):
        from types import SimpleNamespace
        calls = []
        api = SimpleNamespace(
            LK_LOCK=1, LK_UNLCK=2,
            locking=lambda descriptor, operation, count: calls.append(
                (descriptor, operation, count)
            ),
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "lock"
            with path.open("a+b") as lock:
                with bootstrap.exclusive_file_lock(lock, windows=True, windows_api=api):
                    self.assertEqual(path.read_bytes(), bytes(1))
            self.assertEqual([call[1:] for call in calls], [(1, 1), (2, 1)])

    def test_windows_lock_releases_after_failure(self):
        from types import SimpleNamespace
        calls = []
        api = SimpleNamespace(
            LK_LOCK=1, LK_UNLCK=2,
            locking=lambda descriptor, operation, count: calls.append(operation),
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "lock"
            with path.open("a+b") as lock:
                with self.assertRaisesRegex(RuntimeError, "injected"):
                    with bootstrap.exclusive_file_lock(lock, windows=True, windows_api=api):
                        raise RuntimeError("injected")
        self.assertEqual(calls, [1, 2])

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



    def test_successful_bootstrap_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pack, manifest = self._setup(root)
            digest = __import__("hashlib").sha256(pack.read_bytes()).hexdigest()
            previous = {
                "source_path": str(pack.resolve()), "current_sha256": digest,
                "processing_status": "completed",
            }
            with patch.object(bootstrap, "PROJECT", root), \
                 patch.object(bootstrap, "MANIFEST", manifest), \
                 patch("knowledge_embeddings.expected_embedding_space", return_value="provider::embed-v1"), \
                 patch("knowledge_registry.resource_inventory", side_effect=[[], [previous]]), \
                 patch("knowledge_registry.register_resource", return_value={"resource_id": "resource"}), \
                 patch("knowledge_registry.update_resource_classification"), \
                 patch("knowledge_registry.update_resource_processing_status") as status, \
                 patch("knowledge_library.document_chunk_count", return_value=2), \
                 patch("knowledge_ingest.ingest_document", return_value={
                     "document_id": "offline-id", "chunks": 2,
                 }) as ingest:
                first = bootstrap.bootstrap()
                second = bootstrap.bootstrap()
            self.assertEqual(first["ingested_count"], 1)
            self.assertEqual(second["skipped"], ["x"])
            self.assertEqual(ingest.call_count, 1)
            self.assertEqual([call.args[1] for call in status.call_args_list], ["processing", "completed"])

    def test_changed_embedding_space_triggers_reindex(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pack, manifest = self._setup(root)
            digest = __import__("hashlib").sha256(pack.read_bytes()).hexdigest()
            previous = {
                "source_path": str(pack.resolve()), "current_sha256": digest,
                "processing_status": "completed",
            }
            with patch.object(bootstrap, "PROJECT", root), \
                 patch.object(bootstrap, "MANIFEST", manifest), \
                 patch("knowledge_embeddings.expected_embedding_space", return_value="new-provider::embed-v2"), \
                 patch("knowledge_registry.resource_inventory", return_value=[previous]), \
                 patch("knowledge_registry.register_resource", return_value={"resource_id": "resource"}), \
                 patch("knowledge_registry.update_resource_classification"), \
                 patch("knowledge_registry.update_resource_processing_status"), \
                 patch("knowledge_library.document_chunk_count", side_effect=[0, 2]), \
                 patch("knowledge_ingest.ingest_document", return_value={
                     "document_id": "offline-id", "chunks": 2,
                 }) as ingest:
                result = bootstrap.bootstrap()
            self.assertEqual(result["ingested_count"], 1)
            self.assertEqual(
                ingest.call_args.kwargs["expected_embedding_model"],
                "new-provider::embed-v2",
            )

if __name__ == "__main__":
    unittest.main()
