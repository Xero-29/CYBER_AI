"""Pruebas del bucle de supervisión y corrección."""

import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import team_orchestrator
from objective_controller import create_objective_contract


def record(response):
    return {
        "response": response,
        "model": "modelo-de-prueba",
        "done_reason": "generation_finished",
    }


def review(status="compliant"):
    value = {
        "status": status,
        "deviations": [],
        "evidence": ["Evaluación de ejemplo."],
        "corrections": [],
    }
    if status == "requires_correction":
        value["deviations"] = [{
            "criterion": "Responder al objetivo global y al objetivo local.",
            "observed": "[OMISIÓN]",
            "why": "La respuesta debe abordar el objetivo local definido en el contrato.",
        }]
        value["corrections"] = ["Volver al objetivo original."]
    return json.dumps(value)


class TestObjectiveSupervisionIntegration(unittest.TestCase):
    def setUp(self):
        self.contract = create_objective_contract(
            "Investigar una hipótesis sin inventar resultados.",
            ["Responder al objetivo global y al objetivo local."],
            max_review_rounds=2,
        )
        self.config_patch = patch.object(
            team_orchestrator,
            "load_config",
            return_value={
                "agents": {
                    "VERITAS": {"enabled": True, "type": "chat"},
                    "FILTRO": {"enabled": True, "type": "chat"},
                }
            },
        )
        self.config_patch.start()
        self.addCleanup(self.config_patch.stop)

    def run_supervision(self, responses):
        with patch.object(
            team_orchestrator,
            "_invoke_objective_agent",
            side_effect=[(item, None) for item in responses],
        ) as invoke:
            result = team_orchestrator.supervise_step(
                agent="NEXO",
                stage_objective="Formular una hipótesis comprobable.",
                response="Respuesta inicial.",
                initial_record=record("Respuesta inicial."),
                task_prompt="TAREA ORIGINAL",
                contract=self.contract,
                mode="technical",
                token_budget=650,
                max_context_chars=6000,
            )
        return result, invoke

    def test_compliant_review_allows_continuation(self):
        result, invoke = self.run_supervision([
            record(review("compliant")),
        ])
        self.assertEqual(result["status"], "compliant")
        self.assertEqual(result["correction_rounds"], 0)
        invoke.assert_called_once()

    def test_deviation_is_corrected_and_rechecked(self):
        result, invoke = self.run_supervision([
            record(review("requires_correction")),
            record("Respuesta corregida y centrada en el objetivo."),
            record(review("compliant")),
        ])
        self.assertEqual(result["status"], "compliant")
        self.assertEqual(result["correction_rounds"], 1)
        self.assertEqual(
            result["response"],
            "Respuesta corregida y centrada en el objetivo.",
        )
        self.assertEqual(invoke.call_count, 3)

    def test_inconclusive_review_blocks_continuation(self):
        result, _ = self.run_supervision([
            record(review("inconclusive")),
        ])
        self.assertEqual(result["status"], "blocked")

    def test_invalid_review_blocks_if_format_repair_also_fails(self):
        result, invoke = self.run_supervision([
            record("No puedo verificar la respuesta."),
            record("Todavía falta el campo evidence."),
        ])
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(invoke.call_count, 2)
        self.assertEqual(
            result["reviews"][0]["status"],
            "invalid_review",
        )
        self.assertEqual(
            result["reviews"][1]["status"],
            "invalid_review_after_format_repair",
        )

    def test_missing_evidence_gets_one_format_repair(self):
        malformed = json.dumps({
            "status": "requires_correction",
            "deviations": [{
                "criterion": "Responder al objetivo global y al objetivo local.",
                "observed": "La respuesta cambia de tema.",
                "why": "La revisión debe cumplir el esquema obligatorio.",
            }],
            "corrections": ["Revisar la respuesta contra el objetivo original."],
        })
        result, invoke = self.run_supervision([
            record(malformed),
            record(review("compliant")),
        ])
        self.assertEqual(result["status"], "compliant")
        self.assertEqual(invoke.call_count, 2)
        self.assertTrue(
            any(item.get("status") == "format_normalized"
                for item in result["reviews"])
        )

    def test_contradictory_review_is_rechecked_once(self):
        self.contract = create_objective_contract(
            "Explica cómo verificar el controlador. "
            "No afirmes haber ejecutado comandos ni inspeccionado archivos.",
            ["Responder al objetivo original."],
            max_review_rounds=2,
        )
        conflicting = json.dumps({
            "status": "requires_correction",
            "deviations": [{
                "criterion": "Responder al objetivo original.",
                "observed": "Respuesta inicial.",
                "why": "La respuesta debe incluir pruebas ejecutadas.",
            }],
            "evidence": "La respuesta debe incluir pruebas ejecutadas.",
            "corrections": (
                "La respuesta debe incluir pruebas ejecutadas "
                "y resultados concretos."
            ),
        })

        result, invoke = self.run_supervision([
            record(conflicting),
            record(review("compliant")),
        ])

        self.assertEqual(result["status"], "compliant")
        self.assertEqual(invoke.call_count, 2)
        statuses = [
            item.get("status") for item in result["reviews"]
        ]
        self.assertIn("format_normalized", statuses)
        self.assertIn("contract_conflict", statuses)

    def test_persistent_contract_conflict_blocks_flow(self):
        self.contract = create_objective_contract(
            "Explica cómo verificar el controlador. "
            "No afirmes haber ejecutado comandos ni inspeccionado archivos.",
            ["Responder al objetivo original."],
            max_review_rounds=2,
        )
        conflicting = json.dumps({
            "status": "requires_correction",
            "deviations": [{
                "criterion": "Responder al objetivo original.",
                "observed": "Respuesta inicial.",
                "why": "La respuesta debe incluir pruebas ejecutadas.",
            }],
            "evidence": "La respuesta debe incluir pruebas ejecutadas.",
            "corrections": (
                "La respuesta debe incluir pruebas ejecutadas "
                "y resultados concretos."
            ),
        })

        result, invoke = self.run_supervision([
            record(conflicting),
            record(conflicting),
        ])

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(invoke.call_count, 2)
        self.assertIn("contradictoria", result["error"])

    def test_contract_conflict_is_audited_even_when_review_is_ungrounded(self):
        self.contract = create_objective_contract(
            "Explica cómo verificar el controlador. "
            "No afirmes haber ejecutado comandos ni inspeccionado archivos.",
            ["Responder al objetivo original."],
            max_review_rounds=2,
        )
        conflicting_and_ungrounded = json.dumps({
            "status": "requires_correction",
            "deviations": [{
                "criterion": "Un criterio inventado que no figura en el contrato.",
                "observed": "Una frase que no aparece literalmente en la respuesta.",
                "why": "La respuesta debe incluir pruebas ejecutadas.",
            }],
            "evidence": ["La revisión exige pruebas ejecutadas."],
            "corrections": [
                "La respuesta debe incluir pruebas ejecutadas y resultados concretos."
            ],
        })

        result, invoke = self.run_supervision([
            record(conflicting_and_ungrounded),
            record(review("compliant")),
        ])

        self.assertEqual(result["status"], "compliant")
        self.assertEqual(invoke.call_count, 2)

        statuses = [
            item.get("status") for item in result["reviews"]
        ]
        self.assertIn("contract_conflict", statuses)

        second_prompt = invoke.call_args_list[1].args[1]
        self.assertIn("AUDITORÍA DE TU REVISIÓN ANTERIOR", second_prompt)
        self.assertNotIn("REVISIÓN A CORREGIR", second_prompt)

    def test_ungrounded_review_gets_one_recheck(self):
        ungrounded = json.dumps({
            "status": "requires_correction",
            "deviations": [{
                "criterion": "El sistema debe demostrar seguridad absoluta.",
                "observed": "El modelo ejecutó pruebas de penetración.",
                "why": "Motivo no relacionado con la respuesta.",
            }],
            "evidence": ["La respuesta carece de evidencia."],
            "corrections": ["Revisar el objetivo original."],
        })
        result, invoke = self.run_supervision([
            record(ungrounded),
            record(review("compliant")),
        ])
        self.assertEqual(result["status"], "compliant")
        self.assertEqual(invoke.call_count, 2)
        self.assertEqual(
            result["reviews"][0]["status"], "ungrounded_review"
        )

    def test_second_agent_is_different_from_original_agent(self):
        result, invoke = self.run_supervision([
            record(review("compliant")),
        ])
        self.assertEqual(result["status"], "compliant")
        command = invoke.call_args.args
        self.assertEqual(command[0], "VERITAS")
        self.assertNotEqual(command[0], "NEXO")


if __name__ == "__main__":
    unittest.main()
