#!/usr/bin/env python3
"""Auditoría conservadora de madurez, fuentes, laboratorios y revisión de los packs offline."""

import argparse
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "knowledge" / "packs" / "manifest.json"
SHA256_RE = re.compile(r"[a-fA-F0-9]{64}\Z")
COMMIT_RE = re.compile(r"[a-fA-F0-9]{40}\Z")

REQUIRED_SECTIONS = {
    "scope": ("propósito y límites",),
    "foundations": ("fundamentos", "modelo de sistema y conceptos", "principios"),
    "architecture": ("arquitectura",),
    "threat_model": (
        "modelo de amenazas", "análisis de amenazas", "amenazas y escenarios",
        "superficie de ataque",
    ),
    "competencies": ("competencias",),
    "technical_methods": (
        "mecanismos técnicos", "métodos técnicos", "métodos y algoritmos",
        "algoritmos y protocolos", "protocolos y estándares",
    ),
    "controls": ("controles",),
    "methodology": ("metodología",),
    "worked_examples": (
        "ejemplos desarrollados", "ejemplos reproducibles", "casos de estudio",
    ),
    "lab": ("laboratorio",),
    "reproducibility": (
        "reproducibilidad", "validación técnica", "pruebas y métricas",
    ),
    "evaluation": ("evaluación", "criterios de evaluación"),
    "sources": (
        "fuentes verificables", "referencias verificables", "referencias trazables",
    ),
    "agent_safety": ("instrucciones para agentes ia",),
}


def _normalize(value):
    normalized = unicodedata.normalize("NFKD", str(value).lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _resolve_repo_file(root, value):
    """Resolve a repository-relative file while rejecting traversal and symlinks."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("La ruta debe ser un texto POSIX relativo.")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("La ruta absoluta o con traversal está prohibida.")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("No se permiten symlinks en rutas de calidad.")
    resolved = current.resolve(strict=True)
    resolved.relative_to(root)
    if not resolved.is_file():
        raise ValueError("La ruta de calidad debe ser un archivo regular.")
    return resolved


def _aware_timestamp(value):
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _load_json(root, relative):
    if not relative:
        return None
    try:
        path = _resolve_repo_file(root, relative)
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return None


def _source_is_verified(source):
    if not isinstance(source, dict):
        return False
    try:
        parsed = urlsplit(source.get("url", ""))
    except (TypeError, ValueError):
        return False
    return all((
        isinstance(source.get("id"), str) and bool(source["id"].strip()),
        isinstance(source.get("title"), str) and bool(source["title"].strip()),
        isinstance(source.get("publisher"), str) and bool(source["publisher"].strip()),
        parsed.scheme == "https" and bool(parsed.hostname),
        isinstance(source.get("version"), str) and bool(source["version"].strip()),
        isinstance(source.get("license"), str) and bool(source["license"].strip()),
        source.get("license_status") == "approved",
        _aware_timestamp(source.get("verified_at")),
        isinstance(source.get("verification_evidence"), str)
        and bool(source["verification_evidence"].strip()),
    ))


def _valid_source_registry(value):
    if not isinstance(value, dict) or not isinstance(value.get("sources"), list):
        return 0
    sources = value["sources"]
    if not all(isinstance(source, dict) for source in sources):
        return 0
    ids = [source.get("id") for source in sources]
    if not all(isinstance(value, str) and value.strip() for value in ids):
        return 0
    if len(ids) != len(set(ids)):
        return 0
    return sum(_source_is_verified(source) for source in sources)


def _valid_lab_evidence(value):
    if not isinstance(value, dict) or not isinstance(value.get("runs"), list):
        return False
    for run in value["runs"]:
        if not isinstance(run, dict):
            continue
        if (
            run.get("status") == "passed"
            and isinstance(run.get("artifact_sha256"), str)
            and SHA256_RE.fullmatch(run["artifact_sha256"])
            and _aware_timestamp(run.get("executed_at"))
            and isinstance(run.get("environment"), str)
            and run["environment"].strip()
            and isinstance(run.get("command"), str)
            and run["command"].strip()
            and isinstance(run.get("scope"), str)
            and run["scope"].strip()
        ):
            return True
    return False


def _valid_review_record(value):
    if not isinstance(value, dict):
        return False
    return all((
        value.get("decision") == "approved",
        value.get("independent_review") is True,
        isinstance(value.get("reviewer_id"), str) and bool(value["reviewer_id"].strip()),
        _aware_timestamp(value.get("reviewed_at")),
        isinstance(value.get("reviewed_commit"), str)
        and COMMIT_RE.fullmatch(value["reviewed_commit"]),
        isinstance(value.get("evidence"), list) and bool(value["evidence"]),
    ))


def audit_packs(manifest_path=DEFAULT_MANIFEST, *, root=ROOT, area_id=None):
    """Return conservative pack quality results; word count never grants approval."""
    root = Path(root).resolve()
    try:
        raw_manifest = Path(manifest_path)
        relative = (
            raw_manifest.relative_to(root).as_posix()
            if raw_manifest.is_absolute()
            else raw_manifest.as_posix()
        )
        safe_manifest = _resolve_repo_file(root, relative)
        manifest = json.loads(safe_manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        return {
            "status": "invalid",
            "area_count": 0,
            "expert_ready_count": 0,
            "areas": [],
            "errors": [f"Manifiesto inválido: {type(error).__name__}"],
        }

    areas = manifest.get("areas") if isinstance(manifest, dict) else None
    ids = [
        item.get("id") for item in areas
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ] if isinstance(areas, list) else []
    if (
        not isinstance(areas, list)
        or manifest.get("area_count") != len(areas)
        or len(ids) != len(areas)
        or len(ids) != len(set(ids))
    ):
        return {
            "status": "invalid",
            "area_count": 0,
            "expert_ready_count": 0,
            "areas": [],
            "errors": ["El manifiesto tiene áreas inválidas, duplicadas o un conteo incorrecto."],
        }

    results = []
    for area in areas:
        if area_id and area.get("id") != area_id:
            continue
        missing = list(REQUIRED_SECTIONS)
        word_count = 0
        path_error = None
        try:
            pack_path = _resolve_repo_file(root, area.get("path"))
            content = pack_path.read_text(encoding="utf-8")
            word_count = len(re.findall(r"\b[\w'-]+\b", content, flags=re.UNICODE))
            headings = {
                _normalize(match)
                for match in re.findall(r"^#{2,3}\s+(.+?)\s*$", content, flags=re.MULTILINE)
            }
            missing = [
                section for section, aliases in REQUIRED_SECTIONS.items()
                if not any(
                    _normalize(alias) in heading
                    for heading in headings for alias in aliases
                )
            ]
        except (OSError, UnicodeError, ValueError) as error:
            path_error = type(error).__name__
            missing = list(REQUIRED_SECTIONS)

        source_registry = _load_json(root, area.get("source_registry_path"))
        lab_evidence = _load_json(root, area.get("lab_evidence_path"))
        review_record = _load_json(root, area.get("quality_review_path"))
        verified_sources = _valid_source_registry(source_registry)
        lab_verified = _valid_lab_evidence(lab_evidence)
        review_approved = _valid_review_record(review_record)
        expert_ready = (
            path_error is None
            and not missing
            and verified_sources >= 5
            and lab_verified
            and review_approved
        )
        if expert_ready:
            quality_status = "expert_ready"
        elif path_error or missing:
            quality_status = "foundation_draft"
        else:
            quality_status = "awaiting_external_evidence"

        results.append({
            "id": area.get("id"),
            "name": area.get("name"),
            "quality_status": quality_status,
            "expert_ready": expert_ready,
            "word_count": word_count,
            "missing_sections": missing,
            "verified_external_sources": verified_sources,
            "lab_evidence_verified": lab_verified,
            "independent_review_approved": review_approved,
            "path_error": path_error,
        })

    if area_id and not results:
        return {
            "status": "invalid",
            "area_count": 0,
            "expert_ready_count": 0,
            "areas": [],
            "errors": ["El área solicitada no existe en el manifiesto."],
        }

    expert_ready_count = sum(item["expert_ready"] for item in results)
    return {
        "status": "audited",
        "area_count": len(results),
        "expert_ready_count": expert_ready_count,
        "foundation_draft_count": sum(
            item["quality_status"] == "foundation_draft" for item in results
        ),
        "awaiting_external_evidence_count": sum(
            item["quality_status"] == "awaiting_external_evidence" for item in results
        ),
        "areas": results,
        "errors": [],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--area", help="Auditar una sola especialidad.")
    parser.add_argument("--json", action="store_true", help="Imprimir el informe JSON completo.")
    parser.add_argument(
        "--require-expert-ready",
        action="store_true",
        help="Devuelve código 1 si falta evidencia para cualquier especialidad.",
    )
    args = parser.parse_args(argv)
    report = audit_packs(args.manifest, area_id=args.area)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"Áreas: {report['area_count']}; expert-ready: "
            f"{report['expert_ready_count']}; borradores: "
            f"{report.get('foundation_draft_count', 0)}; evidencia externa pendiente: "
            f"{report.get('awaiting_external_evidence_count', 0)}."
        )
        for item in report["areas"]:
            if not item["expert_ready"]:
                print(
                    f"{item['id']}: {item['quality_status']}; "
                    f"secciones faltantes={len(item['missing_sections'])}; "
                    f"fuentes verificadas={item['verified_external_sources']}."
                )
    if report["status"] != "audited":
        return 2
    if args.require_expert_ready and report["expert_ready_count"] != report["area_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
