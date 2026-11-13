#!/usr/bin/env python3
"""Comprobación local de preparación de CYBER_AI sin iniciar servicios ni red."""

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parent
REQUIRED_FILES = (
    "cyber_ai.py",
    "requirements.txt",
    "config/model_roles.json",
    "tests",
)
REQUIRED_MODULES = ("requests", "ddgs")
OPTIONAL_MODULES = {
    "pypdf": "PDF",
    "docx": "DOCX",
    "openpyxl": "XLSX",
    "pptx": "PPTX",
}
OPTIONAL_EXECUTABLES = (
    "docker", "ollama", "nuclei", "ruff", "bandit",
    "semgrep", "syft", "trivy",
)


def collect_checks(root=PROJECT, python_version=None, module_lookup=None,
                   executable_lookup=None, environ=None):
    root = Path(root)
    python_version = python_version or sys.version_info
    module_lookup = module_lookup or importlib.util.find_spec
    executable_lookup = executable_lookup or shutil.which
    environ = os.environ if environ is None else environ
    checks = []

    def add(name, status, detail):
        checks.append({"name": name, "status": status, "detail": detail})

    version = ".".join(map(str, python_version[:3]))
    add("python", "ok" if tuple(python_version[:2]) >= (3, 12) else "error",
        f"Detectado Python {version}; requerido >= 3.12.")

    for relative in REQUIRED_FILES:
        exists = (root / relative).exists()
        add(f"file:{relative}", "ok" if exists else "error",
            "Disponible." if exists else "No se encontró en el repositorio.")

    config = root / "config/model_roles.json"
    if config.is_file():
        try:
            with config.open(encoding="utf-8") as stream:
                parsed = json.load(stream)
            valid = isinstance(parsed, dict)
            add("model_config", "ok" if valid else "error",
                "JSON válido." if valid else "La raíz de configuración debe ser un objeto JSON.")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            add("model_config", "error", f"Configuración ilegible: {error}")

    for module in REQUIRED_MODULES:
        try:
            available = module_lookup(module) is not None
        except (ImportError, ValueError):
            available = False
        add(f"python:{module}", "ok" if available else "error",
            "Instalado." if available else "Falta; ejecuta pip install -r requirements.txt.")

    for module, label in OPTIONAL_MODULES.items():
        try:
            available = module_lookup(module) is not None
        except (ImportError, ValueError):
            available = False
        add(f"optional:{label}", "ok" if available else "warning",
            "Extractor disponible." if available else
            f"Extractor opcional ausente; instala requirements-documents.txt si lo necesitas.")

    for executable in OPTIONAL_EXECUTABLES:
        available = executable_lookup(executable) is not None
        add(f"optional:{executable}", "ok" if available else "warning",
            "Detectado en PATH." if available else "No detectado; solo necesario para esa integración.")

    ledger_path = Path(environ.get(
        "CYBER_AI_LEDGER_PATH", root / "data/execution_ledger.sqlite3"
    ))
    if ledger_path.is_file():
        try:
            from execution_ledger import ExecutionLedger
            integrity = ExecutionLedger(ledger_path).verify()
            valid = integrity.get("valid") is True
            add("execution_ledger", "ok" if valid else "error",
                "Cadena íntegra." if valid else f"Integridad inválida: {integrity}")
        except Exception as error:
            add("execution_ledger", "error", f"No se pudo verificar: {error}")
    else:
        add("execution_ledger", "warning",
            "Aún no existe; se creará al registrar la primera ejecución.")

    errors = sum(item["status"] == "error" for item in checks)
    warnings = sum(item["status"] == "warning" for item in checks)
    return {
        "status": "ready" if errors == 0 else "blocked",
        "errors": errors,
        "warnings": warnings,
        "network_accessed": False,
        "services_started": False,
        "checks": checks,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Imprimir JSON legible por máquinas.")
    args = parser.parse_args(argv)
    report = collect_checks()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"CYBER_AI: {report['status'].upper()}")
        for item in report["checks"]:
            print(f"[{item['status'].upper()}] {item['name']}: {item['detail']}")
        print(f"Errores: {report['errors']} | Advertencias: {report['warnings']}")
        print("No se inició ningún servicio ni se realizó acceso de red.")
    return 0 if report["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
