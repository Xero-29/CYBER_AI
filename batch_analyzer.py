"""Procesa varios informes de texto y genera análisis individuales."""

import hashlib
import json
from pathlib import Path

from report_analyzer import analyze_report
from nvd_client import enrich_analysis
from report_manager import register_report
from safe_io import atomic_write_text, ensure_private_directory, is_real_directory, read_regular_text
from secret_redaction import redact_sensitive_data, redact_text


def process_file(source):
    """Analiza un archivo y guarda su resultado en reports/."""
    source = Path(source)
    text = read_regular_text(source)
    result = enrich_analysis(analyze_report(text))

    output_dir = ensure_private_directory(Path("reports"), create=True)
    source_identity = str(source.resolve()).encode("utf-8")
    source_suffix = hashlib.sha256(source_identity).hexdigest()[:12]
    output = output_dir / f"{source.stem}_{source_suffix}_analysis.json"

    duplicate = register_report(text, output)
    result["duplicate_check"] = duplicate

    if duplicate["duplicate"]:
        result["classification"] = "possible_duplicate"

    atomic_write_text(
        output,
        json.dumps(redact_sensitive_data(result), ensure_ascii=False, indent=2) + "\n",
        mode=0o600,
        create_parents=True,
    )
    return redact_sensitive_data({
        "source": str(source),
        "output": str(output),
        "classification": result["classification"],
        "duplicate": duplicate["duplicate"],
    })


def process_directory(directory):
    """Procesa archivos TXT y Markdown sin volver a leer análisis JSON."""
    folder = Path(directory)
    if not is_real_directory(folder):
        raise NotADirectoryError("La carpeta de informes debe ser un directorio real sin enlaces.")

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
                "error": redact_text(str(exc)),
            })

    return results
