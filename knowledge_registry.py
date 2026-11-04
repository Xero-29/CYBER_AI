#!/usr/bin/env python3
"""Registro persistente de recursos y versiones de CYBER_AI."""

import hashlib
import sqlite3
import uuid

from datetime import datetime, timezone
from pathlib import Path

import knowledge_library as library


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def connect():
    library.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(library.DB_PATH), timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout = 10000")
    return db


def initialize():
    """Crea el registro sin alterar los fragmentos existentes."""
    library.initialize()

    with connect() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS knowledge_resources (
                resource_id TEXT PRIMARY KEY,
                source_path TEXT NOT NULL UNIQUE,
                canonical_uri TEXT,
                title TEXT,
                publisher TEXT,
                resource_type TEXT NOT NULL,
                area_id TEXT,
                domain_id TEXT,
                topic_id TEXT,
                subtopic_id TEXT,
                classification_status TEXT NOT NULL DEFAULT 'pending',
                current_sha256 TEXT,
                file_size INTEGER,
                processing_status TEXT NOT NULL DEFAULT 'discovered',
                validation_status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS knowledge_resource_versions (
                version_id TEXT PRIMARY KEY,
                resource_id TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                modified_at TEXT,
                detected_at TEXT NOT NULL,
                UNIQUE(resource_id, sha256),
                FOREIGN KEY(resource_id)
                    REFERENCES knowledge_resources(resource_id)
            );

            CREATE INDEX IF NOT EXISTS idx_resource_area
            ON knowledge_resources(area_id, domain_id, topic_id);

            CREATE INDEX IF NOT EXISTS idx_resource_status
            ON knowledge_resources(processing_status);

            CREATE INDEX IF NOT EXISTS idx_resource_hash
            ON knowledge_resources(current_sha256);

            CREATE TABLE IF NOT EXISTS knowledge_classification_history (
                history_id TEXT PRIMARY KEY,
                resource_id TEXT NOT NULL,
                previous_classification TEXT NOT NULL,
                new_classification TEXT NOT NULL,
                changed_at TEXT NOT NULL,
                reason TEXT,
                FOREIGN KEY(resource_id)
                    REFERENCES knowledge_resources(resource_id)
            );

            CREATE INDEX IF NOT EXISTS idx_classification_history_resource
            ON knowledge_classification_history(resource_id, changed_at);

            CREATE TABLE IF NOT EXISTS knowledge_processing_runs (
                run_id TEXT PRIMARY KEY,
                version_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                chunks_total INTEGER NOT NULL DEFAULT 0,
                chunks_done INTEGER NOT NULL DEFAULT 0,
                checkpoint INTEGER NOT NULL DEFAULT 0,
                error TEXT,
                started_at TEXT,
                updated_at TEXT NOT NULL,
                finished_at TEXT,
                FOREIGN KEY(version_id)
                    REFERENCES knowledge_resource_versions(version_id)
            );

            CREATE INDEX IF NOT EXISTS idx_processing_version
            ON knowledge_processing_runs(version_id, status);
        """)

        # Migración idempotente: agrega campos sin reconstruir tablas.
        version_columns = {
            "source_version": "TEXT",
            "published_at": "TEXT",
            "license": "TEXT",
            "license_url": "TEXT",
            "license_status": "TEXT NOT NULL DEFAULT 'pending'",
            "provenance_uri": "TEXT",
            "provenance_evidence": "TEXT",
            "validation_status": "TEXT NOT NULL DEFAULT 'pending'",
            "validated_at": "TEXT",
            "validation_notes": "TEXT",
        }

        db = connect()
        try:
            with db:
                existing_columns = {
                    row["name"]
                    for row in db.execute(
                        "PRAGMA table_info(knowledge_resource_versions)"
                    ).fetchall()
                }

                for column, definition in version_columns.items():
                    if column not in existing_columns:
                        db.execute(
                            f"ALTER TABLE knowledge_resource_versions "
                            f"ADD COLUMN {column} {definition}"
                        )
        finally:
            db.close()


def register_resource(
    source_path,
    *,
    sha256,
    file_size,
    resource_type,
    title=None,
    publisher=None,
    canonical_uri=None,
    modified_at=None,
):
    """Registra un archivo y detecta si es nuevo, conocido o modificado."""
    path = Path(source_path).expanduser().resolve()

    if not isinstance(sha256, str) or len(sha256) != 64:
        raise ValueError("SHA-256 inválido.")

    try:
        int(sha256, 16)
    except ValueError as error:
        raise ValueError("SHA-256 inválido.") from error

    if not isinstance(file_size, int) or file_size < 0:
        raise ValueError("file_size debe ser un entero no negativo.")

    if not isinstance(resource_type, str) or not resource_type.strip():
        raise ValueError("resource_type es obligatorio.")

    initialize()
    now = utc_now()

    with connect() as db:
        row = db.execute(
            "SELECT * FROM knowledge_resources WHERE source_path = ?",
            (str(path),),
        ).fetchone()

        if row is None:
            resource_id = uuid.uuid4().hex
            db.execute("""
                INSERT INTO knowledge_resources (
                    resource_id, source_path, canonical_uri, title,
                    publisher, resource_type, current_sha256, file_size,
                    created_at, updated_at, last_seen_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                resource_id, str(path), canonical_uri, title, publisher,
                resource_type.strip(), sha256, file_size, now, now, now,
            ))
            status = "new"
        else:
            resource_id = row["resource_id"]
            status = (
                "unchanged"
                if row["current_sha256"] == sha256
                else "modified"
            )
            db.execute("""
                UPDATE knowledge_resources
                SET canonical_uri = COALESCE(?, canonical_uri),
                    title = COALESCE(?, title),
                    publisher = COALESCE(?, publisher),
                    resource_type = ?,
                    current_sha256 = ?,
                    file_size = ?,
                    updated_at = ?,
                    last_seen_at = ?
                WHERE resource_id = ?
            """, (
                canonical_uri, title, publisher, resource_type.strip(),
                sha256, file_size, now, now, resource_id,
            ))

        version = db.execute("""
            SELECT version_id FROM knowledge_resource_versions
            WHERE resource_id = ? AND sha256 = ?
        """, (resource_id, sha256)).fetchone()

        if version is None:
            version_id = uuid.uuid4().hex
            db.execute("""
                INSERT INTO knowledge_resource_versions (
                    version_id, resource_id, sha256, file_size,
                    modified_at, detected_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                version_id, resource_id, sha256, file_size,
                modified_at, now,
            ))
            version_created = True
        else:
            version_id = version["version_id"]
            version_created = False

    return {
        "resource_id": resource_id,
        "version_id": version_id,
        "status": status,
        "version_created": version_created,
        "sha256": sha256,
    }



_PROVENANCE_UNSET = object()

LICENSE_STATUSES = {"verified", "pending", "restricted", "rejected"}
VALIDATION_STATUSES = {"verified", "pending", "rejected"}


def update_version_provenance(
    version_id,
    *,
    source_version=_PROVENANCE_UNSET,
    published_at=_PROVENANCE_UNSET,
    license=_PROVENANCE_UNSET,
    license_url=_PROVENANCE_UNSET,
    license_status=_PROVENANCE_UNSET,
    provenance_uri=_PROVENANCE_UNSET,
    provenance_evidence=_PROVENANCE_UNSET,
    validation_status=_PROVENANCE_UNSET,
    validation_notes=_PROVENANCE_UNSET,
):
    """Actualiza metadatos sin borrar campos omitidos."""

    if not isinstance(version_id, str) or not version_id.strip():
        raise ValueError("version_id es obligatorio.")

    if license_status is not _PROVENANCE_UNSET:
        if license_status not in LICENSE_STATUSES:
            raise ValueError("license_status no permitido.")

    if validation_status is not _PROVENANCE_UNSET:
        if validation_status not in VALIDATION_STATUSES:
            raise ValueError("validation_status no permitido.")

    fields = {
        "source_version": source_version,
        "published_at": published_at,
        "license": license,
        "license_url": license_url,
        "license_status": license_status,
        "provenance_uri": provenance_uri,
        "provenance_evidence": provenance_evidence,
        "validation_status": validation_status,
        "validation_notes": validation_notes,
    }

    changes = {
        key: value for key, value in fields.items()
        if value is not _PROVENANCE_UNSET
    }

    if validation_status is not _PROVENANCE_UNSET:
        changes["validated_at"] = (
            utc_now() if validation_status == "verified" else None
        )

    if not changes:
        raise ValueError("No se proporcionaron campos para actualizar.")

    assignments = ", ".join(f"{key} = ?" for key in changes)
    values = list(changes.values()) + [version_id]

    db = connect()
    try:
        with db:
            cursor = db.execute(
                f"UPDATE knowledge_resource_versions "
                f"SET {assignments} WHERE version_id = ?",
                values,
            )
            if cursor.rowcount == 0:
                raise ValueError("La versión indicada no existe.")
    finally:
        db.close()

    return True


def resource_inventory():
    """Devuelve el inventario sin leer ni descomprimir los fragmentos."""
    initialize()

    with connect() as db:
        rows = db.execute("""
            SELECT r.*,
                   COUNT(v.version_id) AS versions
            FROM knowledge_resources AS r
            LEFT JOIN knowledge_resource_versions AS v
                ON v.resource_id = r.resource_id
            GROUP BY r.resource_id
            ORDER BY r.source_path
        """).fetchall()

    return [dict(row) for row in rows]

CLASSIFICATION_STATUSES = {
    "pending", "provisional", "verified", "rejected"
}


def update_resource_classification(
    resource_id,
    *,
    area_id,
    domain_id,
    topic_id,
    subtopic_id,
    classification_status="provisional",
    reason=None,
):
    """Actualiza la clasificación y conserva un historial de cambios."""
    if not isinstance(resource_id, str) or not resource_id.strip():
        raise ValueError("resource_id es obligatorio.")

    if classification_status not in CLASSIFICATION_STATUSES:
        raise ValueError("Estado de clasificación inválido.")

    fields = {
        "area_id": area_id,
        "domain_id": domain_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }

    for name, value in fields.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} debe ser un texto no vacío.")

    initialize()

    import json

    now = utc_now()

    with connect() as db:
        row = db.execute(
            "SELECT area_id, domain_id, topic_id, subtopic_id, "
            "classification_status FROM knowledge_resources "
            "WHERE resource_id = ?",
            (resource_id.strip(),),
        ).fetchone()

        if row is None:
            raise ValueError("El recurso indicado no existe.")

        previous = dict(row)
        new = {
            **fields,
            "classification_status": classification_status,
        }

        if previous == new:
            return False

        db.execute("""
            UPDATE knowledge_resources
            SET area_id = ?,
                domain_id = ?,
                topic_id = ?,
                subtopic_id = ?,
                classification_status = ?,
                updated_at = ?
            WHERE resource_id = ?
        """, (
            area_id.strip(),
            domain_id.strip(),
            topic_id.strip(),
            subtopic_id.strip(),
            classification_status,
            now,
            resource_id.strip(),
        ))

        db.execute("""
            INSERT INTO knowledge_classification_history (
                history_id, resource_id, previous_classification,
                new_classification, changed_at, reason
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            uuid.uuid4().hex,
            resource_id.strip(),
            json.dumps(previous, sort_keys=True),
            json.dumps(new, sort_keys=True),
            now,
            reason,
        ))

    return True

