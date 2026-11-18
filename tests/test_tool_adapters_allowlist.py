import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tool_adapters
from tool_allowlist import ToolAllowlistError


class ToolAdapterAllowlistIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.target = Path(self.temp.name) / "target.py"
        self.target.write_text("print('safe')\n", encoding="utf-8")
        self.digest = "a" * 64
        self.binary = {
            "resolved_path": sys.executable,
            "sha256": self.digest,
        }

    def tearDown(self):
        self.temp.cleanup()

    def patches(self, allowlist):
        return (
            patch.object(tool_adapters, "_confined_path", return_value=self.target),
            patch.object(tool_adapters.shutil, "which", return_value=sys.executable),
            patch.object(tool_adapters, "_hash_binary", return_value=self.binary),
            patch.object(
                tool_adapters, "_build_command",
                return_value=[sys.executable, "-c", "print('{}')"],
            ),
            patch.object(tool_adapters, "_probe_tool_version", return_value="python test"),
            patch.object(tool_adapters, "_hash_target", return_value="b" * 64),
            patch.object(tool_adapters, "verify_tool_allowed", return_value=allowlist),
        )

    def test_approved_binary_policy_is_attached_to_execution_evidence(self):
        policy = {"enforced": True, "status": "approved", "sha256": self.digest}
        with self.patches(policy)[0], self.patches(policy)[1], self.patches(policy)[2], \
             self.patches(policy)[3], self.patches(policy)[4], self.patches(policy)[5], \
             self.patches(policy)[6]:
            evidence = tool_adapters.run_local_tool("ruff", "target.py")
        self.assertEqual(evidence["status"], "completed")
        self.assertEqual(evidence["binary_allowlist"], policy)
        self.assertTrue(evidence["tool_reported_success"])

    def test_unapproved_binary_is_denied_before_process_start(self):
        with self.patches(None)[0], self.patches(None)[1], self.patches(None)[2], \
             patch.object(
                 tool_adapters, "verify_tool_allowed",
                 side_effect=ToolAllowlistError("not approved"),
             ), patch.object(tool_adapters.subprocess, "Popen") as process:
            with self.assertRaisesRegex(tool_adapters.ToolExecutionError, "allowlist firmada"):
                tool_adapters.run_local_tool("ruff", "target.py")
        process.assert_not_called()


if __name__ == "__main__":
    unittest.main()
