"""Shared structural contracts for configured multi-agent workflows.

This module is deliberately independent from model providers and tool execution so
both the real orchestrator and deterministic simulator enforce the same schema.
"""
from __future__ import annotations

import math
from typing import Any


class WorkflowContractError(ValueError):
    """A workflow definition violates the supported contract."""


def _positive_integer(value: Any, field: str, *, minimum: int = 1, maximum: int | None = None) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise WorkflowContractError(f"{field} debe ser un entero mayor o igual a {minimum}.")
    if maximum is not None and value > maximum:
        raise WorkflowContractError(f"{field} no puede superar {maximum}.")


def validate_workflow_definition(workflow: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate shared workflow/step fields and return normalized step copies."""
    if not isinstance(workflow, dict):
        raise WorkflowContractError("El flujo debe ser un objeto.")

    workflow_mode = workflow.get("mode", "standard")
    if not isinstance(workflow_mode, str) or workflow_mode not in {"standard", "technical"}:
        raise WorkflowContractError("El modo del flujo no es válido.")

    for field in ("max_rounds", "max_steps", "max_context_chars"):
        if field in workflow:
            _positive_integer(workflow[field], field)

    steps = workflow.get("steps")
    if not isinstance(steps, list) or not steps:
        raise WorkflowContractError("El flujo debe contener al menos un paso.")

    normalized: list[dict[str, Any]] = []
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise WorkflowContractError(f"El paso {index} debe ser un objeto.")

        agent = step.get("agent")
        objective = step.get("objective")
        if not isinstance(agent, str) or not agent.strip():
            raise WorkflowContractError(f"El paso {index} no tiene agente válido.")
        if not isinstance(objective, str) or not objective.strip():
            raise WorkflowContractError(f"El paso {index} no tiene objetivo válido.")

        mode = step.get("mode", workflow_mode)
        if not isinstance(mode, str) or mode not in {"standard", "technical"}:
            raise WorkflowContractError(f"El modo del paso {index} no es válido.")

        prefix = step.get("required_output_prefix", "")
        sections = step.get("required_output_sections", [])
        if not isinstance(prefix, str):
            raise WorkflowContractError(
                f"El prefijo requerido del paso {index} no es válido."
            )
        if not isinstance(sections, list) or any(
            not isinstance(item, str) or not item.strip() for item in sections
        ):
            raise WorkflowContractError(
                f"Las secciones requeridas del paso {index} no son válidas."
            )

        if "max_retries" in step:
            _positive_integer(step["max_retries"], f"Paso {index}: max_retries", minimum=0, maximum=2)
        if "num_predict" in step:
            _positive_integer(step["num_predict"], f"Paso {index}: num_predict", minimum=100, maximum=2500)
        if "max_num_predict" in step:
            _positive_integer(step["max_num_predict"], f"Paso {index}: max_num_predict", minimum=100, maximum=2500)
        if "num_predict" in step and "max_num_predict" in step:
            if step["max_num_predict"] < step["num_predict"]:
                raise WorkflowContractError(
                    f"Paso {index}: max_num_predict no puede ser menor que num_predict."
                )
        if "knowledge_top_k" in step:
            _positive_integer(step["knowledge_top_k"], f"Paso {index}: knowledge_top_k", maximum=5)
        if "knowledge_min_score" in step:
            score = step["knowledge_min_score"]
            if (
                isinstance(score, bool)
                or not isinstance(score, (int, float))
                or not math.isfinite(score)
                or not 0.0 <= score <= 1.0
            ):
                raise WorkflowContractError(
                    f"Paso {index}: knowledge_min_score debe estar entre 0 y 1."
                )
        for boolean_field in ("think", "use_knowledge"):
            if boolean_field in step and not isinstance(step[boolean_field], bool):
                raise WorkflowContractError(
                    f"Paso {index}: {boolean_field} debe ser booleano."
                )

        normalized_step = dict(step)
        normalized_step.update({
            "order": index,
            "agent": agent.strip(),
            "objective": objective.strip(),
            "mode": mode,
            "required_output_prefix": prefix,
            "required_output_sections": list(sections),
        })
        normalized.append(normalized_step)

    return normalized
