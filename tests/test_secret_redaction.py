import json
import unittest

from secret_redaction import redact_sensitive_data, redact_text


class SecretRedactionTests(unittest.TestCase):
    def test_redacts_json_fields_assignments_and_bearer_tokens(self):
        raw = (
            '{"api_key":"json-secret","Authorization":"Bearer bearer-secret",'
            '"safe":"ok"} password=inline-secret token=plain-token-secret'
        )
        cleaned = redact_text(raw)
        for secret in ("json-secret", "bearer-secret", "inline-secret", "plain-token-secret"):
            self.assertNotIn(secret, cleaned)
        self.assertIn('"api_key":"[REDACTED]"', cleaned)
        self.assertIn('"safe":"ok"', cleaned)

    def test_redaction_preserves_json_when_secret_assignment_is_inside_a_string(self):
        raw = json.dumps({"message": "password=embedded-secret", "safe": "ok"})
        cleaned = redact_text(raw)
        parsed = json.loads(cleaned)
        self.assertEqual(parsed["message"], "password=[REDACTED]")
        self.assertEqual(parsed["safe"], "ok")

    def test_redacts_common_provider_token_formats(self):
        tokens = (
            "AKIAIOSFODNN7EXAMPLE",
            "ghp_" + "a" * 30,
            "github_pat_" + "b" * 30,
            "xoxb-1234567890-abcdefghijk",
            "AIza" + "c" * 35,
            "sk-proj-" + "d" * 30,
            "eyJ" + "a" * 20 + "." + "b" * 20 + "." + "c" * 20,
        )
        cleaned = redact_text(" ".join(tokens))
        for token in tokens:
            self.assertNotIn(token, cleaned)

    def test_recursively_redacts_sensitive_fields_and_free_text(self):
        value = {
            "api_key": "nested-secret",
            "result": {
                "access_token": "nested-token",
                "message": "client_secret=inline-secret",
                "safe": "ordinary output",
            },
        }
        cleaned = redact_sensitive_data(value)
        self.assertEqual(cleaned["api_key"], "[REDACTED]")
        self.assertEqual(cleaned["result"]["access_token"], "[REDACTED]")
        self.assertNotIn("inline-secret", cleaned["result"]["message"])
        self.assertEqual(cleaned["result"]["safe"], "ordinary output")

    def test_redacts_private_keys_and_url_credentials(self):
        raw = (
            "https://alice:password@example.test/path "
            "-----BEGIN PRIVATE KEY-----\nprivate-material\n"
            "-----END PRIVATE KEY-----"
        )
        cleaned = redact_text(raw)
        self.assertNotIn("alice:password", cleaned)
        self.assertNotIn("private-material", cleaned)

    def test_redacts_private_signing_session_and_cookie_fields(self):
        value = {
            "private_key": "private-material",
            "hmac_key": "hmac-material",
            "signing_key": "signing-material",
            "cookie": "cookie-material",
            "session_id": "session-material",
        }
        cleaned = redact_sensitive_data(value)
        for field in value:
            self.assertEqual(cleaned[field], "[REDACTED]")
        text = redact_text(
            "hmac_key=inline-hmac cookie=inline-cookie "
            "session_id=inline-session"
        )
        for secret in ("inline-hmac", "inline-cookie", "inline-session"):
            self.assertNotIn(secret, text)

    def test_limits_recursive_depth(self):
        value = "safe"
        for _ in range(70):
            value = {"child": value}
        cleaned = redact_sensitive_data(value)
        for _ in range(65):
            cleaned = cleaned["child"]
        self.assertEqual(cleaned, "[REDACTED: nesting limit]")


if __name__ == "__main__":
    unittest.main()
