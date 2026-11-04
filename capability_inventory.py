#!/usr/bin/env python3
"""Inventario de herramientas y plantillas para CYBER_AI."""

import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def build_inventory():
    # Detectar herramientas instaladas.
    names = ("nuclei", "nmap", "python3", "go", "semgrep")
    tools = {
        name: {"available": bool(shutil.which(name)), "path": shutil.which(name)}
        for name in names
    }

    # Registrar las plantillas Nuclei y sus categorías.
    root = Path.home() / "nuclei-templates"
    items = []
    categories = Counter()

    if root.is_dir():
        for path in root.rglob("*.yaml"):
            relative = path.relative_to(root)
            category = relative.parts[0] if len(relative.parts) > 1 else "other"
            categories[category] += 1
            items.append({
                "name": path.stem,
                "path": str(path),
                "category": category,
            })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tools": tools,
        "nuclei_templates": {
            "root": str(root),
            "available": root.is_dir(),
            "count": len(items),
            "categories": dict(sorted(categories.items())),
            "items": sorted(items, key=lambda item: item["path"]),
        },
        "note": "Inventario solamente; no ejecuta escaneos.",
    }


if __name__ == "__main__":
    output = Path("reports/capability_inventory.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    data = build_inventory()
    output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Herramientas registradas:", len(data["tools"]))
    print("Plantillas encontradas:", data["nuclei_templates"]["count"])
    print("Categorías:", len(data["nuclei_templates"]["categories"]))
    print("Informe:", output)
