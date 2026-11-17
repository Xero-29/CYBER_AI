"""Pruebas del simulador multiagente sin proveedores reales."""
import unittest

from agent_simulation import SimulationError, simulate_workflow, validate_workflow_contract


class TestAgentSimulation(unittest.TestCase):
    def setUp(self):
        self.workflow = {
            "name": "test",
            "mode": "technical",
            "steps": [
                {"agent": "NEXO", "objective": "Analizar", "required_output_prefix": "ANÁLISIS:", "required_output_sections": ["HALLAZGOS:"]},
                {"agent": "VERITAS", "objective": "Verificar", "required_output_prefix": "VEREDICTO:", "required_output_sections": ["EVIDENCIA:", "LIMITACIONES:"]},
            ],
        }

    def test_default_simulation_completes_without_real_calls(self):
        report = simulate_workflow(self.workflow, "Auditoría ficticia")
        self.assertEqual(report["status"], "completed")
        self.assertEqual(report["metrics"]["steps_passed"], 2)
        self.assertEqual(report["metrics"]["context_handoffs"], 1)
        self.assertEqual(report["steps"][1]["input_context"][0]["agent"], "NEXO")
        self.assertEqual(report["real_model_calls"], 0)
        self.assertEqual(report["real_tool_calls"], 0)
        self.assertFalse(report["network_access"])
        self.assertTrue(all(step["simulated"] for step in report["steps"]))

    def test_invalid_response_stops_following_steps(self):
        report = simulate_workflow(
            self.workflow,
            "Auditoría ficticia",
            {"NEXO": "Respuesta que incumple el contrato"},
        )
        self.assertEqual(report["status"], "stopped_invalid_output")
        self.assertEqual(report["metrics"]["steps_executed"], 1)
        self.assertEqual(report["metrics"]["steps_failed"], 1)

    def test_agent_response_sequences_are_supported_without_mutation(self):
        fixtures = {
            "NEXO": ["ANÁLISIS: correcto\\nHALLAZGOS: ninguno"],
            "VERITAS": ["VEREDICTO: conforme\\nEVIDENCIA: sintética\\nLIMITACIONES: simulación"],
        }
        report = simulate_workflow(self.workflow, "Auditoría ficticia", fixtures)
        self.assertEqual(report["status"], "completed")
        self.assertEqual(len(fixtures["NEXO"]), 1)

    def test_empty_task_is_rejected(self):
        with self.assertRaises(SimulationError):
            simulate_workflow(self.workflow, " ")

    def test_empty_workflow_is_rejected(self):
        with self.assertRaises(SimulationError):
            validate_workflow_contract({"steps": []})

    def test_missing_agent_or_objective_is_rejected(self):
        with self.assertRaises(SimulationError):
            validate_workflow_contract({"steps": [{"objective": "sin agente"}]})
        with self.assertRaises(SimulationError):
            validate_workflow_contract({"steps": [{"agent": "NEXO"}]})

    def test_invalid_mode_is_rejected(self):
        with self.assertRaises(SimulationError):
            validate_workflow_contract({
                "steps": [{"agent": "NEXO", "objective": "x", "mode": "unsafe"}]
            })

    def test_non_text_response_fails_closed(self):
        report = simulate_workflow(
            self.workflow, "Auditoría ficticia", {"NEXO": {"unexpected": "object"}}
        )
        self.assertEqual(report["status"], "stopped_invalid_output")
        self.assertTrue(report["steps"][0]["validation_errors"])


if __name__ == "__main__":
    unittest.main()
