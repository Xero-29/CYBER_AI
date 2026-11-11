#!/usr/bin/env python3
"""Reindexa los embeddings de la biblioteca sin mezclar espacios vectoriales.

El proceso prepara vectores en una tabla de staging y solo sustituye los
vectores activos cuando todos los fragmentos han sido procesados y validados.
Antes de aplicar cambios crea una copia SQLite de seguridad.
"""
import argparse
import hashlib
import json
import sqlite3
import uuid
import zlib
from datetime import datetime, timezone
from pathlib import Path

from knowledge_library import DB_PATH, database, initialize, validate_vector
from knowledge_embeddings import generate_embeddings
from model_memory_manager import load_config, resolve_agent
from llm_providers import resolve_provider, resolve_model


STAGING_TABLE = "knowledge_embedding_reindex_stage"


def target_embedding_space(agent_name="ECO"):
    config = load_config()
    name, agent = resolve_agent(agent_name, config)
    if agent.get("type") != "embeddings":
        raise ValueError(f"{name} no es un especialista de embeddings.")
    provider = resolve_provider(config, agent)
    model = resolve_model(provider, agent, name)
    space = model if provider["protocol"] == "ollama" else f"{provider['name']}::{model}"
    return {"agent": name, "provider": provider["name"], "model": model, "space": space}


def inventory(target_space):
    initialize()
    with database() as db:
        rows = db.execute(
            "SELECT embedding_model, COUNT(*) AS total "
            "FROM knowledge_chunks GROUP BY embedding_model ORDER BY embedding_model"
        ).fetchall()
        total = db.execute("SELECT COUNT(*) FROM knowledge_chunks").fetchone()[0]
    spaces = [{"embedding_space": row["embedding_model"], "chunks": row["total"]}
              for row in rows]
    pending = sum(item["chunks"] for item in spaces
                  if item["embedding_space"] != target_space)
    return {"total_chunks": total, "spaces": spaces,
            "target_embedding_space": target_space, "chunks_to_reindex": pending}


def create_backup():
    initialize()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    backup_dir = DB_PATH.parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"knowledge_library_pre_reindex_{stamp}_{uuid.uuid4().hex[:8]}.sqlite3"
    source = sqlite3.connect(str(DB_PATH), timeout=30)
    destination = sqlite3.connect(str(backup_path), timeout=30)
    try:
        source.backup(destination)
    finally:
        destination.close()
        source.close()
    return backup_path


def _verified_content(row):
    try:
        original = zlib.decompress(row["content_z"])
    except zlib.error as error:
        raise ValueError(f"Fragmento {row['id']} tiene contenido comprimido dañado.") from error
    if hashlib.sha256(original).hexdigest() != row["content_sha256"]:
        raise ValueError(f"El hash del fragmento {row['id']} no coincide.")
    if len(original) != row["original_bytes"]:
        raise ValueError(f"El tamaño del fragmento {row['id']} no coincide.")
    try:
        return original.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"El fragmento {row['id']} no contiene UTF-8 válido.") from error


def reindex_knowledge(*, agent_name="ECO", batch_size=8):
    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or not 1 <= batch_size <= 32:
        raise ValueError("batch_size debe estar entre 1 y 32.")

    target = target_embedding_space(agent_name)
    plan = inventory(target["space"])
    if plan["chunks_to_reindex"] == 0:
        return {"status": "already_current", "plan": plan, "backup": None}

    backup_path = create_backup()
    with database() as db:
        rows = db.execute(
            "SELECT id, content_z, content_sha256, original_bytes "
            "FROM knowledge_chunks WHERE embedding_model != ? ORDER BY id",
            (target["space"],),
        ).fetchall()
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {STAGING_TABLE} ("
            "chunk_id TEXT PRIMARY KEY, embedding_json TEXT NOT NULL, "
            "embedding_model TEXT NOT NULL, dimensions INTEGER NOT NULL)"
        )
        db.execute(f"DELETE FROM {STAGING_TABLE}")

    expected_dimensions = None
    processed = 0
    for start in range(0, len(rows), batch_size):
        batch_rows = rows[start:start + batch_size]
        texts = [_verified_content(row) for row in batch_rows]
        generated = generate_embeddings(texts, agent_name=agent_name)
        if generated.get("embedding_space") != target["space"]:
            raise RuntimeError("El proveedor o modelo ECO cambió durante la reindexación.")
        vectors = [validate_vector(vector) for vector in generated.get("embeddings", [])]
        if len(vectors) != len(batch_rows):
            raise RuntimeError("La cantidad de vectores no coincide con los fragmentos.")
        dimensions = len(vectors[0])
        if any(len(vector) != dimensions for vector in vectors):
            raise RuntimeError("El lote contiene vectores de dimensiones diferentes.")
        if expected_dimensions is None:
            expected_dimensions = dimensions
        elif dimensions != expected_dimensions:
            raise RuntimeError("El modelo produjo dimensiones inconsistentes entre lotes.")

        with database() as db:
            db.executemany(
                f"INSERT INTO {STAGING_TABLE} "
                "(chunk_id, embedding_json, embedding_model, dimensions) "
                "VALUES (?, ?, ?, ?)",
                [(row["id"], json.dumps(vector), target["space"], dimensions)
                 for row, vector in zip(batch_rows, vectors)],
            )
        processed += len(batch_rows)
        print(f"Preparados {processed}/{len(rows)} fragmentos.", flush=True)

    # Publicar todos los vectores en una sola transacción. Si algo falla,
    # SQLite revierte la sustitución y el backup previo sigue disponible.
    with database() as db:
        staged = db.execute(f"SELECT COUNT(*) FROM {STAGING_TABLE}").fetchone()[0]
        if staged != len(rows):
            raise RuntimeError("El staging está incompleto; no se publicaron los vectores.")
        db.execute(
            f"UPDATE knowledge_chunks SET "
            "embedding_json = (SELECT s.embedding_json FROM "
            f"{STAGING_TABLE} s WHERE s.chunk_id = knowledge_chunks.id), "
            "embedding_model = (SELECT s.embedding_model FROM "
            f"{STAGING_TABLE} s WHERE s.chunk_id = knowledge_chunks.id), "
            "embedding_dimensions = (SELECT s.dimensions FROM "
            f"{STAGING_TABLE} s WHERE s.chunk_id = knowledge_chunks.id) "
            f"WHERE id IN (SELECT chunk_id FROM {STAGING_TABLE})"
        )
        if db.execute("SELECT changes()").fetchone()[0] != len(rows):
            raise RuntimeError("No se actualizaron todos los fragmentos esperados.")
        db.execute(f"DELETE FROM {STAGING_TABLE}")

    return {
        "status": "completed",
        "plan": plan,
        "reindexed_chunks": processed,
        "embedding_space": target["space"],
        "dimensions": expected_dimensions,
        "backup": str(backup_path),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", default="ECO", help="Especialista de embeddings (por defecto ECO)")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--apply", action="store_true", help="Ejecuta la reindexación")
    parser.add_argument("--confirm", action="store_true", help="Confirma la sustitución de vectores existentes")
    args = parser.parse_args()

    if args.confirm and not args.apply:
        parser.error("--confirm solo puede utilizarse junto con --apply")
    if args.apply and not args.confirm:
        parser.error("La reindexación requiere --apply --confirm")

    target = target_embedding_space(args.agent)
    plan = inventory(target["space"])
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if not args.apply:
        print("\nModo de solo lectura. Para aplicar: python knowledge_reindex.py --apply --confirm")
        return

    result = reindex_knowledge(agent_name=args.agent, batch_size=args.batch_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
