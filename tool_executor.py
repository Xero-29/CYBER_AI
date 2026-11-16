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


def _terminal_status(evidence):
    status = evidence.get("status") if isinstance(evidence, dict) else None
    if status == "timeout":
        return "timeout"
    if status == "denied":
        return "denied"
    if status == "completed" and evidence.get("return_code") == 0:
        return "completed"
    return "failed"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=sorted(TOOL_SPECS))
    parser.add_argument("--target", required=True, help="Ruta relativa dentro del repositorio")
    parser.add_argument("--config", help="Configuración local para Semgrep")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--execute", action="store_true", help="Confirma la ejecución local")
    parser.add_argument("--require-ledger", action="store_true",
                        help="Bloquea la ejecución si no puede registrar inicio y resultado")
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
    ledger = None
    start_event = None
    try:
        ledger = ExecutionLedger()
        start_event = ledger.append(
            namespace="local-tools", task=args.target, status="started",
            tool=args.tool, evidence={"phase": "execution_start"},
            duration_ms=0, metadata={"target": args.target},
        )
    except Exception as ledger_error:
        print(f"AVISO: no se pudo registrar el inicio: {ledger_error}", file=sys.stderr)
        if args.require_ledger:
            return 3

    evidence = {
        "status": "failed",
        "tool": args.tool,
        "target": args.target,
        "error": "execution_aborted",
    }
    artifact_sha256 = None
    try:
        evidence = run_local_tool(
            args.tool, args.target, config_path=args.config, timeout=args.timeout
        )
        if not isinstance(evidence, dict):
            raise TypeError("El adaptador debe devolver un objeto de evidencia.")
        evidence = dict(evidence)
        evidence_dir = os.environ.get("CYBER_AI_EVIDENCE_DIR")
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
            evidence["status"] = "failed"
    except ToolExecutionError as exc:
        evidence = {"status": "denied", "tool": args.tool, "target": args.target,
                    "reason": str(exc)}
    except Exception as exc:
        evidence = {"status": "failed", "tool": args.tool, "target": args.target,
                    "error_type": type(exc).__name__, "error": str(exc)}
    finally:
        if ledger is not None and start_event is not None:
            try:
                terminal = ledger.append(
                    namespace="local-tools",
                    task=args.target,
                    status=_terminal_status(evidence),
                    tool=args.tool,
                    tool_version=evidence.get("tool_version", "unknown"),
                    evidence=evidence,
                    duration_ms=max(0, int((time.monotonic() - started) * 1000)),
                    validator_results=[{
                        "name": "process_exit",
                        "passed": evidence.get("return_code") == 0,
                    }],
                    metadata={
                        "target": evidence.get("target", args.target),
                        "target_sha256": evidence.get("target_sha256"),
                        "target_modified": evidence.get("target_modified"),
                        "evidence_artifact_sha256": artifact_sha256,
                        "start_event_id": start_event["event_id"],
                    },
                )
                evidence["ledger_event"] = terminal
            except Exception as ledger_error:
                evidence["ledger_error"] = str(ledger_error)
                if args.require_ledger:
                    print(json.dumps(evidence, ensure_ascii=False, indent=2))
                    return 3

    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    if evidence.get("status") == "denied":
        return 2
    return 0 if evidence.get("status") == "completed" and evidence.get("return_code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
