import unittest
from unittest.mock import patch
import llm_providers

class ProviderTests(unittest.TestCase):
 def test_provider_config_requires_enabled(self):
  with self.assertRaises(RuntimeError):
   llm_providers.resolve_provider({"llm_providers":{"cloud":{"enabled":False}}},{"provider":"cloud"})
 def test_agent_can_override_default_provider(self):
  c={"default_provider":"ollama","llm_providers":{"ollama":{"enabled":True,"base_url":"http://localhost:11434"},"cloud":{"enabled":True,"protocol":"openai","base_url":"https://api.example/v1"}}}
  self.assertEqual(llm_providers.resolve_provider(c,{"provider":"cloud"})["name"],"cloud")
 def test_openai_chat_is_normalized_to_ollama_shape(self):
  p={"name":"cloud","protocol":"openai","base_url":"https://api.example/v1","requires_api_key":False}
  with patch.object(llm_providers,"_http_json",return_value={"choices":[{"message":{"content":"ok"},"finish_reason":"stop"}],"usage":{"prompt_tokens":2,"completion_tokens":3}}) as call:
   r=llm_providers.request(p,"api/chat",{"model":"m","messages":[{"role":"user","content":"hi"}],"options":{"num_predict":99}})
  self.assertEqual(r["message"]["content"],"ok")
  self.assertEqual(call.call_args.args[0],"https://api.example/v1/chat/completions")
  self.assertEqual(call.call_args.args[1]["max_tokens"],99)



class ResolveModelTests(unittest.TestCase):
    def test_provider_role_mapping_wins(self):
        provider = {"name": "cloud", "models": {"NEXO": "remote-reasoner"}}
        agent = {"id": "nexo", "model": "local-model", "type": "reasoning"}
        self.assertEqual(llm_providers.resolve_model(provider, agent, "NEXO"), "remote-reasoner")

    def test_agent_id_mapping_is_supported(self):
        provider = {"name": "cloud", "models": {"nexo": "remote-by-id"}}
        agent = {"id": "nexo", "model": "local-model"}
        self.assertEqual(llm_providers.resolve_model(provider, agent, "NEXO"), "remote-by-id")

    def test_embedding_model_has_own_setting(self):
        provider = {"name": "cloud", "embedding_model": "remote-embed"}
        agent = {"id": "eco", "model": "local-embed", "type": "embeddings"}
        self.assertEqual(llm_providers.resolve_model(provider, agent, "ECO"), "remote-embed")

    def test_role_mapping_precedes_embedding_default(self):
        provider = {"name": "cloud", "models": {"ECO": "role-embed"}, "embedding_model": "default-embed"}
        agent = {"id": "eco", "model": "local-embed", "type": "embeddings"}
        self.assertEqual(llm_providers.resolve_model(provider, agent, "ECO"), "role-embed")

    def test_provider_default_model_is_used(self):
        provider = {"name": "cloud", "default_model": "remote-default"}
        agent = {"id": "nexo", "model": "local-model"}
        self.assertEqual(llm_providers.resolve_model(provider, agent, "NEXO"), "remote-default")

    def test_local_model_is_fallback(self):
        provider = {"name": "ollama"}
        agent = {"id": "nexo", "model": "qwen-local"}
        self.assertEqual(llm_providers.resolve_model(provider, agent, "NEXO"), "qwen-local")

    def test_invalid_mapping_is_rejected(self):
        provider = {"name": "cloud", "models": []}
        with self.assertRaises(ValueError):
            llm_providers.resolve_model(provider, {"model": "local"}, "NEXO")

    def test_missing_model_is_rejected(self):
        with self.assertRaises(ValueError):
            llm_providers.resolve_model({"name": "cloud"}, {"id": "nexo"}, "NEXO")


if __name__ == "__main__":
    unittest.main()
