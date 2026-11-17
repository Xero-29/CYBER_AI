import json
import tempfile
import unittest
from pathlib import Path

import preflight


class PreflightTests(unittest.TestCase):
    def make_project(self, root):
        for relative in preflight.REQUIRED_FILES:
            path = root / relative
            if relative.endswith(".json"):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")
            elif relative == "tests":
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# fixture\n", encoding="utf-8")

    def test_ready_without_optional_tools_or_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            report = preflight.collect_checks(
                root=root,
                python_version=(3, 12, 0),
                module_lookup=lambda name: object() if name in preflight.REQUIRED_MODULES else None,
                executable_lookup=lambda name: None,
                environ={},
            )
        self.assertEqual(report["status"], "ready")
        self.assertGreater(report["warnings"], 0)
        self.assertFalse(report["network_accessed"])
        self.assertFalse(report["services_started"])

    def test_old_python_blocks_readiness(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            report = preflight.collect_checks(
                root=root,
                python_version=(3, 11, 9),
                module_lookup=lambda name: object(),
                executable_lookup=lambda name: None,
                environ={},
            )
        self.assertEqual(report["status"], "blocked")
        self.assertGreater(report["errors"], 0)



    def test_provider_routing_uses_explicit_embedding_capability_without_network(self):
        config = {
            "default_provider": "anthropic",
            "capability_providers": {"embeddings": "gemini"},
            "llm_providers": {
                "anthropic": {"enabled": True, "protocol": "anthropic"},
                "gemini": {"enabled": True, "protocol": "gemini"},
            },
            "agents": {"ECO": {"type": "embeddings"}},
        }
        checks = preflight.validate_provider_routes(config, environ={})
        self.assertEqual(checks[0]["status"], "ok")
        self.assertIn("gemini ofrece embeddings", checks[0]["detail"])

    def test_provider_routing_warns_when_remote_key_is_missing(self):
        config = {
            "default_provider": "openai",
            "llm_providers": {"openai": {
                "enabled": True, "protocol": "openai",
                "requires_api_key": True, "api_key_env": "CYBER_AI_TEST_KEY",
            }},
            "agents": {"NEXO": {"type": "chat"}},
        }
        checks = preflight.validate_provider_routes(config, environ={})
        self.assertEqual(checks[0]["status"], "warning")
        self.assertIn("falta la variable", checks[0]["detail"])

    def test_provider_routing_blocks_chat_only_provider_for_embeddings(self):
        config = {
            "default_provider": "anthropic",
            "llm_providers": {"anthropic": {
                "enabled": True, "protocol": "anthropic",
            }},
            "agents": {"ECO": {"type": "embeddings"}},
        }
        checks = preflight.validate_provider_routes(config, environ={})
        self.assertEqual(checks[0]["status"], "error")

    def test_secret_hygiene_rejects_literal_api_key(self):
        findings = preflight.validate_secret_hygiene({
            "llm_providers": {"remote": {"api_key": "hard-coded-secret"}}
        })
        self.assertEqual(len(findings), 1)
        self.assertIn("api_key", findings[0]["path"])

    def test_secret_hygiene_accepts_environment_variable_reference(self):
        findings = preflight.validate_secret_hygiene({
            "llm_providers": {"remote": {
                "api_key_env": "CYBER_AI_TEST_API_KEY",
                "requires_api_key": True,
            }}
        })
        self.assertEqual(findings, [])

    def test_secret_hygiene_rejects_malformed_environment_variable_name(self):
        findings = preflight.validate_secret_hygiene({
            "llm_providers": {"remote": {"api_key_env": "not-a-valid-name"}}
        })
        self.assertEqual(len(findings), 1)

    def test_preflight_blocks_project_config_with_embedded_secret(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            (root / "config/model_roles.json").write_text(
                json.dumps({"llm_providers": {"remote": {
                    "api_key": "embedded-secret"
                }}}),
                encoding="utf-8",
            )
            report = preflight.collect_checks(
                root=root,
                python_version=(3, 12, 0),
                module_lookup=lambda name: object(),
                executable_lookup=lambda name: None,
                environ={},
            )
        self.assertEqual(report["status"], "blocked")
        self.assertTrue(any(
            item["name"] == "secret_hygiene" and item["status"] == "error"
            for item in report["checks"]
        ))

    def test_custom_provider_is_reported_without_importing_plugin(self):
        config = {
            "default_provider": "custom",
            "llm_providers": {"custom": {
                "enabled": True, "protocol": "custom_protocol",
            }},
            "agents": {"NEXO": {"type": "chat"}},
        }
        checks = preflight.validate_provider_routes(
            config, environ={}, plugin_protocols={"custom_protocol"}
        )
        self.assertEqual(checks[0]["status"], "warning")
        self.assertIn("se validan al cargarlo", checks[0]["detail"])

if __name__ == "__main__":
    unittest.main()
