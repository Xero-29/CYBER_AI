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


    def test_extracts_html_without_active_content(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "page.html"
            path.write_text("<h1>Manual</h1><script>secret()</script><p>Texto visible</p>", encoding="utf-8")
            text = ingest.extract_document_text(path)
        self.assertIn("Manual", text)
        self.assertIn("Texto visible", text)
        self.assertNotIn("secret()", text)

    def test_extracts_csv_and_json_as_text(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "data.csv"
            csv_path.write_text("name,value\nalpha,1\n", encoding="utf-8")
            json_path = Path(temp) / "data.json"
            json_path.write_text('{"name":"alpha","value":1}', encoding="utf-8")
            self.assertIn("alpha", ingest.extract_document_text(csv_path))
            self.assertIn('"value": 1', ingest.extract_document_text(json_path))

    def test_rejects_unsupported_and_oversized_documents(self):
        with tempfile.TemporaryDirectory() as temp:
            unsupported = Path(temp) / "archive.bin"
            unsupported.write_bytes(b"data")
            with self.assertRaisesRegex(ValueError, "Formato no soportado"):
                ingest.extract_document_text(unsupported)
            oversized = Path(temp) / "large.txt"
            oversized.write_bytes(b"xxxx")
            with patch.object(ingest, "MAX_INPUT_BYTES", 3):
                with self.assertRaisesRegex(ValueError, "100 MiB"):
                    ingest.extract_document_text(oversized)

    def test_embedding_failure_does_not_publish_partial_document(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "partial.md"
            document.write_text(("A" * 250) + "\n\n" + ("B" * 250), encoding="utf-8")
            calls = 0

            def fail_second_batch(texts, agent_name="ECO"):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise RuntimeError("embedding provider unavailable")
                return {
                    "agent": "ECO", "model": "test-embeddings",
                    "embedding_space": "test-embeddings",
                    "embeddings": [[1.0, 0.0] for _ in texts],
                    "dimensions": 2,
                }

            with patch.object(ingest, "generate_embeddings", side_effect=fail_second_batch), \
                 patch.object(ingest, "store_chunks") as store:
                with self.assertRaisesRegex(RuntimeError, "unavailable"):
                    ingest.ingest_document(
                        document, title="Parcial", category="test",
                        batch_size=1, max_chars=300,
                    )
            store.assert_not_called()

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

            def fake_store_chunks(chunks):
                stored_chunks.extend(chunks)
                return [
                    {
                        "id": f"chunk-{index + 1}",
                        "document_id": item["document_id"],
                        "chunk_index": item["chunk_index"],
                    }
                    for index, item in enumerate(chunks)
                ]

            with (
                patch.object(
                    ingest,
                    "generate_embeddings",
                    side_effect=fake_embeddings,
                ),
                patch.object(
                    ingest,
                    "store_chunks",
                    side_effect=fake_store_chunks,
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
