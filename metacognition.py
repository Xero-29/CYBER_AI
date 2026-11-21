#!/usr/bin/env python3
"""Ciclo metacognitivo: evaluar conocimiento, investigar brechas y verificar antes de continuar.

El motor no certifica dominio por autodeclaración. Solo registra conocimiento validado
cuando un verificador separado aprueba la evidencia; el resultado queda trazable.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import stat
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from process_isolation import ProcessIsolationError, run_bounded_process
from safe_io import (
    SafeWriteError, atomic_write_text, ensure_private_directory, open_private_file,
)
from secret_redaction import redact_sensitive_data, redact_text

PROJECT = Path(__file__).resolve().parent
STATE_DIR = PROJECT / "data" / "metacognition"
STATE_FILE = STATE_DIR / "competency_map.json"
RESEARCH_LOG = STATE_DIR / "research_log.jsonl"
MAX_RESEARCH_ROUNDS = 2
MAX_TASK_CHARS = 20_000
MAX_CONTEXT_CHARS = 30_000
MAX_REPORT_CHARS = 100_000
MAX_STATE_BYTES = 4 * 1024 * 1024
MAX_LOG_BYTES = 64 * 1024 * 1024
MAX_EVENT_BYTES = 2 * 1024 * 1024
MAX_GAPS = 32
ANSWER_MARKER = "=== RESPUESTA ==="


class MetacognitionError(RuntimeError):
    """El ciclo no puede continuar sin preservar sus límites de seguridad."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON contiene claves duplicadas.")
        result[key] = value
    return result


def _enforce_json_depth(text: str, max_depth: int = 64) -> None:
    depth = 0
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if depth > max_depth:
                raise MetacognitionError("El JSON supera la profundidad permitida.")
        elif character in "]}":
            depth -= 1
            if depth < 0:
                raise MetacognitionError("El JSON tiene delimitadores desbalanceados.")
    if in_string or depth != 0:
        raise MetacognitionError("El JSON está incompleto o mal formado.")


def _decode_json(raw: bytes) -> Any:
    text = raw.decode("utf-8")
    _enforce_json_depth(text)
    return json.loads(text, object_pairs_hook=_unique_object)


def _read_private_json(path: Path, default: Any) -> Any:
    path = Path(path)
    ensure_private_directory(path.parent, create=True)
    try:
        with open_private_file(path, "rb") as stream:
            raw = stream.read(MAX_STATE_BYTES + 1)
    except SafeWriteError as error:
        if not path.exists() and not path.is_symlink():
            return default
        raise MetacognitionError("El estado metacognitivo no es un archivo privado seguro.") from error
    if len(raw) > MAX_STATE_BYTES:
        raise MetacognitionError("El estado metacognitivo supera 4 MiB.")
    try:
        return _decode_json(raw)
    except (UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        raise MetacognitionError("El estado metacognitivo está dañado o no es JSON válido.") from error


def _read_json(path: Path, default: Any, *, max_bytes: int = MAX_REPORT_CHARS * 4) -> Any:
    """Lee un informe del repositorio con ruta confinada, sin symlinks ni tamaño ilimitado."""
    path = Path(path)
    try:
        resolved = path.resolve(strict=True)
        relative = resolved.relative_to(PROJECT.resolve())
    except FileNotFoundError:
        return default
    except (OSError, ValueError) as error:
        raise MetacognitionError("La ruta del informe no está confinada al repositorio.") from error
    current = PROJECT.resolve()
    for index, part in enumerate(relative.parts):
        current = current / part
        try:
            info = current.lstat()
        except OSError as error:
            raise MetacognitionError("No se pudo inspeccionar la ruta del informe.") from error
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            raise MetacognitionError("No se permiten symlinks ni puntos de reanálisis en informes.")
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise MetacognitionError("Un componente de la ruta del informe no es directorio.")
        if index == len(relative.parts) - 1 and not stat.S_ISREG(info.st_mode):
            raise MetacognitionError("El informe debe ser un archivo regular.")
    descriptor = None
    try:
        before = resolved.lstat()
        descriptor = os.open(resolved, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
        opened = os.fstat(descriptor)
        if opened.st_size > max_bytes:
            raise MetacognitionError("El informe supera el límite de lectura.")
        chunks = []
        total = 0
        while True:
            block = os.read(descriptor, min(8192, max_bytes + 1 - total))
            if not block:
                break
            total += len(block)
            if total > max_bytes:
                raise MetacognitionError("El informe supera el límite de lectura.")
            chunks.append(block)
        after = os.fstat(descriptor)
        path_after = resolved.lstat()
        if (
            (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
            or (opened.st_dev, opened.st_ino) != (after.st_dev, after.st_ino)
            or (after.st_dev, after.st_ino) != (path_after.st_dev, path_after.st_ino)
            or after.st_size != opened.st_size
            or after.st_mtime_ns != opened.st_mtime_ns
            or total != after.st_size
        ):
            raise MetacognitionError("El informe cambió durante su lectura.")
        return _decode_json(b"".join(chunks))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        if isinstance(error, MetacognitionError):
            raise
        raise MetacognitionError("No se pudo leer un informe JSON seguro.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


@contextmanager
def _state_lock(path: Path):
    ensure_private_directory(path.parent, create=True)
    lock_path = path.parent / ".metacognition.lock"
    with open_private_file(lock_path, "a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def load_competency_map(path: Path = STATE_FILE) -> dict:
    default = {"schema_version": 1, "competencies": {}, "updated_at": None}
    data = _read_private_json(path, default)
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != 1
        or not isinstance(data.get("competencies"), dict)
    ):
        raise MetacognitionError("El mapa de competencias no cumple el esquema esperado.")
    return data


def _save_competency_map_unlocked(data: dict, path: Path) -> None:
    if not isinstance(data, dict) or not isinstance(data.get("competencies"), dict):
        raise MetacognitionError("El mapa de competencias no cumple el esquema esperado.")
    data["schema_version"] = 1
    data["updated_at"] = _now()
    rendered = json.dumps(redact_sensitive_data(data), ensure_ascii=False, indent=2) + "\n"
    if len(rendered.encode("utf-8")) > MAX_STATE_BYTES:
        raise MetacognitionError("El mapa de competencias supera 4 MiB.")
    ensure_private_directory(path.parent, create=True)
    atomic_write_text(path, rendered, mode=0o600)


def save_competency_map(data: dict, path: Path = STATE_FILE) -> None:
    with _state_lock(path):
        _save_competency_map_unlocked(data, path)


def append_event(event: dict, path: Path = RESEARCH_LOG) -> None:
    safe_event = redact_sensitive_data(event)
    rendered = json.dumps(safe_event, ensure_ascii=False, separators=(",", ":")) + "\n"
    encoded_size = len(rendered.encode("utf-8"))
    if encoded_size > MAX_EVENT_BYTES:
        raise MetacognitionError("El evento de investigación supera 2 MiB.")
    ensure_private_directory(path.parent, create=True)
    with _state_lock(path):
        with open_private_file(path, "a") as stream:
            if os.fstat(stream.fileno()).st_size + encoded_size > MAX_LOG_BYTES:
                raise MetacognitionError("El registro de investigación alcanzó 64 MiB.")
            stream.write(rendered)


def extract_json_object(text: str) -> dict:
    """Extrae un objeto JSON sin ejecutar contenido ni aceptar arrays como raíz."""
    if not isinstance(text, str):
        raise ValueError("La respuesta del modelo no es texto.")
    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", text):
        try:
            value, _ = decoder.raw_decode(text[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError("El modelo no devolvió un objeto JSON válido.")


def validate_assessment(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Evaluación inválida.")
    sufficient = value.get("knowledge_sufficient")
    confidence = value.get("confidence")
    gaps = value.get("gaps", [])
    if not isinstance(sufficient, bool):
        raise ValueError("knowledge_sufficient debe ser booleano.")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ValueError("confidence debe estar entre 0 y 1.")
    if not isinstance(gaps, list):
        raise ValueError("gaps debe ser una lista.")
    clean_gaps = []
    for item in gaps:
        if not isinstance(item, dict) or not str(item.get("topic", "")).strip():
            raise ValueError("Cada brecha necesita un topic.")
        prerequisites = item.get("prerequisites", [])
        if not isinstance(prerequisites, list):
            raise ValueError("prerequisites debe ser una lista.")
        priority = item.get("priority", 3)
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 5:
            raise ValueError("priority debe ser un entero de 1 a 5.")
        clean_gaps.append({
            "topic": str(item["topic"]).strip(),
            "why": str(item.get("why", "")).strip(),
            "prerequisites": [str(x).strip() for x in prerequisites if str(x).strip()],
            "priority": priority,
        })
    # Si declara suficiencia, no puede ocultar brechas críticas en la misma respuesta.
    if sufficient and confidence < 0.75:
        sufficient = False
    if sufficient and any(item["priority"] >= 4 for item in clean_gaps):
        sufficient = False
    return {
        "knowledge_sufficient": sufficient,
        "confidence": float(confidence),
        "known_topics": value.get("known_topics", []) if isinstance(value.get("known_topics", []), list) else [],
        "gaps": clean_gaps,
        "uncertainties": value.get("uncertainties", []) if isinstance(value.get("uncertainties", []), list) else [],
        "reasoning_summary": str(value.get("reasoning_summary", ""))[:3000],
    }


def build_assessment_prompt(task: str, knowledge_context: str = "", prior_state: dict | None = None) -> str:
    return (
        "Actúas como la IA PRINCIPAL de CYBER_AI. Antes de resolver la tarea, evalúa "
        "honestamente si tienes conocimiento suficiente. No confundas familiaridad con dominio. "
        "Considera la biblioteca recuperada como evidencia de disponibilidad, no como prueba "
        "de comprensión. Identifica subtemas, fundamentos y prerrequisitos que falten. "
        "Si existe incertidumbre importante, declara insuficiencia. No inventes competencias.\n"
        "Devuelve SOLO un objeto JSON con este esquema: "
        '{"knowledge_sufficient":false,"confidence":0.0,"known_topics":[],"gaps":'
        '[{"topic":"...","why":"...","prerequisites":["..."],"priority":1}],'
        '"uncertainties":["..."],"reasoning_summary":"..."}\n'
        "confidence es una estimación calibrada, no una certificación. "
        "Una tarea compleja exige descomponer conocimientos y requisitos.\n\n"
        f"TAREA:\n{task}\n\n"
        f"CONOCIMIENTO RECUPERADO:\n{knowledge_context or '[sin contexto recuperado]'}\n\n"
        f"MAPA DE COMPETENCIAS PREVIO:\n{json.dumps(prior_state or {}, ensure_ascii=False)[:8000]}"
    )


def build_research_request(task: str, assessment: dict, knowledge_context: str = "") -> str:
    return (
        "Eres el INVESTIGADOR AUTÓNOMO de CYBER_AI. Investiga exclusivamente las brechas "
        "indicadas para permitir resolver la tarea. Trabaja en orden de prerrequisitos: "
        "primero fundamentos faltantes y después temas dependientes. Distingue hechos, "
        "inferencias, hipótesis y cuestiones no resueltas. No inventes citas, DOI, URLs, "
        "experimentos ni resultados. Si no puedes consultar fuentes externas, dilo claramente "
        "y entrega una agenda de investigación, no simules haber investigado. "
        "Prioriza fuentes primarias, estándares, documentación oficial y artículos revisados. "
        "Incluye para cada afirmación importante su fuente y fecha si están disponibles. "
        "Entrega: mapa de brechas, fundamentos, explicación técnica, métodos/algoritmos, "
        "ejemplos reproducibles, limitaciones, contradicciones, fuentes trazables y preguntas abiertas.\n\n"
        f"TAREA ORIGINAL:\n{task}\n\n"
        f"DIAGNÓSTICO DE LA IA PRINCIPAL:\n{json.dumps(assessment, ensure_ascii=False)}\n\n"
        f"CONTEXTO RECUPERADO:\n{knowledge_context or '[sin contexto recuperado]'}"
    )


def build_verification_prompt(task: str, assessment: dict, research: str) -> str:
    return (
        "Eres un verificador independiente. No eres el investigador ni la IA principal. "
        "Evalúa si el informe responde a las brechas, si sus afirmaciones están respaldadas "
        "por fuentes trazables, si separa hechos de hipótesis y si declara límites. "
        "No apruebes citas no verificables ni afirmaciones sin evidencia. La aprobación "
        "significa que el informe puede incorporarse como conocimiento provisional revisado, "
        "no que el agente ya domina el tema. Devuelve SOLO JSON: "
        '{"approved":false,"score":0,"evidence_quality":"insufficient",'
        '"gaps_remaining":["..."],"reasons":["..."]}. '
        "score debe ser entero de 0 a 100.\n\n"
        f"TAREA:\n{task}\n\nDIAGNÓSTICO:\n{json.dumps(assessment, ensure_ascii=False)}"
        f"\n\nINFORME A VERIFICAR:\n{research[:24000]}"
    )


def _runner_call(agent: str, prompt: str, *, knowledge: bool = True, timeout: int = 1800) -> str:
    command = [sys.executable, str(PROJECT / "agent_runner.py"), "ask", agent, "--task-text", prompt]
    if knowledge:
        command.append("--knowledge")
    completed = subprocess.run(
        command, cwd=PROJECT, capture_output=True, text=True, timeout=timeout, check=False
    )
    if completed.returncode:
        detail = (completed.stderr or completed.stdout)[-4000:]
        raise RuntimeError(f"Agente {agent} falló (código {completed.returncode}): {detail}")
    output = completed.stdout
    if ANSWER_MARKER in output:
        output = output.rsplit(ANSWER_MARKER, 1)[1]
    answer = output.strip()
    if not answer:
        raise RuntimeError(f"Agente {agent} devolvió una respuesta vacía.")
    return answer


def publish_research_report(report: str, task_id: str) -> dict:
    """Indexa el informe aprobado como conocimiento provisional, nunca como dominio."""
    from knowledge_embeddings import generate_embedding
    from knowledge_library import store_chunks

    vector = generate_embedding(report, agent_name="ECO")
    embedding_model = vector.get("embedding_space") or vector.get("model")
    stored = store_chunks([{
        "title": "Investigación metacognitiva " + task_id,
        "source": "metacognition://" + task_id,
        "license": "UNSPECIFIED",
        "category": "research_provisional",
        "tags": ["metacognition", "ai-research", "provisional", "independently-reviewed"],
        "visibility": "shared",
        "content": report,
        "embedding": vector["embedding"],
        "embedding_model": embedding_model,
    }])
    return {"indexed": True, "document": stored[0]}


def collect_web_evidence(task: str, assessment: dict, *, timeout: int = 900) -> str:
    """Consulta el buscador curado y ejecuta revisión de fuentes existente.

    Solo devuelve informes generados por web_research.py y review_web_report.py.
    Un fallo o ausencia de fuentes se declara explícitamente; nunca se simula búsqueda.
    """
    gaps = assessment.get("gaps", [])[:4]
    if not gaps:
        return "No se definieron brechas concretas; no se lanzó búsqueda web."
    collected = []
    for gap in gaps:
        query = f"{task} {gap['topic']} " + " ".join(gap.get("prerequisites", [])[:3])
        search = subprocess.run(
            [sys.executable, str(PROJECT / "web_research.py"), query,
             "--max-results", "5"],
            cwd=PROJECT, capture_output=True, text=True, timeout=timeout, check=False,
        )
        output = (search.stdout or "") + "\n" + (search.stderr or "")
        match = re.search(r"Datos JSON:\s*(reports/web_research/[^\s]+\.json)", output)
        if search.returncode != 0 or not match:
            collected.append(
                f"BRECHA: {gap['topic']}\nESTADO: búsqueda fallida o sin informe. "
                f"DETALLE: {output[-1200:]}"
            )
            continue
        relative = Path(match.group(1))
        report_path = (PROJECT / relative).resolve()
        if PROJECT.resolve() not in report_path.parents or not report_path.is_file():
            collected.append(f"BRECHA: {gap['topic']}\nESTADO: ruta de informe no válida.")
            continue
        report = _read_json(report_path, {})
        if report.get("search_status") != "ok" or not report.get("results"):
            collected.append(
                f"BRECHA: {gap['topic']}\nESTADO: sin resultados confiables. "
                "No se interpreta la ausencia de resultados como ausencia de conocimiento."
            )
            continue
        review = subprocess.run(
            [sys.executable, str(PROJECT / "review_web_report.py"), str(relative)],
            cwd=PROJECT, capture_output=True, text=True, timeout=timeout, check=False,
        )
        review_output = (review.stdout or "") + "\n" + (review.stderr or "")
        draft_match = re.search(r"(reports/web_research/[^\s]+\.md)", review_output)
        draft_text = ""
        if draft_match:
            draft_path = (PROJECT / draft_match.group(1)).resolve()
            if PROJECT.resolve() in draft_path.parents and draft_path.is_file():
                draft_text = draft_path.read_text(encoding="utf-8")[:12000]
        collected.append(
            f"BRECHA: {gap['topic']}\nESTADO DE BÚSQUEDA: {report.get('search_status')}\n"
            f"ESTADO DE REVISIÓN: {'completada' if review.returncode == 0 else 'fallida'}\n"
            f"DATOS DE FUENTES:\n{json.dumps(report, ensure_ascii=False)[:12000]}\n"
            f"BORRADOR DE REVISIÓN:\n{draft_text or review_output[-5000:]}"
        )
    return "\n\n--- SIGUIENTE BRECHA ---\n\n".join(collected)[:30000]


def run_cycle(
    task: str,
    *,
    principal: str,
    researcher: str,
    verifier: str,
    model_call: Callable[[str, str], str] = _runner_call,
    publisher: Callable[[str, str], dict] = publish_research_report,
    source_researcher: Callable[[str, dict], str] = collect_web_evidence,
    knowledge_context: str = "",
    state_path: Path = STATE_FILE,
    log_path: Path = RESEARCH_LOG,
    max_rounds: int = MAX_RESEARCH_ROUNDS,
) -> dict:
    """Ejecuta evaluación → investigación → verificación → reevaluación.

    model_call recibe (nombre_agente, prompt). Los callbacks facilitan pruebas y
    permiten sustituir proveedores sin cambiar el controlador.
    """
    if not task.strip():
        raise ValueError("La tarea no puede estar vacía.")
    if principal == researcher or principal == verifier or researcher == verifier:
        raise ValueError("Principal, investigador y verificador deben ser roles separados.")
    if not 1 <= max_rounds <= 5:
        raise ValueError("max_rounds debe estar entre 1 y 5.")

    state = load_competency_map(state_path)
    assessment = validate_assessment(extract_json_object(
        model_call(principal, build_assessment_prompt(task, knowledge_context, state))
    ))
    if assessment["knowledge_sufficient"]:
        return {"status": "sufficient", "assessment": assessment, "research_rounds": 0}

    task_id = uuid.uuid4().hex
    accepted_reports = []
    all_reports_indexed = True
    for round_number in range(1, max_rounds + 1):
        if not assessment["gaps"]:
            break
        source_evidence = source_researcher(task, assessment)
        research_context = (
            knowledge_context + "\n\nEVIDENCIA DE INVESTIGACIÓN WEB CURADA:\n"
            + source_evidence
        )[-30000:]
        research = model_call(
            researcher, build_research_request(task, assessment, research_context)
        )
        verification = extract_json_object(
            model_call(verifier, build_verification_prompt(task, assessment, research))
        )
        approved = verification.get("approved") is True
        score = verification.get("score", 0)
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 100:
            approved = False
            score = 0
        event = {
            "task_id": task_id, "round": round_number, "created_at": _now(),
            "task": task, "principal": principal, "researcher": researcher,
            "verifier": verifier, "assessment": assessment, "research": research,
            "verification": verification, "status": "verified_provisional" if approved else "rejected",
        }
        append_event(event, log_path)
        if not approved:
            return {
                "status": "verification_failed", "task_id": task_id,
                "assessment": assessment, "verification": verification,
                "research_rounds": round_number,
            }
        accepted_reports.append(event)
        try:
            publication = publisher(research, task_id)
        except Exception as publish_error:
            publication = {
                "indexed": False,
                "error": type(publish_error).__name__ + ": " + str(publish_error)[:500],
            }
        all_reports_indexed = all_reports_indexed and bool(publication.get("indexed"))
        # "known" significa informe revisado; no significa dominio. El estado
        # registra por separado si el informe quedó indexado para recuperación.
        for gap in assessment["gaps"]:
            key = gap["topic"].casefold()
            state["competencies"][key] = {
                "topic": gap["topic"], "status": "known",
                "source_task_id": task_id, "verification_score": score,
                "verified_at": _now(), "prerequisites": gap["prerequisites"],
                "evidence_log": str(log_path),
                "library_indexed": bool(publication.get("indexed")),
                "library_document": publication.get("document", {}).get("document_id"),
            }
        save_competency_map(state, state_path)
        # Entregar también el informe aceptado directamente al principal para
        # reevaluación, aunque la indexación semántica esté temporalmente caída.
        knowledge_context = (
            knowledge_context + "\n\nINFORME REVISADO PROVISIONALMENTE:\n" + research
        )[-30000:]
        assessment = validate_assessment(extract_json_object(
            model_call(principal, build_assessment_prompt(task, knowledge_context, state))
        ))
        if assessment["knowledge_sufficient"]:
            if not all_reports_indexed:
                return {
                    "status": "knowledge_acquired_not_indexed",
                    "task_id": task_id, "assessment": assessment,
                    "accepted_reports": len(accepted_reports), "research_rounds": round_number,
                    "note": "El conocimiento fue revisado, pero no quedó indexado; se bloquea la ejecución para no perder el contexto adquirido.",
                }
            return {
                "status": "knowledge_acquired_needs_task_execution",
                "task_id": task_id, "assessment": assessment,
                "accepted_reports": len(accepted_reports), "research_rounds": round_number,
                "note": "La tarea original aún debe ejecutarse y evaluarse; investigación aprobada no equivale a dominio.",
            }
    return {
        "status": "insufficient_after_research", "task_id": task_id,
        "assessment": assessment, "accepted_reports": len(accepted_reports),
        "research_rounds": len(accepted_reports),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", choices=["run"])
    parser.add_argument("--principal", required=True)
    parser.add_argument("--researcher", default="INVESTIGADOR")
    parser.add_argument("--verifier", default="VERITAS")
    parser.add_argument("--task-text", required=True)
    parser.add_argument("--no-knowledge", action="store_true")
    parser.add_argument("--max-rounds", type=int, default=MAX_RESEARCH_ROUNDS)
    args = parser.parse_args()
    try:
        def selected_backend(agent_name: str, prompt: str) -> str:
            return _runner_call(
                agent_name, prompt, knowledge=not args.no_knowledge
            )

        result = run_cycle(
            args.task_text, principal=args.principal, researcher=args.researcher,
            verifier=args.verifier, model_call=selected_backend,
            knowledge_context="", max_rounds=args.max_rounds,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["status"] in {"verification_failed", "insufficient_after_research", "knowledge_acquired_not_indexed"}:
            return 2
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"Error en ciclo metacognitivo: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
