"""Ejecución local con captura acotada y terminación de grupos de procesos."""
import os
import signal
import subprocess
import threading


DEFAULT_MAX_OUTPUT_BYTES = 2_000_000


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
):
    """Ejecuta sin shell, con entorno explícito, salida acotada y grupo POSIX propio."""
    if os.name != "posix":
        raise ProcessIsolationError(
            "Ejecución bloqueada: esta plataforma necesita Job Objects para aislar procesos descendientes."
        )
    if not isinstance(command, (list, tuple)) or not command:
        raise ValueError("command debe ser una lista no vacía de argumentos.")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError("timeout debe ser un número positivo.")
    if type(max_output_bytes) is not int or max_output_bytes < 2:
        raise ValueError("max_output_bytes debe ser un entero de al menos 2 bytes.")

    per_stream_limit = max_output_bytes // 2
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    truncated = {"value": False}

    def drain(stream, key):
        try:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    break
                remaining = per_stream_limit - len(captured[key])
                if remaining > 0:
                    captured[key].extend(chunk[:remaining])
                if len(chunk) > remaining:
                    truncated["value"] = True
        except (OSError, ValueError):
            return

    process = None
    readers = []
    timed_out = False
    try:
        process = subprocess.Popen(
            list(command),
            cwd=cwd,
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
            for stream in (process.stdout, process.stderr):
                if stream is not None and not stream.closed:
                    try:
                        stream.close()
                    except OSError:
                        pass
            for reader in readers:
                reader.join(timeout=1)

    if process is None:
        raise ProcessIsolationError("El proceso no llegó a iniciarse.")
    return {
        "returncode": process.returncode,
        "stdout": captured["stdout"].decode("utf-8", errors="replace"),
        "stderr": captured["stderr"].decode("utf-8", errors="replace"),
        "timed_out": timed_out,
        "output_truncated": truncated["value"],
        "process_tree_isolation_enforced": True,
    }


__all__ = [
    "DEFAULT_MAX_OUTPUT_BYTES",
    "ProcessIsolationError",
    "run_bounded_process",
    "terminate_process_tree",
]
