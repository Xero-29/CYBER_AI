#!/usr/bin/env python3
"""Registra hashes SHA-256 de los wheels descargados para un lock exacto."""
import argparse
import hashlib
import json
import platform
import sys
import zipfile
from email.parser import Parser
from pathlib import Path

from sbom_generator import _read_requirements


class ArtifactManifestError(ValueError):
    pass


def _wheel_metadata(path):
    try:
        with zipfile.ZipFile(path) as archive:
            metadata_names = [
                name for name in archive.namelist()
                if name.endswith(".dist-info/METADATA")
            ]
            if len(metadata_names) != 1:
                raise ArtifactManifestError(
                    f"Wheel con METADATA ausente o ambiguo: {path.name}"
                )
            metadata = Parser().parsestr(
                archive.read(metadata_names[0]).decode("utf-8")
            )
            name, version = metadata.get("Name"), metadata.get("Version")
            if not name or not version:
                raise ArtifactManifestError(
                    f"Wheel sin Name/Version válidos: {path.name}"
                )
            return name, version
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError) as error:
        raise ArtifactManifestError(f"Wheel inválido: {path.name}") from error


def build_manifest(root, wheelhouse):
    root = Path(root).resolve()
    wheelhouse = Path(wheelhouse)
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        raise ArtifactManifestError("Wheelhouse debe ser un directorio real.")
    lock = root / "requirements.lock"
    direct = _read_requirements(lock, root)
    wheels = sorted(wheelhouse.glob("*.whl"))
    if not wheels:
        raise ArtifactManifestError("No se encontraron wheels descargados.")
    found = {}
    for wheel in wheels:
        if wheel.is_symlink() or not wheel.is_file():
            raise ArtifactManifestError("No se permiten symlinks en el wheelhouse.")
        name, version = _wheel_metadata(wheel)
        from sbom_generator import _normalize
        normalized = _normalize(name)
        if normalized in found:
            raise ArtifactManifestError(
                f"Más de un wheel para {normalized}; seleccione una plataforma concreta."
            )
        if normalized not in direct or direct[normalized]["version"] != version:
            raise ArtifactManifestError(
                f"Wheel no fijado o versión distinta: {name}=={version}."
            )
        digest = hashlib.sha256()
        with wheel.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest_value = digest.hexdigest()
        if digest_value not in direct[normalized]["hashes"]:
            raise ArtifactManifestError(
                f"El hash del wheel no coincide con requirements.lock: {wheel.name}."
            )
        found[normalized] = {
            "name": normalized,
            "version": version,
            "filename": wheel.name,
            "size_bytes": wheel.stat().st_size,
            "sha256": digest_value,
        }
    missing = sorted(set(direct) - set(found))
    if missing:
        raise ArtifactManifestError(
            "No hay wheel descargado para dependencias fijadas: " + ", ".join(missing)
        )
    return {
        "schema": "cyber-ai-dependency-artifacts-v1",
        "lock_file": "requirements.lock",
        "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "artifacts": [found[name] for name in sorted(found)],
        "scope": "Wheels descargados y verificados contra hashes SHA-256 fijados en requirements.lock para esta plataforma.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.root, args.wheelhouse)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Manifiesto de artefactos generado: {len(manifest['artifacts'])} wheels")
        return 0
    except (OSError, ArtifactManifestError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
