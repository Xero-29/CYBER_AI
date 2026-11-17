#!/usr/bin/env python3
"""Comprobación local de preparación de CYBER_AI sin iniciar servicios ni red."""

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from importlib.metadata import entry_points


PROJECT = Path(__file__).resolve().parent
REQUIRED_FILES = (
    "cyber_ai.py",
    "requirements.txt",
    "requirements.lock",
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


BUILTIN_PROVIDER_CAPABILITIES = {
    "ollama": {"chat", "embeddings", "model_listing"},
    "openai": {"chat", "embeddings"},
    "anthropic": {"chat"},
    "gemini": {"chat", "embeddings"},
}


def validate_provider_routes(config, environ=None, plugin_protocols=None):
    """Comprueba rutas y capacidades sin importar plugins ni hacer llamadas de red."""
    environ = os.environ if environ is None else environ
    providers = config.get("llm_providers", {})
    agents = config.get("agents", {})
    capability_map = config.get("capability_providers", {})
    fallback_map = config.get("fallback_providers", {})
    if not isinstance(providers, dict) or not isinstance(agents, dict):
        return [{"name": "provider_config", "status": "error",
                 "detail": "llm_providers y agents deben ser objetos."}]
    if not isinstance(capability_map, dict) or not isinstance(fallback_map, dict):
        return [{"name": "provider_routing", "status": "error",
                 "detail": "capability_providers y fallback_providers deben ser objetos."}]
    if plugin_protocols is None:
        plugin_protocols = {item.name for item in entry_points(group="cyber_ai.providers")}
    results = []
    default = config.get("default_provider", "ollama")
    for role, agent in agents.items():
        if not isinstance(agent, dict):
            results.append({"name": f"provider:{role}", "status": "error",
                            "detail": "Definición de agente inválida."})
            continue
        capability = "embeddings" if agent.get("type") == "embeddings" else "chat"
        preferred = agent.get("provider") or capability_map.get(capability) or default
        if not isinstance(preferred, str) or not preferred.strip():
            results.append({"name": f"provider:{role}", "status": "error",
                            "detail": "Proveedor preferido inválido."})
            continue
        fallbacks = fallback_map.get(capability, [])
        if (isinstance(fallbacks, str) or not isinstance(fallbacks, (list, tuple))
                or any(not isinstance(value, str) or not value.strip() for value in fallbacks)):
            results.append({"name": f"provider:{role}", "status": "error",
                            "detail": f"fallback_providers.{capability} debe ser una lista de nombres."})
            continue
        candidates = list(dict.fromkeys([preferred, *fallbacks]))
        selected = None
        plugin_pending = False
        for name in candidates:
            item = providers.get(name)
            if not isinstance(name, str) or not isinstance(item, dict) or not item.get("enabled"):
                continue
            protocol = item.get("protocol")
            if protocol in BUILTIN_PROVIDER_CAPABILITIES:
                if capability in BUILTIN_PROVIDER_CAPABILITIES[protocol]:
                    selected = (name, item)
                    break
            elif protocol in plugin_protocols:
                selected = (name, item)
                plugin_pending = True
                break
        if selected is None:
            results.append({
                "name": f"provider:{role}", "status": "error",
                "detail": f"No hay proveedor habilitado con capacidad {capability}.",
            })
            continue
        name, item = selected
        missing_key = (
            item.get("requires_api_key") is True
            and (not item.get("api_key_env") or not environ.get(item.get("api_key_env"), "").strip())
        )
        if missing_key:
            results.append({
                "name": f"provider:{role}", "status": "warning",
                "detail": f"Ruta {name} seleccionada, pero falta la variable de credencial.",
            })
        elif plugin_pending:
            results.append({
                "name": f"provider:{role}", "status": "warning",
                "detail": f"Plugin {item.get('protocol')} instalado; sus capacidades se validan al cargarlo.",
            })
        else:
            results.append({
                "name": f"provider:{role}", "status": "ok",
                "detail": f"{name} ofrece {capability}.",
            })
    return results



def validate_secret_hygiene(config):
    """Detecta secretos incrustados y referencias inseguras a variables de entorno."""
    import re

    findings = []
    secret_fields = {
        "api_key", "api_secret", "access_token", "refresh_token",
        "client_secret", "password", "private_key", "secret_key",
    }
    env_pattern = re.compile(r"^[A-Z][A-Z0-9_]{2,127}$")

    def walk(value, path="$"):
        if isinstance(value, dict):
            for key, child in value.items():
                key_text = str(key).lower()
                child_path = f"{path}.{key}"
                if key_text in secret_fields and isinstance(child, str) and child.strip():
                    findings.append({
                        "path": child_path,
                        "reason": "Secreto literal en configuración; usar un gestor de secretos o variable de entorno.",
                    })
                if key_text == "api_key_env":
                    if not isinstance(child, str) or not env_pattern.fullmatch(child):
                        findings.append({
                            "path": child_path,
                            "reason": "api_key_env debe ser el nombre de una variable de entorno en mayúsculas.",
                        })
                walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")

    walk(config)
    return findings


def validate_env_file_permissions(root):
    """Rechaza archivos .env reales que sean legibles por grupo/otros o symlinks."""
    import stat

    findings = []
    root = Path(root)
    for path in sorted(root.glob(".env*")):
        if path.name in {".env.example", ".env.sample", ".env.template"}:
            continue
        try:
            if path.is_symlink():
                findings.append({
                    "path": path.name,
                    "reason": "El archivo de entorno no debe ser un enlace simbólico.",
                })
                continue
            if not path.is_file():
                continue
            mode = stat.S_IMODE(path.stat(follow_symlinks=False).st_mode)
            if mode & 0o077:
                findings.append({
                    "path": path.name,
                    "reason": "Permisos inseguros: grupo u otros tienen permisos sobre el archivo .env; usar chmod 600.",
                })
        except OSError:
            findings.append({
                "path": path.name,
                "reason": "No se pudieron verificar los permisos del archivo de entorno.",
            })
    return findings



def validate_data_permissions(root):
    """Exige directorios de datos privados y protege archivos locales de claves."""
    import stat

    findings = []
    data_root = Path(root) / "data"
    if not data_root.exists() and not data_root.is_symlink():
        return findings
    if data_root.is_symlink():
        return [{"path": "data", "reason": "El directorio de datos no puede ser un enlace simbólico."}]
    if not data_root.is_dir():
        return [{"path": "data", "reason": "La ruta data debe ser un directorio."}]

    for current, dirs, files in os.walk(data_root, followlinks=False):
        current_path = Path(current)
        try:
            mode = stat.S_IMODE(current_path.stat(follow_symlinks=False).st_mode)
            if mode & 0o077:
                findings.append({
                    "path": str(current_path.relative_to(root)),
                    "reason": "Directorio de datos accesible por grupo u otros; usar chmod 700.",
                })
        except OSError:
            findings.append({
                "path": str(current_path.relative_to(root)),
                "reason": "No se pudieron verificar los permisos del directorio de datos.",
            })
        for name in list(dirs):
            child = current_path / name
            if child.is_symlink():
                findings.append({
                    "path": str(child.relative_to(root)),
                    "reason": "No se permiten enlaces simbólicos dentro de data.",
                })
                dirs.remove(name)
        for name in files:
            child = current_path / name
            if child.is_symlink():
                findings.append({
                    "path": str(child.relative_to(root)),
                    "reason": "No se permiten enlaces simbólicos dentro de data.",
                })
                continue
            lowered = name.lower()
            sensitive = (
                child.suffix.lower() in {".key", ".p12", ".pfx", ".secret"}
                or any(token in lowered for token in ("private", "credential", "token"))
            )
            if not sensitive:
                continue
            try:
                mode = stat.S_IMODE(child.stat(follow_symlinks=False).st_mode)
                if mode & 0o077:
                    findings.append({
                        "path": str(child.relative_to(root)),
                        "reason": "Archivo local sensible accesible por grupo u otros; usar chmod 600.",
                    })
            except OSError:
                findings.append({
                    "path": str(child.relative_to(root)),
                    "reason": "No se pudieron verificar los permisos del archivo sensible.",
                })
    return findings


def validate_evidence_permissions(root):
    """Exige evidencias locales privadas y rechaza symlinks en POSIX."""
    import stat

    if os.name != "posix":
        # Windows ACLs no se pueden verificar de forma portable con mode bits.
        return []
    root = Path(root)
    reports = root / "reports"
    evidence_root = reports / "tool_evidence"
    for path, relative in ((reports, "reports"), (evidence_root, "reports/tool_evidence")):
        if path.is_symlink():
            return [{"path": relative, "reason": "El árbol de evidencias no puede contener enlaces simbólicos."}]
    if not evidence_root.exists():
        return []
    if not evidence_root.is_dir():
        return [{"path": "reports/tool_evidence", "reason": "El destino de evidencias debe ser un directorio."}]

    findings = []
    try:
        directory_mode = stat.S_IMODE(evidence_root.stat(follow_symlinks=False).st_mode)
        if directory_mode & 0o077:
            findings.append({
                "path": "reports/tool_evidence",
                "reason": "Directorio de evidencias accesible por grupo u otros; usar chmod 700.",
            })
        for path in sorted(evidence_root.iterdir()):
            relative = str(path.relative_to(root))
            if path.is_symlink():
                findings.append({
                    "path": relative,
                    "reason": "No se permiten enlaces simbólicos en las evidencias.",
                })
            elif path.is_dir():
                findings.append({
                    "path": relative,
                    "reason": "No se permiten subdirectorios no auditados en las evidencias.",
                })
            elif path.is_file():
                mode = stat.S_IMODE(path.stat(follow_symlinks=False).st_mode)
                if mode & 0o077:
                    findings.append({
                        "path": relative,
                        "reason": "Archivo de evidencia accesible por grupo u otros; usar chmod 600.",
                    })
            else:
                findings.append({
                    "path": relative,
                    "reason": "Tipo de archivo no permitido en el directorio de evidencias.",
                })
    except OSError:
        findings.append({
            "path": "reports/tool_evidence",
            "reason": "No se pudieron verificar los permisos de las evidencias.",
        })
    return findings


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
            if valid:
                secret_findings = validate_secret_hygiene(parsed)
                for finding in secret_findings:
                    add(
                        "secret_hygiene",
                        "error",
                        f"{finding['path']}: {finding['reason']}",
                    )
                if not secret_findings:
                    add(
                        "secret_hygiene", "ok",
                        "No se detectaron secretos literales ni referencias api_key_env inválidas.",
                    )
                for route in validate_provider_routes(parsed, environ=environ):
                    add(route["name"], route["status"], route["detail"])
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            add("model_config", "error", f"Configuración ilegible: {error}")

    for finding in validate_env_file_permissions(root):
        add(
            "env_file_permissions",
            "error",
            f"{finding['path']}: {finding['reason']}",
        )

    for finding in validate_data_permissions(root):
        add(
            "data_permissions",
            "error",
            f"{finding['path']}: {finding['reason']}",
        )

    for finding in validate_evidence_permissions(root):
        add(
            "evidence_permissions",
            "error",
            f"{finding['path']}: {finding['reason']}",
        )

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
