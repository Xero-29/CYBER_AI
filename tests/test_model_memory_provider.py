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

    def test_record_redacts_secrets_and_creates_private_history(self):
        with tempfile.TemporaryDirectory() as directory:
            history = Path(directory) / "private" / "model_usage.jsonl"
            secret = "history-token-secret"
            with patch.object(model_memory_manager, "load_config", return_value={
                "agents": {"NEXO": {"id": "nexo", "model": "local-model"}}
            }), patch.object(model_memory_manager, "resolve_agent",
                             return_value=("NEXO", {"id": "nexo", "model": "local-model"})), \
                 patch.object(model_memory_manager, "HISTORY", history), \
                 patch.object(model_memory_manager, "api_get",
                              return_value={"models": [{"name": "local-model"}]}), \
                 patch.object(model_memory_manager, "read_history", return_value=[]), \
                 patch("builtins.print"):
                model_memory_manager.record("NEXO", f"token={secret}")

            stored = history.read_text(encoding="utf-8")
            self.assertNotIn(secret, stored)
            self.assertIn("token=[REDACTED]", stored)
            if os.name == "posix":
                import stat
                self.assertEqual(stat.S_IMODE(history.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(history.parent.stat().st_mode), 0o700)

    def test_read_history_rejects_symlink_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside.jsonl"
            outside.write_text('{"task":"private"}\\n', encoding="utf-8")
            history = root / "model_usage.jsonl"
            try:
                history.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with patch.object(model_memory_manager, "HISTORY", history):
                with self.assertRaisesRegex(ValueError, "archivo privado seguro"):
                    model_memory_manager.read_history()

    def test_api_get_uses_shared_bounded_ollama_transport(self):
        with patch.object(model_memory_manager, "provider_request", return_value={"models": []}) as request:
            result = model_memory_manager.api_get("api/tags")
        self.assertEqual(result, {"models": []})
        self.assertEqual(
            request.call_args.args,
            (
                {"name": "ollama", "protocol": "ollama", "base_url": model_memory_manager.OLLAMA_API},
                "api/tags",
            ),
        )
        self.assertEqual(request.call_args.kwargs, {"timeout": 5})

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
