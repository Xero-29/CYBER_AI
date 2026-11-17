"""Gestión de informes analizados y detección básica de duplicados."""

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


REPORTS_DIR = Path("reports")
DATA_DIR = Path("data")
INDEX_FILE = DATA_DIR / "report_index.json"


def fingerprint(text):
    """Calcula una huella estable del texto para detectar duplicados exactos."""
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def load_index():
    """Carga el índice; ante corrupción falla de forma segura y no lo reinicia."""
    if not INDEX_FILE.exists():
        return {}
    try:
        data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"El índice de informes no se puede leer; se conserva sin modificar: {INDEX_FILE}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(f"Formato inválido en el índice de informes: {INDEX_FILE}")
    return data


def _write_index_atomic(index):
    """Reemplaza el índice de forma atómica para evitar archivos parciales."""
    serialized = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{INDEX_FILE.name}.", suffix=".tmp", dir=INDEX_FILE.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temporary:
            temporary.write(serialized)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, INDEX_FILE)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def register_report(source_text, output_path):
    """Registra un informe y señala duplicados de texto exacto."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

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
