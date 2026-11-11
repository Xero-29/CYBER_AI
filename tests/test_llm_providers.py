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


    def test_provider_can_be_switched_by_configuration_only(self):
        config = {
            "default_provider": "ollama",
            "llm_providers": {
                "ollama": {"enabled": True, "protocol": "ollama",
                           "base_url": "http://127.0.0.1:11434"},
                "gemini": {"enabled": True, "protocol": "gemini",
                           "base_url": "https://generativelanguage.googleapis.com/v1beta",
                           "requires_api_key": False,
                           "models": {"NEXO": "gemini-chat"}},
            },
        }
        agent = {"id": "nexo", "model": "qwen-local", "type": "reasoning"}
        local_provider = llm_providers.resolve_provider(config, agent)
        local_model = llm_providers.resolve_model(local_provider, agent, "NEXO")
        config["default_provider"] = "gemini"
        remote_provider = llm_providers.resolve_provider(config, agent)
        remote_model = llm_providers.resolve_model(remote_provider, agent, "NEXO")
        self.assertEqual((local_provider["name"], local_model), ("ollama", "qwen-local"))
        self.assertEqual((remote_provider["name"], remote_model), ("gemini", "gemini-chat"))
        self.assertEqual(agent["model"], "qwen-local")

class NativeProtocolTests(unittest.TestCase):
    def test_anthropic_chat_is_normalized(self):
        provider = {
            "name": "anthropic", "protocol": "anthropic",
            "base_url": "https://api.anthropic.com/v1",
            "api_key_env": "TEST_ANTHROPIC_KEY", "requires_api_key": True,
        }
        response = {"content": [{"type": "text", "text": "respuesta"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 7, "output_tokens": 4}}
        with patch.dict("os.environ", {"TEST_ANTHROPIC_KEY": "test-secret"}), \
             patch.object(llm_providers, "_http_json", return_value=response) as call:
            result = llm_providers.request(provider, "api/chat", {
                "model": "claude-test",
                "messages": [{"role": "system", "content": "Reglas"},
                             {"role": "system", "content": "Segunda regla"},
                             {"role": "user", "content": "Hola"}],
                "options": {"num_predict": 80},
            })
        self.assertEqual(result["message"]["content"], "respuesta")
        self.assertEqual(result["prompt_eval_count"], 7)
        self.assertEqual(call.call_args.args[0], "https://api.anthropic.com/v1/messages")
        self.assertEqual(call.call_args.args[1]["system"], "Reglas\\nSegunda regla")
        self.assertEqual(call.call_args.args[1]["max_tokens"], 80)
        self.assertEqual(call.call_args.args[2]["x-api-key"], "test-secret")

    def test_anthropic_embeddings_fail_explicitly(self):
        provider = {"name": "anthropic", "protocol": "anthropic",
                    "requires_api_key": False}
        with self.assertRaisesRegex(ValueError, "no ofrece embeddings"):
            llm_providers.request(provider, "api/embed", {"model": "m", "input": ["x"]})

    def test_gemini_chat_is_normalized(self):
        provider = {"name": "gemini", "protocol": "gemini",
                    "api_key_env": "TEST_GEMINI_KEY", "requires_api_key": True}
        response = {
            "candidates": [{"content": {"parts": [{"text": "hola"}]},
                            "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 2},
        }
        with patch.dict("os.environ", {"TEST_GEMINI_KEY": "gemini-secret"}), \
             patch.object(llm_providers, "_http_json", return_value=response) as call:
            result = llm_providers.request(provider, "api/chat", {
                "model": "gemini-test",
                "messages": [{"role": "system", "content": "Contexto"},
                             {"role": "assistant", "content": "previo"},
                             {"role": "user", "content": "Hola"}],
                "options": {"temperature": 0.2},
            })
        self.assertEqual(result["message"]["content"], "hola")
        self.assertEqual(result["eval_count"], 2)
        self.assertTrue(call.call_args.args[0].endswith("/models/gemini-test:generateContent"))
        body = call.call_args.args[1]
        self.assertEqual(body["systemInstruction"]["parts"][0]["text"], "Contexto")
        self.assertEqual(body["contents"][0]["role"], "model")
        self.assertEqual(call.call_args.args[2]["x-goog-api-key"], "gemini-secret")

    def test_gemini_embeddings_are_normalized(self):
        provider = {"name": "gemini", "protocol": "gemini",
                    "api_key_env": "TEST_GEMINI_KEY", "requires_api_key": True}
        with patch.dict("os.environ", {"TEST_GEMINI_KEY": "gemini-secret"}), \
             patch.object(llm_providers, "_http_json",
                          side_effect=[{"embedding": {"values": [0.1, 0.2]}},
                                       {"embedding": {"values": [0.3, 0.4]}}]) as call:
            result = llm_providers.request(provider, "api/embed", {
                "model": "embedding-test", "input": ["uno", "dos"]})
        self.assertEqual(result["embeddings"], [[0.1, 0.2], [0.3, 0.4]])
        self.assertEqual(call.call_count, 2)

    def test_remote_provider_does_not_claim_local_installed_models(self):
        self.assertIsNone(llm_providers.installed_models({
            "name": "gemini", "protocol": "gemini"}))

    def test_api_key_is_required_from_environment(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1",
                    "api_key_env": "CYBER_AI_TEST_MISSING_KEY",
                    "requires_api_key": True}
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "Falta configurar"):
                llm_providers.request(provider, "api/chat", {
                    "model": "m", "messages": [{"role": "user", "content": "x"}]})


    def test_unknown_protocol_is_rejected_during_resolution(self):
        config = {"llm_providers": {"custom": {
            "enabled": True, "protocol": "unknown", "base_url": "https://example.test"
        }}}
        with self.assertRaisesRegex(ValueError, "no soportado"):
            llm_providers.resolve_provider(config, {"provider": "custom"})

    def test_invalid_provider_base_url_is_rejected(self):
        config = {"llm_providers": {"cloud": {
            "enabled": True, "protocol": "openai", "base_url": "file:///tmp"
        }}}
        with self.assertRaisesRegex(ValueError, "base_url inválida"):
            llm_providers.resolve_provider(config, {"provider": "cloud"})

    def test_required_api_key_without_environment_name_is_rejected(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": True}
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "no declara api_key_env"):
                llm_providers.request(provider, "api/chat", {
                    "model": "m", "messages": [{"role": "user", "content": "x"}]})

if __name__ == "__main__":
    unittest.main()
