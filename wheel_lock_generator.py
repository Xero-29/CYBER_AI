#!/usr/bin/env python3
"""Generate a deterministic, hash-enforced lock from a downloaded wheelhouse."""
import argparse
import hashlib
import os
import re
import stat
import sys
import zipfile
from email.parser import Parser
from pathlib import Path
from safe_io import atomic_write_text
from secret_redaction import redact_text


MAX_WHEEL_METADATA_BYTES = 2 * 1024 * 1024
MAX_WHEEL_BYTES = 512 * 1024 * 1024
MAX_WHEELHOUSE_BYTES = 2 * 1024 * 1024 * 1024
MAX_WHEEL_COUNT = 1024
MAX_WHEEL_ENTRIES = 100_000
MAX_REQUIREMENTS_BYTES = 1024 * 1024
NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.!+_-]*")


class WheelLockError(ValueError):
    pass


def normalize_name(value):
    return re.sub(r"[-_.]+", "-", value).lower()


def wheel_metadata(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise WheelLockError(f"Wheel inexistente o inseguro: {path.name}.")
    try:
        if path.stat().st_size > MAX_WHEEL_BYTES:
            raise WheelLockError(f"Wheel supera el límite de {MAX_WHEEL_BYTES} bytes: {path.name}.")
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_WHEEL_ENTRIES:
                raise WheelLockError(f"Wheel supera el límite de {MAX_WHEEL_ENTRIES} entradas: {path.name}.")
            metadata_files = [
                info for info in entries
                if info.filename.endswith(".dist-info/METADATA")
            ]
            if len(metadata_files) != 1:
                raise WheelLockError(f"Wheel sin METADATA único: {path.name}.")
            metadata_info = metadata_files[0]
            if metadata_info.file_size > MAX_WHEEL_METADATA_BYTES:
                raise WheelLockError(f"Wheel METADATA supera 2 MiB: {path.name}.")
            with archive.open(metadata_info) as stream:
                raw_metadata = stream.read(MAX_WHEEL_METADATA_BYTES + 1)
            if (
                len(raw_metadata) > MAX_WHEEL_METADATA_BYTES
                or len(raw_metadata) != metadata_info.file_size
            ):
                raise WheelLockError(f"Wheel METADATA inválido o demasiado grande: {path.name}.")
            metadata = Parser().parsestr(raw_metadata.decode("utf-8"))
    except WheelLockError:
        raise
    except (
        OSError, zipfile.BadZipFile, zipfile.LargeZipFile, UnicodeDecodeError,
        RuntimeError, NotImplementedError,
    ) as error:
        raise WheelLockError(f"Wheel inválido: {path.name}.") from error

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
        raise WheelLockError(f"Wheel con identidad METADATA ausente, duplicada o inválida: {path.name}.")
    name, version = names[0], versions[0]
    if not NAME_PATTERN.fullmatch(name) or not VERSION_PATTERN.fullmatch(version):
        raise WheelLockError(f"Wheel con Name/Version inválidos: {path.name}.")
    return normalize_name(name), version


def read_expected(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise WheelLockError("Archivo de requisitos inexistente o inseguro.")
    try:
        with path.open("rb") as stream:
            raw_requirements = stream.read(MAX_REQUIREMENTS_BYTES + 1)
        if len(raw_requirements) > MAX_REQUIREMENTS_BYTES:
            raise WheelLockError(
                f"El archivo de requisitos supera {MAX_REQUIREMENTS_BYTES} bytes."
            )
        requirements_text = raw_requirements.decode("utf-8")
    except UnicodeDecodeError as error:
        raise WheelLockError("El archivo de requisitos no es UTF-8 válido.") from error
    expected = {}
    for number, raw in enumerate(requirements_text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(
            rf"({NAME_PATTERN.pattern})==({VERSION_PATTERN.pattern})",
            line,
        )
        if not match:
            raise WheelLockError(f"Requisito directo no fijado en línea {number}.")
        name, version = match.groups()
        normalized = normalize_name(name)
        if normalized in expected and expected[normalized] != version:
            raise WheelLockError(f"Versiones directas incompatibles: {normalized}.")
        expected[normalized] = version
    if not expected:
        raise WheelLockError("No hay requisitos directos.")
    return expected


def build_lock(wheelhouse, requirements):
    wheelhouse = Path(wheelhouse)
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        raise WheelLockError("Wheelhouse inexistente o inseguro.")
    expected = read_expected(requirements)
    packages = {}
    wheels = []
    total_bytes = 0
    try:
        with os.scandir(wheelhouse) as entries:
            for entry in entries:
                if not entry.name.endswith(".whl"):
                    continue
                if len(wheels) >= MAX_WHEEL_COUNT:
                    raise WheelLockError(f"Wheelhouse supera el límite de {MAX_WHEEL_COUNT} wheels.")
                if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
                    raise WheelLockError(f"Wheel inseguro: {entry.name}.")
                size = entry.stat(follow_symlinks=False).st_size
                if size > MAX_WHEEL_BYTES:
                    raise WheelLockError(f"Wheel supera el límite de {MAX_WHEEL_BYTES} bytes: {entry.name}.")
                total_bytes += size
                if total_bytes > MAX_WHEELHOUSE_BYTES:
                    raise WheelLockError(
                        f"Wheelhouse supera el límite total de {MAX_WHEELHOUSE_BYTES} bytes."
                    )
                wheels.append(Path(entry.path))
    except OSError as error:
        raise WheelLockError("No se pudo inspeccionar el wheelhouse.") from error
    if not wheels:
        raise WheelLockError("Wheelhouse vacío.")
    wheels.sort(key=lambda item: item.name)
    verified_total_bytes = 0
    for wheel in wheels:
        before = wheel.stat(follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise WheelLockError(f"Wheel no regular: {wheel.name}.")
        if before.st_size > MAX_WHEEL_BYTES:
            raise WheelLockError(f"Wheel supera el límite de {MAX_WHEEL_BYTES} bytes: {wheel.name}.")
        verified_total_bytes += before.st_size
        if verified_total_bytes > MAX_WHEELHOUSE_BYTES:
            raise WheelLockError(
                f"Wheelhouse supera el límite total de {MAX_WHEELHOUSE_BYTES} bytes."
            )
        name, version = wheel_metadata(wheel)
        digest_builder = hashlib.sha256()
        with wheel.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest_builder.update(chunk)
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
            raise WheelLockError(f"Wheel cambió durante la verificación: {wheel.name}.")
        digest = digest_builder.hexdigest()
        current = packages.get(name)
        if current and current["version"] != version:
            raise WheelLockError(f"Versiones múltiples en wheelhouse: {name}.")
        if current:
            current["hashes"].add(digest)
        else:
            packages[name] = {"version": version, "hashes": {digest}}
    for name, version in expected.items():
        if name not in packages or packages[name]["version"] != version:
            raise WheelLockError(f"Wheelhouse no satisface requisito directo: {name}=={version}.")
    lines = [
        "# Generated from a verified Linux x86_64 CPython 3.12 wheelhouse.",
        "# Do not edit manually; regenerate and review the artifact hashes.",
    ]
    for name in sorted(packages):
        package = packages[name]
        hashes = " ".join(
            f"--hash=sha256:{value}" for value in sorted(package["hashes"])
        )
        lines.append(f"{name}=={package['version']} {hashes}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheelhouse", required=True)
    parser.add_argument("--requirements", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        lock = build_lock(args.wheelhouse, args.requirements)
        if args.output:
            atomic_write_text(args.output, lock)
        else:
            sys.stdout.write(lock)
    except (OSError, WheelLockError) as error:
        print(f"ERROR: {redact_text(str(error))}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
