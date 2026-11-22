import hashlib
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from process_isolation import (
    MAX_PROCESS_OUTPUT_BYTES,
    ProcessIsolationError,
    run_bounded_process,
)


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
        self.assertEqual(result["stdout_bytes"], 5000)
        self.assertEqual(result["stderr_bytes"], 5000)
        self.assertEqual(result["stdout_sha256"], hashlib.sha256(b"x" * 5000).hexdigest())
        self.assertEqual(result["stderr_sha256"], hashlib.sha256(b"y" * 5000).hexdigest())
        self.assertFalse(result["timed_out"])
        self.assertTrue(result["process_group_isolation_enforced"])
        self.assertFalse(result["process_tree_isolation_enforced"])


    def test_tail_capture_preserves_the_last_bytes_and_hashes_the_full_stream(self):
        payload = b"0123456789abcdef"
        with tempfile.TemporaryDirectory() as cwd:
            result = run_bounded_process(
                [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'0123456789abcdef')"],
                cwd=cwd,
                env=os.environ.copy(),
                timeout=5,
                max_output_bytes=16,
                capture_tail=True,
            )
        self.assertEqual(result["stdout"], "89abcdef")
        self.assertEqual(result["stdout_bytes"], len(payload))
        self.assertEqual(result["stdout_sha256"], hashlib.sha256(payload).hexdigest())
        self.assertTrue(result["stdout_truncated"])

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

    def test_output_limit_has_a_hard_upper_bound(self):
        with patch("process_isolation.subprocess.Popen") as popen:
            with self.assertRaises(ValueError):
                run_bounded_process(
                    [sys.executable, "-c", "pass"],
                    cwd=".",
                    env=os.environ.copy(),
                    timeout=1,
                    max_output_bytes=MAX_PROCESS_OUTPUT_BYTES + 1,
                )
        popen.assert_not_called()

    def test_invalid_command_and_environment_are_rejected_before_start(self):
        invalid_cases = (
            ([sys.executable, "\x00"], os.environ.copy(), "."),
            ([sys.executable, object()], os.environ.copy(), "."),
            ([sys.executable], {"BAD=KEY": "value"}, "."),
            ([sys.executable], {"GOOD": "bad\x00value"}, "."),
            ([sys.executable], os.environ.copy(), "\x00"),
        )
        with patch("process_isolation.subprocess.Popen") as popen:
            for command, env, cwd in invalid_cases:
                with self.subTest(command=repr(command), cwd=repr(cwd)):
                    with self.assertRaises(ValueError):
                        run_bounded_process(
                            command, cwd=cwd, env=env, timeout=1
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
