#!/usr/bin/env python3
"""Analiza informes de seguridad sin afirmar vulnerabilidades no verificadas."""

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CVE_PATTERN = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.IGNORECASE)


def analyze_report(text):
    """Mantiene la compatibilidad con el análisis de texto existente."""
    cves = sorted(set(cve.upper() for cve in CVE_PATTERN.findall(text)))

    if cves:
        classification = "known_reference"
        message = "Se encontraron referencias CVE; verificar su relación con el hallazgo."
    else:
        classification = "pending_validation"
        message = (
            "No se encontraron referencias CVE. Esto no demuestra que sea "
            "una vulnerabilidad nueva."
        )

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "classification": classification,
        "cve_references": cves,
        "patch_status": "unverified",
        "confirmed_vulnerability": False,
        "requires_manual_validation": True,
        "message": message,
        "source_text": text[:20000],
    }



def get_finding_guidance(template_id, matcher_name, name):
    """Genera orientación defensiva específica según el hallazgo."""
    template = template_id.lower()
    matcher = matcher_name.lower()

    if "http-missing-security-headers" in template:
        guidance = {
            "permissions-policy": {
                "description": "No se detectó el encabezado HTTP Permissions-Policy.",
                "potential_risk": (
                    "Podrían no existir restricciones explícitas para ciertas "
                    "funciones del navegador, según el comportamiento de la aplicación."
                ),
                "manual_validation": (
                    "Consultar las cabeceras HTTP y comprobar qué funciones del "
                    "navegador utiliza realmente la aplicación."
                ),
                "recommendation": (
                    "Definir una Permissions-Policy que permita únicamente las "
                    "funciones necesarias. Probar su compatibilidad antes de desplegarla."
                ),
            },
            "cross-origin-embedder-policy": {
                "description": "No se detectó el encabezado Cross-Origin-Embedder-Policy (COEP).",
                "potential_risk": (
                    "Si la aplicación necesita aislamiento entre orígenes, su ausencia "
                    "podría impedir obtener las protecciones o capacidades esperadas."
                ),
                "manual_validation": (
                    "Comprobar si la aplicación necesita aislamiento de origen "
                    "y revisar la carga de recursos de terceros."
                ),
                "recommendation": (
                    "Si el aislamiento es necesario, evaluar una política COEP "
                    "adecuada y verificar la compatibilidad de todos los recursos externos."
                ),
            },
            "cross-origin-opener-policy": {
                "description": "No se detectó el encabezado Cross-Origin-Opener-Policy (COOP).",
                "potential_risk": (
                    "Podría faltar aislamiento entre contextos de navegación "
                    "que se comunican mediante ventanas o pestañas."
                ),
                "manual_validation": (
                    "Revisar la interacción con ventanas emergentes, pestañas "
                    "externas y las necesidades de aislamiento de la aplicación."
                ),
                "recommendation": (
                    "Evaluar una política COOP apropiada para la aplicación. "
                    "Probar los flujos de autenticación, ventanas emergentes e integraciones."
                ),
            },
            "cross-origin-resource-policy": {
                "description": "No se detectó el encabezado Cross-Origin-Resource-Policy (CORP).",
                "potential_risk": (
                    "Los recursos podrían carecer de una política explícita "
                    "que controle su carga desde otros orígenes."
                ),
                "manual_validation": (
                    "Identificar los recursos públicos y privados y comprobar "
                    "qué sitios necesitan cargarlos legítimamente."
                ),
                "recommendation": (
                    "Definir una política CORP según las necesidades de acceso "
                    "a los recursos y probar las integraciones legítimas."
                ),
            },
        }

        if matcher in guidance:
            return guidance[matcher]

        return {
            "description": f"No se detectó el encabezado HTTP {matcher_name}.",
            "potential_risk": (
                "La ausencia podría reducir una protección del navegador. "
                "El impacto depende del encabezado y de la aplicación."
            ),
            "manual_validation": (
                "Consultar las cabeceras HTTP en varias rutas y confirmar "
                "que la ausencia sea consistente."
            ),
            "recommendation": (
                "Investigar la finalidad del encabezado y configurar un valor "
                "adecuado si corresponde."
            ),
        }

    return {
        "description": (
            f"Nuclei registró una coincidencia para {name} "
            f"(plantilla: {template_id})."
        ),
        "potential_risk": (
            "El impacto no puede determinarse únicamente con esta coincidencia."
        ),
        "manual_validation": (
            "Revisar la evidencia original y confirmar que el resultado "
            "corresponde al comportamiento real del sistema."
        ),
        "recommendation": (
            "Investigar la causa y aplicar una corrección únicamente "
            "si se confirma una debilidad."
        ),
    }


def analyze_scan(data):
    """Resume los hallazgos y conserva el detalle de cada observación."""
    findings = data.get("findings", []) if isinstance(data, dict) else []
    if not isinstance(findings, list):
        findings = []

    grouped = {}
    severities = Counter()
    cves = set()

    for finding in findings:
        if not isinstance(finding, dict):
            continue

        info = finding.get("info", {})
        if not isinstance(info, dict):
            info = {}

        template_id = str(finding.get("template-id", "unknown"))
        matcher_name = str(finding.get("matcher-name", "unspecified"))
        severity = str(info.get("severity", "unknown")).lower()

        severities[severity] += 1
        cves.update(
            cve.upper()
            for cve in CVE_PATTERN.findall(json.dumps(finding))
        )

        # Cada comprobación específica conserva su propio registro.
        group_key = (template_id, matcher_name)

        if group_key not in grouped:
            grouped[group_key] = {
                "template_id": template_id,
                "matcher_name": matcher_name,
                "name": info.get("name", template_id),
                "severity": severity,
                "count": 0,
                "matched_urls": [],
                **get_finding_guidance(template_id, matcher_name, info.get("name", template_id)),
            }

        item = grouped[group_key]
        item["count"] += 1

        url = finding.get("matched-at") or finding.get("url")
        if url and url not in item["matched_urls"]:
            item["matched_urls"].append(url)

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target": data.get("target") if isinstance(data, dict) else None,
        "scan_status": data.get("status") if isinstance(data, dict) else None,
        "raw_findings_count": len(findings),
        "grouped_findings_count": len(grouped),
        "severity_counts": dict(severities),
        "cve_references": sorted(cves),
        "confirmed_vulnerability": False,
        "findings": list(grouped.values()),
        "requires_manual_validation": True,
    }


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 report_analyzer.py <archivo_informe>")
        return 2

    source = Path(sys.argv[1])
    if not source.is_file():
        print(f"Error: no existe el archivo: {source}", file=sys.stderr)
        return 2

    try:
        raw = source.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Error al leer el informe JSON: {exc}", file=sys.stderr)
        return 2

    result = analyze_scan(data)
    output = Path("reports") / f"{source.stem}_analysis.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nInforme guardado en: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
