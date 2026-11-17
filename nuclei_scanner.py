#!/usr/bin/env python3
"""Escaneo defensivo con Nuclei y seguimiento visible del progreso."""

import json
import os
import signal
import uuid
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

from execution_policy import AuthorizationError, authorize_target
from execution_ledger import ExecutionLedger
from scan_result_validator import validate_scan_result


def validate_target(target):
    """Acepta únicamente URLs HTTP/HTTPS bien formadas."""
    target = target.strip()
    parsed = urlparse(target)

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise ValueError(
            "Usa una URL HTTP/HTTPS autorizada, por ejemplo "
            "http://127.0.0.1:8765"
        )

    return target


def _terminate_process_tree(process):
    """Detiene el grupo completo del escáner para no dejar procesos huérfanos."""
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:
        process.kill()
    process.wait()


def _record_scan_event(target, result, started, *, authorization_id=None, start_event_id=None):
    """Registra intentos, denegaciones y resultados de Nuclei sin ocultar errores."""
    status = result.get("status")
    ledger_status = (
        "denied" if status in {"authorization_required", "authorization_denied"}
        else "timeout" if status == "timeout"
        else "completed" if status == "completed"
        else "failed"
    )
    try:
        event = ExecutionLedger().append(
            namespace="security-scans", task=target, status=ledger_status,
            tool="nuclei", evidence=result,
            duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            metadata={"authorization_id": authorization_id, "scanner_status": status,
                      "start_event_id": start_event_id},
        )
        return event
    except Exception as error:
        print(f"AVISO: no se pudo registrar el escaneo en el ledger: {error}", file=sys.stderr)
        return None


def _record_scan_start(target, authorization_id):
    try:
        event = ExecutionLedger().append(
            namespace="security-scans", task=target, status="started",
            tool="nuclei", evidence={"phase": "scan_start"}, duration_ms=0,
            metadata={"authorization_id": authorization_id},
        )
        return event["event_id"]
    except Exception as error:
        print(f"AVISO: no se pudo registrar el inicio del escaneo: {error}", file=sys.stderr)
        return None


def _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger):
    result.setdefault("evidence_schema", "cyber-ai.remote-scan.v1")
    result.setdefault("scanner", "nuclei")
    result.setdefault("authorization_id", authorization_id)
    result.setdefault("duration_ms", max(0, int((time.monotonic() - started) * 1000)))
    validation = validate_scan_result(result, expected_target=target)
    result["independent_evidence_validation"] = validation
    if result.get("status") == "completed" and not validation["findings_eligible"]:
        result["status"] = "evidence_rejected"
    event_payload = {
        "evidence_schema": result["evidence_schema"],
        "scanner": result["scanner"],
        "target": target,
        "authorization_id": authorization_id,
        "status": result.get("status"),
        "return_code": result.get("return_code"),
        "findings_count": result.get("findings_count", len(result.get("findings", []))),
        "validation": validation,
        "findings": result.get("findings", []),
    }
    event = _record_scan_event(
        target, event_payload, started, authorization_id=authorization_id,
        start_event_id=start_event_id,
    )
    if require_ledger and event is None:
        result["status"] = "ledger_error"
        result["ledger_error"] = "No se pudo persistir el evento terminal del escaneo."
    elif event is not None:
        result["ledger_event_id"] = event.get("event_id")
    return result


def scan_target(target, timeout=45, authorized=False, authorization_id=None,
                require_ledger=False, templates_path=None, severity=None,
                rate_limit=2, concurrency=2):
    """Ejecuta Nuclei solo con un permiso local, específico y vigente."""
    target = validate_target(target)
    if not isinstance(require_ledger, bool):
        raise TypeError("require_ledger debe ser booleano.")
    if type(timeout) is not int or not 5 <= timeout <= 3600:
        raise ValueError("timeout debe estar entre 5 y 3600 segundos.")
    if type(rate_limit) is not int or not 1 <= rate_limit <= 20:
        raise ValueError("rate_limit debe estar entre 1 y 20 solicitudes por segundo.")
    if type(concurrency) is not int or not 1 <= concurrency <= 10:
        raise ValueError("concurrency debe estar entre 1 y 10.")
    allowed_severities = {"info", "low", "medium", "high", "critical"}
    selected_severity = severity or "info,low,medium,high,critical"
    if not isinstance(selected_severity, str) or not selected_severity or not set(selected_severity.split(",")).issubset(allowed_severities):
        raise ValueError("severity contiene valores no permitidos.")
    started = time.monotonic()
    start_event_id = None
    if authorized is not True or not authorization_id:
        result = {
            "target": target,
            "status": "authorization_required",
            "error": "Se requiere confirmación e identificador de autorización.",
            "findings": [],
        }
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
    try:
        grant = authorize_target(target, "nuclei_scan", authorization_id)
    except AuthorizationError as error:
        result = {
            "target": target,
            "status": "authorization_denied",
            "error": str(error),
            "findings": [],
        }
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
    executable = shutil.which("nuclei")

    if not executable:
        result = {
            "target": target,
            "status": "error",
            "error": "Nuclei no se encuentra en el PATH.",
            "findings": [],
        }
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)

    template_root = Path(
        templates_path or os.environ.get(
            "CYBER_AI_NUCLEI_TEMPLATES",
            Path.home() / "nuclei-templates" / "http",
        )
    ).expanduser()
    if template_root.is_symlink():
        result = {"target": target, "status": "error",
                  "error": "El directorio de plantillas no puede ser un enlace simbólico.",
                  "findings": []}
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
    try:
        template_root = template_root.resolve(strict=True)
    except OSError:
        result = {"target": target, "status": "error",
                  "error": "No se encontró el directorio de plantillas HTTP. Instala las plantillas o configura CYBER_AI_NUCLEI_TEMPLATES.",
                  "findings": []}
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
    if (not template_root.is_dir()
            or any(item.is_symlink() for item in template_root.rglob("*"))
            or not any(template_root.rglob("*.yaml"))):
        result = {"target": target, "status": "error",
                  "error": "El directorio de plantillas no contiene archivos YAML.",
                  "findings": []}
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    scan_id = uuid.uuid4().hex
    output_file = output_dir / f"nuclei_scan_{scan_id}.jsonl"

    start_event_id = _record_scan_start(target, authorization_id)
    if require_ledger and start_event_id is None:
        return {
            "target": target, "status": "ledger_error",
            "error": "Escaneo bloqueado: no se pudo registrar el inicio en el ledger.",
            "findings": [],
        }

    command = [
        executable, "-u", target, "-t", str(template_root),
        "-severity", selected_severity, "-type", "http",
        "-exclude-tags", "dos,intrusive,fuzz,code,headless",
        "-disable-unsigned-templates", "-no-stdin", "-jsonl", "-stats",
        "-stats-interval", "5", "-no-interactsh",
        "-disable-update-check", "-disable-redirects",
        "-rl", str(rate_limit), "-c", str(concurrency),
        "-timeout", "5", "-retries", "1", "-max-host-error", "5",
        "-o", str(output_file.resolve()),
    ]

    print("\n[1/4] Preparando escaneo", flush=True)
    print(f"Objetivo: {target}", flush=True)
    print(f"Plantillas: {template_root}", flush=True)
    print(f"Severidades: {selected_severity}; límite: {rate_limit} req/s; concurrencia: {concurrency}.", flush=True)
    print("[2/4] Iniciando Nuclei. La salida aparecerá debajo.", flush=True)

    messages = []

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=(os.name == "posix"),
        )

        def show_output():
            """Muestra cada mensaje de Nuclei conforme llega."""
            if process.stdout is None:
                return

            for line in process.stdout:
                line = line.rstrip()
                if line:
                    if len(messages) < 100:
                        messages.append(line[:2000])
                    print(f"[Nuclei] {line[:2000]}", flush=True)

        reader = threading.Thread(target=show_output, daemon=True)
        reader.start()

        while process.poll() is None:
            elapsed = int(time.monotonic() - started)
            print(
                f"\r[En curso] Tiempo transcurrido: {elapsed}s",
                end="",
                flush=True,
            )

            if elapsed >= timeout:
                _terminate_process_tree(process)
                print("\n[Tiempo agotado] Se detuvo el escaneo.", flush=True)
                result = {
                    "target": target,
                    "status": "timeout",
                    "error": f"El escaneo superó {timeout} segundos.",
                    "findings": [],
                }
                return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)

            time.sleep(1)

        reader.join(timeout=3)
        elapsed = round(time.monotonic() - started, 1)
        print(f"\n[3/4] Escaneo terminado en {elapsed} segundos.", flush=True)

    except OSError as error:
        result = {
            "target": target,
            "status": "error",
            "error": str(error),
            "findings": [],
        }
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)

    findings = []
    malformed_findings_lines = 0
    if output_too_large:
        malformed_findings_lines = 1
    elif output_file.is_file():
        for line in output_file.read_text(encoding="utf-8").splitlines():
            try:
                parsed_finding = json.loads(line)
                if isinstance(parsed_finding, dict):
                    findings.append(parsed_finding)
                else:
                    malformed_findings_lines += 1
            except json.JSONDecodeError:
                malformed_findings_lines += 1

    output_too_large = output_file.is_file() and output_file.stat().st_size > 25_000_000
    status = "evidence_rejected" if output_too_large else ("completed" if process.returncode == 0 else "scanner_error")

    print(f"[4/4] Hallazgos registrados: {len(findings)}", flush=True)
    print(f"Estado final: {status}", flush=True)

    result = {
        "target": target,
        "authorization": grant,
        "status": status,
        "return_code": process.returncode,
        "elapsed_seconds": elapsed,
        "findings_count": len(findings),
        "malformed_findings_lines": malformed_findings_lines,
        "template_directory": str(template_root),
        "severity_filter": selected_severity,
        "rate_limit": rate_limit,
        "concurrency": concurrency,
        "output_too_large": output_too_large,
        "findings": findings,
        "scanner_messages": messages[-100:],
        "note": (
            "Los hallazgos son indicios que requieren validación manual. "
            "Cero hallazgos no demuestra que el objetivo sea seguro."
        ),
    }
    return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
