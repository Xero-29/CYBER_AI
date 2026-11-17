#!/usr/bin/env python3
"""Simulación determinista de flujos multiagente sin invocar modelos ni herramientas.

Este módulo valida contratos y coordinación de etapas. No demuestra calidad semántica
ni sustituye pruebas con proveedores reales.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parent
DEFAULT_WORKFLOWS = PROJECT / "config" / "workflows.json"
DEFAULT_REPORTS = PROJECT / "reports" / "agent_simulations"


class SimulationError(ValueError):
    """La definición del flujo no puede simularse de forma segura."""


def validate_workflow_contract(workflow: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(workflow, dict):
        raise SimulationError("El flujo debe ser un objeto.")
    steps = workflow.get("steps")
    if not isinstance(steps, list) or not steps:
        raise SimulationError("El flujo debe contener al menos un paso.")
    normalized = []
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise SimulationError(f"El paso {index} debe ser un objeto.")
        agent = step.get("agent")
        objective = step.get("objective")
        if not isinstance(agent, str) or not agent.strip():
            raise SimulationError(f"El paso {index} no tiene agente válido.")
        if not isinstance(objective, str) or not objective.strip():
            raise SimulationError(f"El paso {index} no tiene objetivo válido.")
        mode = step.get("mode", workflow.get("mode", "standard"))
        if mode not in {"standard", "technical"}:
            raise SimulationError(f"El modo del paso {index} no es válido.")
        prefix = step.get("required_output_prefix", "")
        sections = step.get("required_output_sections", [])
        if not isinstance(prefix, str):
            raise SimulationError(f"El prefijo requerido del paso {index} no es válido.")
        if not isinstance(sections, list) or any(
            not isinstance(item, str) or not item.strip() for item in sections
        ):
            raise SimulationError(f"Las secciones requeridas del paso {index} no son válidas.")
        normalized.append({
            "order": index,
            "agent": agent.strip(),
            "objective": objective.strip(),
            "mode": mode,
            "required_output_prefix": prefix,
            "required_output_sections": sections,
        })
    return normalized


def _synthetic_response(agent: str, step: dict[str, Any]) -> str:
    """Produce una respuesta marcada como sintética que satisface el contrato formal."""
    lines = []
    prefix = step["required_output_prefix"]
    if prefix:
        lines.append(prefix)
    lines.append(f"SIMULACIÓN — respuesta ficticia de {agent}.")
    for section in step["required_output_sections"]:
        lines.append(f"{section} Contenido sintético para probar el contrato.")
    lines.append("LIMITACIÓN: no se invocó ningún modelo ni herramienta real.")
    return "\n".join(lines)


def _validate_response(response: Any, step: dict[str, Any]) -> list[str]:
    errors = []
    if not isinstance(response, str) or not response.strip():
        return ["La respuesta está vacía o no es texto."]
    text = response.strip()
    if len(text) > 100_000:
        errors.append("La respuesta supera el límite de 100000 caracteres.")
    prefix = step["required_output_prefix"]
    if prefix and not text.startswith(prefix):
        errors.append(f"La respuesta debe comenzar con {prefix!r}.")
    folded = text.casefold()
    for section in step["required_output_sections"]:
        if section.casefold() not in folded:
            errors.append(f"Falta la sección obligatoria {section!r}.")
    return errors


def simulate_workflow(
    workflow: dict[str, Any],
    task: str,
    responses: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Simula el flujo secuencial; responses permite inyectar respuestas de prueba.

    No importa proveedores, no ejecuta subprocess, no accede a la red y no llama
    al pipeline de herramientas.
    """
    if not isinstance(task, str) or not task.strip():
        raise SimulationError("La tarea no puede estar vacía.")
    steps = validate_workflow_contract(workflow)
    responses = responses or {}
    if not isinstance(responses, dict):
        raise SimulationError("responses debe ser un objeto indexado por agente.")

    started = time.perf_counter()
    history: list[dict[str, Any]] = []
    results = []
    status = "completed"

    for step in steps:
        agent = step["agent"]
        supplied = responses.get(agent)
        if isinstance(supplied, list):
            response = supplied.pop(0) if supplied else _synthetic_response(agent, step)
        elif supplied is None:
            response = _synthetic_response(agent, step)
        else:
            response = supplied

        errors = _validate_response(response, step)
        item = {
            **step,
            "status": "passed" if not errors else "failed_contract",
            "response": response if isinstance(response, str) else repr(response),
            "validation_errors": errors,
            "input_context_steps": len(history),
            "simulated": True,
        }
        results.append(item)
        if errors:
            status = "stopped_invalid_output"
            break
        history.append({
            "agent": agent,
            "objective": step["objective"],
            "response": response,
        })

    duration = time.perf_counter() - started
    passed = sum(item["status"] == "passed" for item in results)
    return {
        "schema_version": 1,
        "simulation": True,
        "real_model_calls": 0,
        "real_tool_calls": 0,
        "network_access": False,
        "execution_started": False,
        "task": task.strip(),
        "workflow": workflow.get("name", "unnamed"),
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "steps_total": len(steps),
            "steps_executed": len(results),
            "steps_passed": passed,
            "steps_failed": len(results) - passed,
            "completion_ratio": passed / len(steps),
            "duration_seconds": round(duration, 6),
            "context_handoffs": sum(item["input_context_steps"] for item in results),
        },
        "steps": results,
        "limitations": [
            "Las respuestas son sintéticas o inyectadas por pruebas.",
            "La validación comprueba contratos formales, no exactitud técnica.",
            "No se probaron proveedores, modelos, herramientas ni infraestructura real.",
        ],
    }


def load_workflow(name: str, path: Path = DEFAULT_WORKFLOWS) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SimulationError(f"No se pudo leer el catálogo de flujos: {error}") from error
    workflows = payload.get("workflows", {})
    if name not in workflows:
        raise SimulationError(f"No existe el flujo {name!r}.")
    workflow = dict(workflows[name])
    workflow["name"] = name
    return workflow


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", required=True, help="ID del flujo en config/workflows.json")
    parser.add_argument("--task", required=True, help="Tarea ficticia que se usará en la simulación")
    parser.add_argument("--output", help="Ruta del informe JSON")
    args = parser.parse_args(argv)

    try:
        workflow = load_workflow(args.workflow)
        report = simulate_workflow(workflow, args.task)
    except SimulationError as error:
        parser.error(str(error))

    output = Path(args.output) if args.output else (
        DEFAULT_REPORTS / f"{args.workflow}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "steps": report["metrics"]["steps_executed"],
        "passed": report["metrics"]["steps_passed"],
        "report": str(output),
        "real_model_calls": 0,
        "real_tool_calls": 0,
    }, ensure_ascii=False))
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
