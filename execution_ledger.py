"""Transactional append-only execution evidence ledger for CYBER_AI."""
import hashlib
import json
import math
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
DEFAULT_DB = PROJECT / "data" / "execution_ledger.sqlite3"
GENESIS = "0" * 64
MAX_FIELD = 16384
SECRET_KEY = re.compile(r"(?:api[_-]?key|authorization|password|secret|token|credential)", re.I)
SECRET_ASSIGNMENT = re.compile(
    r"""(?i)\b(api[_-]?key|access[_-]?token|refresh[_-]?token|password|passwd|secret|client[_-]?secret)\b\s*([:=])\s*("[^"]*"|'[^']*'|[^\s,;]+)"""
)
BEARER_TOKEN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
PRIVATE_KEY = re.compile(
    r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.S
)
URL_CREDENTIALS = re.compile(r"(?i)(https?://)[^/@\s:]+:[^/@\s]+@")


def _redact_text(value):
    value = PRIVATE_KEY.sub("[REDACTED PRIVATE KEY]", str(value))
    value = BEARER_TOKEN.sub("Bearer [REDACTED]", value)
    value = SECRET_ASSIGNMENT.sub(r"\1\2[REDACTED]", value)
    return URL_CREDENTIALS.sub(r"\1[REDACTED]@", value)



class LedgerError(ValueError):
    pass


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _clean(value, key=""):
    if SECRET_KEY.search(key):
        return "[REDACTED]"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return _redact_text(value[:MAX_FIELD])
    if isinstance(value, list):
        return [_clean(item) for item in value[:500]]
    if isinstance(value, dict):
        return {str(k)[:128]: _clean(v, str(k)) for k, v in list(value.items())[:500]}
    return str(value)[:MAX_FIELD]


def _digest(previous, payload):
    return hashlib.sha256((previous + "\n" + payload).encode("utf-8")).hexdigest()


class ExecutionLedger:
    """SQLite hash chain. Tamper-evident, not tamper-proof."""

    def __init__(self, path=None):
        configured_path = path if path is not None else os.environ.get("CYBER_AI_LEDGER_PATH", DEFAULT_DB)
        self.path = Path(configured_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self, *, configure_wal=False):
        db = sqlite3.connect(str(self.path), timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=30000")
        # WAL mode is persistent for the database. Configure it during
        # initialization only; repeating this write-capable PRAGMA on every
        # reader/writer connection can contend with concurrent transactions.
        if configure_wal:
            db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def initialize(self):
        with self.connect(configure_wal=True) as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS execution_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL,
                    namespace TEXT NOT NULL, task_fingerprint TEXT NOT NULL,
                    task TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN
                        ('started','completed','failed','timeout','denied','cancelled','interrupted')),
                    tool TEXT NOT NULL, tool_version TEXT NOT NULL,
                    model TEXT NOT NULL, environment TEXT NOT NULL,
                    duration_ms INTEGER NOT NULL CHECK(duration_ms >= 0),
                    cost_microunits INTEGER CHECK(cost_microunits IS NULL OR cost_microunits >= 0),
                    evidence_sha256 TEXT NOT NULL, validator_results TEXT NOT NULL,
                    metadata TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_execution_task
                    ON execution_events(namespace, task_fingerprint, created_at);
                CREATE TRIGGER IF NOT EXISTS execution_events_no_update
                    BEFORE UPDATE ON execution_events BEGIN
                    SELECT RAISE(ABORT, 'execution ledger is append-only');
                END;
                CREATE TRIGGER IF NOT EXISTS execution_events_no_delete
                    BEFORE DELETE ON execution_events BEGIN
                    SELECT RAISE(ABORT, 'execution ledger is append-only');
                END;
            """)
        with self.connect() as db:
            schema = db.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='execution_events'"
            ).fetchone()
            if schema and "'interrupted'" not in schema["sql"]:
                db.executescript("""
                    BEGIN IMMEDIATE;
                    DROP TRIGGER IF EXISTS execution_events_no_update;
                    DROP TRIGGER IF EXISTS execution_events_no_delete;
                    DROP INDEX IF EXISTS idx_execution_task;
                    ALTER TABLE execution_events RENAME TO execution_events_legacy;
                    CREATE TABLE execution_events (
                        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_id TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL,
                        namespace TEXT NOT NULL, task_fingerprint TEXT NOT NULL,
                        task TEXT NOT NULL,
                        status TEXT NOT NULL CHECK(status IN
                            ('started','completed','failed','timeout','denied','cancelled','interrupted')),
                        tool TEXT NOT NULL, tool_version TEXT NOT NULL,
                        model TEXT NOT NULL, environment TEXT NOT NULL,
                        duration_ms INTEGER NOT NULL CHECK(duration_ms >= 0),
                        cost_microunits INTEGER CHECK(cost_microunits IS NULL OR cost_microunits >= 0),
                        evidence_sha256 TEXT NOT NULL, validator_results TEXT NOT NULL,
                        metadata TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL
                    );
                    INSERT INTO execution_events SELECT * FROM execution_events_legacy;
                    DROP TABLE execution_events_legacy;
                    CREATE INDEX idx_execution_task
                        ON execution_events(namespace, task_fingerprint, created_at);
                    CREATE TRIGGER execution_events_no_update BEFORE UPDATE ON execution_events
                        BEGIN SELECT RAISE(ABORT, 'execution ledger is append-only'); END;
                    CREATE TRIGGER execution_events_no_delete BEFORE DELETE ON execution_events
                        BEGIN SELECT RAISE(ABORT, 'execution ledger is append-only'); END;
                    COMMIT;
                """)

    def append(self, *, namespace, task, status, tool, evidence, duration_ms,
               tool_version="unknown", model="none", environment="unknown",
               cost_microunits=None, validator_results=None, metadata=None,
               event_id=None):
        for name, value in (("namespace", namespace), ("task", task), ("tool", tool)):
            if not isinstance(value, str) or not value.strip():
                raise LedgerError(f"{name} es obligatorio.")
        if status not in {"started", "completed", "failed", "timeout", "denied", "cancelled", "interrupted"}:
            raise LedgerError("Estado de ejecución no permitido.")
        if isinstance(duration_ms, bool) or not isinstance(duration_ms, int) or duration_ms < 0:
            raise LedgerError("duration_ms debe ser un entero no negativo.")
        if cost_microunits is not None and (
            isinstance(cost_microunits, bool) or not isinstance(cost_microunits, int)
            or cost_microunits < 0
        ):
            raise LedgerError("cost_microunits debe ser un entero no negativo.")
        evidence_hash = hashlib.sha256(_canonical(_clean(evidence)).encode()).hexdigest()
        validators = _clean(validator_results or [])
        safe_metadata = _clean(metadata or {})
        task = _redact_text(task.strip()[:MAX_FIELD])
        fingerprint = hashlib.sha256(task.casefold().encode()).hexdigest()
        event_id = event_id or uuid.uuid4().hex
        created_at = datetime.now(timezone.utc).isoformat()
        db = self.connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute(
                "SELECT event_hash FROM execution_events ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            previous_hash = previous["event_hash"] if previous else GENESIS
            payload = {
                "event_id": event_id, "created_at": created_at,
                "namespace": namespace.strip(), "task_fingerprint": fingerprint,
                "task": task, "status": status, "tool": tool.strip(),
                "tool_version": _redact_text(str(tool_version)[:256]), "model": _redact_text(str(model)[:256]),
                "environment": _redact_text(str(environment)[:512]), "duration_ms": duration_ms,
                "cost_microunits": cost_microunits, "evidence_sha256": evidence_hash,
                "validator_results": validators, "metadata": safe_metadata,
                "previous_hash": previous_hash,
            }
            event_hash = _digest(previous_hash, _canonical(payload))
            db.execute("""
                INSERT INTO execution_events (
                    event_id,created_at,namespace,task_fingerprint,task,status,tool,
                    tool_version,model,environment,duration_ms,cost_microunits,
                    evidence_sha256,validator_results,metadata,previous_hash,event_hash
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (event_id, created_at, namespace.strip(), fingerprint, task, status,
                  tool.strip(), payload["tool_version"], payload["model"],
                  payload["environment"], duration_ms, cost_microunits, evidence_hash,
                  _canonical(validators), _canonical(safe_metadata), previous_hash, event_hash))
            sequence = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.commit()
            return {"sequence": sequence, "event_id": event_id, "status": status,
                    "evidence_sha256": evidence_hash, "previous_hash": previous_hash,
                    "event_hash": event_hash}
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def reconcile_interrupted(self, *, namespace=None, stale_after_seconds=300):
        """Atomically close stale orphaned starts; call only after stopping workers."""
        if (isinstance(stale_after_seconds, bool)
                or not isinstance(stale_after_seconds, (int, float))
                or not math.isfinite(stale_after_seconds) or stale_after_seconds < 0):
            raise LedgerError("stale_after_seconds debe ser finito y no negativo.")
        cutoff = datetime.now(timezone.utc).timestamp() - stale_after_seconds
        db = self.connect()
        reconciled = []
        try:
            db.execute("BEGIN IMMEDIATE")
            chain_rows = db.execute(
                "SELECT * FROM execution_events ORDER BY sequence"
            ).fetchall()
            previous_hash = GENESIS
            fields = ("event_id", "created_at", "namespace", "task_fingerprint", "task",
                      "status", "tool", "tool_version", "model", "environment",
                      "duration_ms", "cost_microunits", "evidence_sha256", "previous_hash")
            for expected, row in enumerate(chain_rows, 1):
                item = dict(row)
                if item["sequence"] != expected or item["previous_hash"] != previous_hash:
                    raise LedgerError("No se reconcilia un ledger con una cadena rota.")
                try:
                    payload = {key: item[key] for key in fields}
                    payload["validator_results"] = json.loads(item["validator_results"])
                    payload["metadata"] = json.loads(item["metadata"])
                    calculated = _digest(previous_hash, _canonical(payload))
                except (KeyError, TypeError, ValueError) as error:
                    raise LedgerError("No se puede verificar el ledger antes de reconciliar.") from error
                if calculated != item["event_hash"]:
                    raise LedgerError("No se reconcilia un ledger con un hash inválido.")
                previous_hash = item["event_hash"]

            query = "SELECT * FROM execution_events WHERE status='started'"
            params = ()
            if namespace is not None:
                query += " AND namespace=?"
                params = (namespace,)
            query += " ORDER BY sequence"
            starts = db.execute(query, params).fetchall()
            rows = db.execute(
                "SELECT metadata FROM execution_events WHERE status!='started'"
            ).fetchall()
            closed = set()
            for row in rows:
                try:
                    start_id = json.loads(row["metadata"]).get("start_event_id")
                except (TypeError, ValueError, AttributeError):
                    start_id = None
                if start_id:
                    closed.add(start_id)

            for start in starts:
                if start["event_id"] in closed:
                    continue
                try:
                    started_at = datetime.fromisoformat(start["created_at"]).timestamp()
                except (TypeError, ValueError, OverflowError) as error:
                    raise LedgerError("Fecha de inicio inválida; no se reconcilia.") from error
                if started_at > cutoff:
                    continue
                event_id = "interrupted-" + start["event_id"]
                created_at = datetime.now(timezone.utc).isoformat()
                metadata = {
                    "start_event_id": start["event_id"],
                    "recovered_by": "execution_ledger.reconcile_interrupted",
                    "original_started_at": start["created_at"],
                }
                evidence_hash = hashlib.sha256(_canonical({
                    "phase": "lifecycle_reconciliation",
                    "outcome": "unknown",
                    "reason": "start_event_has_no_terminal_record",
                }).encode("utf-8")).hexdigest()
                previous = db.execute(
                    "SELECT event_hash FROM execution_events ORDER BY sequence DESC LIMIT 1"
                ).fetchone()
                previous_hash = previous["event_hash"] if previous else GENESIS
                payload = {
                    "event_id": event_id, "created_at": created_at,
                    "namespace": start["namespace"],
                    "task_fingerprint": start["task_fingerprint"],
                    "task": start["task"], "status": "interrupted",
                    "tool": start["tool"], "tool_version": start["tool_version"],
                    "model": start["model"], "environment": start["environment"],
                    "duration_ms": 0, "cost_microunits": None,
                    "evidence_sha256": evidence_hash, "validator_results": [],
                    "metadata": metadata, "previous_hash": previous_hash,
                }
                event_hash = _digest(previous_hash, _canonical(payload))
                db.execute("""
                    INSERT INTO execution_events (
                        event_id,created_at,namespace,task_fingerprint,task,status,tool,
                        tool_version,model,environment,duration_ms,cost_microunits,
                        evidence_sha256,validator_results,metadata,previous_hash,event_hash
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    event_id, created_at, start["namespace"], start["task_fingerprint"],
                    start["task"], "interrupted", start["tool"], start["tool_version"],
                    start["model"], start["environment"], 0, None, evidence_hash,
                    "[]", _canonical(metadata), previous_hash, event_hash,
                ))
                sequence = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                reconciled.append({
                    "sequence": sequence, "event_id": event_id,
                    "status": "interrupted", "previous_hash": previous_hash,
                    "event_hash": event_hash,
                })
                closed.add(start["event_id"])
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
        return {"reconciled": len(reconciled), "events": reconciled}

    def verify(self):
        with self.connect() as db:
            rows = db.execute("SELECT * FROM execution_events ORDER BY sequence").fetchall()
        previous = GENESIS
        fields = ("event_id", "created_at", "namespace", "task_fingerprint", "task",
                  "status", "tool", "tool_version", "model", "environment",
                  "duration_ms", "cost_microunits", "evidence_sha256", "previous_hash")
        for expected, row in enumerate(rows, 1):
            item = dict(row)
            if item["sequence"] != expected or item["previous_hash"] != previous:
                return {"valid": False, "checked": expected - 1,
                        "failed_sequence": expected, "reason": "chain_link"}
            payload = {key: item[key] for key in fields}
            payload["validator_results"] = json.loads(item["validator_results"])
            payload["metadata"] = json.loads(item["metadata"])
            calculated = _digest(previous, _canonical(payload))
            if calculated != item["event_hash"]:
                return {"valid": False, "checked": expected - 1,
                        "failed_sequence": expected, "reason": "event_hash"}
            previous = item["event_hash"]
        return {"valid": True, "checked": len(rows), "head_hash": previous}

    def namespaces(self):
        """Lista namespaces que ya tienen eventos."""
        with self.connect() as db:
            rows = db.execute(
                "SELECT DISTINCT namespace FROM execution_events ORDER BY namespace"
            ).fetchall()
        return [row["namespace"] for row in rows]

    def history(self, *, namespace, limit=100):
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 1000:
            raise LedgerError("limit debe estar entre 1 y 1000.")
        with self.connect() as db:
            rows = db.execute(
                "SELECT sequence,event_id,created_at,task,task_fingerprint,status,tool,tool_version,model,"
                "environment,duration_ms,cost_microunits,evidence_sha256,validator_results,"
                "metadata,event_hash FROM execution_events WHERE namespace=? "
                "ORDER BY sequence DESC LIMIT ?", (namespace, limit)).fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["validator_results"] = json.loads(item["validator_results"])
            item["metadata"] = json.loads(item["metadata"])
            result.append(item)
        return result
