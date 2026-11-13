import sqlite3
import tempfile
import unittest
from pathlib import Path

from execution_ledger import ExecutionLedger, LedgerError


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

    def test_validation(self):
        with self.assertRaises(LedgerError):
            self.append(status="success")
        with self.assertRaises(LedgerError):
            self.append(duration_ms=-1)

    def test_namespace_isolation(self):
        self.append(namespace="alpha")
        self.append(namespace="beta")
        self.assertEqual(len(self.ledger.history(namespace="alpha")), 1)
        self.assertEqual(len(self.ledger.history(namespace="beta")), 1)


if __name__ == "__main__":
    unittest.main()
