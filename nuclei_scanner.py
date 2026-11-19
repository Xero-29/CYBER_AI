#!/usr/bin/env python3
"""Escaneo defensivo con Nuclei y seguimiento visible del progreso."""

import json
import os
import signal
import stat
import tempfile
import uuid
import shutil
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path
from urllib.parse import urlparse

from execution_policy import AuthorizationError, authorize_target
from execution_ledger import ExecutionLedger
from binary_integrity import (
    BinaryIntegrityError,
    build_minimal_environment,
    hash_executable,
    require_approved_executable,
)
from safe_io import SafeWriteError, ensure_private_directory


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
    event = _record_scan_event(
        target, result, started, authorization_id=authorization_id,
        start_event_id=start_event_id,
    )
    if require_ledger and event is None:
        result["status"] = "ledger_error"
        result["ledger_error"] = "No se pudo persistir el evento terminal del escaneo."
    return result


def scan_target(target, timeout=45, authorized=False, authorization_id=None,
                require_ledger=True):
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

    try:
        binary_provenance = require_approved_executable(executable, "nuclei")
        executable = binary_provenance["resolved_path"]
    except BinaryIntegrityError as error:
        result = {
            "target": target,
            "status": "binary_denied",
            "error": str(error),
            "findings": [],
        }
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)

    try:
        output_dir = ensure_private_directory(Path("reports"))
    except SafeWriteError as error:
        result = {"target": target, "status": "error", "error": str(error), "findings": []}
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
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

    messages = deque(maxlen=100)
    isolated_home = None

    try:
        isolated_home = tempfile.TemporaryDirectory(prefix="cyber-ai-nuclei-")
        if os.name == "posix":
            os.chmod(isolated_home.name, 0o700)
        process_env = build_minimal_environment(isolated_home.name, executable)
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            stdin=subprocess.DEVNULL,
            env=process_env,
            cwd=isolated_home.name,
            close_fds=True,
            start_new_session=(os.name == "posix"),
        )

        def show_output():
            """Muestra cada mensaje de Nuclei conforme llega."""
            if process.stdout is None:
                return

            for line in process.stdout:
                line = line.rstrip()
                if line:
                    safe_line = line[:2000]
                    messages.append(safe_line)
                    print(f"[Nuclei] {safe_line}", flush=True)

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
                try:
                    binary_after = hash_executable(executable)
                    binary_modified = binary_after["sha256"] != binary_provenance["sha256"]
                except BinaryIntegrityError:
                    binary_after = None
                    binary_modified = True
                result = {
                    "target": target,
                    "status": "integrity_error" if binary_modified else "timeout",
                    "error": (
                        "La integridad del binario cambió durante el escaneo."
                        if binary_modified else f"El escaneo superó {timeout} segundos."
                    ),
                    "tool_binary_sha256": binary_provenance["sha256"],
                    "tool_binary_sha256_after": binary_after["sha256"] if binary_after else None,
                    "tool_binary_modified": binary_modified,
                    "tool_allowlist": binary_provenance["allowlist"],
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
            "tool_binary_sha256": binary_provenance["sha256"],
            "tool_allowlist": binary_provenance["allowlist"],
            "findings": [],
        }
        return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
    finally:
        if isolated_home is not None:
            isolated_home.cleanup()

    try:
        binary_after = hash_executable(executable)
        binary_modified = binary_after["sha256"] != binary_provenance["sha256"]
    except BinaryIntegrityError:
        binary_after = None
        binary_modified = True

    findings = []
    output_limit_exceeded = False
    evidence_invalid = False
    if output_file.exists() or output_file.is_symlink():
        try:
            output_info = output_file.lstat()
            if stat.S_ISLNK(output_info.st_mode) or not stat.S_ISREG(output_info.st_mode):
                evidence_invalid = True
            elif output_info.st_size > 20 * 1024 * 1024:
                output_limit_exceeded = True
            else:
                os.chmod(output_file, 0o600, follow_symlinks=False)
                with output_file.open("r", encoding="utf-8") as stream:
                    for line in stream:
                        if len(line.encode("utf-8")) > 1024 * 1024:
                            evidence_invalid = True
                            findings = []
                            break
                        if len(findings) >= 10000:
                            output_limit_exceeded = True
                            findings = []
                            break
                        try:
                            findings.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except OSError:
            evidence_invalid = True

    status = "completed" if process.returncode == 0 else "scanner_error"
    if output_limit_exceeded:
        status = "output_limit_exceeded"
        findings = []
    elif evidence_invalid:
        status = "evidence_invalid"
        findings = []
    discarded_findings = 0
    if binary_modified:
        discarded_findings = len(findings)
        findings = []
        status = "integrity_error"

    print(f"[4/4] Hallazgos registrados: {len(findings)}", flush=True)
    print(f"Estado final: {status}", flush=True)

    result = {
        "target": target,
        "authorization": grant,
        "status": status,
        "return_code": process.returncode,
        "elapsed_seconds": elapsed,
        "tool_binary_sha256": binary_provenance["sha256"],
        "tool_binary_sha256_after": binary_after["sha256"] if binary_after else None,
        "tool_binary_modified": binary_modified,
        "tool_allowlist": binary_provenance["allowlist"],
        "discarded_findings_count": discarded_findings,
        "findings_count": len(findings),
        "findings": findings,
        "scanner_messages": list(messages),
        "note": (
            "Los hallazgos son indicios que requieren validación manual. "
            "Cero hallazgos no demuestra que el objetivo sea seguro."
        ),
    }
    return _finalize_scan(target, result, started, authorization_id, start_event_id, require_ledger)
