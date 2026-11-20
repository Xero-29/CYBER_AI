import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner


class AgentRunnerTransportTests(unittest.TestCase):
    def test_default_ollama_uses_shared_bounded_provider_transport(self):
        payload = {"model": "local-model", "messages": [{"role": "user", "content": "hola"}]}
        expected = {"message": {"content": "respuesta"}}
        with patch.object(agent_runner, "provider_request", return_value=expected) as request:
            result = agent_runner.request_json("api/chat", payload, timeout=17)

        self.assertEqual(result, expected)
        self.assertEqual(
            request.call_args.args,
            (
                {
                    "name": "ollama",
                    "protocol": "ollama",
                    "base_url": agent_runner.API,
                },
                "api/chat",
                payload,
                17,
            ),
        )

    def test_explicit_provider_is_passed_to_shared_transport_unchanged(self):
        provider = {
            "name": "gemini",
            "protocol": "gemini",
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
        }
        with patch.object(agent_runner, "provider_request", return_value={}) as request:
            agent_runner.request_json("api/tags", provider=provider)
        self.assertIs(request.call_args.args[0], provider)


class AgentRunnerPrivateHistoryTests(unittest.TestCase):
    def test_save_jsonl_redacts_secrets_and_creates_private_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data" / "agent_tasks.jsonl"
            secret = "agent-history-secret"
            agent_runner.save_jsonl(path, {
                "task": f"token={secret}",
                "api_key": secret,
                "safe": "visible",
            })
            stored = path.read_text(encoding="utf-8")
            self.assertNotIn(secret, stored)
            self.assertIn("token=[REDACTED]", stored)
            self.assertIn('"api_key": "[REDACTED]"', stored)
            if os.name == "posix":
                import stat
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

    def test_legacy_history_is_redacted_before_prompt_inclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data" / "agent_tasks.jsonl"
            path.parent.mkdir(mode=0o700)
            path.write_text(json.dumps({
                "agent": "NEXO",
                "task": "password=legacy-task-secret",
                "response": "token=legacy-response-secret",
            }) + "\n", encoding="utf-8")
            agent = {
                "context": {
                    "enabled": True,
                    "sources": ["recent_agent_tasks"],
                    "max_items": 4,
                    "max_chars_per_field": 700,
                }
            }
            with patch.object(agent_runner, "TASK_LOG", path):
                prompt = agent_runner.build_task_prompt(agent, "tarea actual")
            self.assertNotIn("legacy-task-secret", prompt)
            self.assertNotIn("legacy-response-secret", prompt)
            self.assertIn("password=[REDACTED]", prompt)
            self.assertIn("token=[REDACTED]", prompt)


class AgentRunnerRemoteEmbeddingTests(unittest.TestCase):
    def test_embed_text_sends_one_item_and_records_remote_provider(self):
        provider = {
            "name": "gemini",
            "protocol": "gemini",
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "requires_api_key": False,
        }
        agent = {"id": "eco", "type": "embeddings", "model": "local-embedding"}
        with tempfile.TemporaryDirectory() as directory:
            lock_path = Path(directory) / "agent.lock"
            with patch.object(agent_runner, "load_config", return_value={}), \
                 patch.object(agent_runner, "resolve_agent", return_value=("ECO", agent)), \
                 patch.object(agent_runner, "resolve_provider", return_value=provider), \
                 patch.object(agent_runner, "resolve_model", return_value="gemini-embed"), \
                 patch.object(agent_runner, "provider_models", return_value=None), \
                 patch.object(agent_runner, "LOCK_FILE", lock_path), \
                 patch.object(agent_runner, "request_json",
                              return_value={"embeddings": [[0.2, 0.8]]}) as request, \
                 patch.object(agent_runner, "save_jsonl") as save, \
                 patch.object(agent_runner, "record") as record, \
                 patch("builtins.print"):
                agent_runner.embed_text("ECO", "texto único")

        self.assertEqual(request.call_args.args[0], "api/embed")
        self.assertEqual(request.call_args.args[1]["input"], ["texto único"])
        self.assertEqual(request.call_args.kwargs["provider"], provider)
        event = save.call_args.args[1]
        self.assertEqual(event["provider"], "gemini")
        self.assertEqual(event["embedding_space"], "gemini::gemini-embed")
        record.assert_called_once_with(
            "ECO", "crear embedding: texto único",
            model="gemini-embed", provider="gemini")


if __name__ == "__main__":
    unittest.main()
