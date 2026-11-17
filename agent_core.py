#!/usr/bin/env python3
"""Motor de herramientas con aprobación explícita y alcance visible."""

import json
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from execution_policy import AuthorizationError, authorize_target


PROJECT = Path(__file__).resolve().parent


class CyberAIEngine:
    """Traduce propuestas del agente; nunca ejecuta acciones por inferencia."""

    def __init__(self):
        print("[CYBER_AI] Motor de herramientas en modo aprobación explícita.")

    def translate_and_execute(self, agent_thought):
        """Devuelve una propuesta; no realiza conexiones ni accede a archivos."""
        thought = str(agent_thought).strip()
        lowered = thought.casefold()
        if any(word in lowered for word in ("cabeceras", "servidor", "http")):
            action = "inspect_http_headers"
        elif any(word in lowered for word in ("archivo", "configuración", "local")):
            action = "inspect_project_file"
        else:
            return {
                "status": "unsupported",
                "message": "No hay una herramienta asignada a esta propuesta.",
            }
        return {
            "status": "approval_required",
            "proposed_action": action,
            "target": None,
            "message": (
                "No se ejecutó ninguna acción. Un usuario debe proporcionar "
                "el destino y aprobar explícitamente la operación."
            ),
        }

    def action_check_headers(self, url, authorized=False, authorization_id=None):
        """Consulta cabeceras solo con un permiso local, específico y vigente."""
        parsed = urlparse(str(url))
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or parsed.username
            or parsed.password
        ):
            return {"status": "error", "error_msg": "URL HTTP/HTTPS no válida."}
        if authorized is not True or not authorization_id:
            return {"status": "authorization_required"}
        try:
            grant = authorize_target(url, "inspect_http_headers", authorization_id)
        except AuthorizationError as error:
            return {"status": "authorization_denied", "error_msg": str(error)}
        try:
            request = Request(
                url, method="HEAD",
                headers={"User-Agent": "CYBER_AI/1.0"},
            )
            class NoRedirect(HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            opener = build_opener(ProxyHandler({}), NoRedirect)
            with opener.open(request, timeout=5) as response:
                headers = dict(response.headers)
            return {
                "status": "success",
                "action": "HTTP Header Inspection",
                "server": headers.get("Server", "No especificado"),
                "header_count": len(headers),
                "target": url,
                "authorization": grant,
            }
        except (URLError, TimeoutError, OSError, ValueError) as error:
            return {"status": "error", "error_msg": str(error)}

    def action_check_local_file(self, filepath):
        """Inspecciona solo archivos dentro del directorio del proyecto."""
        candidate = (PROJECT / filepath).resolve()
        try:
            candidate.relative_to(PROJECT)
        except ValueError:
            return {"status": "error", "error_msg": "Ruta fuera del proyecto."}
        if not candidate.is_file():
            return {
                "status": "not_found",
                "action": "Local File Check",
                "path": str(candidate.relative_to(PROJECT)),
            }
        return {
            "status": "success",
            "action": "Local File Check",
            "path": str(candidate.relative_to(PROJECT)),
            "size_bytes": candidate.stat().st_size,
        }


if __name__ == "__main__":
    engine = CyberAIEngine()
    examples = [
        "Necesito indagar qué tipo de servidor web y cabeceras tiene el objetivo.",
        "Quiero verificar si el archivo de configuración local está disponible.",
        "Texto sin herramienta asignada.",
    ]
    for thought in examples:
        result = engine.translate_and_execute(thought)
        print(json.dumps(result, indent=2, ensure_ascii=False))
