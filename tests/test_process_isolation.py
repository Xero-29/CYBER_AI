import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from process_isolation import ProcessIsolationError, run_bounded_process


class ProcessIsolationTests(unittest.TestCase):
    def test_captures_output_with_a_total_byte_limit(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = run_bounded_process(
                [
                    sys.executable,
                    "-c",
                    "import sys; sys.stdout.write('x' * 5000); sys.stderr.write('y' * 5000)",
                ],
                cwd=cwd,
                env=os.environ.copy(),
                timeout=5,
                max_output_bytes=1024,
            )
        self.assertEqual(result["returncode"], 0)
        self.assertLessEqual(len(result["stdout"].encode()), 512)
        self.assertLessEqual(len(result["stderr"].encode()), 512)
        self.assertTrue(result["output_truncated"])
        self.assertFalse(result["timed_out"])
        self.assertTrue(result["process_group_isolation_enforced"])
        self.assertFalse(result["process_tree_isolation_enforced"])

    def test_timeout_terminates_the_process_group(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = run_bounded_process(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                cwd=cwd,
                env=os.environ.copy(),
                timeout=0.1,
                max_output_bytes=1024,
            )
        self.assertTrue(result["timed_out"])
        self.assertNotEqual(result["returncode"], 0)
        self.assertTrue(result["process_group_isolation_enforced"])
        self.assertFalse(result["process_tree_isolation_enforced"])

    def test_invalid_limits_are_rejected_before_process_start(self):
        invalid_timeouts = (
            0, -1, float("nan"), float("inf"), float("-inf"),
            86_401, 1e308, 10 ** 1000,
        )
        with patch("process_isolation.subprocess.Popen") as popen:
            for timeout in invalid_timeouts:
                with self.subTest(timeout=str(timeout)[:40]):
                    with self.assertRaises(ValueError):
                        run_bounded_process(
                            [sys.executable, "-c", "pass"],
                            cwd=".",
                            env=os.environ.copy(),
                            timeout=timeout,
                        )
        popen.assert_not_called()

    def test_non_posix_execution_fails_closed_without_job_objects(self):
        with patch("process_isolation.os.name", "nt"):
            with patch("process_isolation.subprocess.Popen") as popen:
                with self.assertRaises(ProcessIsolationError):
                    run_bounded_process(
                        [sys.executable, "-c", "pass"],
                        cwd=".",
                        env=os.environ.copy(),
                        timeout=1,
                    )
        popen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
