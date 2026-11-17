"""Prueba que una revisión inválida detiene el flujo."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import team_orchestrator as coordinator


class TestWorkflowValidation(unittest.TestCase):
    def test_completed_supervised_workflow_emits_independent_validator(self):
        report = {
            "status": "completed",
            "workflow": "reviewed",
            "objective_contract": {"global_objective": "test"},
            "steps": [{
                "agent": "NEXO",
                "objective_supervision": {
                    "status": "compliant",
                    "reviews": [{
                        "reviewer": "VERITAS",
                        "review": {
                            "status": "compliant",
                            "deviations": [],
                            "corrections": [],
                            "evidence": ["La respuesta cita el criterio original."],
                        },
                    }],
                },
            }],
        }
        validators = coordinator._objective_validator_results(report)
        self.assertEqual(len(validators), 1)
        self.assertTrue(validators[0]["passed"])
        self.assertTrue(validators[0]["independent"])
        self.assertEqual(validators[0]["reviewer"], "VERITAS")

    def test_self_review_cannot_be_marked_independent(self):
        report = {
            "steps": [{
                "agent": "VERITAS",
                "objective_supervision": {
                    "status": "compliant",
                    "reviews": [{
                        "reviewer": "VERITAS",
                        "review": {
                            "status": "compliant",
                            "deviations": [],
                            "evidence": ["Cita"],
                        },
                    }],
                },
            }],
        }
        validators = coordinator._objective_validator_results(report)
        self.assertEqual(len(validators), 1)
        self.assertFalse(validators[0]["passed"])
        self.assertFalse(validators[0]["independent"])

    def test_workflow_is_appended_to_execution_ledger(self):
        report = {
            "status": "completed",
            "workflow": "reviewed",
            "objective_contract": {"global_objective": "test"},
            "steps": [{
                "agent": "NEXO",
                "objective_supervision": {
                    "status": "compliant",
                    "reviews": [{
                        "reviewer": "VERITAS",
                        "review": {
                            "status": "compliant",
                            "deviations": [],
                            "corrections": [],
                            "evidence": ["Criterio validado."],
                        },
                    }],
                },
            }],
        }
        with patch.dict(os.environ, {"CYBER_AI_NAMESPACE": "forja"}), \
             patch.object(coordinator, "ExecutionLedger") as ledger:
            ledger.return_value.append.return_value = {"event_id": "ledger-event-1"}
            result = coordinator._record_workflow_ledger(report, "tarea supervisada", 12.5)
        self.assertEqual(result["event_id"], "ledger-event-1")
        args = ledger.return_value.append.call_args.kwargs
        self.assertEqual(args["namespace"], "forja")
        self.assertEqual(args["status"], "completed")
        self.assertTrue(args["validator_results"][0]["independent"])

    def test_invalid_veritas_review_stops_before_final_nexo(self):
        workflow = {
            "workflows": {
                "validation_test": {
                    "description": "Prueba aislada de validación",
                    "mode": "technical",
                    "max_rounds": 3,
                    "max_context_chars": 2000,
                    "steps": [
                        {
                            "agent": "NEXO",
                            "objective": "Generar un borrador.",
                        },
                        {
                            "agent": "VERITAS",
                            "objective": "Revisar el borrador.",
                            "required_output_prefix": "VEREDICTO:",
                            "required_output_sections": [
                                "HALLAZGOS:",
                                "OMISIONES:",
                                "LIMITACIONES:",
                            ],
                        },
                        {
                            "agent": "NEXO",
                            "objective": "Corregir el borrador.",
                        },
                    ],
                }
            }
        }

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflow_file = root / "workflows.json"
            task_log = root / "tasks.jsonl"
            report_dir = root / "reports"

            workflow_file.write_text(
                json.dumps(workflow), encoding="utf-8"
            )

            calls = []
            responses = {
                "NEXO": "Borrador técnico de prueba.",
                "VERITAS": (
                    "Aquí tienes algunas observaciones, "
                    "pero falta el formato de revisión."
                ),
            }

            def fake_run(command, cwd=None, timeout=None, check=None):
                agent = command[3]
                calls.append(agent)

                event = {
                    "agent": agent,
                    "model": "modelo-simulado",
                    "response": responses[agent],
                    "done_reason": "stop",
                }
                with task_log.open("a", encoding="utf-8") as file:
                    file.write(json.dumps(event) + "\n")

                return SimpleNamespace(returncode=0)

            fake_config = {
                "agents": {
                    "NEXO": {
                        "enabled": True,
                        "type": "reasoning",
                    },
                    "VERITAS": {
                        "enabled": True,
                        "type": "technical_verification",
                    },
                }
            }

            with (
                patch.object(
                    coordinator, "WORKFLOW_FILE", workflow_file
                ),
                patch.object(coordinator, "TASK_LOG", task_log),
                patch.object(coordinator, "REPORT_DIR", report_dir),
                patch.object(
                    coordinator, "load_config",
                    return_value=fake_config,
                ),
                patch.object(
                    coordinator.subprocess, "run",
                    side_effect=fake_run,
                ),
                patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(root / "ledger.sqlite3")}),
            ):
                result = coordinator.execute_workflow(
                    "Tarea de prueba", "validation_test"
                )

            # VERITAS falla el formato: NEXO no debe ejecutarse por segunda vez.
            self.assertEqual(result, 1)
            self.assertEqual(calls, ["NEXO", "VERITAS"])

            reports = list(report_dir.glob("team_*.json"))
            self.assertEqual(len(reports), 1)

            report = json.loads(
                reports[0].read_text(encoding="utf-8")
            )
            self.assertEqual(report["status"], "stopped_invalid_output")
            self.assertEqual(len(report["steps"]), 2)
            self.assertEqual(
                report["steps"][1]["status"],
                "stopped_invalid_output",
            )
            self.assertTrue(report["steps"][1]["validation_errors"])


    def test_knowledge_flags_are_limited_to_configured_steps(self):
        workflow = {
            "workflows": {
                "knowledge_test": {
                    "description": "Prueba aislada de memoria semántica",
                    "mode": "standard",
                    "max_rounds": 5,
                    "max_context_chars": 2000,
                    "steps": [
                        {
                            "agent": "NEXO",
                            "objective": "Primera etapa.",
                            "use_knowledge": True,
                            "knowledge_top_k": 3,
                            "knowledge_min_score": 0.40,
                        },
                        {
                            "agent": "FILTRO",
                            "objective": "Segunda etapa.",
                        },
                        {
                            "agent": "NEXO",
                            "objective": "Tercera etapa.",
                            "use_knowledge": True,
                            "knowledge_top_k": 3,
                            "knowledge_min_score": 0.40,
                        },
                        {
                            "agent": "VERITAS",
                            "objective": "Cuarta etapa.",
                        },
                        {
                            "agent": "FARO",
                            "objective": "Quinta etapa.",
                        },
                    ],
                }
            }
        }

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflow_file = root / "workflows.json"
            task_log = root / "tasks.jsonl"
            report_dir = root / "reports"
            workflow_file.write_text(
                json.dumps(workflow), encoding="utf-8"
            )

            commands = []
            responses = {
                "NEXO": "Respuesta simulada de NEXO.",
                "FILTRO": "Respuesta simulada de FILTRO.",
                "VERITAS": "Respuesta simulada de VERITAS.",
                "FARO": "Respuesta simulada de FARO.",
            }

            def fake_run(command, cwd=None, timeout=None, check=None):
                agent = command[3]
                commands.append((agent, list(command)))
                event = {
                    "agent": agent,
                    "model": "modelo-simulado",
                    "response": responses[agent],
                    "done_reason": "stop",
                }
                with task_log.open("a", encoding="utf-8") as file:
                    file.write(json.dumps(event) + "\n")
                return SimpleNamespace(returncode=0)

            fake_config = {
                "agents": {
                    name: {"enabled": True, "type": "reasoning"}
                    for name in ("NEXO", "FILTRO", "VERITAS", "FARO")
                }
            }

            with (
                patch.object(coordinator, "WORKFLOW_FILE", workflow_file),
                patch.object(coordinator, "TASK_LOG", task_log),
                patch.object(coordinator, "REPORT_DIR", report_dir),
                patch.object(
                    coordinator, "load_config", return_value=fake_config
                ),
                patch.object(
                    coordinator.subprocess, "run", side_effect=fake_run
                ),
                patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(root / "ledger.sqlite3")}),
            ):
                result = coordinator.execute_workflow(
                    "Prueba de argumentos", "knowledge_test"
                )

            self.assertEqual(result, 0)
            self.assertEqual(
                [agent for agent, _ in commands],
                ["NEXO", "FILTRO", "NEXO", "VERITAS", "FARO"],
            )

            nexo_commands = [
                command for agent, command in commands if agent == "NEXO"
            ]
            self.assertEqual(len(nexo_commands), 2)

            for command in nexo_commands:
                self.assertIn("--knowledge", command)
                self.assertIn("--knowledge-top-k", command)
                self.assertEqual(
                    command[command.index("--knowledge-top-k") + 1], "3"
                )
                self.assertIn("--knowledge-min-score", command)
                self.assertEqual(
                    command[command.index("--knowledge-min-score") + 1],
                    "0.4",
                )

            for agent, command in commands:
                if agent != "NEXO":
                    self.assertNotIn("--knowledge", command)


if __name__ == "__main__":
    unittest.main()
