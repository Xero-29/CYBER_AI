import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from execution_policy import AuthorizationError, authorize_target


class ExecutionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.policy = Path(self.temp.name) / "authorizations.json"
        self.env = patch.dict(
            "os.environ",
            {"CYBER_AI_AUTHORIZATIONS_FILE": str(self.policy)},
        )
        self.env.start()
        self.grant = {
            "id": "grant-001",
            "target": "https://8.8.8.8/",
            "actions": ["nuclei_scan", "inspect_http_headers"],
            "approved_by": "security-owner",
            "ticket": "CHANGE-123",
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat(),
        }
        self.write_policy([self.grant])

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def write_policy(self, grants):
        self.policy.write_text(
            json.dumps({"authorizations": grants}),
            encoding="utf-8",
        )
        self.policy.chmod(0o600)

    def test_exact_target_and_action_grant_is_accepted(self):
        result = authorize_target(
            "https://8.8.8.8",
            "nuclei_scan",
            "grant-001",
        )
        self.assertEqual(result["ticket"], "CHANGE-123")
        self.assertEqual(result["approved_by"], "security-owner")

    def test_wrong_target_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://1.1.1.1", "nuclei_scan", "grant-001")

    def test_wrong_action_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "arbitrary_command", "grant-001")

    def test_expired_grant_is_denied(self):
        self.grant["expires_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=1)
        ).isoformat()
        self.write_policy([self.grant])
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_hostname_is_rejected_until_dns_pinning_exists(self):
        with self.assertRaisesRegex(AuthorizationError, "IP literales"):
            authorize_target("https://example.com", "nuclei_scan", "grant-001")

    def test_private_address_is_denied(self):
        with self.assertRaisesRegex(AuthorizationError, "IP pública"):
            authorize_target("http://127.0.0.1", "nuclei_scan", "grant-001")

    def test_grant_file_with_insecure_permissions_is_denied(self):
        self.policy.chmod(0o644)
        with self.assertRaisesRegex(AuthorizationError, "0600"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_missing_authorization_id_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "")



    def test_duplicate_json_keys_are_rejected(self):
        self.policy.write_text(
            '{"authorizations":[],"authorizations":[]}', encoding="utf-8"
        )
        self.policy.chmod(0o600)
        with self.assertRaisesRegex(AuthorizationError, "duplicadas"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_insecure_empty_policy_remains_deny_by_default(self):
        self.write_policy([])
        self.policy.chmod(0o644)
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_insecure_policy_with_grants_is_rejected(self):
        self.policy.chmod(0o644)
        with self.assertRaisesRegex(AuthorizationError, "0600"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_policy_symlink_is_rejected(self):
        link = Path(self.temp.name) / "policy-link.json"
        try:
            link.symlink_to(self.policy)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with patch.dict("os.environ", {"CYBER_AI_AUTHORIZATIONS_FILE": str(link)}):
            with self.assertRaisesRegex(AuthorizationError, "enlace"):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_non_regular_policy_path_is_rejected(self):
        directory = Path(self.temp.name) / "policy-directory"
        directory.mkdir()
        with patch.dict("os.environ", {"CYBER_AI_AUTHORIZATIONS_FILE": str(directory)}):
            with self.assertRaises(AuthorizationError):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_oversized_policy_is_rejected(self):
        self.policy.write_bytes(b" " * (1024 * 1024 + 1))
        self.policy.chmod(0o600)
        with self.assertRaisesRegex(AuthorizationError, "1 MiB"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_action_string_cannot_match_by_substring(self):
        self.grant["actions"] = "prefix_nuclei_scan_suffix"
        self.write_policy([self.grant])
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_duplicate_grant_ids_are_rejected(self):
        duplicate = dict(self.grant)
        duplicate["target"] = "https://1.1.1.1"
        self.write_policy([self.grant, duplicate])
        with self.assertRaisesRegex(AuthorizationError, "identificadores duplicados"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_ambiguous_url_paths_and_zero_port_are_rejected(self):
        for target in (
            "https://8.8.8.8:0",
            "https://8.8.8.8:/",
            "https://8.8.8.8/%2e%2e/admin",
            "https://8.8.8.8/a/../admin",
            "https://8.8.8.8/a\\\\b",
        ):
            with self.subTest(target=target):
                with self.assertRaises(AuthorizationError):
                    authorize_target(target, "nuclei_scan", "grant-001")

    def test_non_string_action_and_target_are_rejected(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", ["nuclei_scan"], "grant-001")
        with self.assertRaises(AuthorizationError):
            authorize_target(8.8, "nuclei_scan", "grant-001")

if __name__ == "__main__":
    unittest.main()
