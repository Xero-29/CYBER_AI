#!/usr/bin/env python3
"""Almacén comprimido por bloques para CYBER_AI."""

import hashlib
import json
import math
import sqlite3
import uuid
import zlib

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from private_sqlite import connect_private_sqlite

PROJECT = Path(__file__).resolve().parent
DB_PATH = PROJECT / "data" / "compressed_memory.sqlite3"
MAX_BLOCK_BYTES = 2 * 1024 * 1024
MAX_METADATA_BYTES = 64 * 1024


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Los metadatos del bloque contienen claves duplicadas.")
        result[key] = value
    return result


def _reject_json_constant(value):
    raise ValueError("Los metadatos del bloque contienen una constante no estándar.")


def _parse_finite_float(value):
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("Los metadatos del bloque contienen un número no finito.")
    mantissa = value.lower().split("e", 1)[0]
    if parsed == 0.0 and any(digit in "123456789" for digit in mantissa):
        raise ValueError("Los metadatos del bloque contienen un número subdesbordado.")
    return parsed


def _strict_metadata_json(value):
    metadata = json.loads(
        value,
        object_pairs_hook=_unique_json_object,
        parse_constant=_reject_json_constant,
        parse_float=_parse_finite_float,
    )
    if not isinstance(metadata, dict):
        raise ValueError("Los metadatos del bloque deben ser un objeto.")
    return metadata


def utc_now():
    """Devuelve la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def database():
    """Abre SQLite y guarda los cambios de cada operación."""
    connection = connect_private_sqlite(DB_PATH, timeout=10)
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
    session_text = str(session_id).strip()
    if len(session_text) > 128 or any(ord(char) < 0x20 for char in session_text):
        raise ValueError("session_id supera el límite o contiene controles.")

    if not kind or not str(kind).strip():
        raise ValueError("kind es obligatorio.")
    kind_text = str(kind).strip()
    if len(kind_text) > 64 or any(ord(char) < 0x20 for char in kind_text):
        raise ValueError("kind supera el límite o contiene controles.")
    if task_id is not None and (
        not isinstance(task_id, (str, int))
        or isinstance(task_id, bool)
        or not str(task_id).strip()
        or len(str(task_id)) > 128
    ):
        raise ValueError("task_id debe ser texto o entero acotado.")

    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise ValueError("metadata debe ser un objeto.")
    metadata_json = json.dumps(metadata, ensure_ascii=False, allow_nan=False)
    if len(metadata_json.encode("utf-8")) > MAX_METADATA_BYTES:
        raise ValueError("metadata supera el límite de 64 KiB.")

    original = content.encode("utf-8")
    if len(original) > MAX_BLOCK_BYTES:
        raise ValueError("El bloque supera el límite de 2 MiB.")
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
            session_text,
            str(task_id) if task_id is not None else None,
            kind_text,
            sqlite3.Binary(compressed),
            hashlib.sha256(original).hexdigest(),
            len(original),
            len(compressed),
            metadata_json,
            utc_now(),
        ))

    return {
        "id": block_id,
        "session_id": session_text,
        "task_id": task_id,
        "kind": kind_text,
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

    if (
        not isinstance(row["original_bytes"], int)
        or not 0 <= row["original_bytes"] <= MAX_BLOCK_BYTES
        or not isinstance(row["compressed_bytes"], int)
        or row["compressed_bytes"] < 0
        or not isinstance(row["compressed_data"], bytes)
        or len(row["compressed_data"]) != row["compressed_bytes"]
    ):
        raise ValueError("Los tamaños declarados del bloque no son válidos.")

    try:
        decompressor = zlib.decompressobj()
        original = decompressor.decompress(
            row["compressed_data"], MAX_BLOCK_BYTES + 1
        )
    except zlib.error as error:
        raise ValueError("El bloque comprimido está dañado.") from error
    if (
        len(original) > MAX_BLOCK_BYTES
        or decompressor.unconsumed_tail
        or decompressor.unused_data
        or not decompressor.eof
    ):
        raise ValueError("El bloque comprimido excede los límites o está incompleto.")

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
        "metadata": _strict_metadata_json(row["metadata_json"]),
        "created_at": row["created_at"],
    }


def list_blocks(session_id, task_id=None, kind=None, limit=20):
    """Consulta el índice sin descomprimir el contenido de los bloques."""
    if not isinstance(session_id, str) or not session_id.strip() or len(session_id) > 128:
        raise ValueError("session_id debe ser texto no vacío de hasta 128 caracteres.")
    if task_id is not None and (
        not isinstance(task_id, (str, int)) or isinstance(task_id, bool)
        or not str(task_id).strip() or len(str(task_id)) > 128
    ):
        raise ValueError("task_id inválido.")
    if kind is not None and (
        not isinstance(kind, str) or not kind.strip() or len(kind) > 64
    ):
        raise ValueError("kind inválido.")
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("limit debe ser un entero entre 1 y 100.")

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
