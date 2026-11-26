"""Pruebas de la biblioteca indexada de conocimientos."""

import tempfile
import unittest
from unittest.mock import patch
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

    def test_bulk_store_validates_all_chunks_before_publishing(self):
        valid = {
            "title": "Documento", "source": "fixture", "category": "test",
            "content": "contenido", "embedding": [1.0, 0.0],
            "embedding_model": "test-embeddings", "document_id": "bulk-doc",
            "chunk_index": 0,
        }
        invalid = dict(valid, chunk_index=1, content="")
        with self.assertRaises(ValueError):
            library.store_chunks([valid, invalid])
        results = library.search_knowledge(
            query_embedding=[1.0, 0.0],
            embedding_model="test-embeddings",
            top_k=10,
        )
        self.assertEqual(results, [])

    def test_oversized_fragment_is_rejected_before_storage(self):
        with patch.object(library, "MAX_CHUNK_BYTES", 3):
            with self.assertRaisesRegex(ValueError, "2 MiB"):
                self.store("Grande", "cuatro", [1.0, 0.0])

    def test_read_rejects_oversized_declared_content_before_decompression(self):
        saved = self.store("Documento", "contenido válido", [1.0, 0.0])
        library.initialize()
        with library.database() as db:
            db.execute(
                "UPDATE knowledge_chunks SET original_bytes = ? WHERE id = ?",
                (library.MAX_CHUNK_BYTES + 1, saved["id"]),
            )
        with self.assertRaisesRegex(ValueError, "tamaño declarado"):
            library.read_chunk(saved["id"])

    def test_search_rejects_malformed_filters(self):
        with self.assertRaisesRegex(ValueError, "categories"):
            library.search_knowledge(
                query_embedding=[1.0, 0.0],
                embedding_model="test-embeddings",
                categories="linux",
            )
        with self.assertRaisesRegex(ValueError, "min_score"):
            library.search_knowledge(
                query_embedding=[1.0, 0.0],
                embedding_model="test-embeddings",
                min_score="invalid",
            )

    def test_invalid_embedding_is_rejected(self):
        with self.assertRaises(ValueError):
            self.store(
                "Vector inválido", "Texto de prueba.",
                [0.0, 0.0],
            )



    def test_vector_validation_rejects_huge_integer_and_dimension_abuse(self):
        with self.assertRaisesRegex(ValueError, "fuera de rango"):
            library.validate_vector([10 ** 1000])
        with patch.object(library, "MAX_EMBEDDING_DIMENSIONS", 2):
            with self.assertRaisesRegex(ValueError, "dimensiones"):
                library.validate_vector([1.0, 0.0, 0.0])

    def test_cosine_similarity_is_stable_for_large_finite_vectors(self):
        score = library.cosine_similarity(
            [1e308, 1e308],
            [1e308, 0.0],
        )
        self.assertAlmostEqual(score, 0.7071067811865475, places=14)

    def test_vector_with_unrepresentable_norm_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "magnitud"):
            library.validate_vector([1e308, 1e308, 1e308, 1e308])

    def test_search_rejects_out_of_range_top_k_and_min_score(self):
        for top_k in (0, -1, 51, True):
            with self.subTest(top_k=top_k), self.assertRaisesRegex(ValueError, "top_k"):
                library.search_knowledge(
                    query_embedding=[1.0, 0.0],
                    embedding_model="test-embeddings",
                    top_k=top_k,
                )
        with self.assertRaisesRegex(ValueError, "min_score"):
            library.search_knowledge(
                query_embedding=[1.0, 0.0],
                embedding_model="test-embeddings",
                min_score=10 ** 1000,
            )

    def test_list_knowledge_rejects_coerced_or_out_of_range_filters(self):
        for limit in (True, "10", 0, 201, 1.5):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "limit"):
                library.list_knowledge(limit=limit)
        with self.assertRaisesRegex(ValueError, "tenant_id"):
            library.list_knowledge(tenant_id=" ")
        with self.assertRaisesRegex(ValueError, "category"):
            library.list_knowledge(category=" ")

    def test_document_chunk_count_can_filter_embedding_space(self):
        library.store_chunks([
            {
                "title": "Paquete", "source": "offline", "category": "test",
                "content": "contenido v1", "embedding": [1.0, 0.0],
                "embedding_model": "provider-a::model-a",
                "document_id": "stable-doc", "chunk_index": 0,
            },
            {
                "title": "Paquete", "source": "offline", "category": "test",
                "content": "contenido v2", "embedding": [0.0, 1.0],
                "embedding_model": "provider-b::model-b",
                "document_id": "stable-doc", "chunk_index": 0,
            },
        ])
        self.assertEqual(library.document_chunk_count("stable-doc"), 2)
        self.assertEqual(
            library.document_chunk_count("stable-doc", "provider-a::model-a"),
            1,
        )
        self.assertEqual(
            library.document_chunk_count("stable-doc", "provider-b::model-b"),
            1,
        )

    def test_document_chunk_count_respects_visibility_and_tenant_scope(self):
        library.store_chunks([
            {
                "title": "Shared", "source": "source", "category": "test",
                "content": "shared", "embedding": [1.0, 0.0],
                "embedding_model": "test-space", "document_id": "same-id",
                "visibility": "shared",
            },
            {
                "title": "Tenant A", "source": "source", "category": "test",
                "content": "private a", "embedding": [1.0, 0.0],
                "embedding_model": "test-space", "document_id": "same-id",
                "visibility": "tenant", "tenant_id": "tenant-a",
            },
            {
                "title": "Tenant B", "source": "source", "category": "test",
                "content": "private b", "embedding": [1.0, 0.0],
                "embedding_model": "test-space", "document_id": "same-id",
                "visibility": "tenant", "tenant_id": "tenant-b",
            },
        ])
        self.assertEqual(
            library.document_chunk_count("same-id", visibility="shared"), 1
        )
        self.assertEqual(
            library.document_chunk_count(
                "same-id", visibility="tenant", tenant_id="tenant-a"
            ), 1
        )
        self.assertEqual(
            library.document_chunk_count(
                "same-id", visibility="tenant", tenant_id="tenant-b"
            ), 1
        )

    def test_document_chunk_count_requires_tenant_for_private_scope(self):
        with self.assertRaisesRegex(ValueError, "tenant_id"):
            library.document_chunk_count("doc", visibility="tenant")

    def test_document_chunk_count_rejects_empty_model_filter(self):
        with self.assertRaisesRegex(ValueError, "embedding_model"):
            library.document_chunk_count("stable-doc", " ")


    def test_text_index_and_hybrid_search_retrieve_lexical_hit(self):
        if not library.text_index_available():
            self.skipTest("SQLite FTS5 no está disponible.")
        library.store_chunks([{
            "title": "Control de acceso API", "source": "offline-pack",
            "category": "cybersecurity:api",
            "content": "La autorización evita acceso cruzado entre usuarios.",
            "embedding": [1.0, 0.0], "embedding_model": "test-space",
            "document_id": "api-doc", "chunk_index": 0,
        }])
        result = library.search_knowledge_hybrid(
            query_text="autorización acceso cruzado usuarios",
            query_embedding=[0.0, 1.0], embedding_model="test-space", top_k=3,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["category"], "cybersecurity:api")
        self.assertIsNotNone(result[0]["text_rank"])
        self.assertGreater(result[0]["hybrid_score"], 0)

    def test_rebuild_text_index_reindexes_and_verifies_existing_chunks(self):
        if not library.text_index_available():
            self.skipTest("SQLite FTS5 no está disponible.")
        library.store_chunks([{
            "title": "Documento previo", "source": "fixture", "category": "test",
            "content": "texto de referencia", "embedding": [1.0, 0.0],
            "embedding_model": "test-space", "document_id": "prior-doc",
            "chunk_index": 0,
        }])
        result = library.rebuild_text_index()
        self.assertTrue(result["available"])
        self.assertEqual(result["indexed"], 1)


    def test_hybrid_text_search_respects_tenant_isolation(self):
        if not library.text_index_available():
            self.skipTest("SQLite FTS5 no está disponible.")
        library.store_chunks([
            {
                "title": "Compartido", "source": "shared",
                "category": "security", "content": "manual de acceso compartido",
                "embedding": [1.0, 0.0], "embedding_model": "test-space",
                "document_id": "shared-doc", "chunk_index": 0,
                "visibility": "shared",
            },
            {
                "title": "Privado A", "source": "tenant-a",
                "category": "security", "content": "informe reservado alpha",
                "embedding": [1.0, 0.0], "embedding_model": "test-space",
                "document_id": "tenant-a-doc", "chunk_index": 0,
                "visibility": "tenant", "tenant_id": "tenant-a",
            },
            {
                "title": "Privado B", "source": "tenant-b",
                "category": "security", "content": "informe reservado beta",
                "embedding": [1.0, 0.0], "embedding_model": "test-space",
                "document_id": "tenant-b-doc", "chunk_index": 0,
                "visibility": "tenant", "tenant_id": "tenant-b",
            },
        ])
        result = library.search_knowledge_hybrid(
            query_text="informe reservado beta",
            query_embedding=[1.0, 0.0], embedding_model="test-space",
            tenant_id="tenant-a", top_k=10,
        )
        sources = {item["source"] for item in result}
        self.assertIn("shared", sources)
        self.assertIn("tenant-a", sources)
        self.assertNotIn("tenant-b", sources)

if __name__ == "__main__":
    unittest.main()
