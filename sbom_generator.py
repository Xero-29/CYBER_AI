#!/usr/bin/env python3
"""Genera un SBOM CycloneDX determinista desde requirements.lock."""
import argparse
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
PACKAGE_LINE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([A-Za-z0-9][A-Za-z0-9.!+_-]*)$")
NAME_NORMALIZE = re.compile(r"[-_.]+")


class LockfileError(ValueError):
    pass


def _normalize(name):
    return NAME_NORMALIZE.sub("-", name).lower()


def _read_requirements(path, root, seen=None, depth=0):
    if seen is None:
        seen = set()
    if depth > 8:
        raise LockfileError("Demasiados niveles de inclusión de requirements.")
    path = Path(path)
    if path.is_symlink():
        raise LockfileError("No se permiten symlinks en archivos requirements.")
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise LockfileError("El archivo requirements debe permanecer en el proyecto.") from error
    if not resolved.is_file() or resolved in seen:
        if resolved in seen:
            return {}
        raise LockfileError("Archivo requirements inexistente o inválido.")
    seen.add(resolved)
    packages = {}
    for number, raw in enumerate(resolved.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-r "):
            include = line[3:].strip()
            if not include or Path(include).is_absolute() or ".." in Path(include).parts:
                raise LockfileError(f"Inclusión no permitida en {resolved.name}:{number}.")
            child = resolved.parent / include
            included = _read_requirements(child, root, seen, depth + 1)
            for package_name, package in included.items():
                existing = packages.get(package_name)
                if existing and existing["version"] != package["version"]:
                    raise LockfileError(f"Versiones incompatibles para {package_name}.")
                packages[package_name] = package
            continue
        match = PACKAGE_LINE.fullmatch(line)
        if not match:
            raise LockfileError(
                f"Dependencia no fijada o sintaxis no soportada en {resolved.name}:{number}: {line[:120]}"
            )
        name, version = match.groups()
        normalized = _normalize(name)
        if normalized in packages and packages[normalized]["version"] != version:
            raise LockfileError(f"Versiones incompatibles para {normalized}.")
        packages[normalized] = {"name": normalized, "version": version, "source": resolved.name}
    return packages


def build_sbom(root=PROJECT):
    root = Path(root).resolve()
    lock_path = root / "requirements.lock"
    direct_path = root / "requirements.txt"
    if not lock_path.is_file() or not direct_path.is_file():
        raise LockfileError("Faltan requirements.lock o requirements.txt.")
    locked = _read_requirements(lock_path, root)
    direct = _read_requirements(direct_path, root)
    if not locked or not direct:
        raise LockfileError("No se encontraron dependencias fijadas.")
    missing = set(direct) - set(locked)
    if missing:
        raise LockfileError(f"Dependencias directas ausentes del lock: {sorted(missing)}.")
    lock_hash = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    components = []
    refs = []
    for name, item in sorted(locked.items()):
        ref = f"pkg:pypi/{name}@{item['version']}"
        refs.append(ref)
        components.append({
            "type": "library",
            "bom-ref": ref,
            "name": name,
            "version": item["version"],
            "purl": ref,
            "scope": "required",
            "properties": [
                {"name": "cyber_ai:dependency_type",
                 "value": "direct" if name in direct else "transitive"},
                {"name": "cyber_ai:lock_source", "value": item["source"]},
                {"name": "cyber_ai:artifact_hash", "value": "not-recorded"},
            ],
        })
    serial = uuid.uuid5(uuid.NAMESPACE_URL, f"cyber-ai-requirements:{lock_hash}")
    root_ref = "pkg:generic/cyber-ai@unreleased"
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{serial}",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application", "bom-ref": root_ref,
                "name": "CYBER_AI", "version": "unreleased",
            },
            "properties": [
                {"name": "cyber_ai:lock_file", "value": "requirements.lock"},
                {"name": "cyber_ai:lock_sha256", "value": lock_hash},
                {"name": "cyber_ai:artifact_hashes", "value": "not-available-in-lock"},
                {"name": "cyber_ai:dependency_graph", "value": "root-to-locked-components; transitive edges not inferred"},
            ],
        },
        "components": components,
        "dependencies": [{"ref": root_ref, "dependsOn": refs}],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        document = build_sbom(args.root)
        rendered = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"SBOM CycloneDX generado: {args.output} ({len(document['components'])} componentes)")
        else:
            sys.stdout.write(rendered)
    except (OSError, LockfileError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
