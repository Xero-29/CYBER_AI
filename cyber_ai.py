#!/usr/bin/env python3
"""Entrada principal de CYBER_AI."""

import argparse
import hashlib
import json
import os
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
    group.add_argument("--ask", help="Enviar una tarea al flujo integrado de agentes.")
    group.add_argument("--team", help="Enviar una tarea al flujo multiagente supervisado.")
    group.add_argument("--report", help="Analizar un archivo TXT o Markdown.")
    group.add_argument("--batch", help="Analizar todos los TXT y Markdown de una carpeta.")
    group.add_argument("--self-test", action="store_true", help="Comprobar archivos básicos.")
    group.add_argument("--scan", help="Escanear una URL HTTP/HTTPS autorizada con Nuclei.")
    parser.add_argument("--agent", help="Especialista opcional para --ask.")
    parser.add_argument("--workflow", help="Flujo de config/workflows.json para --team.")
    parser.add_argument("--execute-tools", action="store_true", help="Ejecutar adaptadores locales planificados.")
    parser.add_argument("--confirm-tool-execution", action="store_true", help="Confirmación explícita para ejecutar adaptadores.")
    parser.add_argument("--tool-target", help="Ruta del archivo o directorio que se analizará.")
    parser.add_argument("--allow-external-targets", action="store_true", help="Permitir objetivos externos; requiere perfil extended y confirmación.")
    parser.add_argument("--tool-profile", help="Perfil de ejecución: standard, extended o restricted.")
    parser.add_argument("--no-knowledge", action="store_true", help="Desactivar recuperación de conocimiento en --ask.")
    parser.add_argument("--confirm-authorized", action="store_true", help="Confirmación adicional del operador.")
    parser.add_argument("--authorization-id", help="ID de autorización local, vigente y limitada al destino.")
    parser.add_argument("--nuclei-templates", help="Directorio local de plantillas HTTP de Nuclei.")
    parser.add_argument("--scan-severity", default="info,low,medium,high,critical", help="Severidades Nuclei separadas por coma.")
    parser.add_argument("--scan-timeout", type=int, default=300, help="Tiempo máximo del escaneo Nuclei (5-3600 s).")
    parser.add_argument("--scan-rate-limit", type=int, default=2, help="Máximo de solicitudes Nuclei por segundo (1-20).")
    parser.add_argument("--scan-concurrency", type=int, default=2, help="Concurrencia Nuclei (1-10).")
    args = parser.parse_args()

    if args.team:
        if args.tool_profile:
            if not args.execute_tools:
                parser.error("--tool-profile requiere --execute-tools.")
            if not __import__("re").fullmatch(r"[a-z0-9_-]{1,48}", args.tool_profile):
                parser.error("Nombre de perfil inválido.")
            os.environ["CYBER_AI_TOOL_PROFILE"] = args.tool_profile
        if args.agent or args.no_knowledge:
            parser.error("--agent y --no-knowledge no se aplican al flujo --team.")
        if args.execute_tools and (
            not args.confirm_tool_execution or not args.tool_target
        ):
            parser.error("--execute-tools requiere --confirm-tool-execution y --tool-target.")
        if not args.execute_tools and (
            args.confirm_tool_execution or args.tool_target or args.allow_external_targets
        ):
            parser.error("--confirm-tool-execution y --tool-target requieren --execute-tools.")
        command = [
            sys.executable,
            str(Path(__file__).resolve().parent / "team_orchestrator.py"),
            "--supervise-objectives",
        ]
        if args.workflow:
            command.extend(["--workflow", args.workflow])
        if args.execute_tools:
            command.extend([
                "--execute-tools", "--confirm-tool-execution",
                "--tool-target", args.tool_target,
            ])
            if args.allow_external_targets:
                command.append("--allow-external-targets")
        command.append(args.team)
        result = subprocess.run(command, cwd=Path(__file__).resolve().parent, check=False)
        return result.returncode

    if args.workflow or args.execute_tools or args.confirm_tool_execution or args.tool_target or args.allow_external_targets or args.tool_profile:
        parser.error("--workflow y las opciones de ejecución solo pueden utilizarse junto con --team.")

    if args.ask:
        command = [sys.executable, str(Path(__file__).resolve().parent / "director.py"), args.ask]
        if args.agent:
            command.extend(["--agent", args.agent])
        if args.no_knowledge:
            command.append("--no-knowledge")
        # La ruta principal consulta conocimiento por defecto; DIRECTOR permite
        # desactivarlo explícitamente cuando no haya embeddings configurados.
        result = subprocess.run(command, cwd=Path(__file__).resolve().parent, check=False)
        return result.returncode

    if args.agent or args.no_knowledge:
        parser.error("--agent y --no-knowledge solo pueden utilizarse junto con --ask.")

    if args.scan:
        try:
            result = scan_target(
                args.scan,
                timeout=args.scan_timeout,
                authorized=args.confirm_authorized,
                authorization_id=args.authorization_id,
                require_ledger=True,
                templates_path=args.nuclei_templates,
                severity=args.scan_severity,
                rate_limit=args.scan_rate_limit,
                concurrency=args.scan_concurrency,
            )
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

    if (args.nuclei_templates or args.authorization_id or args.confirm_authorized
            or args.scan_severity != "info,low,medium,high,critical"
            or args.scan_timeout != 300 or args.scan_rate_limit != 2
            or args.scan_concurrency != 2) and not args.scan:
        parser.error("Las opciones de Nuclei requieren --scan.")
 
    if args.self_test:
        required = [
            "report_analyzer.py", "nvd_client.py", "report_manager.py",
            "batch_analyzer.py", "nuclei_scanner.py", "isolated_tool_runner.py", "director.py",
            "agent_runner.py", "CONTEXT.md",
        ]
        missing = [name for name in required if not Path(name).is_file()]
        if missing:
            print("Faltan archivos: " + ", ".join(missing))
            return 1
        print("Comprobación básica correcta.")
        print("Para ejecutar la suite completa usa: python -m unittest discover -s tests -v")
        return 0

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
