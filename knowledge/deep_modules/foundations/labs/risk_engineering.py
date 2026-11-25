"""Small deterministic risk-estimation lab using explicitly synthetic assumptions."""
from __future__ import annotations

import json
import math
from typing import Any


def expected_annual_loss(frequency_per_year: float, loss_per_event: float) -> float:
    """Return expected annual loss for a single, defined scenario.

    This multiplication is valid only when frequency and conditional loss refer
    to the same scenario, horizon and population, and their assumptions are
    defensible. It is not a universal risk score.
    """
    values = (frequency_per_year, loss_per_event)
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in values
    ):
        raise ValueError("frequency and loss must be finite numeric values")
    if frequency_per_year < 0 or loss_per_event < 0:
        raise ValueError("frequency and loss must be non-negative")
    return frequency_per_year * loss_per_event


def run_lab() -> dict[str, Any]:
    """Compare a baseline and controlled scenario; values are illustrative USD."""
    baseline_frequency = 0.40
    baseline_loss = 120_000.0
    residual_frequency = 0.15
    residual_loss = 80_000.0
    annual_control_cost = 15_000.0

    baseline_eal = expected_annual_loss(baseline_frequency, baseline_loss)
    residual_eal = expected_annual_loss(residual_frequency, residual_loss)
    avoided_eal = baseline_eal - residual_eal
    net_modeled_benefit = avoided_eal - annual_control_cost

    sensitivity = []
    for label, frequency, loss in (
        ("low", 0.20, 80_000.0),
        ("base", baseline_frequency, baseline_loss),
        ("high", 0.60, 160_000.0),
    ):
        residual_f = frequency * (residual_frequency / baseline_frequency)
        residual_l = loss * (residual_loss / baseline_loss)
        before = expected_annual_loss(frequency, loss)
        after = expected_annual_loss(residual_f, residual_l)
        sensitivity.append({
            "case": label,
            "baseline_eal_usd": round(before, 2),
            "residual_eal_usd": round(after, 2),
            "avoided_eal_usd": round(before - after, 2),
            "net_after_control_cost_usd": round(before - after - annual_control_cost, 2),
        })

    multidimensional_sensitivity = []
    frequency_factors = (0.5, 1.0, 1.5)
    loss_factors = (0.5, 1.0, 1.5)
    residual_frequency_factors = (0.75, 1.0, 1.25)
    for frequency_factor in frequency_factors:
        for loss_factor in loss_factors:
            for residual_frequency_factor in residual_frequency_factors:
                scenario_frequency = baseline_frequency * frequency_factor
                scenario_loss = baseline_loss * loss_factor
                scenario_residual_frequency = (
                    scenario_frequency
                    * (residual_frequency / baseline_frequency)
                    * residual_frequency_factor
                )
                scenario_residual_loss = (
                    scenario_loss * (residual_loss / baseline_loss)
                )
                before = expected_annual_loss(scenario_frequency, scenario_loss)
                after = expected_annual_loss(
                    scenario_residual_frequency, scenario_residual_loss
                )
                multidimensional_sensitivity.append({
                    "baseline_frequency_factor": frequency_factor,
                    "baseline_loss_factor": loss_factor,
                    "residual_frequency_factor": residual_frequency_factor,
                    "baseline_eal_usd": round(before, 2),
                    "residual_eal_usd": round(after, 2),
                    "avoided_eal_usd": round(before - after, 2),
                    "net_after_control_cost_usd": round(
                        before - after - annual_control_cost, 2
                    ),
                })

    return {
        "schema_version": "1.0.0",
        "lab_id": "LAB-FND-14A",
        "synthetic_only": True,
        "currency": "USD",
        "assumptions": {
            "baseline_frequency_per_year": baseline_frequency,
            "baseline_conditional_loss_usd": baseline_loss,
            "residual_frequency_per_year": residual_frequency,
            "residual_conditional_loss_usd": residual_loss,
            "annual_control_cost_usd": annual_control_cost,
            "scenario": "unauthorized CI deployment publishes a tampered production artifact",
        },
        "results": {
            "baseline_eal_usd": round(baseline_eal, 2),
            "residual_eal_usd": round(residual_eal, 2),
            "avoided_eal_usd": round(avoided_eal, 2),
            "net_modeled_benefit_usd": round(net_modeled_benefit, 2),
            "break_even_annual_control_cost_usd": round(avoided_eal, 2),
        },
        "sensitivity": sensitivity,
        "multidimensional_sensitivity": {
            "method": "deterministic_factorial_grid_not_probability_distribution",
            "rows": multidimensional_sensitivity,
            "row_count": len(multidimensional_sensitivity),
            "assumption_factors": {
                "baseline_frequency": list(frequency_factors),
                "baseline_loss": list(loss_factors),
                "residual_frequency_effectiveness": list(residual_frequency_factors),
            },
        },
        "checks": {
            "baseline_eal_correct": baseline_eal == 48_000.0,
            "residual_eal_correct": residual_eal == 12_000.0,
            "avoided_loss_correct": avoided_eal == 36_000.0,
            "net_benefit_correct": net_modeled_benefit == 21_000.0,
            "sensitivity_ordered": (
                sensitivity[0]["avoided_eal_usd"]
                < sensitivity[1]["avoided_eal_usd"]
                < sensitivity[2]["avoided_eal_usd"]
            ),
            "multidimensional_grid_complete": len(multidimensional_sensitivity) == 27,
            "multidimensional_grid_nonnegative": all(
                item["baseline_eal_usd"] >= 0
                and item["residual_eal_usd"] >= 0
                for item in multidimensional_sensitivity
            ),
        },
        "all_checks_passed": all((
            baseline_eal == 48_000.0,
            residual_eal == 12_000.0,
            avoided_eal == 36_000.0,
            net_modeled_benefit == 21_000.0,
            sensitivity[0]["avoided_eal_usd"]
            < sensitivity[1]["avoided_eal_usd"]
            < sensitivity[2]["avoided_eal_usd"],
            len(multidimensional_sensitivity) == 27,
            all(item["baseline_eal_usd"] >= 0
                and item["residual_eal_usd"] >= 0
                for item in multidimensional_sensitivity),
        )),
        "limitations": [
            "Illustrative assumptions are not measured incident frequencies or loss data.",
            "Frequency and conditional loss must be scenario-consistent; dependencies and tail losses are not modeled.",
            "The net benefit is a simplified economic comparison, not a risk-acceptance decision.",
            "No control efficacy, production system or external dataset was independently validated.",
            "The 27-row factorial sensitivity grid is deterministic and does not represent probability distributions, Monte Carlo estimates or confidence intervals.",
            "Frequency, loss and residual-frequency factors are illustrative assumptions; dependence between scenarios and tail risk remain unmodeled.",
        ],
    }


def main() -> int:
    report = run_lab()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
