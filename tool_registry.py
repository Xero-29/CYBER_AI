#!/usr/bin/env python3
"""Descubre herramientas pertinentes sin ejecutarlas.

La selección de una herramienta nunca concede permiso de ejecución. Los
adaptadores ejecutables deben validar su política específica por separado.
"""
import argparse
import json
import shutil

from capability_inventory import TOOL_CATALOG, build_inventory
from tool_adapters import TOOL_SPECS
from tool_execution_profiles import get_custom_tools


TASK_TERMS = {
    "sast": ("codigo", "code", "sast", "analisis estatico", "análisis estático", "python", "bug", "calidad"),
    "quality": ("lint", "calidad", "estilo", "shell", "python"),
    "dependencies": ("dependencias", "dependency", "paquetes", "cve", "vulnerabilidades de software"),
    "supply_chain": ("sbom", "supply chain", "cadena de suministro", "imagen", "artefacto"),
    "iac": ("terraform", "iac", "infraestructura como codigo", "infraestructura como código", "cloud config"),
    "secrets": ("secretos", "secrets", "tokens", "credenciales", "claves expuestas"),
    "containers": ("dockerfile", "docker", "contenedor"),
    "ci_cd": ("github actions", "workflow", "pipeline", "ci/cd", "ci cd"),
    "kubernetes": ("kubernetes", "k8s", "manifiestos"),
    "malware_analysis": ("malware", "yara", "muestra sospechosa"),
    "network_forensics": ("pcap", "captura de red", "trafico", "tráfico", "wireshark", "zeek"),
    "memory_forensics": ("memoria ram", "volcado de memoria", "memory dump", "forense de memoria"),
    "network_discovery": ("descubrimiento de red", "inventario de red", "puertos", "nmap"),
    "vulnerability_scanning": ("escaneo autorizado", "auditoria web", "auditoría web", "nuclei"),
}


def select_tools(task, *, inventory=None, limit=10):
    """Devuelve candidatos explicables; no ejecuta comandos."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("La tarea debe ser texto no vacío.")
    if not isinstance(limit, int) or not 1 <= limit <= 50:
        raise ValueError("limit debe estar entre 1 y 50.")
    inventory = inventory or build_inventory()
    availability = inventory.get("tools", {})
    normalized = task.casefold()
    ranked = []
    for item in TOOL_CATALOG:
        terms = TASK_TERMS.get(item["category"], ())
        matched = [term for term in terms if term.casefold() in normalized]
        if not matched:
            continue
        detected = availability.get(item["id"], {})
        active = item["risk"] == "active_network"
        ranked.append({
            **item,
            "available": bool(detected.get("available", False)),
            "path": detected.get("path"),
            "matched_terms": matched,
            "authorization_required": active,
            "execution_permitted": False,
            "adapter_supported": item["id"] in TOOL_SPECS,
            "adapter_status": (
                "blocked_network_policy" if item["id"] in TOOL_SPECS and TOOL_SPECS[item["id"]]["network"]
                else "local_adapter_available" if item["id"] in TOOL_SPECS
                else "separate_runner" if item["id"] == "nuclei"
                else "not_implemented"
            ),
            "status": "candidate_only",
        })
    for custom in get_custom_tools():
        terms = custom.get("keywords", [])
        matched = [term for term in terms if term.casefold() in normalized]
        if not matched:
            continue
        executable = custom["executable"]
        available = bool(shutil.which(executable) or (
            __import__("pathlib").Path(executable).is_absolute()
            and __import__("pathlib").Path(executable).is_file()
        ))
        ranked.append({
            "id": custom["id"],
            "name": custom.get("description", custom["id"]),
            "category": custom.get("category", "custom"),
            "description": custom.get("description", "Herramienta personalizada"),
            "risk": "local",
            "available": available,
            "path": executable if available else None,
            "matched_terms": matched,
            "authorization_required": True,
            "execution_permitted": False,
            "adapter_supported": True,
            "adapter_status": "custom_argv_runner",
            "status": "candidate_only",
        })
    ranked.sort(key=lambda item: (
        not item["available"],
        item["category"],
        item["id"],
    ))
    return {
        "task": task,
        "candidate_count": len(ranked[:limit]),
        "candidates": ranked[:limit],
        "execution_started": False,
        "note": "La selección es orientativa. No ejecuta herramientas ni concede autorización.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="Descripción de la tarea")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(
        select_tools(args.task, limit=args.limit),
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
