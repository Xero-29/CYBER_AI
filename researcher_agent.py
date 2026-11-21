"""Contrato neutral del investigador: desacopla metodología y proveedor de IA."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Callable

from secret_redaction import redact_text


MAX_TASK_CHARS = 20_000
MAX_CONTEXT_CHARS = 30_000
MAX_REPORT_CHARS = 100_000


@dataclass(frozen=True)
class ModelBackend:
    """Adaptador intercambiable: cualquier proveedor implementa generate(prompt)."""

    name: str
    model: str
    generate: Callable[[str], str]
    remote: bool = False

    def __post_init__(self):
        if not isinstance(self.name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", self.name):
            raise ValueError("Nombre de backend inválido.")
        if not isinstance(self.model, str) or not self.model.strip() or len(self.model) > 128:
            raise ValueError("Nombre de modelo inválido.")
        if not callable(self.generate):
            raise TypeError("El backend debe proporcionar generate(prompt).")
        if not isinstance(self.remote, bool):
            raise TypeError("remote debe ser booleano.")


class ResearcherAgent:
    """Investigador pequeño y reemplazable; nunca certifica sus propios resultados."""

    def __init__(self, backend: ModelBackend):
        if not isinstance(backend, ModelBackend):
            raise TypeError("backend debe ser una instancia de ModelBackend.")
        self.backend = backend

    def investigate(self, task: str, gap_report: dict, *, context: str = "") -> dict:
        if not isinstance(task, str) or not task.strip() or len(task) > MAX_TASK_CHARS:
            raise ValueError("La tarea debe ser texto no vacío de hasta 20.000 caracteres.")
        if not isinstance(gap_report, dict):
            raise ValueError("El informe de brechas debe ser un objeto.")
        try:
            gap_text = json.dumps(gap_report, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise ValueError("El informe de brechas debe contener solo datos JSON.") from error
        if len(gap_text) > MAX_CONTEXT_CHARS:
            raise ValueError("El informe de brechas supera 30.000 caracteres.")
        if not isinstance(context, str) or len(context) > MAX_CONTEXT_CHARS:
            raise ValueError("El contexto supera 30.000 caracteres.")
        if self.backend.remote and os.environ.get("CYBER_AI_METACOGNITION_ALLOW_REMOTE") != "1":
            raise PermissionError("El backend remoto requiere consentimiento explícito.")

        prompt = (
            "Investiga las brechas y prerrequisitos sin inventar fuentes ni resultados. "
            "Distingue hechos, inferencias e incertidumbres. Si no tienes acceso a fuentes, "
            "declara la limitación y no simules una búsqueda. Prioriza fuentes primarias, "
            "estándares y documentación oficial. Devuelve un informe técnico con: "
            "objetivo, brechas, fundamentos, explicación, metodología, ejemplos, límites, "
            "fuentes trazables y preguntas abiertas.\n\n"
            f"TAREA:\n{task}\n\nBRECHAS:\n{gap_text}\n\nCONTEXTO:\n{context}"
        )
        report = self.backend.generate(prompt)
        if not isinstance(report, str) or not report.strip() or len(report) > MAX_REPORT_CHARS:
            raise RuntimeError("El modelo investigador devolvió un informe vacío o demasiado grande.")
        return {
            "provider": self.backend.name,
            "model": self.backend.model,
            "report": redact_text(report),
            "self_verified": False,
            "status": "pending_independent_verification",
        }
