#!/usr/bin/env python3
"""Ejecuta adaptadores CYBER_AI dentro de un contenedor Docker endurecido."""
import argparse
import os
import re
import shutil
import subprocess
import stat
import sys
import tempfile
import uuid
from pathlib import Path

from tool_adapters import TOOL_SPECS, ToolExecutionError, _confined_path, PROJECT_ROOT
from tool_allowlist import ToolAllowlistError, load_signed_tool_allowlist
from safe_io import (
    SafeWriteError,
    atomic_write_text,
    ensure_private_directory,
    read_regular_file,
)
from secret_redaction import redact_text


DEFAULT_IMAGE = "cyber-ai-tool-sandbox:local"
# El contenedor recibe únicamente estos módulos de runtime, no la raíz del repositorio.
RUNTIME_MODULES = (
    "tool_executor.py",
    "tool_adapters.py",
    "tool_allowlist.py",
    "execution_ledger.py",
    "process_isolation.py",
    "safe_io.py",
    "secret_redaction.py",
)
MAX_RUNTIME_MODULE_BYTES = 2_000_000
# Debe coincidir con los binarios realmente instalados en sandbox/Dockerfile.
SANDBOX_TOOLS = frozenset({"ruff", "bandit"})

def _docker_user_args(platform_name=None):
    """Keep the container non-root without assuming POSIX APIs on Windows."""
    platform_name = os.name if platform_name is None else platform_name
    if platform_name == "nt":
        # sandbox/Dockerfile declares USER 65532:65532.
        return []
    if platform_name != "posix":
        raise ToolExecutionError("Plataforma no compatible con la política de usuario Docker.")
    host_uid = os.getuid()
    if host_uid == 0:
        raise ToolExecutionError(
            "La sandbox no se ejecuta desde un host root; usa una cuenta sin privilegios."
        )
    return [f"--user={host_uid}:{os.getgid()}"]



def _paths_overlap(left, right):
    return left == right or left in right.parents or right in left.parents


def prepare_runtime_bundle(destination):
    """Create a minimal, read-only runtime tree containing no repository data."""
    path = Path(os.path.abspath(os.fspath(destination)))
    if any(character in str(path) for character in (",", "\n", "\r")):
        raise ToolExecutionError("La ruta del runtime contiene delimitadores no permitidos.")
    project = PROJECT_ROOT.resolve()
    if _paths_overlap(path, project):
        raise ToolExecutionError("El runtime aislado no puede solaparse con el repositorio.")
    try:
        runtime = ensure_private_directory(path, create=True)
        if any(runtime.iterdir()):
            raise ToolExecutionError("El directorio temporal del runtime debe estar vacío.")
        for name in RUNTIME_MODULES:
            source = PROJECT_ROOT / name
            raw = read_regular_file(source, max_bytes=MAX_RUNTIME_MODULE_BYTES)
            content = raw.decode("utf-8")
            destination_file = runtime / name
            atomic_write_text(
                destination_file,
                content,
                mode=0o600,
                create_parents=False,
            )
            os.chmod(destination_file, 0o444)
        os.chmod(runtime, 0o555)
        return runtime.resolve(strict=True)
    except ToolExecutionError:
        raise
    except (SafeWriteError, OSError, UnicodeError, ValueError) as error:
        raise ToolExecutionError(
            "No se pudo preparar el runtime mínimo y verificado de la sandbox."
        ) from error


def _validate_runtime_bundle(runtime_dir):
    path = Path(os.path.abspath(os.fspath(runtime_dir)))
    if any(character in str(path) for character in (",", "\n", "\r")):
        raise ToolExecutionError("La ruta del runtime contiene delimitadores no permitidos.")
    try:
        path = path.resolve(strict=True)
        info = path.lstat()
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if (
            not stat.S_ISDIR(info.st_mode)
            or stat.S_ISLNK(info.st_mode)
            or getattr(info, "st_file_attributes", 0) & reparse_flag
        ):
            raise ToolExecutionError("El runtime debe ser un directorio real.")
        project = PROJECT_ROOT.resolve()
        if _paths_overlap(path, project):
            raise ToolExecutionError("El runtime aislado no puede solaparse con el repositorio.")
        if os.name != "nt" and (
            info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) & 0o222
        ):
            raise ToolExecutionError("El runtime debe pertenecer al usuario y ser de solo lectura.")
        entries = {item.name for item in path.iterdir()}
        if entries != set(RUNTIME_MODULES):
            raise ToolExecutionError("El runtime contiene archivos ausentes o no autorizados.")
        for name in RUNTIME_MODULES:
            item = path / name
            file_info = item.lstat()
            if (
                stat.S_ISLNK(file_info.st_mode)
                or getattr(file_info, "st_file_attributes", 0) & reparse_flag
                or not stat.S_ISREG(file_info.st_mode)
                or file_info.st_size > MAX_RUNTIME_MODULE_BYTES
                or (os.name == "posix" and file_info.st_nlink != 1)
                or (os.name != "nt" and stat.S_IMODE(file_info.st_mode) & 0o222)
            ):
                raise ToolExecutionError("El runtime contiene un módulo inseguro.")
    except ToolExecutionError:
        raise
    except OSError as error:
        raise ToolExecutionError("No se pudo validar el runtime aislado.") from error
    return path


def _signed_allowlist_mount_args(tool_id):
    """Validate and mount a one-tool HMAC allowlist read-only into the sandbox."""
    path_value = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_PATH", "").strip()
    key_value = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY", "")
    if not path_value and not key_value:
        raise ToolExecutionError(
            "La sandbox exige una allowlist HMAC firmada para el ejecutable."
        )
    if not path_value or not key_value:
        raise ToolExecutionError(
            "La ruta y la clave HMAC de la allowlist deben configurarse juntas."
        )
    key = key_value.encode("utf-8")
    if len(key) < 32:
        raise ToolExecutionError(
            "La clave HMAC de la allowlist debe tener al menos 32 bytes."
        )

    candidate = Path(os.path.abspath(path_value))
    if any(character in str(candidate) for character in (",", "\n", "\r")):
        raise ToolExecutionError(
            "La ruta de la allowlist contiene caracteres no permitidos para Docker --mount."
        )
    try:
        candidate.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        pass
    else:
        raise ToolExecutionError("La allowlist debe almacenarse fuera del repositorio.")

    try:
        approved = load_signed_tool_allowlist(candidate, key)
    except ToolAllowlistError as exc:
        raise ToolExecutionError(
            "La allowlist HMAC no es válida o no cumple la política de archivos."
        ) from exc
    if set(approved) != {tool_id}:
        raise ToolExecutionError(
            "La allowlist debe autorizar exclusivamente la herramienta solicitada."
        )
    return [
        "--mount",
        f"type=bind,src={candidate.resolve(strict=True)},dst=/run/cyber-ai-tool-allowlist.json,readonly",
        "--env",
        "CYBER_AI_TOOL_ALLOWLIST_PATH=/run/cyber-ai-tool-allowlist.json",
        "--env",
        "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY",
        "--env",
        "CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1",
    ]


def build_docker_command(
    tool_id, target, evidence_dir, image=DEFAULT_IMAGE, timeout=None, config=None,
    *, runtime_dir,
):
    if tool_id not in TOOL_SPECS:
        raise ToolExecutionError("Herramienta no registrada.")
    if tool_id not in SANDBOX_TOOLS:
        raise ToolExecutionError(
            "La herramienta está registrada, pero no está instalada en la imagen sandbox."
        )
    if TOOL_SPECS[tool_id]["network"]:
        raise ToolExecutionError("La herramienta requiere red y está bloqueada por política.")
    if not isinstance(image, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,254}", image):
        raise ToolExecutionError("Nombre de imagen Docker inválido.")
    target_path = _confined_path(target)
    if any(character in str(target_path) for character in (",", "\n", "\r")):
        raise ToolExecutionError("La ruta del objetivo contiene delimitadores no permitidos para Docker --mount.")
    relative_target = "target"
    runtime = _validate_runtime_bundle(runtime_dir)
    evidence_root = Path(evidence_dir)
    if not evidence_root.is_absolute():
        evidence_root = PROJECT_ROOT / evidence_root
    evidence_root = Path(os.path.abspath(os.fspath(evidence_root)))
    if any(character in str(evidence_root) for character in (",", "\n", "\r")):
        raise ToolExecutionError("La ruta de evidencias contiene caracteres no permitidos para Docker --mount.")
    try:
        evidence_candidate = evidence_root.resolve(strict=False)
    except OSError as error:
        raise ToolExecutionError("La ruta de evidencias no se puede resolver de forma segura.") from error
    if _paths_overlap(evidence_candidate, PROJECT_ROOT.resolve()):
        raise ToolExecutionError("La ruta de evidencias no puede solaparse con el repositorio.")
    if evidence_root.is_symlink():
        raise ToolExecutionError("La carpeta de evidencias no puede ser un enlace simbólico.")
    if evidence_root.exists() and evidence_root.is_dir() and os.name != "nt":
        existing_info = evidence_root.stat(follow_symlinks=False)
        if (
            existing_info.st_uid != os.geteuid()
            or stat.S_IMODE(existing_info.st_mode) & 0o077
        ):
            raise ToolExecutionError(
                "La carpeta de evidencias existente debe pertenecer al usuario y ser privada (0700)."
            )
    try:
        evidence_root = ensure_private_directory(evidence_root, create=True).resolve(strict=True)
        evidence_candidate = evidence_root / ("run-" + uuid.uuid4().hex)
        evidence = ensure_private_directory(evidence_candidate, create=True).resolve(strict=True)
        if any(evidence.iterdir()):
            raise ToolExecutionError("El directorio de evidencia de esta ejecución debe estar vacío.")
    except ToolExecutionError:
        raise
    except SafeWriteError as exc:
        raise ToolExecutionError(
            "La ruta de evidencias no cumple la política de directorios privados."
        ) from exc
    if _paths_overlap(evidence, PROJECT_ROOT.resolve()):
        raise ToolExecutionError("La ruta de evidencias no puede solaparse con el repositorio.")
    if _paths_overlap(runtime, evidence):
        raise ToolExecutionError("El runtime y las evidencias no pueden compartir rutas.")

    user_args = _docker_user_args()
    allowlist_args = _signed_allowlist_mount_args(tool_id)

    command = [
        "docker", "run", "--rm", "--pull=never",
        "--name", "cyber-ai-sandbox-" + uuid.uuid4().hex,
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges:true",
        "--pids-limit=128",
        "--memory=1g",
        "--cpus=2",
        *user_args,
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=64m",
        "--mount", f"type=bind,src={runtime},dst=/workspace,readonly",
        "--mount", f"type=bind,src={target_path},dst=/workspace/target,readonly",
        "--mount", f"type=bind,src={evidence},dst=/evidence",
        *allowlist_args,
        "--workdir=/workspace",
        "--env", "CYBER_AI_EVIDENCE_DIR=/evidence",
        "--env", "CYBER_AI_LEDGER_PATH=/evidence/execution_ledger.sqlite3",
        "--env", "HOME=/tmp",
        "--env", "RUFF_NO_CACHE=1",
        image,
        "/workspace/tool_executor.py",
        "--tool", tool_id,
        "--target", relative_target,
        "--execute", "--require-ledger",
    ]
    if timeout is not None:
        if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 600:
            raise ToolExecutionError("El timeout debe estar entre 1 y 600 segundos.")
        command.extend(["--timeout", str(timeout)])
    if config:
        config_path = _confined_path(config)
        if not config_path.is_file() or any(
            character in str(config_path) for character in (",", "\n", "\r")
        ):
            raise ToolExecutionError("La configuración debe ser un archivo local válido para Docker --mount.")
        command.extend([
            "--mount",
            f"type=bind,src={config_path},dst=/workspace/config,readonly",
            "--config", "config",
        ])
    return command


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=sorted(TOOL_SPECS))
    parser.add_argument("--target", required=True)
    parser.add_argument("--evidence-dir", default="../cyber-ai-evidence")
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--config")
    parser.add_argument("--execute", action="store_true", help="Confirma la ejecución Docker")
    args = parser.parse_args(argv)
    if not args.execute:
        print("Dry-run: añade --execute para ejecutar dentro del contenedor.")
        return 0
    if not shutil.which("docker"):
        print("Docker CLI no está disponible.", file=sys.stderr)
        return 2
    container_name = None
    try:
        with tempfile.TemporaryDirectory(prefix="cyber-ai-sandbox-runtime-") as runtime_temp:
            runtime_bundle = prepare_runtime_bundle(runtime_temp)
            command = build_docker_command(
                args.tool, args.target, args.evidence_dir, args.image,
                timeout=args.timeout, config=args.config,
                runtime_dir=runtime_bundle,
            )
            container_name = command[command.index("--name") + 1]
            evidence_mount = next(
                value for value in command
                if value.startswith("type=bind,src=") and ",dst=/evidence" in value
            )
            evidence_path = evidence_mount.split("src=", 1)[1].split(",dst=", 1)[0]
            print(f"Evidencia aislada de esta ejecución: {evidence_path}", flush=True)
            effective_timeout = args.timeout or TOOL_SPECS[args.tool]["timeout"]
            try:
                result = subprocess.run(
                    command, cwd=PROJECT_ROOT, check=False,
                    timeout=effective_timeout + 60,
                )
            except subprocess.TimeoutExpired:
                if container_name:
                    for cleanup in (
                        ["docker", "kill", container_name],
                        ["docker", "rm", "--force", container_name],
                    ):
                        try:
                            subprocess.run(cleanup, check=False, timeout=10)
                        except (OSError, subprocess.TimeoutExpired):
                            pass
                print("El proceso Docker superó el límite de tiempo del host; se solicitó eliminar el contenedor.", file=sys.stderr)
                return 124
    except (ToolExecutionError, OSError) as exc:
        print(f"Ejecución denegada: {redact_text(str(exc))}", file=sys.stderr)
        return 2
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
