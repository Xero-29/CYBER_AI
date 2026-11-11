import unittest
from unittest.mock import patch

from agent_core import CyberAIEngine


class AgentCoreTests(unittest.TestCase):
    def setUp(self):
        self.engine = CyberAIEngine()

    def test_translation_never_executes_http_request(self):
        with patch.object(self.engine, "action_check_headers") as action:
            result = self.engine.translate_and_execute("revisar cabeceras HTTP")
        self.assertEqual(result["status"], "approval_required")
        action.assert_not_called()

    def test_http_action_requires_explicit_authorization(self):
        result = self.engine.action_check_headers("https://example.com")
        self.assertEqual(result["status"], "authorization_required")

    def test_http_action_rejects_invalid_url(self):
        result = self.engine.action_check_headers("file:///etc/passwd", authorized=True)
        self.assertEqual(result["status"], "error")

    def test_local_file_inspection_rejects_path_traversal(self):
        result = self.engine.action_check_local_file("../../etc/passwd")
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
