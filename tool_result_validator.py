"""Validación independiente de integridad de evidencias de adaptadores."""
import re


SHA256 = re.compile(r"[0-9a-f]{64}")


def validate_tool_evidence(evidence):
    errors = []
    if not isinstance(evidence, dict):
        return {"status": "invalid", "errors": ["evidence_not_object"], "findings_eligible": False}
    for field in ("target_sha256", "target_sha256_after", "tool_binary_sha256", "tool_binary_sha256_after"):
        value = evidence.get(field)
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            errors.append(field + "_invalid")
    if evidence.get("status") != "completed":
        errors.append("tool_status_not_completed")
    if evidence.get("return_code") != 0:
        errors.append("nonzero_or_missing_return_code")
    if evidence.get("tool_reported_success") is not True:
        errors.append("tool_did_not_report_success")
    if evidence.get("target_modified") is not False:
        errors.append("target_integrity_not_preserved")
    if evidence.get("tool_binary_modified") is not False:
        errors.append("binary_integrity_not_preserved")
    if evidence.get("target_sha256") != evidence.get("target_sha256_after"):
        errors.append("target_hash_mismatch")
    if evidence.get("tool_binary_sha256") != evidence.get("tool_binary_sha256_after"):
        errors.append("binary_hash_mismatch")
    allowlist = evidence.get("tool_allowlist")
    if not isinstance(allowlist, dict) or allowlist.get("enforced") is not True:
        errors.append("signed_allowlist_not_enforced")
    if evidence.get("output_truncated") is not False:
        errors.append("output_truncated_or_unknown")
    return {
        "status": "valid_integrity" if not errors else "rejected",
        "errors": errors,
        "findings_eligible": not errors,
        "scope_note": (
            "Valida integridad y condiciones de ejecución, no la veracidad ni "
            "la explotabilidad de los hallazgos."
        ),
    }
