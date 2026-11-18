import json
import tempfile
import unittest
from pathlib import Path

from preflight import collect_checks
from tool_allowlist import sign_tool_allowlist


class PreflightToolAllowlistTests(unittest.TestCase):
    def collect(self, root, environ):
        return collect_checks(
            root=root,
            module_lookup=lambda _name: None,
            executable_lookup=lambda _name: None,
            environ=environ,
        )

    def tool_allowlist_check(self, report):
        return next(item for item in report["checks"] if item["name"] == "tool_allowlist")

    def test_missing_optional_allowlist_is_reported_as_warning(self):
        with tempfile.TemporaryDirectory() as temp:
            report = self.collect(Path(temp), {})
        check = self.tool_allowlist_check(report)
        self.assertEqual(check["status"], "warning")
        self.assertIn("compatibilidad", check["detail"])

    def test_missing_required_allowlist_blocks_preflight(self):
        with tempfile.TemporaryDirectory() as temp:
            report = self.collect(
                Path(temp), {"CYBER_AI_TOOL_ALLOWLIST_REQUIRED": "1"}
            )
        check = self.tool_allowlist_check(report)
        self.assertEqual(check["status"], "error")
        self.assertEqual(report["status"], "blocked")

    def test_valid_signed_allowlist_is_reported_without_exposing_key(self):
        key = "preflight-test-key-material-at-least-32-bytes"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = sign_tool_allowlist(
                {"ruff": {"sha256": "a" * 64}}, key.encode("utf-8")
            )
            path = root / "tools.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            report = self.collect(root, {
                "CYBER_AI_TOOL_ALLOWLIST_REQUIRED": "true",
                "CYBER_AI_TOOL_ALLOWLIST_PATH": str(path),
                "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": key,
            })
        check = self.tool_allowlist_check(report)
        self.assertEqual(check["status"], "ok")
        self.assertNotIn(key, check["detail"])
        self.assertIn("1 ejecutables", check["detail"])

    def test_partial_allowlist_configuration_is_an_error(self):
        with tempfile.TemporaryDirectory() as temp:
            report = self.collect(
                Path(temp),
                {"CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": "a" * 32},
            )
        check = self.tool_allowlist_check(report)
        self.assertEqual(check["status"], "error")


if __name__ == "__main__":
    unittest.main()
