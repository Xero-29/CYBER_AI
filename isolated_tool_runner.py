"""Ejecución de análisis de muestras dentro de un contenedor Docker endurecido.

El contenedor no recibe red, capacidades, socket Docker ni acceso de escritura
al host. El objetivo y las reglas se montan en solo lectura.
"""
import hashlib
import os
import shutil
import subprocess
import threading
import time
from pathlib import Path

from tool_adapters import ToolExecutionError, _confined_path, _hash_target
from tool_allowlist import verify_tool_allowed

IMAGE_DEFAULT = "cyber-ai-analysis-sandbox:1.0"
MAX_OUTPUT = 2_000_000


def _docker_image_id(docker, image):
    result = subprocess.run(
        [docker, "image", "inspect", "--format", "{{.Id}}", image],
        stdin=subprocess.DEVNULL, capture_output=True, text=True,
        timeout=15, check=False,
    )
    if result.returncode != 0:
        raise ToolExecutionError(
            "No está construida la imagen aislada. Ejecuta sh build-analysis-sandbox.sh."
        )
    value = result.stdout.strip()
    if not value.startswith("sha256:") or len(value) != 71:
        raise ToolExecutionError("Docker devolvió un identificador de imagen inválido.")
    return value.removeprefix("sha256:")


def run_isolated_tool(tool_id, target, *, config_path=None, timeout=180,
                      allow_external=False):
    if os.name != "posix":
        raise ToolExecutionError("El sandbox Docker de análisis está habilitado solo en sistemas POSIX; Windows queda bloqueado hasta su validación.")
    if tool_id not in {"yara", "tshark"}:
        raise ToolExecutionError("La herramienta no está habilitada para el sandbox Docker.")
    path = _confined_path(target, allow_external=allow_external)
    if tool_id == "tshark" and (
        not path.is_file() or path.suffix.lower() not in {".pcap", ".pcapng", ".cap"}
    ):
        raise ToolExecutionError("tshark requiere un archivo PCAP/PCAPNG/CAP.")
    rules = None
    if tool_id == "yara":
        if not config_path:
            raise ToolExecutionError("YARA requiere reglas locales explícitas.")
        rules = _confined_path(config_path, allow_external=allow_external)
        if not rules.is_file():
            raise ToolExecutionError("El archivo de reglas YARA debe ser un archivo regular.")
    if type(timeout) is not int or not 1 <= timeout <= 600:
        raise ToolExecutionError("Timeout aislado fuera de rango.")
    docker = shutil.which("docker")
    if not docker:
        raise ToolExecutionError("Docker no está instalado o no está en PATH; ejecución aislada bloqueada.")
    image = os.environ.get("CYBER_AI_ANALYSIS_SANDBOX_IMAGE", IMAGE_DEFAULT)
    image_id = _docker_image_id(docker, image)
    allowlist = verify_tool_allowed(tool_id, image_id)
    before = _hash_target(path)
    started = time.monotonic()
    if os.name == "posix" and hasattr(os, "getuid") and os.getuid() != 0:
        container_user = f"{os.getuid()}:{os.getgid()}"
    else:
        container_user = "65532:65532"
    command = [
        docker, "run", "--rm", "--pull=never",
        "--network=none", "--read-only", "--cap-drop=ALL",
        "--security-opt=no-new-privileges", "--pids-limit=64",
        "--memory=1g", "--cpus=1.0", "--user=" + container_user,
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=64m",
        "--mount", "type=bind,src=" + str(path) + ",dst=" +
            ("/input" if path.is_dir() else "/input/target") + ",readonly",
    ]
    if rules is not None:
        command.extend([
            "--mount", "type=bind,src=" + str(rules) + ",dst=/rules/rules.yar,readonly",
        ])
    command.append(image)
    if tool_id == "yara":
        command.extend(["yara", "-r", "/rules/rules.yar", "/input"])
    else:
        command.extend(["tshark", "-r", "/input/target", "-T", "json"])

    captured = {"stdout": bytearray(), "stderr": bytearray()}
    truncated = {"value": False}

    def drain(stream, key):
        cap = MAX_OUTPUT // 2
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            remaining = cap - len(captured[key])
            if remaining > 0:
                captured[key].extend(chunk[:remaining])
            if len(chunk) > remaining:
                truncated["value"] = True

    process = None
    try:
        process = subprocess.Popen(
            command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False, start_new_session=(os.name == "posix"),
        )
        readers = [
            threading.Thread(target=drain, args=(process.stdout, "stdout"), daemon=True),
            threading.Thread(target=drain, args=(process.stderr, "stderr"), daemon=True),
        ]
        for reader in readers:
            reader.start()
        timed_out = False
        try:
            return_code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "posix":
                import signal
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
        raise ToolExecutionError("No se pudo iniciar Docker para el análisis aislado.") from exc

    after = _hash_target(path)
    modified = before != after
    status = "timeout" if timed_out else "completed"
    if modified:
        status = "integrity_error"
    return {
        "schema_version": "1.0", "tool": tool_id,
        "tool_version": image, "tool_binary_path": "docker-image:" + image,
        "tool_binary_sha256": image_id, "tool_binary_sha256_after": image_id,
        "tool_binary_modified": False, "tool_allowlist": allowlist,
        "target": str(path), "target_sha256": before, "target_sha256_after": after,
        "target_modified": modified,
        "started_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "status": status, "return_code": return_code,
        "tool_reported_success": return_code == 0 and not timed_out and not modified,
        "output_truncated": truncated["value"],
        "stdout": captured["stdout"].decode("utf-8", errors="replace"),
        "stderr": captured["stderr"].decode("utf-8", errors="replace"),
        "parsed_json": None, "network_access": "disabled_by_docker_network_none",
        "network_isolation_enforced": True,
        "isolation": {
            "runtime": "docker", "image": image, "image_id": "sha256:" + image_id,
            "network": "none", "root_filesystem": "read_only",
            "target_mount": "read_only", "capabilities": "dropped_all",
            "no_new_privileges": True, "pids_limit": 64, "memory_limit": "1g",
            "cpu_limit": 1.0, "docker_socket_mounted": False,
        },
    }
