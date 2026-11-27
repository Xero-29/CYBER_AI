#!/usr/bin/env python3
"""Descubre modelos locales de Ollama sin mantener listas duplicadas."""
import json
from urllib.error import URLError
from urllib.request import Request, urlopen

def discover_ollama_models(base_url="http://127.0.0.1:11434", timeout=3.0):
    """Consulta /api/tags; no descarga, ejecuta ni modifica modelos."""
    url = base_url.rstrip("/") + "/api/tags"
    try:
        with urlopen(Request(url, headers={"Accept": "application/json"}), timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        models = payload.get("models", [])
        if not isinstance(models, list): raise ValueError("Respuesta Ollama inválida.")
        normalized = [{"name": x["name"], "model": x.get("model"), "size": x.get("size"),
            "modified_at": x.get("modified_at"), "digest": x.get("digest"), "source": "ollama_local_api"}
            for x in models if isinstance(x, dict) and isinstance(x.get("name"), str)]
        return {"status": "available", "endpoint": url, "models": normalized}
    except (URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        return {"status": "unavailable", "endpoint": url, "models": [], "error": str(exc)}

if __name__ == "__main__":
    print(json.dumps(discover_ollama_models(), indent=2, ensure_ascii=False))
