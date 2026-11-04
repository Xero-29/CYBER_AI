"""Pruebas del importador de documentos de CYBER_AI."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import knowledge_ingest as ingest


class TestKnowledgeIngest(unittest.TestCase):
    def test_split_text_rejects_empty_content(self):
        with self.assertRaises(ValueError):
            ingest.split_text("   ")

    def test_split_text_respects_chunk_limit(self):
        text = "A" * 700

        chunks = ingest.split_text(
            text,
            max_chars=300,
            overlap=50,
        )

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 300 for chunk in chunks))

        # Las partes siguientes conservan contexto mediante solapamiento.
        self.assertTrue(
            any(
                chunks[index][-50:] == chunks[index + 1][:50]
                for index in range(len(chunks) - 1)
            )
        )

    def test_split_text_combines_short_paragraphs(self):
        text = "Primer párrafo.\n\nSegundo párrafo."

        chunks = ingest.split_text(text, max_chars=300)

        self.assertEqual(len(chunks), 1)
        self.assertIn("Primer párrafo.", chunks[0])
        self.assertIn("Segundo párrafo.", chunks[0])

    def test_ingest_batches_embeddings_and_stores_chunks(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "guia.md"
            document.write_text(
                ("A" * 250) + "\n\n" + ("B" * 250),
                encoding="utf-8",
            )

            embedding_calls = []
            stored_chunks = []

            def fake_embeddings(texts, agent_name="ECO"):
                embedding_calls.append(list(texts))
                return {
                    "agent": "ECO",
                    "model": "test-embeddings",
                    "embeddings": [[1.0, 0.0] for _ in texts],
                    "dimensions": 2,
                }

            def fake_store_chunk(**kwargs):
                stored_chunks.append(kwargs)
                return {
                    "id": f"chunk-{len(stored_chunks)}",
                    "document_id": kwargs["document_id"],
                    "chunk_index": kwargs["chunk_index"],
                }

            with (
                patch.object(
                    ingest,
                    "generate_embeddings",
                    side_effect=fake_embeddings,
                ),
                patch.object(
                    ingest,
                    "store_chunk",
                    side_effect=fake_store_chunk,
                ),
            ):
                result = ingest.ingest_document(
                    document,
                    title="Guía de prueba",
                    category="pruebas",
                    batch_size=1,
                    max_chars=300,
                )

            self.assertEqual(result["chunks"], 2)
            self.assertEqual(len(embedding_calls), 2)
            self.assertEqual(len(stored_chunks), 2)
            self.assertEqual(
                [item["chunk_index"] for item in stored_chunks],
                [0, 1],
            )
            self.assertTrue(result["document_sha256"])
            self.assertTrue(
                all(
                    item["visibility"] == "shared"
                    for item in stored_chunks
                )
            )


if __name__ == "__main__":
    unittest.main()
