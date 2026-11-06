#!/usr/bin/env python3
"""Descubre manifiestos sin importar ni ejecutar código."""
import argparse, json
from pathlib import Path
from core.plugin_registry import build_inventory, write_inventory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

def default_roots():
    return [PROJECT_ROOT / name for name in ("agents", "plugins", "tools", "modules", "scanners", "patchers", "stress_testing")]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", default=[], help="Raíz adicional/reemplazo.")
    parser.add_argument("--output", default="reports/component_inventory.json")
    args = parser.parse_args()
    inventory = build_inventory([Path(x) for x in args.root] if args.root else default_roots())
    destination = write_inventory(inventory, args.output)
    print(json.dumps({"components": inventory["component_count"], "errors": len(inventory["errors"]), "inventory": str(destination), "sha256": inventory["sha256"]}, indent=2, ensure_ascii=False))
    return 0 if not inventory["errors"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
