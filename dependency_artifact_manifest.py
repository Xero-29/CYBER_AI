#!/usr/bin/env python3
"""Registra hashes SHA-256 de los wheels descargados para un lock exacto."""
import argparse
import hashlib
import json
import os
import platform
import re
import stat
import sys
import zipfile
from email.parser import Parser
from pathlib import Path
from safe_io import atomic_write_text

from sbom_generator import _read_requirements


MAX_WHEEL_METADATA_BYTES = 2 * 1024 * 1024
MAX_WHEEL_BYTES = 512 * 1024 * 1024
MAX_WHEELHOUSE_BYTES = 2 * 1024 * 1024 * 1024
MAX_WHEEL_COUNT = 1024
MAX_WHEEL_ENTRIES = 100_000
NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.!+_-]*")


class ArtifactManifestError(ValueError):
    pass


def _wheel_metadata(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ArtifactManifestError(f"Wheel inexistente o inseguro: {path.name}")
    try:
        if path.stat().st_size > MAX_WHEEL_BYTES:
            raise ArtifactManifestError(
                f"Wheel supera el límite de {MAX_WHEEL_BYTES} bytes: {path.name}"
            )
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_WHEEL_ENTRIES:
                raise ArtifactManifestError(
                    f"Wheel supera el límite de {MAX_WHEEL_ENTRIES} entradas: {path.name}"
                )
            metadata_names = [
                info for info in entries
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
    except ArtifactManifestError:
        raise
    except (
        OSError, zipfile.BadZipFile, zipfile.LargeZipFile, UnicodeDecodeError,
        RuntimeError, NotImplementedError,
    ) as error:
        raise ArtifactManifestError(f"Wheel inválido: {path.name}") from error

    names = metadata.get_all("Name", [])
    versions = metadata.get_all("Version", [])
    metadata_versions = metadata.get_all("Metadata-Version", [])
    if (
        metadata.defects
        or len(names) != 1
        or len(versions) != 1
        or len(metadata_versions) != 1
        or not re.fullmatch(r"[0-9]+\.[0-9]+", metadata_versions[0])
    ):
        raise ArtifactManifestError(
            f"Wheel con identidad METADATA ausente, duplicada o inválida: {path.name}"
        )
    name, version = names[0], versions[0]
    if not NAME_PATTERN.fullmatch(name) or not VERSION_PATTERN.fullmatch(version):
        raise ArtifactManifestError(f"Wheel con Name/Version inválidos: {path.name}")
    return name, version


def build_manifest(root, wheelhouse, lock_file="requirements.lock"):
    root = Path(root).resolve()
    wheelhouse = Path(wheelhouse)
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        raise ArtifactManifestError("Wheelhouse debe ser un directorio real.")
    lock_candidate = Path(lock_file)
    if not lock_candidate.is_absolute():
        lock_candidate = root / lock_candidate
    if lock_candidate.is_symlink():
        raise ArtifactManifestError("No se permiten symlinks en el lock.")
    lock = lock_candidate.resolve(strict=True)
    try:
        lock.relative_to(root)
    except ValueError as error:
        raise ArtifactManifestError("El lock debe permanecer dentro del proyecto.") from error
    direct = _read_requirements(lock, root)
    wheels = []
    total_bytes = 0
    try:
        with os.scandir(wheelhouse) as entries:
            for entry in entries:
                if not entry.name.endswith(".whl"):
                    continue
                if len(wheels) >= MAX_WHEEL_COUNT:
                    raise ArtifactManifestError(
                        f"Wheelhouse supera el límite de {MAX_WHEEL_COUNT} wheels."
                    )
                if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
                    raise ArtifactManifestError("No se permiten symlinks en el wheelhouse.")
                size = entry.stat(follow_symlinks=False).st_size
                if size > MAX_WHEEL_BYTES:
                    raise ArtifactManifestError(
                        f"Wheel supera el límite de {MAX_WHEEL_BYTES} bytes: {entry.name}"
                    )
                total_bytes += size
                if total_bytes > MAX_WHEELHOUSE_BYTES:
                    raise ArtifactManifestError(
                        f"Wheelhouse supera el límite total de {MAX_WHEELHOUSE_BYTES} bytes."
                    )
                wheels.append(Path(entry.path))
    except OSError as error:
        raise ArtifactManifestError("No se pudo inspeccionar el wheelhouse.") from error
    if not wheels:
        raise ArtifactManifestError("No se encontraron wheels descargados.")
    wheels.sort(key=lambda item: item.name)
    found = {}
    verified_total_bytes = 0
    for wheel in wheels:
        before = wheel.stat(follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise ArtifactManifestError(f"Wheel no regular: {wheel.name}")
        if before.st_size > MAX_WHEEL_BYTES:
            raise ArtifactManifestError(
                f"Wheel supera el límite de {MAX_WHEEL_BYTES} bytes: {wheel.name}"
            )
        verified_total_bytes += before.st_size
        if verified_total_bytes > MAX_WHEELHOUSE_BYTES:
            raise ArtifactManifestError(
                f"Wheelhouse supera el límite total de {MAX_WHEELHOUSE_BYTES} bytes."
            )
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
        after = wheel.stat(follow_symlinks=False)
        identity_before = (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        identity_after = (
            after.st_dev, after.st_ino, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        )
        if identity_before != identity_after:
            raise ArtifactManifestError(
                f"Wheel cambió durante la verificación: {wheel.name}"
            )
        if digest_value not in direct[normalized]["hashes"]:
            raise ArtifactManifestError(
                f"El hash del wheel no coincide con requirements.lock: {wheel.name}."
            )
        found[normalized] = {
            "name": normalized,
            "version": version,
            "filename": wheel.name,
            "size_bytes": after.st_size,
            "sha256": digest_value,
        }
    missing = sorted(set(direct) - set(found))
    if missing:
        raise ArtifactManifestError(
            "No hay wheel descargado para dependencias fijadas: " + ", ".join(missing)
        )
    return {
        "schema": "cyber-ai-dependency-artifacts-v1",
        "lock_file": lock.relative_to(root).as_posix(),
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
    parser.add_argument("--lock-file", type=Path, default=Path("requirements.lock"))
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
