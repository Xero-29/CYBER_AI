import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from execution_ledger import (
    MAX_SQLITE_INTEGER, ExecutionLedger, LedgerError, _redact_text,
)


class ExecutionLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = ExecutionLedger(Path(self.tmp.name) / "ledger.sqlite3")

    def tearDown(self):
        self.tmp.cleanup()

    def append(self, **changes):
        data = dict(namespace="test", task="lint repository", status="completed",
                    tool="ruff", evidence={"stdout": "ok", "api_key": "sensitive"},
                    duration_ms=42, validator_results=[{"name": "exit_code", "passed": True}])
        data.update(changes)
        return self.ledger.append(**data)

    def test_hash_chain(self):
        first = self.append()
        second = self.append(status="failed", duration_ms=50)
        self.assertEqual(first["previous_hash"], "0" * 64)
        self.assertEqual(second["previous_hash"], first["event_hash"])
        self.assertTrue(self.ledger.verify()["valid"])
        self.assertEqual(self.ledger.verify()["checked"], 2)

    def test_started_event_is_a_valid_lifecycle_record(self):
        event = self.append(status="started", evidence={"phase": "start"}, duration_ms=0)
        self.assertEqual(event["status"], "started")
        self.assertTrue(self.ledger.verify()["valid"])

    def test_update_delete_blocked(self):
        self.append()
        with sqlite3.connect(self.ledger.path) as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("UPDATE execution_events SET status='failed'")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("DELETE FROM execution_events")

    def test_tampering_detected(self):
        self.append()
        with sqlite3.connect(self.ledger.path) as db:
            db.execute("DROP TRIGGER execution_events_no_update")
            db.execute("UPDATE execution_events SET task='tampered'")
        result = self.ledger.verify()
        self.assertFalse(result["valid"])
        self.assertEqual(result["failed_sequence"], 1)

    def test_verify_reports_malformed_json_without_raising(self):
        self.append()
        with sqlite3.connect(self.ledger.path) as db:
            db.execute("DROP TRIGGER execution_events_no_update")
            db.execute("UPDATE execution_events SET metadata='{'")
        result = self.ledger.verify()
        self.assertFalse(result["valid"])
        self.assertEqual(result["failed_sequence"], 1)
        self.assertEqual(result["reason"], "malformed_payload")

    def test_verify_runs_sqlite_integrity_check(self):
        self.append()
        with patch.object(self.ledger, "connect", wraps=self.ledger.connect) as connect:
            result = self.ledger.verify()
        self.assertTrue(result["valid"], result)
        self.assertTrue(connect.called)

    def test_connections_apply_defensive_sqlite_pragmas(self):
        connection = self.ledger.connect()
        try:
            self.assertEqual(
                connection.execute("PRAGMA trusted_schema").fetchone()[0], 0
            )
            self.assertEqual(
                connection.execute("PRAGMA secure_delete").fetchone()[0], 1
            )
            self.assertEqual(
                connection.execute("PRAGMA foreign_keys").fetchone()[0], 1
            )
        finally:
            connection.close()

    def test_secrets_are_redacted_from_free_text(self):
        value = _redact_text(
            "Authorization: Bearer abc123 api_key='super secret' "
            "https://alice:password@example.com/private"
        )
        for secret in ("abc123", "super secret", "alice:password"):
            self.assertNotIn(secret, value)
        self.assertIn("[REDACTED]", value)

    def test_redacts_provider_tokens_used_as_metadata_keys(self):
        tokens = ("ghp_" + "a" * 30, "ghp_" + "b" * 30)
        self.append(metadata={tokens[0]: "first", tokens[1]: "second"})
        with sqlite3.connect(self.ledger.path) as db:
            stored = db.execute(
                "SELECT metadata FROM execution_events"
            ).fetchone()[0]
        for token in tokens:
            self.assertNotIn(token, stored)
        parsed = __import__("json").loads(stored)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(set(parsed.values()), {"first", "second"})
        self.assertTrue(self.ledger.verify()["valid"])

    def test_redacts_private_keys_cookies_and_bytes_from_stored_metadata(self):
        self.append(
            metadata={
                "private_key": "private-material",
                "hmac_key": "hmac-material",
                "cookie": "cookie-material",
                "payload": b"Bearer byte-token-material",
            },
            validator_results=[{"session_id": "session-material"}],
        )
        with sqlite3.connect(self.ledger.path) as db:
            row = db.execute(
                "SELECT metadata, validator_results FROM execution_events"
            ).fetchone()
        stored = " ".join(row)
        for secret in (
            "private-material", "hmac-material", "cookie-material",
            "byte-token-material", "session-material",
        ):
            self.assertNotIn(secret, stored)
        self.assertIn("[REDACTED]", stored)

    def test_ledger_sanitization_limits_nested_metadata_depth(self):
        nested = "safe"
        for _ in range(100):
            nested = {"child": nested}
        self.append(metadata=nested)
        with sqlite3.connect(self.ledger.path) as db:
            stored = db.execute(
                "SELECT metadata FROM execution_events"
            ).fetchone()[0]
        self.assertIn("nesting limit", stored)
        self.assertTrue(self.ledger.verify()["valid"])

    def test_validation(self):
        with self.assertRaises(LedgerError):
            self.append(status="success")
        with self.assertRaises(LedgerError):
            self.append(duration_ms=-1)

    def test_sqlite_integer_bounds_are_validated_before_insert(self):
        accepted = self.append(
            duration_ms=MAX_SQLITE_INTEGER,
            cost_microunits=MAX_SQLITE_INTEGER,
        )
        self.assertEqual(accepted["status"], "completed")
        with self.assertRaises(LedgerError):
            self.append(task="duration overflow", duration_ms=MAX_SQLITE_INTEGER + 1)
        with self.assertRaises(LedgerError):
            self.append(
                task="cost overflow", cost_microunits=MAX_SQLITE_INTEGER + 1
            )
        self.assertTrue(self.ledger.verify()["valid"])

    def test_migrates_legacy_schema_without_breaking_hash_chain(self):
        path = Path(self.tmp.name) / "legacy.sqlite3"
        with sqlite3.connect(path) as db:
            db.executescript("""
                CREATE TABLE execution_events (
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
            """)
        migrated = ExecutionLedger(path)
        event = migrated.append(namespace="test", task="after migration",
                                status="started", tool="unit", evidence={}, duration_ms=0)
        self.assertEqual(event["status"], "started")
        recovered = migrated.reconcile_interrupted(stale_after_seconds=0)
        self.assertEqual(recovered["reconciled"], 1)
        self.assertEqual(migrated.history(namespace="test")[0]["status"], "interrupted")
        self.assertTrue(migrated.verify()["valid"])

    def test_environment_path_is_used_when_no_path_is_passed(self):
        configured = Path(self.tmp.name) / "external" / "ledger.sqlite3"
        with patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(configured)}):
            ledger = ExecutionLedger()
            ledger.append(namespace="test", task="env path", status="completed",
                          tool="unit-test", evidence={"ok": True}, duration_ms=1)
        self.assertTrue(configured.is_file())

    @unittest.skipIf(os.name == "nt", "Los bits POSIX no representan ACL de Windows.")
    def test_ledger_storage_is_created_with_private_permissions(self):
        path = Path(self.tmp.name) / "private" / "ledger.sqlite3"
        ExecutionLedger(path)
        self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    @unittest.skipIf(os.name == "nt", "La validación de permisos POSIX no aplica en Windows.")
    def test_ledger_rejects_group_or_world_accessible_parent(self):
        parent = Path(self.tmp.name) / "public"
        parent.mkdir(mode=0o755)
        parent.chmod(0o755)
        with self.assertRaisesRegex(LedgerError, "privado"):
            ExecutionLedger(parent / "ledger.sqlite3")

    @unittest.skipIf(os.name == "nt", "La propiedad POSIX no se valida en Windows.")
    def test_ledger_directory_must_belong_to_effective_user(self):
        parent = Path(self.tmp.name) / "owned-by-other"
        parent.mkdir(mode=0o700)
        other_uid = os.geteuid() + 1
        with patch("execution_ledger.os.geteuid", return_value=other_uid):
            with self.assertRaisesRegex(LedgerError, "pertenecer al usuario"):
                ExecutionLedger(parent / "ledger.sqlite3")

    @unittest.skipIf(os.name == "nt", "Los hard links POSIX no representan ACL de Windows.")
    def test_ledger_rejects_hard_linked_database_file(self):
        parent = Path(self.tmp.name) / "hard-link-case"
        parent.mkdir(mode=0o700)
        original = parent / "original.db"
        original.write_bytes(b"not a ledger")
        linked = parent / "ledger.sqlite3"
        os.link(original, linked)
        with self.assertRaisesRegex(LedgerError, "enlaces duros"):
            ExecutionLedger(linked)

    def test_ledger_rejects_symlinked_database_and_parent(self):
        target = Path(self.tmp.name) / "target.sqlite3"
        target.write_bytes(b"")
        database_link = Path(self.tmp.name) / "database-link.sqlite3"
        database_link.symlink_to(target)
        with self.assertRaisesRegex(LedgerError, "symlinks"):
            ExecutionLedger(database_link)

        real_parent = Path(self.tmp.name) / "real-parent"
        real_parent.mkdir(mode=0o700)
        parent_link = Path(self.tmp.name) / "parent-link"
        parent_link.symlink_to(real_parent, target_is_directory=True)
        with self.assertRaisesRegex(LedgerError, "symlinks"):
            ExecutionLedger(parent_link / "ledger.sqlite3")

    def test_ledger_rejects_symlinked_wal_companion(self):
        directory = Path(self.tmp.name) / "wal-case"
        directory.mkdir(mode=0o700)
        path = directory / "ledger.sqlite3"
        target = directory / "external-wal"
        target.write_bytes(b"")
        Path(f"{path}-wal").symlink_to(target)
        with self.assertRaisesRegex(LedgerError, "archivos auxiliares"):
            ExecutionLedger(path)

    def test_namespace_isolation(self):
        self.append(namespace="alpha")
        self.append(namespace="beta")
        self.assertEqual(len(self.ledger.history(namespace="alpha")), 1)
        self.assertEqual(len(self.ledger.history(namespace="beta")), 1)

    def test_real_subprocess_crash_is_reconciled_after_restart(self):
        path = Path(self.tmp.name) / "crash-ledger.sqlite3"
        code = """
import os
import sys
from execution_ledger import ExecutionLedger
ledger = ExecutionLedger(sys.argv[1])
ledger.append(
    namespace="crash-test", task="crash between start and result",
    status="started", tool="subprocess-fixture",
    evidence={"phase": "start"}, duration_ms=0,
    metadata={"task_id": "abrupt-exit-fixture"},
)
os._exit(0)
"""
        subprocess.run(
            [sys.executable, "-c", code, str(path)],
            cwd=str(Path(__file__).resolve().parents[1]),
            check=True,
            timeout=15,
        )
        recovered = ExecutionLedger(path)
        result = recovered.reconcile_interrupted(stale_after_seconds=0)
        self.assertEqual(result["reconciled"], 1)
        history = sorted(
            recovered.history(namespace="crash-test"),
            key=lambda event: event["sequence"],
        )
        self.assertEqual(
            [event["status"] for event in history],
            ["started", "interrupted"],
        )
        self.assertEqual(
            history[-1]["metadata"]["start_event_id"],
            history[0]["event_id"],
        )
        self.assertTrue(recovered.verify()["valid"])
        self.assertEqual(recovered.reconcile_interrupted()["reconciled"], 0)

    def test_reconcile_marks_orphaned_start_as_interrupted_and_is_idempotent(self):
        started = self.append(
            status="started",
            evidence={"phase": "start"},
            duration_ms=0,
            metadata={"task_id": "crashed-task"},
        )
        result = self.ledger.reconcile_interrupted(stale_after_seconds=0)
        self.assertEqual(result["reconciled"], 1)
        history = self.ledger.history(namespace="test")
        terminal = next(item for item in history if item["status"] == "interrupted")
        self.assertEqual(terminal["metadata"]["start_event_id"], started["event_id"])
        self.assertEqual(terminal["metadata"]["recovered_by"], "execution_ledger.reconcile_interrupted")
        self.assertEqual(terminal["status"], "interrupted")
        self.assertEqual(terminal["metadata"]["original_started_at"], history[-1]["created_at"])
        self.assertEqual(self.ledger.reconcile_interrupted()["reconciled"], 0)
        self.assertTrue(self.ledger.verify()["valid"])

    def test_reconcile_refuses_to_append_to_a_corrupted_chain(self):
        self.append(status="started", evidence={"phase": "start"}, duration_ms=0)
        with sqlite3.connect(self.ledger.path) as db:
            db.execute("DROP TRIGGER execution_events_no_update")
            db.execute("UPDATE execution_events SET task='tampered'")
        with self.assertRaises(LedgerError):
            self.ledger.reconcile_interrupted()
        with sqlite3.connect(self.ledger.path) as db:
            count = db.execute(
                "SELECT COUNT(*) FROM execution_events WHERE status='interrupted'"
            ).fetchone()[0]
        self.assertEqual(count, 0)

    def test_reconcile_skips_recent_starts_by_default(self):
        self.append(status="started", evidence={"phase": "start"}, duration_ms=0)
        result = self.ledger.reconcile_interrupted()
        self.assertEqual(result["reconciled"], 0)
        self.assertTrue(self.ledger.verify()["valid"])

    def test_reconcile_rejects_unrepresentable_stale_threshold(self):
        with self.assertRaises(LedgerError):
            self.ledger.reconcile_interrupted(stale_after_seconds=10**1000)

    def test_reconcile_does_not_close_start_with_existing_terminal_event(self):
        started = self.append(
            status="started", evidence={"phase": "start"}, duration_ms=0,
        )
        self.append(
            status="completed",
            metadata={"start_event_id": started["event_id"]},
        )
        result = self.ledger.reconcile_interrupted()
        self.assertEqual(result["reconciled"], 0)
        self.assertTrue(self.ledger.verify()["valid"])

    def test_concurrent_writers_preserve_a_valid_contiguous_hash_chain(self):
        worker_count = 6
        events_per_worker = 8

        def write_events(worker):
            return [
                self.ledger.append(
                    namespace=f"worker-{worker}",
                    task=f"concurrent task {worker}-{index}",
                    status="completed",
                    tool="concurrency-test",
                    evidence={"worker": worker, "index": index},
                    duration_ms=index,
                )
                for index in range(events_per_worker)
            ]

        with ThreadPoolExecutor(max_workers=worker_count) as pool:
            results = list(pool.map(write_events, range(worker_count)))

        written = [event for worker_events in results for event in worker_events]
        sequences = sorted(event["sequence"] for event in written)
        expected_count = worker_count * events_per_worker
        self.assertEqual(sequences, list(range(1, expected_count + 1)))
        verification = self.ledger.verify()
        self.assertTrue(verification["valid"], verification)
        self.assertEqual(verification["checked"], expected_count)



    def test_sqlite_busy_writer_fails_without_partial_event(self):
        self.append(task="before lock")
        with sqlite3.connect(self.ledger.path, timeout=0, isolation_level=None) as lock:
            lock.execute("BEGIN IMMEDIATE")

            def no_wait_connection():
                db = sqlite3.connect(
                    str(self.ledger.path), timeout=0, isolation_level=None
                )
                db.row_factory = sqlite3.Row
                db.execute("PRAGMA busy_timeout=0")
                return db

            with patch.object(self.ledger, "connect", side_effect=no_wait_connection):
                with self.assertRaises(sqlite3.OperationalError):
                    self.append(task="blocked writer")

            lock.rollback()

        history = self.ledger.history(namespace="test")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["task"], "before lock")
        self.assertTrue(self.ledger.verify()["valid"])

    def test_verify_reports_unreadable_sqlite_database(self):
        self.ledger.append(
            namespace="test", task="before corruption", status="completed",
            tool="unit", evidence={}, duration_ms=1,
        )
        with self.ledger.connect() as db:
            db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        self.ledger.path.write_bytes(b"not a SQLite database")
        result = self.ledger.verify()
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "database_error")

    def test_failed_sqlite_write_rolls_back_without_partial_ledger_event(self):
        self.append(task="prior valid event")
        with sqlite3.connect(self.ledger.path) as db:
            db.execute("""
                CREATE TRIGGER simulate_storage_failure
                AFTER INSERT ON execution_events
                BEGIN
                    SELECT RAISE(ABORT, 'simulated storage failure');
                END
            """)
        with self.assertRaisesRegex(sqlite3.IntegrityError, "simulated storage failure"):
            self.append(task="event that must roll back")
        with sqlite3.connect(self.ledger.path) as db:
            rows = db.execute(
                "SELECT task,status FROM execution_events ORDER BY sequence"
            ).fetchall()
        self.assertEqual(rows, [("prior valid event", "completed")])
        verification = self.ledger.verify()
        self.assertTrue(verification["valid"], verification)
        self.assertEqual(verification["checked"], 1)

    def test_duplicate_event_id_does_not_change_existing_hash_chain(self):
        first = self.append(event_id="stable-event-id", task="first event")
        with self.assertRaises(sqlite3.IntegrityError):
            self.append(event_id="stable-event-id", task="duplicate event")
        history = self.ledger.history(namespace="test")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["event_id"], first["event_id"])
        self.assertTrue(self.ledger.verify()["valid"])

if __name__ == "__main__":
    unittest.main()
