import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import task_planner


class TaskPlannerFallbackTests(unittest.TestCase):
    @patch("task_planner.select_tools")
    @patch("task_planner.select_capabilities", side_effect=FileNotFoundError("missing inventory"))
    def test_missing_capability_inventory_produces_degraded_plan(
        self, select_capabilities, select_tools
    ):
        select_tools.return_value = {"candidates": [], "candidate_count": 0}
        with tempfile.TemporaryDirectory() as temp:
            plan, path = task_planner.create_plan(
                "review source", output_path=Path(temp) / "plan.json"
            )
            self.assertEqual(plan["candidate_count"], 0)
            self.assertTrue(plan["planning_warnings"])
            self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
