"""Pruebas de integración opcional del motor de experimentos."""

import unittest
from unittest.mock import patch

import team_orchestrator


class TestTeamOrchestratorExperiment(unittest.TestCase):
    def setUp(self):
        self.test_path = "tests/test_knowledge_library.py"
        self.hypothesis = "La biblioteca supera las pruebas seleccionadas."

    def base_args(self):
        return [
            "--workflow", "investigacion",
            "--experiment-test", self.test_path,
            "--experiment-hypothesis", self.hypothesis,
            "Tarea de integración",
        ]

    def test_dry_run_only_plans_experiment(self):
        planned = {"status": "planned", "executed": False}
        with (
            patch.object(team_orchestrator, "execute_workflow", return_value=0) as workflow,
            patch.object(team_orchestrator.experiment_engine, "run_experiment", return_value=planned) as runner,
        ):
            code = team_orchestrator.main(self.base_args() + ["--dry-run"])

        self.assertEqual(code, 0)
        workflow.assert_called_once_with(
            "Tarea de integración", "investigacion", dry_run=True
        )
        runner.assert_called_once_with(
            hypothesis=self.hypothesis,
            test_path=self.test_path,
            timeout=60,
            execute=False,
        )

    def test_failed_workflow_blocks_experiment(self):
        with (
            patch.object(team_orchestrator, "execute_workflow", return_value=1),
            patch.object(team_orchestrator.experiment_engine, "run_experiment") as runner,
        ):
            code = team_orchestrator.main(
                self.base_args() + ["--execute-experiment"]
            )

        self.assertEqual(code, 1)
        runner.assert_not_called()

    def test_existing_workflow_without_experiment_is_preserved(self):
        with (
            patch.object(team_orchestrator, "execute_workflow", return_value=0) as workflow,
            patch.object(team_orchestrator.experiment_engine, "run_experiment") as runner,
        ):
            code = team_orchestrator.main([
                "--workflow", "investigacion", "Tarea antigua"
            ])

        self.assertEqual(code, 0)
        workflow.assert_called_once_with(
            "Tarea antigua", "investigacion", dry_run=False
        )
        runner.assert_not_called()

    def test_execution_flag_is_forwarded_explicitly(self):
        with (
            patch.object(team_orchestrator, "execute_workflow", return_value=0),
            patch.object(
                team_orchestrator.experiment_engine,
                "run_experiment",
                return_value={"status": "passed", "executed": True},
            ) as runner,
        ):
            code = team_orchestrator.main(
                self.base_args() + ["--execute-experiment"]
            )

        self.assertEqual(code, 0)
        runner.assert_called_once_with(
            hypothesis=self.hypothesis,
            test_path=self.test_path,
            timeout=60,
            execute=True,
        )


if __name__ == "__main__":
    unittest.main()
