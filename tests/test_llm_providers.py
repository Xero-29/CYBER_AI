import unittest
from urllib.error import HTTPError
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
        self.assertEqual(call.call_args.args[1]["system"], "Reglas\nSegunda regla")
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


    def test_installed_provider_plugin_can_be_selected_without_core_changes(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                if endpoint == "api/chat":
                    return {"message": {"content": "respuesta del plugin", "thinking": ""}}
                if endpoint == "api/embed":
                    return {"embeddings": [[1.0, 0.0] for _ in payload.get("input", [])]}
                if endpoint == "api/ps":
                    return {"models": []}
                raise ValueError("endpoint no soportado")
            def capabilities(self, provider):
                return ["chat", "embeddings"]
            def installed_models(self, provider):
                return {"remote-model"}

        config = {"llm_providers": {"custom": {
            "enabled": True, "protocol": "test_plugin",
            "requires_api_key": False,
        }}}
        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            provider = llm_providers.resolve_provider(config, {"provider": "custom"})
            self.assertEqual(
                llm_providers.request(provider, "api/chat", {"model": "m"}),
                {"message": {"content": "respuesta del plugin", "thinking": ""}},
            )
            self.assertEqual(
                llm_providers.provider_capabilities(provider), ["chat", "embeddings"]
            )
            self.assertEqual(
                llm_providers.request(provider, "api/embed", {"input": ["a"]}),
                {"embeddings": [[1.0, 0.0]]},
            )
            self.assertEqual(llm_providers.installed_models(provider), {"remote-model"})

    def test_plugin_invalid_embedding_contract_is_rejected(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                return {"embeddings": [[1.0, float("nan")]]}
            def capabilities(self, provider):
                return ["embeddings"]
        provider = {"name": "custom", "protocol": "test_plugin"}
        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            with self.assertRaisesRegex(RuntimeError, "vector inválido"):
                llm_providers.request(provider, "api/embed", {"input": ["x"]})

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


    def test_plugin_must_declare_capabilities(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                return {"message": {"content": "ok"}}
        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            with self.assertRaisesRegex(RuntimeError, "capabilities"):
                llm_providers.provider_capabilities({"name": "custom", "protocol": "custom"})

    def test_plugin_cannot_claim_unknown_capability(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                return {}
            def capabilities(self, provider):
                return ["shell_access"]
        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            with self.assertRaisesRegex(RuntimeError, "capacidades inválidas"):
                llm_providers.provider_capabilities({"name": "custom", "protocol": "custom"})

    def test_openai_compatible_does_not_claim_model_listing_without_adapter(self):
        self.assertEqual(
            llm_providers.provider_capabilities({"name": "openai", "protocol": "openai"}),
            ["chat", "embeddings"],
        )


    def test_capability_provider_is_selected_for_embeddings(self):
        config = {
            "default_provider": "anthropic",
            "capability_providers": {"embeddings": "gemini"},
            "llm_providers": {
                "anthropic": {"enabled": True, "protocol": "anthropic", "base_url": "https://api.anthropic.com"},
                "gemini": {"enabled": True, "protocol": "gemini", "base_url": "https://generativelanguage.googleapis.com"},
            },
        }
        provider = llm_providers.resolve_provider(config, {"type": "embeddings"}, capability="embeddings")
        self.assertEqual(provider["name"], "gemini")

    def test_explicit_agent_provider_has_priority_over_capability_mapping(self):
        config = {
            "default_provider": "anthropic",
            "capability_providers": {"chat": "gemini"},
            "llm_providers": {
                "anthropic": {"enabled": True, "protocol": "anthropic", "base_url": "https://api.anthropic.com"},
                "gemini": {"enabled": True, "protocol": "gemini", "base_url": "https://generativelanguage.googleapis.com"},
            },
        }
        provider = llm_providers.resolve_provider(config, {"provider": "anthropic"}, capability="chat")
        self.assertEqual(provider["name"], "anthropic")

    def test_explicit_fallback_provider_is_used_when_default_lacks_capability(self):
        config = {
            "default_provider": "anthropic",
            "fallback_providers": {"embeddings": ["gemini"]},
            "llm_providers": {
                "anthropic": {"enabled": True, "protocol": "anthropic"},
                "gemini": {"enabled": True, "protocol": "gemini"},
            },
        }
        provider = llm_providers.resolve_provider(config, {"type": "embeddings"}, capability="embeddings")
        self.assertEqual(provider["name"], "gemini")

    def test_missing_capability_provider_fails_explicitly(self):
        config = {
            "default_provider": "anthropic",
            "llm_providers": {"anthropic": {"enabled": True, "protocol": "anthropic"}},
        }
        with self.assertRaisesRegex(RuntimeError, "(?i)no hay proveedor habilitado"):
            llm_providers.resolve_provider(config, {"type": "embeddings"}, capability="embeddings")


    def test_builtin_provider_uses_safe_default_base_url(self):
        provider = llm_providers.resolve_provider(
            {"llm_providers": {"gemini": {"enabled": True, "protocol": "gemini"}}},
            {"provider": "gemini"},
            capability="embeddings",
        )
        self.assertEqual(
            provider["base_url"],
            "https://generativelanguage.googleapis.com/v1beta",
        )



class ProviderBoundaryValidationTests(unittest.TestCase):
    def test_timeout_must_be_finite_and_bounded(self):
        provider = {"name": "local", "protocol": "ollama",
                    "base_url": "http://127.0.0.1:11434"}
        for timeout in (0, -1, 601, float("inf"), float("nan"), True, "5", 10 ** 1000):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                llm_providers.request(provider, "api/chat", {}, timeout=timeout)

    def test_timeout_is_forwarded_to_builtin_transport(self):
        provider = {"name": "local", "protocol": "ollama",
                    "base_url": "http://127.0.0.1:11434"}
        with patch.object(llm_providers, "_http_json", return_value={"message": {"content": "ok"}}) as call:
            llm_providers.request(provider, "api/chat", {}, timeout=12.5)
        self.assertEqual(call.call_args.kwargs["timeout"], 12.5)

    def test_builtin_embedding_response_must_match_input_count(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": False}
        with patch.object(llm_providers, "_http_json", return_value={
            "data": [{"index": 0, "embedding": [0.1, 0.2]}]
        }):
            with self.assertRaisesRegex(RuntimeError, "número de embeddings"):
                llm_providers.request(provider, "api/embed", {
                    "model": "embed", "input": ["uno", "dos"]
                })

    def test_builtin_embedding_response_rejects_non_finite_values(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": False}
        with patch.object(llm_providers, "_http_json", return_value={
            "data": [{"index": 0, "embedding": [0.1, float("nan")]}]
        }):
            with self.assertRaisesRegex(RuntimeError, "vector inválido"):
                llm_providers.request(provider, "api/embed", {
                    "model": "embed", "input": ["uno"]
                })

    def test_invalid_usage_counters_are_rejected(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": False}
        with patch.object(llm_providers, "_http_json", return_value={
            "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10 ** 1000, "completion_tokens": 2},
        }):
            with self.assertRaisesRegex(RuntimeError, "contador inválido"):
                llm_providers.request(provider, "api/chat", {
                    "model": "m", "messages": [{"role": "user", "content": "hola"}]
                })


    def test_provider_request_payload_is_bounded_before_transport(self):
        provider = {"name": "custom", "protocol": "custom"}
        plugin = unittest.mock.Mock()
        plugin.capabilities.return_value = ["chat"]
        with patch.object(llm_providers, "_load_provider_plugin", return_value=plugin):
            with self.assertRaisesRegex(ValueError, "supera 8 MiB"):
                llm_providers.request(
                    provider,
                    "api/chat",
                    {"content": "x" * (llm_providers.MAX_PROVIDER_REQUEST_BYTES + 1)},
                )
        plugin.request.assert_not_called()

    def test_http_transport_bounds_response_bytes(self):
        class Response:
            requested = None
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, amount):
                self.requested = amount
                return b"x" * amount

        response = Response()
        with patch.object(llm_providers._HTTP_OPENER, "open", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "supera 16 MiB"):
                llm_providers._http_json("https://provider.example/v1/models")
        self.assertEqual(
            response.requested,
            llm_providers.MAX_PROVIDER_RESPONSE_BYTES + 1,
        )

    def test_http_error_body_read_is_bounded(self):
        class ErrorBody:
            requested = None
            def read(self, amount=-1):
                self.requested = amount
                return b"e" * amount

        body = ErrorBody()
        error = HTTPError(
            "https://provider.example/v1/chat",
            500,
            "failure",
            {},
            body,
        )
        with patch.object(llm_providers._HTTP_OPENER, "open", side_effect=error):
            with self.assertRaisesRegex(RuntimeError, "HTTP 500"):
                llm_providers._http_json("https://provider.example/v1/chat", {})
        self.assertEqual(body.requested, llm_providers.MAX_PROVIDER_ERROR_BYTES)

    def test_plugin_response_size_is_bounded(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                return {"message": {"content": "x" * (llm_providers.MAX_PROVIDER_RESPONSE_BYTES + 1)}}
            def capabilities(self, provider):
                return ["chat"]

        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            with self.assertRaisesRegex(RuntimeError, "límite de respuesta"):
                llm_providers.request(
                    {"name": "custom", "protocol": "custom"},
                    "api/chat",
                    {"model": "test"},
                )

    def test_invalid_api_key_environment_variable_name_is_rejected(self):
        provider = {
            "name": "cloud",
            "protocol": "openai",
            "base_url": "https://api.example/v1",
            "api_key_env": "INVALID\nENV",
            "requires_api_key": True,
        }
        with self.assertRaisesRegex(RuntimeError, "nombre de variable"):
            llm_providers.request(
                provider,
                "api/chat",
                {"model": "test", "messages": [{"role": "user", "content": "hi"}]},
            )


    def test_request_rejects_invalid_provider_payload_and_endpoint_shapes(self):
        with self.assertRaisesRegex(ValueError, "provider debe ser"):
            llm_providers.request([], "api/chat", {})
        provider = {"name": "local", "protocol": "ollama",
                    "base_url": "http://127.0.0.1:11434"}
        with self.assertRaisesRegex(ValueError, "payload debe ser"):
            llm_providers.request(provider, "api/chat", ["not", "an", "object"])
        with self.assertRaisesRegex(ValueError, "Endpoint de proveedor"):
            llm_providers.request(provider, "api/shell", {})


    def test_plugin_chat_rejects_non_string_thinking(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                return {"message": {"content": "ok", "thinking": 123}}
            def capabilities(self, provider):
                return ["chat"]

        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            with self.assertRaisesRegex(RuntimeError, "contrato de chat"):
                llm_providers.request(
                    {"name": "custom", "protocol": "custom"},
                    "api/chat",
                    {"model": "test"},
                )

    def test_plugin_model_catalog_requires_named_models(self):
        class Plugin:
            def request(self, provider, endpoint, payload, timeout):
                return {"models": [{"name": None}]}
            def capabilities(self, provider):
                return ["model_listing"]
            def installed_models(self, provider):
                return set()

        with patch.object(llm_providers, "_load_provider_plugin", return_value=Plugin()):
            with self.assertRaisesRegex(RuntimeError, "contrato de catálogo"):
                llm_providers.request(
                    {"name": "custom", "protocol": "custom"},
                    "api/ps",
                    {},
                )

if __name__ == "__main__":
    unittest.main()
