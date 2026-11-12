"""Central deny-by-default authorization for network actions.

Authorization grants are local deployment configuration, not agent-generated data.
Set CYBER_AI_AUTHORIZATIONS_FILE to an administrator-managed file outside Git.
"""
import ipaddress
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


PROJECT = Path(__file__).resolve().parent
DEFAULT_AUTHORIZATIONS = PROJECT / "config" / "authorized_targets.json"


class AuthorizationError(ValueError):
    """Raised when a requested action has no matching valid grant."""


def _canonical_target(target):
    parsed = urlsplit(str(target).strip())
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise AuthorizationError("Destino HTTP/HTTPS inválido o ambiguo.")
    try:
        address = ipaddress.ip_address(parsed.hostname)
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        # Hostnames require a pinned-DNS transport; accepting them here would
        # leave a DNS-rebinding window before the scanner connects.
        if "does not appear to be an IPv4 or IPv6 address" in str(exc):
            raise AuthorizationError(
                "Por seguridad, esta versión solo admite destinos IP literales; "
                "los dominios requieren transporte con DNS fijado."
            ) from exc
        raise AuthorizationError("IP o puerto inválido.") from exc
    if not 1 <= port <= 65535:
        raise AuthorizationError("Puerto fuera de rango.")
    normalized_host = address.compressed
    if address.version == 6:
        normalized_host = f"[{normalized_host}]"
    netloc = normalized_host if port in (80, 443) and (
        (parsed.scheme == "http" and port == 80)
        or (parsed.scheme == "https" and port == 443)
    ) else f"{normalized_host}:{port}"
    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme, netloc, path, "", "")), address


def _load_grants():
    path = Path(os.environ.get("CYBER_AI_AUTHORIZATIONS_FILE", DEFAULT_AUTHORIZATIONS))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuthorizationError("No existe el archivo local de autorizaciones.") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthorizationError("No se pudo leer la política de autorizaciones.") from exc
    grants = data.get("authorizations") if isinstance(data, dict) else None
    if not isinstance(grants, list):
        raise AuthorizationError("La política no contiene una lista de autorizaciones.")
    return grants


def authorize_target(target, action, authorization_id):
    """Validate exact target/action grant, expiry, identity, and address scope."""
    if not isinstance(authorization_id, str) or not authorization_id.strip():
        raise AuthorizationError("Se requiere un identificador de autorización.")
    canonical, address = _canonical_target(target)
    if not address.is_global:
        raise AuthorizationError("El destino no es una IP pública global.")
    now = datetime.now(timezone.utc)
    for grant in _load_grants():
        if not isinstance(grant, dict) or grant.get("id") != authorization_id:
            continue
        try:
            expires = datetime.fromisoformat(
                grant["expires_at"].replace("Z", "+00:00")
            )
            if expires.tzinfo is None:
                raise ValueError("La expiración debe incluir zona horaria.")
        except (KeyError, AttributeError, TypeError, ValueError) as exc:
            raise AuthorizationError("La autorización tiene una expiración inválida.") from exc
        try:
            grant_target, _ = _canonical_target(grant.get("target", ""))
        except AuthorizationError:
            continue
        if (
            grant_target == canonical
            and action in grant.get("actions", [])
            and expires > now
            and isinstance(grant.get("approved_by"), str)
            and grant["approved_by"].strip()
            and isinstance(grant.get("ticket"), str)
            and grant["ticket"].strip()
        ):
            return {
                "authorization_id": authorization_id,
                "approved_by": grant["approved_by"],
                "ticket": grant["ticket"],
                "target": canonical,
                "action": action,
                "expires_at": expires.isoformat(),
            }
    raise AuthorizationError(
        "No existe una autorización vigente para ese destino y esa acción."
    )
