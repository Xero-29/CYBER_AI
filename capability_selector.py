#!/usr/bin/env python3
"""Selecciona plantillas según la intención de la auditoría."""

import json
import re
import sys
from pathlib import Path

INVENTORY = Path("reports/capability_inventory.json")
TEMPLATE_ROOT = Path.home() / "nuclei-templates"


def select_capabilities(task, limit=25):
    """Puntúa las plantillas según la tarea y su aplicabilidad general."""
    if not INVENTORY.is_file():
        raise FileNotFoundError(
            "Ejecuta primero: python3 capability_inventory.py"
        )

    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    templates = data["nuclei_templates"]["items"]
    task = task.lower()

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
        path = Path(item["path"])
        path_text = str(path).lower()
        name = item.get("name", "").lower()

        try:
            relative = path.relative_to(TEMPLATE_ROOT)
        except ValueError:
            continue

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
            header = "\n".join(content.splitlines()[:100]).lower()
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

    ranked.sort(key=lambda pair: (-pair[0], pair[1]["path"]))

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
