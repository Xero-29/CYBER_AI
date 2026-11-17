"""Validación opcional y fail-closed de una allowlist HMAC de ejecutables."""
import hashlib
import hmac
import json
import os
import re
import stat
from pathlib import Path


class ToolAllowlistError(ValueError):
    """La política firmada de herramientas no es válida o no autoriza el binario."""


def _canonical_payload(document):
    payload = {key: value for key, value in document.items() if key != "signature"}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_tool_allowlist(tools, key):
    """Helper para generar manifiestos durante enrolamiento controlado."""
    if not isinstance(key, bytes) or len(key) < 32:
        raise ToolAllowlistError("La clave HMAC debe tener al menos 32 bytes.")
    if not isinstance(tools, dict) or not tools:
        raise ToolAllowlistError("La lista de herramientas no puede estar vacía.")
    document = {"schema_version": 1, "tools": tools}
    document["signature"] = hmac.new(key, _canonical_payload(document), hashlib.sha256).hexdigest()
    return document


def load_signed_tool_allowlist(path, key):
    if not isinstance(key, bytes) or len(key) < 32:
        raise ToolAllowlistError("La clave HMAC debe tener al menos 32 bytes.")
    candidate = Path(path)
    if candidate.is_symlink():
        raise ToolAllowlistError("La allowlist no puede ser un enlace simbólico.")
    try:
        info = candidate.stat(follow_symlinks=False)
        if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
            raise ToolAllowlistError("La allowlist debe ser un archivo regular de hasta 64 KiB.")
        document = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ToolAllowlistError("No se pudo leer la allowlist firmada.") from exc
    if not isinstance(document, dict) or set(document) != {"schema_version", "tools", "signature"}:
        raise ToolAllowlistError("Esquema de allowlist inválido.")
    if document["schema_version"] != 1 or not isinstance(document["tools"], dict):
        raise ToolAllowlistError("Versión o catálogo de allowlist inválido.")
    signature = document["signature"]
    if not isinstance(signature, str) or not re.fullmatch(r"[0-9a-f]{64}", signature):
        raise ToolAllowlistError("Firma HMAC inválida.")
    expected = hmac.new(key, _canonical_payload(document), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise ToolAllowlistError("La firma HMAC de la allowlist no coincide.")
    for tool_id, entry in document["tools"].items():
        if (not isinstance(tool_id, str) or not re.fullmatch(r"[a-z0-9_-]{1,64}", tool_id)
                or not isinstance(entry, dict) or set(entry) != {"sha256"}
                or not isinstance(entry["sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])):
            raise ToolAllowlistError("Entrada de herramienta inválida en la allowlist.")
    return document["tools"]


def verify_tool_allowed(tool_id, binary_sha256):
    path = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_PATH")
    key_text = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY")
    required = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_REQUIRED", "").strip().lower() in {"1", "true", "yes"}
    if not path and not key_text:
        if required:
            raise ToolAllowlistError("La política exige allowlist, pero no está configurada.")
        return {"enforced": False, "status": "not_configured"}
    if not path or not key_text:
        raise ToolAllowlistError("La ruta y la clave de la allowlist deben configurarse juntas.")
    key = key_text.encode("utf-8")
    tools = load_signed_tool_allowlist(path, key)
    entry = tools.get(tool_id)
    if entry is None or not hmac.compare_digest(entry["sha256"], binary_sha256):
        raise ToolAllowlistError("El ejecutable no está aprobado por la allowlist firmada.")
    return {"enforced": True, "status": "approved", "sha256": binary_sha256}


__all__ = ["ToolAllowlistError", "load_signed_tool_allowlist", "sign_tool_allowlist", "verify_tool_allowed"]
