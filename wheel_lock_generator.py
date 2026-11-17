#!/usr/bin/env python3
"""Generate a deterministic, hash-enforced lock from a downloaded wheelhouse."""
import argparse
import hashlib
from email.parser import Parser
import re
import sys
import zipfile
from pathlib import Path


class WheelLockError(ValueError):
    pass


def normalize_name(value):
    return re.sub(r"[-_.]+", "-", value).lower()


def wheel_metadata(path):
    try:
        with zipfile.ZipFile(path) as archive:
            metadata_files = [
                name for name in archive.namelist()
                if name.endswith(".dist-info/METADATA")
            ]
            if len(metadata_files) != 1:
                raise WheelLockError(f"Wheel sin METADATA único: {path.name}.")
            metadata = Parser().parsestr(
                archive.read(metadata_files[0]).decode("utf-8")
            )
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError) as error:
        raise WheelLockError(f"Wheel inválido: {path.name}.") from error
    name, version = metadata.get("Name"), metadata.get("Version")
    if not name or not version:
        raise WheelLockError(f"Wheel sin nombre o versión: {path.name}.")
    return normalize_name(name), version


def read_expected(path):
    expected = {}
    for number, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(
            r"([A-Za-z0-9][A-Za-z0-9._-]*)==([A-Za-z0-9][A-Za-z0-9.!+_-]*)",
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
    wheels = sorted(wheelhouse.glob("*.whl"))
    if not wheels:
        raise WheelLockError("Wheelhouse vacío.")
    for wheel in wheels:
        name, version = wheel_metadata(wheel)
        digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
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
            Path(args.output).write_text(lock, encoding="utf-8")
        else:
            sys.stdout.write(lock)
    except (OSError, WheelLockError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
