#!/usr/bin/env python3
"""Motor inicial de experimentos reproducibles para CYBER_AI.

Solo permite ejecutar archivos test_*.py situados dentro de tests/.
La ejecución requiere --execute explícitamente.
Esta restricción no convierte pytest en un sandbox para código no confiable.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

import evidence_graph
from compressed_evidence import store_evidence

PROJECT = Path(__file__).resolve().parent
MAX_TIMEOUT_SECONDS = 120
MAX_CAPTURE_BYTES = 12000


def validate_test_path(test_path):
    """Acepta únicamente archivos Python test_*.py dentro de tests/."""
    project = PROJECT.resolve()
    tests_root = (project / "tests").resolve()
    candidate = Path(test_path)

    if not candidate.is_absolute():
        candidate = project / candidate

    candidate = candidate.resolve()

    try:
        relative = candidate.relative_to(tests_root)
    except ValueError as error:
        raise ValueError(
            "El experimento solo puede usar archivos dentro de tests/."
        ) from error

    if (
        not candidate.is_file()
        or candidate.suffix != ".py"
        or not candidate.name.startswith("test_")
    ):
        raise ValueError("El objetivo debe ser un archivo existente test_*.py.")

    return candidate, (Path("tests") / relative).as_posix()


def build_plan(hypothesis, test_path, timeout=60):
    """Valida la hipótesis y construye un plan sin ejecutar ni guardar datos."""
    if not isinstance(hypothesis, str) or not hypothesis.strip():
        raise ValueError("La hipótesis es obligatoria.")

    if len(hypothesis) > 2000:
        raise ValueError("La hipótesis no puede superar 2000 caracteres.")

    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, int)
        or not 1 <= timeout <= MAX_TIMEOUT_SECONDS
    ):
        raise ValueError(
            f"timeout debe ser un entero entre 1 y {MAX_TIMEOUT_SECONDS}."
        )

    _, relative_path = validate_test_path(test_path)
    experiment_id = uuid.uuid4().hex

    return {
        "experiment_id": experiment_id,
        "status": "planned",
        "hypothesis": hypothesis.strip(),
        "test_path": relative_path,
        "timeout_seconds": timeout,
        "command": [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            relative_path,
        ],
        "executed": False,
        "security_conclusion": "not_determined_by_test_runner",
    }


def _summarize_stream(stream):
    """Calcula el hash de toda la salida y conserva solo sus últimos bytes."""
    stream.flush()
    stream.seek(0, os.SEEK_END)
    size = stream.tell()

    digest = hashlib.sha256()
    stream.seek(0)

    while True:
        chunk = stream.read(65536)
        if not chunk:
            break
        digest.update(chunk)

    stream.seek(max(0, size - MAX_CAPTURE_BYTES))
    tail = stream.read(MAX_CAPTURE_BYTES)

    return {
        "text": tail.decode("utf-8", errors="replace"),
        "sha256": digest.hexdigest(),
        "bytes": size,
        "truncated": size > MAX_CAPTURE_BYTES,
    }


def _interpret_outcome(status):
    """No confunde el resultado de pytest con un veredicto de seguridad."""
    interpretations = {
        "passed": (
            "Las pruebas terminaron correctamente. Esto solo respalda los "
            "casos examinados; no demuestra la ausencia general de "
            "vulnerabilidades."
        ),
        "failed": (
            "Una o más pruebas fallaron. Deben revisarse la aserción y "
            "la salida; un test fallido no demuestra por sí solo una "
            "vulnerabilidad."
        ),
        "timeout": (
            "La ejecución superó el tiempo permitido. El resultado es "
            "inconcluso: no confirma ni refuta la hipótesis."
        ),
        "execution_error": (
            "No se pudo iniciar pytest. No se obtuvo evidencia de una "
            "ejecución válida."
        ),
    }
    return interpretations[status]


def run_experiment(*, hypothesis, test_path, timeout=60, execute=False):
    """Prepara un experimento o lo ejecuta y registra sus resultados reales."""
    plan = build_plan(hypothesis, test_path, timeout=timeout)

    # El modo predeterminado es solo de planificación y no crea registros.
    if not execute:
        return plan

    session_id = evidence_graph.create_session(
        name=f"Experimento {plan['experiment_id'][:8]}"
    )

    started = time.monotonic()
    return_code = None
    error_message = None

    # Usamos archivos temporales para no acumular una salida ilimitada
    # en memoria durante la ejecución de pytest.
    with (
        tempfile.TemporaryFile(mode="w+b") as stdout_file,
        tempfile.TemporaryFile(mode="w+b") as stderr_file,
    ):
        try:
            result = subprocess.run(
                plan["command"],
                cwd=PROJECT,
                stdout=stdout_file,
                stderr=stderr_file,
                timeout=timeout,
                check=False,
            )
            return_code = result.returncode
            status = "passed" if return_code == 0 else "failed"

        except subprocess.TimeoutExpired:
            status = "timeout"
            error_message = f"Tiempo límite agotado: {timeout} segundos."

        except OSError as error:
            status = "execution_error"
            error_message = f"{type(error).__name__}: {error}"

        elapsed = round(time.monotonic() - started, 3)
        stdout = _summarize_stream(stdout_file)
        stderr = _summarize_stream(stderr_file)

    report = {
        **plan,
        "status": status,
        "executed": True,
        "return_code": return_code,
        "elapsed_seconds": elapsed,
        "stdout": stdout["text"],
        "stdout_sha256": stdout["sha256"],
        "stdout_bytes": stdout["bytes"],
        "stdout_truncated": stdout["truncated"],
        "stderr": stderr["text"],
        "stderr_sha256": stderr["sha256"],
        "stderr_bytes": stderr["bytes"],
        "stderr_truncated": stderr["truncated"],
        "error": error_message,
        "outcome_interpretation": _interpret_outcome(status),
        "security_conclusion": "not_determined_by_test_runner",
    }

    # Guardar la hipótesis y el resultado en la sesión de evidencia existente.
    hypothesis_node = evidence_graph.add_node(
        kind="hypothesis",
        content=plan["hypothesis"],
        task_id=plan["experiment_id"],
        session_id=session_id,
        status="tested",
        metadata={
            "experiment_id": plan["experiment_id"],
            "test_path": plan["test_path"],
            "test_status": status,
        },
    )
    report["session_id"] = session_id
    report["hypothesis_node_id"] = hypothesis_node

    evidence = store_evidence(
        title=f"Resultado de experimento {plan['experiment_id'][:8]}",
        content=json.dumps(report, ensure_ascii=False, indent=2),
        session_id=session_id,
        task_id=plan["experiment_id"],
        kind="experiment_result",
        status=status,
        metadata={
            "experiment_id": plan["experiment_id"],
            "test_path": plan["test_path"],
            "return_code": return_code,
            "elapsed_seconds": elapsed,
            "stdout_sha256": stdout["sha256"],
            "stderr_sha256": stderr["sha256"],
            "security_conclusion": "not_determined_by_test_runner",
        },
    )

    report["evidence_node_id"] = evidence["node_id"]
    report["compressed_block_id"] = evidence["block_id"]

    edge_id = evidence_graph.add_edge(
        hypothesis_node,
        "tested_by",
        evidence["node_id"],
        metadata={
            "experiment_id": plan["experiment_id"],
            "test_status": status,
        },
    )
    report["evidence_edge_id"] = edge_id

    report_dir = PROJECT / "reports" / "experiments"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"experiment_{plan['experiment_id']}.json"

    report["report_path"] = report_path.relative_to(PROJECT).as_posix()
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hypothesis", required=True, help="Hipótesis comprobable")
    parser.add_argument("--test", required=True, help="Archivo test_*.py dentro de tests/")
    parser.add_argument(
        "--timeout", type=int, default=60,
        help=f"Tiempo máximo en segundos (1-{MAX_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help="Ejecutar pytest y registrar las salidas reales",
    )
    args = parser.parse_args(argv)

    try:
        report = run_experiment(
            hypothesis=args.hypothesis,
            test_path=args.test,
            timeout=args.timeout,
            execute=args.execute,
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not args.execute:
        print("Plan validado: no se ejecutó ninguna prueba.")
        return 0

    # Código de salida de la herramienta distinto del resultado de la prueba.
    if report["status"] == "passed":
        return 0
    if report["status"] == "timeout":
        return 3
    if report["status"] == "execution_error":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
