"""Pruebas de validación del formato de las etapas."""

import unittest

from team_orchestrator import validate_step_output


class TestStepOutputValidation(unittest.TestCase):
    def setUp(self):
        self.step = {
            "agent": "VERITAS",
            "required_output_prefix": "VEREDICTO:",
            "required_output_sections": [
                "HALLAZGOS:",
                "OMISIONES:",
                "LIMITACIONES:",
            ],
        }

    def test_accepts_review_with_all_required_sections(self):
        response = (
            "VEREDICTO: REQUIERE_CORRECCION\\n"
            "HALLAZGOS: El comando tiene un error.\\n"
            "OMISIONES: Falta interpretar el resultado.\\n"
            "LIMITACIONES: No se inspeccionó un sistema real."
        )

        valid, errors = validate_step_output(response, self.step)

        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_rejects_response_without_required_prefix(self):
        response = (
            "Aquí tienes una respuesta.\\n"
            "HALLAZGOS: Ninguno identificado.\\n"
            "OMISIONES: Ninguna.\\n"
            "LIMITACIONES: No se inspeccionó un sistema real."
        )

        valid, errors = validate_step_output(response, self.step)

        self.assertFalse(valid)
        self.assertTrue(any("comenzar" in error for error in errors))

    def test_rejects_response_missing_required_section(self):
        response = (
            "VEREDICTO: SIN_ERRORES_IDENTIFICADOS\\n"
            "HALLAZGOS: Ninguno identificado.\\n"
            "OMISIONES: Ninguna."
        )

        valid, errors = validate_step_output(response, self.step)

        self.assertFalse(valid)
        self.assertTrue(any("LIMITACIONES:" in error for error in errors))

    def test_step_without_format_rules_is_accepted(self):
        valid, errors = validate_step_output(
            "Respuesta normal.",
            {"agent": "NEXO"},
        )

        self.assertTrue(valid)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
