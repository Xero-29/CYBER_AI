"""Pruebas contra críticas que contradicen el objetivo original."""

import unittest

from objective_controller import (
    create_objective_contract,
    find_review_contract_conflicts,
    parse_review,
)


class TestObjectiveReviewGuard(unittest.TestCase):
    def setUp(self):
        self.contract = create_objective_contract(
            global_objective=(
                "Explica cómo verificar el controlador. "
                "No afirmes haber ejecutado comandos ni inspeccionado archivos."
            ),
            acceptance_criteria=[
                "La respuesta explica cómo verificar el controlador."
            ],
        )

    def make_review(self, correction, evidence="La respuesta carece de datos."):
        return parse_review(
            __import__("json").dumps({
                "status": "requires_correction",
                "deviations": [{
                    "criterion": "Cumplir el objetivo",
                    "observed": "No hay resultados de pruebas.",
                    "why": "Se exige evidencia ejecutada.",
                }],
                "evidence": evidence,
                "corrections": [correction],
            })
        )

    def test_detects_demand_for_tests_that_were_not_requested(self):
        review = self.make_review(
            "La respuesta debe incluir pruebas ejecutadas y resultados concretos."
        )
        conflicts = find_review_contract_conflicts(review, self.contract)
        self.assertTrue(conflicts)

    def test_detects_exact_paraphrase_from_failed_run(self):
        review = self.make_review(
            "La respuesta debe incluir evidencia de pruebas ejecutadas "
            "y resultados observados para validar las capacidades."
        )
        conflicts = find_review_contract_conflicts(review, self.contract)
        self.assertTrue(conflicts)

    def test_detects_request_for_real_results_from_failed_run(self):
        review = self.make_review(
            "Asegúrese de que las acciones descritas en la respuesta se hayan "
            "realizado en un entorno real y proporcione resultados reales "
            "de las pruebas ejecutadas."
        )
        conflicts = find_review_contract_conflicts(review, self.contract)
        self.assertTrue(conflicts)

    def test_does_not_reject_a_methodology_correction(self):
        review = self.make_review(
            "Explicar cómo ejecutar las pruebas y cómo interpretar los resultados."
        )
        conflicts = find_review_contract_conflicts(review, self.contract)
        self.assertEqual(conflicts, [])

    def test_does_not_flag_a_compliant_review(self):
        review = parse_review(
            __import__("json").dumps({
                "status": "compliant",
                "deviations": [],
                "evidence": ["La respuesta explica el procedimiento solicitado."],
                "corrections": [],
            })
        )
        self.assertEqual(
            find_review_contract_conflicts(review, self.contract),
            [],
        )


if __name__ == "__main__":
    unittest.main()
