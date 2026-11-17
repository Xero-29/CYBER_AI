"""Adaptadores de análisis local con ejecución acotada y evidencia estructurada.

No instala herramientas ni usa shell. pip-audit queda bloqueado porque su
consulta de vulnerabilidades requiere red y aún no existe una política de red
específica para ese servicio.
"""
import hashlib
import json
import os
import re
import shutil
import stat
import uuid
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
    "semgrep": {"binary": "semgrep", "network": False, "timeout": 180, "version_args": ["--version"]},
    "bandit": {"binary": "bandit", "network": False, "timeout": 180, "version_args": ["--version"]},
    "ruff": {"binary": "ruff", "network": False, "timeout": 120, "version_args": ["--version"]},
    "syft": {"binary": "syft", "network": False, "timeout": 180, "version_args": ["version"]},
    "trivy": {"binary": "trivy", "network": False, "timeout": 240, "version_args": ["--version"]},
    "pip_audit": {"binary": "pip-audit", "network": True, "timeout": 180},
    "checkov": {"binary": "checkov", "network": False, "timeout": 180, "version_args": ["--version"]},
    "detect_secrets": {"binary": "detect-secrets", "network": False, "timeout": 120, "version_args": ["--version"]},
    "hadolint": {"binary": "hadolint", "network": False, "timeout": 60, "version_args": ["--version"]},
    "shellcheck": {"binary": "shellcheck", "network": False, "timeout": 120, "version_args": ["--version"]},
    "actionlint": {"binary": "actionlint", "network": False, "timeout": 60, "version_args": ["-version"]},
    "kube_linter": {"binary": "kube-linter", "network": False, "timeout": 120, "version_args": ["version"]},
    "yara": {"binary": "yara", "network": False, "requires_isolation": True, "timeout": 180, "version_args": ["--version"]},
    "tshark": {"binary": "tshark", "network": False, "requires_isolation": True, "timeout": 180, "version_args": ["--version"]},
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
        return [binary, "check", "--no-cache", "--output-format=json", str(target)]
    if tool_id == "syft":
        return [binary, "scan", "dir:" + str(target), "-o", "json"]
    if tool_id == "trivy":
        return [
            binary, "fs", "--format", "json",
            "--scanners", "vuln,misconfig,secret",
            "--offline-scan", "--skip-db-update", "--skip-java-db-update",
            "--skip-check-update", "--no-progress", str(target),
        ]
    if tool_id == "checkov":
        mode = ["-d", str(target)] if target.is_dir() else ["-f", str(target)]
        return [binary, *mode, "--output", "json", "--quiet"]
    if tool_id == "detect_secrets":
        if not target.is_dir():
            raise ToolExecutionError("detect-secrets requiere un directorio de repositorio.")
        return [binary, "scan", "--all-files", str(target)]
    if tool_id in {"hadolint", "shellcheck", "actionlint"}:
        if target.is_file():
            files = [target]
        elif tool_id == "hadolint":
            files = sorted(p for p in target.rglob("Dockerfile") if p.is_file() and not p.is_symlink())
        elif tool_id == "shellcheck":
            files = sorted(p for p in target.rglob("*") if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".sh", ".bash"})
        else:
            files = sorted(p for p in target.rglob("*") if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".yml", ".yaml"})
        if not files:
            raise ToolExecutionError("No se encontraron archivos compatibles con la herramienta.")
        if tool_id == "hadolint":
            return [binary, "--format", "json", *map(str, files)]
        if tool_id == "shellcheck":
            return [binary, "--format=json", *map(str, files)]
        return [binary, "-oneline", *map(str, files)]
    if tool_id == "kube_linter":
        return [binary, "lint", str(target), "--format", "json"]
    if tool_id == "yara":
        if not config_path:
            raise ToolExecutionError("YARA requiere un archivo de reglas local explícito.")
        rules = _confined_path(config_path)
        if not rules.is_file():
            raise ToolExecutionError("Las reglas YARA deben ser un archivo local.")
        return [binary, "-r", str(rules), str(target)]
    if tool_id == "tshark":
        if not target.is_file() or target.suffix.lower() not in {".pcap", ".pcapng", ".cap"}:
            raise ToolExecutionError("tshark requiere un archivo PCAP/PCAPNG local.")
        return [binary, "-r", str(target), "-T", "json"]
    raise ToolExecutionError("Herramienta sin adaptador ejecutable.")


def _hash_binary(binary):
    """Resuelve el ejecutable real y calcula su SHA-256 para trazabilidad."""
    try:
        resolved = Path(binary).resolve(strict=True)
        if not resolved.is_file():
            raise ToolExecutionError("El ejecutable resuelto no es un archivo regular.")
        digest = hashlib.sha256()
        with resolved.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return {"resolved_path": str(resolved), "sha256": digest.hexdigest()}
    except OSError as exc:
        raise ToolExecutionError("No se pudo verificar la identidad del ejecutable.") from exc


def _probe_tool_version(binary, tool_id, env):
    """Obtiene la versión instalada sin shell ni acceso de red intencional."""
    arguments = TOOL_SPECS[tool_id].get("version_args", ["--version"])
    try:
        result = subprocess.run(
            [binary, *arguments], cwd=str(PROJECT_ROOT), env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, timeout=5,
            shell=False, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"
    if result.returncode != 0 or not result.stdout.strip():
        return "unknown"
    return result.stdout.strip().splitlines()[0][:256]


def run_local_tool(tool_id, target, *, config_path=None, timeout=None):
    """Ejecuta un adaptador local; no aplica aislamiento de red al proceso."""
    if tool_id not in TOOL_SPECS:
        raise ToolExecutionError("Herramienta no registrada.")
    spec = TOOL_SPECS[tool_id]
    if spec.get("requires_isolation"):
        raise ToolExecutionError(
            "La herramienta analiza muestras o capturas y requiere un sandbox aislado; "
            "la ejecución directa en el host está bloqueada."
        )
    if spec["network"]:
        raise ToolExecutionError(
            "pip-audit requiere consultar un servicio remoto; ejecución bloqueada "
            "hasta disponer de autorización de red específica y auditable."
        )
    path = _confined_path(target)
    binary = shutil.which(spec["binary"])
    if not binary:
        raise ToolExecutionError("La herramienta no está instalada o no está en PATH.")
    binary_provenance = _hash_binary(binary)
    binary = binary_provenance["resolved_path"]
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
    tool_version = _probe_tool_version(binary, tool_id, env)
    if _hash_binary(binary)["sha256"] != binary_provenance["sha256"]:
        raise ToolExecutionError("El ejecutable cambió durante la identificación de versión.")
    target_hash_before = _hash_target(path)
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
        status = "timeout" if timed_out else "completed"
    except OSError as exc:
        raise ToolExecutionError("No se pudo iniciar el ejecutable.") from exc

    out_text = captured["stdout"].decode("utf-8", errors="replace")
    err_text = captured["stderr"].decode("utf-8", errors="replace")
    truncated = stream_truncated["value"]
    try:
        parsed = json.loads(out_text) if out_text.strip() else None
    except json.JSONDecodeError:
        parsed = None
    target_hash_after = _hash_target(path)
    try:
        binary_hash_after = _hash_binary(binary)["sha256"]
    except ToolExecutionError:
        binary_hash_after = None
    binary_modified = binary_hash_after != binary_provenance["sha256"]
    if binary_modified:
        status = "integrity_error"
    evidence = {
        "schema_version": "1.0",
        "tool": tool_id,
        "tool_version": tool_version,
        "tool_binary_path": binary_provenance["resolved_path"],
        "tool_binary_sha256": binary_provenance["sha256"],
        "tool_binary_sha256_after": binary_hash_after,
        "tool_binary_modified": binary_modified,
        "target": str(path.relative_to(PROJECT_ROOT)),
        "target_sha256": target_hash_before,
        "target_sha256_after": target_hash_after,
        "target_modified": target_hash_before != target_hash_after,
        "started_at": timestamp,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "status": status,
        "return_code": returncode,
        "tool_reported_success": returncode == 0 and not binary_modified,
        "output_truncated": truncated,
        "stdout": out_text,
        "stderr": err_text,
        "parsed_json": parsed,
        "command": command[1:],
        "network_access": "not_enforced",
        "network_isolation_enforced": False,
        "network_policy": "Los adaptadores que requieren red se deniegan; el egress de procesos locales no está aislado por este ejecutor.",
        "note": "Salida de herramienta no confiable; requiere validación antes de generar hallazgos o Skills. La ejecución no sustituye aislamiento del sistema operativo.",
    }
    return evidence


def write_evidence(evidence, output_dir="reports/tool_evidence", *, allow_external=False):
    raw = Path(output_dir)
    if not raw.is_absolute():
        raw = PROJECT_ROOT / raw
    if raw.is_symlink():
        raise ToolExecutionError("El destino de evidencias no puede ser un enlace simbólico.")
    try:
        raw.mkdir(parents=True, exist_ok=True, mode=0o700)
        if raw.is_symlink():
            raise ToolExecutionError("El destino de evidencias no puede ser un enlace simbólico.")
        if allow_external:
            destination = raw.resolve(strict=True)
            if not destination.is_dir():
                raise ToolExecutionError("El destino de evidencias debe ser un directorio.")
        else:
            destination = _confined_path(raw)
            if not destination.is_dir():
                raise ToolExecutionError("El destino de evidencias debe ser un directorio.")

        # Tool output may contain sensitive paths or data. Keep the directory
        # private on POSIX and create every evidence file with mode 0600.
        if os.name == "posix":
            os.chmod(destination, 0o700)
            directory_mode = stat.S_IMODE(
                destination.stat(follow_symlinks=False).st_mode
            )
            if directory_mode & 0o077:
                raise ToolExecutionError("El directorio de evidencias no es privado.")
        tool = evidence.get("tool") if isinstance(evidence, dict) else None
        if not isinstance(tool, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", tool):
            raise ToolExecutionError("Identificador de herramienta inválido para el nombre de evidencia.")

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        token = uuid.uuid4().hex
        path = destination / f"{tool}_{stamp}_{token}.json"
        temporary = destination / f".{tool}_{stamp}_{token}.tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary, flags, 0o600)
        try:
            if os.name == "posix":
                os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                descriptor = -1
                stream.write(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            # Publish only a fully written file; destination directory is private.
            os.replace(temporary, path)
            if os.name == "posix":
                directory_fd = os.open(destination, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        except Exception:
            if descriptor >= 0:
                os.close(descriptor)
            temporary.unlink(missing_ok=True)
            raise
        return path
    except ToolExecutionError:
        raise
    except OSError as error:
        raise ToolExecutionError("No se pudo escribir evidencia protegida.") from error


__all__ = ["TOOL_SPECS", "ToolExecutionError", "run_local_tool", "write_evidence"]
