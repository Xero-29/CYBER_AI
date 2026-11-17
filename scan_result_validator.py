"""Contrato común de evidencia para escaneos remotos autorizados.

Valida estructura, alcance declarado y consistencia básica; no certifica
la veracidad, explotabilidad ni exhaustividad de los hallazgos.
"""
from urllib.parse import urlsplit


def validate_scan_result(result, *, expected_target=None):
    errors = []
    if not isinstance(result, dict):
        return {"status": "rejected", "errors": ["result_not_object"],
                "findings_eligible": False}
    target = result.get("target")
    if not isinstance(target, str) or not target:
        errors.append("target_missing")
    elif expected_target is not None and target != expected_target:
        errors.append("target_mismatch")
    try:
        parsed_target = urlsplit(target or "")
        if parsed_target.scheme not in {"http", "https"} or not parsed_target.hostname:
            errors.append("target_invalid")
    except ValueError:
        parsed_target = None
        errors.append("target_invalid")
    if result.get("status") != "completed":
        errors.append("scan_not_completed")
    if result.get("return_code") != 0:
        errors.append("scanner_return_code_not_zero")
    if not isinstance(result.get("authorization"), dict):
        errors.append("authorization_evidence_missing")
    elif not result["authorization"].get("authorization_id"):
        errors.append("authorization_id_missing")
    findings = result.get("findings")
    if not isinstance(findings, list):
        errors.append("findings_not_list")
        findings = []
    if result.get("findings_count") != len(findings):
        errors.append("findings_count_mismatch")
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"finding_{index}_not_object")
            continue
        matched = finding.get("matched-at") or finding.get("matched_at")
        if not isinstance(matched, str):
            errors.append(f"finding_{index}_matched_target_missing")
            continue
        try:
            parsed_match = urlsplit(matched)
            if (parsed_target is None or parsed_match.scheme not in {"http", "https"}
                    or not parsed_match.hostname
                    or parsed_match.hostname.lower() != parsed_target.hostname.lower()
                    or parsed_match.port != parsed_target.port):
                errors.append(f"finding_{index}_outside_authorized_origin")
        except ValueError:
            errors.append(f"finding_{index}_matched_target_invalid")
    return {
        "status": "valid_structure" if not errors else "rejected",
        "errors": errors,
        "findings_eligible": not errors,
        "scope_note": (
            "Valida estructura y correspondencia con el origen autorizado; "
            "no demuestra veracidad, explotabilidad ni exhaustividad."
        ),
    }
