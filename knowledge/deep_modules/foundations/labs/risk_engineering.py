"""Small deterministic risk-estimation lab using explicitly synthetic assumptions."""
from __future__ import annotations

import json
from typing import Any


def expected_annual_loss(frequency_per_year: float, loss_per_event: float) -> float:
    """Return expected annual loss for a single, defined scenario.

    This multiplication is valid only when frequency and conditional loss refer
    to the same scenario, horizon and population, and their assumptions are
    defensible. It is not a universal risk score.
    """
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
        },
        "all_checks_passed": all((
            baseline_eal == 48_000.0,
            residual_eal == 12_000.0,
            avoided_eal == 36_000.0,
            net_modeled_benefit == 21_000.0,
            sensitivity[0]["avoided_eal_usd"]
            < sensitivity[1]["avoided_eal_usd"]
            < sensitivity[2]["avoided_eal_usd"],
        )),
        "limitations": [
            "Illustrative assumptions are not measured incident frequencies or loss data.",
            "Frequency and conditional loss must be scenario-consistent; dependencies and tail losses are not modeled.",
            "The net benefit is a simplified economic comparison, not a risk-acceptance decision.",
            "No control efficacy, production system or external dataset was independently validated.",
        ],
    }


def main() -> int:
    report = run_lab()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
