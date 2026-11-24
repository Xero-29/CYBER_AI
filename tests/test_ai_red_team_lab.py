import unittest

from knowledge.deep_modules.ai_red_team.lab_runner import (
    _bounded_execution,
    _retrieve_for_tenant,
    _tool_allowed,
    _validate_structured_output,
    run_suite,
)


class AIRedTeamSyntheticHarnessTests(unittest.TestCase):
    def test_all_nine_cases_pass_without_model_or_network(self):
        report = run_suite()
        self.assertEqual(report["summary"], {
            "total": 9, "passed": 9, "failed": 0, "all_passed": True
        })
        self.assertFalse(report["model_execution"])
        self.assertFalse(report["network_access"])
        self.assertTrue(report["synthetic_only"])
        self.assertEqual(
            [item["id"] for item in report["results"]],
            [f"ART-{number:02d}" for number in range(1, 10)],
        )

    def test_tenant_filter_never_returns_other_tenant(self):
        docs = [
            {"id": "r", "tenant_id": "red"},
            {"id": "b", "tenant_id": "blue"},
        ]
        self.assertEqual(_retrieve_for_tenant("red", docs), [docs[0]])
        self.assertEqual(_retrieve_for_tenant("blue", docs), [docs[1]])

    def test_tool_broker_denies_unknown_tool_cross_owner_and_duplicate(self):
        args = {"resource_id": "CASE-001", "idempotency_key": "idem-1"}
        self.assertTrue(_tool_allowed("analyst", "create_ticket", "u1", "u1", args, set()))
        self.assertFalse(_tool_allowed("analyst", "send_message", "u1", "u1", args, set()))
        self.assertFalse(_tool_allowed("analyst", "create_ticket", "u2", "u1", args, set()))
        self.assertFalse(_tool_allowed("analyst", "create_ticket", "u1", "u1", args, {"idem-1"}))

    def test_structured_output_rejects_extra_fields_and_path_traversal(self):
        self.assertTrue(_validate_structured_output(
            '{"action":"read_record","record_id":"CASE-001"}'
        ))
        self.assertFalse(_validate_structured_output(
            '{"action":"read_record","record_id":"CASE-001","path":"../../etc/passwd"}'
        ))

    def test_budget_is_hard_bounded(self):
        result = _bounded_execution(1000, max_steps=7, max_calls=4, max_tokens=600)
        self.assertLessEqual(result["steps"], 7)
        self.assertLessEqual(result["calls"], 4)
        self.assertLessEqual(result["tokens"], 600)
        self.assertTrue(result["stopped"])


if __name__ == "__main__":
    unittest.main()
