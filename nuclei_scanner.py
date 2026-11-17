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
                require_ledger=False):
    """Ejecuta Nuclei solo con un permiso local, específico y vigente."""
    target = validate_target(target)
    if not isinstance(require_ledger, bool):
        raise TypeError("require_ledger debe ser booleano.")
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
        executable,
        "-u", target,
        "-t", str(Path.home() / "nuclei-templates/http/technologies/bulma-detect.yaml"),
        "-t", str(Path.home() / "nuclei-templates/http/misconfiguration/http-missing-security-headers.yaml"),
        "-jsonl",
        "-stats",
        "-stats-interval", "5",
        "-no-interactsh",
        "-disable-update-check",
        "-disable-redirects",
        "-rl", "2",
        "-c", "2",
        "-timeout", "5",
        "-retries", "1",
        "-o", str(output_file.resolve()),
    ]

    print("\n[1/4] Preparando escaneo", flush=True)
    print(f"Objetivo: {target}", flush=True)
    print("Límite de solicitudes: 2 por segundo; concurrencia: 2.", flush=True)
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
                    messages.append(line)
                    print(f"[Nuclei] {line}", flush=True)

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
        _record_scan_event(target, result, started, authorization_id=authorization_id)
        return result

    findings = []
    if output_file.is_file():
        for line in output_file.read_text(encoding="utf-8").splitlines():
            try:
                findings.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    status = "completed" if process.returncode == 0 else "scanner_error"

    print(f"[4/4] Hallazgos registrados: {len(findings)}", flush=True)
    print(f"Estado final: {status}", flush=True)

    result = {
        "target": target,
        "authorization": grant,
        "status": status,
        "return_code": process.returncode,
        "elapsed_seconds": elapsed,
        "findings_count": len(findings),
        "findings": findings,
        "scanner_messages": messages[-100:],
        "note": (
            "Los hallazgos son indicios que requieren validación manual. "
            "Cero hallazgos no demuestra que el objetivo sea seguro."
        ),
    }
    return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
