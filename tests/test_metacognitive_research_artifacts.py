import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import knowledge_library
import metacognition


class MetacognitiveResearchArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_project = metacognition.PROJECT
        self.original_db = knowledge_library.DB_PATH
        metacognition.PROJECT = self.root
        knowledge_library.DB_PATH = self.root / "data" / "knowledge.sqlite3"
        knowledge_library.initialize()

    def tearDown(self):
        metacognition.PROJECT = self.original_project
        knowledge_library.DB_PATH = self.original_db
        self.temp.cleanup()

    @patch("knowledge_embeddings.generate_embedding")
    def test_new_verified_report_is_saved_and_indexed_once(self, generate):
        generate.return_value = {
            "embedding": [1.0, 0.0],
            "embedding_space": "test::embedding-v1",
            "model": "test",
        }
        report = "# Fundamentos\n\nInforme técnico verificable."
        first = metacognition.publish_research_report(report, "task-a")
        second = metacognition.publish_research_report(report, "task-b")

        self.assertTrue(first["indexed"])
        self.assertFalse(first["duplicate"])
        self.assertTrue((self.root / first["artifact_path"]).is_file())
        self.assertTrue(second["indexed"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(first["document"]["sha256"],
                         second.get("document", first["document"])["sha256"])
        with knowledge_library.database() as db:
            count = db.execute(
                "SELECT COUNT(*) FROM knowledge_chunks WHERE category = 'research_provisional'"
            ).fetchone()[0]
        self.assertEqual(count, 1)

    @patch("knowledge_embeddings.generate_embedding")
    def test_semantic_near_duplicate_is_saved_as_candidate_not_indexed(self, generate):
        generate.return_value = {
            "embedding": [1.0, 0.0],
            "embedding_space": "test::embedding-v1",
            "model": "test",
        }
        knowledge_library.store_chunks([{
            "title": "Conocimiento existente",
            "source": "fixture://existing",
            "category": "cybersecurity:foundations",
            "license": "UNSPECIFIED",
            "content": "Contenido existente relacionado con el mismo tema.",
            "embedding": [1.0, 0.0],
            "embedding_model": "test::embedding-v1",
            "visibility": "shared",
        }])
        result = metacognition.publish_research_report(
            "Contenido nuevo sobre el mismo tema, con algunos detalles adicionales.",
            "task-near",
        )

        self.assertFalse(result["indexed"])
        self.assertTrue(result["near_duplicate"])
        self.assertEqual(result["status"], "merge_review_required")
        self.assertTrue((self.root / result["artifact_path"]).is_file())
        with knowledge_library.database() as db:
            count = db.execute("SELECT COUNT(*) FROM knowledge_chunks").fetchone()[0]
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
