"""Ejecución opt-in de herramientas locales planificadas con evidencia y ledger.

La selección nunca concede permisos. Esta ruta requiere confirmación explícita,
allowlist HMAC obligatoria y objetivos locales confinados al repositorio.
"""
import os
from pathlib import Path

from execution_ledger import ExecutionLedger
from tool_result_validator import validate_tool_evidence
from tool_adapters import (
    TOOL_SPECS,
    ToolExecutionError,
    run_local_tool,
    write_evidence,
)


def execute_tool_plan(plan, target, *, confirmed=False, max_tools=3):
    if not confirmed:
        raise ToolExecutionError("La ejecución requiere confirmación explícita del operador.")
    if not isinstance(plan, dict) or not isinstance(plan.get("tool_candidates"), list):
        raise ToolExecutionError("Plan de herramientas inválido.")
    if not isinstance(max_tools, int) or not 1 <= max_tools <= 3:
        raise ToolExecutionError("El límite de herramientas debe estar entre 1 y 3.")
    target_path = Path(target)
    if target_path.is_absolute():
        raise ToolExecutionError("El objetivo debe expresarse como ruta relativa al repositorio.")
    if ".." in target_path.parts:
        raise ToolExecutionError("No se permiten rutas que salgan del repositorio.")
    selected = [
        item for item in plan["tool_candidates"]
        if isinstance(item, dict)
        and item.get("id") in TOOL_SPECS
        and item.get("adapter_supported") is True
        and item.get("available") is True
        and item.get("risk") != "active_network"
    ][:max_tools]
    if not selected:
        raise ToolExecutionError("El plan no contiene adaptadores locales elegibles.")
    if not os.environ.get("CYBER_AI_TOOL_ALLOWLIST_PATH") or not os.environ.get(
        "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY"
    ):
        raise ToolExecutionError(
            "La ejecución integrada exige CYBER_AI_TOOL_ALLOWLIST_PATH y "
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY."
        )

    previous_required = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_REQUIRED")
    os.environ["CYBER_AI_TOOL_ALLOWLIST_REQUIRED"] = "1"
    results = []
    try:
        for item in selected:
            tool_id = item["id"]
            try:
                evidence = run_local_tool(tool_id, str(target_path))
                validation = validate_tool_evidence(evidence)
                evidence["independent_integrity_validation"] = validation
                evidence_path = write_evidence(evidence)
                status = evidence.get("status", "failed")
                ledger_status = (
                    "completed" if validation["status"] == "valid_integrity" else
                    "timeout" if status == "timeout" else "failed"
                )
                event = ExecutionLedger().append(
                    namespace="security-tool-executions",
                    task=plan.get("task", "planned tool execution"),
                    status=ledger_status,
                    tool=tool_id,
                    tool_version=str(evidence.get("tool_version", "unknown")),
                    environment="local-adapter",
                    evidence={
                        "evidence_path": str(evidence_path),
                        "target_sha256": evidence.get("target_sha256"),
                        "tool_binary_sha256": evidence.get("tool_binary_sha256"),
                        "status": status,
                        "validation": validation,
                    },
                    duration_ms=int(evidence.get("duration_ms", 0)),
                    metadata={"plan_status": plan.get("status"), "authorization_mode": "operator-confirmed-local-allowlist"},
                )
                results.append({
                    "tool": tool_id, "status": status,
                    "evidence_path": str(evidence_path),
                    "ledger_event_id": event["event_id"],
                    "findings_count": evidence.get("findings_count"),
                    "validation": validation,
                })
            except Exception as error:
                event = ExecutionLedger().append(
                    namespace="security-tool-executions",
                    task=plan.get("task", "planned tool execution"),
                    status="failed", tool=tool_id,
                    evidence={"error_type": type(error).__name__, "error": str(error)[:1000]},
                    duration_ms=0,
                    metadata={"plan_status": plan.get("status")},
                )
                results.append({
                    "tool": tool_id, "status": "failed",
                    "error": str(error)[:1000],
                    "ledger_event_id": event["event_id"],
                })
    finally:
        if previous_required is None:
            os.environ.pop("CYBER_AI_TOOL_ALLOWLIST_REQUIRED", None)
        else:
            os.environ["CYBER_AI_TOOL_ALLOWLIST_REQUIRED"] = previous_required
    return {
        "status": "completed" if results and all(
            x["status"] == "completed"
            and x.get("validation", {}).get("status") == "valid_integrity"
            for x in results
        ) else "partial_or_failed",
        "target": str(target_path),
        "results": results,
        "note": "Los hallazgos son indicios no confiables y requieren validación independiente.",
    }
