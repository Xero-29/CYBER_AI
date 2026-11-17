import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tool_execution_profiles import (
    ProfileConfigError, get_custom_tools, load_active_profile,
)
from custom_tool_runner import run_custom_tool
from tool_allowlist import sign_tool_allowlist


class ToolExecutionProfileTests(unittest.TestCase):
    def _config(self, directory):
        path = Path(directory) / "profiles.json"
        path.write_text(json.dumps({
            "schema_version": 1,
            "default_profile": "standard",
            "profiles": {
                "standard": {"max_tools": 2, "allow_external_targets": False,
                             "timeout_seconds": 90, "enable_custom_tools": False},
                "extended": {"max_tools": None, "allow_external_targets": True,
                             "timeout_seconds": 240, "enable_custom_tools": True},
            },
            "custom_tools": [{
                "id": "custom_python_check", "description": "Custom Python check",
                "category": "quality", "keywords": ["custom check"],
                "executable": sys.executable,
                "argv": ["-c", "print('custom-ok')", "{target}"],
                "timeout_seconds": 30, "enabled": True,
            }],
        }), encoding="utf-8")
        return path

    def test_profile_selection_and_custom_tool_opt_in(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            with patch.dict(os.environ, {
                "CYBER_AI_TOOL_CONFIG": str(path),
                "CYBER_AI_TOOL_PROFILE": "standard",
            }, clear=False):
                _, name, profile = load_active_profile()
                self.assertEqual(name, "standard")
                self.assertFalse(profile["allow_external_targets"])
                self.assertEqual(get_custom_tools(), [])
            with patch.dict(os.environ, {
                "CYBER_AI_TOOL_CONFIG": str(path),
                "CYBER_AI_TOOL_PROFILE": "extended",
            }, clear=False):
                _, name, profile = load_active_profile()
                self.assertEqual(name, "extended")
                self.assertTrue(profile["allow_external_targets"])
                self.assertEqual(len(get_custom_tools()), 1)

    def test_unknown_profile_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            with patch.dict(os.environ, {
                "CYBER_AI_TOOL_CONFIG": str(path),
                "CYBER_AI_TOOL_PROFILE": "missing",
            }, clear=False):
                with self.assertRaises(ProfileConfigError):
                    load_active_profile()

    def test_custom_runner_uses_argv_and_signed_binary_allowlist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            import hashlib
            digest = hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()
            key = "k" * 64
            allowlist = sign_tool_allowlist(
                {"custom_python_check": {"sha256": digest}}, key.encode("utf-8")
            )
            allowlist_path = root / "allowlist.json"
            allowlist_path.write_text(json.dumps(allowlist), encoding="utf-8")
            spec = {
                "id": "custom_python_check", "executable": sys.executable,
                "argv": ["-c", "print('custom-ok')", "{target}"],
                "timeout_seconds": 10,
            }
            with patch.dict(os.environ, {
                "CYBER_AI_TOOL_ALLOWLIST_PATH": str(allowlist_path),
                "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": key,
                "CYBER_AI_TOOL_ALLOWLIST_REQUIRED": "1",
            }, clear=False):
                evidence = run_custom_tool(spec, str(target), allow_external=True)
            self.assertEqual(evidence["status"], "completed")
            self.assertEqual(evidence["return_code"], 0)
            self.assertIn("custom-ok", evidence["stdout"])
            self.assertTrue(evidence["tool_allowlist"]["enforced"])
            self.assertEqual(evidence["network_access"], "not_enforced")


if __name__ == "__main__":
    unittest.main()
