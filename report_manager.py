"""Gestión de informes analizados y detección básica de duplicados."""

import hashlib
import json
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
    """Carga el índice local o crea uno vacío si aún no existe."""
    if not INDEX_FILE.exists():
        return {}
    try:
        data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


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
        INDEX_FILE.write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return result
