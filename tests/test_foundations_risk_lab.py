import unittest

from knowledge.deep_modules.foundations.labs.risk_engineering import (
    expected_annual_loss,
    run_lab,
)


class FoundationsRiskEngineeringLabTests(unittest.TestCase):
    def test_expected_annual_loss_uses_frequency_times_conditional_loss(self):
        self.assertEqual(expected_annual_loss(0.4, 120_000), 48_000)

    def test_negative_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            expected_annual_loss(-0.1, 100)
        with self.assertRaises(ValueError):
            expected_annual_loss(0.1, -100)

    def test_lab_results_and_sensitivity_are_reproducible(self):
        report = run_lab()
        self.assertEqual(report["lab_id"], "LAB-FND-14A")
        self.assertTrue(report["synthetic_only"])
        self.assertTrue(report["all_checks_passed"])
        self.assertEqual(report["results"]["baseline_eal_usd"], 48_000)
        self.assertEqual(report["results"]["residual_eal_usd"], 12_000)
        self.assertEqual(report["results"]["avoided_eal_usd"], 36_000)
        self.assertEqual(report["results"]["net_modeled_benefit_usd"], 21_000)
        self.assertEqual(
            [item["case"] for item in report["sensitivity"]],
            ["low", "base", "high"],
        )


if __name__ == "__main__":
    unittest.main()
