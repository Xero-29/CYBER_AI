#!/usr/bin/env python3
"""Ejecuta adaptadores CYBER_AI dentro de un contenedor Docker endurecido."""
import argparse
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from tool_adapters import TOOL_SPECS, ToolExecutionError, _confined_path, PROJECT_ROOT


DEFAULT_IMAGE = "cyber-ai-tool-sandbox:local"
# Debe coincidir con los binarios realmente instalados en sandbox/Dockerfile.
SANDBOX_TOOLS = frozenset({"ruff", "bandit"})


def build_docker_command(tool_id, target, evidence_dir, image=DEFAULT_IMAGE, timeout=None, config=None):
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
    relative_target = target_path.relative_to(PROJECT_ROOT).as_posix()
    evidence = Path(evidence_dir)
    if any(character in str(evidence) for character in (",", "\n", "\r")):
        raise ToolExecutionError("La ruta de evidencias contiene caracteres no permitidos para Docker --mount.")
    if evidence.is_symlink():
        raise ToolExecutionError("La carpeta de evidencias no puede ser un enlace simbólico.")
    evidence.mkdir(parents=True, exist_ok=True)
    evidence = evidence.resolve(strict=True)
    try:
        evidence.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        pass
    else:
        raise ToolExecutionError("La carpeta de evidencias debe estar fuera del repositorio.")

    command = [
        "docker", "run", "--rm",
        "--name", "cyber-ai-sandbox-" + uuid.uuid4().hex,
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges:true",
        "--pids-limit=128",
        "--memory=1g",
        "--cpus=2",
        f"--user={os.getuid()}:{os.getgid()}",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=64m",
        "--mount", f"type=bind,src={PROJECT_ROOT.resolve()},dst=/workspace,readonly",
        "--mount", f"type=bind,src={evidence},dst=/evidence",
        "--workdir=/workspace",
        "--env", "CYBER_AI_EVIDENCE_DIR=/evidence",
        "--env", "CYBER_AI_LEDGER_PATH=/evidence/execution_ledger.sqlite3",
        "--env", "HOME=/tmp",
        "--env", "RUFF_NO_CACHE=1",
        image,
        "/workspace/tool_executor.py",
        "--tool", tool_id,
        "--target", relative_target,
        "--execute",
    ]
    if timeout is not None:
        if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 600:
            raise ToolExecutionError("El timeout debe estar entre 1 y 600 segundos.")
        command.extend(["--timeout", str(timeout)])
    if config:
        config_path = _confined_path(config)
        command.extend(["--config", config_path.relative_to(PROJECT_ROOT).as_posix()])
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
        command = build_docker_command(
            args.tool, args.target, args.evidence_dir, args.image,
            timeout=args.timeout, config=args.config,
        )
        container_name = command[command.index("--name") + 1]
        effective_timeout = args.timeout or TOOL_SPECS[args.tool]["timeout"]
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
        print(f"Ejecución denegada: {exc}", file=sys.stderr)
        return 2
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
