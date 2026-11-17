import unittest

from team_orchestrator import step_uses_knowledge


class TeamKnowledgePolicyTests(unittest.TestCase):
    def test_knowledge_defaults_to_enabled(self):
        self.assertTrue(step_uses_knowledge({}, {}))

    def test_workflow_default_can_be_overridden_by_step(self):
        self.assertFalse(
            step_uses_knowledge({"use_knowledge": False}, {"use_knowledge": True})
        )
        self.assertTrue(
            step_uses_knowledge({"use_knowledge": True}, {"use_knowledge": False})
        )

    def test_workflow_level_policy_is_respected(self):
        self.assertFalse(step_uses_knowledge({}, {"use_knowledge": False}))

    def test_non_boolean_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            step_uses_knowledge({"use_knowledge": "yes"}, {})


if __name__ == "__main__":
    unittest.main()
