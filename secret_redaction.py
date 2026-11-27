"""Redact sensitive credentials from tool output and structured evidence."""
import re


SECRET_FIELD = re.compile(
    r"(?:api[_-]?key|client[_-]?secret|access[_-]?key|access[_-]?token|refresh[_-]?token|token|"
    r"authorization|password|passwd|secret|credential|private[_-]?key|cookie|"
    r"set[_-]?cookie|session[_-]?(?:id|token|key)|hmac[_-]?key|"
    r"signing[_-]?key|encryption[_-]?key|signature|\bsig\b|"
    r"aws[_-]?access[_-]?key[_-]?id|access[_-]?key[_-]?id)",
    re.IGNORECASE,
)
SECRET_ASSIGNMENT = re.compile(
    r'''(?i)(["']?(?:api[_-]?key|access[_-]?key|access[_-]?token|refresh[_-]?token|token|password|'''
    r'''passwd|secret|client[_-]?secret|authorization|credential|private[_-]?key|cookie|'''
    r'''set[_-]?cookie|session[_-]?(?:id|token|key)|hmac[_-]?key|signing[_-]?key|encryption[_-]?key|signature|\bsig\b|'''
    r'''aws[_-]?access[_-]?key[_-]?id|access[_-]?key[_-]?id)'''
    r'''["']?\s*[:=]\s*)(\\"(?:[^"\\]|\\.)*\\"|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[^\s,&;}\]"']+)'''
)

PRIVATE_KEY = re.compile(
    r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----",
    re.DOTALL,
)
BEARER_TOKEN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
BASIC_AUTH = re.compile(r"(?i)\bBasic\s+[A-Za-z0-9+/=]{12,}")
URL_CREDENTIALS = re.compile(
    r"(?i)([a-z][a-z0-9+.-]*://)[^/@\s:]*:[^/@\s]+@"
)
TOKEN_PATTERNS = (
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
)


def _replace_assignment(match):
    prefix, value = match.groups()
    if value.startswith(r'\"') and value.endswith(r'\"'):
        value = r'\"[REDACTED]\"'
    elif len(value) >= 2 and value[0] in {"'", '"'} and value[-1] == value[0]:
        value = f"{value[0]}[REDACTED]{value[0]}"
    else:
        value = "[REDACTED]"
    return prefix + value


def redact_text(value):
    """Redact common credential formats without logging the original value."""
    result = PRIVATE_KEY.sub("[REDACTED PRIVATE KEY]", str(value))
    result = URL_CREDENTIALS.sub(r"\1[REDACTED]@", result)
    result = BEARER_TOKEN.sub("Bearer [REDACTED]", result)
    result = BASIC_AUTH.sub("Basic [REDACTED]", result)
    result = SECRET_ASSIGNMENT.sub(_replace_assignment, result)
    for pattern in TOKEN_PATTERNS:
        result = pattern.sub("[REDACTED TOKEN]", result)
    return result


def redact_sensitive_data(value, key="", *, max_depth=64, _depth=0):
    """Recursively redact credential-valued fields and sensitive free text."""
    if key and SECRET_FIELD.search(str(key)):
        return "[REDACTED]"
    if _depth > max_depth:
        return "[REDACTED: nesting limit]"
    if isinstance(value, dict):
        return {
            str(item_key)[:256]: redact_sensitive_data(
                item_value, str(item_key), max_depth=max_depth, _depth=_depth + 1
            )
            for item_key, item_value in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [
            redact_sensitive_data(
                item, max_depth=max_depth, _depth=_depth + 1
            )
            for item in value
        ]
    if isinstance(value, bytes):
        return redact_text(value.decode("utf-8", errors="replace"))
    if isinstance(value, str):
        return redact_text(value)
    return value


__all__ = ["redact_sensitive_data", "redact_text"]
