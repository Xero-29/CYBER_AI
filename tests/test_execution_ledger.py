import os
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from execution_ledger import ExecutionLedger, LedgerError, _redact_text


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

    def test_secrets_are_redacted_from_free_text(self):
        value = _redact_text(
            "Authorization: Bearer abc123 api_key='super secret' "
            "https://alice:password@example.com/private"
        )
        for secret in ("abc123", "super secret", "alice:password"):
            self.assertNotIn(secret, value)
        self.assertIn("[REDACTED]", value)

    def test_validation(self):
        with self.assertRaises(LedgerError):
            self.append(status="success")
        with self.assertRaises(LedgerError):
            self.append(duration_ms=-1)

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
        self.assertTrue(migrated.verify()["valid"])

    def test_environment_path_is_used_when_no_path_is_passed(self):
        configured = Path(self.tmp.name) / "external" / "ledger.sqlite3"
        with patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(configured)}):
            ledger = ExecutionLedger()
            ledger.append(namespace="test", task="env path", status="completed",
                          tool="unit-test", evidence={"ok": True}, duration_ms=1)
        self.assertTrue(configured.is_file())

    def test_namespace_isolation(self):
        self.append(namespace="alpha")
        self.append(namespace="beta")
        self.assertEqual(len(self.ledger.history(namespace="alpha")), 1)
        self.assertEqual(len(self.ledger.history(namespace="beta")), 1)

    def test_reconcile_marks_orphaned_start_as_interrupted_and_is_idempotent(self):
        started = self.append(
            status="started",
            evidence={"phase": "start"},
            duration_ms=0,
            metadata={"task_id": "crashed-task"},
        )
        result = self.ledger.reconcile_interrupted()
        self.assertEqual(result["reconciled"], 1)
        history = self.ledger.history(namespace="test")
        terminal = next(item for item in history if item["status"] == "interrupted")
        self.assertEqual(terminal["metadata"]["start_event_id"], started["event_id"])
        self.assertEqual(terminal["metadata"]["recovered_by"], "execution_ledger.reconcile_interrupted")
        self.assertEqual(terminal["status"], "interrupted")
        self.assertEqual(terminal["metadata"]["original_started_at"], history[-1]["created_at"])
        self.assertEqual(self.ledger.reconcile_interrupted()["reconciled"], 0)
        self.assertTrue(self.ledger.verify()["valid"])

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


if __name__ == "__main__":
    unittest.main()
