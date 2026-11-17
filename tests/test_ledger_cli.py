import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import ledger_cli
from execution_ledger import ExecutionLedger


class LedgerCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "ledger.sqlite3"
        self.env = patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(self.path)})
        self.env.start()
        ExecutionLedger().append(
            namespace="test", task="cli verification", status="completed",
            tool="unit-test", evidence={"ok": True}, duration_ms=1,
        )

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def test_verify_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = ledger_cli.main(["verify"])
        self.assertEqual(result, 0)
        self.assertTrue(json.loads(output.getvalue())["valid"])

    def test_history_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = ledger_cli.main(["history", "--namespace", "test"])
        self.assertEqual(result, 0)
        events = json.loads(output.getvalue())
        self.assertEqual(events[0]["task"], "cli verification")

    def test_namespaces_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = ledger_cli.main(["namespaces"])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue()), ["test"])


if __name__ == "__main__":
    unittest.main()
