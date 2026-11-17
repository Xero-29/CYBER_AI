import json
import os
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

    def test_env_file_with_group_or_world_read_permissions_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env_file = root / ".env"
            env_file.write_text("API_KEY=not-a-real-key\\n", encoding="utf-8")
            env_file.chmod(0o644)
            findings = preflight.validate_env_file_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("chmod 600", findings[0]["reason"])

    def test_env_file_with_group_write_permission_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env_file = root / ".env"
            env_file.write_text("API_KEY=not-a-real-key\\n", encoding="utf-8")
            env_file.chmod(0o660)
            findings = preflight.validate_env_file_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("grupo u otros", findings[0]["reason"])

    def test_env_file_with_owner_only_permissions_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env_file = root / ".env.local"
            env_file.write_text("API_KEY=not-a-real-key\\n", encoding="utf-8")
            env_file.chmod(0o600)
            findings = preflight.validate_env_file_permissions(root)
        self.assertEqual(findings, [])

    def test_env_example_is_excluded_from_permission_check(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env_file = root / ".env.example"
            env_file.write_text("API_KEY=\\n", encoding="utf-8")
            env_file.chmod(0o644)
            findings = preflight.validate_env_file_permissions(root)
        self.assertEqual(findings, [])

    def test_env_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "secrets"
            target.write_text("API_KEY=not-a-real-key\\n", encoding="utf-8")
            (root / ".env").symlink_to(target)
            findings = preflight.validate_env_file_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("enlace simbólico", findings[0]["reason"])

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


    def test_data_directory_requires_private_permissions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = root / "data"
            data.mkdir()
            data.chmod(0o755)
            findings = preflight.validate_data_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("chmod 700", findings[0]["reason"])

    def test_private_data_directory_and_nested_directory_are_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            nested = root / "data" / "nested"
            nested.mkdir(parents=True)
            (root / "data").chmod(0o700)
            nested.chmod(0o700)
            findings = preflight.validate_data_permissions(root)
        self.assertEqual(findings, [])

    def test_sensitive_local_key_file_rejects_group_or_world_access(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = root / "data"
            data.mkdir()
            data.chmod(0o700)
            key = data / "provider_private.key"
            key.write_text("fixture", encoding="utf-8")
            key.chmod(0o644)
            findings = preflight.validate_data_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("chmod 600", findings[0]["reason"])

    def test_evidence_directory_and_files_require_private_permissions(self):
        if os.name != "posix":
            self.skipTest("POSIX mode bits are not a Windows ACL check")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = root / "reports" / "tool_evidence"
            evidence.mkdir(parents=True)
            (evidence / "ruff.json").write_text('{"tool":"ruff"}', encoding="utf-8")
            evidence.chmod(0o755)
            (evidence / "ruff.json").chmod(0o644)
            findings = preflight.validate_evidence_permissions(root)
        self.assertEqual(len(findings), 2)
        self.assertTrue(any("chmod 700" in item["reason"] for item in findings))
        self.assertTrue(any("chmod 600" in item["reason"] for item in findings))

    def test_evidence_preflight_rejects_reports_path_that_is_a_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "reports").write_text("not a directory", encoding="utf-8")
            findings = preflight.validate_evidence_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("reports debe ser un directorio", findings[0]["reason"])

    def test_private_evidence_directory_and_file_are_accepted(self):
        if os.name != "posix":
            self.skipTest("POSIX mode bits are not a Windows ACL check")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = root / "reports" / "tool_evidence"
            evidence.mkdir(parents=True)
            (evidence / "ruff.json").write_text('{"tool":"ruff"}', encoding="utf-8")
            evidence.chmod(0o700)
            (evidence / "ruff.json").chmod(0o600)
            self.assertEqual(preflight.validate_evidence_permissions(root), [])

    def test_evidence_symlink_is_rejected(self):
        if os.name != "posix":
            self.skipTest("POSIX symlinks are not a Windows ACL check")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root / "outside"
            outside.mkdir()
            reports = root / "reports"
            reports.mkdir()
            (reports / "tool_evidence").symlink_to(outside, target_is_directory=True)
            findings = preflight.validate_evidence_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("enlaces simbólicos", findings[0]["reason"])

    def test_data_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root / "outside"
            outside.mkdir()
            (root / "data").symlink_to(outside, target_is_directory=True)
            findings = preflight.validate_data_permissions(root)
        self.assertEqual(len(findings), 1)
        self.assertIn("enlace simbólico", findings[0]["reason"])

if __name__ == "__main__":
    unittest.main()
