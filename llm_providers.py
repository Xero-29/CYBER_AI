"""Adaptadores desacoplados para proveedores de modelos de CYBER_AI.

Credenciales únicamente desde variables de entorno. El núcleo no depende de SDKs
propietarios; los proveedores OpenAI-compatible usan la API HTTP estándar.
"""
import ipaddress
import json
import math
import os
from functools import lru_cache
from importlib.metadata import entry_points
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener
from urllib.request import Request
from urllib.error import HTTPError, URLError


class _NoRedirect(HTTPRedirectHandler):
    """No reenvía credenciales de proveedor a destinos de redirección."""

    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


_HTTP_OPENER = build_opener(_NoRedirect)
MAX_PROVIDER_REQUEST_BYTES = 16 * 1024 * 1024
MAX_PROVIDER_RESPONSE_BYTES = 16 * 1024 * 1024


def _unique_json_object(pairs):
    """Reject duplicate keys in provider responses, including nested objects."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("La respuesta del proveedor contiene claves JSON duplicadas.")
        result[key] = value
    return result


def _reject_json_constant(value):
    raise ValueError("La respuesta del proveedor contiene una constante JSON no estándar.")


def _parse_finite_float(value):
    """Reject float overflow and underflow that would corrupt provider evidence."""
    try:
        parsed = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError("La respuesta del proveedor contiene un número fuera de rango.") from error
    if not math.isfinite(parsed):
        raise ValueError("La respuesta del proveedor contiene un número no finito.")
    mantissa = value.lower().split("e", 1)[0]
    if parsed == 0.0 and any(digit in "123456789" for digit in mantissa):
        raise ValueError("La respuesta del proveedor contiene un número subdesbordado.")
    return parsed


@lru_cache(maxsize=32)
def _load_provider_plugin(protocol):
    """Carga solo plugins instalados y declarados en cyber_ai.providers."""
    matches = [item for item in entry_points(group="cyber_ai.providers")
               if item.name == protocol]
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError(f"Hay varios plugins instalados para el protocolo {protocol}.")
    adapter = matches[0].load()
    if not callable(getattr(adapter, "request", None)):
        raise RuntimeError(
            f"El plugin {protocol} debe exponer request(provider, endpoint, payload, timeout)."
        )
    if not callable(getattr(adapter, "capabilities", None)):
        raise RuntimeError(
            f"El plugin {protocol} debe declarar capabilities(provider)."
        )
    return adapter


DEFAULT_BASE_URLS = {
    "ollama": "http://127.0.0.1:11434",
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta",
}


def _validate_base_url(base_url, provider_name):
    """Apply the same transport boundary to resolved and direct adapter calls."""
    if not isinstance(base_url, str):
        raise ValueError(f"base_url inválida para el proveedor {provider_name}.")
    if (
        not base_url or len(base_url) > 2048
        or base_url != base_url.strip()
        or any(
            character.isspace() or ord(character) < 0x20
            or 0x7F <= ord(character) <= 0x9F
            for character in base_url
        )
    ):
        raise ValueError(f"base_url inválida para el proveedor {provider_name}.")
    try:
        parsed = urlsplit(base_url)
        hostname = (parsed.hostname or "").lower().rstrip(".")
        port = parsed.port
    except ValueError as error:
        raise ValueError(f"base_url inválida para el proveedor {provider_name}.") from error
    if (
        parsed.scheme not in {"http", "https"} or not hostname
        or parsed.username is not None or parsed.password is not None
        or parsed.query or parsed.fragment
        or "?" in base_url or "#" in base_url
        or "%" in parsed.netloc or "\\\\" in parsed.netloc or "\\\\" in parsed.path
        or (port is not None and not 1 <= port <= 65535)
    ):
        raise ValueError(f"base_url inválida para el proveedor {provider_name}.")
    try:
        loopback = ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        loopback = hostname == "localhost"
    if parsed.scheme == "http" and not loopback:
        raise ValueError(
            "base_url HTTP solo se permite en loopback; usa HTTPS para proveedores remotos."
        )
    return base_url.rstrip("/")


def resolve_provider(config, agent, capability=None):
    """Resuelve un proveedor habilitado y, si se solicita, compatible con una capacidad."""
    registry = config.get("llm_providers", {})
    if not isinstance(registry, dict):
        raise ValueError("llm_providers debe ser un objeto.")
    if capability is not None and capability not in {"chat", "embeddings", "model_listing"}:
        raise ValueError("Capacidad de proveedor no reconocida.")

    capability_map = config.get("capability_providers", {})
    fallback_map = config.get("fallback_providers", {})
    if not isinstance(capability_map, dict) or not isinstance(fallback_map, dict):
        raise ValueError("capability_providers y fallback_providers deben ser objetos.")

    explicit = agent.get("provider")
    preferred = explicit or (
        capability_map.get(capability) if capability else None
    ) or config.get("default_provider") or "ollama"
    if not isinstance(preferred, str) or not preferred.strip():
        raise ValueError("Proveedor preferido inválido.")
    candidates = [preferred]
    if capability:
        fallbacks = fallback_map.get(capability, [])
        if isinstance(fallbacks, str) or not isinstance(fallbacks, (list, tuple)):
            raise ValueError(f"fallback_providers.{capability} debe ser una lista.")
        if any(not isinstance(name, str) or not name.strip() for name in fallbacks):
            raise ValueError(f"fallback_providers.{capability} contiene nombres inválidos.")
        candidates.extend(fallbacks)
    candidates = list(dict.fromkeys(candidates))
    last_reason = None

    for name in candidates:
        item = registry.get(name)
        if not isinstance(item, dict) or not item.get("enabled", False):
            last_reason = f"Proveedor no configurado o deshabilitado: {name}"
            continue
        result = dict(item)
        result["name"] = name
        protocol = result.get("protocol")
        builtin = protocol in {"ollama", "openai", "anthropic", "gemini"}
        if not builtin and _load_provider_plugin(protocol) is None:
            raise ValueError(f"Protocolo de proveedor no soportado: {protocol}")
        base_url = result.get("base_url") or DEFAULT_BASE_URLS.get(protocol, "")
        if not base_url and not builtin:
            if capability and capability not in provider_capabilities(result):
                last_reason = f"{name} no ofrece {capability}"
                continue
            return result
        result["base_url"] = _validate_base_url(base_url, name)
        if capability and capability not in provider_capabilities(result):
            last_reason = f"{name} no ofrece {capability}"
            continue
        return result

    raise RuntimeError(
        f"No hay proveedor habilitado con capacidad {capability or 'solicitada'}: "
        f"{last_reason or 'ninguna alternativa configurada'}."
    )


def resolve_model(provider, agent, agent_name=None):
    """Resuelve el modelo del especialista sin acoplarlo al proveedor.

    Precedencia: provider.models[agent_name], provider.models[agent.id],
    provider.embedding_model (solo embeddings), provider.default_model y,
    finalmente, el modelo local declarado en el agente.
    """
    models = provider.get("models", {})
    if not isinstance(models, dict):
        raise ValueError("provider.models debe ser un objeto.")

    candidates = []
    if agent_name:
        candidates.append(agent_name)
    if agent.get("id"):
        candidates.append(agent["id"])
    for key in candidates:
        value = models.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    if agent.get("type") == "embeddings":
        value = provider.get("embedding_model")
        if isinstance(value, str) and value.strip():
            return value.strip()

    value = provider.get("default_model")
    if isinstance(value, str) and value.strip():
        return value.strip()

    value = agent.get("model")
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"No hay modelo configurado para el especialista {agent_name or agent.get('id') or 'desconocido'}."
        )
    return value.strip()


def _http_json(url, payload=None, headers=None, timeout=600):
    try:
        data = None if payload is None else json.dumps(
            payload, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError, RecursionError, UnicodeError) as error:
        raise ValueError(
            "La solicitud al proveedor no se puede serializar como JSON válido."
        ) from error
    if data is not None and len(data) > MAX_PROVIDER_REQUEST_BYTES:
        raise ValueError(
            "La solicitud al proveedor IA supera el límite permitido de 16 MiB."
        )
    request = Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})},
                      method="GET" if payload is None else "POST")
    try:
        with _HTTP_OPENER.open(request, timeout=timeout) as response:
            raw = response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)
        if len(raw) > MAX_PROVIDER_RESPONSE_BYTES:
            raise RuntimeError(
                "La respuesta del proveedor IA supera el límite de 16 MiB."
            )
        try:
            parsed = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_unique_json_object,
                parse_constant=_reject_json_constant,
                parse_float=_parse_finite_float,
            )
        except (UnicodeDecodeError, ValueError, RecursionError) as error:
            raise RuntimeError(
                "El proveedor IA devolvió una respuesta que no es JSON UTF-8 válido."
            ) from error
        if not isinstance(parsed, dict):
            raise RuntimeError(
                "El proveedor IA devolvió una respuesta JSON que no es un objeto."
            )
        return parsed
    except HTTPError as exc:
        # Never echo untrusted provider bodies: they may contain credentials or
        # sensitive prompt fragments reflected by an upstream gateway.
        status = exc.code
        try:
            exc.close()
        except OSError:
            pass
        raise RuntimeError(f"Proveedor IA respondió HTTP {status}.") from None
    except URLError as exc:
        reason_type = type(exc.reason).__name__
        raise RuntimeError(
            f"No se pudo conectar con el proveedor IA ({reason_type})."
        ) from None


def _credentials(provider):
    key_env = provider.get("api_key_env")
    key = os.environ.get(key_env, "") if key_env else ""
    if provider.get("requires_api_key", True) and not key:
        if not key_env:
            raise RuntimeError("El proveedor exige API key, pero no declara api_key_env.")
        raise RuntimeError(f"Falta configurar la variable de entorno {key_env}.")
    return key


def _openai_request(provider, endpoint, payload, timeout):
    base = str(provider.get("base_url", "")).rstrip("/")
    key = _credentials(provider)
    headers = {"Authorization": "Bearer " + key} if key else {}
    if endpoint == "api/chat":
        body = {"model": payload["model"], "messages": payload["messages"], "stream": False}
        options = payload.get("options", {})
        for source, target in (("temperature", "temperature"), ("top_p", "top_p"),
                               ("num_predict", "max_tokens")):
            if source in options:
                body[target] = options[source]
        if "format" in payload:
            body["response_format"] = {"type": "json_object"}
        result = _http_json(base + "/chat/completions", body, headers, timeout)
        choice = (result.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        return {"message": {"content": message.get("content") or "",
                            "thinking": message.get("reasoning_content") or ""},
                "done_reason": choice.get("finish_reason") or "stop",
                "prompt_eval_count": (result.get("usage") or {}).get("prompt_tokens", 0),
                "eval_count": (result.get("usage") or {}).get("completion_tokens", 0)}
    if endpoint == "api/embed":
        result = _http_json(base + "/embeddings",
            {"model": payload["model"], "input": payload["input"]}, headers, timeout)
        data = sorted(result.get("data", []), key=lambda item: item.get("index", 0))
        return {"embeddings": [item.get("embedding") for item in data]}
    if endpoint == "api/tags":
        result = _http_json(base + "/models", None, headers, timeout)
        return {"models": [{"name": item.get("id")} for item in result.get("data", [])]}
    if endpoint == "api/ps":
        return {"models": []}
    raise ValueError(f"Endpoint no disponible para proveedor remoto: {endpoint}")


def _anthropic_request(provider, endpoint, payload, timeout):
    if endpoint != "api/chat":
        if endpoint == "api/ps":
            return {"models": []}
        raise ValueError("Anthropic no ofrece embeddings nativos en este adaptador.")
    base = str(provider.get("base_url", "https://api.anthropic.com/v1")).rstrip("/")
    key = _credentials(provider)
    messages = payload.get("messages", [])
    system = "\n".join(m.get("content", "") for m in messages if m.get("role") == "system")
    body_messages = [{"role": m.get("role"), "content": m.get("content", "")}
                     for m in messages if m.get("role") in {"user", "assistant"}]
    options = payload.get("options", {})
    body = {"model": payload["model"], "messages": body_messages,
            "max_tokens": int(options.get("num_predict", 1024))}
    if system:
        body["system"] = system
    for key_name in ("temperature", "top_p"):
        if key_name in options:
            body[key_name] = options[key_name]
    result = _http_json(base + "/messages", body,
        {"x-api-key": key, "anthropic-version": provider.get("api_version", "2023-06-01")}, timeout)
    content = "".join(block.get("text", "") for block in result.get("content", [])
                      if block.get("type") == "text")
    usage = result.get("usage", {})
    return {"message": {"content": content, "thinking": ""},
            "done_reason": result.get("stop_reason") or "stop",
            "prompt_eval_count": usage.get("input_tokens", 0),
            "eval_count": usage.get("output_tokens", 0)}


def _gemini_request(provider, endpoint, payload, timeout):
    base = str(provider.get("base_url", "https://generativelanguage.googleapis.com/v1beta")).rstrip("/")
    key = _credentials(provider)
    headers = {"x-goog-api-key": key}
    model = payload.get("model", "")
    if endpoint == "api/chat":
        messages = payload.get("messages", [])
        system_parts = [{"text": m.get("content", "")} for m in messages if m.get("role") == "system"]
        contents = [{"role": "model" if m.get("role") == "assistant" else "user",
                     "parts": [{"text": m.get("content", "")}]}
                    for m in messages if m.get("role") in {"user", "assistant"}]
        body = {"contents": contents}
        if system_parts:
            body["systemInstruction"] = {"parts": system_parts}
        options = payload.get("options", {})
        generation = {}
        if "temperature" in options: generation["temperature"] = options["temperature"]
        if "top_p" in options: generation["topP"] = options["top_p"]
        if "num_predict" in options: generation["maxOutputTokens"] = options["num_predict"]
        if generation: body["generationConfig"] = generation
        result = _http_json(f"{base}/models/{model}:generateContent", body, headers, timeout)
        candidates = result.get("candidates", [])
        parts = (candidates[0].get("content", {}).get("parts", []) if candidates else [])
        content = "".join(part.get("text", "") for part in parts)
        usage = result.get("usageMetadata", {})
        return {"message": {"content": content, "thinking": ""},
                "done_reason": (candidates[0].get("finishReason", "STOP") if candidates else "STOP"),
                "prompt_eval_count": usage.get("promptTokenCount", 0),
                "eval_count": usage.get("candidatesTokenCount", 0)}
    if endpoint == "api/embed":
        vectors = []
        for value in payload.get("input", []):
            result = _http_json(f"{base}/models/{model}:embedContent",
                {"content": {"parts": [{"text": value}]}}, headers, timeout)
            vectors.append(result.get("embedding", {}).get("values"))
        return {"embeddings": vectors}
    if endpoint == "api/ps":
        return {"models": []}
    raise ValueError(f"Endpoint no disponible para Gemini: {endpoint}")


def _finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, ValueError):
        return False


def _validate_plugin_response(endpoint, result, protocol):
    """Valida el contrato interno antes de aceptar datos de un proveedor externo."""
    if not isinstance(result, dict):
        raise RuntimeError(f"El plugin {protocol} devolvió una respuesta no estructurada.")
    if endpoint == "api/chat":
        message = result.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise RuntimeError(f"El plugin {protocol} no cumple el contrato de chat.")
    elif endpoint == "api/embed":
        vectors = result.get("embeddings")
        if not isinstance(vectors, list) or not vectors:
            raise RuntimeError(f"El plugin {protocol} no cumple el contrato de embeddings.")
        dimensions = set()
        for vector in vectors:
            if (
                not isinstance(vector, list) or not vector
                or any(not _finite_number(value) for value in vector)
            ):
                raise RuntimeError(f"El plugin {protocol} devolvió un vector inválido.")
            dimensions.add(len(vector))
        if len(dimensions) != 1:
            raise RuntimeError(f"El plugin {protocol} devolvió dimensiones inconsistentes.")
    elif endpoint == "api/ps":
        if not isinstance(result.get("models"), list):
            raise RuntimeError(f"El plugin {protocol} no cumple el contrato de catálogo.")
    else:
        raise ValueError(f"Endpoint no admitido para plugins: {endpoint}")
    return result


def request(provider, endpoint, payload=None, timeout=600):
    """Normaliza llamadas y valida respuestas de todos los proveedores."""
    try:
        valid_timeout = (
            not isinstance(timeout, bool)
            and isinstance(timeout, (int, float))
            and math.isfinite(timeout)
            and 0 < timeout <= 600
        )
    except OverflowError:
        valid_timeout = False
    if not valid_timeout:
        raise ValueError("timeout debe ser un número finito mayor que 0 y máximo 600 segundos.")
    if not isinstance(provider, dict):
        raise ValueError("La configuración del proveedor debe ser un objeto.")
    provider = dict(provider)
    if "enabled" in provider and provider["enabled"] is not True:
        raise ValueError("El proveedor está deshabilitado o su estado no es booleano.")
    protocol = provider.get("protocol")
    if protocol in DEFAULT_BASE_URLS:
        base_url = provider.get("base_url") or DEFAULT_BASE_URLS[protocol]
        provider["base_url"] = _validate_base_url(
            base_url, provider.get("name") or protocol
        )
    required = {"api/chat": "chat", "api/embed": "embeddings", "api/ps": "model_listing"}.get(endpoint)
    if required and required not in provider_capabilities(provider):
        raise ValueError(f"El proveedor {provider.get('name', protocol)} no ofrece {required}.")
    request_payload = payload or {}
    if protocol == "ollama":
        base = str(provider.get("base_url", "")).rstrip("/")
        if not base:
            raise ValueError("base_url es obligatorio para Ollama.")
        result = _http_json(base + "/" + endpoint, request_payload, timeout=timeout)
    elif protocol == "openai":
        result = _openai_request(provider, endpoint, request_payload, timeout)
    elif protocol == "anthropic":
        result = _anthropic_request(provider, endpoint, request_payload, timeout)
    elif protocol == "gemini":
        result = _gemini_request(provider, endpoint, request_payload, timeout)
    else:
        adapter = _load_provider_plugin(protocol)
        if adapter is None:
            raise ValueError(f"Protocolo no compatible: {protocol}")
        result = adapter.request(provider, endpoint, request_payload, timeout)
    result = _validate_plugin_response(endpoint, result, protocol)
    if endpoint == "api/embed":
        expected = request_payload.get("input")
        if isinstance(expected, list) and len(result["embeddings"]) != len(expected):
            raise RuntimeError(f"El proveedor {protocol} devolvió un número de embeddings distinto al solicitado.")
    for field in ("prompt_eval_count", "eval_count"):
        value = result.get(field)
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0
        ):
            raise RuntimeError(f"El proveedor {protocol} devolvió un contador inválido: {field}.")
    return result


def provider_capabilities(provider):
    """Devuelve capacidades declaradas por el adaptador del proveedor."""
    protocol = provider.get("protocol")
    builtins = {
        "ollama": {"chat", "embeddings", "model_listing"},
        "openai": {"chat", "embeddings"},
        "anthropic": {"chat"},
        "gemini": {"chat", "embeddings"},
    }
    if protocol in builtins:
        return sorted(builtins[protocol])
    adapter = _load_provider_plugin(protocol)
    if adapter is None:
        return []
    if not callable(getattr(adapter, "capabilities", None)):
        raise RuntimeError(f"El plugin {protocol} debe declarar capabilities(provider).")
    values = adapter.capabilities(provider)
    allowed = {"chat", "embeddings", "model_listing"}
    if (
        not isinstance(values, (list, tuple, set))
        or any(not isinstance(value, str) or value not in allowed for value in values)
    ):
        raise RuntimeError(f"El plugin {protocol} devolvió capacidades inválidas.")
    capabilities = set(values)
    if "model_listing" in capabilities and not callable(getattr(adapter, "installed_models", None)):
        raise RuntimeError(f"El plugin {protocol} declara model_listing sin installed_models(provider).")
    return sorted(capabilities)


def installed_models(provider):
    protocol = provider.get("protocol")
    if protocol == "ollama":
        return {item.get("name") or item.get("model")
                for item in request(provider,"api/tags").get("models",[])}
    if protocol in {"openai", "anthropic", "gemini"}:
        return None
    adapter = _load_provider_plugin(protocol)
    if adapter is not None and callable(getattr(adapter, "installed_models", None)):
        return adapter.installed_models(provider)
    return None
