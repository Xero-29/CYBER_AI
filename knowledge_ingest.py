#!/usr/bin/env python3
"""Importa documentos de texto a la biblioteca indexada de CYBER_AI."""

import argparse
import hashlib
import uuid
from pathlib import Path

from knowledge_embeddings import generate_embeddings
from knowledge_library import store_chunk

PROJECT = Path(__file__).resolve().parent


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
    file_path = Path(file_path).expanduser().resolve()

    if not file_path.is_file():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")

    if file_path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError("Esta versión admite únicamente archivos .txt y .md.")

    if not 1 <= batch_size <= 32:
        raise ValueError("batch_size debe estar entre 1 y 32.")

    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(
            "El archivo no está codificado en UTF-8. "
            "Convierte su texto a UTF-8 e inténtalo de nuevo."
        ) from error

    chunks = split_text(text, max_chars=max_chars)
    document_id = uuid.uuid4().hex
    source = source or file_path.name

    # La huella permite identificar el documento importado en el informe.
    document_sha256 = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

    stored = []
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

            item = store_chunk(
                title=title,
                source=source,
                license=license,
                category=category,
                content=chunk,
                embedding=vector,
                embedding_model=result.get("embedding_space", result["model"]),
                document_id=document_id,
                chunk_index=index,
                tags=tags,
                visibility=visibility,
                tenant_id=tenant_id,
            )
            stored.append(item["id"])

        print(
            f"Procesados {min(start + len(batch), total)}/{total} "
            "fragmentos.",
            flush=True,
        )

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
    parser.add_argument("file", help="Archivo .txt o .md que se importará")
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
