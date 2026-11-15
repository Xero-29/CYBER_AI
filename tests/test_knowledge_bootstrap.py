import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import knowledge_bootstrap


class KnowledgeBootstrapTests(unittest.TestCase):
    def test_dry_run_checks_hashes_without_embedding_import(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pack = root / "knowledge" / "packs" / "x.md"
            pack.parent.mkdir(parents=True)
            pack.write_text("# x\ncontenido", encoding="utf-8")
            manifest = pack.parent / "manifest.json"
            manifest.write_text(json.dumps({"area_count": 1, "areas": [
                {"id": "x", "name": "X", "path": "knowledge/packs/x.md"}
            ]}), encoding="utf-8")
            with patch.object(knowledge_bootstrap, "PROJECT", root), patch.object(knowledge_bootstrap, "MANIFEST", manifest):
                result = knowledge_bootstrap.bootstrap(dry_run=True)
            self.assertTrue(result["dry_run"])
            self.assertEqual(result["selected"], 1)
            self.assertEqual(result["ingested_count"], 0)
            self.assertEqual(len(result["items"][0]["sha256"]), 64)

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root.parent / "cyber-ai-outside-test.md"
            outside.write_text("outside", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"area_count": 1, "areas": [
                {"id": "bad", "path": "../cyber-ai-outside-test.md"}
            ]}), encoding="utf-8")
            with patch.object(knowledge_bootstrap, "PROJECT", root), patch.object(knowledge_bootstrap, "MANIFEST", manifest):
                with self.assertRaisesRegex(ValueError, "fuera del proyecto"):
                    knowledge_bootstrap.load_packs()
            outside.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
