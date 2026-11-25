#!/usr/bin/env python3
"""Interfaz CLI explícita para los adaptadores locales de CYBER_AI."""
import argparse
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

from tool_adapters import TOOL_SPECS, ToolExecutionError, run_local_tool, write_evidence
from execution_ledger import MAX_SQLITE_INTEGER, ExecutionLedger, _redact_text


def _terminal_status(evidence):
    status = evidence.get("status") if isinstance(evidence, dict) else None
    if not isinstance(evidence, dict):
        return "failed"
    if evidence.get("output_truncated") is True or evidence.get("output_limit_exceeded") is True:
        return "failed"
    if status == "timeout":
        return "timeout"
    if status == "denied":
        return "denied"
    return_code = evidence.get("return_code")
    if status == "completed" and type(return_code) is int and return_code == 0:
        return "completed"
    return "failed"


def _duration_ms(evidence, started):
    """Prefer a bounded adapter duration; fall back to the monotonic clock."""
    elapsed = evidence.get("elapsed_seconds") if isinstance(evidence, dict) else None
    if isinstance(elapsed, int) and not isinstance(elapsed, bool):
        if 0 <= elapsed <= MAX_SQLITE_INTEGER // 1000:
            return elapsed * 1000
    elif isinstance(elapsed, float) and math.isfinite(elapsed) and elapsed >= 0:
        milliseconds = elapsed * 1000
        if math.isfinite(milliseconds) and milliseconds <= MAX_SQLITE_INTEGER:
            return int(milliseconds)
    return max(0, int((time.monotonic() - started) * 1000))


def _integrity_pair_passed(evidence, modified_key, before_key, after_key):
    """Require an explicit unchanged flag and two matching SHA-256 digests."""
    before = evidence.get(before_key)
    after = evidence.get(after_key)
    if evidence.get(modified_key) is not False:
        return False
    if not isinstance(before, str) or not isinstance(after, str):
        return False
    if len(before) != 64 or len(after) != 64:
        return False
    if any(char not in "0123456789abcdef" for char in before.lower() + after.lower()):
        return False
    return before.lower() == after.lower()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=sorted(TOOL_SPECS))
    parser.add_argument("--target", required=True, help="Ruta relativa dentro del repositorio")
    parser.add_argument("--config", help="Configuración local para Semgrep")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--execute", action="store_true", help="Confirma la ejecución local")
    ledger_policy = parser.add_mutually_exclusive_group()
    ledger_policy.add_argument(
        "--require-ledger", dest="require_ledger", action="store_true",
        help="Exige registrar inicio y resultado en el ledger (predeterminado).",
    )
    ledger_policy.add_argument(
        "--allow-unlogged-execution", dest="require_ledger", action="store_false",
        help="Permite explícitamente ejecutar sin ledger; no recomendado.",
    )
    parser.set_defaults(require_ledger=True)
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
        print(
            "AVISO: no se pudo registrar el inicio ("
            f"{type(ledger_error).__name__}).",
            file=sys.stderr,
        )
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
        if evidence.get("output_truncated") is True or evidence.get("output_limit_exceeded") is True:
            if evidence.get("status") == "completed":
                evidence["status"] = "output_incomplete"
            evidence["tool_reported_success"] = False
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
            evidence["evidence_write_error_type"] = type(evidence_error).__name__
            evidence["reason"] = "evidence_persistence_failed"
            evidence["status"] = "failed"
    except ToolExecutionError as exc:
        evidence = {
            "status": "denied",
            "tool": args.tool,
            "target": args.target,
            "reason": _redact_text(str(exc)),
        }
    except Exception as exc:
        evidence = {
            "status": "failed",
            "tool": args.tool,
            "target": args.target,
            "error_type": type(exc).__name__,
            "reason": "unexpected_adapter_error",
        }
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
                    duration_ms=_duration_ms(evidence, started),
                    validator_results=[
                        {
                            "name": "process_exit",
                            "passed": (
                                isinstance(evidence.get("return_code"), int)
                                and not isinstance(evidence.get("return_code"), bool)
                                and evidence.get("return_code") == 0
                            ),
                        },
                        {
                            "name": "tool_binary_integrity",
                            "passed": _integrity_pair_passed(
                                evidence, "tool_binary_modified",
                                "tool_binary_sha256", "tool_binary_sha256_after",
                            ),
                            "evidence": {
                                "sha256_before": evidence.get("tool_binary_sha256"),
                                "sha256_after": evidence.get("tool_binary_sha256_after"),
                            },
                        },
                        {
                            "name": "target_integrity",
                            "passed": _integrity_pair_passed(
                                evidence, "target_modified",
                                "target_sha256", "target_sha256_after",
                            ),
                            "evidence": {
                                "sha256_before": evidence.get("target_sha256"),
                                "sha256_after": evidence.get("target_sha256_after"),
                            },
                        },
                        {
                            "name": "output_completeness",
                            "passed": (
                                evidence.get("output_truncated", False) is False
                                and evidence.get("output_limit_exceeded", False) is False
                                and evidence.get("output_limit_termination_failed", False) is False
                            ),
                            "evidence": {
                                "output_bytes_observed": evidence.get("output_bytes_observed"),
                                "output_limit_bytes": evidence.get("output_limit_bytes"),
                                "output_truncated": evidence.get("output_truncated"),
                                "output_limit_exceeded": evidence.get("output_limit_exceeded"),
                            },
                        },
                    ],
                    metadata={
                        "target": evidence.get("target", args.target),
                        "target_sha256": evidence.get("target_sha256"),
                        "target_sha256_after": evidence.get("target_sha256_after"),
                        "target_modified": evidence.get("target_modified"),
                        "evidence_artifact_sha256": artifact_sha256,
                        "start_event_id": start_event["event_id"],
                    },
                )
                evidence["ledger_event"] = terminal
            except Exception as ledger_error:
                evidence["ledger_error_type"] = type(ledger_error).__name__
                if args.require_ledger:
                    print(json.dumps(evidence, ensure_ascii=False, indent=2))
                    return 3

    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    if evidence.get("status") == "denied":
        return 2
    return 0 if evidence.get("status") == "completed" and evidence.get("return_code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
