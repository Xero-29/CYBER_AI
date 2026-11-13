#!/usr/bin/env python3
"""Escaneo defensivo con Nuclei y seguimiento visible del progreso."""

import json
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


def _record_scan_event(target, result, started, *, authorization_id=None):
    """Registra intentos, denegaciones y resultados de Nuclei sin ocultar errores."""
    status = result.get("status")
    ledger_status = (
        "denied" if status in {"authorization_required", "authorization_denied"}
        else "timeout" if status == "timeout"
        else "completed" if status == "completed"
        else "failed"
    )
    try:
        ExecutionLedger().append(
            namespace="security-scans", task=target, status=ledger_status,
            tool="nuclei", evidence=result,
            duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            metadata={"authorization_id": authorization_id, "scanner_status": status},
        )
    except Exception as error:
        print(f"AVISO: no se pudo registrar el escaneo en el ledger: {error}", file=sys.stderr)


def scan_target(target, timeout=45, authorized=False, authorization_id=None):
    """Ejecuta Nuclei solo con un permiso local, específico y vigente."""
    target = validate_target(target)
    started = time.monotonic()
    if authorized is not True or not authorization_id:
        result = {
            "target": target,
            "status": "authorization_required",
            "error": "Se requiere confirmación e identificador de autorización.",
            "findings": [],
        }
        _record_scan_event(target, result, started, authorization_id=authorization_id)
        return result
    try:
        grant = authorize_target(target, "nuclei_scan", authorization_id)
    except AuthorizationError as error:
        result = {
            "target": target,
            "status": "authorization_denied",
            "error": str(error),
            "findings": [],
        }
        _record_scan_event(target, result, started, authorization_id=authorization_id)
        return result
    executable = shutil.which("nuclei")

    if not executable:
        result = {
            "target": target,
            "status": "error",
            "error": "Nuclei no se encuentra en el PATH.",
            "findings": [],
        }
        _record_scan_event(target, result, started, authorization_id=authorization_id)
        return result

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    scan_id = uuid.uuid4().hex
    output_file = output_dir / f"nuclei_scan_{scan_id}.jsonl"

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
                process.kill()
                process.wait()
                print("\n[Tiempo agotado] Se detuvo el escaneo.", flush=True)
                result = {
                    "target": target,
                    "status": "timeout",
                    "error": f"El escaneo superó {timeout} segundos.",
                    "findings": [],
                }
                _record_scan_event(target, result, started, authorization_id=authorization_id)
                return result

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
    _record_scan_event(target, result, started, authorization_id=authorization_id)
    return result
