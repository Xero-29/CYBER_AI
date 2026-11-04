"""Pruebas de la biblioteca indexada de conocimientos."""

import tempfile
import unittest
from pathlib import Path

import knowledge_library as library


class TestKnowledgeLibrary(unittest.TestCase):
    def setUp(self):
        # Cada prueba recibe una base temporal aislada.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = library.DB_PATH
        library.DB_PATH = Path(self.temp_dir.name) / "knowledge_test.sqlite3"

    def tearDown(self):
        library.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def store(
        self,
        title,
        content,
        embedding,
        *,
        visibility="shared",
        tenant_id=None,
        category="general",
    ):
        return library.store_chunk(
            title=title,
            source="Fuente de prueba",
            category=category,
            content=content,
            embedding=embedding,
            embedding_model="test-embeddings",
            visibility=visibility,
            tenant_id=tenant_id,
        )

    def test_round_trip_compressed_content(self):
        text = "Los permisos Unix controlan lectura, escritura y ejecución."

        saved = self.store(
            "Permisos Unix", text, [1.0, 0.0]
        )
        recovered = library.read_chunk(saved["id"])

        self.assertEqual(recovered["content"], text)
        self.assertEqual(recovered["title"], "Permisos Unix")
        self.assertEqual(recovered["source"], "Fuente de prueba")

    def test_search_orders_by_semantic_similarity(self):
        linux = self.store(
            "Permisos Linux", "Contenido sobre permisos.",
            [1.0, 0.0], category="linux",
        )
        self.store(
            "Redes", "Contenido sobre redes.",
            [0.0, 1.0], category="redes",
        )

        results = library.search_knowledge(
            query_embedding=[0.98, 0.02],
            embedding_model="test-embeddings",
            top_k=2,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], linux["id"])
        self.assertGreater(
            results[0]["similarity"], results[1]["similarity"]
        )

    def test_category_filter_limits_results(self):
        self.store(
            "Permisos", "Contenido de permisos.",
            [1.0, 0.0], category="linux",
        )
        self.store(
            "Redes", "Contenido de redes.",
            [0.9, 0.1], category="redes",
        )

        results = library.search_knowledge(
            query_embedding=[1.0, 0.0],
            embedding_model="test-embeddings",
            categories=["linux"],
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["category"], "linux")

    def test_tenant_search_cannot_see_another_tenant(self):
        shared = self.store(
            "Conocimiento compartido", "Visible para clientes.",
            [1.0, 0.0],
        )
        own = self.store(
            "Privado A", "Secreto de A.",
            [0.9, 0.1], visibility="tenant", tenant_id="empresa-a",
        )
        other = self.store(
            "Privado B", "Secreto de B.",
            [0.8, 0.2], visibility="tenant", tenant_id="empresa-b",
        )

        results = library.search_knowledge(
            query_embedding=[1.0, 0.0],
            embedding_model="test-embeddings",
            top_k=10,
            tenant_id="empresa-a",
        )
        result_ids = {item["id"] for item in results}

        self.assertIn(shared["id"], result_ids)
        self.assertIn(own["id"], result_ids)
        self.assertNotIn(other["id"], result_ids)

    def test_reading_other_tenant_chunk_is_denied(self):
        other = self.store(
            "Privado B", "Secreto de B.",
            [1.0, 0.0], visibility="tenant", tenant_id="empresa-b",
        )

        with self.assertRaises(KeyError):
            library.read_chunk(other["id"], tenant_id="empresa-a")

    def test_private_knowledge_requires_tenant_id(self):
        with self.assertRaises(ValueError):
            self.store(
                "Privado", "Contenido privado.",
                [1.0, 0.0], visibility="tenant",
            )

    def test_invalid_embedding_is_rejected(self):
        with self.assertRaises(ValueError):
            self.store(
                "Vector inválido", "Texto de prueba.",
                [0.0, 0.0],
            )


if __name__ == "__main__":
    unittest.main()
