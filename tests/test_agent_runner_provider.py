import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner


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
