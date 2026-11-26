"""Bounded, race-aware parsing of newline-delimited scanner evidence."""
import json
import stat
from pathlib import Path

from safe_io import SafeWriteError, read_regular_file
from secret_redaction import redact_sensitive_data


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("La evidencia JSON contiene claves duplicadas.")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"Constante JSON no estándar: {value}")


def read_jsonl_findings(
    path,
    *,
    max_output_bytes,
    max_line_bytes,
    max_findings,
    allow_blank_lines=False,
):
    """Read bounded JSONL evidence; invalid or unstable files yield no findings.

    Returns (findings, output_limit_exceeded, evidence_invalid). A missing output
    file is treated as an empty result because scanners may create it only when
    they have findings. All other unsafe file states fail closed.
    """
    for name, value in (
        ("max_output_bytes", max_output_bytes),
        ("max_line_bytes", max_line_bytes),
        ("max_findings", max_findings),
    ):
        if type(value) is not int or value < 1:
            raise ValueError(f"{name} debe ser un entero positivo.")
    if not isinstance(allow_blank_lines, bool):
        raise ValueError("allow_blank_lines debe ser booleano.")

    candidate = Path(path)
    try:
        info = candidate.lstat()
    except FileNotFoundError:
        return [], False, False
    except (OSError, TypeError, ValueError):
        return [], False, True

    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    if (
        stat.S_ISLNK(info.st_mode)
        or getattr(info, "st_file_attributes", 0) & reparse_flag
        or not stat.S_ISREG(info.st_mode)
        or getattr(info, "st_nlink", 1) != 1
    ):
        return [], False, True
    if info.st_size > max_output_bytes:
        return [], True, False

    try:
        raw = read_regular_file(candidate, max_bytes=max_output_bytes)
    except SafeWriteError:
        return [], False, True
    if len(raw) > max_output_bytes:
        return [], True, False
    if not raw:
        return [], False, False

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [], False, True

    lines = text.split("\n")
    if text.endswith("\n"):
        lines.pop()

    findings = []
    for index, line in enumerate(lines):
        delimiter_bytes = 1 if index < len(lines) - 1 or text.endswith("\n") else 0
        try:
            line_bytes = len(line.encode("utf-8")) + delimiter_bytes
        except UnicodeEncodeError:
            return [], False, True
        if line_bytes > max_line_bytes:
            return [], False, True
        if not line.strip():
            if allow_blank_lines:
                continue
            return [], False, True
        if len(findings) >= max_findings:
            return [], True, False
        try:
            record = json.loads(
                line,
                object_pairs_hook=_unique_object,
                parse_constant=_reject_constant,
            )
        except (json.JSONDecodeError, ValueError, RecursionError):
            return [], False, True
        if not isinstance(record, dict):
            return [], False, True
        try:
            findings.append(redact_sensitive_data(record))
        except (TypeError, ValueError, RecursionError):
            return [], False, True

    return findings, False, False


__all__ = ["read_jsonl_findings"]
