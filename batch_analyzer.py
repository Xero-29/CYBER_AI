"""Procesa varios informes de texto y genera análisis individuales."""

import hashlib
import json
from pathlib import Path

from report_analyzer import analyze_report
from nvd_client import enrich_analysis
from report_manager import register_report


def process_file(source):
    """Analiza un archivo y guarda su resultado en reports/."""
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(f"No existe el informe: {source}")

    text = source.read_text(encoding="utf-8")
    result = enrich_analysis(analyze_report(text))

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    source_identity = str(source.resolve()).encode("utf-8")
    source_suffix = hashlib.sha256(source_identity).hexdigest()[:12]
    output = output_dir / f"{source.stem}_{source_suffix}_analysis.json"

    duplicate = register_report(text, output)
    result["duplicate_check"] = duplicate

    if duplicate["duplicate"]:
        result["classification"] = "possible_duplicate"

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "source": str(source),
        "output": str(output),
        "classification": result["classification"],
        "duplicate": duplicate["duplicate"],
    }


def process_directory(directory):
    """Procesa archivos TXT y Markdown sin volver a leer análisis JSON."""
    folder = Path(directory)
    if not folder.is_dir():
        raise NotADirectoryError(f"No existe la carpeta: {folder}")

    files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in {".txt", ".md"}
        and not p.name.endswith("_analysis.txt")
    )

    results = []
    for source in files:
        try:
            results.append(process_file(source))
        except (OSError, UnicodeError, ValueError) as exc:
            results.append({
                "source": str(source),
                "error": str(exc),
            })

    return results
