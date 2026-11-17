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
import re

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
DB_PATH = PROJECT / "data" / "knowledge_library.sqlite3"
MAX_CHUNK_BYTES = 2 * 1024 * 1024


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
        try:
            db.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_chunks_fts "
                "USING fts5(chunk_id UNINDEXED, title, source, "
                "category UNINDEXED, content, tokenize='unicode61')"
            )
        except sqlite3.OperationalError as error:
            if "no such module: fts5" not in str(error).lower():
                raise
            # SQLite compilado sin FTS5 conserva la búsqueda semántica existente.

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


def _prepare_chunk(chunk):
    """Valida y prepara un fragmento sin escribirlo en la base de datos."""
    if not isinstance(chunk, dict):
        raise ValueError("Cada fragmento debe ser un objeto.")
    allowed = {
        "title", "source", "category", "content", "embedding",
        "embedding_model", "license", "document_id", "chunk_index",
        "tags", "visibility", "tenant_id",
    }
    unknown = set(chunk) - allowed
    if unknown:
        raise ValueError(f"Campos de fragmento no reconocidos: {sorted(unknown)}")

    title = chunk.get("title")
    source = chunk.get("source")
    category = chunk.get("category")
    content = chunk.get("content")
    embedding_model = chunk.get("embedding_model")
    license_name = chunk.get("license", "UNSPECIFIED")
    for field, value in (
        ("title", title), ("source", source), ("license", license_name),
        ("category", category), ("content", content),
        ("embedding_model", embedding_model),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} es obligatorio y debe ser texto.")

    visibility = chunk.get("visibility", "shared")
    tenant_id = chunk.get("tenant_id")
    if not isinstance(visibility, str) or visibility not in {"shared", "tenant"}:
        raise ValueError("visibility debe ser 'shared' o 'tenant'.")
    if visibility == "tenant" and (
        not isinstance(tenant_id, str) or not tenant_id.strip()
    ):
        raise ValueError("Los conocimientos privados requieren tenant_id.")
    if visibility == "shared" and tenant_id is not None:
        raise ValueError("Los conocimientos compartidos no deben tener tenant_id.")
    if tenant_id is not None:
        tenant_id = tenant_id.strip()

    chunk_index = chunk.get("chunk_index", 0)
    if isinstance(chunk_index, bool) or not isinstance(chunk_index, int) or chunk_index < 0:
        raise ValueError("chunk_index debe ser un entero no negativo.")

    tags = chunk.get("tags")
    if tags is None:
        tags = []
    if not isinstance(tags, (list, tuple)):
        raise ValueError("tags debe ser una lista de textos.")
    if not all(isinstance(tag, str) and tag.strip() for tag in tags):
        raise ValueError("Cada etiqueta debe ser texto no vacío.")
    tags = list(dict.fromkeys(tag.strip() for tag in tags))

    document_id = chunk.get("document_id")
    if document_id is None:
        document_id = uuid.uuid4().hex
    elif not isinstance(document_id, str) or not document_id.strip():
        raise ValueError("document_id debe ser texto no vacío.")
    else:
        document_id = document_id.strip()

    vector = validate_vector(chunk.get("embedding"))
    original = content.encode("utf-8")
    if len(original) > MAX_CHUNK_BYTES:
        raise ValueError("El fragmento supera el límite de 2 MiB.")
    compressed = zlib.compress(original, level=9)
    digest = hashlib.sha256(original).hexdigest()
    chunk_id = uuid.uuid4().hex
    stamp = utc_now()
    values = (
        chunk_id, document_id, chunk_index, title.strip(), source.strip(),
        license_name.strip(), category.strip(), json.dumps(tags, ensure_ascii=False),
        visibility, tenant_id, sqlite3.Binary(compressed), digest,
        len(original), len(compressed), json.dumps(vector),
        embedding_model.strip(), len(vector), stamp,
    )
    result = {
        "id": chunk_id, "document_id": document_id,
        "chunk_index": chunk_index, "license": license_name.strip(),
        "original_bytes": len(original), "compressed_bytes": len(compressed),
        "sha256": digest,
    }
    return values, result


def store_chunks(chunks):
    """Valida todos los fragmentos y los publica en una única transacción."""
    if not isinstance(chunks, (list, tuple)) or not chunks:
        raise ValueError("chunks debe ser una lista no vacía.")
    prepared = [_prepare_chunk(chunk) for chunk in chunks]
    initialize()
    with database() as db:
        db.executemany("""
            INSERT INTO knowledge_chunks (
                id, document_id, chunk_index, title, source, license,
                category, tags_json, visibility, tenant_id, content_z,
                content_sha256, original_bytes, compressed_bytes,
                embedding_json, embedding_model, embedding_dimensions,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [item[0] for item in prepared])
        if _text_index_available(db):
            db.executemany(
                "INSERT INTO knowledge_chunks_fts "
                "(chunk_id,title,source,category,content) VALUES (?,?,?,?,?)",
                [(item["id"], chunk["title"], chunk["source"],
                  chunk["category"], chunk["content"])
                 for chunk, item in zip(chunks, (entry[1] for entry in prepared))],
            )
    return [item[1] for item in prepared]


def _text_index_available(db):
    return db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='knowledge_chunks_fts'"
    ).fetchone() is not None


def text_index_available():
    initialize()
    with database() as db:
        return _text_index_available(db)


def rebuild_text_index(batch_size=128):
    """Reconstruye FTS5 verificando SHA-256 y límites de cada fragmento."""
    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or not 1 <= batch_size <= 1000:
        raise ValueError("batch_size debe estar entre 1 y 1000.")
    initialize()
    with database() as db:
        if not _text_index_available(db):
            return {"available": False, "indexed": 0}
        db.execute("DELETE FROM knowledge_chunks_fts")
        cursor = db.execute(
            "SELECT id,title,source,category,content_z,content_sha256,"
            "original_bytes,compressed_bytes FROM knowledge_chunks ORDER BY id"
        )
        indexed = 0
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            entries = []
            for row in rows:
                if (row["original_bytes"] < 0 or row["original_bytes"] > MAX_CHUNK_BYTES
                        or row["compressed_bytes"] < 0 or len(row["content_z"]) != row["compressed_bytes"]):
                    raise ValueError("Metadatos de fragmento inválidos durante rebuild FTS.")
                decoder = zlib.decompressobj()
                raw = decoder.decompress(row["content_z"], MAX_CHUNK_BYTES + 1)
                if (len(raw) > MAX_CHUNK_BYTES or decoder.unconsumed_tail
                        or decoder.unused_data or not decoder.eof
                        or len(raw) != row["original_bytes"]
                        or hashlib.sha256(raw).hexdigest() != row["content_sha256"]):
                    raise ValueError("Fragmento corrupto durante rebuild FTS.")
                try:
                    content = raw.decode("utf-8")
                except UnicodeDecodeError as error:
                    raise ValueError("Fragmento no UTF-8 durante rebuild FTS.") from error
                entries.append((row["id"], row["title"], row["source"], row["category"], content))
            db.executemany(
                "INSERT INTO knowledge_chunks_fts "
                "(chunk_id,title,source,category,content) VALUES (?,?,?,?,?)",
                entries,
            )
            indexed += len(entries)
    return {"available": True, "indexed": indexed}


def _fts_terms(query):
    tokens = re.findall(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ_-]+", str(query).casefold())
    return list(dict.fromkeys(token for token in tokens if len(token) > 1))[:32]


def search_knowledge_hybrid(
    *, query_text, query_embedding, embedding_model, top_k=5,
    tenant_id=None, categories=None, tags=None, min_score=-1.0,
    rrf_constant=60,
):
    """Combina similitud vectorial y FTS5 mediante Reciprocal Rank Fusion."""
    if not isinstance(query_text, str) or not query_text.strip():
        raise ValueError("query_text es obligatorio.")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 50:
        raise ValueError("top_k debe estar entre 1 y 50.")
    if isinstance(rrf_constant, bool) or not isinstance(rrf_constant, int) or not 1 <= rrf_constant <= 1000:
        raise ValueError("rrf_constant debe estar entre 1 y 1000.")
    if categories is not None and (
        isinstance(categories, str) or not isinstance(categories, (list, tuple))
        or any(not isinstance(value, str) or not value.strip() for value in categories)
    ):
        raise ValueError("categories debe ser una lista de textos.")
    if tags is not None and (
        isinstance(tags, str) or not isinstance(tags, (list, tuple))
        or any(not isinstance(value, str) or not value.strip() for value in tags)
    ):
        raise ValueError("tags debe ser una lista de textos.")
    semantic = search_knowledge(
        query_embedding=query_embedding, embedding_model=embedding_model,
        top_k=min(50, top_k * 3), tenant_id=tenant_id, categories=categories,
        tags=tags, min_score=min_score,
    )
    scores, items = {}, {}
    for rank, item in enumerate(semantic, 1):
        items[item["id"]] = dict(item)
        scores[item["id"]] = scores.get(item["id"], 0.0) + 1.0 / (rrf_constant + rank)

    terms = _fts_terms(query_text)
    text_ids = []
    with database() as db:
        if _text_index_available(db) and terms:
            match = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
            sql = (
                "SELECT f.chunk_id FROM knowledge_chunks_fts AS f "
                "JOIN knowledge_chunks AS k ON k.id=f.chunk_id "
                "WHERE knowledge_chunks_fts MATCH ? AND k.embedding_model = ? "
                "AND (k.visibility='shared'"
            )
            params = [match, embedding_model]
            if tenant_id is not None:
                sql += " OR (k.visibility='tenant' AND k.tenant_id = ?)"
                params.append(tenant_id)
            sql += ")"
            if categories:
                sql += " AND k.category IN (" + ",".join("?" for _ in categories) + ")"
                params.extend(categories)
            sql += " ORDER BY bm25(knowledge_chunks_fts) LIMIT ?"
            params.append(min(150, top_k * 10))
            rows = db.execute(sql, params).fetchall()
            for row in rows:
                chunk_id = row["chunk_id"]
                if tags:
                    tag_row = db.execute(
                        "SELECT tags_json FROM knowledge_chunks WHERE id=?",
                        (chunk_id,),
                    ).fetchone()
                    if tag_row is None or not set(tags).intersection(json.loads(tag_row["tags_json"])):
                        continue
                text_ids.append(chunk_id)

    for rank, chunk_id in enumerate(text_ids, 1):
        if chunk_id not in items:
            items[chunk_id] = read_chunk(chunk_id, tenant_id=tenant_id)
            items[chunk_id]["similarity"] = 0.0
        items[chunk_id]["text_rank"] = rank
        scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (rrf_constant + rank)

    ranked = sorted(scores, key=lambda key: scores[key], reverse=True)[:top_k]
    output = []
    for chunk_id in ranked:
        item = items[chunk_id]
        item["hybrid_score"] = scores[chunk_id]
        item.setdefault("text_rank", None)
        output.append(item)
    return output


def document_chunk_count(
    document_id, embedding_model=None, *, visibility=None, tenant_id=None
):
    """Cuenta fragmentos publicados, opcionalmente dentro de un ámbito autorizado."""
    if not isinstance(document_id, str) or not document_id.strip():
        raise ValueError("document_id es obligatorio.")
    if embedding_model is not None and (
        not isinstance(embedding_model, str) or not embedding_model.strip()
    ):
        raise ValueError("embedding_model debe ser texto no vacío.")
    if visibility is not None:
        if not isinstance(visibility, str) or visibility not in {"shared", "tenant"}:
            raise ValueError("visibility debe ser 'shared' o 'tenant'.")
        if visibility == "tenant" and (
            not isinstance(tenant_id, str) or not tenant_id.strip()
        ):
            raise ValueError("tenant_id es obligatorio para contar conocimiento privado.")
        if visibility == "shared" and tenant_id is not None:
            raise ValueError("El ámbito shared no admite tenant_id.")
    elif tenant_id is not None:
        raise ValueError("tenant_id requiere un filtro visibility.")

    initialize()
    filters = ["document_id = ?"]
    parameters = [document_id.strip()]
    if embedding_model is not None:
        filters.append("embedding_model = ?")
        parameters.append(embedding_model.strip())
    if visibility is not None:
        filters.append("visibility = ?")
        parameters.append(visibility)
        if visibility == "tenant":
            filters.append("tenant_id = ?")
            parameters.append(tenant_id.strip())
    query = (
        "SELECT COUNT(*) AS total FROM knowledge_chunks WHERE "
        + " AND ".join(filters)
    )
    with database() as db:
        row = db.execute(query, tuple(parameters)).fetchone()
    return int(row["total"])


def store_chunk(**kwargs):
    """Compatibilidad: almacena un único fragmento en una transacción."""
    return store_chunks([kwargs])[0]


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

    if (
        row["original_bytes"] < 0
        or row["original_bytes"] > MAX_CHUNK_BYTES
        or row["compressed_bytes"] < 0
        or len(row["content_z"]) != row["compressed_bytes"]
    ):
        raise ValueError("El tamaño declarado del fragmento no es válido.")

    try:
        decompressor = zlib.decompressobj()
        original = decompressor.decompress(row["content_z"], MAX_CHUNK_BYTES + 1)
    except zlib.error as error:
        raise ValueError("El fragmento comprimido está dañado.") from error
    if (
        len(original) > MAX_CHUNK_BYTES
        or decompressor.unconsumed_tail
        or decompressor.unused_data
        or not decompressor.eof
    ):
        raise ValueError("El fragmento comprimido excede los límites o está incompleto.")

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
    embedding_model = embedding_model.strip()

    if isinstance(top_k, bool) or not isinstance(top_k, int):
        raise ValueError("top_k debe ser un entero.")
    top_k = max(1, min(top_k, 50))
    if (
        isinstance(min_score, bool)
        or not isinstance(min_score, (int, float))
        or not math.isfinite(float(min_score))
        or min_score < -1
        or min_score > 1
    ):
        raise ValueError("min_score debe ser un número entre -1 y 1.")
    min_score = float(min_score)
    if tenant_id is not None and (
        not isinstance(tenant_id, str) or not tenant_id.strip()
    ):
        raise ValueError("tenant_id debe ser texto no vacío.")

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

    if categories is None:
        categories = []
    elif isinstance(categories, str) or not isinstance(categories, (list, tuple)):
        raise ValueError("categories debe ser una lista de categorías.")
    if any(not isinstance(category, str) or not category.strip() for category in categories):
        raise ValueError("Cada categoría debe ser texto no vacío.")
    categories = list(dict.fromkeys(category.strip() for category in categories))
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
    tags = list(dict.fromkeys(tag.strip() for tag in tags))

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
