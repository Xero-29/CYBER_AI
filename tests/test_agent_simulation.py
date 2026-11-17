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



    def test_empty_falsy_fixture_mapping_is_rejected(self):
        for invalid in ([], "", 0, False):
            with self.subTest(invalid=invalid):
                with self.assertRaises(SimulationError):
                    simulate_workflow(self.workflow, "tarea", invalid)

    def test_empty_fixture_sequence_is_rejected(self):
        with self.assertRaises(SimulationError):
            simulate_workflow(self.workflow, "tarea", {"NEXO": []})

    def test_unknown_fixture_agent_is_rejected(self):
        with self.assertRaises(SimulationError):
            simulate_workflow(self.workflow, "tarea", {"AGENTE_INEXISTENTE": "texto"})

    def test_fixture_sequence_with_non_text_item_stops_at_output_contract(self):
        report = simulate_workflow(self.workflow, "tarea", {"NEXO": ["texto", None]})
        self.assertEqual(report["status"], "stopped_invalid_output")
        self.assertEqual(report["metrics"]["steps_executed"], 1)

    def test_unhashable_mode_is_rejected_as_contract_error(self):
        with self.assertRaises(SimulationError):
            validate_workflow_contract({
                "steps": [{"agent": "NEXO", "objective": "x", "mode": []}]
            })

    def test_invalid_workflow_limits_are_rejected(self):
        for field in ("max_rounds", "max_context_chars"):
            with self.subTest(field=field):
                with self.assertRaises(SimulationError):
                    validate_workflow_contract({
                        field: True,
                        "steps": [{"agent": "NEXO", "objective": "x"}],
                    })

    def test_task_size_limit_is_enforced(self):
        with self.assertRaises(SimulationError):
            simulate_workflow(self.workflow, "x" * 100_001)

    def test_context_handoff_respects_workflow_character_limit(self):
        workflow = {
            "name": "bounded",
            "max_context_chars": 250,
            "steps": [
                {"agent": "NEXO", "objective": "Generar borrador"},
                {"agent": "VERITAS", "objective": "Revisar borrador"},
            ],
        }
        fixtures = {
            "NEXO": "Borrador: " + ("x" * 1200),
        }
        report = simulate_workflow(workflow, "tarea", fixtures)
        second = report["steps"][1]
        self.assertEqual(second["input_context_steps"], 0)
        self.assertEqual(second["context_steps_dropped"], 1)
        self.assertLessEqual(second["input_context_chars"], 250)
        self.assertEqual(report["metrics"]["context_steps_dropped"], 1)

    def test_all_repository_workflows_load_and_simulate(self):
        from agent_simulation import load_workflow

        for name in ("investigacion", "critica_corta", "revision_tecnica"):
            with self.subTest(workflow=name):
                workflow = load_workflow(name)
                report = simulate_workflow(workflow, "Prueba sintética")
                self.assertEqual(report["status"], "completed")
                self.assertEqual(report["metrics"]["steps_total"], len(workflow["steps"]))
                self.assertEqual(report["metrics"]["steps_passed"], len(workflow["steps"]))

    def test_loader_rejects_path_like_workflow_ids(self):
        from agent_simulation import load_workflow

        with self.assertRaises(SimulationError):
            load_workflow("../README")

    def test_loader_rejects_invalid_catalog_roots(self):
        import json
        import tempfile
        from pathlib import Path
        from agent_simulation import load_workflow

        for payload in ([], {"version": 1, "workflows": []}, {"workflows": None}):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "workflows.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(SimulationError):
                    load_workflow("demo", path)

    def test_cli_writes_report_for_real_catalog_workflow(self):
        import json
        import tempfile
        from pathlib import Path
        from agent_simulation import main

        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "simulation.json"
            result = main([
                "--workflow", "investigacion",
                "--task", "Prueba CLI sin proveedor real",
                "--output", str(output),
            ])
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result, 0)
            self.assertEqual(report["status"], "completed")
            self.assertEqual(report["real_model_calls"], 0)
            self.assertEqual(report["real_tool_calls"], 0)

if __name__ == "__main__":
    unittest.main()
