"""Pruebas de salida estructurada para las revisiones."""

import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import agent_runner
import team_orchestrator


class TestStructuredReviewOutput(unittest.TestCase):
    def test_regular_output_does_not_add_format(self):
        payload = {"model": "modelo", "messages": []}
        result = agent_runner.apply_review_output_schema(payload, False)

        self.assertNotIn("format", result)
        self.assertNotIn("format", payload)

    def test_review_output_adds_required_schema(self):
        payload = {"model": "modelo", "messages": []}
        result = agent_runner.apply_review_output_schema(payload, True)

        self.assertEqual(result["format"], agent_runner.REVIEW_OUTPUT_SCHEMA)
        self.assertEqual(
            set(result["format"]["required"]),
            {"status", "deviations", "evidence", "corrections"},
        )
        self.assertFalse(result["format"]["additionalProperties"])
        self.assertEqual(
            result["format"]["properties"]["evidence"]["minItems"], 1
        )

    def test_cli_forwards_review_json_flag(self):
        argv = [
            "agent_runner.py", "ask", "VERITAS",
            "--review-json", "--task-text", "Revisa esta respuesta.",
        ]
        with (
            patch.object(sys, "argv", argv),
            patch.object(agent_runner, "run_agent") as fake_run,
        ):
            agent_runner.main()

        self.assertTrue(fake_run.call_args.kwargs["structured_output"])

    def test_orchestrator_passes_structured_flag_to_subprocess(self):
        with (
            patch.object(
                team_orchestrator.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=0),
            ) as fake_run,
            patch.object(
                team_orchestrator,
                "latest_record_after",
                return_value={
                    "response": "{}",
                    "done_reason": "stop",
                },
            ),
        ):
            _, error = team_orchestrator._invoke_objective_agent(
                "VERITAS",
                "Revisa",
                "technical",
                800,
                review_json=True,
            )

        self.assertIsNone(error)
        command = fake_run.call_args.args[0]
        self.assertIn("--review-json", command)
        self.assertIn("--task-text", command)
        self.assertEqual(command[command.index("--task-text") + 1], "Revisa")


if __name__ == "__main__":
    unittest.main()
