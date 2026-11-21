#!/usr/bin/env python3
"""Ciclo metacognitivo: evaluar conocimiento, investigar brechas y verificar antes de continuar.

El motor no certifica dominio por autodeclaración. Solo registra conocimiento validado
cuando un verificador separado aprueba la evidencia; el resultado queda trazable.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import math
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
            elif character == "\\":
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
    """Extrae un objeto JSON acotado, sin claves duplicadas ni anidamiento excesivo."""
    if not isinstance(text, str) or len(text) > MAX_REPORT_CHARS:
        raise ValueError("La respuesta del modelo debe ser texto de hasta 100.000 caracteres.")
    decoder = json.JSONDecoder(object_pairs_hook=_unique_object)
    for match in re.finditer(r"\{", text):
        try:
            value, end = decoder.raw_decode(text[match.start():])
        except (json.JSONDecodeError, ValueError, RecursionError):
            continue
        if isinstance(value, dict):
            _enforce_json_depth(text[match.start():match.start() + end])
            return value
    raise ValueError("El modelo no devolvió un objeto JSON válido.")


def _bounded_text_list(value, field, *, maximum=64, item_chars=240):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError(f"{field} debe ser una lista de hasta {maximum} elementos.")
    cleaned = []
    for item in value:
        if not isinstance(item, str) or not item.strip() or len(item) > item_chars:
            raise ValueError(f"{field} contiene un elemento inválido.")
        cleaned.append(item.strip())
    return cleaned


def validate_assessment(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Evaluación inválida.")
    sufficient = value.get("knowledge_sufficient")
    confidence = value.get("confidence")
    gaps = value.get("gaps", [])
    if not isinstance(sufficient, bool):
        raise ValueError("knowledge_sufficient debe ser booleano.")
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not math.isfinite(float(confidence))
        or not 0 <= confidence <= 1
    ):
        raise ValueError("confidence debe ser finita y estar entre 0 y 1.")
    if not isinstance(gaps, list) or len(gaps) > MAX_GAPS:
        raise ValueError(f"gaps debe ser una lista de hasta {MAX_GAPS} elementos.")
    clean_gaps = []
    seen_topics = set()
    for item in gaps:
        if not isinstance(item, dict):
            raise ValueError("Cada brecha debe ser un objeto.")
        topic = item.get("topic")
        why = item.get("why", "")
        prerequisites = item.get("prerequisites", [])
        priority = item.get("priority", 3)
        if not isinstance(topic, str) or not topic.strip() or len(topic) > 240:
            raise ValueError("Cada brecha necesita un topic de hasta 240 caracteres.")
        key = topic.strip().casefold()
        if key in seen_topics:
            raise ValueError("La evaluación contiene brechas duplicadas.")
        seen_topics.add(key)
        if not isinstance(why, str) or len(why) > 2000:
            raise ValueError("why debe ser texto de hasta 2.000 caracteres.")
        if not isinstance(prerequisites, list) or len(prerequisites) > 16:
            raise ValueError("prerequisites debe contener hasta 16 elementos.")
        clean_prerequisites = []
        for prerequisite in prerequisites:
            if not isinstance(prerequisite, str) or not prerequisite.strip() or len(prerequisite) > 240:
                raise ValueError("Cada prerrequisito debe ser texto de hasta 240 caracteres.")
            clean_prerequisites.append(prerequisite.strip())
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 5:
            raise ValueError("priority debe ser un entero de 1 a 5.")
        clean_gaps.append({
            "topic": topic.strip(),
            "why": why.strip(),
            "prerequisites": clean_prerequisites,
            "priority": priority,
        })
    known_topics = _bounded_text_list(value.get("known_topics", []), "known_topics")
    uncertainties = _bounded_text_list(value.get("uncertainties", []), "uncertainties")
    reasoning_summary = value.get("reasoning_summary", "")
    if not isinstance(reasoning_summary, str) or len(reasoning_summary) > 3000:
        raise ValueError("reasoning_summary debe ser texto de hasta 3.000 caracteres.")
    # Una declaración de suficiencia no puede ocultar brechas críticas ni incertidumbre.
    if sufficient and (
        confidence < 0.75
        or uncertainties
        or any(item["priority"] >= 4 for item in clean_gaps)
        or clean_gaps
    ):
        sufficient = False
    return {
        "knowledge_sufficient": sufficient,
        "confidence": float(confidence),
        "known_topics": known_topics,
        "gaps": clean_gaps,
        "uncertainties": uncertainties,
        "reasoning_summary": reasoning_summary.strip(),
    }


def validate_verification(value: dict) -> dict:
    if not isinstance(value, dict) or not isinstance(value.get("approved"), bool):
        raise ValueError("La verificación debe declarar approved como booleano.")
    score = value.get("score")
    quality = value.get("evidence_quality", "insufficient")
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 100:
        raise ValueError("score debe ser un entero de 0 a 100.")
    if not isinstance(quality, str) or quality not in {
        "insufficient", "low", "medium", "good", "high", "strong", "excellent",
    }:
        raise ValueError("evidence_quality no pertenece al vocabulario permitido.")
    gaps_remaining = _bounded_text_list(
        value.get("gaps_remaining", []), "gaps_remaining", maximum=MAX_GAPS
    )
    reasons = _bounded_text_list(
        value.get("reasons", []), "reasons", maximum=32, item_chars=1000
    )
    approved = (
        value["approved"]
        and score >= 75
        and quality in {"good", "high", "strong", "excellent"}
        and not gaps_remaining
    )
    return {
        "approved": approved,
        "score": score,
        "evidence_quality": quality,
        "gaps_remaining": gaps_remaining,
        "reasons": reasons,
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


def _provider_context(agent_names, *, capability="chat"):
    from llm_providers import resolve_provider
    from model_memory_manager import load_config, resolve_agent

    config = load_config()
    meta = config.get("metacognition", {})
    allow_remote = (
        isinstance(meta, dict)
        and meta.get("allow_remote_provider") is True
        and os.environ.get("CYBER_AI_METACOGNITION_ALLOW_REMOTE") == "1"
    )
    providers = []
    for agent_name in agent_names:
        _, agent = resolve_agent(agent_name, config)
        provider = resolve_provider(config, agent, capability=capability)
        if provider.get("protocol") != "ollama" and not allow_remote:
            raise MetacognitionError(
                "Proveedor remoto bloqueado para metacognición; requiere "
                "allow_remote_provider=true y CYBER_AI_METACOGNITION_ALLOW_REMOTE=1."
            )
        providers.append(provider)
    return config, providers, allow_remote


def _child_environment(home: str, config: dict, allow_remote: bool) -> dict:
    path_entries = [str(Path(sys.executable).resolve().parent)]
    path_entries.extend(entry for entry in os.defpath.split(os.pathsep) if entry)
    env = {
        "PATH": os.pathsep.join(dict.fromkeys(path_entries)),
        "HOME": home,
        "TMPDIR": home,
        "TEMP": home,
        "TMP": home,
        "XDG_CONFIG_HOME": str(Path(home) / "config"),
        "XDG_CACHE_HOME": str(Path(home) / "cache"),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_PROXY": "localhost,127.0.0.1,::1",
    }
    for key in ("CYBER_AI_TENANT_ID", "CYBER_AI_LEDGER_PATH", "CYBER_AI_LEDGER_REQUIRED"):
        if key in os.environ:
            env[key] = os.environ[key]
    if allow_remote:
        registry = config.get("llm_providers", {})
        if isinstance(registry, dict):
            for provider in registry.values():
                if isinstance(provider, dict):
                    key_name = provider.get("api_key_env")
                    if isinstance(key_name, str) and key_name in os.environ:
                        env[key_name] = os.environ[key_name]
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "SSL_CERT_FILE", "SSL_CERT_DIR"):
            if key in os.environ:
                env[key] = os.environ[key]
    return env


def _run_bounded_command(
    command, *, timeout: int, max_output_bytes: int,
    agent_names=(), config=None, allow_remote=False,
):
    if type(timeout) is not int or not 1 <= timeout <= 1800:
        raise ValueError("El timeout del subproceso debe estar entre 1 y 1800 segundos.")
    if config is None:
        config = {}
    with tempfile.TemporaryDirectory(prefix="cyber-ai-metacognition-") as home:
        os.chmod(home, 0o700)
        env = _child_environment(home, config, allow_remote)
        try:
            result = run_bounded_process(
                command,
                cwd=str(PROJECT),
                env=env,
                timeout=timeout,
                max_output_bytes=max_output_bytes,
            )
        except (OSError, ProcessIsolationError, ValueError) as error:
            raise MetacognitionError(
                f"No se pudo ejecutar el subproceso metacognitivo ({type(error).__name__})."
            ) from error
    if result.get("timed_out"):
        raise MetacognitionError("El subproceso metacognitivo superó su timeout.")
    if result.get("output_truncated"):
        raise MetacognitionError("La salida del subproceso superó el límite permitido.")
    result["stdout"] = redact_text(result.get("stdout", ""))
    result["stderr"] = redact_text(result.get("stderr", ""))
    return result


def _runner_call(agent: str, prompt: str, *, knowledge: bool = True, timeout: int = 1800) -> str:
    if not isinstance(agent, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", agent):
        raise ValueError("Identificador de agente inválido.")
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > MAX_REPORT_CHARS:
        raise ValueError("El prompt del agente está vacío o supera 100.000 caracteres.")
    if not isinstance(knowledge, bool):
        raise TypeError("knowledge debe ser booleano.")
    config, _, allow_remote = _provider_context([agent])
    command = [
        sys.executable, str(PROJECT / "agent_runner.py"),
        "ask", agent, "--task-text", prompt,
    ]
    if knowledge:
        command.append("--knowledge")
    completed = _run_bounded_command(
        command, timeout=timeout, max_output_bytes=2_000_000,
        agent_names=[agent], config=config, allow_remote=allow_remote,
    )
    if completed.get("returncode") != 0:
        detail = (completed.get("stderr") or completed.get("stdout") or "")[-4000:]
        raise RuntimeError(
            f"Agente {agent} falló (código {completed.get('returncode')}): {detail}"
        )
    output = completed.get("stdout", "")
    if ANSWER_MARKER in output:
        output = output.rsplit(ANSWER_MARKER, 1)[1]
    answer = output.strip()
    if not answer:
        raise RuntimeError(f"Agente {agent} devolvió una respuesta vacía.")
    return answer[:MAX_REPORT_CHARS]


def publish_research_report(report: str, task_id: str) -> dict:
    """Indexa como conocimiento privado y provisional, nunca como dominio."""
    from knowledge_embeddings import generate_embedding
    from knowledge_library import store_chunks

    if not isinstance(report, str) or not report.strip() or len(report) > MAX_REPORT_CHARS:
        raise MetacognitionError("El informe de investigación está vacío o supera el límite.")
    tenant_id = os.environ.get("CYBER_AI_TENANT_ID", "local")
    if not re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", tenant_id):
        raise MetacognitionError("CYBER_AI_TENANT_ID no cumple el formato permitido.")
    _provider_context(["ECO"], capability="embeddings")
    safe_report = redact_text(report)
    vector = generate_embedding(safe_report, agent_name="ECO")
    embedding_model = vector.get("embedding_space") or vector.get("model")
    stored = store_chunks([{
        "title": "Investigación metacognitiva " + task_id,
        "source": "metacognition://" + task_id,
        "license": "UNSPECIFIED",
        "category": "research_provisional",
        "tags": ["metacognition", "ai-research", "provisional", "independently-reviewed"],
        "visibility": "tenant",
        "tenant_id": tenant_id,
        "content": safe_report,
        "embedding": vector["embedding"],
        "embedding_model": embedding_model,
    }])
    return {"indexed": True, "document": stored[0], "visibility": "tenant"}


def collect_web_evidence(task: str, assessment: dict, *, timeout: int = 900) -> dict:
    """Busca fuentes registradas, las revisa y solo cuenta páginas con revisión completada."""
    if type(timeout) is not int or not 5 <= timeout <= 900:
        raise ValueError("El timeout de investigación web debe estar entre 5 y 900 segundos.")
    gaps = assessment.get("gaps", [])[:4]
    if not gaps:
        return {"status": "unavailable", "verified_sources": 0, "report": "No hay brechas para investigar."}
    collected = []
    verified_sources = 0
    for gap in gaps:
        query = redact_text(
            f"{task} {gap['topic']} " + " ".join(gap.get("prerequisites", [])[:3])
        )
        search = _run_bounded_command(
            [sys.executable, str(PROJECT / "web_research.py"), query, "--max-results", "5"],
            timeout=timeout, max_output_bytes=1_000_000,
        )
        output = (search.get("stdout", "") + "\n" + search.get("stderr", ""))[-8000:]
        match = re.search(r"Datos JSON:\s*(reports/web_research/[^\s]+\.json)", output)
        if search.get("returncode") != 0 or not match:
            collected.append(
                f"BRECHA: {gap['topic']}\nESTADO: búsqueda fallida o sin informe. "
                f"DETALLE: {output[-1200:]}"
            )
            continue
        relative = Path(match.group(1))
        if relative.is_absolute() or ".." in relative.parts:
            collected.append(f"BRECHA: {gap['topic']}\nESTADO: ruta de informe no válida.")
            continue
        report_path = PROJECT / relative
        report = _read_json(report_path, {})
        if (
            not isinstance(report, dict)
            or report.get("search_status") != "ok"
            or not isinstance(report.get("results"), list)
        ):
            collected.append(
                f"BRECHA: {gap['topic']}\nESTADO: sin resultados confiables."
            )
            continue
        pages = [
            item for item in report["results"]
            if isinstance(item, dict)
            and item.get("registered_source") is True
            and item.get("fetch_status") == "pagina consultada"
            and isinstance(item.get("page_text"), str)
            and item.get("page_text")
            and isinstance(item.get("url"), str)
        ][:4]
        if not pages:
            collected.append(
                f"BRECHA: {gap['topic']}\nESTADO: no hay páginas registradas consultadas."
            )
            continue
        review_config, _, review_remote = _provider_context(["NEXO", "FILTRO", "VERITAS"])
        review = _run_bounded_command(
            [sys.executable, str(PROJECT / "review_web_report.py"), str(relative)],
            timeout=timeout, max_output_bytes=1_000_000,
            agent_names=["NEXO", "FILTRO", "VERITAS"],
            config=review_config, allow_remote=review_remote,
        )
        review_output = (review.get("stdout", "") + "\n" + review.get("stderr", ""))[-8000:]
        review_ok = review.get("returncode") == 0
        if review_ok:
            verified_sources += len(pages)
        safe_report = redact_sensitive_data({
            "query": report.get("query"),
            "retrieved_at_utc": report.get("retrieved_at_utc"),
            "results": pages,
        })
        collected.append(
            f"BRECHA: {gap['topic']}\n"
            f"ESTADO DE BÚSQUEDA: ok\n"
            f"ESTADO DE REVISIÓN: {'completada' if review_ok else 'fallida'}\n"
            f"FUENTES REGISTRADAS: {len(pages) if review_ok else 0}\n"
            f"DATOS DE FUENTES:\n{json.dumps(safe_report, ensure_ascii=False)[:12000]}\n"
            f"BORRADOR DE REVISIÓN:\n{review_output[-5000:]}"
        )
    status = "ok" if verified_sources > 0 else "unavailable"
    return {
        "status": status,
        "verified_sources": verified_sources,
        "report": redact_text("\n\n--- SIGUIENTE BRECHA ---\n\n".join(collected)[:MAX_CONTEXT_CHARS]),
    }

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
