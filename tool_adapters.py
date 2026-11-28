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
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from tool_allowlist import ToolAllowlistError, verify_tool_allowed
from process_isolation import ProcessIsolationError, run_bounded_process
from safe_io import ensure_private_directory
from secret_redaction import redact_sensitive_data, redact_text


PROJECT_ROOT = Path(__file__).resolve().parent
MAX_OUTPUT_BYTES = 2_000_000
MAX_TOTAL_OUTPUT_BYTES = 8_000_000
MAX_TARGET_BYTES = 100_000_000
MAX_TARGET_FILES = 10_000
MAX_TARGET_ENTRIES = 20_000
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


def _directory_state(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        getattr(info, "st_ctime_ns", 0),
        info.st_mode,
        info.st_nlink,
    )


def _is_reparse_point(info):
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(getattr(info, "st_file_attributes", 0) & flag)


def _confined_path(target):
    """Resolve a repository path without accepting linked ancestors or hardlinks."""
    try:
        candidate = Path(os.fspath(target))
        if not candidate.is_absolute():
            candidate = PROJECT_ROOT / candidate
        candidate = Path(os.path.abspath(os.fspath(candidate)))
        project_root = PROJECT_ROOT.resolve(strict=True)
        relative = candidate.relative_to(project_root)
    except (OSError, TypeError, ValueError) as exc:
        raise ToolExecutionError(
            "La ruta debe existir y permanecer dentro del repositorio."
        ) from exc

    current = project_root
    parts = relative.parts
    if not parts:
        try:
            root_info = current.lstat()
        except OSError as exc:
            raise ToolExecutionError("La raíz del objetivo no está disponible.") from exc
        if not stat.S_ISDIR(root_info.st_mode) or _is_reparse_point(root_info):
            raise ToolExecutionError("La raíz del objetivo debe ser un directorio real.")
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except OSError as exc:
            raise ToolExecutionError("La ruta del objetivo no está disponible.") from exc
        if stat.S_ISLNK(info.st_mode) or _is_reparse_point(info):
            raise ToolExecutionError(
                "No se permiten enlaces simbólicos ni puntos de reanálisis en el objetivo o sus ancestros."
            )
        final_component = index == len(parts) - 1
        if not final_component:
            if not stat.S_ISDIR(info.st_mode):
                raise ToolExecutionError("Los componentes padre del objetivo deben ser directorios reales.")
            continue
        if stat.S_ISREG(info.st_mode):
            if info.st_nlink != 1:
                raise ToolExecutionError("No se permiten enlaces duros en archivos objetivo.")
        elif not stat.S_ISDIR(info.st_mode):
            raise ToolExecutionError("El objetivo debe ser un archivo regular o un directorio real.")

    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(project_root)
    except (OSError, ValueError) as exc:
        raise ToolExecutionError(
            "La ruta debe existir y permanecer dentro del repositorio."
        ) from exc
    if os.path.normcase(os.fspath(resolved)) != os.path.normcase(os.fspath(candidate)):
        raise ToolExecutionError("La ruta del objetivo cambió al resolver sus componentes.")
    return resolved


def _terminate_process_tree(process, *, posix=None):
    """Terminate the process group when possible; report unverified fallbacks."""
    if posix is None:
        posix = os.name == "posix"
    if posix:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            return True
        except OSError:
            try:
                process.kill()
            except OSError:
                pass
            return False
        return True
    try:
        process.kill()
    except OSError:
        pass
    # Windows fallback kills only the direct child; descendants are not proven dead.
    return False


def _hash_target(path):
    """Hash a bounded target tree while rejecting links and unstable file identities."""
    path = Path(path)
    try:
        root_info = path.lstat()
    except OSError as exc:
        raise ToolExecutionError("No se pudo inspeccionar el objetivo.") from exc
    if stat.S_ISLNK(root_info.st_mode) or _is_reparse_point(root_info):
        raise ToolExecutionError("El objetivo contiene un enlace o punto de reanálisis.")
    directory_states = {path: root_info} if stat.S_ISDIR(root_info.st_mode) else {}
    if stat.S_ISDIR(root_info.st_mode):
        files = []
        entry_count = 0
        pending_directories = [path]
        try:
            while pending_directories:
                current_path = pending_directories.pop()
                current_info = current_path.lstat()
                if (
                    not stat.S_ISDIR(current_info.st_mode)
                    or _is_reparse_point(current_info)
                ):
                    raise ToolExecutionError(
                        "El objetivo contiene un directorio no seguro."
                    )
                previous_info = directory_states.get(current_path)
                if (
                    previous_info is not None
                    and _directory_state(previous_info) != _directory_state(current_info)
                ):
                    raise ToolExecutionError(
                        "Un directorio del objetivo cambió durante la enumeración."
                    )
                directory_states[current_path] = current_info

                with os.scandir(current_path) as entries:
                    for entry in entries:
                        entry_count += 1
                        if entry_count > MAX_TARGET_ENTRIES:
                            raise ToolExecutionError(
                                "El objetivo supera el límite total de entradas."
                            )
                        item = Path(entry.path)
                        info = entry.stat(follow_symlinks=False)
                        if stat.S_ISLNK(info.st_mode) or _is_reparse_point(info):
                            raise ToolExecutionError(
                                "El objetivo contiene enlaces simbólicos o puntos de reanálisis; análisis bloqueado."
                            )
                        if stat.S_ISDIR(info.st_mode):
                            directory_states[item] = info
                            pending_directories.append(item)
                            continue
                        if not stat.S_ISREG(info.st_mode):
                            raise ToolExecutionError(
                                "El objetivo contiene entradas que no son archivos regulares ni directorios."
                            )
                        if info.st_nlink != 1:
                            raise ToolExecutionError(
                                "El objetivo contiene archivos con enlaces duros; análisis bloqueado."
                            )
                        files.append((item, info))
                        if len(files) > MAX_TARGET_FILES:
                            raise ToolExecutionError(
                                "El objetivo supera el límite de archivos."
                            )
        except ToolExecutionError:
            raise
        except OSError as exc:
            raise ToolExecutionError(
                "No se pudo enumerar el objetivo de forma segura."
            ) from exc
        base = path
    elif stat.S_ISREG(root_info.st_mode):
        if root_info.st_nlink != 1:
            raise ToolExecutionError("No se permiten enlaces duros en archivos objetivo.")
        files = [(path, root_info)]
        base = path.parent
    else:
        raise ToolExecutionError("El objetivo debe ser un archivo regular o un directorio real.")

    files.sort(key=lambda item: item[0].relative_to(base).as_posix())
    if len(files) > MAX_TARGET_FILES:
        raise ToolExecutionError("El objetivo supera el límite de archivos.")
    total_bytes = sum(info.st_size for _, info in files)
    if total_bytes > MAX_TARGET_BYTES:
        raise ToolExecutionError("El objetivo supera el límite de tamaño de análisis.")

    digest = hashlib.sha256()
    for item, expected in files:
        descriptor = None
        try:
            _confined_path(item)
            flags = (
                os.O_RDONLY
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NONBLOCK", 0)
            )
            descriptor = os.open(item, flags)
            opened = os.fstat(descriptor)
            path_opened = item.lstat()
            if (
                not stat.S_ISREG(opened.st_mode)
                or _is_reparse_point(opened)
                or stat.S_ISLNK(path_opened.st_mode)
                or _is_reparse_point(path_opened)
                or opened.st_nlink != 1
                or (opened.st_dev, opened.st_ino) != (expected.st_dev, expected.st_ino)
                or (opened.st_dev, opened.st_ino) != (path_opened.st_dev, path_opened.st_ino)
                or opened.st_size != expected.st_size
                or opened.st_mtime_ns != expected.st_mtime_ns
            ):
                raise ToolExecutionError("El archivo objetivo cambió o contiene enlaces durante su apertura.")

            relative = item.relative_to(base).as_posix().encode("utf-8")
            digest.update(len(relative).to_bytes(4, "big"))
            digest.update(relative)
            digest.update(opened.st_size.to_bytes(8, "big"))
            bytes_read = 0
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                bytes_read += len(chunk)
                digest.update(chunk)

            final = os.fstat(descriptor)
            path_final = item.lstat()
            if (
                not stat.S_ISREG(final.st_mode)
                or _is_reparse_point(final)
                or stat.S_ISLNK(path_final.st_mode)
                or _is_reparse_point(path_final)
                or final.st_nlink != 1
                or (final.st_dev, final.st_ino) != (opened.st_dev, opened.st_ino)
                or (path_final.st_dev, path_final.st_ino) != (final.st_dev, final.st_ino)
                or final.st_size != bytes_read
                or final.st_size != opened.st_size
                or final.st_mtime_ns != opened.st_mtime_ns
                or getattr(final, "st_ctime_ns", 0) != getattr(opened, "st_ctime_ns", 0)
            ):
                raise ToolExecutionError("El archivo objetivo cambió durante el cálculo de su huella.")
        except ToolExecutionError:
            raise
        except OSError as exc:
            raise ToolExecutionError("No se pudo calcular la huella segura del objetivo.") from exc
        finally:
            if descriptor is not None:
                os.close(descriptor)

    for directory, expected in directory_states.items():
        try:
            current = directory.lstat()
        except OSError as exc:
            raise ToolExecutionError(
                "Un directorio del objetivo desapareció durante el análisis."
            ) from exc
        if (
            not stat.S_ISDIR(current.st_mode)
            or _is_reparse_point(current)
            or _directory_state(current) != _directory_state(expected)
        ):
            raise ToolExecutionError(
                "El árbol del objetivo cambió durante el cálculo de su huella."
            )
    return digest.hexdigest()


def _bounded_matching_files(root, predicate):
    """Enumerate matching regular files without following links or exceeding tree limits."""
    root = Path(root)
    try:
        root_info = root.lstat()
    except OSError as exc:
        raise ToolExecutionError("No se pudo inspeccionar el directorio objetivo.") from exc
    if not stat.S_ISDIR(root_info.st_mode) or stat.S_ISLNK(root_info.st_mode) or _is_reparse_point(root_info):
        raise ToolExecutionError("El objetivo debe ser un directorio real, sin enlaces.")

    directory_states = {root: root_info}
    pending = [root]
    files = []
    entry_count = 0
    try:
        while pending:
            current = pending.pop()
            current_info = current.lstat()
            previous_info = directory_states.get(current)
            if (
                not stat.S_ISDIR(current_info.st_mode)
                or stat.S_ISLNK(current_info.st_mode)
                or _is_reparse_point(current_info)
                or (
                    previous_info is not None
                    and _directory_state(previous_info) != _directory_state(current_info)
                )
            ):
                raise ToolExecutionError("Un directorio del objetivo cambió durante la enumeración.")
            directory_states[current] = current_info
            with os.scandir(current) as entries:
                for entry in entries:
                    entry_count += 1
                    if entry_count > MAX_TARGET_ENTRIES:
                        raise ToolExecutionError("El objetivo supera el límite total de entradas.")
                    item = Path(entry.path)
                    info = entry.stat(follow_symlinks=False)
                    if stat.S_ISLNK(info.st_mode) or _is_reparse_point(info):
                        raise ToolExecutionError(
                            "El objetivo contiene enlaces simbólicos o puntos de reanálisis; análisis bloqueado."
                        )
                    if stat.S_ISDIR(info.st_mode):
                        directory_states[item] = info
                        pending.append(item)
                        continue
                    if not stat.S_ISREG(info.st_mode):
                        raise ToolExecutionError(
                            "El objetivo contiene entradas que no son archivos regulares ni directorios."
                        )
                    if info.st_nlink != 1:
                        raise ToolExecutionError(
                            "El objetivo contiene archivos con enlaces duros; análisis bloqueado."
                        )
                    if predicate(item):
                        files.append(item)
                        if len(files) > MAX_TARGET_FILES:
                            raise ToolExecutionError("El objetivo supera el límite de archivos.")
    except ToolExecutionError:
        raise
    except OSError as exc:
        raise ToolExecutionError("No se pudo enumerar el objetivo de forma segura.") from exc

    for directory, expected in directory_states.items():
        try:
            current = directory.lstat()
        except OSError as exc:
            raise ToolExecutionError("Un directorio del objetivo desapareció durante la enumeración.") from exc
        if (
            not stat.S_ISDIR(current.st_mode)
            or stat.S_ISLNK(current.st_mode)
            or _is_reparse_point(current)
            or _directory_state(current) != _directory_state(expected)
        ):
            raise ToolExecutionError("El árbol del objetivo cambió durante la enumeración.")

    files.sort(key=lambda item: item.relative_to(root).as_posix())
    return files


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
            files = _bounded_matching_files(target, lambda path: path.name == "Dockerfile")
        elif tool_id == "shellcheck":
            files = _bounded_matching_files(target, lambda path: path.suffix.lower() in {".sh", ".bash"})
        else:
            files = _bounded_matching_files(target, lambda path: path.suffix.lower() in {".yml", ".yaml"})
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
    """Obtiene la versión con timeout, salida acotada y grupo POSIX propio."""
    arguments = TOOL_SPECS[tool_id].get("version_args", ["--version"])
    isolated_cwd = env.get("HOME") if isinstance(env, dict) else None
    if not isinstance(isolated_cwd, str) or not isolated_cwd:
        return "unknown"
    try:
        result = run_bounded_process(
            [binary, *arguments],
            cwd=isolated_cwd,
            env=env,
            timeout=5,
            max_output_bytes=8192,
        )
    except (OSError, ProcessIsolationError, ValueError):
        return "unknown"
    if (
        result.get("timed_out")
        or result.get("output_capture_complete") is not True
        or result.get("output_truncated")
        or not result.get("process_group_isolation_enforced")
        or result.get("returncode") != 0
    ):
        return "unknown"
    output = "\n".join(
        part for part in (result.get("stdout", ""), result.get("stderr", ""))
        if isinstance(part, str) and part
    )
    if not output.strip():
        return "unknown"
    return redact_text(output.strip().splitlines()[0][:256])


def run_local_tool(tool_id, target, *, config_path=None, timeout=None):
    """Ejecuta el adaptador con HOME/TMP efímeros y entorno mínimo."""
    if os.name != "posix":
        raise ToolExecutionError(
            "Ejecución bloqueada: se requiere un Job Object para aislar procesos descendientes en Windows."
        )
    with tempfile.TemporaryDirectory(prefix="cyber-ai-tool-home-") as isolated_home:
        if os.name == "posix":
            os.chmod(isolated_home, 0o700)
        return _run_local_tool_with_home(
            tool_id, target, config_path=config_path, timeout=timeout,
            isolated_home=isolated_home,
        )


def _run_local_tool_with_home(
    tool_id, target, *, config_path=None, timeout=None, isolated_home
):
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
    try:
        binary_allowlist = verify_tool_allowed(tool_id, binary_provenance["sha256"])
    except ToolAllowlistError as exc:
        raise ToolExecutionError(
            "El ejecutable no está aprobado por la allowlist firmada."
        ) from exc
    limit = spec["timeout"] if timeout is None else timeout
    if not isinstance(limit, int) or not 1 <= limit <= 600:
        raise ToolExecutionError("El timeout debe estar entre 1 y 600 segundos.")
    enumerates_directory = (
        tool_id in {"hadolint", "shellcheck", "actionlint"} and path.is_dir()
    )
    target_hash_before = _hash_target(path) if enumerates_directory else None
    command = _build_command(tool_id, binary, path, config_path=config_path)
    if enumerates_directory and _hash_target(path) != target_hash_before:
        raise ToolExecutionError(
            "El objetivo cambió mientras se preparaba la lista de archivos; ejecución bloqueada."
        )
    # Never expose the caller's home/configuration tree or ambient secrets
    # to a host tool. The executable itself is absolute; child lookups are
    # limited to its installation directory and the platform default PATH.
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
    tool_version = _probe_tool_version(binary, tool_id, env)
    if _hash_binary(binary)["sha256"] != binary_provenance["sha256"]:
        raise ToolExecutionError("El ejecutable cambió durante la identificación de versión.")
    if target_hash_before is None:
        target_hash_before = _hash_target(path)
    started = time.monotonic()
    timestamp = datetime.now(timezone.utc).isoformat()
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    stream_truncated = {"value": False}
    output_limit_exceeded = threading.Event()
    output_lock = threading.Lock()
    output_bytes_observed = {"value": 0}
    stream_bytes_observed = {"stdout": 0, "stderr": 0}
    output_limit_termination_failed = {"value": False}
    reader_errors = set()

    def drain(stream, key):
        cap = MAX_OUTPUT_BYTES // 2
        try:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    break
                terminate = False
                with output_lock:
                    if output_limit_exceeded.is_set():
                        return
                    stream_bytes_observed[key] += len(chunk)
                    output_bytes_observed["value"] += len(chunk)
                    remaining = cap - len(captured[key])
                    if remaining > 0:
                        captured[key].extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        stream_truncated["value"] = True
                    if output_bytes_observed["value"] > MAX_TOTAL_OUTPUT_BYTES:
                        output_limit_exceeded.set()
                        stream_truncated["value"] = True
                        terminate = True
                if terminate and process is not None:
                    if not _terminate_process_tree(process):
                        output_limit_termination_failed["value"] = True
                    return
        except Exception:
            # Stream wrappers may raise unexpected exceptions or return invalid
            # chunk types. Never turn a partial read into successful evidence.
            # Do not retain exception text: it may contain sensitive data.
            reader_errors.add(key)
            return

    process = None
    readers = []
    process_finished = False
    try:
        process = subprocess.Popen(
            command, cwd=isolated_home, env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False,
            start_new_session=(os.name == "posix"),
        )
        for stream, key in ((process.stdout, "stdout"), (process.stderr, "stderr")):
            reader = threading.Thread(target=drain, args=(stream, key), daemon=True)
            reader.start()
            readers.append(reader)
        timed_out = False
        try:
            returncode = process.wait(timeout=limit)
            process_finished = True
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
            process_finished = True
            returncode = None
        if timed_out:
            status = "timeout"
        elif output_limit_exceeded.is_set():
            status = "output_limit_exceeded"
        elif stream_truncated["value"]:
            status = "output_truncated"
        else:
            status = "completed"
    except OSError as exc:
        raise ToolExecutionError("No se pudo iniciar el ejecutable.") from exc
    finally:
        if process is not None and not process_finished:
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                try:
                    process.kill()
                except OSError:
                    pass
            try:
                process.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                pass
        for reader in readers:
            reader.join(timeout=5)
        if any(reader.is_alive() for reader in readers) and process is not None:
            # A descendant retaining stdout/stderr must not outlive this tool
            # invocation or keep the pipe-draining threads blocked.
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            for reader in readers:
                reader.join(timeout=2)
        if process is not None:
            for stream in (process.stdout, process.stderr):
                if stream is not None and not stream.closed:
                    try:
                        stream.close()
                    except OSError:
                        pass
        for reader in readers:
            reader.join(timeout=1)

    expected_streams = ("stdout", "stderr")
    unfinished_readers = [
        key for reader, key in zip(readers, expected_streams)
        if reader.is_alive()
    ]
    if process is not None and len(readers) != len(expected_streams):
        unfinished_readers.extend(expected_streams[len(readers):])
    if reader_errors or unfinished_readers:
        failed_streams = sorted(reader_errors | set(unfinished_readers))
        raise ProcessIsolationError(
            "No se pudo capturar íntegramente la salida de la herramienta ("
            + ", ".join(failed_streams)
            + "); la evidencia no es confiable."
        )

    out_text = redact_text(captured["stdout"].decode("utf-8", errors="replace"))
    err_text = redact_text(captured["stderr"].decode("utf-8", errors="replace"))
    truncated = stream_truncated["value"]
    try:
        parsed = json.loads(out_text) if out_text.strip() else None
        if parsed is not None:
            parsed = redact_sensitive_data(parsed)
    except (json.JSONDecodeError, RecursionError):
        parsed = None
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
        "binary_allowlist": binary_allowlist,
        "tool_binary_sha256": binary_provenance["sha256"],
        "tool_binary_sha256_after": binary_hash_after,
        "tool_binary_modified": binary_modified,
        "target": str(path.relative_to(PROJECT_ROOT)),
        "target_sha256": target_hash_before,
        "target_sha256_after": target_hash_after,
        "target_modified": target_modified,
        "started_at": timestamp,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "status": status,
        "return_code": returncode,
        "tool_reported_success": (
            returncode == 0
            and not binary_modified
            and not target_modified
            and status == "completed"
            and not truncated
        ),
        "output_capture_complete": not output_limit_exceeded.is_set(),
        "output_truncated": truncated,
        "output_limit_exceeded": output_limit_exceeded.is_set(),
        "output_bytes_observed": output_bytes_observed["value"],
        "output_limit_bytes": MAX_TOTAL_OUTPUT_BYTES,
        "stdout_bytes_observed": stream_bytes_observed["stdout"],
        "stderr_bytes_observed": stream_bytes_observed["stderr"],
        "output_limit_termination_failed": output_limit_termination_failed["value"],
        "stdout": out_text,
        "stderr": err_text,
        "parsed_json": parsed,
        "command": redact_sensitive_data(command[1:]),
        "network_access": "not_enforced",
        "network_isolation_enforced": False,
        "network_policy": "Los adaptadores que requieren red se deniegan; el egress de procesos locales no está aislado por este ejecutor.",
        "note": "Salida de herramienta no confiable; requiere validación antes de generar hallazgos o Skills. La ejecución no sustituye aislamiento del sistema operativo.",
    }
    return evidence


def write_evidence(evidence, output_dir="reports/tool_evidence", *, allow_external=False):
    if not isinstance(allow_external, bool):
        raise ToolExecutionError("allow_external debe ser un booleano explícito.")
    raw = Path(output_dir)
    if not raw.is_absolute():
        raw = PROJECT_ROOT / raw
    raw = Path(os.path.abspath(os.fspath(raw)))
    project_root = PROJECT_ROOT.resolve()
    if raw == project_root or raw in project_root.parents:
        raise ToolExecutionError(
            "El destino de evidencias no puede ser la raíz del repositorio ni un ancestro."
        )
    if raw.exists() and not raw.is_symlink() and raw.is_dir() and os.name == "posix":
        existing_info = raw.stat(follow_symlinks=False)
        if (
            existing_info.st_uid != os.geteuid()
            or stat.S_IMODE(existing_info.st_mode) & 0o077
        ):
            raise ToolExecutionError(
                "Un directorio de evidencias existente debe ser del usuario y ya tener modo privado 0700."
            )
    try:
        if not allow_external:
            existing = raw
            while not existing.exists() and not existing.is_symlink():
                existing = existing.parent
            _confined_path(existing)
        destination = ensure_private_directory(raw, create=True)
        if allow_external:
            destination = destination.resolve(strict=True)
        else:
            destination = _confined_path(destination)
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
        safe_evidence = redact_sensitive_data(evidence)
        tool = safe_evidence.get("tool") if isinstance(safe_evidence, dict) else None
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
                stream.write(json.dumps(safe_evidence, ensure_ascii=False, indent=2) + "\n")
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
