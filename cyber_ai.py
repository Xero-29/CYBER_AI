#!/usr/bin/env python3
"""Entrada principal de CYBER_AI."""

import argparse
import json
import sys
import subprocess
import uuid
from pathlib import Path

from report_analyzer import analyze_report, analyze_scan
from nvd_client import enrich_analysis
from report_manager import register_report
from batch_analyzer import process_directory
from nuclei_scanner import scan_target


def process_one(filename):
    """Analiza un informe individual y guarda el resultado."""
    source = Path(filename)
    if not source.is_file():
        print(f"No existe el informe: {source}", file=sys.stderr)
        return 2

    try:
        text = source.read_text(encoding="utf-8")
        result = enrich_analysis(analyze_report(text))
        output_dir = Path("reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / f"{source.stem}_analysis.json"

        duplicate = register_report(text, output)
        result["duplicate_check"] = duplicate
        if duplicate["duplicate"]:
            result["classification"] = "possible_duplicate"

        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Resultado: {output}")
        print(f"Clasificación: {result['classification']}")
        print(f"Referencias CVE: {len(result['cve_references'])}")
        print(f"Duplicado exacto: {'sí' if duplicate['duplicate'] else 'no'}")
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2



def print_scan_summary(summary):
    """Muestra un resumen legible de los hallazgos de Nuclei."""
    print("\\n========== RESUMEN DE SEGURIDAD ==========")
    print(f"Objetivo: {summary.get('target') or 'No disponible'}")
    print(f"Estado: {summary.get('scan_status') or 'Desconocido'}")
    print(f"Hallazgos: {summary.get('raw_findings_count', 0)}")
    print(f"Grupos: {summary.get('grouped_findings_count', 0)}")

    print("\\n--- SEVERIDADES ---")
    severities = summary.get("severity_counts", {})
    if severities:
        for severity, count in sorted(severities.items()):
            print(f"{severity.upper()}: {count}")
    else:
        print("No se registraron hallazgos.")

    print("\\n--- DETALLE DE HALLAZGOS ---")
    findings = summary.get("findings", [])

    if not findings:
        print("No hay hallazgos registrados.")
    else:
        for index, finding in enumerate(findings, 1):
            print(f"\\n{index}. {finding.get('name', 'Sin nombre')}")
            print(f"   Severidad: {finding.get('severity', 'unknown').upper()}")
            print(f"   Plantilla: {finding.get('template_id', 'unknown')}")
            print(f"   Comprobación: {finding.get('matcher_name', 'unspecified')}")
            print(f"   Coincidencias: {finding.get('count', 0)}")

            for url in finding.get("matched_urls", []):
                print(f"   Ubicación: {url}")

            print(f"   Descripción: {finding.get('description', 'No disponible')}")
            print(f"   Riesgo potencial: {finding.get('potential_risk', 'No evaluado')}")
            print(f"   Verificación manual: {finding.get('manual_validation', 'No disponible')}")
            print(f"   Recomendación: {finding.get('recommendation', 'No disponible')}")

    print("\\n--- VALIDACIÓN ---")
    if summary.get("requires_manual_validation", True):
        print("Los hallazgos requieren validación manual.")
    print("Ninguna vulnerabilidad se declara confirmada automáticamente.")
    print("==========================================\\n")


def main():
    parser = argparse.ArgumentParser(description="CYBER_AI: análisis de informes de seguridad.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--report", help="Analizar un archivo TXT o Markdown.")
    group.add_argument("--batch", help="Analizar todos los TXT y Markdown de una carpeta.")
    group.add_argument("--self-test", action="store_true", help="Comprobar archivos básicos.")
    group.add_argument("--scan", help="Escanear una URL HTTP/HTTPS autorizada con Nuclei.")
    parser.add_argument("--confirm-authorized", action="store_true", help="Confirmar que tienes autorización para analizar el objetivo indicado en --scan.")
    args = parser.parse_args()

    if args.scan:
        try:
            result = scan_target(args.scan, authorized=args.confirm_authorized)
            output_dir = Path("reports")
            output_dir.mkdir(parents=True, exist_ok=True)

            # Guardamos el resultado completo de Nuclei sin perder evidencias.
            scan_id = uuid.uuid4().hex
            output = output_dir / f"nuclei_scan_{scan_id}_analysis.json"
            output.write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            # Generamos un segundo informe agrupado por plantilla y severidad.
            summary = analyze_scan(result)
            summary_output = output_dir / f"nuclei_scan_{scan_id}_summary.json"
            summary_output.write_text(
                json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            print(f"Informe completo: {output}")
            print(f"Resumen analizado: {summary_output}")
            print_scan_summary(summary)
            return 0 if result.get("status") == "completed" else 1
        except ValueError as exc:
            print(f"Objetivo inválido: {exc}", file=sys.stderr)
            return 2

    if args.self_test:
        required = [
            "report_analyzer.py", "nvd_client.py", "report_manager.py",
            "batch_analyzer.py", "nuclei_scanner.py", "CONTEXT.md",
        ]
        missing = [name for name in required if not Path(name).is_file()]
        if missing:
            print("Faltan archivos: " + ", ".join(missing))
            return 1
        tests_dir = Path("tests")
        if not tests_dir.is_dir():
            print("No existe el directorio tests/.")
            return 1
        print("Ejecutando pruebas unitarias...")
        return subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(tests_dir), "-v"],
            check=False,
        ).returncode

    if args.report:
        return process_one(args.report)

    if args.batch:
        try:
            results = process_directory(args.batch)
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return 1 if any("error" in item for item in results) else 0
        except (OSError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
