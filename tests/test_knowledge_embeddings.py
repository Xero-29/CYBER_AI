import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import knowledge_embeddings


class KnowledgeEmbeddingProviderTests(unittest.TestCase):
    def _run(self, protocol, provider_name, embedding_space):
        provider = {
            "name": provider_name,
            "protocol": protocol,
            "base_url": "https://api.example/v1" if protocol != "ollama" else "http://localhost:11434",
            "requires_api_key": False,
        }
        agent = {"id": "eco", "type": "embeddings", "model": "legacy-local"}
        with tempfile.TemporaryDirectory() as directory:
            lock_path = Path(directory) / "runner.lock"
            with patch.object(knowledge_embeddings, "LOCK_FILE", lock_path), \
                 patch.object(knowledge_embeddings, "load_config", return_value={"default_provider": provider_name}), \
                 patch.object(knowledge_embeddings, "resolve_agent", return_value=("ECO", agent)), \
                 patch.object(knowledge_embeddings, "resolve_provider", return_value=provider), \
                 patch.object(knowledge_embeddings, "resolve_model", return_value="selected-embedding-model"), \
                 patch.object(knowledge_embeddings, "provider_models", return_value=None), \
                 patch.object(knowledge_embeddings, "provider_request",
                              return_value={"embeddings": [[0.25, 0.75]]}) as request, \
                 patch.object(knowledge_embeddings, "unload_other_models") as unload:
                result = knowledge_embeddings.generate_embeddings(["texto de prueba"])
        self.assertEqual(result["model"], "selected-embedding-model")
        self.assertEqual(result["embedding_space"], embedding_space)
        self.assertEqual(result["embeddings"], [[0.25, 0.75]])
        self.assertEqual(request.call_args.args[0], provider)
        if protocol == "ollama":
            unload.assert_called_once_with("selected-embedding-model")
        else:
            unload.assert_not_called()

    def test_remote_embedding_provider_is_used(self):
        self._run("gemini", "gemini", "gemini::selected-embedding-model")

    def test_ollama_embedding_identifier_remains_backward_compatible(self):
        self._run("ollama", "ollama", "selected-embedding-model")



    def test_expected_embedding_space_is_resolved_without_provider_network_call(self):
        provider = {"name": "openai", "protocol": "openai"}
        agent = {"type": "embeddings"}
        with patch.object(knowledge_embeddings, "load_config", return_value={}), \
             patch.object(knowledge_embeddings, "resolve_agent", return_value=("ECO", agent)), \
             patch.object(knowledge_embeddings, "resolve_provider", return_value=provider), \
             patch.object(knowledge_embeddings, "provider_capabilities", return_value=["chat", "embeddings"]), \
             patch.object(knowledge_embeddings, "resolve_model", return_value="embed-v2"):
            self.assertEqual(
                knowledge_embeddings.expected_embedding_space(),
                "openai::embed-v2",
            )

    def test_expected_embedding_space_rejects_chat_only_provider(self):
        provider = {"name": "anthropic", "protocol": "anthropic"}
        with patch.object(knowledge_embeddings, "load_config", return_value={}), \
             patch.object(knowledge_embeddings, "resolve_agent", return_value=("ECO", {"type": "embeddings"})), \
             patch.object(knowledge_embeddings, "resolve_provider", return_value=provider), \
             patch.object(knowledge_embeddings, "provider_capabilities", return_value=["chat"]):
            with self.assertRaisesRegex(ValueError, "no ofrece embeddings"):
                knowledge_embeddings.expected_embedding_space()

if __name__ == "__main__":
    unittest.main()
