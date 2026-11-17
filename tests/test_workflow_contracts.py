"""Contract tests shared by the live orchestrator and offline simulator."""
import json
import tempfile
import unittest
from pathlib import Path

from workflow_contracts import WorkflowContractError, validate_workflow_definition


class WorkflowContractTests(unittest.TestCase):
    def test_repository_workflow_catalog_satisfies_shared_contract(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads(
            (root / "config" / "workflows.json").read_text(encoding="utf-8")
        )
        self.assertEqual(catalog.get("version"), 1)
        self.assertIsInstance(catalog.get("workflows"), dict)
        for name, workflow in catalog["workflows"].items():
            with self.subTest(workflow=name):
                steps = validate_workflow_definition(workflow)
                self.assertEqual(len(steps), len(workflow["steps"]))

    def test_rejects_unknown_mode_types(self):
        for mode in ([], {}, None, 1):
            with self.subTest(mode=mode):
                with self.assertRaises(WorkflowContractError):
                    validate_workflow_definition({
                        "mode": mode,
                        "steps": [{"agent": "NEXO", "objective": "test"}],
                    })

    def test_rejects_non_positive_workflow_limits(self):
        for field in ("max_rounds", "max_steps", "max_context_chars"):
            with self.subTest(field=field):
                with self.assertRaises(WorkflowContractError):
                    validate_workflow_definition({
                        field: 0,
                        "steps": [{"agent": "NEXO", "objective": "test"}],
                    })

    def test_rejects_invalid_retry_and_token_budgets(self):
        cases = (
            {"max_retries": -1},
            {"max_retries": 3},
            {"num_predict": 99},
            {"num_predict": 2600},
            {"num_predict": 500, "max_num_predict": 400},
            {"max_num_predict": True},
        )
        for options in cases:
            with self.subTest(options=options):
                step = {"agent": "NEXO", "objective": "test", **options}
                with self.assertRaises(WorkflowContractError):
                    validate_workflow_definition({"steps": [step]})

    def test_rejects_invalid_knowledge_retrieval_options(self):
        cases = (
            {"knowledge_top_k": 0},
            {"knowledge_top_k": 6},
            {"knowledge_top_k": True},
            {"knowledge_min_score": -0.1},
            {"knowledge_min_score": 1.1},
            {"knowledge_min_score": float("nan")},
            {"knowledge_min_score": True},
        )
        for options in cases:
            with self.subTest(options=options):
                step = {"agent": "NEXO", "objective": "test", **options}
                with self.assertRaises(WorkflowContractError):
                    validate_workflow_definition({"steps": [step]})

    def test_rejects_non_boolean_feature_flags(self):
        for field in ("think", "use_knowledge"):
            with self.subTest(field=field):
                with self.assertRaises(WorkflowContractError):
                    validate_workflow_definition({
                        "steps": [{
                            "agent": "NEXO", "objective": "test", field: "yes"
                        }]
                    })

    def test_normalization_preserves_runtime_step_options(self):
        workflow = {
            "steps": [{
                "agent": " NEXO ",
                "objective": " Analizar ",
                "num_predict": 300,
                "custom_metadata": {"scope": "test"},
            }]
        }
        steps = validate_workflow_definition(workflow)
        self.assertEqual(steps[0]["agent"], "NEXO")
        self.assertEqual(steps[0]["objective"], "Analizar")
        self.assertEqual(steps[0]["num_predict"], 300)
        self.assertEqual(steps[0]["custom_metadata"], {"scope": "test"})
        self.assertEqual(steps[0]["required_output_sections"], [])


if __name__ == "__main__":
    unittest.main()
