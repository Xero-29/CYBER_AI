import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch


class MetacognitionDirectorTests(unittest.TestCase):
    @patch("director.subprocess.run")
    @patch("director.run_cycle")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_failed_knowledge_assessment_blocks_original_task(
        self, load_config, select_agent, run_cycle, run_process
    ):
        load_config.return_value = {
            "metacognition": {
                "enabled": True, "researcher_agent": "INVESTIGADOR",
                "verifier_agent": "VERITAS", "max_rounds": 2,
            }
        }
        select_agent.return_value = (
            "NEXO", {"model": "principal", "type": "reasoning"}, [],
        )
        run_cycle.return_value = {"status": "verification_failed"}
        with patch.object(sys, "argv", ["director.py", "explicar un tema desconocido"]):
            from director import main
            self.assertEqual(main(), 2)
        run_cycle.assert_called_once()
        self.assertEqual(run_cycle.call_args.kwargs["principal"], "NEXO")
        self.assertEqual(run_cycle.call_args.kwargs["researcher"], "INVESTIGADOR")
        run_process.assert_not_called()

    @patch("director.subprocess.run")
    @patch("director.run_cycle")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_successful_assessment_then_runs_original_task(
        self, load_config, select_agent, run_cycle, run_process
    ):
        load_config.return_value = {
            "metacognition": {
                "enabled": True, "researcher_agent": "INVESTIGADOR",
                "verifier_agent": "VERITAS", "max_rounds": 2,
            }
        }
        select_agent.return_value = (
            "NEXO", {"model": "principal", "type": "reasoning"}, [],
        )
        run_cycle.return_value = {"status": "sufficient"}
        run_process.return_value = SimpleNamespace(returncode=0)
        with patch.object(sys, "argv", ["director.py", "explicar TCP"]):
            from director import main
            self.assertEqual(main(), 0)
        run_cycle.assert_called_once()
        run_process.assert_called_once()
        command = run_process.call_args.args[0]
        self.assertIn("agent_runner.py", command[1])
        self.assertIn("--task-text", command)

    @patch("director.subprocess.run")
    @patch("director.run_cycle")
    @patch("director.select_agent")
    @patch("director.load_config")
    def test_explicit_bypass_does_not_run_metacognition(
        self, load_config, select_agent, run_cycle, run_process
    ):
        load_config.return_value = {
            "metacognition": {"enabled": True},
        }
        select_agent.return_value = (
            "NEXO", {"model": "principal", "type": "reasoning"}, [],
        )
        run_process.return_value = SimpleNamespace(returncode=0)
        with patch.object(
            sys, "argv", ["director.py", "--no-metacognition", "explicar TCP"]
        ):
            from director import main
            self.assertEqual(main(), 0)
        run_cycle.assert_not_called()
        run_process.assert_called_once()


if __name__ == "__main__":
    unittest.main()
