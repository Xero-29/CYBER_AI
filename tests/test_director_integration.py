import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch


class DirectorIntegrationTests(unittest.TestCase):
    @patch("director.subprocess.run")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_knowledge_is_enabled_by_default(self, load_config, select_agent, run):
        load_config.return_value = {}
        select_agent.return_value = ("NEXO", {"model": "test-model", "type": "chat"}, [])
        run.return_value = SimpleNamespace(returncode=0)
        with patch.object(sys, "argv", ["director.py", "auditoría web"]):
            from director import main
            self.assertEqual(main(), 0)
        command = run.call_args.args[0]
        self.assertIn("--knowledge", command)
        self.assertIn("--task-text", command)
        self.assertEqual(command[command.index("--task-text") + 1], "auditoría web")

    @patch("director.subprocess.run")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_knowledge_can_be_disabled_explicitly(self, load_config, select_agent, run):
        load_config.return_value = {}
        select_agent.return_value = ("NEXO", {"model": "test-model", "type": "chat"}, [])
        run.return_value = SimpleNamespace(returncode=0)
        with patch.object(sys, "argv", ["director.py", "--no-knowledge", "consulta simple"]):
            from director import main
            self.assertEqual(main(), 0)
        self.assertNotIn("--knowledge", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
