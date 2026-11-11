#!/usr/bin/env python3
"""Conector de ECO para generar embeddings individuales o por lotes."""

import fcntl

from agent_runner import (
    LOCK_FILE,
    installed_models,
    unload_other_models,
    request_json,
)
from model_memory_manager import load_config, resolve_agent
from llm_providers import resolve_provider, resolve_model, request as provider_request, installed_models as provider_models
from knowledge_library import validate_vector


def generate_embeddings(texts, agent_name="ECO"):
    """Genera varios embeddings mediante una sola petición a Ollama."""

    if isinstance(texts, str) or not isinstance(texts, (list, tuple)):
        raise TypeError("texts debe ser una lista de textos.")

    if not texts:
        raise ValueError("La lista de textos está vacía.")

    if any(not isinstance(text, str) or not text.strip() for text in texts):
        raise ValueError("Todos los textos deben ser cadenas no vacías.")

    config = load_config()
    name, agent = resolve_agent(agent_name, config)

    if agent.get("type") != "embeddings":
        raise ValueError(f"{name} no es un especialista de embeddings.")

    provider = resolve_provider(config, agent)
    model = resolve_model(provider, agent, name)
    available_models = provider_models(provider)

    if available_models is not None and model not in available_models:
        raise ValueError(f"El modelo de embeddings no está instalado: {model}")

    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOCK_FILE.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)

        try:
            if provider["protocol"] == "ollama":
                unload_other_models(model)

            result = provider_request(
                provider,
                "api/embed",
                {
                    "model": model,
                    "input": list(texts),
                    "keep_alive": 0,
                },
            )

            raw_vectors = result.get("embeddings", [])

            if len(raw_vectors) != len(texts):
                raise RuntimeError(
                    "Ollama devolvió una cantidad de embeddings distinta "
                    "de la cantidad de textos enviados."
                )

            vectors = [validate_vector(vector) for vector in raw_vectors]
            dimensions = len(vectors[0])

            if any(len(vector) != dimensions for vector in vectors):
                raise RuntimeError(
                    "Ollama devolvió embeddings con dimensiones diferentes."
                )

            return {
                "agent": name,
                "model": model,
                "embeddings": vectors,
                "dimensions": dimensions,
            }

        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def generate_embedding(text, agent_name="ECO"):
    """Mantiene la interfaz individual compatible con el código existente."""

    result = generate_embeddings([text], agent_name=agent_name)

    return {
        "agent": result["agent"],
        "model": result["model"],
        "embedding": result["embeddings"][0],
        "dimensions": result["dimensions"],
    }
