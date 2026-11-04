#!/usr/bin/env python3
"""Almacén comprimido por bloques para CYBER_AI."""

import hashlib
import json
import sqlite3
import uuid
import zlib

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
DB_PATH = PROJECT / "data" / "compressed_memory.sqlite3"


def utc_now():
    """Devuelve la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def database():
    """Abre SQLite y guarda los cambios de cada operación."""
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
    """Crea la tabla y los índices si todavía no existen."""
    with database() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS compressed_blocks (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                task_id TEXT,
                kind TEXT NOT NULL,
                compressed_data BLOB NOT NULL,
                sha256 TEXT NOT NULL,
                original_bytes INTEGER NOT NULL,
                compressed_bytes INTEGER NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_blocks_session_task
            ON compressed_blocks(session_id, task_id);

            CREATE INDEX IF NOT EXISTS idx_blocks_session_kind
            ON compressed_blocks(session_id, kind);
        """)


def store_block(
    *,
    content,
    session_id,
    task_id=None,
    kind="note",
    metadata=None,
):
    """Comprime y almacena un bloque independiente sin pérdida de datos."""
    if not isinstance(content, str):
        raise TypeError("content debe ser texto.")

    if not session_id or not str(session_id).strip():
        raise ValueError("session_id es obligatorio.")

    if not kind or not str(kind).strip():
        raise ValueError("kind es obligatorio.")

    original = content.encode("utf-8")
    compressed = zlib.compress(original, level=9)
    block_id = uuid.uuid4().hex

    initialize()

    with database() as db:
        db.execute("""
            INSERT INTO compressed_blocks (
                id, session_id, task_id, kind, compressed_data,
                sha256, original_bytes, compressed_bytes,
                metadata_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            block_id,
            str(session_id),
            task_id,
            str(kind),
            sqlite3.Binary(compressed),
            hashlib.sha256(original).hexdigest(),
            len(original),
            len(compressed),
            json.dumps(metadata or {}, ensure_ascii=False),
            utc_now(),
        ))

    return {
        "id": block_id,
        "session_id": str(session_id),
        "task_id": task_id,
        "kind": str(kind),
        "original_bytes": len(original),
        "compressed_bytes": len(compressed),
        "sha256": hashlib.sha256(original).hexdigest(),
    }


def read_block(block_id, session_id):
    """Recupera solamente un bloque de la sesión autorizada."""
    initialize()

    with database() as db:
        row = db.execute("""
            SELECT * FROM compressed_blocks
            WHERE id = ? AND session_id = ?
        """, (block_id, session_id)).fetchone()

    if row is None:
        raise KeyError("Bloque inexistente o ajeno a esta sesión.")

    try:
        original = zlib.decompress(row["compressed_data"])
    except zlib.error as error:
        raise ValueError("El bloque comprimido está dañado.") from error

    actual_hash = hashlib.sha256(original).hexdigest()
    if actual_hash != row["sha256"]:
        raise ValueError("La comprobación SHA-256 ha fallado.")

    if len(original) != row["original_bytes"]:
        raise ValueError("El tamaño original no coincide.")

    try:
        content = original.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("El bloque recuperado no es texto UTF-8 válido.") from error

    return {
        "id": row["id"],
        "session_id": row["session_id"],
        "task_id": row["task_id"],
        "kind": row["kind"],
        "content": content,
        "metadata": json.loads(row["metadata_json"]),
        "created_at": row["created_at"],
    }


def list_blocks(session_id, task_id=None, kind=None, limit=20):
    """Consulta el índice sin descomprimir el contenido de los bloques."""
    if not session_id:
        raise ValueError("session_id es obligatorio.")

    limit = max(1, min(int(limit), 100))

    query = """
        SELECT id, session_id, task_id, kind, sha256,
               original_bytes, compressed_bytes, created_at
        FROM compressed_blocks
        WHERE session_id = ?
    """
    parameters = [session_id]

    if task_id is not None:
        query += " AND task_id = ?"
        parameters.append(task_id)

    if kind is not None:
        query += " AND kind = ?"
        parameters.append(kind)

    query += " ORDER BY created_at DESC LIMIT ?"
    parameters.append(limit)

    initialize()

    with database() as db:
        rows = db.execute(query, parameters).fetchall()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize()
    print("Almacén comprimido inicializado.")
    print("Base de datos:", DB_PATH)
