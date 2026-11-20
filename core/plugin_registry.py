#!/usr/bin/env python3
"""Validated, non-executing registry for CYBER_AI components."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any

MANIFEST_VERSION = 1
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,79}$")
KINDS = {"agent", "scanner", "analyzer", "verifier", "patcher", "stress_tester", "collector", "knowledge_provider", "integration", "orchestrator", "other"}
RISKS = {"read_only", "low", "moderate", "high", "critical"}

class ManifestError(ValueError):
    """Invalid component manifest."""

def _string(value: Any, field: str, required: bool = True):
    if value is None and not required: return None
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{field} debe ser texto no vacío.")
    return value.strip()

def validate_manifest(data: Any, source: Path) -> dict[str, Any]:
    if not isinstance(data, dict): raise ManifestError("El manifiesto debe ser un objeto JSON.")
    if data.get("manifest_version") != MANIFEST_VERSION:
        raise ManifestError(f"manifest_version debe ser {MANIFEST_VERSION}.")
    component_id = _string(data.get("id"), "id")
    if not ID_RE.fullmatch(component_id): raise ManifestError("id no cumple el formato.")
    name, version, kind = (_string(data.get(k), k) for k in ("name", "version", "kind"))
    if kind not in KINDS: raise ManifestError(f"kind no soportado: {kind}")
    entrypoint = _string(data.get("entrypoint"), "entrypoint", False)
    capabilities, dependencies = data.get("capabilities", []), data.get("dependencies", [])
    for field, value in (("capabilities", capabilities), ("dependencies", dependencies)):
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            raise ManifestError(f"{field} debe ser una lista de cadenas.")
    permissions = data.get("permissions", {})
    if not isinstance(permissions, dict): raise ManifestError("permissions debe ser un objeto.")
    risk, requested = permissions.get("risk", "high"), permissions.get("requested", [])
    if risk not in RISKS: raise ManifestError(f"Nivel de riesgo no válido: {risk}")
    if not isinstance(requested, list) or any(not isinstance(x, str) for x in requested):
        raise ManifestError("permissions.requested debe ser una lista de cadenas.")
    enabled = data.get("enabled", False)
    if not isinstance(enabled, bool): raise ManifestError("enabled debe ser booleano.")
    return {
        "manifest_version": MANIFEST_VERSION, "id": component_id, "name": name,
        "version": version, "kind": kind, "entrypoint": entrypoint,
        "capabilities": sorted(set(capabilities)), "dependencies": sorted(set(dependencies)),
        "permissions": {"risk": risk, "requested": sorted(set(requested)),
            "requires_approval": bool(permissions.get("requires_approval", True)),
            "scope_required": bool(permissions.get("scope_required", True))},
        "enabled": enabled, "discovered_from": str(source),
        "trust_status": "untrusted", "execution_authorized": False
    }

def load_manifest(path: Path) -> dict[str, Any]:
    try: raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"No se pudo leer {path}: {exc}") from exc
    return validate_manifest(raw, path)

def build_inventory(roots: list[str | Path]) -> dict[str, Any]:
    components, errors, seen = [], [], set()
    for value in roots:
        root = Path(value).expanduser().resolve()
        if not root.exists(): continue
        if not root.is_dir():
            errors.append({"path": str(root), "error": "La raíz no es un directorio."}); continue
        for path in sorted(root.rglob("*.component.json")):
            if path.is_symlink() or not path.is_file(): continue
            try:
                item = load_manifest(path)
                if item["id"] in seen: raise ManifestError(f"ID duplicado: {item['id']}")
                seen.add(item["id"]); components.append(item)
            except ManifestError as exc: errors.append({"path": str(path), "error": str(exc)})
    canonical = json.dumps(components, sort_keys=True, ensure_ascii=False).encode()
    return {"inventory_version": 1, "component_count": len(components),
        "components": components, "errors": errors,
        "sha256": hashlib.sha256(canonical).hexdigest(),
        "security_note": "Descubierto no significa confiable, habilitado ni autorizado. El inventario no importa ni ejecuta componentes."}

def write_inventory(inventory: dict[str, Any], destination: str | Path) -> Path:
    path = Path(destination); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path); return path
