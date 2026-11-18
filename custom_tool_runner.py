"""Runner argv-only para herramientas personalizadas aprobadas."""
import hashlib
import os
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from tool_adapters import (
    MAX_OUTPUT_BYTES, ToolExecutionError, _confined_path, _hash_binary, _hash_target,
)
from tool_allowlist import ToolAllowlistError, verify_tool_allowed


def run_custom_tool(spec, target, *, allow_external=False, timeout=None):
    tool_id = spec["id"]
    path = _confined_path(target, allow_external=allow_external)
    executable = shutil.which(spec["executable"])
    if not executable:
        candidate = Path(spec["executable"])
        if candidate.is_absolute() and candidate.is_file():
            executable = str(candidate)
    if not executable:
        raise ToolExecutionError("El ejecutable personalizado no está instalado o no se encuentra.")
    provenance = _hash_binary(executable)
    try:
        allowlist = verify_tool_allowed(tool_id, provenance["sha256"])
    except ToolAllowlistError as error:
        raise ToolExecutionError(
            "El binario personalizado no está aprobado por la allowlist firmada."
        ) from error
    executable = provenance["resolved_path"]
    argv = [arg.replace("{target}", str(path)) for arg in spec["argv"]]
    if any("{" in arg or "}" in arg for arg in argv):
        raise ToolExecutionError("Solo se permite el marcador {target} en argv.")
    limit = spec.get("timeout_seconds", 180) if timeout is None else timeout
    if type(limit) is not int or not 1 <= limit <= 600:
        raise ToolExecutionError("Timeout personalizado fuera de rango.")
    before = _hash_target(path)
    started = time.monotonic()
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    truncated = {"value": False}

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
                truncated["value"] = True

    command = [executable, *argv]
    timed_out = False
    return_code = None
    try:
        with tempfile.TemporaryDirectory(prefix="cyber-ai-custom-home-") as isolated_home:
            if os.name == "posix":
                os.chmod(isolated_home, 0o700)
            safe_path_entries = [str(Path(executable).parent)]
            safe_path_entries.extend(
                entry for entry in os.defpath.split(os.pathsep) if entry
            )
            env = {
                "PATH": os.pathsep.join(dict.fromkeys(safe_path_entries)),
                "HOME": isolated_home,
                "TMPDIR": isolated_home,
                "TEMP": isolated_home,
                "TMP": isolated_home,
                "XDG_CONFIG_HOME": str(Path(isolated_home) / "config"),
                "XDG_CACHE_HOME": str(Path(isolated_home) / "cache"),
                "PYTHONNOUSERSITE": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "NO_COLOR": "1",
            }
            if os.name == "nt":
                for variable in ("SYSTEMROOT", "WINDIR", "PATHEXT", "COMSPEC"):
                    if os.environ.get(variable):
                        env[variable] = os.environ[variable]
                env["USERPROFILE"] = isolated_home
                env["APPDATA"] = str(Path(isolated_home) / "AppData" / "Roaming")
                env["LOCALAPPDATA"] = str(Path(isolated_home) / "AppData" / "Local")
            process = subprocess.Popen(
                command, cwd=str(Path(__file__).resolve().parent),
                env=env, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=False, start_new_session=(os.name == "posix"),
            )
            readers = [
                threading.Thread(target=drain, args=(process.stdout, "stdout"), daemon=True),
                threading.Thread(target=drain, args=(process.stderr, "stderr"), daemon=True),
            ]
            for reader in readers:
                reader.start()
            try:
                return_code = process.wait(timeout=limit)
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
                return_code = None
            for reader in readers:
                reader.join(timeout=5)
            if any(reader.is_alive() for reader in readers):
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                elif process.poll() is None:
                    process.kill()
                if process.poll() is None:
                    process.wait()
                for reader in readers:
                    reader.join(timeout=5)
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass
            for reader in readers:
                reader.join(timeout=1)
    except OSError as exc:
        raise ToolExecutionError("No se pudo iniciar la herramienta personalizada.") from exc

    after = _hash_target(path)
    try:
        binary_after = _hash_binary(executable)["sha256"]
    except ToolExecutionError:
        binary_after = None
    target_modified = before != after
    binary_modified = provenance["sha256"] != binary_after
    status = "timeout" if timed_out else "completed"
    if target_modified or binary_modified:
        status = "integrity_error"
    return {
        "schema_version": "1.0", "tool": tool_id,
        "tool_version": "custom-configured", "tool_binary_path": executable,
        "tool_binary_sha256": provenance["sha256"], "tool_binary_sha256_after": binary_after,
        "tool_binary_modified": binary_modified, "tool_allowlist": allowlist,
        "target": str(path), "target_sha256": before, "target_sha256_after": after,
        "target_modified": target_modified,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 3), "status": status,
        "return_code": return_code,
        "tool_reported_success": return_code == 0 and not timed_out and not target_modified and not binary_modified,
        "output_truncated": truncated["value"],
        "stdout": captured["stdout"].decode("utf-8", errors="replace"),
        "stderr": captured["stderr"].decode("utf-8", errors="replace"),
        "parsed_json": None, "command": argv,
        "network_access": "not_enforced", "network_isolation_enforced": False,
        "note": "Herramienta personalizada argv-only; el aislamiento de red no está impuesto por este runner.",
    }
