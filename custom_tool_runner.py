"""Runner argv-only para herramientas personalizadas aprobadas."""
import hashlib
import os
import shutil
import signal
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from tool_adapters import (
    MAX_OUTPUT_BYTES, ToolExecutionError, _confined_path, _hash_binary, _hash_target,
)
from tool_allowlist import verify_tool_allowed


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
    allowlist = verify_tool_allowed(tool_id, provenance["sha256"])
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
    try:
        process = subprocess.Popen(
            command, cwd=str(Path(__file__).resolve().parent),
            env={"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", ""),
                 "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "NO_COLOR": "1"},
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=False, start_new_session=(os.name == "posix"),
        )
        readers = [threading.Thread(target=drain, args=(process.stdout, "stdout"), daemon=True),
                   threading.Thread(target=drain, args=(process.stderr, "stderr"), daemon=True)]
        for reader in readers:
            reader.start()
        timed_out = False
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
