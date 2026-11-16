import unittest
from unittest.mock import patch

import task_runner


class TaskRunnerLedgerTests(unittest.TestCase):
    def test_records_started_and_terminal_status_mapping(self):
        ledger = unittest.mock.Mock()
        ledger.append.return_value = {"event_id": "terminal"}
        with patch.object(task_runner, "ExecutionLedger", return_value=ledger):
            result = task_runner._record_task_scan(
                "audit", "https://example.test", {"status": "timeout"},
                0.0, "auth-1", "start-1",
            )
        self.assertEqual(result["event_id"], "terminal")
        args = ledger.append.call_args.kwargs
        self.assertEqual(args["status"], "timeout")
        self.assertEqual(args["metadata"]["start_event_id"], "start-1")
        self.assertEqual(args["metadata"]["authorization_id"], "auth-1")

    def test_ledger_failure_is_reported_to_fail_closed_caller(self):
        with patch.object(task_runner, "ExecutionLedger", side_effect=OSError("offline")):
            result = task_runner._record_task_scan(
                "audit", "https://example.test", {"status": "completed"}, 0.0
            )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
