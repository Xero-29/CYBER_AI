import unittest
from unittest.mock import call, patch

import llm_providers


class OllamaEmbeddingCompatibilityTests(unittest.TestCase):
    provider = {
        "name": "ollama",
        "protocol": "ollama",
        "base_url": "http://127.0.0.1:11434",
    }

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
