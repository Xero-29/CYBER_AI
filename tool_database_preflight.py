"""Read-only preflight for local vulnerability databases.

The checks never download, update, or extract vulnerability databases.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path


MAX_STATUS_OUTPUT = 128_000
DEFAULT_GRYPE_MAX_AGE_DAYS = 14


def _parse_max_age(value: str | None, *, default: int) -> int:
    if value is None or value == "":
        return default
    if not re.fullmatch(r"[0-9]{1,4}", value):
        raise ValueError("CYBER_AI_GRYPE_DB_MAX_AGE_DAYS debe ser un entero entre 1 y 3650.")
    days = int(value)
    if not 1 <= days <= 3650:
        raise ValueError("CYBER_AI_GRYPE_DB_MAX_AGE_DAYS debe estar entre 1 y 3650.")
    return days


def _osv_database_directory(environ: dict, home: Path, temp: Path) -> Path:
    configured = (
        environ.get("OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY")
        or environ.get("OSV_SCALIBR_LOCAL_DB_CACHE_DIRECTORY")
    )
    if configured:
        base = Path(configured).expanduser()
        return base if base.name == "osv-scalibr" else base / "osv-scalibr"
    user_cache = home / ".cache" / "osv-scalibr"
    if user_cache.exists():
        return user_cache
    return temp / "osv-scalibr"


def inspect_osv_database(*, environ=None, home=None, temp_dir=None) -> dict:
    """Check local OSV archive presence and ZIP directory integrity.

    OSV's documented offline bundle does not expose an authoritative database
    build timestamp or a stable schema identifier in the all.zip layout. The
    result therefore never claims freshness or schema validation.
    """
    environ = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    temp_dir = Path(os.getenv("TMPDIR", "/tmp")) if temp_dir is None else Path(temp_dir)
    root = _osv_database_directory(environ, home, temp_dir)
    result = {
        "tool": "osv_scanner",
        "database_directory": str(root),
        "status": "missing",
        "archive_count": 0,
        "ecosystems": [],
        "freshness": "unknown",
        "schema_validation": "not_exposed_by_documented_all_zip_layout",
        "network_access": False,
        "note": (
            "Se valida presencia y estructura ZIP de las bases detectadas. "
            "OSV no expone aquí una fecha de construcción autoritativa; "
            "el escáner valida el ecosistema requerido durante el análisis."
        ),
    }
    if root.is_symlink() or not root.is_dir():
        return result

    archives = []
    try:
        for ecosystem_dir in sorted(root.iterdir()):
            if ecosystem_dir.is_symlink() or not ecosystem_dir.is_dir():
                continue
            archive = ecosystem_dir / "all.zip"
            if archive.is_symlink() or not archive.is_file():
                continue
            try:
                if archive.stat().st_size <= 0:
                    continue
                with zipfile.ZipFile(archive, "r") as bundle:
                    members = bundle.infolist()
                    if not members or not any(
                        item.filename.lower().endswith(".json") for item in members
                    ):
                        continue
                    if len(members) > 250_000:
                        continue
                    archives.append(ecosystem_dir.name)
            except (OSError, zipfile.BadZipFile, RuntimeError):
                continue
    except OSError:
        result["status"] = "error"
        return result

    result["archive_count"] = len(archives)
    result["ecosystems"] = archives
    result["status"] = "present_structure_checked" if archives else "missing_or_invalid"
    return result


def inspect_grype_database(binary: str, *, environ=None, max_age_days=None) -> dict:
    """Use Grype's read-only db status command and validate metadata/freshness."""
    environ = os.environ if environ is None else environ
    if max_age_days is None:
        max_age_days = _parse_max_age(
            environ.get("CYBER_AI_GRYPE_DB_MAX_AGE_DAYS"),
            default=DEFAULT_GRYPE_MAX_AGE_DAYS,
        )
    if not isinstance(max_age_days, int) or isinstance(max_age_days, bool) or not 1 <= max_age_days <= 3650:
        raise ValueError("La antigüedad máxima de Grype debe estar entre 1 y 3650 días.")

    env = {
        "PATH": environ.get("PATH", ""),
        "HOME": environ.get("HOME", str(Path.home())),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
        "GRYPE_DB_AUTO_UPDATE": "false",
        "GRYPE_EXTERNAL_SOURCES_ENABLE": "false",
        "GRYPE_CHECK_FOR_APP_UPDATE": "false",
    }
    if environ.get("GRYPE_DB_CACHE_DIR"):
        env["GRYPE_DB_CACHE_DIR"] = environ["GRYPE_DB_CACHE_DIR"]

    try:
        completed = subprocess.run(
            [binary, "db", "status", "--output", "json"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            shell=False,
            check=False,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "tool": "grype",
            "status": "unavailable",
            "reason": type(exc).__name__,
            "network_access": False,
        }

    if completed.returncode != 0 or len(completed.stdout) > MAX_STATUS_OUTPUT:
        return {
            "tool": "grype",
            "status": "missing_or_invalid",
            "return_code": completed.returncode,
            "stderr": completed.stderr[:2048],
            "network_access": False,
        }
    try:
        payload = json.loads(completed.stdout)
        if isinstance(payload, list):
            if len(payload) != 1 or not isinstance(payload[0], dict):
                raise ValueError("Formato JSON de estado Grype inesperado.")
            payload = payload[0]
        if not isinstance(payload, dict):
            raise ValueError("El estado JSON de Grype debe ser un objeto.")
    except (json.JSONDecodeError, ValueError) as exc:
        return {
            "tool": "grype",
            "status": "invalid_metadata",
            "reason": str(exc),
            "network_access": False,
        }

    error = payload.get("error")
    status = payload.get("status")
    schema = payload.get("schemaVersion")
    built = payload.get("built")
    database_path = payload.get("path") or payload.get("location")
    if error not in (None, "", False) or (status is not None and str(status).lower() != "valid"):
        return {
            "tool": "grype",
            "status": "invalid_database",
            "error": str(error or status)[:2048],
            "schema_version": schema,
            "built": built,
            "network_access": False,
        }
    if not isinstance(schema, str) or not re.fullmatch(r"v?[0-9]+(?:\.[0-9]+){0,3}", schema):
        return {
            "tool": "grype",
            "status": "invalid_metadata",
            "reason": "schemaVersion ausente o inválido.",
            "network_access": False,
        }
    if not isinstance(built, str):
        return {
            "tool": "grype",
            "status": "invalid_metadata",
            "reason": "built ausente.",
            "schema_version": schema,
            "network_access": False,
        }
    try:
        built_at = datetime.fromisoformat(built.replace("Z", "+00:00"))
        if built_at.tzinfo is None:
            raise ValueError("built debe incluir zona horaria.")
        built_at = built_at.astimezone(timezone.utc)
    except ValueError:
        return {
            "tool": "grype",
            "status": "invalid_metadata",
            "reason": "built no es una fecha ISO-8601 con zona horaria.",
            "schema_version": schema,
            "network_access": False,
        }

    now = datetime.now(timezone.utc)
    age_seconds = (now - built_at).total_seconds()
    if age_seconds < -300:
        return {
            "tool": "grype",
            "status": "invalid_metadata",
            "reason": "La fecha de construcción está en el futuro.",
            "schema_version": schema,
            "built": built,
            "network_access": False,
        }
    age_days = max(0.0, age_seconds / 86400)
    if age_days > max_age_days:
        return {
            "tool": "grype",
            "status": "stale",
            "schema_version": schema,
            "built": built,
            "age_days": round(age_days, 2),
            "max_age_days": max_age_days,
            "network_access": False,
        }
    if not isinstance(database_path, str) or not database_path:
        return {
            "tool": "grype",
            "status": "invalid_metadata",
            "reason": "La ruta de la base no está presente.",
            "schema_version": schema,
            "built": built,
            "network_access": False,
        }
    path = Path(database_path).expanduser()
    if path.is_symlink() or not path.is_file():
        return {
            "tool": "grype",
            "status": "missing_or_invalid",
            "reason": "La ruta de la base no es un archivo regular local.",
            "schema_version": schema,
            "built": built,
            "network_access": False,
        }
    return {
        "tool": "grype",
        "status": "ready",
        "schema_version": schema,
        "built": built,
        "age_days": round(age_days, 2),
        "max_age_days": max_age_days,
        "database_path": str(path.resolve()),
        "network_access": False,
    }


def inspect_tool_database(tool_id: str, binary: str, *, environ=None) -> dict | None:
    """Return a fail-closed database status for tools that require local DBs."""
    if tool_id == "osv_scanner":
        return inspect_osv_database(environ=environ)
    if tool_id == "grype":
        return inspect_grype_database(binary, environ=environ)
    return None


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("osv_scanner", "grype", "all"), default="all")
    parser.add_argument("--json", action="store_true", help="Emite JSON legible por máquina.")
    args = parser.parse_args(argv)
    selected = ("osv_scanner", "grype") if args.tool == "all" else (args.tool,)
    results = []
    for tool_id in selected:
        if tool_id == "osv_scanner":
            results.append(inspect_osv_database())
        else:
            binary = shutil.which("grype")
            results.append(
                inspect_grype_database(binary) if binary else
                {"tool": "grype", "status": "binary_missing", "network_access": False}
            )
    ok = all(item["status"] in {"ready", "present_structure_checked"} for item in results)
    print(json.dumps({"ok": ok, "databases": results}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
