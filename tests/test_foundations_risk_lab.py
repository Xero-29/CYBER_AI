import math
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
        for invalid in (math.nan, math.inf, -math.inf):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    expected_annual_loss(invalid, 100)
                with self.assertRaises(ValueError):
                    expected_annual_loss(0.1, invalid)
        with self.assertRaises(ValueError):
            expected_annual_loss(True, 100)

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
        grid = report["multidimensional_sensitivity"]
        self.assertEqual(grid["row_count"], 27)
        self.assertEqual(len(grid["rows"]), 27)
        self.assertEqual(
            grid["method"],
            "deterministic_factorial_grid_not_probability_distribution",
        )
        base_row = next(
            item for item in grid["rows"]
            if item["baseline_frequency_factor"] == 1.0
            and item["baseline_loss_factor"] == 1.0
            and item["residual_frequency_factor"] == 1.0
        )
        self.assertEqual(base_row["baseline_eal_usd"], 48_000)
        self.assertEqual(base_row["residual_eal_usd"], 12_000)


if __name__ == "__main__":
    unittest.main()
