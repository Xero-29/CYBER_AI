import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tool_allowlist import (
    ToolAllowlistError,
    load_signed_tool_allowlist,
    sign_tool_allowlist,
    verify_tool_allowed,
)


class ToolAllowlistTests(unittest.TestCase):
    def setUp(self):
        self.key = b"test-only-key-material-32-bytes!!"
        self.digest = "a" * 64
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "tools.json"
        self.document = sign_tool_allowlist({"ruff": {"sha256": self.digest}}, self.key)
        self.path.write_text(json.dumps(self.document), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_signature_and_binary_are_accepted(self):
        self.assertEqual(load_signed_tool_allowlist(self.path, self.key)["ruff"]["sha256"], self.digest)

    def test_tampered_manifest_is_rejected(self):
        changed = dict(self.document)
        changed["tools"] = {"ruff": {"sha256": "b" * 64}}
        self.path.write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaises(ToolAllowlistError):
            load_signed_tool_allowlist(self.path, self.key)


    def test_duplicate_json_keys_are_rejected(self):
        self.path.write_text(
            '{"schema_version":1,"schema_version":1,"tools":{}, "signature":"'
            + "0" * 64 + '"}', encoding="utf-8"
        )
        with self.assertRaises(ToolAllowlistError):
            load_signed_tool_allowlist(self.path, self.key)

    def test_signer_rejects_invalid_tool_ids_and_hashes(self):
        with self.assertRaises(ToolAllowlistError):
            sign_tool_allowlist({"Ruff": {"sha256": self.digest}}, self.key)
        with self.assertRaises(ToolAllowlistError):
            sign_tool_allowlist({"ruff": {"sha256": "not-a-hash"}}, self.key)

    def test_oversized_manifest_is_rejected(self):
        self.path.write_bytes(b" " * 65537)
        with self.assertRaises(ToolAllowlistError):
            load_signed_tool_allowlist(self.path, self.key)

    def test_non_regular_manifest_is_rejected(self):
        directory = Path(self.temp.name) / "manifest-dir"
        directory.mkdir()
        with self.assertRaises(ToolAllowlistError):
            load_signed_tool_allowlist(directory, self.key)

    def test_verifier_rejects_invalid_tool_id_and_binary_digest(self):
        with self.assertRaises(ToolAllowlistError):
            verify_tool_allowed("../ruff", self.digest)
        with self.assertRaises(ToolAllowlistError):
            verify_tool_allowed("ruff", "not-a-digest")

    def test_short_key_is_rejected(self):
        with self.assertRaises(ToolAllowlistError):
            sign_tool_allowlist({"ruff": {"sha256": self.digest}}, b"short")

    def test_symlink_is_rejected(self):
        link = Path(self.temp.name) / "link.json"
        try:
            link.symlink_to(self.path)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaises(ToolAllowlistError):
            load_signed_tool_allowlist(link, self.key)

    def test_required_policy_fails_when_not_configured(self):
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_REQUIRED": "1",
            "CYBER_AI_TOOL_ALLOWLIST_PATH": "",
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": "",
        }, clear=False):
            with self.assertRaises(ToolAllowlistError):
                verify_tool_allowed("ruff", self.digest)

    def test_matching_tool_is_approved(self):
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": str(self.path),
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": self.key.decode(),
            "CYBER_AI_TOOL_ALLOWLIST_REQUIRED": "1",
        }, clear=False):
            self.assertTrue(verify_tool_allowed("ruff", self.digest)["enforced"])

    def test_unknown_or_changed_binary_is_denied(self):
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": str(self.path),
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": self.key.decode(),
            "CYBER_AI_TOOL_ALLOWLIST_REQUIRED": "1",
        }, clear=False):
            with self.assertRaises(ToolAllowlistError):
                verify_tool_allowed("ruff", "c" * 64)


if __name__ == "__main__":
    unittest.main()
