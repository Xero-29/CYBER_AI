#!/usr/bin/env python3
"""Ciclo metacognitivo: evaluar conocimiento, investigar brechas y verificar antes de continuar.

El motor no certifica dominio por autodeclaración. Solo registra conocimiento validado
cuando un verificador separado aprueba la evidencia; el resultado queda trazable.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

PROJECT = Path(__file__).resolve().parent
STATE_DIR = PROJECT / "data" / "metacognition"
STATE_FILE = STATE_DIR / "competency_map.json"
RESEARCH_LOG = STATE_DIR / "research_log.jsonl"
MAX_RESEARCH_ROUNDS = 2
ANSWER_MARKER = "=== RESPUESTA ==="


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def load_competency_map(path: Path = STATE_FILE) -> dict:
    data = _read_json(path, {"schema_version": 1, "competencies": {}, "updated_at": None})
    if not isinstance(data, dict) or not isinstance(data.get("competencies"), dict):
        return {"schema_version": 1, "competencies": {}, "updated_at": None}
    return data


def save_competency_map(data: dict, path: Path = STATE_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now()
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def append_event(event: dict, path: Path = RESEARCH_LOG) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")


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


def run_cycle(
    task: str,
    *,
    principal: str,
    researcher: str,
    verifier: str,
    model_call: Callable[[str, str], str] = _runner_call,
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
    for round_number in range(1, max_rounds + 1):
        if not assessment["gaps"]:
            break
        research = model_call(
            researcher, build_research_request(task, assessment, knowledge_context)
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
        # Actualizar solo como "known", nunca "mastered": dominar requiere una
        # evaluación práctica separada del informe de investigación.
        for gap in assessment["gaps"]:
            key = gap["topic"].casefold()
            state["competencies"][key] = {
                "topic": gap["topic"], "status": "known",
                "source_task_id": task_id, "verification_score": score,
                "verified_at": _now(), "prerequisites": gap["prerequisites"],
                "evidence_log": str(log_path),
            }
        save_competency_map(state, state_path)
        assessment = validate_assessment(extract_json_object(
            model_call(principal, build_assessment_prompt(task, knowledge_context, state))
        ))
        if assessment["knowledge_sufficient"]:
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
        result = run_cycle(
            args.task_text, principal=args.principal, researcher=args.researcher,
            verifier=args.verifier, knowledge_context="",
            max_rounds=args.max_rounds,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["status"] in {"verification_failed", "insufficient_after_research"}:
            return 2
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"Error en ciclo metacognitivo: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
