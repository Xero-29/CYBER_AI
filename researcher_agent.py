"""Contrato neutral del investigador: desacopla metodología y proveedor de IA."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ModelBackend:
    """Adaptador intercambiable: cualquier proveedor implementa generate(prompt)."""
    name: str
    model: str
    generate: Callable[[str], str]


class ResearcherAgent:
    """Investigador pequeño y reemplazable; no certifica sus propios resultados."""

    def __init__(self, backend: ModelBackend):
        if not callable(backend.generate):
            raise TypeError("El backend debe proporcionar generate(prompt).")
        self.backend = backend

    def investigate(self, task: str, gap_report: dict, *, context: str = "") -> dict:
        if not task.strip():
            raise ValueError("La tarea no puede estar vacía.")
        prompt = (
            "Investiga las brechas y prerrequisitos sin inventar fuentes ni resultados. "
            "Distingue hechos, inferencias e incertidumbres. Si no tienes acceso a fuentes, "
            "declara la limitación y no simules una búsqueda. Prioriza fuentes primarias, "
            "estándares y documentación oficial. Devuelve un informe técnico con: "
            "objetivo, brechas, fundamentos, explicación, metodología, ejemplos, límites, "
            "fuentes trazables y preguntas abiertas.\n\n"
            f"TAREA:\n{task}\n\nBRECHAS:\n{gap_report!r}\n\nCONTEXTO:\n{context}"
        )
        report = self.backend.generate(prompt)
        if not isinstance(report, str) or not report.strip():
            raise RuntimeError("El modelo investigador devolvió un informe vacío.")
        return {
            "provider": self.backend.name,
            "model": self.backend.model,
            "report": report,
            "self_verified": False,
            "status": "pending_independent_verification",
        }
