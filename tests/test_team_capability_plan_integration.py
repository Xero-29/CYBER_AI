import unittest
from unittest.mock import patch

import team_orchestrator


class TeamCapabilityPlanIntegrationTests(unittest.TestCase):
    @patch("team_orchestrator.create_plan")
    @patch("team_orchestrator.load_workflow")
    def test_team_workflow_generates_capability_and_tool_plan(
        self, load_workflow, create_plan
    ):
        load_workflow.return_value = {
            "description": "test workflow",
            "steps": [{"agent": "NEXO", "objective": "analyze safely"}],
        }
        create_plan.return_value = (
            {
                "candidate_count": 2,
                "tool_candidate_count": 1,
                "steps": [{"template": "http/technologies/test.yaml"}],
                "tool_candidates": [{"id": "ruff"}],
            },
            "reports/team_runs/plan.json",
        )
        result = team_orchestrator.execute_workflow(
            "review application", "test", dry_run=True
        )
        self.assertEqual(result, 0)
        create_plan.assert_called_once()
        self.assertEqual(create_plan.call_args.args[0], "review application")
        self.assertIn("output_path", create_plan.call_args.kwargs)


if __name__ == "__main__":
    unittest.main()
