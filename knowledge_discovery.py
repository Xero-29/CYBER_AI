#!/usr/bin/env python3
"""Descubrimiento e inventario seguro de recursos de CYBER_AI."""

import hashlib
from pathlib import Path

import knowledge_registry as registry


SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".json": "json",
    ".csv": "csv",
    ".txt": "text",
    ".md": "markdown",
    ".html": "html",
    ".htm": "html",
    ".xml": "xml",
    ".yaml": "yaml",
    ".yml": "yaml",
}

CHUNK_SIZE = 1024 * 1024


def detect_resource_type(path):
    """Identifica el formato por extensión."""
    name = path.name.lower()

    if name.endswith(".csv.gz"):
        return "csv_gz"

    return SUPPORTED_EXTENSIONS.get(path.suffix.lower())


def calculate_sha256(path, chunk_size=CHUNK_SIZE):
    """Calcula SHA-256 leyendo el archivo por bloques."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while True:
            block = file.read(chunk_size)
            if not block:
                break
            digest.update(block)

    return digest.hexdigest()


def discover_resources(roots, *, area_id=None):
    """
    Recorre las raíces indicadas e inventaría archivos compatibles.
    No modifica los archivos originales ni los ingiere.
    """
    results = {
        "discovered": 0,
        "new": 0,
        "modified": 0,
        "unchanged": 0,
        "skipped": 0,
        "errors": [],
        "resources": [],
    }

    registry.initialize()

    for root_value in roots:
        root = Path(root_value).expanduser().resolve()

        if not root.exists() or not root.is_dir():
            results["errors"].append({
                "path": str(root),
                "error": "La carpeta no existe o no es accesible.",
            })
            continue

        for path in sorted(root.rglob("*")):
            try:
                if path.is_symlink() or not path.is_file():
                    continue

                resource_type = detect_resource_type(path)

                if resource_type is None:
                    results["skipped"] += 1
                    continue

                before = path.stat()
                sha256 = calculate_sha256(path)
                after = path.stat()

                # Evita registrar archivos modificados durante la lectura.
                if (
                    before.st_size != after.st_size
                    or before.st_mtime_ns != after.st_mtime_ns
                ):
                    results["errors"].append({
                        "path": str(path),
                        "error": "El archivo cambió durante el análisis.",
                    })
                    continue

                registration = registry.register_resource(
                    path,
                    sha256=sha256,
                    file_size=after.st_size,
                    resource_type=resource_type,
                    title=path.stem,
                    modified_at=after.st_mtime,
                )

                # Asocia el recurso con el área indicada, sin alterar
                # versiones ni datos de los fragmentos.
                if area_id:
                    with registry.connect() as db:
                        db.execute("""
                            UPDATE knowledge_resources
                            SET area_id = ?
                            WHERE resource_id = ?
                        """, (area_id, registration["resource_id"]))

                status = registration["status"]
                results[status] += 1
                results["discovered"] += 1

                results["resources"].append({
                    "path": str(path),
                    "type": resource_type,
                    "size": after.st_size,
                    "sha256": sha256,
                    "status": status,
                    "version_id": registration["version_id"],
                })

            except (OSError, ValueError) as error:
                results["errors"].append({
                    "path": str(path),
                    "error": str(error),
                })

    return results
