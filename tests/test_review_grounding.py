"""Pruebas de trazabilidad entre criterios, citas y hallazgos."""

import unittest

from objective_controller import (
    create_objective_contract,
    parse_review,
    validate_review_grounding,
)


class TestReviewGrounding(unittest.TestCase):
    def setUp(self):
        self.contract = create_objective_contract(
            "Explicar cómo verificar el controlador.",
            [
                "Responder al objetivo original.",
                "No afirmar pruebas que no se ejecutaron.",
            ],
        )
        self.response = (
            "Para verificar el controlador, ejecutaría las pruebas "
            "automatizadas y revisaría sus resultados. No he ejecutado "
            "esas pruebas en esta respuesta."
        )

    def make_review(self, criterion, observed):
        return parse_review(
            __import__("json").dumps({
                "status": "requires_correction",
                "deviations": [{
                    "criterion": criterion,
                    "observed": observed,
                    "why": "Motivo de prueba.",
                }],
                "evidence": ["Evaluación de prueba."],
                "corrections": ["Revisar la respuesta."],
            })
        )

    def test_accepts_original_criterion_and_exact_quote(self):
        review = self.make_review(
            "No afirmar pruebas que no se ejecutaron.",
            "No he ejecutado esas pruebas en esta respuesta.",
        )
        errors = validate_review_grounding(
            review, self.contract, self.response
        )
        self.assertEqual(errors, [])

    def test_rejects_invented_criterion(self):
        review = self.make_review(
            "El sistema debe confirmar una vulnerabilidad.",
            "No he ejecutado esas pruebas en esta respuesta.",
        )
        errors = validate_review_grounding(
            review, self.contract, self.response
        )
        self.assertTrue(any("criterio" in error for error in errors))

    def test_rejects_quote_not_present_in_response(self):
        review = self.make_review(
            "Responder al objetivo original.",
            "El modelo ejecutó pruebas de penetración.",
        )
        errors = validate_review_grounding(
            review, self.contract, self.response
        )
        self.assertTrue(any("no aparece literalmente" in error for error in errors))

    def test_allows_explicit_omission_marker(self):
        review = self.make_review(
            "Responder al objetivo original.",
            "[OMISIÓN]",
        )
        errors = validate_review_grounding(
            review, self.contract, self.response
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
