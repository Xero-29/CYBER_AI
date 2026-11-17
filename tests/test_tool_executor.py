import unittest

from tool_executor import _terminal_status


class ToolExecutorTests(unittest.TestCase):
    def test_finding_exit_code_can_represent_a_successful_scan(self):
        self.assertEqual(
            _terminal_status({
                "status": "completed",
                "return_code": 1,
                "tool_reported_success": True,
                "findings_present": True,
            }),
            "completed",
        )

    def test_unaccepted_exit_code_remains_a_failed_execution(self):
        self.assertEqual(
            _terminal_status({
                "status": "completed",
                "return_code": 2,
                "tool_reported_success": False,
            }),
            "failed",
        )

    def test_timeout_and_denied_statuses_are_preserved(self):
        self.assertEqual(_terminal_status({"status": "timeout"}), "timeout")
        self.assertEqual(_terminal_status({"status": "denied"}), "denied")


if __name__ == "__main__":
    unittest.main()
