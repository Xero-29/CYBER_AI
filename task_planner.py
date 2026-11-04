#!/usr/bin/env python3
"""Genera un plan de análisis a partir de la tarea solicitada."""

import json
from datetime import datetime, timezone
from pathlib import Path
from capability_selector import select_capabilities

def create_plan(task):
    candidates = select_capabilities(task, limit=25)
    plan = {
        "task": task,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "planned",
        "candidate_count": len(candidates),
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
        "note": "Plan preliminar basado en reglas; requiere validar relevancia antes de ejecutar."
    }
    output = Path("reports/task_plan.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return plan, output

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Uso: python3 task_planner.py "auditoria web"')
        raise SystemExit(2)
    plan, output = create_plan(" ".join(sys.argv[1:]))
    print("Tarea:", plan["task"])
    print("Comprobaciones candidatas:", plan["candidate_count"])
    print("Plan:", output)
    print("Estado:", plan["status"])
