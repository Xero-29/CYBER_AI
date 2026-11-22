#!/usr/bin/env python3
"""Auditoría conservadora de madurez, fuentes, laboratorios y revisión de los packs offline."""

import argparse
import base64
import binascii
import hashlib
import hmac
import json
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from safe_io import SafeWriteError, read_regular_file


ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "knowledge" / "packs" / "manifest.json"
SHA256_RE = re.compile(r"[a-fA-F0-9]{64}\Z")
COMMIT_RE = re.compile(r"[a-fA-F0-9]{40}\Z")
MAX_PACK_BYTES = 16 * 1024 * 1024
MAX_EVIDENCE_BYTES = 16 * 1024 * 1024
MAX_REVIEW_KEY_BYTES = 16 * 1024
REVIEW_PUBLIC_KEY_ENV = "CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_PEM"
REVIEW_PUBLIC_KEY_SHA256_ENV = "CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_SHA256"
REVIEWER_ID_ENV = "CYBER_AI_KNOWLEDGE_REVIEWER_ID"

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
    """Resolve a canonical repository-relative file while rejecting links and traversal."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("La ruta debe ser un texto POSIX relativo.")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or value != relative.as_posix()
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise ValueError("La ruta absoluta, no canónica o con traversal está prohibida.")

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


def _read_repo_file(root, relative, *, max_bytes=MAX_EVIDENCE_BYTES):
    path = _resolve_repo_file(root, relative)
    return path, read_regular_file(path, max_bytes=max_bytes)


def _load_json_document(root, relative):
    """Load a bounded repository JSON file and retain its exact content digest."""
    if not isinstance(relative, str) or not relative:
        return None, None, None
    try:
        path, raw = _read_repo_file(root, relative)
        value = json.loads(raw.decode("utf-8"))
        return value, path, hashlib.sha256(raw).hexdigest()
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, SafeWriteError):
        return None, None, None


def _file_matches_hash(root, relative, expected):
    if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
        return False
    try:
        _, raw = _read_repo_file(root, relative)
    except (OSError, UnicodeError, ValueError, SafeWriteError):
        return False
    actual = hashlib.sha256(raw).hexdigest()
    return hmac.compare_digest(actual, expected.lower())


def _aware_timestamp(value):
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _public_https_reference(value):
    """Reject credential-bearing, local, ambiguous, or non-HTTPS source references."""
    if not isinstance(value, str) or not value or len(value) > 4096:
        return False
    try:
        parsed = urlsplit(value)
        host = parsed.hostname
        port = parsed.port
    except ValueError:
        return False
    if (
        parsed.scheme != "https"
        or not host
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or (port is not None and not 1 <= port <= 65535)
    ):
        return False

    normalized_host = host.rstrip(".").lower()
    if (
        normalized_host == "localhost"
        or normalized_host.endswith((".localhost", ".local", ".internal", ".test", ".invalid"))
    ):
        return False
    try:
        import ipaddress
        address = ipaddress.ip_address(normalized_host)
    except ValueError:
        return True
    return address.is_global


def _source_is_verified(source, root):
    if not isinstance(source, dict):
        return False
    return all((
        isinstance(source.get("id"), str) and bool(source["id"].strip()),
        isinstance(source.get("title"), str) and bool(source["title"].strip()),
        isinstance(source.get("publisher"), str) and bool(source["publisher"].strip()),
        _public_https_reference(source.get("url")),
        isinstance(source.get("version"), str) and bool(source["version"].strip()),
        isinstance(source.get("license"), str) and bool(source["license"].strip()),
        source.get("license_status") == "approved",
        _aware_timestamp(source.get("verified_at")),
        isinstance(source.get("verification_evidence"), str)
        and bool(source["verification_evidence"].strip()),
        _file_matches_hash(
            root,
            source.get("verification_evidence_path"),
            source.get("verification_evidence_sha256"),
        ),
    ))


def _valid_source_registry(value, root):
    if not isinstance(value, dict) or not isinstance(value.get("sources"), list):
        return 0
    sources = value["sources"]
    if not all(isinstance(source, dict) for source in sources):
        return 0
    ids = [source.get("id") for source in sources]
    if not all(isinstance(item, str) and item.strip() for item in ids):
        return 0
    if len(ids) != len(set(ids)):
        return 0
    return sum(_source_is_verified(source, root) for source in sources)


def _valid_lab_evidence(value, root):
    if not isinstance(value, dict) or not isinstance(value.get("runs"), list):
        return False
    for run in value["runs"]:
        if not isinstance(run, dict):
            continue
        if (
            run.get("status") == "passed"
            and isinstance(run.get("artifact_sha256"), str)
            and SHA256_RE.fullmatch(run["artifact_sha256"])
            and _file_matches_hash(
                root, run.get("artifact_path"), run.get("artifact_sha256")
            )
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


def review_signature_payload(record, area_id):
    """Return canonical UTF-8 bytes signed by the independent Ed25519 reviewer."""
    fields = (
        "decision",
        "evidence",
        "independent_review",
        "reviewed_at",
        "reviewed_commit",
        "reviewed_lab_evidence_sha256",
        "reviewed_pack_sha256",
        "reviewed_sources_sha256",
        "reviewer_id",
    )
    payload = {"schema_version": 1, "area_id": area_id}
    payload.update({field: record.get(field) for field in fields})
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _verify_review_signature(record, area_id):
    """Verify an Ed25519 attestation against an externally pinned public key."""
    public_key_pem = os.environ.get(REVIEW_PUBLIC_KEY_ENV, "")
    expected_fingerprint = os.environ.get(REVIEW_PUBLIC_KEY_SHA256_ENV, "").strip().lower()
    trusted_reviewer = os.environ.get(REVIEWER_ID_ENV, "").strip()
    if (
        not public_key_pem
        or not expected_fingerprint
        or not trusted_reviewer
        or record.get("reviewer_id") != trusted_reviewer
    ):
        return False

    try:
        key_bytes = public_key_pem.encode("utf-8")
        if (
            len(key_bytes) > MAX_REVIEW_KEY_BYTES
            or b"-----BEGIN PUBLIC KEY-----" not in key_bytes
            or b"-----END PUBLIC KEY-----" not in key_bytes
            or not SHA256_RE.fullmatch(expected_fingerprint)
            or not hmac.compare_digest(
                hashlib.sha256(key_bytes).hexdigest(),
                expected_fingerprint,
            )
        ):
            return False

        signature_text = record.get("signature")
        if not isinstance(signature_text, str) or len(signature_text) > 2048:
            return False
        signature = base64.b64decode(signature_text, validate=True)
        if len(signature) != 64:
            return False

        openssl = shutil.which("openssl")
        if not openssl:
            return False

        payload = review_signature_payload(record, area_id)
        with tempfile.TemporaryDirectory(prefix="cyber-ai-review-") as directory:
            work = Path(directory)
            key_path = work / "reviewer-public.pem"
            payload_path = work / "review-payload.json"
            signature_path = work / "review-signature.bin"
            for path, content in (
                (key_path, key_bytes),
                (payload_path, payload),
                (signature_path, signature),
            ):
                descriptor = os.open(
                    path,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o600,
                )
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())

            result = subprocess.run(
                [
                    openssl, "pkeyutl", "-verify", "-pubin",
                    "-inkey", str(key_path), "-rawin",
                    "-in", str(payload_path), "-sigfile", str(signature_path),
                ],
                cwd=directory,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
                check=False,
                env={"PATH": os.environ.get("PATH", ""), "LC_ALL": "C", "LANG": "C"},
            )
            return result.returncode == 0
    except (OSError, ValueError, binascii.Error, subprocess.SubprocessError):
        return False


def _valid_review_record(
    value, root, area_id, pack_sha256, sources_sha256, lab_evidence_sha256
):
    if not isinstance(value, dict):
        return False
    if not all((
        value.get("decision") == "approved",
        value.get("independent_review") is True,
        isinstance(value.get("reviewer_id"), str) and bool(value["reviewer_id"].strip()),
        _aware_timestamp(value.get("reviewed_at")),
        isinstance(value.get("reviewed_commit"), str)
        and COMMIT_RE.fullmatch(value["reviewed_commit"]),
        isinstance(pack_sha256, str)
        and value.get("reviewed_pack_sha256") == pack_sha256,
        isinstance(sources_sha256, str)
        and value.get("reviewed_sources_sha256") == sources_sha256,
        isinstance(lab_evidence_sha256, str)
        and value.get("reviewed_lab_evidence_sha256") == lab_evidence_sha256,
    )):
        return False

    evidence = value.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return False
    seen_paths = set()
    for item in evidence:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            return False
        path = item.get("path")
        if not isinstance(path, str) or path in seen_paths:
            return False
        seen_paths.add(path)
        if not _file_matches_hash(root, path, item.get("sha256")):
            return False

    return _verify_review_signature(value, area_id)


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
        manifest_raw = read_regular_file(safe_manifest, max_bytes=MAX_PACK_BYTES)
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, SafeWriteError) as error:
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
        pack_sha256 = None
        try:
            pack_path = _resolve_repo_file(root, area.get("path"))
            pack_raw = read_regular_file(pack_path, max_bytes=MAX_PACK_BYTES)
            content = pack_raw.decode("utf-8")
            pack_sha256 = hashlib.sha256(pack_raw).hexdigest()
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
        except (OSError, UnicodeError, ValueError, SafeWriteError) as error:
            path_error = type(error).__name__
            missing = list(REQUIRED_SECTIONS)

        source_registry, _, sources_sha256 = _load_json_document(
            root, area.get("source_registry_path")
        )
        lab_evidence, _, lab_evidence_sha256 = _load_json_document(
            root, area.get("lab_evidence_path")
        )
        review_record, _, _ = _load_json_document(
            root, area.get("quality_review_path")
        )
        verified_sources = _valid_source_registry(source_registry, root)
        lab_verified = _valid_lab_evidence(lab_evidence, root)
        review_approved = _valid_review_record(
            review_record,
            root,
            area.get("id"),
            pack_sha256,
            sources_sha256,
            lab_evidence_sha256,
        )
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
