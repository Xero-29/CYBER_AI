import unittest
from unittest.mock import patch

import task_runner


class TaskRunnerLedgerTests(unittest.TestCase):
    def test_timeout_is_recorded(self):
        report = {"status": "timeout", "findings": []}
        with patch.object(task_runner, "ExecutionLedger") as ledger:
            task_runner._record_task_scan("web headers", "http://127.0.0.1", report, 0.0, "auth-1")
        ledger.return_value.append.assert_called_once()
        args = ledger.return_value.append.call_args.kwargs
        self.assertEqual(args["status"], "timeout")
        self.assertEqual(args["tool"], "nuclei_task_runner")
        self.assertEqual(args["namespace"], "security-scans")

    def test_authorization_denial_is_recorded(self):
        report = {"status": "authorization_denied", "findings": []}
        with patch.object(task_runner, "ExecutionLedger") as ledger:
            task_runner._record_task_scan("web headers", "http://127.0.0.1", report, 0.0)
        self.assertEqual(ledger.return_value.append.call_args.kwargs["status"], "denied")


if __name__ == "__main__":
    unittest.main()
