#!/usr/bin/env python3
"""Interfaz CLI explícita para los adaptadores locales de CYBER_AI."""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

from tool_adapters import TOOL_SPECS, ToolExecutionError, run_local_tool, write_evidence
from execution_ledger import ExecutionLedger


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=sorted(TOOL_SPECS))
    parser.add_argument("--target", required=True, help="Ruta relativa dentro del repositorio")
    parser.add_argument("--config", help="Configuración local para Semgrep")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--execute", action="store_true", help="Confirma la ejecución local")
    args = parser.parse_args(argv)

    if not args.execute:
        print(json.dumps({
            "status": "dry_run",
            "tool": args.tool,
            "target": args.target,
            "execution_started": False,
            "message": "Añade --execute para iniciar el adaptador local.",
        }, ensure_ascii=False, indent=2))
        return 0

    started = time.monotonic()
    try:
        evidence = run_local_tool(
            args.tool, args.target, config_path=args.config, timeout=args.timeout
        )
    except ToolExecutionError as exc:
        try:
            ExecutionLedger().append(
                namespace="local-tools", task=args.target, status="denied",
                tool=args.tool, evidence={"reason": str(exc)},
                duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            )
        except Exception as ledger_error:
            print(f"AVISO: ledger no disponible: {ledger_error}", file=sys.stderr)
        print(json.dumps({"status": "denied", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    evidence_dir = os.environ.get("CYBER_AI_EVIDENCE_DIR")
    evidence_path = None
    artifact_sha256 = None
    try:
        evidence_path = write_evidence(
            evidence,
            output_dir=evidence_dir or "reports/tool_evidence",
            allow_external=bool(evidence_dir),
        )
        artifact_sha256 = hashlib.sha256(Path(evidence_path).read_bytes()).hexdigest()
        evidence["evidence_file"] = str(evidence_path)
    except (ToolExecutionError, OSError) as evidence_error:
        evidence["evidence_write_error"] = str(evidence_error)

    try:
        ledger_status = evidence.get("status")
        if ledger_status not in {"completed", "timeout"}:
            ledger_status = "failed"
        ledger_event = ExecutionLedger().append(
            namespace="local-tools", task=args.target, status=ledger_status,
            tool=args.tool, tool_version=evidence.get("tool_version", "unknown"),
            evidence=evidence,
            duration_ms=max(0, int(float(evidence.get("elapsed_seconds", 0)) * 1000)),
            validator_results=[{"name": "process_exit", "passed": evidence.get("return_code") == 0}],
            metadata={"target": evidence.get("target"),
                      "target_sha256": evidence.get("target_sha256"),
                      "target_modified": evidence.get("target_modified"),
                      "evidence_artifact_sha256": artifact_sha256},
        )
        evidence["ledger_event"] = ledger_event
    except Exception as ledger_error:
        evidence["ledger_error"] = str(ledger_error)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if evidence["status"] == "completed" and evidence["return_code"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
