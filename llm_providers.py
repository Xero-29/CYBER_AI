"""Adaptadores desacoplados para proveedores de modelos de CYBER_AI.

Credenciales únicamente desde variables de entorno. El núcleo no depende de SDKs
propietarios; los proveedores OpenAI-compatible usan la API HTTP estándar.
"""
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def resolve_provider(config, agent):
    registry = config.get("llm_providers", {})
    name = agent.get("provider") or config.get("default_provider") or "ollama"
    item = registry.get(name)
    if not isinstance(item, dict) or not item.get("enabled", False):
        raise RuntimeError(f"Proveedor de IA no configurado o deshabilitado: {name}")
    result = dict(item)
    result["name"] = name
    return result


def _http_json(url, payload=None, headers=None, timeout=600):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})},
                      method="GET" if payload is None else "POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"Proveedor IA respondió HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"No se pudo conectar con el proveedor IA: {exc}") from exc


def request(provider, endpoint, payload=None, timeout=600):
    name = provider["name"]
    base = str(provider.get("base_url", "")).rstrip("/")
    if name == "ollama":
        return _http_json(base + "/" + endpoint, payload, timeout=timeout)
    if provider.get("protocol") != "openai":
        raise ValueError(f"Protocolo no compatible: {provider.get('protocol')}")
    key_env = provider.get("api_key_env")
    key = os.environ.get(key_env, "") if key_env else ""
    if provider.get("requires_api_key", True) and not key:
        raise RuntimeError(f"Falta configurar la variable de entorno {key_env}.")
    headers = {"Authorization": "Bearer " + key} if key else {}
    if endpoint == "api/chat":
        body = {"model": payload["model"], "messages": payload["messages"],
                "stream": False}
        options = payload.get("options", {})
        for source, target in (("temperature","temperature"),("top_p","top_p"),
                               ("num_predict","max_tokens")):
            if source in options: body[target] = options[source]
        if "format" in payload: body["response_format"] = {"type":"json_object"}
        result = _http_json(base + "/chat/completions", body, headers, timeout)
        choice = (result.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        return {"message":{"content":message.get("content") or "",
                           "thinking":message.get("reasoning_content") or ""},
                "done_reason":(choice.get("finish_reason") or "stop"),
                "prompt_eval_count":(result.get("usage") or {}).get("prompt_tokens",0),
                "eval_count":(result.get("usage") or {}).get("completion_tokens",0)}
    if endpoint == "api/embed":
        result = _http_json(base + "/embeddings",
            {"model":payload["model"],"input":payload["input"]},headers,timeout)
        vectors = [item.get("embedding") for item in result.get("data",[])]
        return {"embeddings":vectors}
    if endpoint == "api/tags":
        result = _http_json(base + "/models",None,headers,timeout)
        return {"models":[{"name":item.get("id")} for item in result.get("data",[])]}
    if endpoint == "api/ps":
        return {"models":[]}
    raise ValueError(f"Endpoint no disponible para proveedor remoto: {endpoint}")


def installed_models(provider):
    if provider["name"] == "ollama":
        return {item.get("name") or item.get("model")
                for item in request(provider,"api/tags").get("models",[])}
    # Los proveedores remotos pueden ocultar o limitar su catálogo.
    return None
