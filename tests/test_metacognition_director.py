import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch


class MetacognitionDirectorTests(unittest.TestCase):
    @patch("director.subprocess.run")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_failed_knowledge_assessment_blocks_original_task(self, load_config, select_agent, run):
        load_config.return_value = {
            "metacognition": {
                "enabled": True, "researcher_agent": "INVESTIGADOR",
                "verifier_agent": "VERITAS", "max_rounds": 2,
            }
        }
        select_agent.return_value = ("NEXO", {"model": "principal", "type": "reasoning"}, [])
        run.return_value = SimpleNamespace(returncode=2, stdout='{"status":"verification_failed"}', stderr="")
        with patch.object(sys, "argv", ["director.py", "explicar un tema desconocido"]):
            from director import main
            self.assertEqual(main(), 2)
        self.assertEqual(run.call_count, 1)
        command = run.call_args.args[0]
        self.assertIn("metacognition.py", command[1])
        self.assertIn("--researcher", command)
        self.assertIn("INVESTIGADOR", command)

    @patch("director.subprocess.run")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_successful_assessment_then_runs_original_task(self, load_config, select_agent, run):
        load_config.return_value = {
            "metacognition": {
                "enabled": True, "researcher_agent": "INVESTIGADOR",
                "verifier_agent": "VERITAS", "max_rounds": 2,
            }
        }
        select_agent.return_value = ("NEXO", {"model": "principal", "type": "reasoning"}, [])
        run.side_effect = [
            SimpleNamespace(returncode=0, stdout='{"status":"sufficient"}', stderr=""),
            SimpleNamespace(returncode=0, stdout="", stderr=""),
        ]
        with patch.object(sys, "argv", ["director.py", "explicar TCP"]):
            from director import main
            self.assertEqual(main(), 0)
        self.assertEqual(run.call_count, 2)
        self.assertIn("metacognition.py", run.call_args_list[0].args[0][1])
        self.assertIn("agent_runner.py", run.call_args_list[1].args[0][1])


if __name__ == "__main__":
    unittest.main()
