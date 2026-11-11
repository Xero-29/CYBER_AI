import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import model_memory_manager


class ProviderUsageHistoryTests(unittest.TestCase):
    def test_remote_provider_record_does_not_query_ollama(self):
        with tempfile.TemporaryDirectory() as directory:
            history = Path(directory) / "model_usage.jsonl"
            with patch.object(model_memory_manager, "load_config", return_value={
                "agents": {"NEXO": {"id": "nexo", "model": "local-model"}}
            }), patch.object(model_memory_manager, "resolve_agent",
                             return_value=("NEXO", {"id": "nexo", "model": "local-model"})), \
                 patch.object(model_memory_manager, "HISTORY", history), \
                 patch.object(model_memory_manager, "api_get") as api_get, \
                 patch.object(model_memory_manager, "read_history", return_value=[]), \
                 patch("builtins.print"):
                model_memory_manager.record(
                    "NEXO", "task", model="remote-reasoner", provider="gemini")
            api_get.assert_not_called()
            event = json.loads(history.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(event["provider"], "gemini")
            self.assertEqual(event["model"], "remote-reasoner")

    def test_ollama_record_still_checks_installed_model(self):
        with tempfile.TemporaryDirectory() as directory:
            history = Path(directory) / "model_usage.jsonl"
            with patch.object(model_memory_manager, "load_config", return_value={
                "agents": {"NEXO": {"id": "nexo", "model": "local-model"}}
            }), patch.object(model_memory_manager, "resolve_agent",
                             return_value=("NEXO", {"id": "nexo", "model": "local-model"})), \
                 patch.object(model_memory_manager, "api_get",
                              return_value={"models": [{"name": "local-model"}]}) as api_get, \
                 patch.object(model_memory_manager, "read_history", return_value=[]), \
                 patch.object(model_memory_manager, "HISTORY", history), \
                 patch("builtins.print"):
                model_memory_manager.record("NEXO", "task")
            api_get.assert_called_once_with("api/tags")
            event = json.loads(history.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(event["provider"], "ollama")
            self.assertEqual(event["model"], "local-model")


if __name__ == "__main__":
    unittest.main()
