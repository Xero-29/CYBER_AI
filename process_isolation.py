"""Ejecución local con entorno explícito, captura acotada y grupos POSIX."""
import hashlib
import math
import os
import signal
import subprocess
import threading


DEFAULT_MAX_OUTPUT_BYTES = 2_000_000
MAX_PROCESS_OUTPUT_BYTES = 64 * 1024 * 1024
MAX_PROCESS_TIMEOUT_SECONDS = 86_400


class ProcessIsolationError(RuntimeError):
    """No se puede garantizar el aislamiento del árbol de procesos."""


def terminate_process_tree(process):
    """Termina el grupo POSIX creado para una ejecución aislada."""
    if os.name != "posix":
        raise ProcessIsolationError(
            "La terminación completa del árbol requiere un Job Object de Windows."
        )
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)


def run_bounded_process(
    command,
    *,
    cwd,
    env,
    timeout,
    max_output_bytes=DEFAULT_MAX_OUTPUT_BYTES,
    capture_tail=False,
):
    """Ejecuta sin shell, con entorno explícito, salida acotada y grupo POSIX propio."""
    if os.name != "posix":
        raise ProcessIsolationError(
            "Ejecución bloqueada: esta plataforma necesita Job Objects para aislar procesos descendientes."
        )
    if not isinstance(command, (list, tuple)) or not command:
        raise ValueError("command debe ser una lista no vacía de argumentos.")
    normalized_command = []
    for index, argument in enumerate(command):
        try:
            value = os.fspath(argument)
        except TypeError as error:
            raise ValueError("Todos los argumentos del proceso deben ser texto o PathLike.") from error
        if not isinstance(value, str) or "\x00" in value or (index == 0 and not value):
            raise ValueError("Los argumentos del proceso deben ser texto válido sin NUL.")
        normalized_command.append(value)
    try:
        working_directory = os.fspath(cwd)
    except TypeError as error:
        raise ValueError("cwd debe ser una ruta de texto.") from error
    if not isinstance(working_directory, str) or "\x00" in working_directory:
        raise ValueError("cwd debe ser una ruta de texto sin NUL.")
    if not isinstance(env, dict):
        raise ValueError("env debe ser un diccionario explícito de texto.")
    for key, value in env.items():
        if (
            not isinstance(key, str) or not key or "=" in key or "\x00" in key
            or not isinstance(value, str) or "\x00" in value
        ):
            raise ValueError("env contiene una clave o valor no válido.")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError("timeout debe ser positivo, finito y no superar 86400 segundos.")
    try:
        valid_timeout = math.isfinite(timeout) and 0 < timeout <= MAX_PROCESS_TIMEOUT_SECONDS
    except OverflowError:
        valid_timeout = False
    if not valid_timeout:
        raise ValueError("timeout debe ser un número positivo y finito.")
    if (
        type(max_output_bytes) is not int
        or not 2 <= max_output_bytes <= MAX_PROCESS_OUTPUT_BYTES
    ):
        raise ValueError(
            f"max_output_bytes debe estar entre 2 y {MAX_PROCESS_OUTPUT_BYTES} bytes."
        )

    if not isinstance(capture_tail, bool):
        raise ValueError("capture_tail debe ser booleano.")

    per_stream_limit = max_output_bytes // 2
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    digests = {"stdout": hashlib.sha256(), "stderr": hashlib.sha256()}
    total_bytes = {"stdout": 0, "stderr": 0}
    truncated = {"stdout": False, "stderr": False}
    read_errors = set()

    def drain(stream, key):
        try:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    break
                total_bytes[key] += len(chunk)
                digests[key].update(chunk)
                if capture_tail:
                    captured[key].extend(chunk)
                    if len(captured[key]) > per_stream_limit:
                        del captured[key][:-per_stream_limit]
                        truncated[key] = True
                else:
                    remaining = per_stream_limit - len(captured[key])
                    if remaining > 0:
                        captured[key].extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        truncated[key] = True
        except Exception:
            # A partial stream digest is not trustworthy evidence. Record only the
            # stream name; never propagate an exception message that may contain data.
            read_errors.add(key)

    process = None
    readers = []
    timed_out = False
    try:
        process = subprocess.Popen(
            normalized_command,
            cwd=working_directory,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            close_fds=True,
            start_new_session=True,
            bufsize=0,
        )
        for stream, key in ((process.stdout, "stdout"), (process.stderr, "stderr")):
            reader = threading.Thread(target=drain, args=(stream, key), daemon=True)
            reader.start()
            readers.append(reader)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            terminate_process_tree(process)
    finally:
        if process is not None:
            if process.poll() is None:
                terminate_process_tree(process)
            for reader in readers:
                reader.join(timeout=5)
            if any(reader.is_alive() for reader in readers):
                terminate_process_tree(process)
                for reader in readers:
                    reader.join(timeout=2)
            for stream, key in ((process.stdout, "stdout"), (process.stderr, "stderr")):
                if stream is not None and not stream.closed:
                    try:
                        stream.close()
                    except (OSError, ValueError):
                        read_errors.add(key)
            for reader in readers:
                reader.join(timeout=1)

    unfinished_readers = [
        key for reader, key in zip(readers, ("stdout", "stderr"))
        if reader.is_alive()
    ]
    if read_errors or unfinished_readers:
        failed_streams = sorted(read_errors | set(unfinished_readers))
        raise ProcessIsolationError(
            "No se pudo capturar íntegramente la salida del proceso ("
            + ", ".join(failed_streams)
            + "); la evidencia no es confiable."
        )

    if process is None:
        raise ProcessIsolationError("El proceso no llegó a iniciarse.")
    return {
        "returncode": process.returncode,
        "stdout": captured["stdout"].decode("utf-8", errors="replace"),
        "stderr": captured["stderr"].decode("utf-8", errors="replace"),
        "timed_out": timed_out,
        "output_capture_complete": True,
        "output_truncated": any(truncated.values()),
        "stdout_sha256": digests["stdout"].hexdigest(),
        "stderr_sha256": digests["stderr"].hexdigest(),
        "stdout_bytes": total_bytes["stdout"],
        "stderr_bytes": total_bytes["stderr"],
        "stdout_truncated": truncated["stdout"],
        "stderr_truncated": truncated["stderr"],
        # POSIX process groups do not contain descendants that deliberately call
        # setsid()/setpgid(); stronger containment requires cgroups or a container.
        "process_group_isolation_enforced": True,
        "process_tree_isolation_enforced": False,
    }


__all__ = [
    "DEFAULT_MAX_OUTPUT_BYTES",
    "MAX_PROCESS_OUTPUT_BYTES",
    "ProcessIsolationError",
    "run_bounded_process",
    "terminate_process_tree",
]
