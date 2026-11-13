#!/usr/bin/env python3
"""Importa documentos de texto a la biblioteca indexada de CYBER_AI."""

import argparse
import csv
import hashlib
import json
import zipfile
import uuid
from html.parser import HTMLParser
from pathlib import Path

from knowledge_embeddings import generate_embeddings
from knowledge_library import store_chunks

PROJECT = Path(__file__).resolve().parent
MAX_INPUT_BYTES = 100 * 1024 * 1024
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 256 * 1024 * 1024
MAX_EXTRACTED_CHARS = 10_000_000
TEXT_EXTENSIONS = {
    ".txt", ".md", ".rst", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".sh",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".log", ".sql",
    ".xml",
}


class _VisibleHTMLText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "noscript", "template"}:
            self.hidden_depth += 1
        elif tag.lower() in {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "section"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "noscript", "template"} and self.hidden_depth:
            self.hidden_depth -= 1
        elif tag.lower() in {"p", "div", "li", "tr", "h1", "h2", "h3", "section"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden_depth and data.strip():
            self.parts.append(data.strip())
            self.parts.append(" ")


def _validate_office_archive(path):
    try:
        with zipfile.ZipFile(path) as archive:
            items = archive.infolist()
            if len(items) > 10_000:
                raise ValueError("El documento Office contiene demasiadas entradas.")
            total = 0
            for item in items:
                name = item.filename.replace("\\", "/")
                if name.startswith("/") or ".." in Path(name).parts:
                    raise ValueError("El documento Office contiene rutas internas inválidas.")
                total += item.file_size
                if total > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                    raise ValueError("El contenido descomprimido supera el límite permitido.")
                if item.file_size / max(1, item.compress_size) > 500:
                    raise ValueError("Ratio de compresión sospechoso en el documento Office.")
    except zipfile.BadZipFile as error:
        raise ValueError("El documento Office no es un paquete ZIP válido.") from error


def extract_document_text(file_path):
    """Extrae texto de formatos comunes con límites de tamaño y expansión."""
    raw_path = Path(file_path).expanduser()
    if raw_path.is_symlink():
        raise ValueError("No se permiten enlaces simbólicos como documentos de entrada.")
    path = raw_path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("El documento supera el límite de 100 MiB.")
    suffix = path.suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as error:
            raise ValueError("El documento de texto debe estar codificado en UTF-8.") from error
    elif suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("El JSON no es válido o no está codificado en UTF-8.") from error
        text = json.dumps(data, ensure_ascii=False, indent=2)
    elif suffix == ".jsonl":
        try:
            records = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("El JSONL contiene una línea inválida o no está codificado en UTF-8.") from error
        text = "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in records)
    elif suffix in {".html", ".htm"}:
        try:
            parser = _VisibleHTMLText()
            parser.feed(path.read_text(encoding="utf-8-sig"))
            text = "".join(parser.parts)
        except UnicodeDecodeError as error:
            raise ValueError("El HTML debe estar codificado en UTF-8.") from error
    elif suffix == ".csv":
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as stream:
                rows = []
                for index, row in enumerate(csv.reader(stream), 1):
                    if index > 200_000:
                        raise ValueError("El CSV supera el límite de 200.000 filas.")
                    rows.append("\t".join(cell for cell in row))
            text = "\n".join(rows)
        except UnicodeDecodeError as error:
            raise ValueError("El CSV debe estar codificado en UTF-8.") from error
    elif suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as error:
            raise RuntimeError("Para PDF instala las dependencias opcionales: pip install -r requirements-documents.txt") from error
        reader = PdfReader(str(path), strict=True)
        if reader.is_encrypted:
            raise ValueError("No se ingieren PDF cifrados.")
        if len(reader.pages) > 5000:
            raise ValueError("El PDF supera el límite de 5.000 páginas.")
        text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
        if not text.strip():
            raise ValueError("El PDF no contiene texto extraíble; requiere OCR externo.")
    elif suffix == ".docx":
        _validate_office_archive(path)
        try:
            from docx import Document
        except ImportError as error:
            raise RuntimeError("Para DOCX instala requirements-documents.txt.") from error
        document = Document(str(path))
        parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        for table in document.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text for cell in row.cells))
        text = "\n".join(parts)
    elif suffix == ".xlsx":
        _validate_office_archive(path)
        try:
            from openpyxl import load_workbook
        except ImportError as error:
            raise RuntimeError("Para XLSX instala requirements-documents.txt.") from error
        workbook = load_workbook(path, read_only=True, data_only=True)
        parts = []
        count = 0
        try:
            for sheet in workbook.worksheets:
                parts.append(f"[Hoja: {sheet.title}]")
                for row in sheet.iter_rows(values_only=True):
                    count += 1
                    if count > 200_000:
                        raise ValueError("El XLSX supera el límite de 200.000 filas.")
                    parts.append(" | ".join("" if value is None else str(value) for value in row))
        finally:
            workbook.close()
        text = "\n".join(parts)
    elif suffix == ".pptx":
        _validate_office_archive(path)
        try:
            from pptx import Presentation
        except ImportError as error:
            raise RuntimeError("Para PPTX instala requirements-documents.txt.") from error
        presentation = Presentation(str(path))
        if len(presentation.slides) > 5000:
            raise ValueError("La presentación supera el límite de 5.000 diapositivas.")
        parts = []
        for index, slide in enumerate(presentation.slides, 1):
            parts.append(f"[Diapositiva {index}]")
            for shape in slide.shapes:
                if getattr(shape, "has_text_frame", False) and shape.text.strip():
                    parts.append(shape.text)
                if getattr(shape, "has_table", False):
                    for row in shape.table.rows:
                        parts.append(" | ".join(cell.text for cell in row.cells))
        text = "\n".join(parts)
    else:
        raise ValueError(f"Formato no soportado: {suffix or '(sin extensión)'}.")

    if len(text) > MAX_EXTRACTED_CHARS:
        raise ValueError("El texto extraído supera el límite de 10 millones de caracteres.")
    if not text.strip():
        raise ValueError("No se pudo extraer texto útil del documento.")
    return text


def split_text(text, max_chars=1200, overlap=150):
    """Divide un documento en fragmentos que conservan su contenido."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("El documento está vacío.")

    if max_chars < 300:
        raise ValueError("max_chars debe ser al menos 300.")

    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap debe ser menor que max_chars.")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        # Los párrafos largos se dividen conservando algo de contexto.
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""

            start = 0
            while start < len(paragraph):
                end = min(start + max_chars, len(paragraph))

                # Preferimos cortar entre palabras cuando sea posible.
                if end < len(paragraph):
                    boundary = paragraph.rfind(
                        " ", start + max_chars // 2, end
                    )
                    if boundary > start:
                        end = boundary

                part = paragraph[start:end].strip()
                if part:
                    chunks.append(part)

                if end >= len(paragraph):
                    break

                start = max(start + 1, end - overlap)

            continue

        candidate = (
            current + "\n\n" + paragraph
            if current else paragraph
        )

        if len(candidate) <= max_chars:
            current = candidate
        else:
            chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    if not chunks:
        raise ValueError("No se pudieron crear fragmentos del documento.")

    return chunks


def ingest_document(
    file_path,
    *,
    title,
    category,
    source=None,
    license="UNSPECIFIED",
    visibility="shared",
    tenant_id=None,
    tags=None,
    batch_size=8,
    max_chars=1200,
):
    """Lee un documento, genera sus embeddings y almacena los fragmentos."""
    raw_file_path = Path(file_path).expanduser()
    if raw_file_path.is_symlink():
        raise ValueError("No se permiten enlaces simbólicos como documentos de entrada.")
    file_path = raw_file_path.resolve()

    if not file_path.is_file():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")

    if not 1 <= batch_size <= 32:
        raise ValueError("batch_size debe estar entre 1 y 32.")

    text = extract_document_text(file_path)

    chunks = split_text(text, max_chars=max_chars)
    document_id = uuid.uuid4().hex
    source = source or file_path.name

    # La huella permite identificar el documento importado en el informe.
    document_sha256 = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

    pending_chunks = []
    total = len(chunks)

    for start in range(0, total, batch_size):
        batch = chunks[start:start + batch_size]

        # ECO genera un vector por fragmento en una petición por lote.
        result = generate_embeddings(batch, agent_name="ECO")

        if len(result["embeddings"]) != len(batch):
            raise RuntimeError(
                "La cantidad de embeddings no coincide con los fragmentos."
            )

        for offset, (chunk, vector) in enumerate(
            zip(batch, result["embeddings"])
        ):
            index = start + offset

            pending_chunks.append({
                "title": title,
                "source": source,
                "license": license,
                "category": category,
                "content": chunk,
                "embedding": vector,
                "embedding_model": result.get("embedding_space", result["model"]),
                "document_id": document_id,
                "chunk_index": index,
                "tags": tags,
                "visibility": visibility,
                "tenant_id": tenant_id,
            })

        print(
            f"Generados embeddings {min(start + len(batch), total)}/{total} "
            "fragmentos.",
            flush=True,
        )

    # Publica todos los fragmentos juntos: si falla cualquier lote de embeddings,
    # la biblioteca no queda con una versión parcial del documento.
    stored = store_chunks(pending_chunks)

    return {
        "document_id": document_id,
        "document_sha256": document_sha256,
        "title": title,
        "source": source,
        "license": license,
        "category": category,
        "visibility": visibility,
        "tenant_id": tenant_id,
        "chunks": len(stored),
        "chunk_ids": stored,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Documento TXT, MD, HTML, CSV, JSON, código, PDF, DOCX, XLSX o PPTX")
    parser.add_argument("--title", required=True, help="Título del documento")
    parser.add_argument("--category", required=True, help="Categoría del conocimiento")
    parser.add_argument("--source", default=None, help="Nombre de la fuente")
    parser.add_argument(
        "--license", default="UNSPECIFIED",
        help="Licencia declarada de la fuente importada",
    )
    parser.add_argument(
        "--visibility",
        choices=("shared", "tenant"),
        default="shared",
        help="shared: biblioteca compartida; tenant: privada de una empresa",
    )
    parser.add_argument(
        "--tenant-id",
        default=None,
        help="Identificador de la empresa cuando visibility=tenant",
    )
    parser.add_argument(
        "--tag", action="append", default=[],
        help="Etiqueta del documento; la opción puede repetirse",
    )
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-chars", type=int, default=1200)
    args = parser.parse_args()

    if args.visibility == "tenant" and not args.tenant_id:
        parser.error("--tenant-id es obligatorio para documentos privados")

    if args.visibility == "shared" and args.tenant_id:
        parser.error("--tenant-id solo se usa con --visibility tenant")

    result = ingest_document(
        args.file,
        title=args.title,
        category=args.category,
        source=args.source,
        license=args.license,
        visibility=args.visibility,
        tenant_id=args.tenant_id,
        tags=args.tag,
        batch_size=args.batch_size,
        max_chars=args.max_chars,
    )

    print("\nImportación completada.")
    print("Título:", result["title"])
    print("ID de documento:", result["document_id"])
    print("SHA-256:", result["document_sha256"])
    print("Fragmentos guardados:", result["chunks"])
    print("Visibilidad:", result["visibility"])


if __name__ == "__main__":
    main()
