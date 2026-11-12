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

    def test_missing_authorization_id_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "")


if __name__ == "__main__":
    unittest.main()
