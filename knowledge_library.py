#!/usr/bin/env python3
"""Biblioteca indexada de conocimientos para CYBER_AI.

Almacena fragmentos comprimidos, metadatos y embeddings.
Permite búsqueda por similitud semántica y separación por empresa.
No llama directamente a ningún modelo; ECO proporcionará los vectores.
"""

import hashlib
import json
import math
import sqlite3
import uuid
import zlib

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
DB_PATH = PROJECT / "data" / "knowledge_library.sqlite3"


def utc_now():
    """Devuelve la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def database():
    """Abre SQLite y confirma o revierte cada operación."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DB_PATH), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 10000")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize():
    """Crea la biblioteca y sus índices si no existen."""
    with database() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS knowledge_chunks (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                license TEXT NOT NULL DEFAULT 'UNSPECIFIED',
                category TEXT NOT NULL,
                tags_json TEXT NOT NULL DEFAULT '[]',
                visibility TEXT NOT NULL
                    CHECK (visibility IN ('shared', 'tenant')),
                tenant_id TEXT,
                content_z BLOB NOT NULL,
                content_sha256 TEXT NOT NULL,
                original_bytes INTEGER NOT NULL,
                compressed_bytes INTEGER NOT NULL,
                embedding_json TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_dimensions INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                CHECK (
                    (visibility = 'shared' AND tenant_id IS NULL)
                    OR
                    (visibility = 'tenant' AND tenant_id IS NOT NULL)
                )
            );

            CREATE INDEX IF NOT EXISTS idx_knowledge_document
            ON knowledge_chunks(document_id, chunk_index);

            CREATE INDEX IF NOT EXISTS idx_knowledge_category
            ON knowledge_chunks(category);

            CREATE INDEX IF NOT EXISTS idx_knowledge_scope
            ON knowledge_chunks(visibility, tenant_id);

            CREATE INDEX IF NOT EXISTS idx_knowledge_embedding_model
            ON knowledge_chunks(embedding_model);
        """)

        # Migración compatible: conservar todos los fragmentos existentes.
        columns = {
            row["name"]
            for row in db.execute("PRAGMA table_info(knowledge_chunks)")
        }
        if "license" not in columns:
            db.execute(
                "ALTER TABLE knowledge_chunks ADD COLUMN "
                "license TEXT NOT NULL DEFAULT 'UNSPECIFIED'"
            )



def validate_vector(vector):
    """Valida un vector numérico antes de guardarlo o consultarlo."""
    if not isinstance(vector, (list, tuple)) or not vector:
        raise ValueError("El embedding debe ser una lista numérica no vacía.")

    values = []
    for value in vector:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("El embedding contiene un valor no numérico.")

        value = float(value)
        if not math.isfinite(value):
            raise ValueError("El embedding contiene un valor no finito.")
        values.append(value)

    if math.sqrt(sum(value * value for value in values)) == 0:
        raise ValueError("El embedding no puede ser un vector de ceros.")

    return values


def cosine_similarity(left, right):
    """Calcula similitud coseno entre dos vectores de igual dimensión."""
    left = validate_vector(left)
    right = validate_vector(right)

    if len(left) != len(right):
        raise ValueError("Los embeddings tienen dimensiones diferentes.")

    dot = sum(a * b for a, b in zip(left, right))
    norm_left = math.sqrt(sum(a * a for a in left))
    norm_right = math.sqrt(sum(b * b for b in right))

    return dot / (norm_left * norm_right)


def store_chunk(
    *,
    title,
    source,
    category,
    content,
    embedding,
    embedding_model,
    license="UNSPECIFIED",
    document_id=None,
    chunk_index=0,
    tags=None,
    visibility="shared",
    tenant_id=None,
):
    """Comprime y registra un fragmento de conocimiento con su embedding."""
    for field, value in (
        ("title", title),
        ("source", source),
        ("license", license),
        ("category", category),
        ("content", content),
        ("embedding_model", embedding_model),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} es obligatorio y debe ser texto.")

    if visibility not in {"shared", "tenant"}:
        raise ValueError("visibility debe ser 'shared' o 'tenant'.")

    if visibility == "tenant" and (
        not isinstance(tenant_id, str) or not tenant_id.strip()
    ):
        raise ValueError("Los conocimientos privados requieren tenant_id.")

    if visibility == "shared" and tenant_id is not None:
        raise ValueError(
            "Los conocimientos compartidos no deben tener tenant_id."
        )

    if not isinstance(chunk_index, int) or chunk_index < 0:
        raise ValueError("chunk_index debe ser un entero no negativo.")

    vector = validate_vector(embedding)
    original = content.encode("utf-8")
    compressed = zlib.compress(original, level=9)
    digest = hashlib.sha256(original).hexdigest()
    chunk_id = uuid.uuid4().hex
    document_id = document_id or uuid.uuid4().hex
    tags = list(dict.fromkeys(tags or []))

    if not all(isinstance(tag, str) and tag.strip() for tag in tags):
        raise ValueError("Cada etiqueta debe ser texto no vacío.")

    initialize()

    with database() as db:
        db.execute("""
            INSERT INTO knowledge_chunks (
                id, document_id, chunk_index, title, source, license,
                category, tags_json, visibility, tenant_id, content_z,
                content_sha256, original_bytes, compressed_bytes,
                embedding_json, embedding_model, embedding_dimensions,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chunk_id, document_id, chunk_index, title.strip(),
            source.strip(), license.strip(), category.strip(),
            json.dumps(tags, ensure_ascii=False),
            visibility, tenant_id, sqlite3.Binary(compressed),
            digest, len(original), len(compressed),
            json.dumps(vector), embedding_model.strip(), len(vector),
            utc_now(),
        ))

    return {
        "id": chunk_id,
        "document_id": document_id,
        "chunk_index": chunk_index,
        "license": license.strip(),
        "original_bytes": len(original),
        "compressed_bytes": len(compressed),
        "sha256": digest,
    }


def read_chunk(chunk_id, tenant_id=None):
    """Lee y verifica un único fragmento autorizado."""
    initialize()

    with database() as db:
        if tenant_id is None:
            row = db.execute("""
                SELECT * FROM knowledge_chunks
                WHERE id = ? AND visibility = 'shared'
            """, (chunk_id,)).fetchone()
        else:
            row = db.execute("""
                SELECT * FROM knowledge_chunks
                WHERE id = ?
                  AND (
                      visibility = 'shared'
                      OR (visibility = 'tenant' AND tenant_id = ?)
                  )
            """, (chunk_id, tenant_id)).fetchone()

    if row is None:
        raise KeyError("Fragmento inexistente o no autorizado.")

    try:
        original = zlib.decompress(row["content_z"])
    except zlib.error as error:
        raise ValueError("El fragmento comprimido está dañado.") from error

    if hashlib.sha256(original).hexdigest() != row["content_sha256"]:
        raise ValueError("La comprobación SHA-256 del fragmento ha fallado.")

    if len(original) != row["original_bytes"]:
        raise ValueError("El tamaño original del fragmento no coincide.")

    try:
        content = original.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("El fragmento no contiene UTF-8 válido.") from error

    return {
        "id": row["id"],
        "document_id": row["document_id"],
        "chunk_index": row["chunk_index"],
        "title": row["title"],
        "source": row["source"],
        "license": row["license"],
        "category": row["category"],
        "tags": json.loads(row["tags_json"]),
        "visibility": row["visibility"],
        "content": content,
        "embedding_model": row["embedding_model"],
        "created_at": row["created_at"],
    }


def search_knowledge(
    *,
    query_embedding,
    embedding_model,
    top_k=5,
    tenant_id=None,
    categories=None,
    tags=None,
    min_score=-1.0,
):
    """Busca por similitud y descomprime únicamente los mejores fragmentos.

    La primera versión calcula la similitud recorriendo los vectores
    permitidos. Los índices SQL filtran por modelo, categoría y alcance.
    Para bibliotecas enormes se podrá sustituir por un índice vectorial
    especializado sin cambiar la interfaz pública de búsqueda.
    """
    query_vector = validate_vector(query_embedding)

    if not isinstance(embedding_model, str) or not embedding_model.strip():
        raise ValueError("embedding_model es obligatorio.")

    top_k = max(1, min(int(top_k), 50))
    if not math.isfinite(float(min_score)) or min_score < -1 or min_score > 1:
        raise ValueError("min_score debe estar entre -1 y 1.")

    query = """
        SELECT id, embedding_json, embedding_dimensions, tags_json
        FROM knowledge_chunks
        WHERE embedding_model = ?
          AND (
              visibility = 'shared'
              OR (visibility = 'tenant' AND tenant_id = ?)
          )
    """
    parameters = [embedding_model, tenant_id]

    if tenant_id is None:
        query = """
            SELECT id, embedding_json, embedding_dimensions, tags_json
            FROM knowledge_chunks
            WHERE embedding_model = ?
              AND visibility = 'shared'
        """
        parameters = [embedding_model]

    categories = list(dict.fromkeys(categories or []))
    if categories:
        placeholders = ",".join("?" for _ in categories)
        query += f" AND category IN ({placeholders})"
        parameters.extend(categories)

    if tags is None:
        tags = []
    elif isinstance(tags, str) or not isinstance(tags, (list, tuple)):
        raise ValueError("tags debe ser una lista de etiquetas.")
    if any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        raise ValueError("Cada etiqueta debe ser texto no vacío.")
    tags = list(dict.fromkeys(tags))

    initialize()
    with database() as db:
        candidates = db.execute(query, parameters).fetchall()

    ranked = []
    for row in candidates:
        # Filtrar por etiqueta exacta antes de calcular similitud.
        if tags:
            try:
                stored_tags = json.loads(row["tags_json"])
            except (TypeError, json.JSONDecodeError):
                continue
            if not set(tags).intersection(stored_tags):
                continue

        if row["embedding_dimensions"] != len(query_vector):
            continue

        try:
            vector = json.loads(row["embedding_json"])
            score = cosine_similarity(query_vector, vector)
        except (ValueError, TypeError, json.JSONDecodeError):
            continue

        if score >= min_score:
            ranked.append((score, row["id"]))

    ranked.sort(key=lambda item: item[0], reverse=True)

    results = []
    for score, chunk_id in ranked[:top_k]:
        item = read_chunk(chunk_id, tenant_id=tenant_id)
        item["similarity"] = score
        results.append(item)

    return results


def list_knowledge(
    *,
    tenant_id=None,
    category=None,
    limit=50,
):
    """Lista metadatos sin descomprimir los contenidos."""
    limit = max(1, min(int(limit), 200))
    query = """
        SELECT id, document_id, chunk_index, title, source, license, category,
               tags_json, visibility, tenant_id, original_bytes,
               compressed_bytes, embedding_model, created_at
        FROM knowledge_chunks
        WHERE visibility = 'shared'
    """
    parameters = []

    if tenant_id is not None:
        query = """
            SELECT id, document_id, chunk_index, title, source, category,
                   tags_json, visibility, tenant_id, original_bytes,
                   compressed_bytes, embedding_model, created_at
            FROM knowledge_chunks
            WHERE (
                visibility = 'shared'
                OR (visibility = 'tenant' AND tenant_id = ?)
            )
        """
        parameters.append(tenant_id)

    if category is not None:
        query += " AND category = ?"
        parameters.append(category)

    query += " ORDER BY created_at DESC LIMIT ?"
    parameters.append(limit)

    initialize()
    with database() as db:
        rows = db.execute(query, parameters).fetchall()

    result = []
    for row in rows:
        item = dict(row)
        item["tags"] = json.loads(item.pop("tags_json"))
        result.append(item)

    return result
