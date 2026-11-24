import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from knowledge.deep_modules.ai_red_team.model_probe import (
    OpenAICompatibleChatClient,
    run_model_probes,
    validate_endpoint,
)


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length))
        self.server.requests.append(payload)
        if payload["messages"][-1]["content"] == "trigger-redirect":
            self.send_response(302)
            self.send_header("Location", "https://example.com/collect")
            self.end_headers()
            return
        body = json.dumps({
            "choices": [{"message": {"content": (
                ""
                if payload["model"] == "empty-model"
                else (
                    '{"action":"read_record","record_id":"CASE-001"}'
                    if "Return exactly" in payload["messages"][-1]["content"]
                    else "I cannot disclose synthetic confidential context."
                )
            )}}]
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


class AIRedTeamModelProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), _Handler)
        cls.server.requests = []
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.endpoint = f"http://127.0.0.1:{cls.server.server_port}/v1/chat/completions"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_loopback_endpoint_is_accepted_and_remote_http_is_rejected(self):
        self.assertEqual(validate_endpoint(self.endpoint), self.endpoint)
        with self.assertRaises(ValueError):
            validate_endpoint("http://example.com/v1/chat/completions")

    def test_endpoint_query_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_endpoint(self.endpoint + "?api_key=not-allowed")

    def test_http_redirect_is_not_followed(self):
        client = OpenAICompatibleChatClient(self.endpoint, "stub-model")
        with self.assertRaises(RuntimeError):
            client.complete([{"role": "user", "content": "trigger-redirect"}])

    def test_remote_requires_https_and_explicit_opt_in(self):
        with self.assertRaises(ValueError):
            validate_endpoint("https://example.com/v1/chat/completions")
        self.assertEqual(
            validate_endpoint("https://example.com/v1/chat/completions", allow_remote=True),
            "https://example.com/v1/chat/completions",
        )

    def test_client_sends_bounded_openai_compatible_request(self):
        client = OpenAICompatibleChatClient(self.endpoint, "stub-model")
        content, elapsed = client.complete(
            [{"role": "user", "content": "hello"}], max_tokens=64
        )
        self.assertEqual(content, "I cannot disclose synthetic confidential context.")
        self.assertGreaterEqual(elapsed, 0)
        self.assertEqual(self.server.requests[-1]["model"], "stub-model")
        self.assertEqual(self.server.requests[-1]["max_tokens"], 64)
        self.assertFalse(self.server.requests[-1]["stream"])

    def test_empty_model_responses_are_inconclusive_not_pass(self):
        client = OpenAICompatibleChatClient(self.endpoint, "empty-model")
        report = run_model_probes(client)
        self.assertEqual(
            [item["status"] for item in report["results"]],
            ["INCONCLUSIVE"] * 4,
        )
        self.assertEqual(report["summary"]["passed"], 0)
        self.assertEqual(report["summary"]["failed"], 0)
        self.assertEqual(report["summary"]["inconclusive"], 4)

    def test_live_probes_report_four_model_level_cases(self):
        client = OpenAICompatibleChatClient(self.endpoint, "stub-model")
        report = run_model_probes(client)
        self.assertEqual(
            [item["id"] for item in report["results"]],
            ["ART-01", "ART-02", "ART-06", "ART-07"],
        )
        self.assertTrue(report["model_execution"])
        self.assertFalse(report["tools_exposed"])
        self.assertEqual(report["summary"]["passed"], 4)
        self.assertEqual(report["summary"]["failed"], 0)


if __name__ == "__main__":
    unittest.main()
