"""Race-aware validation and hashing of local Nuclei templates."""
import hashlib
import hmac
import os
import re
import stat
from pathlib import Path, PurePosixPath

from tool_allowlist import ToolAllowlistError, load_signed_tool_allowlist


PROJECT_ROOT = Path(__file__).resolve().parent
MAX_TEMPLATE_BYTES = 2 * 1024 * 1024


def template_allowlist_id(relative_path):
    """Return a stable, bounded ID for one repository-relative Nuclei template."""
    if (
        not isinstance(relative_path, str)
        or not relative_path
        or "\\" in relative_path
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in relative_path)
    ):
        raise TemplateIntegrityError("La ruta relativa de plantilla no es válida.")
    pure = PurePosixPath(relative_path)
    if (
        pure.is_absolute()
        or any(part in {"", ".", ".."} for part in pure.parts)
        or pure.as_posix() != relative_path
    ):
        raise TemplateIntegrityError("La ruta relativa de plantilla no es canónica.")
    slug = re.sub(r"[^a-z0-9]+", "_", relative_path.lower()).strip("_")
    suffix = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:8]
    prefix = "nuclei_template_"
    slug_limit = 64 - len(prefix) - 1 - len(suffix)
    if not slug or slug_limit < 1:
        raise TemplateIntegrityError("No se pudo generar el identificador de plantilla.")
    return f"{prefix}{slug[:slug_limit]}_{suffix}"


def verify_approved_templates(selected):
    """Require exact path/hash entries in the private signed tool allowlist."""
    if not isinstance(selected, list) or not selected or len(selected) > 64:
        raise TemplateIntegrityError("La selección de plantillas no es válida.")
    path_text = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_PATH", "").strip()
    key_text = os.environ.get("CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY", "")
    if not path_text or not key_text:
        raise TemplateIntegrityError(
            "Nuclei requiere una allowlist HMAC configurada para aprobar sus plantillas."
        )
    candidate = Path(os.path.abspath(path_text))
    try:
        candidate.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        pass
    else:
        raise TemplateIntegrityError(
            "La allowlist firmada debe almacenarse fuera del repositorio."
        )
    try:
        approved = load_signed_tool_allowlist(candidate, key_text.encode("utf-8"))
    except ToolAllowlistError as error:
        raise TemplateIntegrityError(
            "No se pudo validar la allowlist firmada de herramientas y plantillas."
        ) from error

    identifiers = []
    seen = set()
    for item in selected:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "sha256"}
            or not isinstance(item["sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
        ):
            raise TemplateIntegrityError("La evidencia de plantilla tiene un esquema inválido.")
        identifier = template_allowlist_id(item["path"])
        if identifier in seen:
            raise TemplateIntegrityError("La selección contiene IDs de plantilla duplicados.")
        seen.add(identifier)
        entry = approved.get(identifier)
        if entry is None or not hmac.compare_digest(entry["sha256"], item["sha256"]):
            raise TemplateIntegrityError(
                "Una plantilla Nuclei no está aprobada por hash en la allowlist firmada."
            )
        identifiers.append(identifier)
    return {"enforced": True, "approved_template_ids": identifiers}


class TemplateIntegrityError(ValueError):
    """A template is outside the approved root or changed while being read."""


def _is_link_or_reparse(info):
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & reparse_flag
    )


def resolve_template_path(path, root):
    """Resolve one regular, bounded template without accepting symlink components."""
    try:
        root = Path(root)
        root_info = root.lstat()
        if _is_link_or_reparse(root_info) or not stat.S_ISDIR(root_info.st_mode):
            raise TemplateIntegrityError("La raíz de plantillas debe ser un directorio real.")

        root_absolute = root.absolute()
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = root_absolute / candidate
        if ".." in candidate.parts:
            raise TemplateIntegrityError("La ruta de plantilla no puede contener traversal.")

        candidate_absolute = candidate.absolute()
        relative = candidate_absolute.relative_to(root_absolute)
        if not relative.parts:
            raise TemplateIntegrityError("La ruta debe identificar un archivo de plantilla.")

        current = root_absolute
        final_info = None
        for index, part in enumerate(relative.parts):
            current = current / part
            info = current.lstat()
            if _is_link_or_reparse(info):
                raise TemplateIntegrityError("No se permiten symlinks ni puntos de reanálisis en plantillas.")
            if index < len(relative.parts) - 1:
                if not stat.S_ISDIR(info.st_mode):
                    raise TemplateIntegrityError("Un componente de la ruta de plantilla no es un directorio.")
            else:
                if (
                    not stat.S_ISREG(info.st_mode)
                    or info.st_size <= 0
                    or info.st_size > MAX_TEMPLATE_BYTES
                    or info.st_nlink != 1
                ):
                    raise TemplateIntegrityError("La plantilla debe ser un archivo regular de tamaño permitido.")
                final_info = info

        root_resolved = root.resolve(strict=True)
        resolved = candidate_absolute.resolve(strict=True)
        resolved.relative_to(root_resolved)
        root_after = root.lstat()
        if (root_info.st_dev, root_info.st_ino) != (root_after.st_dev, root_after.st_ino):
            raise TemplateIntegrityError("La raíz de plantillas cambió durante la validación.")
        if final_info is None:
            raise TemplateIntegrityError("No se pudo validar la plantilla.")
        return resolved
    except TemplateIntegrityError:
        raise
    except (OSError, RuntimeError, ValueError) as error:
        raise TemplateIntegrityError("No se pudo validar una ruta de plantilla segura.") from error


def _hash_resolved_template(path):
    descriptor = None
    try:
        resolved = Path(path)
        before = resolved.lstat()
        if (
            _is_link_or_reparse(before)
            or not stat.S_ISREG(before.st_mode)
            or before.st_size <= 0
            or before.st_size > MAX_TEMPLATE_BYTES
            or before.st_nlink != 1
        ):
            raise TemplateIntegrityError("La plantilla dejó de ser un archivo regular permitido.")

        flags = (
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(resolved, flags)
        opened = os.fstat(descriptor)
        identity = (opened.st_dev, opened.st_ino)
        if (
            not stat.S_ISREG(opened.st_mode)
            or identity != (before.st_dev, before.st_ino)
            or opened.st_size != before.st_size
            or opened.st_mtime_ns != before.st_mtime_ns
            or opened.st_nlink != 1
        ):
            raise TemplateIntegrityError("La plantilla cambió durante su apertura.")

        digest = hashlib.sha256()
        total = 0
        while True:
            block = os.read(descriptor, 64 * 1024)
            if not block:
                break
            total += len(block)
            if total > MAX_TEMPLATE_BYTES:
                raise TemplateIntegrityError("La plantilla supera el límite de tamaño.")
            digest.update(block)

        after = os.fstat(descriptor)
        path_after = resolved.lstat()
        if (
            (after.st_dev, after.st_ino) != identity
            or (path_after.st_dev, path_after.st_ino) != identity
            or _is_link_or_reparse(path_after)
            or not stat.S_ISREG(path_after.st_mode)
            or after.st_size != opened.st_size
            or after.st_mtime_ns != opened.st_mtime_ns
            or after.st_nlink != 1
            or path_after.st_nlink != 1
            or total != after.st_size
        ):
            raise TemplateIntegrityError("La plantilla cambió mientras se calculaba su hash.")
        return digest.hexdigest()
    except TemplateIntegrityError:
        raise
    except (OSError, RuntimeError, ValueError) as error:
        raise TemplateIntegrityError("No se pudo calcular la integridad de una plantilla.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def hash_selected_templates(selected, root):
    """Return deterministic relative-path/hash evidence for validated templates."""
    try:
        root_resolved = Path(root).resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as error:
        raise TemplateIntegrityError("La raíz de plantillas no está disponible.") from error
    evidence = []
    seen = set()
    for item in selected:
        path = item.get("path") if isinstance(item, dict) else item
        if not isinstance(path, (str, Path)) or not str(path).strip():
            raise TemplateIntegrityError("Cada plantilla debe incluir una ruta no vacía.")
        resolved = resolve_template_path(path, root)
        relative = resolved.relative_to(root_resolved).as_posix()
        if relative in seen:
            raise TemplateIntegrityError("La selección contiene una plantilla duplicada.")
        seen.add(relative)
        evidence.append({"path": relative, "sha256": _hash_resolved_template(resolved)})
    return evidence


def safe_template_path(path, root):
    """Compatibility helper for candidate filtering; unsafe paths return None."""
    try:
        return resolve_template_path(path, root)
    except TemplateIntegrityError:
        return None


__all__ = [
    "MAX_TEMPLATE_BYTES",
    "TemplateIntegrityError",
    "hash_selected_templates",
    "resolve_template_path",
    "safe_template_path",
    "template_allowlist_id",
    "verify_approved_templates",
]
