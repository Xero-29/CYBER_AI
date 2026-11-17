"""Perfiles declarativos y registro de herramientas personalizadas.

La configuración nunca concede confirmación ni omite la allowlist HMAC.
"""
import json
import os
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "tool_execution_profiles.json"


class ProfileConfigError(ValueError):
    pass


def load_execution_config(path=None):
    candidate = Path(path or os.environ.get("CYBER_AI_TOOL_CONFIG", DEFAULT_CONFIG))
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    if candidate.is_symlink():
        raise ProfileConfigError("El archivo de perfiles no puede ser un enlace simbólico.")
    try:
        if not candidate.exists():
            return {"schema_version": 1, "default_profile": "standard",
                    "profiles": {"standard": {}}, "custom_tools": []}
        if candidate.stat().st_size > 262144:
            raise ProfileConfigError("La configuración supera 256 KiB.")
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProfileConfigError("No se pudo leer la configuración de ejecución.") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ProfileConfigError("Versión o estructura de configuración inválida.")
    profiles = data.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ProfileConfigError("Debe existir al menos un perfil.")
    for name, profile in profiles.items():
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9_-]{1,48}", name):
            raise ProfileConfigError("Nombre de perfil inválido.")
        if not isinstance(profile, dict):
            raise ProfileConfigError("Cada perfil debe ser un objeto.")
        if set(profile) - {"max_tools", "allow_external_targets", "timeout_seconds",
                           "enabled_tools", "enable_custom_tools"}:
            raise ProfileConfigError("El perfil contiene propiedades desconocidas.")
        maximum = profile.get("max_tools")
        if maximum is not None and (type(maximum) is not int or not 1 <= maximum <= 100):
            raise ProfileConfigError("max_tools debe ser null o un entero entre 1 y 100.")
        timeout = profile.get("timeout_seconds", 180)
        if type(timeout) is not int or not 1 <= timeout <= 600:
            raise ProfileConfigError("timeout_seconds debe estar entre 1 y 600.")
        for flag in ("allow_external_targets", "enable_custom_tools"):
            if flag in profile and type(profile[flag]) is not bool:
                raise ProfileConfigError(flag + " debe ser booleano.")
        enabled = profile.get("enabled_tools")
        if enabled is not None and (not isinstance(enabled, list) or
                                    any(not isinstance(x, str) for x in enabled)):
            raise ProfileConfigError("enabled_tools debe ser una lista de identificadores.")
    default = data.get("default_profile", "standard")
    selected = os.environ.get("CYBER_AI_TOOL_PROFILE", default)
    if selected not in profiles:
        raise ProfileConfigError("Perfil desconocido: " + str(selected))
    tools = data.get("custom_tools", [])
    if not isinstance(tools, list) or len(tools) > 100:
        raise ProfileConfigError("custom_tools debe ser una lista de hasta 100 entradas.")
    seen = set()
    for tool in tools:
        if not isinstance(tool, dict):
            raise ProfileConfigError("Cada herramienta personalizada debe ser un objeto.")
        required = {"id", "description", "category", "keywords", "executable", "argv"}
        if not required.issubset(tool) or set(tool) - (required | {"timeout_seconds", "enabled"}):
            raise ProfileConfigError("Definición de herramienta personalizada incompleta o desconocida.")
        tool_id = tool["id"]
        if not isinstance(tool_id, str) or not re.fullmatch(r"[a-z0-9_-]{1,64}", tool_id):
            raise ProfileConfigError("ID de herramienta personalizada inválido.")
        if tool_id in seen:
            raise ProfileConfigError("ID de herramienta personalizada duplicado.")
        seen.add(tool_id)
        if not isinstance(tool["executable"], str) or not tool["executable"].strip():
            raise ProfileConfigError("executable debe ser una ruta o nombre ejecutable.")
        argv = tool["argv"]
        if (not isinstance(argv, list) or not argv or
                any(not isinstance(arg, str) or len(arg) > 2048 for arg in argv) or
                not any("{target}" in arg for arg in argv)):
            raise ProfileConfigError("argv debe ser una lista e incluir {target}.")
        if not isinstance(tool["keywords"], list) or any(not isinstance(x, str) for x in tool["keywords"]):
            raise ProfileConfigError("keywords debe ser una lista de texto.")
        timeout = tool.get("timeout_seconds", 180)
        if type(timeout) is not int or not 1 <= timeout <= 600:
            raise ProfileConfigError("timeout_seconds de herramienta debe estar entre 1 y 600.")
        if "enabled" in tool and type(tool["enabled"]) is not bool:
            raise ProfileConfigError("enabled debe ser booleano.")
    return data


def load_active_profile(path=None):
    config = load_execution_config(path)
    name = os.environ.get("CYBER_AI_TOOL_PROFILE", config.get("default_profile", "standard"))
    return config, name, config["profiles"][name]


def get_custom_tools(path=None, *, enabled_only=True):
    config, _, profile = load_active_profile(path)
    if not profile.get("enable_custom_tools", False):
        return []
    return [item for item in config.get("custom_tools", [])
            if (item.get("enabled", True) or not enabled_only)]
