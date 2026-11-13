"""Adaptadores de análisis local con ejecución acotada y evidencia estructurada.

No instala herramientas ni usa shell. pip-audit queda bloqueado porque su
consulta de vulnerabilidades requiere red y aún no existe una política de red
específica para ese servicio.
"""
import hashlib
import json
import os
import shutil
import signal
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
MAX_OUTPUT_BYTES = 2_000_000
MAX_TARGET_BYTES = 100_000_000
MAX_TARGET_FILES = 10_000
DEFAULT_TIMEOUT = 180
TOOL_SPECS = {
    "semgrep": {"binary": "semgrep", "network": False, "timeout": 180},
    "bandit": {"binary": "bandit", "network": False, "timeout": 180},
    "ruff": {"binary": "ruff", "network": False, "timeout": 120},
    "syft": {"binary": "syft", "network": False, "timeout": 180},
    "trivy": {"binary": "trivy", "network": False, "timeout": 240},
    "pip_audit": {"binary": "pip-audit", "network": True, "timeout": 180},
}


class ToolExecutionError(RuntimeError):
    """A safe tool execution could not be completed."""


def _confined_path(target):
    candidate = Path(target)
    if candidate.is_symlink():
        raise ToolExecutionError("No se permiten enlaces simbólicos como objetivo.")
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(PROJECT_ROOT.resolve())
    except (OSError, ValueError) as exc:
        raise ToolExecutionError("La ruta debe existir y permanecer dentro del repositorio.") from exc
    if not (resolved.is_file() or resolved.is_dir()):
        raise ToolExecutionError("El objetivo debe ser un archivo o directorio.")
    return resolved


def _hash_target(path):
    digest = hashlib.sha256()
    files = [path] if path.is_file() else sorted(
        item for item in path.rglob("*")
        if item.is_file() and not item.is_symlink()
    )
    if path.is_dir():
        for item in path.rglob("*"):
            if item.is_symlink():
                raise ToolExecutionError("El objetivo contiene enlaces simbólicos; análisis bloqueado.")
    if len(files) > MAX_TARGET_FILES:
        raise ToolExecutionError("El objetivo supera el límite de archivos.")
    total_bytes = sum(item.stat().st_size for item in files)
    if total_bytes > MAX_TARGET_BYTES:
        raise ToolExecutionError("El objetivo supera el límite de tamaño de análisis.")
    for item in files:
        try:
            digest.update(item.relative_to(path if path.is_dir() else path.parent).as_posix().encode())
            with item.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
        except OSError as exc:
            raise ToolExecutionError("No se pudo calcular la huella del objetivo.") from exc
    return digest.hexdigest()


def _build_command(tool_id, binary, target, config_path=None):
    if tool_id == "semgrep":
        if not config_path:
            raise ToolExecutionError("Semgrep requiere una configuración local explícita; no se descargan reglas.")
        config = _confined_path(config_path)
        if not config.is_file():
            raise ToolExecutionError("La configuración de Semgrep debe ser un archivo local.")
        return [binary, "scan", "--json", "--metrics=off", "--config", str(config), str(target)]
    if tool_id == "bandit":
        return [binary, "-r", str(target), "-f", "json", "-q"]
    if tool_id == "ruff":
        return [binary, "check", "--output-format=json", str(target)]
    if tool_id == "syft":
        return [binary, "scan", "dir:" + str(target), "-o", "json"]
    if tool_id == "trivy":
        return [
            binary, "fs", "--format", "json",
            "--scanners", "vuln,misconfig,secret",
            "--offline-scan", "--skip-db-update", "--skip-java-db-update",
            "--skip-check-update", "--no-progress", str(target),
        ]
    raise ToolExecutionError("Herramienta sin adaptador ejecutable.")


def run_local_tool(tool_id, target, *, config_path=None, timeout=None):
    """Ejecuta un adaptador local; pip-audit se deniega por requerir red."""
    if tool_id not in TOOL_SPECS:
        raise ToolExecutionError("Herramienta no registrada.")
    spec = TOOL_SPECS[tool_id]
    if spec["network"]:
        raise ToolExecutionError(
            "pip-audit requiere consultar un servicio remoto; ejecución bloqueada "
            "hasta disponer de autorización de red específica y auditable."
        )
    path = _confined_path(target)
    binary = shutil.which(spec["binary"])
    if not binary:
        raise ToolExecutionError("La herramienta no está instalada o no está en PATH.")
    limit = spec["timeout"] if timeout is None else timeout
    if not isinstance(limit, int) or not 1 <= limit <= 600:
        raise ToolExecutionError("El timeout debe estar entre 1 y 600 segundos.")
    command = _build_command(tool_id, binary, path, config_path=config_path)
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
    }
    started = time.monotonic()
    timestamp = datetime.now(timezone.utc).isoformat()
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    stream_truncated = {"value": False}

    def drain(stream, key):
        cap = MAX_OUTPUT_BYTES // 2
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            remaining = cap - len(captured[key])
            if remaining > 0:
                captured[key].extend(chunk[:remaining])
            if len(chunk) > remaining:
                stream_truncated["value"] = True

    try:
        process = subprocess.Popen(
            command, cwd=str(PROJECT_ROOT), env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False,
            start_new_session=(os.name == "posix"),
        )
        readers = [
            threading.Thread(target=drain, args=(process.stdout, "stdout"), daemon=True),
            threading.Thread(target=drain, args=(process.stderr, "stderr"), daemon=True),
        ]
        for reader in readers:
            reader.start()
        timed_out = False
        try:
            returncode = process.wait(timeout=limit)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            process.wait()
            returncode = None
        for reader in readers:
            reader.join(timeout=5)
        status = "timeout" if timed_out else (
            "completed" if returncode == 0 else "findings_or_tool_error"
        )
    except OSError as exc:
        raise ToolExecutionError("No se pudo iniciar el ejecutable.") from exc

    out_text = captured["stdout"].decode("utf-8", errors="replace")
    err_text = captured["stderr"].decode("utf-8", errors="replace")
    truncated = stream_truncated["value"]
    try:
        parsed = json.loads(out_text) if out_text.strip() else None
    except json.JSONDecodeError:
        parsed = None
    evidence = {
        "schema_version": "1.0",
        "tool": tool_id,
        "tool_version": "not_probed",
        "target": str(path.relative_to(PROJECT_ROOT)),
        "target_sha256": _hash_target(path),
        "started_at": timestamp,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "status": status,
        "return_code": returncode,
        "output_truncated": truncated,
        "stdout": out_text,
        "stderr": err_text,
        "parsed_json": parsed,
        "command": command[1:],
        "network_access": False,
        "note": "Salida de herramienta no confiable; requiere validación antes de generar hallazgos o Skills.",
    }
    return evidence


def write_evidence(evidence, output_dir="reports/tool_evidence"):
    raw = Path(output_dir)
    if not raw.is_absolute():
        raw = PROJECT_ROOT / raw
    raw.mkdir(parents=True, exist_ok=True)
    destination = _confined_path(raw)
    if not destination.is_dir():
        raise ToolExecutionError("El destino de evidencias debe ser un directorio.")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = destination / (evidence["tool"] + "_" + stamp + ".json")
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


__all__ = ["TOOL_SPECS", "ToolExecutionError", "run_local_tool", "write_evidence"]
