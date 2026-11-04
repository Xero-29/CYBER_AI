"""Pruebas de integración del contexto recuperado por ECO."""

import unittest
from unittest.mock import patch

from agent_runner import retrieve_knowledge_context


class TestKnowledgeRetrievalContext(unittest.TestCase):
    @patch("knowledge_library.search_knowledge")
    @patch("knowledge_embeddings.generate_embedding")
    def test_passes_requested_category_to_semantic_search(
        self, mock_embedding, mock_search
    ):
        mock_embedding.return_value = {
            "agent": "ECO",
            "model": "nomic-embed-text:latest",
            "embedding": [1.0, 0.0],
            "dimensions": 2,
        }

        mock_search.return_value = [{
            "id": "chunk-owasp-1",
            "title": "OWASP Authorization Cheat Sheet",
            "source": "OWASP",
            "category": "application-security",
            "similarity": 0.55,
            "content": (
                "La autorización determina si una entidad puede "
                "realizar una acción sobre un recurso."
            ),
        }]

        categories = ["application-security"]

        context, retrieved = retrieve_knowledge_context(
            "Evitar que un usuario acceda a datos de otro usuario",
            top_k=3,
            min_score=0.40,
            categories=categories,
        )

        mock_search.assert_called_once()
        self.assertEqual(
            mock_search.call_args.kwargs["categories"],
            categories,
        )
        self.assertIn("OWASP Authorization Cheat Sheet", context)
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(
            retrieved[0]["category"],
            "application-security",
        )

    @patch("knowledge_library.search_knowledge")
    @patch("knowledge_embeddings.generate_embedding")
    def test_preserves_top_k_and_similarity_threshold(
        self, mock_embedding, mock_search
    ):
        mock_embedding.return_value = {
            "agent": "ECO",
            "model": "nomic-embed-text:latest",
            "embedding": [1.0, 0.0],
            "dimensions": 2,
        }
        mock_search.return_value = []

        context, retrieved = retrieve_knowledge_context(
            "Consulta de prueba",
            top_k=2,
            min_score=0.45,
            categories=["linux"],
        )

        kwargs = mock_search.call_args.kwargs
        self.assertEqual(kwargs["top_k"], 2)
        self.assertEqual(kwargs["min_score"], 0.45)
        self.assertEqual(kwargs["categories"], ["linux"])
        self.assertEqual(context, "")
        self.assertEqual(retrieved, [])

    @patch("knowledge_library.search_knowledge")
    @patch("knowledge_embeddings.generate_embedding")
    def test_returns_only_metadata_for_selected_fragments(
        self, mock_embedding, mock_search
    ):
        mock_embedding.return_value = {
            "agent": "ECO",
            "model": "nomic-embed-text:latest",
            "embedding": [1.0, 0.0],
            "dimensions": 2,
        }
        mock_search.return_value = [{
            "id": "chunk-1",
            "title": "Guía de autorización",
            "source": "OWASP",
            "category": "application-security",
            "similarity": 0.62,
            "content": "Contenido de referencia.",
        }]

        context, retrieved = retrieve_knowledge_context(
            "Revisar autorización",
            categories=["application-security"],
        )

        self.assertIn("Contenido de referencia.", context)
        self.assertEqual(
            set(retrieved[0]),
            {"id", "title", "source", "category", "similarity"},
        )
        self.assertEqual(retrieved[0]["id"], "chunk-1")


if __name__ == "__main__":
    unittest.main()
