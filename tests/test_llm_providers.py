import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import llm_providers


def request_enabled(provider, *args, **kwargs):
    return llm_providers.request({**provider, "enabled": True}, *args, **kwargs)

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
   r=request_enabled(p,"api/chat",{"model":"m","messages":[{"role":"user","content":"hi"}],"options":{"num_predict":99}})
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
            result = request_enabled(provider, "api/chat", {
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
            request_enabled(provider, "api/embed", {"model": "m", "input": ["x"]})

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
            result = request_enabled(provider, "api/chat", {
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
            result = request_enabled(provider, "api/embed", {
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
                request_enabled(provider, "api/chat", {
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
                request_enabled(provider, "api/chat", {"model": "m"}),
                {"message": {"content": "respuesta del plugin", "thinking": ""}},
            )
            self.assertEqual(
                llm_providers.provider_capabilities(provider), ["chat", "embeddings"]
            )
            self.assertEqual(
                request_enabled(provider, "api/embed", {"input": ["a"]}),
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
                request_enabled(provider, "api/embed", {"input": ["x"]})

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
                request_enabled(provider, "api/chat", {
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
    def test_http_json_rejects_duplicate_keys_and_non_finite_numbers(self):
        invalid_bodies = (
            b'{"choices":[],"choices":[{"message":{"content":"shadow"}}]}',
            b'{"nested":{"score":1e999}}',
            b'{"nested":{"score":-1e-999}}',
            b'{"score":NaN}',
        )
        for body in invalid_bodies:
            with self.subTest(body=body):
                response = MagicMock()
                response.__enter__.return_value = response
                response.read.return_value = body
                with patch.object(llm_providers._HTTP_OPENER, "open", return_value=response):
                    with self.assertRaisesRegex(RuntimeError, "JSON UTF-8 válido"):
                        llm_providers._http_json("https://provider.example/v1/models")

    def test_http_json_rejects_oversized_request_before_network(self):
        with patch.object(llm_providers, "MAX_PROVIDER_REQUEST_BYTES", 32), \
             patch.object(llm_providers._HTTP_OPENER, "open") as open_call:
            with self.assertRaisesRegex(ValueError, "16 MiB"):
                llm_providers._http_json(
                    "https://provider.example/v1/chat",
                    {"prompt": "x" * 64},
                )
        open_call.assert_not_called()

    def test_http_json_rejects_unserializable_request_before_network(self):
        with patch.object(llm_providers._HTTP_OPENER, "open") as open_call:
            with self.assertRaisesRegex(ValueError, "JSON válido"):
                llm_providers._http_json(
                    "https://provider.example/v1/chat",
                    {"invalid": object()},
                )
        open_call.assert_not_called()

    def test_http_json_rejects_non_object_response(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b"[]"
        with patch.object(llm_providers._HTTP_OPENER, "open", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "no es un objeto"):
                llm_providers._http_json("https://provider.example/v1/models")

    def test_http_json_accepts_finite_exponent_values(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"score":-1.25e2}'
        with patch.object(llm_providers._HTTP_OPENER, "open", return_value=response):
            result = llm_providers._http_json("https://provider.example/v1/models")
        self.assertEqual(result, {"score": -125.0})

    def test_http_json_rejects_non_finite_request_values_before_network(self):
        with patch.object(llm_providers._HTTP_OPENER, "open") as open_call:
            with self.assertRaises(ValueError):
                llm_providers._http_json(
                    "https://provider.example/v1/chat",
                    {"temperature": float("nan")},
                )
        open_call.assert_not_called()

    def test_provider_base_url_rejects_whitespace_and_control_characters(self):
        for base_url in (
            "https://api.example/v1\n",
            "https://api.example /v1",
            "https://api.example/v1\t",
            "https://api.example/v1?",
            "https://api.example/v1#",
            "https://api.example%2f.evil/v1",
        ):
            config = {"llm_providers": {"cloud": {
                "enabled": True, "protocol": "openai", "base_url": base_url,
            }}}
            with self.subTest(base_url=repr(base_url)):
                with self.assertRaisesRegex(ValueError, "base_url inválida"):
                    llm_providers.resolve_provider(config, {"provider": "cloud"})

    def test_timeout_must_be_finite_and_bounded(self):
        provider = {"name": "local", "protocol": "ollama",
                    "base_url": "http://127.0.0.1:11434"}
        for timeout in (0, -1, 601, float("inf"), float("nan"), True, "5", 10 ** 1000):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                request_enabled(provider, "api/chat", {}, timeout=timeout)

    def test_direct_request_cannot_bypass_remote_http_transport_policy(self):
        provider = {
            "name": "untrusted-local-adapter",
            "protocol": "ollama",
            "base_url": "http://192.0.2.25:11434",
        }
        with patch.object(llm_providers, "_http_json") as transport:
            with self.assertRaisesRegex(ValueError, "HTTP solo se permite en loopback"):
                llm_providers.request(provider, "api/chat", {"model": "m", "messages": []})
        transport.assert_not_called()

    def test_direct_request_rejects_disabled_provider_before_transport(self):
        provider = {
            "name": "disabled-local",
            "protocol": "ollama",
            "base_url": "http://127.0.0.1:11434",
            "enabled": False,
        }
        with patch.object(llm_providers, "_http_json") as transport:
            with self.assertRaisesRegex(ValueError, "habilitado explícitamente"):
                request_enabled(provider, "api/chat", {"model": "m", "messages": []})
        transport.assert_not_called()

    def test_direct_ollama_request_uses_safe_loopback_default(self):
        provider = {"name": "local", "protocol": "ollama"}
        with patch.object(llm_providers, "_http_json", return_value={"message": {"content": "ok"}}) as transport:
            result = request_enabled(provider, "api/chat", {"model": "m", "messages": []})
        self.assertEqual(result["message"]["content"], "ok")
        self.assertEqual(transport.call_args.args[0], "http://127.0.0.1:11434/api/chat")

    def test_timeout_is_forwarded_to_builtin_transport(self):
        provider = {"name": "local", "protocol": "ollama",
                    "base_url": "http://127.0.0.1:11434"}
        with patch.object(llm_providers, "_http_json", return_value={"message": {"content": "ok"}}) as call:
            request_enabled(provider, "api/chat", {}, timeout=12.5)
        self.assertEqual(call.call_args.kwargs["timeout"], 12.5)

    def test_http_json_rejects_oversized_provider_response(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b"x" * (
            llm_providers.MAX_PROVIDER_RESPONSE_BYTES + 1
        )
        with patch.object(llm_providers._HTTP_OPENER, "open", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "16 MiB"):
                llm_providers._http_json("https://provider.example/v1/models")

    def test_http_error_body_is_not_echoed_to_logs(self):
        secret = "provider-secret-value"
        error = HTTPError(
            "https://provider.example/v1/chat/completions",
            401,
            "Unauthorized",
            {},
            BytesIO(json_bytes := ('{"api_key":"' + secret + '"}').encode("utf-8")),
        )
        with patch.object(llm_providers._HTTP_OPENER, "open", side_effect=error):
            with self.assertRaisesRegex(RuntimeError, "HTTP 401") as caught:
                llm_providers._http_json("https://provider.example/v1/chat/completions")
        self.assertNotIn(secret, str(caught.exception))
        self.assertNotIn(json_bytes.decode("utf-8"), str(caught.exception))
        self.assertTrue(error.fp.closed)

    def test_url_error_does_not_echo_provider_url_or_reason(self):
        with patch.object(
            llm_providers._HTTP_OPENER, "open",
            side_effect=URLError("sensitive-upstream-detail"),
        ):
            with self.assertRaisesRegex(RuntimeError, "No se pudo conectar") as caught:
                llm_providers._http_json("https://provider.example/v1/models")
        self.assertNotIn("sensitive-upstream-detail", str(caught.exception))

    def test_builtin_embedding_response_must_match_input_count(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": False}
        with patch.object(llm_providers, "_http_json", return_value={
            "data": [{"index": 0, "embedding": [0.1, 0.2]}]
        }):
            with self.assertRaisesRegex(RuntimeError, "número de embeddings"):
                request_enabled(provider, "api/embed", {
                    "model": "embed", "input": ["uno", "dos"]
                })

    def test_builtin_embedding_response_rejects_non_finite_values(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": False}
        with patch.object(llm_providers, "_http_json", return_value={
            "data": [{"index": 0, "embedding": [0.1, float("nan")]}]
        }):
            with self.assertRaisesRegex(RuntimeError, "vector inválido"):
                request_enabled(provider, "api/embed", {
                    "model": "embed", "input": ["uno"]
                })

    def test_invalid_usage_counters_are_rejected(self):
        provider = {"name": "cloud", "protocol": "openai",
                    "base_url": "https://api.example/v1", "requires_api_key": False}
        with patch.object(llm_providers, "_http_json", return_value={
            "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": -1, "completion_tokens": 2},
        }):
            with self.assertRaisesRegex(RuntimeError, "contador inválido"):
                request_enabled(provider, "api/chat", {
                    "model": "m", "messages": [{"role": "user", "content": "hola"}]
                })


    def test_provider_base_url_rejects_single_backslashes_and_encoded_separators(self):
        invalid_urls = (
            r"https://api.example\evil/v1",
            r"https://api.example/v1\..\admin",
            "https://api.example/v1%2f..%2fadmin",
            "https://api.example/v1%5c..%5cadmin",
            "https://api.example/v1/../admin",
            "https://api.example/v1//admin",
            "https://api.example:",
        )
        for base_url in invalid_urls:
            config = {"llm_providers": {"cloud": {
                "enabled": True, "protocol": "openai", "base_url": base_url,
            }}}
            with self.subTest(base_url=base_url):
                with self.assertRaisesRegex(ValueError, "base_url inválida"):
                    llm_providers.resolve_provider(config, {"provider": "cloud"})

    def test_request_rejects_unknown_endpoint_before_transport(self):
        provider = {
            "name": "local",
            "protocol": "ollama",
            "base_url": "http://127.0.0.1:11434",
        }
        with patch.object(llm_providers, "_http_json") as transport:
            with self.assertRaisesRegex(ValueError, "Endpoint de proveedor no admitido"):
                request_enabled(provider, "api/../admin", {})
        transport.assert_not_called()

    def test_api_tags_is_restricted_to_ollama_model_listing(self):
        provider = {
            "name": "cloud",
            "protocol": "openai",
            "base_url": "https://api.example/v1",
            "requires_api_key": False,
        }
        with patch.object(llm_providers, "_http_json") as transport:
            with self.assertRaisesRegex(ValueError, "api/tags solo está disponible para Ollama"):
                request_enabled(provider, "api/tags", {})
        transport.assert_not_called()

    def test_request_rejects_non_string_protocol_and_non_object_payload(self):
        with patch.object(llm_providers, "_http_json") as transport:
            with self.assertRaisesRegex(ValueError, "protocolo"):
                request_enabled({"protocol": ["ollama"]}, "api/chat", {})
            with self.assertRaisesRegex(ValueError, "payload"):
                request_enabled(
                    {"protocol": "ollama", "base_url": "http://127.0.0.1:11434"},
                    "api/chat",
                    ["not", "an", "object"],
                )
        transport.assert_not_called()

    def test_ollama_model_listing_endpoint_remains_available(self):
        provider = {
            "name": "local",
            "protocol": "ollama",
            "base_url": "http://127.0.0.1:11434",
        }
        with patch.object(llm_providers, "_http_json", return_value={"models": []}) as transport:
            result = request_enabled(provider, "api/tags")
        self.assertEqual(result, {"models": []})
        self.assertEqual(transport.call_args.args[0], "http://127.0.0.1:11434/api/tags")


    def test_ollama_model_listing_rejects_malformed_catalog_response(self):
        provider = {
            "name": "local",
            "protocol": "ollama",
            "base_url": "http://127.0.0.1:11434",
        }
        with patch.object(llm_providers, "_http_json", return_value={"models": "invalid"}):
            with self.assertRaisesRegex(RuntimeError, "contrato de catálogo"):
                request_enabled(provider, "api/tags")


    def test_resolve_provider_rejects_non_string_protocol(self):
        config = {
            "llm_providers": {
                "malformed": {"enabled": True, "protocol": ["ollama"]},
            },
        }
        with self.assertRaisesRegex(ValueError, "Protocolo de proveedor inválido"):
            llm_providers.resolve_provider(config, {"provider": "malformed"})


    def test_direct_request_requires_explicit_provider_enablement(self):
        provider = {
            "name": "local",
            "protocol": "ollama",
            "base_url": "http://127.0.0.1:11434",
        }
        with patch.object(llm_providers, "_http_json") as transport:
            with self.assertRaisesRegex(ValueError, "habilitado explícitamente"):
                llm_providers.request(provider, "api/chat", {})
        transport.assert_not_called()

    def test_resolve_provider_requires_boolean_true_enablement(self):
        for enabled in (1, "true", "yes", None):
            config = {
                "llm_providers": {
                    "cloud": {
                        "enabled": enabled,
                        "protocol": "openai",
                        "base_url": "https://api.example/v1",
                    },
                },
            }
            with self.subTest(enabled=enabled):
                with self.assertRaisesRegex(RuntimeError, "no configurado o deshabilitado"):
                    llm_providers.resolve_provider(config, {"provider": "cloud"})

    def test_resolve_provider_rejects_invalid_config_shapes_and_base_url_type(self):
        with self.assertRaisesRegex(ValueError, "configuración y el agente"):
            llm_providers.resolve_provider(None, {})
        with self.assertRaisesRegex(ValueError, "configuración y el agente"):
            llm_providers.resolve_provider({}, [])
        for base_url in (0, ""):
            config = {
                "llm_providers": {
                    "cloud": {
                        "enabled": True,
                        "protocol": "custom",
                        "base_url": base_url,
                    },
                },
            }
            with patch.object(llm_providers, "_load_provider_plugin") as loader:
                with self.subTest(base_url=base_url):
                    with self.assertRaisesRegex(ValueError, "base_url debe ser texto"):
                        llm_providers.resolve_provider(config, {"provider": "cloud"})
                loader.assert_not_called()


    def test_invalid_plugin_request_is_rejected_before_loading_plugin_code(self):
        provider = {"enabled": True, "name": "custom", "protocol": "custom"}
        with patch.object(llm_providers, "_load_provider_plugin") as loader:
            with self.assertRaisesRegex(ValueError, "Endpoint de proveedor no admitido"):
                llm_providers.request(provider, "api/../admin", {})
            with self.assertRaisesRegex(ValueError, "payload"):
                llm_providers.request(provider, "api/chat", ["invalid"])
        loader.assert_not_called()


    def test_plugin_base_url_is_validated_before_loading_plugin_code(self):
        provider = {
            "enabled": True,
            "name": "custom",
            "protocol": "custom",
            "base_url": "http://192.0.2.10:8080",
        }
        with patch.object(llm_providers, "_load_provider_plugin") as loader:
            with self.assertRaisesRegex(ValueError, "HTTP solo se permite en loopback"):
                llm_providers.request(provider, "api/chat", {})
        loader.assert_not_called()


    def test_resolve_provider_rejects_unsafe_plugin_base_url_before_import(self):
        config = {
            "llm_providers": {
                "custom": {
                    "enabled": True,
                    "protocol": "custom",
                    "base_url": "http://192.0.2.10:8080",
                },
            },
        }
        with patch.object(llm_providers, "_load_provider_plugin") as loader:
            with self.assertRaisesRegex(ValueError, "HTTP solo se permite en loopback"):
                llm_providers.resolve_provider(config, {"provider": "custom"})
        loader.assert_not_called()


if __name__ == "__main__":
    unittest.main()
