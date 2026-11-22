import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from execution_ledger import ExecutionLedger
import ledger_checkpoint
from ledger_checkpoint import CheckpointError, create_checkpoint, verify_checkpoint


class LedgerCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = ExecutionLedger(self.root / "ledger.sqlite3")
        self.key = "test-ledger-checkpoint-key-32-bytes-minimum"
        self.env = {"CYBER_AI_LEDGER_CHECKPOINT_KEY": self.key}
        self.ledger.append(namespace="test", task="checkpoint test",
                           status="completed", tool="unit", evidence={"ok": True},
                           duration_ms=1)

    def tearDown(self):
        self.temp.cleanup()

    def test_create_and_verify_external_anchor(self):
        checkpoint = self.root / "external" / "checkpoint.json"
        created = create_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)
        self.assertEqual(created["sequence"], 1)
        verified = verify_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)
        self.assertTrue(verified["valid"])

    def test_detects_checkpoint_tampering(self):
        checkpoint = self.root / "checkpoint.json"
        create_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)
        data = json.loads(checkpoint.read_text())
        data["head_hash"] = "f" * 64
        checkpoint.write_text(json.dumps(data))
        with self.assertRaises(CheckpointError):
            verify_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)

    def test_detects_ledger_rollback_to_empty_database(self):
        checkpoint = self.root / "checkpoint.json"
        create_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)
        empty = ExecutionLedger(self.root / "empty.sqlite3")
        with self.assertRaises(CheckpointError):
            verify_checkpoint(checkpoint, ledger=empty, environ=self.env)

    def test_requires_external_key(self):
        checkpoint = self.root / "checkpoint.json"
        with self.assertRaises(CheckpointError):
            create_checkpoint(checkpoint, ledger=self.ledger, environ={})

    def test_refuses_overwrite(self):
        checkpoint = self.root / "checkpoint.json"
        create_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)
        with self.assertRaises(CheckpointError):
            create_checkpoint(checkpoint, ledger=self.ledger, environ=self.env)


    def test_cli_redacts_error_and_result_paths(self):
        secret = "checkpoint-cli-secret"
        error_output = io.StringIO()
        with patch("sys.argv", ["ledger_checkpoint.py", "create", "--output", str(self.root / "x")]), patch.object(
            ledger_checkpoint, "create_checkpoint",
            side_effect=CheckpointError(f"checkpoint failed token={secret}"),
        ), redirect_stderr(error_output):
            result = ledger_checkpoint.main()
        self.assertEqual(result, 2)
        self.assertNotIn(secret, error_output.getvalue())
        self.assertIn("token=[REDACTED]", error_output.getvalue())

        success_output = io.StringIO()
        with patch("sys.argv", ["ledger_checkpoint.py", "create", "--output", str(self.root / "x")]), patch.object(
            ledger_checkpoint, "create_checkpoint",
            return_value={"checkpoint": f"/tmp/api_key={secret}", "sequence": 1},
        ), redirect_stdout(success_output):
            result = ledger_checkpoint.main()
        self.assertEqual(result, 0)
        self.assertNotIn(secret, success_output.getvalue())
        self.assertIn("[REDACTED]", success_output.getvalue())

if __name__ == "__main__":
    unittest.main()
