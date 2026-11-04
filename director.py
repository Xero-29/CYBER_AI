#!/usr/bin/env python3
"""DIRECTOR: selecciona y coordina especialistas configurados."""

import argparse
import subprocess
import sys
import unicodedata
from pathlib import Path

from model_memory_manager import load_config, resolve_agent

PROJECT = Path(__file__).resolve().parent


def normalize(text):
    """Normaliza mayúsculas y tildes para comparar palabras."""
    text = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in text if not unicodedata.combining(char))


def select_agent(task, config, requested=None):
    """Selecciona especialistas sin depender de nombres fijos."""

    if requested:
        name, agent = resolve_agent(requested, config)
        if not agent.get("enabled", True):
            raise ValueError(f"El especialista {name} está deshabilitado.")
        if agent.get("type") == "embeddings":
            raise ValueError(
                f"{name} es un modelo de embeddings; la búsqueda semántica "
                "todavía no está conectada al DIRECTOR."
            )
        return name, agent, []

    normalized_task = normalize(task)
    candidates = []

    for name, agent in config["agents"].items():
        # Los agentes deshabilitados no participan en la selección.
        # Los modelos de embeddings requieren un flujo diferente.
        if not agent.get("enabled", True):
            continue
        if agent.get("type") == "embeddings":
            continue

        keywords = agent.get("routing_keywords", [])
        matched = [
            keyword for keyword in keywords
            if normalize(keyword) in normalized_task
        ]

        if matched:
            # Las frases más específicas reciben mayor peso.
            score = sum(1 + len(keyword.split()) for keyword in matched)
            candidates.append((score, name, agent, matched))

    if candidates:
        best_score = max(item[0] for item in candidates)
        tied = [item for item in candidates if item[0] == best_score]

        default = config.get("coordinator", {}).get("default_agent", "NEXO")
        chosen = next((item for item in tied if item[1] == default), tied[0])
        _, name, agent, matched = chosen
        return name, agent, matched

    # Si no hay coincidencias, utiliza el especialista predeterminado.
    default = config.get("coordinator", {}).get("default_agent")
    name, agent = resolve_agent(default, config)
    if agent.get("type") == "embeddings":
        raise ValueError("El especialista predeterminado no puede ser embeddings.")
    return name, agent, []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent",
        help="Seleccionar un especialista manualmente",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar la selección sin ejecutar el modelo",
    )
    parser.add_argument("task", nargs="+", help="Tarea para CYBER_AI")
    args = parser.parse_args()

    try:
        config = load_config()
        task = " ".join(args.task)
        name, agent, matched = select_agent(task, config, args.agent)

        print(f"DIRECTOR seleccionó: {name}")
        print(f"Modelo: {agent['model']}")
        print(f"Tipo: {agent['type']}")
        print(f"Motivos de selección: {', '.join(matched) or 'selección predeterminada/manual'}")

        if args.dry_run:
            print("Simulación: no se cargó ningún modelo.")
            return 0

        command = [
            sys.executable,
            str(PROJECT / "agent_runner.py"),
            "ask",
            name,
            task,
        ]
        result = subprocess.run(command, cwd=PROJECT, check=False)
        return result.returncode

    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
