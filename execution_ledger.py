"""Transactional append-only execution evidence ledger for CYBER_AI."""
import hashlib
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
DEFAULT_DB = PROJECT / "data" / "execution_ledger.sqlite3"
GENESIS = "0" * 64
SECRET_KEY = re.compile(r"(?:api[_-]?key|authorization|password|secret|token|credential)", re.I)
MAX_FIELD = 16384


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
        return value[:MAX_FIELD]
    if isinstance(value, list):
        return [_clean(item) for item in value[:500]]
    if isinstance(value, dict):
        return {str(k)[:128]: _clean(v, str(k)) for k, v in list(value.items())[:500]}
    return str(value)[:MAX_FIELD]


def _digest(previous, payload):
    return hashlib.sha256((previous + "\n" + payload).encode("utf-8")).hexdigest()


class ExecutionLedger:
    """SQLite hash chain. Tamper-evident, not tamper-proof."""

    def __init__(self, path=DEFAULT_DB):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        db = sqlite3.connect(str(self.path), timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=30000")
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def initialize(self):
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS execution_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL,
                    namespace TEXT NOT NULL, task_fingerprint TEXT NOT NULL,
                    task TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN
                        ('completed','failed','timeout','denied','cancelled')),
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

    def append(self, *, namespace, task, status, tool, evidence, duration_ms,
               tool_version="unknown", model="none", environment="unknown",
               cost_microunits=None, validator_results=None, metadata=None,
               event_id=None):
        for name, value in (("namespace", namespace), ("task", task), ("tool", tool)):
            if not isinstance(value, str) or not value.strip():
                raise LedgerError(f"{name} es obligatorio.")
        if status not in {"completed", "failed", "timeout", "denied", "cancelled"}:
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
        task = task.strip()[:MAX_FIELD]
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
                "tool_version": str(tool_version)[:256], "model": str(model)[:256],
                "environment": str(environment)[:512], "duration_ms": duration_ms,
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

    def history(self, *, namespace, limit=100):
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 1000:
            raise LedgerError("limit debe estar entre 1 y 1000.")
        with self.connect() as db:
            rows = db.execute(
                "SELECT sequence,event_id,created_at,task,status,tool,tool_version,model,"
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
