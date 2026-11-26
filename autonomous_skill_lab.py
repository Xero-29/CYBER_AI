#!/usr/bin/env python3
"""Ciclo experimental 9B -> agente pequeño -> sandbox -> diagnóstico -> revisión.

El primer perfil ejecutable es deliberadamente acotado a laboratorios Rust sin
dependencias externas. Los modelos nunca pueden emitir comandos de shell.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_IMAGE = "cyber-ai-rust-skill-lab:local"
ALLOWED_FILES = {"Cargo.toml", "src/main.rs", "src/lib.rs"}
MAX_FILE_BYTES = 64 * 1024
MAX_ROUNDS = 3


class LabError(RuntimeError):
    pass


def _json_object(text):
    if not isinstance(text, str):
        raise LabError("El modelo no devolvió texto.")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LabError("La respuesta del modelo no es JSON válido.") from exc
    if not isinstance(value, dict):
        raise LabError("La respuesta del modelo debe ser un objeto JSON.")
    return value


def ollama_chat(model, messages, *, base_url=None, timeout=180):
    """Llama a Ollama local sin herramientas, function-calling ni acceso a shell."""
    base = (base_url or os.environ.get("CYBER_AI_OLLAMA_URL", "http://127.0.0.1:11434")).rstrip("/")
    if not re.fullmatch(r"http://(?:127\.0\.0\.1|localhost|\[::1\])(?::\d{1,5})?", base):
        raise LabError("Por seguridad, Ollama debe estar en loopback HTTP.")
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 2048},
    }).encode("utf-8")
    request = urllib.request.Request(
        base + "/api/chat", data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise LabError("No se pudo completar la llamada local a Ollama: " + str(exc)[:500]) from exc
    message = result.get("message") or {}
    return message.get("content", "")


def validate_generated_files(files):
    if not isinstance(files, dict) or not files:
        raise LabError("El agente ejecutor no entregó archivos.")
    normalized = {}
    for name, content in files.items():
        if name not in ALLOWED_FILES:
            raise LabError("Ruta generada fuera de la allowlist: " + str(name))
        if not isinstance(content, str) or not content.strip():
            raise LabError("Contenido vacío o inválido: " + name)
        if len(content.encode("utf-8")) > MAX_FILE_BYTES:
            raise LabError("Archivo demasiado grande: " + name)
        normalized[name] = content
    if "Cargo.toml" not in normalized or not ({"src/main.rs", "src/lib.rs"} & set(normalized)):
        raise LabError("El proyecto requiere Cargo.toml y main.rs o lib.rs.")
    manifest = normalized["Cargo.toml"]
    if re.search(r"(?im)^\s*\[(?:dependencies|dev-dependencies|build-dependencies)\]\s*$", manifest):
        raise LabError("No se permiten dependencias ni scripts de build en este perfil offline.")
    if re.search(r"(?im)^\s*build\s*=", manifest):
        raise LabError("No se permiten build scripts.")
    return normalized


def build_docker_command(workspace, *, image=DEFAULT_IMAGE, timeout=180):
    if not isinstance(image, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,254}", image):
        raise LabError("Nombre de imagen Docker inválido.")
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 10 <= timeout <= 600:
        raise LabError("Timeout fuera del rango permitido (10-600 s).")
    path = Path(workspace).resolve(strict=True)
    if not path.is_dir() or path.is_symlink():
        raise LabError("Workspace inválido.")
    return [
        "docker", "run", "--rm",
        "--name", "cyber-ai-rust-lab-" + os.urandom(8).hex(),
        "--network=none", "--read-only", "--cap-drop=ALL",
        "--security-opt=no-new-privileges:true",
        "--pids-limit=96", "--memory=1g", "--cpus=2",
        f"--user={os.getuid()}:{os.getgid()}",
        "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m",
        "--mount", f"type=bind,src={path},dst=/workspace",
        "--workdir=/workspace",
        "--env", "HOME=/tmp",
        "--env", "CARGO_HOME=/tmp/cargo-home",
        "--env", "CARGO_TARGET_DIR=/tmp/cargo-target",
        "--env", "CARGO_NET_OFFLINE=true",
        image, "cargo", "test", "--offline", "--manifest-path", "/workspace/Cargo.toml",
    ]


def run_rust_lab(files, *, image=DEFAULT_IMAGE, timeout=180, docker_bin="docker", memory_path=None):
    if not shutil.which(docker_bin):
        raise LabError("Docker no está instalado o no está disponible en PATH.")
    safe_files = validate_generated_files(files)
    with tempfile.TemporaryDirectory(prefix="cyber-ai-skill-lab-") as temp:
        workspace = Path(temp)
        for name, content in safe_files.items():
            destination = workspace / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        command = build_docker_command(workspace, image=image, timeout=timeout)
        started = time.monotonic()
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=False, timeout=timeout + 30,
            )
        except subprocess.TimeoutExpired as exc:
            container_name = command[command.index("--name") + 1]
            for cleanup in (
                [docker_bin, "kill", container_name],
                [docker_bin, "rm", "--force", container_name],
            ):
                try:
                    subprocess.run(cleanup, capture_output=True, text=True, check=False, timeout=10)
                except (OSError, subprocess.TimeoutExpired):
                    pass
            raise LabError("El sandbox superó el timeout; se solicitó eliminar el contenedor.") from exc
        elapsed = round(time.monotonic() - started, 3)
        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "duration_seconds": elapsed,
            "stdout": result.stdout[-12000:],
            "stderr": result.stderr[-6000:],
            "files": sorted(safe_files),
            "validator": "docker_cargo_test_offline",
            "network": "disabled",
        }


def _ask_json(model, system, user, *, base_url=None, timeout=180):
    raw = ollama_chat(
        model,
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        base_url=base_url, timeout=timeout,
    )
    return _json_object(raw)


def _memory_tokens(value):
    return {token.lower() for token in re.findall(r"[a-zA-Z0-9_+-]{3,}", value)}

def load_skill_memory(task, path, *, limit=3):
    """Recupera candidatos previos como referencias no confiables, nunca como permisos."""
    memory_file = Path(path)
    if not memory_file.is_file():
        return []
    query = _memory_tokens(task)
    ranked = []
    try:
        lines = memory_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines[-500:]:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict) or item.get("status") != "candidate_only":
            continue
        procedure = item.get("procedure", [])
        text_value = str(item.get("task", "")) + " " + " ".join(procedure if isinstance(procedure, list) else [])
        tokens = _memory_tokens(text_value)
        score = len(query & tokens) / max(1, len(query))
        if score >= 0.2:
            ranked.append((score, item))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in ranked[:limit]]

def persist_skill_candidate(task, procedure, planner_model, executor_model, path):
    """Guarda una metodología como candidata no verificada; no la activa ni ejecuta."""
    if not isinstance(procedure, list) or not procedure or len(procedure) > 30:
        return None
    clean = [str(step)[:1000] for step in procedure if isinstance(step, str) and step.strip()]
    if not clean:
        return None
    record = {
        "schema_version": "1.0", "status": "candidate_only",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "task": task[:4000], "procedure": clean,
        "planner_model": planner_model, "executor_model": executor_model,
    }
    canonical = json.dumps(record, sort_keys=True, ensure_ascii=False)
    record["candidate_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    memory_file = Path(path)
    memory_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(memory_file.parent, 0o700)
    descriptor = os.open(memory_file, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    os.chmod(memory_file, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\\n")
    return record["candidate_sha256"]

def run_learning_cycle(task, *, planner_model="qwen3.5:9b",
                       executor_model="qwen3.5:2b-q4_K_M",
                       image=DEFAULT_IMAGE, max_rounds=2, base_url=None,
                       timeout=180, docker_bin="docker", memory_path=None):
    if not isinstance(task, str) or not task.strip() or len(task) > 4000:
        raise LabError("La tarea debe contener entre 1 y 4000 caracteres.")
    if isinstance(max_rounds, bool) or not isinstance(max_rounds, int) or not 1 <= max_rounds <= MAX_ROUNDS:
        raise LabError("max_rounds debe estar entre 1 y 3.")
    history = []
    memory_path = Path(memory_path) if memory_path else ROOT / "data" / "autonomous_skill_lab" / "skill_candidates.jsonl"
    remembered = load_skill_memory(task, memory_path)
    plan = _ask_json(
        planner_model,
        "Eres el planificador técnico de CYBER_AI. Diseña una demostración educativa y defensiva "
        "en Rust. No solicites explotación real, robo de secretos ni objetivos externos. "
        "Devuelve JSON con objective, hypothesis, acceptance_criteria y safety_notes. "
        "No incluyas comandos ejecutables.",
        task, base_url=base_url, timeout=timeout,
    )
    for round_number in range(1, max_rounds + 1):
        execution = _ask_json(
            executor_model,
            "Eres el agente ejecutor y aprendiz de CYBER_AI. Convierte la especificación en un "
            "proyecto Rust mínimo que demuestre la hipótesis de forma segura. Devuelve JSON "
            "con files, procedure y expected_result. files solo puede contener Cargo.toml, "
            "src/main.rs y/o src/lib.rs. No incluyas dependencias, build.rs, comandos shell, "
            "acceso a red, secretos ni rutas adicionales. Incluye pruebas unitarias relevantes.",
            json.dumps({"task": task, "plan": plan, "previous_attempts": history, "relevant_skill_candidates": remembered}, ensure_ascii=False),
            base_url=base_url, timeout=timeout,
        )
        try:
            files = validate_generated_files(execution.get("files"))
        except LabError as exc:
            evidence = {"status": "failed", "error": str(exc), "phase": "artifact_validation"}
        else:
            try:
                evidence = run_rust_lab(
                    files, image=image, timeout=min(timeout, 600), docker_bin=docker_bin,
                )
            except LabError as exc:
                evidence = {"status": "inconclusive", "error": str(exc), "phase": "sandbox_execution"}
        attempt = {
            "round": round_number,
            "procedure": execution.get("procedure"),
            "expected_result": execution.get("expected_result"),
            "evidence": evidence,
        }
        history.append(attempt)
        if evidence.get("status") == "passed":
            break
        if round_number < max_rounds:
            plan = _ask_json(
                planner_model,
                "Eres el planificador de CYBER_AI. Analiza el fallo observado, identifica la causa "
                "sin inventar evidencia y revisa la hipótesis o el diseño. Devuelve el mismo esquema "
                "JSON. No propongas comandos ejecutables.",
                json.dumps({"task": task, "previous_plan": plan, "attempts": history}, ensure_ascii=False),
                base_url=base_url, timeout=timeout,
            )

    passed = bool(history and history[-1]["evidence"].get("status") == "passed")
    candidate_hash = persist_skill_candidate(task, history[-1].get("procedure"), planner_model, executor_model, memory_path) if passed else None
    return {
        "schema_version": "1.0",
        "status": "passed" if passed else (
            "failed" if history and history[-1]["evidence"].get("status") == "failed"
            else "inconclusive"
        ),
        "task": task,
        "planner_model": planner_model,
        "executor_model": executor_model,
        "plan": plan,
        "attempts": history,
        "skill_candidate": {
            "status": "candidate_only" if candidate_hash else "not_eligible",
            "candidate_sha256": candidate_hash,
            "memory_path": str(memory_path) if candidate_hash else None,
            "reused_candidates": len(remembered),
            "promotion_rule": "No se promociona automáticamente: requiere repetición independiente y revisión externa.",
            "procedure": history[-1].get("procedure") if history else None,
        },
        "limitations": [
            "El modelo pequeño no modifica sus pesos; aprende y reutiliza procedimientos externos versionados.",
            "La prueba inicial solo compila y ejecuta proyectos Rust sin dependencias en un contenedor aislado.",
            "Un cargo test exitoso demuestra los tests generados, no la verdad general de la hipótesis.",
            "La promoción de skills requiere validación independiente y no ocurre en este prototipo.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--planner-model", default=os.environ.get("CYBER_AI_PLANNER_MODEL", "qwen3.5:9b"))
    parser.add_argument("--executor-model", default=os.environ.get("CYBER_AI_EXECUTOR_MODEL", "qwen3.5:2b-q4_K_M"))
    parser.add_argument("--image", default=os.environ.get("CYBER_AI_RUST_LAB_IMAGE", DEFAULT_IMAGE))
    parser.add_argument("--max-rounds", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", default="reports/skill_lab/latest.json")
    parser.add_argument("--memory-path", default="data/autonomous_skill_lab/skill_candidates.jsonl")
    args = parser.parse_args(argv)
    try:
        result = run_learning_cycle(
            args.task, planner_model=args.planner_model, executor_model=args.executor_model,
            image=args.image, max_rounds=args.max_rounds, timeout=args.timeout,
            memory_path=ROOT / args.memory_path,
        )
        output = ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "passed" else 1
    except (LabError, OSError, ValueError) as exc:
        print(json.dumps({"status": "inconclusive", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
