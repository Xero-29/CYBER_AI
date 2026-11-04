#!/usr/bin/env python3
"""Grafo de evidencia, contexto selectivo y checkpoints de CYBER_AI."""

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
DB_PATH = PROJECT / "data" / "evidence_graph.sqlite3"


def utc_now():
    """Fecha actual en UTC."""
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def database():
    """Abre SQLite y cierra la conexión al terminar cada operación."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DB_PATH), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
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
    """Crea las tablas e índices si todavía no existen."""
    with database() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_updated
            ON sessions(updated_at);

            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                task_id TEXT,
                session_id TEXT REFERENCES sessions(id),
                kind TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                source_url TEXT,
                source_quote TEXT,
                confidence REAL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_nodes_task
            ON nodes(task_id, created_at);

            CREATE INDEX IF NOT EXISTS idx_nodes_kind_status
            ON nodes(kind, status);

            CREATE TABLE IF NOT EXISTS edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
                relation TEXT NOT NULL,
                target_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                UNIQUE(source_id, relation, target_id)
            );

            CREATE INDEX IF NOT EXISTS idx_edges_source
            ON edges(source_id, relation);

            CREATE INDEX IF NOT EXISTS idx_edges_target
            ON edges(target_id, relation);

            CREATE TABLE IF NOT EXISTS checkpoints (
                task_id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id),
                original_task TEXT,
                mode TEXT NOT NULL DEFAULT 'standard',
                agent TEXT NOT NULL,
                status TEXT NOT NULL,
                current_step TEXT,
                last_completed_step TEXT,
                next_action TEXT,
                partial_output TEXT,
                focus_node_ids_json TEXT NOT NULL DEFAULT '[]',
                updated_at TEXT NOT NULL
            );
        """)

        # Migración de bases anteriores: no elimina ni reescribe los datos.
        for table in ("nodes", "checkpoints"):
            columns = {
                row["name"]
                for row in db.execute(f"PRAGMA table_info({table})")
            }
            if "session_id" not in columns:
                db.execute(
                    f"ALTER TABLE {table} "
                    "ADD COLUMN session_id TEXT REFERENCES sessions(id)"
                )

        # Migración compatible: añadir la instrucción original a bases existentes.
        checkpoint_columns = {
            row["name"]
            for row in db.execute("PRAGMA table_info(checkpoints)")
        }
        if "original_task" not in checkpoint_columns:
            db.execute(
                "ALTER TABLE checkpoints ADD COLUMN original_task TEXT"
            )

        if "mode" not in checkpoint_columns:
            db.execute(
                "ALTER TABLE checkpoints ADD COLUMN "
                "mode TEXT NOT NULL DEFAULT 'standard'"
            )

        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_nodes_session_task
            ON nodes(session_id, task_id, created_at)
        """)
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_checkpoints_session_task
            ON checkpoints(session_id, task_id)
        """)


def create_session(name="Nueva sesión"):
    """Crea una sesión aislada y devuelve su identificador."""
    initialize()

    name = str(name).strip()
    if not name:
        raise ValueError("El nombre de la sesión no puede estar vacío.")

    session_id = uuid.uuid4().hex
    now = utc_now()

    with database() as db:
        db.execute("""
            INSERT INTO sessions (id, name, status, created_at, updated_at)
            VALUES (?, ?, 'active', ?, ?)
        """, (session_id, name, now, now))

    return session_id


def get_session(session_id):
    """Recupera los metadatos de una sesión concreta."""
    initialize()

    with database() as db:
        row = db.execute(
            "SELECT * FROM sessions WHERE id = ?",
            (session_id,),
        ).fetchone()

    return dict(row) if row else None


def list_sessions(limit=20):
    """Lista sesiones recientes sin cargar sus tareas ni sus evidencias."""
    initialize()
    limit = max(1, min(int(limit), 100))

    with database() as db:
        rows = db.execute("""
            SELECT id, name, status, created_at, updated_at
            FROM sessions
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [dict(row) for row in rows]


def add_node(
    *,
    kind,
    content,
    task_id=None,
    session_id=None,
    status="pending",
    source_url=None,
    source_quote=None,
    confidence=None,
    metadata=None,
    node_id=None,
):
    """Añade una fila de información y devuelve su identificador."""
    initialize()

    kind = str(kind).strip()
    content = str(content).strip()
    status = str(status).strip()

    if not kind or not content or not status:
        raise ValueError("kind, content y status son obligatorios.")

    if confidence is not None and not 0 <= float(confidence) <= 1:
        raise ValueError("confidence debe estar entre 0 y 1.")

    if session_id:
        with database() as db:
            exists = db.execute(
                "SELECT 1 FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
        if not exists:
            raise ValueError("La sesión indicada no existe.")

    identifier = node_id or str(uuid.uuid4())
    created_at = utc_now()
    metadata_json = json.dumps(
        metadata or {}, ensure_ascii=False
    )

    with database() as db:
        db.execute("""
            INSERT INTO nodes (
                id, task_id, session_id, kind, content, status, source_url,
                source_quote, confidence, metadata_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            identifier, task_id, session_id, kind, content, status,
            source_url, source_quote, confidence, metadata_json, created_at
        ))

    return identifier


def add_edge(source_id, relation, target_id, metadata=None):
    """Crea una relación entre dos nodos existentes."""
    initialize()

    relation = str(relation).strip()
    if not source_id or not target_id or not relation:
        raise ValueError("La relación requiere origen, destino y nombre.")

    with database() as db:
        source = db.execute(
            "SELECT session_id FROM nodes WHERE id = ?", (source_id,)
        ).fetchone()
        target = db.execute(
            "SELECT session_id FROM nodes WHERE id = ?", (target_id,)
        ).fetchone()

        if not source or not target:
            raise ValueError("Ambos nodos deben existir.")
        if source["session_id"] != target["session_id"]:
            raise ValueError("No se pueden relacionar nodos de sesiones diferentes.")

        db.execute("""
            INSERT INTO edges (
                source_id, relation, target_id, metadata_json, created_at
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(source_id, relation, target_id) DO NOTHING
        """, (
            source_id,
            relation,
            target_id,
            json.dumps(metadata or {}, ensure_ascii=False),
            utc_now(),
        ))

        row = db.execute("""
            SELECT id FROM edges
            WHERE source_id = ? AND relation = ? AND target_id = ?
        """, (source_id, relation, target_id)).fetchone()

    return row["id"]


def get_node(node_id):
    """Recupera una fila concreta, no la tabla completa."""
    initialize()

    with database() as db:
        row = db.execute(
            "SELECT * FROM nodes WHERE id = ?",
            (node_id,)
        ).fetchone()

    return dict(row) if row else None


def save_checkpoint(
    *,
    task_id,
    agent,
    status,
    session_id=None,
    original_task=None,
    mode=None,
    current_step=None,
    last_completed_step=None,
    next_action=None,
    partial_output=None,
    focus_node_ids=None,
):
    """Guarda el punto de continuidad de una tarea."""
    initialize()

    if not task_id or not agent or not status:
        raise ValueError("task_id, agent y status son obligatorios.")
    if mode is not None and mode not in {"standard", "technical"}:
        raise ValueError("mode debe ser standard o technical.")

    focus_ids = list(dict.fromkeys(focus_node_ids or []))

    with database() as db:
        if session_id:
            exists = db.execute(
                "SELECT 1 FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
            if not exists:
                raise ValueError("La sesión indicada no existe.")

        existing = db.execute(
            "SELECT session_id FROM checkpoints WHERE task_id = ?",
            (task_id,),
        ).fetchone()
        if existing and existing["session_id"] != session_id:
            raise ValueError(
                "Ese task_id ya pertenece a otra sesión o a datos antiguos. "
                "Usa un task_id nuevo."
            )

        db.execute("""
            INSERT INTO checkpoints (
                task_id, session_id, original_task, mode, agent, status,
                current_step, last_completed_step, next_action,
                partial_output, focus_node_ids_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
                session_id = excluded.session_id,
                original_task = COALESCE(
                    checkpoints.original_task, excluded.original_task
                ),
                mode = CASE WHEN ? IS NULL THEN checkpoints.mode
                            ELSE excluded.mode END,
                agent = excluded.agent,
                status = excluded.status,
                current_step = excluded.current_step,
                last_completed_step = excluded.last_completed_step,
                next_action = excluded.next_action,
                partial_output = excluded.partial_output,
                focus_node_ids_json = excluded.focus_node_ids_json,
                updated_at = excluded.updated_at
        """, (
            task_id, session_id, original_task, mode or 'standard',
            agent, status, current_step, last_completed_step,
            next_action, partial_output,
            json.dumps(focus_ids, ensure_ascii=False),
            utc_now(), mode,
        ))


def get_checkpoint(task_id, session_id=None):
    """Recupera el estado de continuidad de una tarea concreta."""
    initialize()

    with database() as db:
        if session_id is None:
            row = db.execute(
                "SELECT * FROM checkpoints WHERE task_id = ?",
                (task_id,),
            ).fetchone()
        else:
            row = db.execute(
                "SELECT * FROM checkpoints "
                "WHERE task_id = ? AND session_id = ?",
                (task_id, session_id),
            ).fetchone()

    if not row:
        return None

    result = dict(row)
    result["focus_node_ids"] = json.loads(
        result.pop("focus_node_ids_json")
    )
    return result


def build_context(
    *,
    task_id=None,
    session_id=None,
    focus_node_ids=None,
    max_nodes=12,
    max_chars=3000,
    include_related=True,
):
    """Construye contexto compacto a partir de un subgrafo específico.

    Primero consulta IDs explícitos y/o nodos de una tarea. Después,
    opcionalmente, recupera relaciones de esos nodos y algunos vecinos.
    Nunca lee toda la base como un único bloque de contexto.
    """
    initialize()

    if session_id:
        with database() as db:
            exists = db.execute(
                "SELECT 1 FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
        if not exists:
            raise ValueError("La sesión indicada no existe.")

    max_nodes = max(1, min(int(max_nodes), 50))
    max_chars = max(300, min(int(max_chars), 12000))
    focus_ids = list(dict.fromkeys(focus_node_ids or []))[:max_nodes]

    if not task_id and not focus_ids and not session_id:
        raise ValueError(
            "Indica task_id o focus_node_ids para limitar la consulta."
        )

    selected = []
    selected_ids = set()

    def include_row(row):
        if row and row["id"] not in selected_ids and len(selected) < max_nodes:
            selected.append(dict(row))
            selected_ids.add(row["id"])

    with database() as db:
        # 1. Recuperar solo los nodos solicitados explícitamente.
        if focus_ids:
            placeholders = ",".join("?" for _ in focus_ids)
            if session_id:
                rows = db.execute(
                    f"SELECT * FROM nodes WHERE id IN ({placeholders}) "
                    "AND session_id = ?",
                    (*focus_ids, session_id),
                ).fetchall()
            else:
                rows = db.execute(
                    f"SELECT * FROM nodes WHERE id IN ({placeholders})",
                    focus_ids,
                ).fetchall()
            rows_by_id = {row["id"]: row for row in rows}
            for identifier in focus_ids:
                include_row(rows_by_id.get(identifier))

        # 2. Si queda espacio, recuperar filas de la tarea actual.
        if task_id and len(selected) < max_nodes:
            if session_id:
                rows = db.execute("""
                    SELECT * FROM nodes
                    WHERE task_id = ? AND session_id = ?
                    ORDER BY created_at DESC LIMIT ?
                """, (task_id, session_id, max_nodes)).fetchall()
            else:
                rows = db.execute("""
                    SELECT * FROM nodes
                    WHERE task_id = ?
                    ORDER BY created_at DESC LIMIT ?
                """, (task_id, max_nodes)).fetchall()

            # Mostrar primero las filas de la tarea más reciente.
            for row in rows:
                include_row(row)

        # Si solo se indicó la sesión, añade datos recientes de esa sesión.
        if session_id and len(selected) < max_nodes:
            rows = db.execute("""
                SELECT * FROM nodes WHERE session_id = ?
                ORDER BY created_at DESC LIMIT ?
            """, (session_id, max_nodes)).fetchall()
            for row in rows:
                include_row(row)

        # 3. Recuperar relaciones del conjunto actual y sus vecinos.
        edges = []
        if include_related and selected_ids:
            ids = list(selected_ids)
            placeholders = ",".join("?" for _ in ids)
            if session_id:
                edges = db.execute(f"""
                    SELECT e.* FROM edges AS e
                    JOIN nodes AS src ON src.id = e.source_id
                    JOIN nodes AS dst ON dst.id = e.target_id
                    WHERE (e.source_id IN ({placeholders})
                       OR e.target_id IN ({placeholders}))
                      AND src.session_id = ? AND dst.session_id = ?
                    ORDER BY e.id DESC LIMIT ?
                """, (
                    *ids, *ids, session_id, session_id, max_nodes * 3
                )).fetchall()
            else:
                edges = db.execute(f"""
                    SELECT * FROM edges
                    WHERE source_id IN ({placeholders})
                       OR target_id IN ({placeholders})
                    ORDER BY id DESC LIMIT ?
                """, (*ids, *ids, max_nodes * 3)).fetchall()

            neighbor_ids = []
            for edge in edges:
                if edge["source_id"] not in selected_ids:
                    neighbor_ids.append(edge["source_id"])
                if edge["target_id"] not in selected_ids:
                    neighbor_ids.append(edge["target_id"])

            neighbor_ids = list(dict.fromkeys(neighbor_ids))
            slots = max_nodes - len(selected)

            if slots and neighbor_ids:
                neighbor_ids = neighbor_ids[:slots]
                placeholders = ",".join("?" for _ in neighbor_ids)
                if session_id:
                    rows = db.execute(
                        f"SELECT * FROM nodes WHERE id IN ({placeholders}) "
                        "AND session_id = ?",
                        (*neighbor_ids, session_id),
                    ).fetchall()
                else:
                    rows = db.execute(
                        f"SELECT * FROM nodes WHERE id IN ({placeholders})",
                        neighbor_ids,
                    ).fetchall()
                rows_by_id = {row["id"]: row for row in rows}

                for identifier in neighbor_ids:
                    include_row(rows_by_id.get(identifier))

    if not selected:
        return ""

    lines = [
        "CONTEXTO RECUPERADO DEL GRAFO",
        "Los datos son referencias; comprueba su estado y evidencia.",
    ]

    for node in selected:
        lines.append(
            f"[{node['id']}] tipo={node['kind']} "
            f"estado={node['status']}: {node['content']}"
        )

        if node.get("source_url"):
            lines.append(f"  Fuente: {node['source_url']}")
        if node.get("source_quote"):
            lines.append(f"  Evidencia: {node['source_quote']}")

    for edge in edges:
        lines.append(
            f"RELACION: {edge['source_id']} "
            f"--{edge['relation']}--> {edge['target_id']}"
        )

    result = "\n".join(lines)
    if len(result) > max_chars:
        result = result[:max_chars].rstrip()
        result += "\n[Contexto recortado; consulta el grafo si necesitas más.]"

    return result


def counts():
    """Devuelve cantidades de filas sin cargar sus contenidos."""
    initialize()

    with database() as db:
        return {
            "nodes": db.execute("SELECT COUNT(*) FROM nodes").fetchone()[0],
            "edges": db.execute("SELECT COUNT(*) FROM edges").fetchone()[0],
            "checkpoints": db.execute(
                "SELECT COUNT(*) FROM checkpoints"
            ).fetchone()[0],
        }


if __name__ == "__main__":
    initialize()
    print("Grafo de evidencia de CYBER_AI")
    print("Base de datos:", DB_PATH)
    for table, amount in counts().items():
        print(f"{table}: {amount}")
