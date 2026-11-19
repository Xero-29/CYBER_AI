#!/usr/bin/env python3
"""Ejecutor controlado de comprobaciones seleccionadas por CYBER_AI."""

import argparse
import json
import os
import shutil
import stat
import sys
import tempfile
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

from capability_selector import select_capabilities
from execution_policy import AuthorizationError, authorize_target
from execution_ledger import ExecutionLedger
from binary_integrity import (
    BinaryIntegrityError,
    build_minimal_environment,
    hash_executable,
    require_approved_executable,
)
from safe_io import SafeWriteError, atomic_write_text, ensure_private_directory
from process_isolation import ProcessIsolationError, run_bounded_process
from template_integrity import (
    hash_selected_templates as _hash_selected_templates,
    safe_template_path as _safe_template_path,
)


MAX_SCAN_OUTPUT_BYTES = 20 * 1024 * 1024
MAX_FINDINGS = 10000


def _record_task_scan(task, target, report, started, authorization_id=None, start_event_id=None):
    """Registra ejecuciones del runner de plantillas Nuclei."""
    status = report.get("status")
    ledger_status = (
        "denied" if status == "authorization_denied"
        else "timeout" if status == "timeout"
        else "completed" if status == "completed"
        else "failed"
    )
    try:
        event = ExecutionLedger().append(
            namespace="security-scans", task=f"{task} :: {target}",
            status=ledger_status, tool="nuclei_task_runner",
            evidence=report,
            duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            metadata={"authorization_id": authorization_id, "scanner_status": status,
                      "start_event_id": start_event_id},
        )
        return event
    except Exception as error:
        print(f"AVISO: no se pudo registrar el escaneo en el ledger: {error}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Ejecutor de tareas CYBER_AI")
    parser.add_argument("--task", required=True, help="Objetivo del análisis")
    parser.add_argument("--target", required=True, help="URL autorizada")
    parser.add_argument("--execute", action="store_true", help="Ejecutar el análisis")
    parser.add_argument(
        "--confirm-authorized",
        action="store_true",
        help="Confirmación interactiva adicional del operador",
    )
    parser.add_argument(
        "--authorization-id",
        help="ID de una autorización local vigente y limitada al destino",
    )
    ledger_policy = parser.add_mutually_exclusive_group()
    ledger_policy.add_argument(
        "--require-ledger", dest="require_ledger", action="store_true",
        help="Exige ledger para el escaneo (predeterminado).",
    )
    ledger_policy.add_argument(
        "--allow-unlogged-execution", dest="require_ledger", action="store_false",
        help="Permite explícitamente escanear sin ledger; no recomendado.",
    )
    parser.set_defaults(require_ledger=True)
    args = parser.parse_args()

    parsed = urlparse(args.target)
    task_started = time.monotonic()
    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        parser.error("Indica una URL HTTP/HTTPS válida.")

    # Solo permitir inicialmente comprobaciones de tecnologías
    # y configuraciones; excluimos otras familias de plantillas.
    root = Path.home() / "nuclei-templates"
    candidates = select_capabilities(args.task, limit=20000)
    safe_candidates = []
    for item in candidates:
        safe_path = _safe_template_path(item.get("path", ""), root)
        if safe_path is not None:
            safe_candidates.append({**item, "path": str(safe_path)})

    # Plantillas generales seleccionadas explícitamente para auditoría web.
    preferred = [
        "http/technologies/tech-detect.yaml",
        "http/technologies/favicon-detect.yaml",
        "http/misconfiguration/http-missing-security-headers.yaml",
        "http/misconfiguration/cookies-without-secure.yaml",
        "http/misconfiguration/cookies-without-httponly.yaml",
        "http/misconfiguration/missing-cookie-samesite-strict.yaml",
    ]

    by_relative_path = {}
    root_resolved = root.resolve(strict=False)
    for item in safe_candidates:
        try:
            relative = Path(item["path"]).relative_to(root_resolved).as_posix()
        except ValueError:
            continue
        by_relative_path[relative] = item

    selected = [
        by_relative_path[name]
        for name in preferred
        if name in by_relative_path
        and _safe_template_path(by_relative_path[name]["path"], root) is not None
    ][:10]

    if not selected:
        print("No se encontraron plantillas adecuadas para esta tarea.")
        return 1

    print("Tarea:", args.task)
    print("Objetivo:", args.target)
    print("Plantillas seleccionadas:", len(selected))
    for item in selected:
        print(" -", item["path"])

    if not args.execute:
        print("\nModo de prueba: no se ejecutó ningún escaneo.")
        print("Revisa las plantillas antes de autorizar su ejecución.")
        return 0

    if not args.confirm_authorized or not args.authorization_id:
        print("ERROR: se requiere --confirm-authorized y --authorization-id.")
        recorded = _record_task_scan(
            args.task, args.target,
            {"task": args.task, "target": args.target,
             "status": "authorization_denied",
             "reason": "missing_operator_confirmation_or_authorization_id"},
            task_started, args.authorization_id,
        )
        return 3 if args.require_ledger and recorded is None else 2

    try:
        grant = authorize_target(args.target, "nuclei_scan", args.authorization_id)
    except AuthorizationError as error:
        print("ERROR: autorización denegada:", error)
        recorded = _record_task_scan(args.task, args.target,
                                     {"task": args.task, "target": args.target,
                                      "status": "authorization_denied", "error": str(error)},
                                     task_started, args.authorization_id)
        return 3 if args.require_ledger and recorded is None else 2

    nuclei = shutil.which("nuclei")
    if not nuclei:
        print("ERROR: Nuclei no está instalado o no está en PATH.")
        recorded = _record_task_scan(args.task, args.target,
                                     {"task": args.task, "target": args.target,
                                      "status": "scanner_missing", "findings": []},
                                     task_started, args.authorization_id)
        return 3 if args.require_ledger and recorded is None else 1

    try:
        binary_provenance = require_approved_executable(nuclei, "nuclei")
        nuclei = binary_provenance["resolved_path"]
    except BinaryIntegrityError as error:
        print("ERROR: ejecución bloqueada; Nuclei no está aprobado:", error, file=sys.stderr)
        recorded = _record_task_scan(
            args.task, args.target,
            {"task": args.task, "target": args.target,
             "status": "authorization_denied",
             "reason": "scanner_binary_not_approved"},
            task_started, args.authorization_id,
        )
        return 3 if args.require_ledger and recorded is None else 2

    try:
        output_dir = ensure_private_directory(Path("reports"))
    except SafeWriteError as error:
        print("ERROR: directorio de informes inseguro:", error, file=sys.stderr)
        recorded = _record_task_scan(
            args.task, args.target,
            {"task": args.task, "target": args.target, "status": "failed",
             "reason": "unsafe_report_directory"},
            task_started, args.authorization_id,
        )
        return 3 if args.require_ledger and recorded is None else 2
    scan_id = uuid.uuid4().hex
    results_file = output_dir / f"task_scan_{scan_id}.jsonl"
    report_file = output_dir / f"task_scan_{scan_id}_report.json"

    try:
        template_provenance = _hash_selected_templates(selected, root)
    except (OSError, ValueError) as error:
        print("ERROR: integridad de plantillas no válida:", error, file=sys.stderr)
        recorded = _record_task_scan(
            args.task, args.target,
            {"task": args.task, "target": args.target, "status": "failed",
             "reason": "unsafe_or_changed_templates"},
            task_started, args.authorization_id,
        )
        return 3 if args.require_ledger and recorded is None else 2

    start_event_id = None
    try:
        start_event = ExecutionLedger().append(
            namespace="security-scans", task=f"{args.task} :: {args.target}",
            status="started", tool="nuclei_task_runner",
            evidence={"phase": "scan_start", "selected_templates": len(selected)},
            duration_ms=0, metadata={"authorization_id": args.authorization_id},
        )
        start_event_id = start_event["event_id"]
    except Exception as ledger_error:
        print("AVISO: no se pudo registrar el inicio:", ledger_error, file=sys.stderr)
        if args.require_ledger:
            return 3

    try:
        command = [
            nuclei, "-u", args.target,
            "-jsonl", "-o", str(results_file.resolve()),
            "-no-interactsh", "-no-stdin",
            "-type", "http",
            "-exclude-tags", "dos,intrusive,fuzz,code,headless",
            "-disable-unsigned-templates",
            "-omit-raw", "-omit-template",
            "-disable-update-check", "-disable-redirects",
            "-max-host-error", "5",
            "-rl", "2", "-c", "2", "-timeout", "5", "-retries", "0",
        ]
        for item in selected:
            command.extend(["-t", item["path"]])
    
        print("\nIniciando comprobaciones limitadas...")
        started = time.monotonic()
        with tempfile.TemporaryDirectory(prefix="cyber-ai-nuclei-") as isolated_home:
            if os.name == "posix":
                os.chmod(isolated_home, 0o700)
            process_env = build_minimal_environment(isolated_home, nuclei)
            process_result = run_bounded_process(
                command,
                cwd=isolated_home,
                env=process_env,
                timeout=90,
                max_output_bytes=2_000_000,
            )
        elapsed = round(time.monotonic() - started, 2)
        scanner_output = (process_result["stdout"] + "\n" + process_result["stderr"])[-12000:]

        if process_result["timed_out"]:
            try:
                binary_after = hash_executable(nuclei)
                binary_modified = binary_after["sha256"] != binary_provenance["sha256"]
            except BinaryIntegrityError:
                binary_after = None
                binary_modified = True
            try:
                templates_after = _hash_selected_templates(selected, root)
                templates_modified = templates_after != template_provenance
            except (OSError, ValueError):
                templates_after = []
                templates_modified = True
            integrity_failed = binary_modified or templates_modified
            report = {
                "task": args.task, "target": args.target,
                "status": "integrity_error" if integrity_failed else "timeout",
                "elapsed_seconds": elapsed,
                "tool_binary_sha256": binary_provenance["sha256"],
                "tool_binary_sha256_after": binary_after["sha256"] if binary_after else None,
                "tool_binary_modified": binary_modified,
                "tool_allowlist": binary_provenance["allowlist"],
                "templates_before": template_provenance,
                "templates_after": templates_after,
                "templates_modified": templates_modified,
                "scanner_output": scanner_output,
                "output_truncated": process_result["output_truncated"],
                "process_tree_isolation_enforced": process_result["process_tree_isolation_enforced"],
                "findings": [],
            }
            atomic_write_text(
                report_file,
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            )
            recorded = _record_task_scan(args.task, args.target, report, task_started, args.authorization_id, start_event_id)
            if args.require_ledger and recorded is None:
                return 3
            print("Tiempo agotado. Informe:", report_file)
            return 1

        try:
            binary_after = hash_executable(nuclei)
            binary_modified = binary_after["sha256"] != binary_provenance["sha256"]
        except BinaryIntegrityError:
            binary_after = None
            binary_modified = True

        findings = []
        output_limit_exceeded = False
        evidence_invalid = False
        if results_file.exists() or results_file.is_symlink():
            try:
                output_info = results_file.lstat()
                if stat.S_ISLNK(output_info.st_mode) or not stat.S_ISREG(output_info.st_mode):
                    evidence_invalid = True
                elif output_info.st_size > MAX_SCAN_OUTPUT_BYTES:
                    output_limit_exceeded = True
                else:
                    with results_file.open("r", encoding="utf-8") as stream:
                        for line in stream:
                            if len(line.encode("utf-8")) > 1024 * 1024:
                                evidence_invalid = True
                                findings = []
                                break
                            if len(findings) >= MAX_FINDINGS:
                                output_limit_exceeded = True
                                findings = []
                                break
                            try:
                                findings.append(json.loads(line))
                            except json.JSONDecodeError:
                                evidence_invalid = True
                                findings = []
                                break
            except OSError:
                evidence_invalid = True

        try:
            templates_after = _hash_selected_templates(selected, root)
            templates_modified = templates_after != template_provenance
        except (OSError, ValueError):
            templates_after = []
            templates_modified = True

        discarded_findings_count = 0
        if binary_modified or templates_modified:
            discarded_findings_count = len(findings)
            findings = []

        report_status = (
            "integrity_error" if binary_modified or templates_modified
            else "output_limit_exceeded" if output_limit_exceeded
            else "evidence_invalid" if evidence_invalid
            else "isolation_incomplete" if not process_result["process_tree_isolation_enforced"]
            else "completed" if process_result["returncode"] == 0 else "scanner_error"
        )

        report = {
            "task": args.task,
            "target": args.target,
            "authorization": grant,
            "status": report_status,
            "elapsed_seconds": elapsed,
            "tool_binary_sha256": binary_provenance["sha256"],
            "tool_binary_sha256_after": binary_after["sha256"] if binary_after else None,
            "tool_binary_modified": binary_modified,
            "tool_allowlist": binary_provenance["allowlist"],
            "templates_used": [item["path"] for item in selected],
            "templates_before": template_provenance,
            "templates_after": templates_after,
            "templates_modified": templates_modified,
            "findings_count": len(findings),
            "discarded_findings_count": discarded_findings_count,
            "output_limit_exceeded": output_limit_exceeded,
            "evidence_invalid": evidence_invalid,
            "findings": findings,
            "output_truncated": process_result["output_truncated"],
            "process_tree_isolation_enforced": process_result["process_tree_isolation_enforced"],
            "scanner_output": scanner_output,
            "note": "Los resultados son indicios y requieren validación.",
        }
        atomic_write_text(
            report_file,
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        )
        recorded = _record_task_scan(args.task, args.target, report, task_started, args.authorization_id, start_event_id)
        if args.require_ledger and recorded is None:
            return 3
        print("\nEstado:", report["status"])
        print("Tiempo:", elapsed, "segundos")
        print("Hallazgos:", len(findings))
        print("Informe:", report_file)
        return 0 if report_status == "completed" else 1
    except Exception as error:
        isolation_required = isinstance(error, ProcessIsolationError)
        report = {
            "task": args.task,
            "target": args.target,
            "status": "isolation_required" if isolation_required else "failed",
            "error_type": type(error).__name__,
            "reason": (
                "process_isolation_unavailable"
                if isolation_required
                else "execution_failed"
            ),
            "findings": [],
            "report_persisted": True,
        }
        try:
            atomic_write_text(
                report_file,
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            )
        except (SafeWriteError, OSError, ValueError):
            report["report_persisted"] = False

        recorded = _record_task_scan(
            args.task, args.target, report, task_started,
            args.authorization_id, start_event_id,
        )
        if args.require_ledger and recorded is None:
            return 3
        if report["report_persisted"]:
            print("ERROR: la ejecución terminó; informe privado:", report_file, file=sys.stderr)
        else:
            print("ERROR: la ejecución terminó y no se pudo persistir el informe privado.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
