"""Adaptadores locales y de red con alcance explícito y evidencia estructurada.

No instala herramientas ni usa shell. YARA/TShark se ejecutan en Docker aislado.
OSV-Scanner, Grype y Volatility 3 solicitan modo offline; Zeek y Gitleaks
procesan artefactos locales. Nmap requiere autorización y allowlist CIDR.
pip-audit permanece bloqueado hasta disponer de una política de red auditable.
"""
import hashlib
import ipaddress
import xml.etree.ElementTree as ET
import json
import os
import re
import shutil
import stat
import uuid
import signal
import subprocess
import threading
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from tool_allowlist import verify_tool_allowed
from tool_database_preflight import inspect_tool_database


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
    "osv_scanner": {"binary": "osv-scanner", "network": False, "offline_only": True, "local_database_required": True, "timeout": 240, "version_args": ["--version"], "accepted_exit_codes": [0, 1]},
    "grype": {"binary": "grype", "network": False, "offline_only": True, "local_database_required": True, "timeout": 240, "version_args": ["version"]},
    "gitleaks": {"binary": "gitleaks", "network": False, "offline_only": True, "timeout": 180, "version_args": ["version"], "accepted_exit_codes": [0, 1]},
    "zeek": {"binary": "zeek", "network": False, "offline_only": True, "timeout": 300, "version_args": ["--version"], "input_extensions": [".pcap", ".pcapng", ".cap"]},
    "volatility3": {"binary": "vol", "network": False, "offline_only": True, "timeout": 300, "version_args": ["--version"], "allowed_plugins": ["windows.info", "windows.pslist", "windows.pstree", "windows.netscan", "windows.cmdline", "windows.dlllist", "linux.pslist", "linux.pstree", "linux.bash", "linux.lsmod", "linux.mount", "linux.sockstat", "mac.pslist", "mac.lsmod"]},
    "nmap": {"binary": "nmap", "network": True, "scoped_network": True, "timeout": 90, "version_args": ["--version"], "accepted_exit_codes": [0]},
    "yara": {"binary": "yara", "network": False, "requires_isolation": True, "timeout": 180, "version_args": ["--version"]},
    "tshark": {"binary": "tshark", "network": False, "requires_isolation": True, "timeout": 180, "version_args": ["--version"]},
}


class ToolExecutionError(RuntimeError):
    """A safe tool execution could not be completed."""


def _confined_path(target, *, allow_external=False):
    candidate = Path(target)
    if candidate.is_symlink():
        raise ToolExecutionError("No se permiten enlaces simbólicos como objetivo.")
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    try:
        resolved = candidate.resolve(strict=True)
        if not allow_external:
            resolved.relative_to(PROJECT_ROOT.resolve())
    except (OSError, ValueError) as exc:
        message = "La ruta debe existir y permanecer dentro del repositorio." if not allow_external else "La ruta externa debe existir y ser accesible."
        raise ToolExecutionError(message) from exc
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


def _build_command(tool_id, binary, target, config_path=None, plugin=None):
    if tool_id == "osv_scanner":
        return [binary, "--offline", "scan", "source", "-r", str(target), "--format", "json"]
    if tool_id == "grype":
        return [binary, str(target), "-o", "json"]
    if tool_id == "gitleaks":
        if not target.is_dir():
            raise ToolExecutionError("Gitleaks requiere un directorio de repositorio.")
        return [
            binary, "dir", str(target), "--report-format", "json",
            "--redact=100", "--no-banner",
        ]
    if tool_id == "zeek":
        if not target.is_file() or target.suffix.lower() not in {".pcap", ".pcapng", ".cap"}:
            raise ToolExecutionError("Zeek requiere un archivo PCAP/PCAPNG/CAP para análisis offline.")
        return [binary, "-r", str(target), "LogAscii::use_json=T"]
    if tool_id == "volatility3":
        if not target.is_file():
            raise ToolExecutionError("Volatility 3 requiere un volcado de memoria como archivo.")
        if not isinstance(plugin, str) or plugin not in TOOL_SPECS[tool_id]["allowed_plugins"]:
            raise ToolExecutionError("Volatility 3 requiere un plugin explícito de la allowlist.")
        return [binary, "--offline", "-f", str(target), plugin]
    if plugin is not None:
        raise ToolExecutionError("El parámetro plugin solo se admite para Volatility 3.")
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



def _validated_nmap_scope(target):
    """Valida una IP/CIDR pequeña contra una allowlist explícita del operador."""
    if not isinstance(target, str) or not target.strip() or any(ch.isspace() for ch in target):
        raise ToolExecutionError("Nmap requiere una IP o CIDR literal, sin espacios.")
    try:
        if "/" in target:
            requested = ipaddress.ip_network(target, strict=False)
        else:
            address = ipaddress.ip_address(target)
            requested = ipaddress.ip_network(
                f"{address}/{address.max_prefixlen}", strict=True
            )
    except ValueError as error:
        raise ToolExecutionError("Nmap no acepta DNS, argumentos ni objetivos no IP.") from error
    if requested.num_addresses > 16 or requested.network_address.is_multicast or requested.network_address.is_unspecified:
        raise ToolExecutionError("El alcance Nmap debe ser un bloque unicast de máximo 16 direcciones.")

    raw_allowlist = os.environ.get("CYBER_AI_NMAP_ALLOWED_CIDRS", "")
    if not raw_allowlist.strip():
        raise ToolExecutionError(
            "Nmap está bloqueado: configura la allowlist CIDR CYBER_AI_NMAP_ALLOWED_CIDRS con los rangos autorizados."
        )
    allowed = []
    for value in raw_allowlist.split(","):
        value = value.strip()
        if not value:
            continue
        try:
            if "/" in value:
                allowed.append(ipaddress.ip_network(value, strict=False))
            else:
                address = ipaddress.ip_address(value)
                allowed.append(ipaddress.ip_network(
                    f"{address}/{address.max_prefixlen}", strict=True
                ))
        except ValueError as error:
            raise ToolExecutionError("La allowlist CIDR de Nmap contiene una entrada inválida.") from error
    if not allowed or not any(
        requested.version == network.version and requested.subnet_of(network)
        for network in allowed
    ):
        raise ToolExecutionError("El objetivo Nmap no está contenido en la allowlist autorizada.")
    return str(requested), str(requested), hashlib.sha256(
        raw_allowlist.encode("utf-8")
    ).hexdigest()


def _build_nmap_command(binary, target):
    """Escaneo TCP connect acotado; sin NSE, detección OS, DNS ni evasión."""
    return [
        binary, "-sT", "-Pn", "-n", "--top-ports", "100",
        "--max-retries", "1", "--host-timeout", "60s",
        "--max-rate", "25", "-oX", "-", target,
    ]


def _parse_nmap_xml(output):
    try:
        root = ET.fromstring(output)
    except (ET.ParseError, ValueError):
        return None
    hosts = []
    for host in root.findall("host"):
        addresses = [
            item.attrib.get("addr")
            for item in host.findall("address")
            if item.attrib.get("addr")
        ]
        status = host.find("status")
        ports = []
        ports_node = host.find("ports")
        if ports_node is not None:
            for port in ports_node.findall("port"):
                state = port.find("state")
                service = port.find("service")
                ports.append({
                    "protocol": port.attrib.get("protocol"),
                    "port": port.attrib.get("portid"),
                    "state": state.attrib.get("state") if state is not None else None,
                    "service": service.attrib.get("name") if service is not None else None,
                    "product": service.attrib.get("product") if service is not None else None,
                    "version": service.attrib.get("version") if service is not None else None,
                })
        hosts.append({
            "addresses": addresses,
            "status": status.attrib.get("state") if status is not None else None,
            "ports": ports,
        })
    return {"hosts": hosts, "host_count": len(hosts)}



def _run_scoped_nmap(target, spec, *, timeout=None):
    normalized_target, scope, allowlist_hash = _validated_nmap_scope(target)
    limit = spec["timeout"] if timeout is None else timeout
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 180:
        raise ToolExecutionError("El timeout Nmap debe estar entre 1 y 180 segundos.")
    binary = shutil.which(spec["binary"])
    if not binary:
        raise ToolExecutionError("Nmap no está instalado o no está en PATH.")
    provenance = _hash_binary(binary)
    allowlist_evidence = verify_tool_allowed("nmap", provenance["sha256"])
    binary = provenance["resolved_path"]
    # Keep caller credentials and configuration out of host tool processes.
    safe_path_entries = [str(Path(binary).parent)]
    safe_path_entries.extend(
        entry for entry in os.defpath.split(os.pathsep) if entry
    )
    safe_path = os.pathsep.join(dict.fromkeys(safe_path_entries))
    env = {
        "PATH": safe_path,
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
    version = _probe_tool_version(binary, "nmap", env)
    if _hash_binary(binary)["sha256"] != provenance["sha256"]:
        raise ToolExecutionError("El ejecutable Nmap cambió durante la identificación.")
    command = _build_nmap_command(binary, normalized_target)
    started = time.monotonic()
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        result = subprocess.run(
            command, cwd=str(PROJECT_ROOT), env=env,
            stdin=subprocess.DEVNULL, capture_output=True,
            text=True, timeout=limit, shell=False, check=False,
        )
        return_code = result.returncode
        out_text = result.stdout[:MAX_OUTPUT_BYTES]
        err_text = result.stderr[:MAX_OUTPUT_BYTES]
        truncated = len(result.stdout) > MAX_OUTPUT_BYTES or len(result.stderr) > MAX_OUTPUT_BYTES
        status = "completed"
    except subprocess.TimeoutExpired as error:
        return_code = None
        out_text = str(error.stdout or "")[:MAX_OUTPUT_BYTES]
        err_text = str(error.stderr or "")[:MAX_OUTPUT_BYTES]
        truncated = False
        status = "timeout"
    except OSError as error:
        raise ToolExecutionError("No se pudo iniciar Nmap.") from error
    try:
        binary_after = _hash_binary(binary)["sha256"]
    except ToolExecutionError:
        binary_after = None
    binary_modified = binary_after != provenance["sha256"]
    if binary_modified:
        status = "integrity_error"
    parsed = _parse_nmap_xml(out_text)
    return {
        "schema_version": "1.0",
        "tool": "nmap",
        "tool_version": version,
        "tool_binary_path": provenance["resolved_path"],
        "tool_binary_sha256": provenance["sha256"],
        "tool_binary_sha256_after": binary_after,
        "tool_binary_modified": binary_modified,
        "tool_allowlist": allowlist_evidence,
        "target": normalized_target,
        "target_type": "network",
        "target_sha256": None,
        "target_sha256_after": None,
        "target_modified": None,
        "authorization_required": True,
        "scope_validated": True,
        "authorization_scope": scope,
        "scope_allowlist_sha256": allowlist_hash,
        "started_at": timestamp,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "status": status,
        "return_code": return_code,
        "tool_reported_success": (
            status == "completed" and return_code in spec.get("accepted_exit_codes", [0])
            and not binary_modified
        ),
        "findings_present": bool(parsed and any(
            port.get("state") == "open"
            for host in parsed["hosts"] for port in host["ports"]
        )),
        "output_truncated": truncated,
        "stdout": out_text,
        "stderr": err_text,
        "parsed_json": parsed,
        "command": command[1:],
        "network_access": "authorized_active_network_scan",
        "network_isolation_enforced": False,
        "network_policy": "Alcance literal IP/CIDR validado contra CYBER_AI_NMAP_ALLOWED_CIDRS; el proceso host no tiene aislamiento de egress del SO.",
        "note": "Escaneo TCP connect limitado a 100 puertos frecuentes, sin NSE, DNS, detección OS ni técnicas de evasión. Solo ejecutar con autorización explícita del propietario del rango.",
    }



def run_local_tool(
    tool_id, target, *, config_path=None, plugin=None, timeout=None,
    allow_external=False, allow_network=False
):
    """Ejecuta un adaptador con HOME/TMP efímeros y entorno mínimo."""
    with tempfile.TemporaryDirectory(prefix="cyber-ai-tool-home-") as isolated_home:
        if os.name == "posix":
            os.chmod(isolated_home, 0o700)
        return _run_local_tool_with_home(
            tool_id, target, config_path=config_path, plugin=plugin,
            timeout=timeout, allow_external=allow_external,
            allow_network=allow_network, isolated_home=isolated_home,
        )


def _run_local_tool_with_home(
    tool_id, target, *, config_path=None, plugin=None, timeout=None,
    allow_external=False, allow_network=False, isolated_home
):
    """Ejecuta un adaptador local; YARA/TShark se delegan al sandbox Docker."""
    if tool_id not in TOOL_SPECS:
        raise ToolExecutionError("Herramienta no registrada.")
    spec = TOOL_SPECS[tool_id]
    if spec.get("scoped_network"):
        if not allow_network:
            raise ToolExecutionError("Nmap requiere --authorized-network además de la allowlist CIDR.")
        return _run_scoped_nmap(target, spec, timeout=timeout)
    if spec.get("requires_isolation"):
        from isolated_tool_runner import run_isolated_tool
        return run_isolated_tool(
            tool_id, target,
            config_path=config_path or os.environ.get("CYBER_AI_YARA_RULES"),
            timeout=timeout or spec["timeout"],
            allow_external=allow_external,
        )
    if spec["network"]:
        raise ToolExecutionError(
            "pip-audit requiere consultar un servicio remoto; ejecución bloqueada "
            "hasta disponer de autorización de red específica y auditable."
        )
    path = _confined_path(target, allow_external=allow_external)
    binary = shutil.which(spec["binary"])
    if not binary:
        raise ToolExecutionError("La herramienta no está instalada o no está en PATH.")
    binary_provenance = _hash_binary(binary)
    allowlist_evidence = verify_tool_allowed(tool_id, binary_provenance["sha256"])
    binary = binary_provenance["resolved_path"]
    limit = spec["timeout"] if timeout is None else timeout
    if not isinstance(limit, int) or not 1 <= limit <= 600:
        raise ToolExecutionError("El timeout debe estar entre 1 y 600 segundos.")
    if config_path is None and tool_id == "semgrep":
        config_path = os.environ.get("CYBER_AI_SEMGREP_CONFIG")
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
    }
    for variable in (
        "OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY",
        "OSV_SCALIBR_LOCAL_DB_CACHE_DIRECTORY",
        "GRYPE_DB_CACHE_DIR",
        "CYBER_AI_GRYPE_DB_MAX_AGE_DAYS",
    ):
        if os.environ.get(variable):
            env[variable] = os.environ[variable]
    if tool_id == "grype":
        env["GRYPE_DB_AUTO_UPDATE"] = "false"
        env["GRYPE_EXTERNAL_SOURCES_ENABLE"] = "false"
        env["GRYPE_CHECK_FOR_APP_UPDATE"] = "false"
    command = _build_command(
        tool_id, binary, path, config_path=config_path, plugin=plugin
    )
    database_preflight = inspect_tool_database(tool_id, binary, environ=env)
    if database_preflight is not None:
        expected_status = (
            "present_structure_checked" if tool_id == "osv_scanner" else "ready"
        )
        if database_preflight.get("status") != expected_status:
            raise ToolExecutionError(
                f"Preflight de base local de {tool_id} no superado "
                f"({database_preflight.get('status', 'unknown')}); no se inició el escaneo."
            )
    tool_version = _probe_tool_version(binary, tool_id, env)
    if _hash_binary(binary)["sha256"] != binary_provenance["sha256"]:
        raise ToolExecutionError("El ejecutable cambió durante la identificación de versión.")
    target_hash_before = _hash_target(path)
    started = time.monotonic()
    timestamp = datetime.now(timezone.utc).isoformat()
    zeek_workspace = None
    volatility_workspace = None
    working_directory = PROJECT_ROOT
    if tool_id == "volatility3":
        volatility_workspace = tempfile.TemporaryDirectory(prefix="cyber-ai-volatility-")
        env["VOLATILITY_CACHE_PATH"] = volatility_workspace.name
    if tool_id == "zeek":
        zeek_workspace = tempfile.TemporaryDirectory(prefix="cyber-ai-zeek-")
        working_directory = Path(zeek_workspace.name)
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
            command, cwd=str(working_directory), env=env,
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
        if zeek_workspace is not None:
            zeek_workspace.cleanup()
        if volatility_workspace is not None:
            volatility_workspace.cleanup()
        raise ToolExecutionError("No se pudo iniciar el ejecutable.") from exc

    out_text = captured["stdout"].decode("utf-8", errors="replace")
    err_text = captured["stderr"].decode("utf-8", errors="replace")
    truncated = stream_truncated["value"]
    try:
        parsed = json.loads(out_text) if out_text.strip() else None
    except json.JSONDecodeError:
        parsed = None
    if tool_id == "zeek" and zeek_workspace is not None:
        log_data = {}
        total_log_bytes = 0
        for log_path in sorted(working_directory.glob("*.log")):
            if log_path.is_symlink() or not log_path.is_file():
                continue
            remaining = MAX_OUTPUT_BYTES - total_log_bytes
            if remaining <= 0:
                truncated = True
                break
            log_size = log_path.stat().st_size
            with log_path.open("rb") as log_stream:
                raw = log_stream.read(remaining)
            total_log_bytes += len(raw)
            if log_size > len(raw):
                truncated = True
            entries = []
            for line in raw.decode("utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    entries.append({"unparsed_line": line[:4096]})
            log_data[log_path.name] = entries
        parsed = {"logs": log_data, "log_files": len(log_data)}
        zeek_workspace.cleanup()
    if volatility_workspace is not None:
        volatility_workspace.cleanup()
    target_hash_after = _hash_target(path)
    target_modified = target_hash_before != target_hash_after
    try:
        binary_hash_after = _hash_binary(binary)["sha256"]
    except ToolExecutionError:
        binary_hash_after = None
    binary_modified = binary_hash_after != binary_provenance["sha256"]
    if binary_modified or target_modified:
        status = "integrity_error"
    evidence = {
        "schema_version": "1.0",
        "tool": tool_id,
        "tool_version": tool_version,
        "tool_binary_path": binary_provenance["resolved_path"],
        "tool_binary_sha256": binary_provenance["sha256"],
        "tool_binary_sha256_after": binary_hash_after,
        "tool_binary_modified": binary_modified,
        "tool_allowlist": allowlist_evidence,
        "target": str(path.relative_to(PROJECT_ROOT)) if path.is_relative_to(PROJECT_ROOT) else str(path),
        "target_sha256": target_hash_before,
        "target_sha256_after": target_hash_after,
        "target_modified": target_modified,
        "started_at": timestamp,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "status": status,
        "return_code": returncode,
        "tool_reported_success": (
            returncode in spec.get("accepted_exit_codes", [0])
            and not binary_modified and not target_modified
        ),
        "findings_present": (
            bool(parsed) if isinstance(parsed, (list, dict)) else None
        ),
        "output_truncated": truncated,
        "stdout": out_text,
        "stderr": err_text,
        "parsed_json": parsed,
        "command": command[1:],
        "network_access": (
            "disabled_by_tool_offline_mode" if spec.get("offline_only")
            else "not_enforced"
        ),
        "network_isolation_enforced": False,
        "network_policy": (
            "Modo offline solicitado al propio escáner; el proceso host no tiene "
            "aislamiento de egress del sistema operativo."
            if spec.get("offline_only") else
            "Los adaptadores que requieren red se deniegan; el egress de procesos locales no está aislado por este ejecutor."
        ),
        "database_preflight": database_preflight,
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
    except (OSError, TypeError, ValueError) as error:
        raise ToolExecutionError("No se pudo serializar o escribir evidencia protegida.") from error


__all__ = ["TOOL_SPECS", "ToolExecutionError", "run_local_tool", "write_evidence"]
