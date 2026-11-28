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

    def test_redacts_escaped_quoted_assignments_without_breaking_json(self):
        message = 'password="prefix\\"suffix"'
        raw = json.dumps({"message": message, "safe": "ok"})
        cleaned = redact_text(raw)
        parsed = json.loads(cleaned)
        self.assertEqual(parsed["message"], 'password="[REDACTED]"')
        self.assertNotIn("prefix", cleaned)
        self.assertNotIn("suffix", cleaned)

        structured = redact_sensitive_data({"message": message})
        self.assertEqual(structured["message"], 'password="[REDACTED]"')

    def test_redacts_credentials_in_non_http_uris(self):
        raw = (
            "postgresql://cyber_user:db-secret@db.internal:5432/cyber "
            "postgres://:empty-user-secret@db.internal/cyber"
        )
        cleaned = redact_text(raw)
        for secret in ("cyber_user:db-secret", "db-secret", "empty-user-secret"):
            self.assertNotIn(secret, cleaned)
        self.assertIn("postgresql://[REDACTED]@db.internal", cleaned)
        self.assertIn("postgres://[REDACTED]@db.internal", cleaned)

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

    def test_redacts_provider_tokens_used_as_mapping_keys_without_losing_entries(self):
        tokens = ("ghp_" + "a" * 30, "ghp_" + "b" * 30)
        cleaned = redact_sensitive_data({tokens[0]: "first", tokens[1]: "second"})
        serialized = json.dumps(cleaned)
        for token in tokens:
            self.assertNotIn(token, serialized)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(set(cleaned.values()), {"first", "second"})
        self.assertTrue(all(key.startswith("[REDACTED TOKEN]") for key in cleaned))


    def test_redacted_mapping_key_suffix_collision_never_overwrites_entries(self):
        token_a = "ghp_" + "a" * 30
        token_b = "ghp_" + "b" * 30
        source = {
            "[REDACTED TOKEN]#2": "literal-key",
            token_a: "first-token",
            token_b: "second-token",
        }
        cleaned = redact_sensitive_data(source)
        serialized = json.dumps(cleaned)
        self.assertNotIn(token_a, serialized)
        self.assertNotIn(token_b, serialized)
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(set(cleaned.values()), {"literal-key", "first-token", "second-token"})

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

    def test_redacts_client_secret_fields_in_nested_structures(self):
        value = {
            "client_secret": "snake-case-client-secret",
            "oauth": {
                "clientSecret": "camel-case-client-secret",
                "safe": "ordinary value",
            },
        }
        cleaned = redact_sensitive_data(value)
        self.assertEqual(cleaned["client_secret"], "[REDACTED]")
        self.assertEqual(cleaned["oauth"]["clientSecret"], "[REDACTED]")
        self.assertEqual(cleaned["oauth"]["safe"], "ordinary value")

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



    def test_redacts_signed_url_query_credentials(self):
        raw = (
            "https://cdn.example.org/file.pdf?"
            "X-Amz-Credential=aws-credential-secret&"
            "X-Amz-Signature=signature-secret&"
            "X-Amz-Security-Token=security-token-secret&"
            "sig=short-signature-secret&response-content-type=application%2Fpdf"
        )
        cleaned = redact_text(raw)
        for secret in (
            "aws-credential-secret",
            "signature-secret",
            "security-token-secret",
            "short-signature-secret",
        ):
            self.assertNotIn(secret, cleaned)
        self.assertIn("response-content-type=application%2Fpdf", cleaned)
        self.assertIn("X-Amz-Signature=[REDACTED]", cleaned)

if __name__ == "__main__":
    unittest.main()
