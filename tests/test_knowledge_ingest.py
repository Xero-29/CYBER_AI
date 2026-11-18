"""Pruebas del importador de documentos de CYBER_AI."""

import csv
import stat
import sys
import tempfile
import types
import unittest
import zipfile
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

    def test_csv_extraction_restores_process_global_field_limit(self):
        original_limit = csv.field_size_limit()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bounded.csv"
            path.write_text("name,value\nalpha,1\n", encoding="utf-8")
            self.assertIn("alpha", ingest.extract_document_text(path))
            self.assertEqual(csv.field_size_limit(), original_limit)

            with patch.object(ingest, "MAX_EXTRACTED_CHARS", 5):
                with self.assertRaisesRegex(ValueError, "límite de 10 millones"):
                    ingest.extract_document_text(path)
            self.assertEqual(csv.field_size_limit(), original_limit)

    def test_extracts_real_docx_when_optional_dependency_is_installed(self):
        try:
            from docx import Document
        except ImportError:
            self.skipTest("python-docx opcional no instalado")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.docx"
            document = Document()
            document.add_paragraph("DOCX integration fixture")
            document.save(path)
            text = ingest.extract_document_text(path)
        self.assertIn("DOCX integration fixture", text)

    def test_extracts_real_xlsx_when_optional_dependency_is_installed(self):
        try:
            from openpyxl import Workbook
        except ImportError:
            self.skipTest("openpyxl opcional no instalado")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.xlsx"
            workbook = Workbook()
            workbook.active["A1"] = "XLSX integration fixture"
            workbook.save(path)
            text = ingest.extract_document_text(path)
        self.assertIn("XLSX integration fixture", text)

    def test_extracts_real_pptx_when_optional_dependency_is_installed(self):
        try:
            from pptx import Presentation
            from pptx.util import Inches
        except ImportError:
            self.skipTest("python-pptx opcional no instalado")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.pptx"
            presentation = Presentation()
            slide = presentation.slides.add_slide(presentation.slide_layouts[6])
            shape = slide.shapes.add_textbox(
                Inches(1), Inches(1), Inches(5), Inches(1)
            )
            shape.text_frame.text = "PPTX integration fixture"
            presentation.save(path)
            text = ingest.extract_document_text(path)
        self.assertIn("PPTX integration fixture", text)

    def test_pdf_extraction_preserves_page_markers_for_chunk_citations(self):
        class FakePage:
            def __init__(self, content):
                self.content = content
            def extract_text(self):
                return self.content

        class FakeReader:
            is_encrypted = False
            pages = [FakePage("Primera página"), FakePage("Segunda página")]

            def __init__(self, path, strict=True):
                self.path = path

        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "source.pdf"
            path.write_bytes(b"%PDF-test")
            fake_module = types.SimpleNamespace(PdfReader=FakeReader)
            with patch.dict(sys.modules, {"pypdf": fake_module}):
                text = ingest.extract_document_text(path)
        self.assertIn("[PDF page 1]", text)
        self.assertIn("[PDF page 2]", text)
        self.assertLess(text.index("Primera página"), text.index("Segunda página"))

    def test_office_archive_rejects_symlink_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "malicious.docx"
            info = zipfile.ZipInfo("word/document.xml")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(info, "../outside.xml")
            with self.assertRaisesRegex(ValueError, "enlaces simbólicos"):
                ingest._validate_office_archive(path)

    def test_office_archive_rejects_macro_payloads(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "macro.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/vbaProject.bin", b"macro")
            with self.assertRaisesRegex(ValueError, "macros"):
                ingest._validate_office_archive(path)

    def test_office_archive_rejects_duplicate_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "duplicate.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", b"one")
                archive.writestr("word/document.xml", b"two")
            with self.assertRaisesRegex(ValueError, "duplicadas"):
                ingest._validate_office_archive(path)

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

    def test_extraction_character_limit_is_enforced_incrementally(self):
        with tempfile.TemporaryDirectory() as temp:
            html = Path(temp) / "large.html"
            html.write_text("<p>12345678901</p>", encoding="utf-8")
            with patch.object(ingest, "MAX_EXTRACTED_CHARS", 10):
                with self.assertRaisesRegex(ValueError, "límite de extracción"):
                    ingest.extract_document_text(html)

            csv_file = Path(temp) / "large.csv"
            csv_file.write_text("a,b\\n123456,7890\\n", encoding="utf-8")
            with patch.object(ingest, "MAX_EXTRACTED_CHARS", 10):
                with self.assertRaisesRegex(ValueError, "límite de 10 millones"):
                    ingest.extract_document_text(csv_file)

            jsonl_file = Path(temp) / "large.jsonl"
            jsonl_file.write_text('{"a":1}\\n{"a":1}\\n', encoding="utf-8")
            with patch.object(ingest, "MAX_EXTRACTED_CHARS", 10):
                with self.assertRaisesRegex(ValueError, "límite de 10 millones"):
                    ingest.extract_document_text(jsonl_file)

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



    def test_deterministic_document_id_skips_existing_chunks(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "existing.md"
            document.write_text("# Existing\nContenido", encoding="utf-8")
            with patch.object(ingest, "document_chunk_count", return_value=3), \
                 patch.object(ingest, "generate_embeddings") as embeddings, \
                 patch.object(ingest, "store_chunks") as store:
                result = ingest.ingest_document(
                    document, title="Existente", category="test",
                    document_id="stable-document-id",
                )
            self.assertTrue(result["already_present"])
            self.assertEqual(result["chunks"], 3)
            embeddings.assert_not_called()
            store.assert_not_called()

    def test_default_document_id_is_stable_and_scope_specific(self):
        identity = {
            "document_sha256": "a" * 64, "title": "Manual", "category": "network",
            "source": "manual.pdf", "license": "CC-BY-4.0",
            "visibility": "tenant", "tenant_id": "tenant-a", "tags": ["dns", "tls"],
            "expected_embedding_model": "provider::embed-v1",
        }
        first = ingest._default_document_id(**identity)
        self.assertEqual(first, ingest._default_document_id(**identity))
        self.assertNotEqual(
            first,
            ingest._default_document_id(**{**identity, "tenant_id": "tenant-b"}),
        )
        self.assertNotEqual(
            first,
            ingest._default_document_id(**{**identity, "visibility": "shared", "tenant_id": None}),
        )
        self.assertNotEqual(
            first,
            ingest._default_document_id(**{**identity, "document_sha256": "b" * 64}),
        )

    def test_default_document_id_makes_retries_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "repeat.md"
            document.write_text("# Repeat\nTexto estable", encoding="utf-8")
            with patch.object(ingest, "document_chunk_count", side_effect=[0, 1]), \
                 patch.object(ingest, "generate_embeddings", return_value={
                     "model": "fixture-v1", "embedding_space": "fixture::v1",
                     "embeddings": [[1.0, 0.0]],
                 }) as embeddings, \
                 patch.object(ingest, "store_chunks", return_value=["chunk-1"]):
                first = ingest.ingest_document(
                    document, title="Repeat", category="test", source="repeat.md"
                )
                second = ingest.ingest_document(
                    document, title="Repeat", category="test", source="repeat.md"
                )
        self.assertEqual(first["document_id"], second["document_id"])
        self.assertFalse(first.get("already_present", False))
        self.assertTrue(second["already_present"])
        embeddings.assert_called_once()

    def test_invalid_deterministic_document_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "input.md"
            document.write_text("contenido", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "document_id"):
                ingest.ingest_document(
                    document, title="x", category="test", document_id="  "
                )


    def test_ingest_reindexes_when_embedding_space_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "changed-model.md"
            document.write_text("# Reindexar\nTexto de prueba", encoding="utf-8")
            with patch.object(ingest, "document_chunk_count", return_value=0), \
                 patch.object(ingest, "generate_embeddings", return_value={
                     "model": "model-v2", "embedding_space": "provider::model-v2",
                     "embeddings": [[1.0, 0.0]],
                 }), patch.object(ingest, "store_chunks", return_value=[{"id": "chunk"}]) as store:
                result = ingest.ingest_document(
                    document, title="Modelo nuevo", category="test",
                    document_id="stable-id", expected_embedding_model="provider::model-v2",
                )
            self.assertEqual(result["chunks"], 1)
            self.assertEqual(store.call_args.args[0][0]["embedding_model"], "provider::model-v2")

    def test_ingest_rejects_unexpected_embedding_space(self):
        with tempfile.TemporaryDirectory() as temp:
            document = Path(temp) / "wrong-model.md"
            document.write_text("# Wrong\nTexto de prueba", encoding="utf-8")
            with patch.object(ingest, "document_chunk_count", return_value=0), \
                 patch.object(ingest, "generate_embeddings", return_value={
                     "model": "model-v1", "embedding_space": "provider::model-v1",
                     "embeddings": [[1.0, 0.0]],
                 }), patch.object(ingest, "store_chunks") as store:
                with self.assertRaisesRegex(RuntimeError, "cambió de espacio"):
                    ingest.ingest_document(
                        document, title="Modelo incorrecto", category="test",
                        expected_embedding_model="provider::model-v2",
                    )
            store.assert_not_called()

if __name__ == "__main__":
    unittest.main()
