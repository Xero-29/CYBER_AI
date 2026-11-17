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


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ToolAllowlistError("La allowlist contiene claves JSON duplicadas.")
        result[key] = value
    return result


def _validate_tools(tools):
    if not isinstance(tools, dict) or not tools:
        raise ToolAllowlistError("La lista de herramientas no puede estar vacía.")
    for tool_id, entry in tools.items():
        if (not isinstance(tool_id, str) or not re.fullmatch(r"[a-z0-9_-]{1,64}", tool_id)
                or not isinstance(entry, dict) or set(entry) != {"sha256"}
                or not isinstance(entry["sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])):
            raise ToolAllowlistError("Entrada de herramienta inválida en la allowlist.")


def _canonical_payload(document):
    payload = {key: value for key, value in document.items() if key != "signature"}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_tool_allowlist(tools, key):
    """Genera un manifiesto durante un proceso de enrolamiento controlado."""
    if not isinstance(key, bytes) or len(key) < 32:
        raise ToolAllowlistError("La clave HMAC debe tener al menos 32 bytes.")
    _validate_tools(tools)
    document = {"schema_version": 1, "tools": tools}
    document["signature"] = hmac.new(key, _canonical_payload(document), hashlib.sha256).hexdigest()
    return document


def load_signed_tool_allowlist(path, key):
    if not isinstance(key, bytes) or len(key) < 32:
        raise ToolAllowlistError("La clave HMAC debe tener al menos 32 bytes.")
    candidate = Path(path)
    if candidate.is_symlink():
        raise ToolAllowlistError("La allowlist no puede ser un enlace simbólico.")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = None
    try:
        descriptor = os.open(candidate, flags)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
            raise ToolAllowlistError("La allowlist debe ser un archivo regular de hasta 64 KiB.")
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if getattr(info, "st_file_attributes", 0) & reparse_flag:
            raise ToolAllowlistError("La allowlist no puede ser un punto de reanálisis de Windows.")
        chunks = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(8192, 65537 - total))
            if not chunk:
                break
            total += len(chunk)
            if total > 65536:
                raise ToolAllowlistError("La allowlist supera el límite de 64 KiB.")
            chunks.append(chunk)
        document = json.loads(b"".join(chunks).decode("utf-8"), object_pairs_hook=_unique_object)
    except ToolAllowlistError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ToolAllowlistError("No se pudo leer la allowlist firmada.") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if not isinstance(document, dict) or set(document) != {"schema_version", "tools", "signature"}:
        raise ToolAllowlistError("Esquema de allowlist inválido.")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise ToolAllowlistError("Versión de allowlist inválida.")
    _validate_tools(document["tools"])
    signature = document["signature"]
    if not isinstance(signature, str) or not re.fullmatch(r"[0-9a-f]{64}", signature):
        raise ToolAllowlistError("Firma HMAC inválida.")
    expected = hmac.new(key, _canonical_payload(document), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise ToolAllowlistError("La firma HMAC de la allowlist no coincide.")
    return document["tools"]


def verify_tool_allowed(tool_id, binary_sha256):
    if not isinstance(tool_id, str) or not re.fullmatch(r"[a-z0-9_-]{1,64}", tool_id):
        raise ToolAllowlistError("Identificador de herramienta inválido.")
    if not isinstance(binary_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", binary_sha256):
        raise ToolAllowlistError("SHA-256 de ejecutable inválido.")
    path = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_PATH")
    key_text = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY")
    required = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_REQUIRED", "").strip().lower() in {"1", "true", "yes"}
    if not path and not key_text:
        if required:
            raise ToolAllowlistError("La política exige allowlist, pero no está configurada.")
        return {"enforced": False, "status": "not_configured"}
    if not path or not key_text:
        raise ToolAllowlistError("La ruta y la clave de la allowlist deben configurarse juntas.")
    tools = load_signed_tool_allowlist(path, key_text.encode("utf-8"))
    entry = tools.get(tool_id)
    if entry is None or not hmac.compare_digest(entry["sha256"], binary_sha256):
        raise ToolAllowlistError("El ejecutable no está aprobado por la allowlist firmada.")
    return {"enforced": True, "status": "approved", "sha256": binary_sha256}


__all__ = ["ToolAllowlistError", "load_signed_tool_allowlist", "sign_tool_allowlist", "verify_tool_allowed"]
