#!/usr/bin/env python3
"""Genera un plan de análisis a partir de la tarea solicitada."""

import json
from datetime import datetime, timezone
from pathlib import Path

from capability_selector import select_capabilities
from domain_capability_matrix import select_domain_capabilities
from tool_registry import select_tools


def create_plan(task, output_path=None):
    planning_warnings = []
    try:
        candidates = select_capabilities(task, limit=25)
    except FileNotFoundError:
        candidates = []
        planning_warnings.append(
            "El inventario de capacidades no está generado; se continúa "
            "en modo degradado sin plantillas candidatas."
        )

    tool_plan = select_tools(task, limit=10)
    try:
        domain_plan = select_domain_capabilities(task, limit=12)
    except (FileNotFoundError, OSError, ValueError, ImportError) as error:
        domain_plan = {
            "matched_domain_count": 0,
            "domains": [],
            "skill_candidates": [],
            "execution_started": False,
            "note": "La matriz de dominios no pudo consultarse.",
        }
        planning_warnings.append(
            f"Matriz de dominios/Skills no disponible: {type(error).__name__}."
        )

    domain_tools = {}
    planned_tools = {item["id"]: {**item, "source_domains": []}
                     for item in tool_plan["candidates"]}
    for domain in domain_plan["domains"]:
        for candidate in domain["tool_candidates"]:
            entry = domain_tools.setdefault(candidate["id"], {
                **candidate, "source_domains": [],
            })
            entry["source_domains"].append(domain["id"])
            # La matriz aporta candidatos al plan de ejecución, pero solo
            # después se aplican las mismas barreras del pipeline: adaptador,
            # disponibilidad, riesgo y confirmación explícita.
            planned = planned_tools.setdefault(candidate["id"], {
                **candidate, "source_domains": [],
            })
            if domain["id"] not in planned["source_domains"]:
                planned["source_domains"].append(domain["id"])

    merged_tool_candidates = list(planned_tools.values())

    plan = {
        "planning_warnings": planning_warnings,
        "task": task,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "planned",
        "candidate_count": len(candidates),
        "tool_candidates": merged_tool_candidates,
        "tool_candidate_count": len(merged_tool_candidates),
        "domain_capabilities": domain_plan["domains"],
        "domain_candidate_count": domain_plan["matched_domain_count"],
        "domain_tool_candidates": list(domain_tools.values()),
        "skill_candidates": domain_plan["skill_candidates"],
        "tool_execution_started": False,
        "steps": [
            {
                "order": i,
                "template": item["name"],
                "path": item["path"],
                "category": item["category"],
                "reason": "Coincidencia con la tarea solicitada",
                "requires_authorized_target": True,
            }
            for i, item in enumerate(candidates, 1)
        ],
        "execution_started": False,
        "note": (
            "Plan preliminar: relaciona dominios, paquetes de conocimiento, "
            "herramientas y Skills. Las candidatas requieren revisión y no "
            "se ejecutan ni autorizan automáticamente."
        ),
    }
    output = Path(output_path) if output_path is not None else Path("reports/task_plan.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return plan, output


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Uso: python3 task_planner.py "auditoria web"')
        raise SystemExit(2)
    plan, output = create_plan(" ".join(sys.argv[1:]))
    print("Tarea:", plan["task"])
    print("Comprobaciones candidatas:", plan["candidate_count"])
    print("Dominios relacionados:", plan["domain_candidate_count"])
    print("Herramientas por dominio:", len(plan["domain_tool_candidates"]))
    print("Skills relacionadas:", len(plan["skill_candidates"]))
    print("Plan:", output)
    print("Estado:", plan["status"])
