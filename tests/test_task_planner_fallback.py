import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import task_planner


class TaskPlannerFallbackTests(unittest.TestCase):
    @patch("task_planner.select_domain_capabilities", return_value={
        "matched_domain_count": 0, "domains": [], "skill_candidates": [],
    })
    @patch("task_planner.select_tools")
    @patch("task_planner.select_capabilities", side_effect=FileNotFoundError("missing inventory"))
    def test_missing_capability_inventory_produces_degraded_plan(
        self, select_capabilities, select_tools, select_domain_capabilities
    ):
        select_tools.return_value = {"candidates": [], "candidate_count": 0}
        with tempfile.TemporaryDirectory() as temp:
            plan, path = task_planner.create_plan(
                "review source", output_path=Path(temp) / "plan.json"
            )
            self.assertEqual(plan["candidate_count"], 0)
            self.assertTrue(plan["planning_warnings"])
            self.assertEqual(plan["domain_candidate_count"], 0)
            self.assertTrue(path.is_file())

    @patch("task_planner.select_domain_capabilities", return_value={
        "matched_domain_count": 1,
        "domains": [{
            "id": "network", "tool_candidates": [
                {"id": "tshark", "name": "PCAP", "available": False,
                 "adapter_registered": True, "adapter_status": "isolated_runner",
                 "execution_permitted": False}
            ]
        }],
        "skill_candidates": [{"skill_id": "skill-1", "name": "PCAP review"}],
    })
    @patch("task_planner.select_tools", return_value={"candidates": [], "candidate_count": 0})
    @patch("task_planner.select_capabilities", return_value=[])
    def test_plan_exposes_domain_tool_and_skill_links(
        self, select_capabilities, select_tools, select_domain_capabilities
    ):
        with tempfile.TemporaryDirectory() as temp:
            plan, _ = task_planner.create_plan(
                "análisis de red", output_path=Path(temp) / "plan.json"
            )
        self.assertEqual(plan["domain_candidate_count"], 1)
        self.assertEqual(plan["domain_tool_candidates"][0]["id"], "tshark")
        self.assertEqual(plan["domain_tool_candidates"][0]["source_domains"], ["network"])
        self.assertEqual(plan["skill_candidates"][0]["skill_id"], "skill-1")
        self.assertFalse(plan["tool_execution_started"])


if __name__ == "__main__":
    unittest.main()
