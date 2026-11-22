"""Gestión de informes analizados y detección básica de duplicados."""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from safe_io import SafeWriteError, atomic_write_text, ensure_private_directory, open_private_file
from secret_redaction import redact_sensitive_data


REPORTS_DIR = Path("reports")
DATA_DIR = Path("data")
INDEX_FILE = DATA_DIR / "report_index.json"


def fingerprint(text):
    """Calcula una huella estable del texto para detectar duplicados exactos."""
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def load_index():
    """Carga el índice; ante corrupción falla de forma segura y no lo reinicia."""
    try:
        ensure_private_directory(DATA_DIR, create=True)
        if not INDEX_FILE.exists() and not INDEX_FILE.is_symlink():
            return {}
        with open_private_file(INDEX_FILE, "r") as stream:
            data = json.load(stream)
    except (OSError, SafeWriteError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"El índice de informes no se puede leer; se conserva sin modificar: {INDEX_FILE}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(f"Formato inválido en el índice de informes: {INDEX_FILE}")
    return data


def _write_index_atomic(index):
    """Reemplaza el índice con permisos privados y publicación atómica."""
    serialized = json.dumps(
        redact_sensitive_data(index), ensure_ascii=False, indent=2
    ) + "\n"
    atomic_write_text(
        INDEX_FILE, serialized, mode=0o600, create_parents=True
    )


def register_report(source_text, output_path):
    """Registra un informe y señala duplicados de texto exacto."""
    ensure_private_directory(REPORTS_DIR, create=True)
    ensure_private_directory(DATA_DIR, create=True)

    digest = fingerprint(source_text)
    index = load_index()
    previous = index.get(digest)

    result = {
        "fingerprint": digest,
        "duplicate": previous is not None,
        "previous_report": previous,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }

    if previous is None:
        index[digest] = str(output_path)
        _write_index_atomic(index)

    return result
