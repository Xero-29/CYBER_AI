#!/usr/bin/env python3
"""Genera un SBOM CycloneDX determinista desde requirements.lock."""
import argparse
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path
from safe_io import atomic_write_text

PROJECT = Path(__file__).resolve().parent
PACKAGE_LINE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([A-Za-z0-9][A-Za-z0-9.!+_-]*)$")
HASH_LINE = re.compile(r"^--hash=sha256:([a-f0-9]{64})$")
NAME_NORMALIZE = re.compile(r"[-_.]+")


class LockfileError(ValueError):
    pass


def _normalize(name):
    return NAME_NORMALIZE.sub("-", name).lower()


def _logical_requirement_lines(path):
    pending = ""
    start_line = None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if pending:
            if line.endswith(chr(92)):
                pending += " " + line[:-1].strip()
                continue
            yield start_line, pending + " " + line
            pending = ""
            start_line = None
        elif line.endswith(chr(92)):
            pending = line[:-1].strip()
            start_line = number
        else:
            yield number, line
    if pending:
        raise LockfileError(f"Continuación incompleta en {path.name}:{start_line}.")


def _read_requirements(path, root, seen=None, depth=0, require_hashes=True):
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
    for number, line in _logical_requirement_lines(resolved):
        if line.startswith("-r "):
            include = line[3:].strip()
            if not include or Path(include).is_absolute() or ".." in Path(include).parts:
                raise LockfileError(f"Inclusión no permitida en {resolved.name}:{number}.")
            child = resolved.parent / include
            included = _read_requirements(child, root, seen, depth + 1, require_hashes)
            for package_name, package in included.items():
                existing = packages.get(package_name)
                if existing and existing["version"] != package["version"]:
                    raise LockfileError(f"Versiones incompatibles para {package_name}.")
                if existing:
                    existing["hashes"] = sorted(set(existing["hashes"]) | set(package["hashes"]))
                else:
                    packages[package_name] = package
            continue
        tokens = line.split()
        match = PACKAGE_LINE.fullmatch(tokens[0]) if tokens else None
        if not match:
            raise LockfileError(
                f"Dependencia no fijada o sintaxis no soportada en {resolved.name}:{number}: {line[:120]}"
            )
        name, version = match.groups()
        hashes = []
        for token in tokens[1:]:
            hash_match = HASH_LINE.fullmatch(token)
            if not hash_match:
                raise LockfileError(f"Hash SHA-256 inválido en {resolved.name}:{number}.")
            hashes.append(hash_match.group(1))
        if not hashes and require_hashes:
            raise LockfileError(
                f"Dependencia sin hash SHA-256 en {resolved.name}:{number}: {name}=={version}."
            )
        normalized = _normalize(name)
        existing = packages.get(normalized)
        if existing and existing["version"] != version:
            raise LockfileError(f"Versiones incompatibles para {normalized}.")
        if existing:
            existing["hashes"] = sorted(set(existing["hashes"]) | set(hashes))
        else:
            packages[normalized] = {
                "name": normalized, "version": version,
                "source": resolved.name, "hashes": sorted(set(hashes)),
            }
    return packages


def _project_file(root, value):
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    if candidate.is_symlink():
        raise LockfileError("No se permiten symlinks en archivos de dependencias.")
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise LockfileError("Los archivos de dependencias deben permanecer en el proyecto.") from error
    if not resolved.is_file():
        raise LockfileError("Archivo de dependencias inexistente o inválido.")
    return resolved


def build_sbom(
    root=PROJECT,
    artifact_manifest=None,
    lock_file="requirements.lock",
    direct_requirements="requirements.txt",
):
    root = Path(root).resolve()
    lock_path = _project_file(root, lock_file)
    direct_path = _project_file(root, direct_requirements)
    locked = _read_requirements(lock_path, root)
    direct = _read_requirements(direct_path, root, require_hashes=False)
    if not locked or not direct:
        raise LockfileError("No se encontraron dependencias fijadas.")
    missing = set(direct) - set(locked)
    mismatched = {
        name for name in direct
        if name in locked and direct[name]["version"] != locked[name]["version"]
    }
    if missing or mismatched:
        raise LockfileError(
            f"Dependencias directas ausentes o con versión distinta: "
            f"missing={sorted(missing)}, mismatched={sorted(mismatched)}."
        )
    lock_hash = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    artifact_hashes = {}
    if artifact_manifest is not None:
        manifest_path = Path(artifact_manifest)
        if manifest_path.is_symlink() or not manifest_path.is_file():
            raise LockfileError("Manifiesto de artefactos inválido.")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise LockfileError("No se pudo leer el manifiesto de artefactos.") from error
        if not isinstance(manifest, dict) or manifest.get("lock_sha256") != lock_hash:
            raise LockfileError("El manifiesto no corresponde al lock seleccionado o tiene formato inválido.")
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, list):
            raise LockfileError("La lista de artefactos del manifiesto es inválida.")
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                raise LockfileError("Entrada de artefacto inválida.")
            name = _normalize(str(artifact.get("name", "")))
            version = artifact.get("version")
            digest = artifact.get("sha256")
            if (
                name not in locked
                or locked[name]["version"] != version
                or not isinstance(digest, str)
                or not re.fullmatch(r"[a-f0-9]{64}", digest)
                or name in artifact_hashes
            ):
                raise LockfileError("El manifiesto contiene un artefacto no fijado o inválido.")
            if digest not in locked[name]["hashes"]:
                raise LockfileError(
                    f"El hash del artefacto de {name} no coincide con el lock."
                )
            artifact_hashes[name] = digest
        if set(artifact_hashes) != set(locked):
            raise LockfileError("El manifiesto no cubre todas las dependencias fijadas.")
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
            **({
                "hashes": [{"alg": "SHA-256", "content": artifact_hashes[name]}]
            } if name in artifact_hashes else {}),
            "properties": [
                {"name": "cyber_ai:dependency_type",
                 "value": "direct" if name in direct else "transitive"},
                {"name": "cyber_ai:lock_source", "value": item["source"]},
                {"name": "cyber_ai:artifact_hash",
                 "value": artifact_hashes.get(name, "not-recorded")},
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
                {"name": "cyber_ai:lock_file", "value": lock_path.relative_to(root).as_posix()},
                {"name": "cyber_ai:lock_sha256", "value": lock_hash},
                {"name": "cyber_ai:artifact_hashes",
                 "value": "captured-for-build-platform" if artifact_hashes else "not-recorded"},
                {"name": "cyber_ai:dependency_graph",
                 "value": "root-to-locked-components; transitive edges not inferred"},
            ],
        },
        "components": components,
        "dependencies": [{"ref": root_ref, "dependsOn": refs}],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--artifact-manifest", type=Path)
    parser.add_argument("--lock-file", type=Path, default=Path("requirements.lock"))
    parser.add_argument("--direct-requirements", type=Path, default=Path("requirements.txt"))
    args = parser.parse_args(argv)
    try:
        document = build_sbom(
            args.root,
            artifact_manifest=args.artifact_manifest,
            lock_file=args.lock_file,
            direct_requirements=args.direct_requirements,
        )
        rendered = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if args.output:
            atomic_write_text(args.output, rendered, create_parents=True)
            print(f"SBOM CycloneDX generado: {args.output} ({len(document['components'])} componentes)")
        else:
            sys.stdout.write(rendered)
    except (OSError, LockfileError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
