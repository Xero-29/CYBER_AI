#!/usr/bin/env python3
"""Administra modelos y especialistas mediante una configuración extensible."""

import argparse
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

PROJECT = Path(__file__).resolve().parent
CONFIG_FILE = PROJECT / "config" / "model_roles.json"
MODEL_ROOT = Path("/usr/share/ollama/.ollama/models")
MANIFEST_ROOT = MODEL_ROOT / "manifests"
BLOB_ROOT = MODEL_ROOT / "blobs"
HISTORY = PROJECT / "data" / "model_usage.jsonl"
OLLAMA_API = "http://127.0.0.1:11434"
CHUNK_SIZE = 8 * 1024 * 1024


def load_config():
    """Lee y valida el registro sin depender de nombres específicos."""
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    required = config.get("schema", {}).get(
        "required_fields",
        ["model", "type", "description", "capabilities", "instructions"],
    )
    agents = config.get("agents")

    if not isinstance(agents, dict) or not agents:
        raise ValueError("La configuración no contiene agentes.")

    ids = set()
    for name, agent in agents.items():
        if not isinstance(agent, dict):
            raise ValueError(f"Configuración inválida para {name}.")
        missing = [field for field in required if field not in agent]
        if missing:
            raise ValueError(f"{name}: faltan campos {missing}.")
        agent_id = agent.get("id", name.lower())
        if agent_id in ids:
            raise ValueError(f"Identificador duplicado: {agent_id}.")
        ids.add(agent_id)

    return config


def api_get(endpoint):
    """Consulta la API local de Ollama, sin acceder a Internet."""
    with urlopen(f"{OLLAMA_API}/{endpoint}", timeout=5) as response:
        return json.load(response)


def available_ram():
    """Obtiene la RAM disponible indicada por Linux."""
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("No se pudo consultar la RAM disponible.")


def model_name(item):
    return item.get("name") or item.get("model") or ""


def read_history():
    """Lee también los registros antiguos que no tenían nombre de agente."""
    if not HISTORY.is_file():
        return []
    events = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                events.append(item)
        except json.JSONDecodeError:
            continue
    return events


def agent_for_model(model, config):
    """Relaciona un modelo con el especialista declarado en la configuración."""
    matches = [
        name for name, info in config["agents"].items()
        if info.get("model") == model and info.get("enabled", True)
    ]
    return matches[0] if len(matches) == 1 else None


def resolve_agent(target, config):
    """Acepta nombre, identificador o nombre de modelo."""
    agents = config["agents"]
    key = target.casefold()

    # Primero priorizamos el nombre y el identificador.
    for name, info in agents.items():
        if (
            name.casefold() == key
            or str(info.get("id", name)).casefold() == key
        ):
            return name, info

    matches = [
        (name, info) for name, info in agents.items()
        if info.get("model") == target and info.get("enabled", True)
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(
            "Varios agentes utilizan ese modelo; indica el nombre del agente."
        )
    raise ValueError(f"No existe un agente habilitado llamado {target!r}.")


def status():
    """Muestra modelos instalados, activos y estado de cada agente."""
    config = load_config()
    installed = {
        model_name(item) for item in api_get("api/tags").get("models", [])
    }
    running = {
        model_name(item) for item in api_get("api/ps").get("models", [])
    }

    print(f"RAM disponible: {available_ram() / 1024**3:.2f} GiB")
    policy = config.get("resource_policy", {})
    print(
        "Límite configurado de modelos conversacionales: "
        f"{policy.get('max_chat_models_loaded', 1)}"
    )
    print("\n=== ESPECIALISTAS ===")

    for name, info in config["agents"].items():
        model = info["model"]
        if not info.get("enabled", True):
            state = "DESHABILITADO"
        elif model not in installed:
            state = "FALTA EL MODELO"
        elif model in running:
            state = "CALIENTE: cargado"
        else:
            state = "FRÍO: instalado, no cargado"

        print(f"{name:14} | {model:26} | {state}")

    print(f"\nModelos cargados: {len(running)}")
    print(f"Registros de uso: {len(read_history())}")


def record(target, task):
    """Registra el agente y conserva el historial anterior."""
    config = load_config()
    agent, info = resolve_agent(target, config)
    model = info["model"]

    installed = {
        model_name(item) for item in api_get("api/tags").get("models", [])
    }
    if model not in installed:
        raise ValueError(f"El modelo {model!r} no está instalado.")

    events = read_history()
    previous = events[-1] if events else {}
    previous_model = previous.get("model")
    previous_agent = previous.get("agent") or agent_for_model(
        previous_model, config
    )

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "previous_agent": previous_agent,
        "previous_model": previous_model,
        "agent": agent,
        "agent_id": info.get("id", agent.lower()),
        "model": model,
        "task": task,
    }

    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"Agente registrado: {agent}")
    print(f"Modelo: {model}")
    print(f"Tarea: {task}")
    print(f"Agente anterior: {previous_agent or 'ninguno'}")


def recommend(target):
    """Resume las transiciones registradas, sin inventar predicciones."""
    config = load_config()
    current, _ = resolve_agent(target, config)
    counts = Counter()

    for event in read_history():
        previous_agent = event.get("previous_agent") or agent_for_model(
            event.get("previous_model"), config
        )
        next_agent = event.get("agent") or agent_for_model(
            event.get("model"), config
        )
        if (
            previous_agent == current
            and next_agent
            and next_agent != current
            and config["agents"].get(next_agent, {}).get("enabled", True)
        ):
            counts[next_agent] += 1

    print(f"Transiciones registradas después de {current}:")
    if not counts:
        print("Todavía no hay suficientes datos.")
        return

    for name, count in counts.most_common():
        print(f"  {name}: {count} veces")


def find_manifest(model):
    """Encuentra el manifiesto local del modelo."""
    repository, separator, tag = model.rpartition(":")
    if not separator:
        repository, tag = model, "latest"

    parts = repository.split("/")
    if len(parts) == 1:
        parts = ["library", *parts]

    for path in MANIFEST_ROOT.rglob(tag):
        if not path.is_file() or path.name != tag:
            continue
        parents = path.relative_to(MANIFEST_ROOT).parts[:-1]
        if parents[-len(parts):] == tuple(parts):
            return path

    raise FileNotFoundError(f"No se encontró el manifiesto de {model}.")


def warm(target):
    """Solicita a Linux la lectura anticipada de los archivos de un modelo."""
    config = load_config()
    agent, info = resolve_agent(target, config)
    model = info["model"]

    running = {
        model_name(item) for item in api_get("api/ps").get("models", [])
    }
    if model in running:
        print(f"{agent} ya está cargado; no necesita esta preparación.")
        return

    manifest = json.loads(find_manifest(model).read_text(encoding="utf-8"))
    allowed_types = {
        "application/vnd.ollama.image.model",
        "application/vnd.ollama.image.projector",
        "application/vnd.ollama.image.adapter",
    }
    files = []

    for layer in manifest.get("layers", []):
        if layer.get("mediaType") not in allowed_types:
            continue
        digest = layer.get("digest", "").removeprefix("sha256:")
        blob = BLOB_ROOT / f"sha256-{digest}"
        if not blob.is_file():
            raise FileNotFoundError(f"Falta un componente: {blob}")
        files.append(blob)

    if not files:
        raise ValueError("No se encontraron archivos de modelo que preparar.")

    total = sum(path.stat().st_size for path in files)
    reserve = int(
        config.get("resource_policy", {}).get("reserve_ram_gib", 4)
    ) * 1024**3
    available = available_ram()

    print(f"Agente: {agent}")
    print(f"Archivos: {total / 1024**3:.2f} GiB")
    print(f"RAM disponible: {available / 1024**3:.2f} GiB")

    if available < total + reserve:
        print("Precarga cancelada para proteger la RAM disponible.")
        return

    start = time.monotonic()
    for path in files:
        with path.open("rb") as file:
            while file.read(CHUNK_SIZE):
                pass

    print(f"Lectura terminada en {time.monotonic() - start:.1f} segundos.")
    print("El modelo sigue frío; Linux decide cuánto conserva en caché.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("status")

    entry = commands.add_parser("record")
    entry.add_argument("agent")
    entry.add_argument("task", nargs="+")

    prediction = commands.add_parser("recommend")
    prediction.add_argument("agent")

    preload = commands.add_parser("warm")
    preload.add_argument("agent")

    args = parser.parse_args()

    try:
        if args.command == "status":
            status()
        elif args.command == "record":
            record(args.agent, " ".join(args.task))
        elif args.command == "recommend":
            recommend(args.agent)
        elif args.command == "warm":
            warm(args.agent)
    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
