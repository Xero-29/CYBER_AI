#!/usr/bin/env python3
"""Audita procedencia, licencias y obsolescencia del catálogo de conocimiento.

No descarga ni considera confiable una fuente por el mero hecho de estar catalogada.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
DEFAULT_CATALOG = ROOT / "data/knowledge_sources/knowledge_catalog.json"
LICENSE_STATES = {"pending", "approved", "denied", "restricted"}


def _date(value, field, resource_id, issues):
    if not isinstance(value, str) or not value.strip():
        issues.append({"resource": resource_id, "severity": "pending",
                       "code": f"missing_{field}", "detail": f"Falta {field}."})
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        issues.append({"resource": resource_id, "severity": "error",
                       "code": f"invalid_{field}", "detail": f"{field} no es ISO-8601."})
        return None
    if parsed.tzinfo is None:
        issues.append({"resource": resource_id, "severity": "error",
                       "code": f"naive_{field}", "detail": f"{field} debe incluir zona horaria."})
        return None
    return parsed.astimezone(timezone.utc)


def audit_catalog(catalog, *, now=None, require_reviewed=False):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now debe incluir zona horaria.")
    issues = []
    resources = catalog.get("resources")
    if not isinstance(resources, list):
        return {"status": "invalid", "resources": 0, "reviewed": 0,
                "pending": 0, "stale": 0, "errors": 1,
                "issues": [{"severity": "error", "code": "invalid_resources",
                            "detail": "resources debe ser una lista."}]}

    ids = set()
    reviewed = pending = stale = errors = 0
    for item in resources:
        if not isinstance(item, dict):
            errors += 1
            issues.append({"severity": "error", "code": "invalid_resource",
                           "detail": "Cada recurso debe ser un objeto."})
            continue
        rid = item.get("id")
        if not isinstance(rid, str) or not rid.strip():
            errors += 1
            issues.append({"severity": "error", "code": "missing_id",
                           "detail": "Recurso sin identificador."})
            rid = "<sin-id>"
        elif rid in ids:
            errors += 1
            issues.append({"resource": rid, "severity": "error",
                           "code": "duplicate_id", "detail": "ID duplicado."})
        ids.add(rid)

        url = item.get("url")
        parsed = urlsplit(url) if isinstance(url, str) else None
        if not parsed or parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            errors += 1
            issues.append({"resource": rid, "severity": "error",
                           "code": "invalid_url", "detail": "La fuente debe usar HTTPS y no incluir credenciales."})
        publisher = item.get("publisher")
        if not isinstance(publisher, str) or not publisher.strip():
            pending += 1
            issues.append({"resource": rid, "severity": "pending",
                           "code": "missing_publisher", "detail": "Falta editor o dominio responsable."})
        elif parsed and parsed.hostname and publisher.lower().removeprefix("www.") != parsed.hostname.lower().removeprefix("www."):
            pending += 1
            issues.append({"resource": rid, "severity": "pending",
                           "code": "publisher_host_mismatch", "detail": "El editor declarado no coincide con el host; requiere revisión."})

        license_state = item.get("license_status", "pending")
        if license_state not in LICENSE_STATES:
            errors += 1
            issues.append({"resource": rid, "severity": "error",
                           "code": "invalid_license_state", "detail": "Estado de licencia desconocido."})
        elif license_state != "approved":
            pending += 1
            issues.append({"resource": rid, "severity": "pending",
                           "code": "license_not_approved",
                           "detail": "La licencia no está aprobada para uso/redistribución."})
        elif not item.get("license_evidence"):
            pending += 1
            issues.append({"resource": rid, "severity": "pending",
                           "code": "missing_license_evidence",
                           "detail": "Falta evidencia verificable de la aprobación de licencia."})
        if item.get("verified_for_download") is True:
            if license_state != "approved" or not item.get("license_evidence"):
                errors += 1
                issues.append({"resource": rid, "severity": "error",
                               "code": "unsafe_download_gate",
                               "detail": "Una fuente descargable requiere licencia aprobada y evidencia."})

        reviewed_at = _date(item.get("last_reviewed_at"), "last_reviewed_at", rid, issues)
        interval = item.get("review_interval_days")
        if isinstance(interval, bool) or not isinstance(interval, int) or not 1 <= interval <= 3650:
            issues.append({"resource": rid, "severity": "pending",
                           "code": "missing_review_interval",
                           "detail": "Falta un intervalo de revisión válido (1–3650 días)."})
            pending += 1
            interval = None
        if reviewed_at and interval:
            if reviewed_at > now:
                errors += 1
                issues.append({"resource": rid, "severity": "error",
                               "code": "future_review", "detail": "La fecha de revisión está en el futuro."})
            elif (now - reviewed_at).days > interval:
                stale += 1
                issues.append({"resource": rid, "severity": "stale",
                               "code": "review_expired", "detail": "La revisión de la fuente está vencida."})
            elif license_state == "approved":
                reviewed += 1
        elif license_state == "approved":
            pending += 1

        if item.get("download") is True and item.get("verified_for_download") is not True:
            errors += 1
            issues.append({"resource": rid, "severity": "error",
                           "code": "download_without_verification",
                           "detail": "download=true requiere verified_for_download=true."})

    if require_reviewed and (pending or stale):
        issues.append({"severity": "error", "code": "review_gate",
                       "detail": "El modo estricto exige fuentes revisadas y vigentes."})
    # Todas las rutas de validación, incluidas fechas inválidas, se contabilizan.
    errors = sum(issue.get("severity") == "error" for issue in issues)
    status = "invalid" if errors else ("needs_review" if pending or stale else "ready")
    return {"status": status, "resources": len(resources), "reviewed": reviewed,
            "pending": pending, "stale": stale, "errors": errors, "issues": issues}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--require-reviewed", action="store_true",
                        help="Falla si hay fuentes pendientes o revisiones vencidas.")
    parser.add_argument("--json", action="store_true", help="Imprime el informe como JSON.")
    args = parser.parse_args(argv)
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        report = audit_catalog(catalog, require_reviewed=args.require_reviewed)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Auditoría de procedencia del conocimiento")
        print("Estado: {status} | fuentes: {resources} | revisadas: {reviewed} | pendientes: {pending} | vencidas: {stale} | errores: {errors}".format(**report))
        for issue in report["issues"]:
            print("[{level}] {resource}: {code} — {detail}".format(
                level=issue["severity"].upper(),
                resource=issue.get("resource", "CATÁLOGO"),
                code=issue["code"], detail=issue["detail"]))
    return 1 if report["errors"] else (2 if args.require_reviewed and report["status"] != "ready" else 0)


if __name__ == "__main__":
    raise SystemExit(main())
