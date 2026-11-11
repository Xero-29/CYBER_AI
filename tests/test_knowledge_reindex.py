import hashlib
import zlib
import unittest
from unittest.mock import patch

import knowledge_reindex


class KnowledgeReindexTests(unittest.TestCase):
    def test_verified_content_checks_hash_and_size(self):
        original = "contenido de conocimiento".encode("utf-8")
        row = {
            "id": "chunk-1",
            "content_z": zlib.compress(original),
            "content_sha256": hashlib.sha256(original).hexdigest(),
            "original_bytes": len(original),
        }
        self.assertEqual(knowledge_reindex._verified_content(row), "contenido de conocimiento")

    def test_verified_content_rejects_tampered_hash(self):
        original = b"contenido"
        row = {
            "id": "chunk-tampered",
            "content_z": zlib.compress(original),
            "content_sha256": "0" * 64,
            "original_bytes": len(original),
        }
        with self.assertRaisesRegex(ValueError, "hash"):
            knowledge_reindex._verified_content(row)

    def test_verified_content_rejects_size_mismatch(self):
        original = b"contenido"
        row = {
            "id": "chunk-size",
            "content_z": zlib.compress(original),
            "content_sha256": hashlib.sha256(original).hexdigest(),
            "original_bytes": len(original) + 1,
        }
        with self.assertRaisesRegex(ValueError, "tamaño"):
            knowledge_reindex._verified_content(row)

    def test_reindex_batch_size_is_bounded(self):
        with patch.object(knowledge_reindex, "target_embedding_space",
                          return_value={"space": "ollama::model"}), \
             patch.object(knowledge_reindex, "inventory",
                          return_value={"chunks_to_reindex": 0}):
            with self.assertRaisesRegex(ValueError, "batch_size"):
                knowledge_reindex.reindex_knowledge(batch_size=0)

    def test_noop_when_all_vectors_are_already_current(self):
        plan = {"chunks_to_reindex": 0, "total_chunks": 4}
        with patch.object(knowledge_reindex, "target_embedding_space",
                          return_value={"space": "gemini::embed-model"}), \
             patch.object(knowledge_reindex, "inventory", return_value=plan):
            result = knowledge_reindex.reindex_knowledge()
        self.assertEqual(result["status"], "already_current")
        self.assertIsNone(result["backup"])


if __name__ == "__main__":
    unittest.main()
