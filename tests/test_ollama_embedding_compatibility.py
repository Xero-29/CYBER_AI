import unittest
from unittest.mock import call, patch

import llm_providers


class OllamaEmbeddingCompatibilityTests(unittest.TestCase):
    provider = {
        "name": "ollama",
        "protocol": "ollama",
        "base_url": "http://127.0.0.1:11434",
    }


    def test_loopback_requests_bypass_environment_proxies(self):
        opener = llm_providers._opener_for_url(
            "http://127.0.0.1:11434/api/embeddings"
        )
        proxy_handlers = [
            handler for handler in opener.handlers
            if handler.__class__.__name__ == "ProxyHandler"
        ]
        self.assertEqual(len(proxy_handlers), 1)
        self.assertEqual(proxy_handlers[0].proxies, {})

    def test_localhost_requests_bypass_environment_proxies(self):
        opener = llm_providers._opener_for_url("http://localhost:11434/api/tags")
        proxy_handlers = [
            handler for handler in opener.handlers
            if handler.__class__.__name__ == "ProxyHandler"
        ]
        self.assertEqual(len(proxy_handlers), 1)
        self.assertEqual(proxy_handlers[0].proxies, {})

    def test_remote_provider_keeps_configured_opener(self):
        self.assertIs(
            llm_providers._opener_for_url("https://api.example.com/v1/embeddings"),
            llm_providers._HTTP_OPENER,
        )

    def test_model_catalog_uses_get_not_post(self):
        response = {"models": [{"name": "nomic-embed-text:latest"}]}
        with patch("llm_providers._http_json", return_value=response) as http:
            result = llm_providers.request(self.provider, "api/tags")

        self.assertEqual(result, response)
        http.assert_called_once_with(
            "http://127.0.0.1:11434/api/tags", None, timeout=600
        )

    def test_active_process_catalog_uses_get_not_post(self):
        response = {"models": []}
        with patch("llm_providers._http_json", return_value=response) as http:
            result = llm_providers.request(self.provider, "api/ps")

        self.assertEqual(result, response)
        http.assert_called_once_with(
            "http://127.0.0.1:11434/api/ps", None, timeout=600
        )

    def test_installed_models_reads_ollama_catalog(self):
        response = {"models": [{"name": "nomic-embed-text:latest"}]}
        with patch("llm_providers._http_json", return_value=response) as http:
            result = llm_providers.installed_models(self.provider)

        self.assertEqual(result, {"nomic-embed-text:latest"})
        http.assert_called_once_with(
            "http://127.0.0.1:11434/api/tags", None, timeout=600
        )

    def test_uses_modern_batch_endpoint_when_available(self):
        payload = {"model": "nomic-embed-text:latest", "input": ["uno", "dos"]}
        response = {"embeddings": [[0.1, 0.2], [0.3, 0.4]]}
        with patch("llm_providers._http_json", return_value=response) as http:
            result = llm_providers.request(self.provider, "api/embed", payload)

        self.assertEqual(result["embeddings"], response["embeddings"])
        http.assert_called_once_with(
            "http://127.0.0.1:11434/api/embed", payload, timeout=600
        )

    def test_falls_back_to_legacy_endpoint_on_404_or_405(self):
        payload = {
            "model": "nomic-embed-text:latest",
            "input": ["texto uno", "texto dos"],
            "keep_alive": 0,
        }
        legacy_vectors = [[0.1, 0.2], [0.3, 0.4]]
        with patch(
            "llm_providers._http_json",
            side_effect=[
                RuntimeError("Proveedor IA respondió HTTP 405: method not allowed"),
                {"embedding": legacy_vectors[0]},
                {"embedding": legacy_vectors[1]},
            ],
        ) as http:
            result = llm_providers.request(self.provider, "api/embed", payload)

        self.assertEqual(result["embeddings"], legacy_vectors)
        self.assertEqual(http.call_args_list, [
            call("http://127.0.0.1:11434/api/embed", payload, timeout=600),
            call("http://127.0.0.1:11434/api/embeddings",
                 {"model": payload["model"], "prompt": "texto uno", "keep_alive": 0},
                 timeout=600),
            call("http://127.0.0.1:11434/api/embeddings",
                 {"model": payload["model"], "prompt": "texto dos", "keep_alive": 0},
                 timeout=600),
        ])

    def test_does_not_hide_unrelated_provider_errors(self):
        payload = {"model": "nomic-embed-text:latest", "input": ["texto"]}
        with patch(
            "llm_providers._http_json",
            side_effect=RuntimeError("Proveedor IA respondió HTTP 500: internal error"),
        ) as http:
            with self.assertRaisesRegex(RuntimeError, "HTTP 500"):
                llm_providers.request(self.provider, "api/embed", payload)
        http.assert_called_once()


if __name__ == "__main__":
    unittest.main()
