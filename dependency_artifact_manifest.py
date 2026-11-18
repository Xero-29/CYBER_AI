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
from safe_io import atomic_write_text

from sbom_generator import _project_file, _read_requirements


MAX_WHEEL_METADATA_BYTES = 2 * 1024 * 1024


class ArtifactManifestError(ValueError):
    pass


def _wheel_metadata(path):
    try:
        with zipfile.ZipFile(path) as archive:
            metadata_names = [
                info for info in archive.infolist()
                if info.filename.endswith(".dist-info/METADATA")
            ]
            if len(metadata_names) != 1:
                raise ArtifactManifestError(
                    f"Wheel con METADATA ausente o ambiguo: {path.name}"
                )
            metadata_info = metadata_names[0]
            if metadata_info.file_size > MAX_WHEEL_METADATA_BYTES:
                raise ArtifactManifestError(
                    f"Wheel METADATA supera 2 MiB: {path.name}"
                )
            with archive.open(metadata_info) as stream:
                raw_metadata = stream.read(MAX_WHEEL_METADATA_BYTES + 1)
            if (
                len(raw_metadata) > MAX_WHEEL_METADATA_BYTES
                or len(raw_metadata) != metadata_info.file_size
            ):
                raise ArtifactManifestError(
                    f"Wheel METADATA inválido o demasiado grande: {path.name}"
                )
            metadata = Parser().parsestr(raw_metadata.decode("utf-8"))
            name, version = metadata.get("Name"), metadata.get("Version")
            if not name or not version:
                raise ArtifactManifestError(
                    f"Wheel sin Name/Version válidos: {path.name}"
                )
            return name, version
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError, RuntimeError, NotImplementedError) as error:
        raise ArtifactManifestError(f"Wheel inválido: {path.name}") from error


def build_manifest(root, wheelhouse, *, lock_file="requirements.lock"):
    root = Path(root).resolve()
    wheelhouse = Path(wheelhouse)
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        raise ArtifactManifestError("Wheelhouse debe ser un directorio real.")
    try:
        lock = _project_file(root, lock_file)
        direct = _read_requirements(lock, root)
    except (OSError, ValueError) as error:
        raise ArtifactManifestError("Archivo lock inexistente o inválido.") from error
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
        found[normalized] = {
            "name": normalized,
            "version": version,
            "filename": wheel.name,
            "size_bytes": wheel.stat().st_size,
            "sha256": digest.hexdigest(),
        }
    missing = sorted(set(direct) - set(found))
    if missing:
        raise ArtifactManifestError(
            "No hay wheel descargado para dependencias fijadas: " + ", ".join(missing)
        )
    return {
        "schema": "cyber-ai-dependency-artifacts-v1",
        "lock_file": Path(lock_file).as_posix(),
        "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "artifacts": [found[name] for name in sorted(found)],
        "scope": "Wheels descargados y hasheados en esta ejecución/plataforma; no son hashes fijados en requirements.lock.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--lock-file", default="requirements.lock", help="Lock relativo a --root.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.root, args.wheelhouse, lock_file=args.lock_file)
        atomic_write_text(
            args.output,
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            create_parents=True,
        )
        print(f"Manifiesto de artefactos generado: {len(manifest['artifacts'])} wheels")
        return 0
    except (OSError, ArtifactManifestError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
