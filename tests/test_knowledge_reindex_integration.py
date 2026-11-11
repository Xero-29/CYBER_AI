import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import knowledge_library
import knowledge_reindex


class KnowledgeReindexIntegrationTests(unittest.TestCase):
    def test_reindex_publishes_complete_vector_set_and_keeps_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "knowledge.sqlite3"
            with patch.object(knowledge_library, "DB_PATH", db_path), \
                 patch.object(knowledge_reindex, "DB_PATH", db_path):
                first = knowledge_library.store_chunk(
                    title="Documento uno", source="test", category="security",
                    content="Contenido de prueba uno", embedding=[1.0, 0.0],
                    embedding_model="old-model")
                second = knowledge_library.store_chunk(
                    title="Documento dos", source="test", category="security",
                    content="Contenido de prueba dos", embedding=[1.0, 0.0],
                    embedding_model="old-model")

                target = {
                    "agent": "ECO", "provider": "gemini",
                    "model": "gemini-embed", "space": "gemini::gemini-embed",
                }

                def fake_embeddings(texts, agent_name="ECO"):
                    return {
                        "embedding_space": target["space"],
                        "embeddings": [[0.0, 1.0] for _ in texts],
                    }

                with patch.object(knowledge_reindex, "target_embedding_space",
                                  return_value=target), \
                     patch.object(knowledge_reindex, "generate_embeddings",
                                  side_effect=fake_embeddings):
                    result = knowledge_reindex.reindex_knowledge(batch_size=1)

                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["reindexed_chunks"], 2)
                self.assertTrue(Path(result["backup"]).is_file())

                inventory = knowledge_reindex.inventory(target["space"])
                self.assertEqual(inventory["chunks_to_reindex"], 0)
                self.assertEqual(inventory["total_chunks"], 2)

                matches = knowledge_library.search_knowledge(
                    query_embedding=[0.0, 1.0],
                    embedding_model=target["space"],
                    top_k=5,
                    min_score=0.99,
                )
                self.assertEqual({item["id"] for item in matches},
                                 {first["id"], second["id"]})


if __name__ == "__main__":
    unittest.main()
