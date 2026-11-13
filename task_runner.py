#!/usr/bin/env python3
"""Ejecutor controlado de comprobaciones seleccionadas por CYBER_AI."""

import argparse
import json
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

from capability_selector import select_capabilities
from execution_policy import AuthorizationError, authorize_target
from execution_ledger import ExecutionLedger


def _record_task_scan(task, target, report, started, authorization_id=None):
    """Registra ejecuciones del runner de plantillas Nuclei."""
    status = report.get("status")
    ledger_status = (
        "denied" if status == "authorization_denied"
        else "timeout" if status == "timeout"
        else "completed" if status == "completed"
        else "failed"
    )
    try:
        ExecutionLedger().append(
            namespace="security-scans", task=f"{task} :: {target}",
            status=ledger_status, tool="nuclei_task_runner",
            evidence=report,
            duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            metadata={"authorization_id": authorization_id, "scanner_status": status},
        )
    except Exception as error:
        print(f"AVISO: no se pudo registrar el escaneo en el ledger: {error}", file=sys.stderr)


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
    allowed = []
    for item in candidates:
        path = Path(item["path"])
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if (
            len(relative.parts) >= 3
            and relative.parts[0] == "http"
            and relative.parts[1] in ("technologies", "misconfiguration")
            and path.is_file()
        ):
            allowed.append(item)

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
    for item in candidates:
        try:
            relative = Path(item["path"]).relative_to(root).as_posix()
        except ValueError:
            continue
        by_relative_path[relative] = item

    selected = [
        by_relative_path[name]
        for name in preferred
        if name in by_relative_path
        and Path(by_relative_path[name]["path"]).is_file()
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
        return 2

    try:
        grant = authorize_target(args.target, "nuclei_scan", args.authorization_id)
    except AuthorizationError as error:
        print("ERROR: autorización denegada:", error)
        _record_task_scan(args.task, args.target,
                          {"task": args.task, "target": args.target,
                           "status": "authorization_denied", "error": str(error)},
                          task_started, args.authorization_id)
        return 2

    nuclei = shutil.which("nuclei")
    if not nuclei:
        print("ERROR: Nuclei no está instalado o no está en PATH.")
        _record_task_scan(args.task, args.target,
                          {"task": args.task, "target": args.target,
                           "status": "scanner_missing", "findings": []},
                          task_started, args.authorization_id)
        return 1

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    scan_id = uuid.uuid4().hex
    results_file = output_dir / f"task_scan_{scan_id}.jsonl"
    report_file = output_dir / f"task_scan_{scan_id}_report.json"

    command = [
        nuclei, "-u", args.target,
        "-jsonl", "-o", str(results_file.resolve()),
        "-no-interactsh", "-disable-update-check", "-disable-redirects",
        "-rl", "2", "-c", "2", "-timeout", "5", "-retries", "0",
    ]
    for item in selected:
        command.extend(["-t", item["path"]])

    print("\nIniciando comprobaciones limitadas...")
    started = time.monotonic()
    try:
        process = subprocess.run(
            command, capture_output=True, text=True, timeout=90
        )
        elapsed = round(time.monotonic() - started, 2)
    except subprocess.TimeoutExpired:
        report = {
            "task": args.task, "target": args.target,
            "status": "timeout", "elapsed_seconds": 90,
            "findings": [],
        }
        report_file.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        _record_task_scan(args.task, args.target, report, task_started, args.authorization_id)
        print("Tiempo agotado. Informe:", report_file)
        return 1

    findings = []
    if results_file.is_file():
        for line in results_file.read_text(encoding="utf-8").splitlines():
            try:
                findings.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    report = {
        "task": args.task,
        "target": args.target,
        "authorization": grant,
        "status": "completed" if process.returncode == 0 else "scanner_error",
        "elapsed_seconds": elapsed,
        "templates_used": [item["path"] for item in selected],
        "findings_count": len(findings),
        "findings": findings,
        "scanner_output": (process.stdout + "\n" + process.stderr)[-12000:],
        "note": "Los resultados son indicios y requieren validación.",
    }
    report_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _record_task_scan(args.task, args.target, report, task_started, args.authorization_id)
    print("\nEstado:", report["status"])
    print("Tiempo:", elapsed, "segundos")
    print("Hallazgos:", len(findings))
    print("Informe:", report_file)
    return 0 if process.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
