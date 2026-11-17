#!/usr/bin/env python3
"""Selecciona plantillas según la intención de la auditoría."""

import json
import re
import sys
from pathlib import Path

from capability_inventory import build_inventory

INVENTORY = Path("reports/capability_inventory.json")
TEMPLATE_ROOT = Path.home() / "nuclei-templates"


def _load_templates():
    """Carga el inventario existente o descubre metadatos en memoria."""
    if INVENTORY.is_symlink():
        raise ValueError("El inventario de capacidades no puede ser un symlink.")

    if INVENTORY.is_file():
        data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    else:
        # A clean clone must be usable without a preparatory inventory command.
        # Discovery is local and declarative: it never executes tools or templates.
        data = build_inventory()

    if not isinstance(data, dict):
        raise ValueError("El inventario de capacidades debe ser un objeto JSON.")
    nuclei = data.get("nuclei_templates")
    if not isinstance(nuclei, dict):
        raise ValueError("El inventario no contiene metadatos de plantillas válidos.")
    templates = nuclei.get("items", [])
    if not isinstance(templates, list):
        raise ValueError("La lista de plantillas del inventario no es válida.")
    return templates


def select_capabilities(task, limit=25):
    """Puntúa las plantillas según la tarea y su aplicabilidad general."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("La tarea debe ser texto no vacío.")
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("limit debe ser un entero entre 1 y 100.")

    templates = _load_templates()
    task = task.casefold()
    template_root = TEMPLATE_ROOT.resolve()

    # Detectar el objetivo solicitado.
    general_audit = any(
        word in task
        for word in ("auditoria", "auditoría", "seguridad", "general")
    )
    vulnerability_task = any(
        word in task for word in ("vulnerabilidad", "cve", "exploit")
    )
    config_task = any(
        word in task for word in ("configuracion", "configuración", "misconfig")
    )

    # Solo estas palabras específicas aportan coincidencias textuales.
    groups = {
        "api": ("api", "swagger", "graphql"),
        "red": ("network", "dns", "tcp"),
        "tecnologia": ("technolog", "fingerprint", "detect"),
        "cloud": ("cloud", "aws", "azure", "gcp"),
        "vulnerabilidad": ("cve", "vulnerab", "exposure"),
        "configuracion": ("misconfig", "configuration"),
    }

    keywords = set()
    for key, words in groups.items():
        if key in task:
            keywords.update(words)

    ranked = []

    for item in templates:
        if not isinstance(item, dict):
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            continue
        path = Path(raw_path)
        if path.is_symlink() or not path.is_file():
            continue
        try:
            path = path.resolve(strict=True)
            relative = path.relative_to(template_root)
        except (OSError, ValueError):
            # Never use stale inventory entries to read outside the template root.
            continue

        path_text = str(path).casefold()
        raw_name = item.get("name")
        name = raw_name.casefold() if isinstance(raw_name, str) else path.stem.casefold()
        parts = relative.parts
        category = parts[1] if len(parts) > 1 and parts[0] == "http" else ""

        score = 0

        # Auditoría general: favorecer detecciones comunes y configuraciones.
        if general_audit and category == "technologies":
            score += 10
        if general_audit and category == "misconfiguration":
            score += 25

        # Evitar que una lista de productos especializados domine la selección.
        generic_names = (
            "security-headers", "http-missing-security-headers",
            "robots.txt", "robots-txt", "cors", "cookie",
            "http-methods", "options-method",
        )
        if general_audit and any(term in path_text or term in name
                                 for term in generic_names):
            score += 35

        # Dar prioridad a plantillas sencillas y de aplicación amplia.
        if category in ("technologies", "misconfiguration"):
            if len(parts) <= 3:
                score += 12
            else:
                score -= (len(parts) - 3) * 4

        # Leer etiquetas para distinguir detección de otras comprobaciones.
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            header = "\n".join(content.splitlines()[:100]).casefold()
        except OSError:
            header = ""

        tags_match = re.search(r"(?m)^\s*tags\s*:\s*(.+)$", header)
        tags = tags_match.group(1) if tags_match else ""

        if "discovery" in tags or "detect" in tags:
            score += 8
        if "tech" in tags:
            score += 8

        # Evitar pruebas especializadas en una auditoría general.
        if general_audit and not vulnerability_task:
            if any(word in path_text or word in name for word in (
                "exposure", "default-login", "takeover", "/cves/",
                "/vulnerabilities/",
            )):
                score -= 35

        # Ajustes para solicitudes concretas.
        if vulnerability_task and any(
            word in path_text or word in name
            for word in ("cve", "vulnerab", "exposure")
        ):
            score += 35

        if config_task and category == "misconfiguration":
            score += 35

        # Coincidencias de términos específicos, sin premiar "http" o "ssl"
        # por aparecer en casi todas las plantillas web.
        for word in keywords:
            if word in path_text:
                score += 2
            if word in name:
                score += 3

        if score > 0:
            ranked.append((score, item))

    ranked.sort(key=lambda pair: (-pair[0], pair[1].get("path", "")))

    return [
        {"score": score, **item}
        for score, item in ranked[:limit]
    ]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python3 capability_selector.py "auditoria web"')
        raise SystemExit(2)

    task = " ".join(sys.argv[1:])
    results = select_capabilities(task)

    print(json.dumps({
        "task": task,
        "selected_count": len(results),
        "candidates": results,
        "note": "Candidatas sugeridas; aún no se ejecutan automáticamente.",
    }, ensure_ascii=False, indent=2))
