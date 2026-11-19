"""Central deny-by-default authorization for network actions.

Authorization grants are local deployment configuration, not agent-generated data.
Set CYBER_AI_AUTHORIZATIONS_FILE to an administrator-managed file outside Git.
"""
import ipaddress
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


PROJECT = Path(__file__).resolve().parent
DEFAULT_AUTHORIZATIONS = PROJECT / "config" / "authorized_targets.json"
MAX_POLICY_BYTES = 1024 * 1024
MAX_GRANTS = 500
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
ACTION = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")
ALLOWED_PRIVATE_RANGES = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("fc00::/7"),
)


class AuthorizationError(ValueError):
    """Raised when a requested action has no matching valid grant."""


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuthorizationError("La política contiene claves JSON duplicadas.")
        result[key] = value
    return result



def _address_is_allowed(address):
    """Allow global, RFC1918, ULA and loopback IPs; reject special-purpose ranges."""
    if (
        address.is_multicast
        or address.is_unspecified
        or address.is_link_local
        or address.is_reserved
    ):
        return False
    approved_private = any(address in network for network in ALLOWED_PRIVATE_RANGES)
    return address.is_global or approved_private or address.is_loopback


def _canonical_target(target):
    if (
        not isinstance(target, str)
        or not target.strip()
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in target)
    ):
        raise AuthorizationError("Destino HTTP/HTTPS inválido o ambiguo.")
    try:
        parsed = urlsplit(target.strip())
    except ValueError as exc:
        raise AuthorizationError("Destino HTTP/HTTPS inválido o ambiguo.") from exc
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or "%" in parsed.netloc
        or "\\" in parsed.path
        or "%" in parsed.path
        or "//" in parsed.path
        or any(part in {".", ".."} for part in parsed.path.split("/"))
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in parsed.path)
    ):
        raise AuthorizationError("Destino HTTP/HTTPS inválido o ambiguo.")
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError as exc:
        # Hostnames require a pinned-DNS transport; accepting them here would
        # leave a DNS-rebinding window before the scanner connects.
        raise AuthorizationError(
            "Por seguridad, esta versión solo admite destinos IP literales; "
            "los dominios requieren transporte con DNS fijado."
        ) from exc
    if parsed.netloc.endswith(":"):
        raise AuthorizationError("IP o puerto inválido.")
    try:
        explicit_port = parsed.port
        port = (443 if parsed.scheme == "https" else 80) if explicit_port is None else explicit_port
    except ValueError as exc:
        raise AuthorizationError("IP o puerto inválido.") from exc
    if not 1 <= port <= 65535:
        raise AuthorizationError("Puerto fuera de rango.")
    normalized_host = address.compressed
    if address.version == 6:
        normalized_host = f"[{normalized_host}]"
    default_port = 80 if parsed.scheme == "http" else 443
    netloc = normalized_host if port == default_port else f"{normalized_host}:{port}"
    # Only collapse the empty path and root slash. A trailing slash on
    # any other path can identify a different resource and must remain scoped.
    path = "" if parsed.path in {"", "/"} else parsed.path
    return urlunsplit((parsed.scheme, netloc, path, "", "")), address


def _validate_grants(grants):
    if not isinstance(grants, list) or len(grants) > MAX_GRANTS:
        raise AuthorizationError("La política contiene una lista de autorizaciones inválida.")
    seen_ids = set()
    required = {"id", "target", "actions", "approved_by", "ticket", "expires_at"}
    for grant in grants:
        if not isinstance(grant, dict) or set(grant) != required:
            raise AuthorizationError("La política contiene una autorización con esquema inválido.")
        grant_id = grant["id"]
        if not isinstance(grant_id, str) or not IDENTIFIER.fullmatch(grant_id):
            raise AuthorizationError("La política contiene un identificador de autorización inválido.")
        if grant_id in seen_ids:
            raise AuthorizationError("La política contiene identificadores duplicados.")
        seen_ids.add(grant_id)

        actions = grant["actions"]
        if (
            not isinstance(actions, list)
            or not actions
            or len(actions) > 64
            or any(not isinstance(item, str) or not ACTION.fullmatch(item) for item in actions)
            or len(set(actions)) != len(actions)
        ):
            raise AuthorizationError("La autorización contiene acciones inválidas.")

        for field in ("approved_by", "ticket"):
            value = grant[field]
            if not isinstance(value, str) or not value.strip() or len(value) > 256:
                raise AuthorizationError(f"El campo {field} de la autorización es inválido.")

        expires_at = grant["expires_at"]
        if not isinstance(expires_at, str) or len(expires_at) > 64:
            raise AuthorizationError("La autorización tiene una expiración inválida.")
        try:
            expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if expires.tzinfo is None or expires.utcoffset() is None:
                raise ValueError("La expiración debe incluir zona horaria.")
        except (TypeError, ValueError, OverflowError) as exc:
            raise AuthorizationError("La autorización tiene una expiración inválida.") from exc

        _, address = _canonical_target(grant["target"])
        if not _address_is_allowed(address):
            raise AuthorizationError("La política contiene una IP reservada o fuera del alcance permitido.")


def _load_grants():
    path = Path(os.environ.get("CYBER_AI_AUTHORIZATIONS_FILE", DEFAULT_AUTHORIZATIONS))
    descriptor = None
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    try:
        parent_before = path.parent.lstat()
        if (
            stat.S_ISLNK(parent_before.st_mode)
            or getattr(parent_before, "st_file_attributes", 0) & reparse_flag
            or not stat.S_ISDIR(parent_before.st_mode)
        ):
            raise AuthorizationError("El directorio padre de autorizaciones no puede ser un enlace.")
        if os.name != "nt" and stat.S_IMODE(parent_before.st_mode) & 0o022:
            raise AuthorizationError(
                "El directorio padre de autorizaciones no puede ser modificable por grupo u otros."
            )
        before = path.lstat()
        if (
            stat.S_ISLNK(before.st_mode)
            or getattr(before, "st_file_attributes", 0) & reparse_flag
        ):
            raise AuthorizationError("El archivo de autorizaciones no puede ser un enlace.")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        after = path.lstat()
        parent_after = path.parent.lstat()
        if (
            not stat.S_ISREG(opened.st_mode)
            or stat.S_ISLNK(after.st_mode)
            or getattr(after, "st_file_attributes", 0) & reparse_flag
            or stat.S_ISLNK(parent_after.st_mode)
            or getattr(parent_after, "st_file_attributes", 0) & reparse_flag
            or (parent_before.st_dev, parent_before.st_ino) !=
               (parent_after.st_dev, parent_after.st_ino)
            or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
            or (opened.st_dev, opened.st_ino) != (after.st_dev, after.st_ino)
        ):
            raise AuthorizationError(
                "El archivo de autorizaciones y su directorio deben ser regulares y estables."
            )
        if opened.st_size > MAX_POLICY_BYTES:
            raise AuthorizationError("El archivo de autorizaciones supera 1 MiB.")
        if os.name != "nt" and opened.st_uid != os.geteuid():
            raise AuthorizationError(
                "El archivo de autorizaciones debe pertenecer al usuario efectivo del proceso."
            )
        insecure_mode = (
            os.name != "nt" and stat.S_IMODE(opened.st_mode) & 0o077
        )
        chunks = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(8192, MAX_POLICY_BYTES + 1 - total))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_POLICY_BYTES:
                raise AuthorizationError("El archivo de autorizaciones supera 1 MiB.")
            chunks.append(chunk)
        data = json.loads(
            b"".join(chunks).decode("utf-8"),
            object_pairs_hook=_unique_object,
        )
        opened_after_read = os.fstat(descriptor)
        if (
            (opened.st_dev, opened.st_ino) != (opened_after_read.st_dev, opened_after_read.st_ino)
            or opened.st_size != opened_after_read.st_size
            or opened.st_mtime_ns != opened_after_read.st_mtime_ns
            or (os.name != "nt" and opened_after_read.st_uid != os.geteuid())
        ):
            raise AuthorizationError("La política cambió mientras se leía.")
    except AuthorizationError:
        raise
    except FileNotFoundError as exc:
        raise AuthorizationError("No existe el archivo local de autorizaciones.") from exc
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise AuthorizationError("No se pudo leer la política de autorizaciones.") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)

    if not isinstance(data, dict) or set(data) != {"authorizations"}:
        raise AuthorizationError("La política no tiene el esquema esperado.")
    grants = data["authorizations"]
    _validate_grants(grants)
    if grants and insecure_mode:
        raise AuthorizationError(
            "El archivo de autorizaciones debe ser privado (permisos 0600)."
        )
    return grants


def authorize_target(target, action, authorization_id):
    """Validate exact target/action grant, expiry, identity, and address scope."""
    if not isinstance(action, str) or not ACTION.fullmatch(action):
        raise AuthorizationError("La acción solicitada es inválida.")
    if not isinstance(authorization_id, str) or not IDENTIFIER.fullmatch(authorization_id):
        raise AuthorizationError("Se requiere un identificador de autorización válido.")
    canonical, address = _canonical_target(target)
    if not _address_is_allowed(address):
        raise AuthorizationError("La dirección IP es reservada, multicast, no especificada o link-local, o está fuera del alcance permitido.")

    grants = _load_grants()
    now = datetime.now(timezone.utc)
    for grant in grants:
        if grant["id"] != authorization_id:
            continue
        expires = datetime.fromisoformat(grant["expires_at"].replace("Z", "+00:00"))
        grant_target, _ = _canonical_target(grant["target"])
        if (
            grant_target == canonical
            and action in grant["actions"]
            and expires > now
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
