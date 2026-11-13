#!/usr/bin/env python3
"""Descargador verificable y reanudable de conocimientos para CYBER_AI.

La descarga está deshabilitada por defecto en el catálogo. Las fuentes
habilitadas solo pueden usar HTTPS público, sin proxies del entorno ni
redirecciones a otros hosts.
"""
import argparse
import fcntl
import hashlib
import ipaddress
import json
import re
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "data/knowledge_sources/download_catalog.json"
MANIFEST = ROOT / "data/knowledge_sources/download_manifest.json"
BASE = ROOT / "data/knowledge_base"
MAX_BYTES = 2 * 1024**3
HEADERS = {"User-Agent": "CYBER_AI-Knowledge-Downloader/1.0"}
TIMEOUT = (5, 30)
MAX_REDIRECTS = 3
ALLOWED_CONTENT_TYPES = (
    "text/html", "text/plain", "application/pdf",
    "application/x-pdf", "application/octet-stream",
)


def now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path, default):
    if not path.exists():
        return default
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"El archivo JSON debe contener un objeto: {path}")
    return data


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def used_bytes():
    if not BASE.exists():
        return 0
    total = 0
    for path in BASE.rglob("*"):
        if path.is_symlink():
            raise ValueError("La biblioteca contiene enlaces simbólicos; descarga bloqueada.")
        if path.is_file():
            total += path.stat().st_size
    return total


def _safe_destination(item, *, create=True):
    item_id = item.get("id")
    folder = item.get("folder")
    filename = item.get("filename")
    if not isinstance(item_id, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", item_id):
        raise ValueError("ID de recurso inválido.")
    if not isinstance(folder, str) or not folder or Path(folder).is_absolute():
        raise ValueError("Carpeta de destino inválida.")
    folder_parts = Path(folder).parts
    if any(part in {"", ".", ".."} for part in folder_parts):
        raise ValueError("La carpeta no puede salir de la biblioteca.")
    if not isinstance(filename, str) or filename in {"", ".", ".."} or Path(filename).name != filename:
        raise ValueError("Nombre de archivo inválido.")
    if "/" in filename or "\\" in filename:
        raise ValueError("El nombre de archivo no puede contener rutas.")
    if BASE.is_symlink():
        raise ValueError("La biblioteca base no puede ser un enlace simbólico.")
    if create:
        BASE.mkdir(parents=True, exist_ok=True)
    base = BASE.resolve(strict=create)
    if not base.is_relative_to(ROOT.resolve()):
        raise ValueError("La biblioteca base escapa del repositorio.")
    target_dir = base
    for part in folder_parts:
        target_dir = target_dir / part
        if target_dir.is_symlink():
            raise ValueError("No se permiten enlaces simbólicos en el destino.")
    if create:
        target_dir.mkdir(parents=True, exist_ok=True)
    resolved_dir = target_dir.resolve(strict=create)
    if not resolved_dir.is_relative_to(base):
        raise ValueError("El destino escapa de la biblioteca.")
    destination = resolved_dir / filename
    if destination.is_symlink():
        raise ValueError("El archivo de destino no puede ser un enlace simbólico.")
    return destination


def _validate_public_https(url, expected_host=None, *, resolve=True):
    if not isinstance(url, str) or any(ch.isspace() for ch in url):
        raise ValueError("URL de descarga inválida.")
    parsed = urlparse(url)
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError("Puerto URL inválido.") from error
    host = (parsed.hostname or "").rstrip(".").lower()
    if (
        parsed.scheme != "https" or not host or parsed.username or parsed.password
        or port not in (None, 443) or not parsed.path.startswith("/")
    ):
        raise ValueError("Solo se permiten URLs HTTPS públicas en el puerto 443.")
    if expected_host is not None and host != expected_host:
        raise ValueError("La redirección a otro host está bloqueada.")
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    if literal is not None:
        raise ValueError("No se permiten direcciones IP literales.")
    if not resolve:
        return host
    try:
        addresses = {entry[4][0] for entry in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)}
    except OSError as error:
        raise ValueError("No se pudo resolver el host de la fuente.") from error
    if not addresses:
        raise ValueError("El host no tiene direcciones resolubles.")
    for address in addresses:
        ip = ipaddress.ip_address(address.split("%", 1)[0])
        if not ip.is_global:
            raise ValueError("La fuente resuelve a una dirección no pública.")
    return host


def _request_public_resource(session, url):
    original_host = _validate_public_https(url)
    current = url
    for redirect_count in range(MAX_REDIRECTS + 1):
        _validate_public_https(current, expected_host=original_host)
        response = session.get(
            current, headers=HEADERS, stream=True, timeout=TIMEOUT,
            allow_redirects=False,
        )
        if response.status_code in {301, 302, 303, 307, 308}:
            location = response.headers.get("Location")
            response.close()
            if not location or redirect_count >= MAX_REDIRECTS:
                raise ValueError("Redirección ausente o límite de redirecciones excedido.")
            current = urljoin(current, location)
            continue
        response.raise_for_status()
        return response
    raise ValueError("No se pudo completar la descarga.")


def download(item, manifest, dry_run=False):
    if item.get("verified_for_download") is not True:
        return "not_verified"
    destination = _safe_destination(item, create=not dry_run)
    url = item.get("url")
    host = _validate_public_https(url, resolve=not dry_run)
    item_id = item["id"]
    state = manifest["resources"].get(item_id)
    if state is None:
        state = {} if dry_run else manifest["resources"].setdefault(item_id, {
            "status": "pending", "url": url, "updated_at": now(),
        })

    if destination.exists() and state.get("sha256"):
        if sha256(destination) == state["sha256"]:
            state.update(status="downloaded", updated_at=now())
            return "already_verified"

    limit = item.get("max_bytes", 20 * 1024**2)
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_BYTES:
        raise ValueError("max_bytes debe estar entre 1 byte y 2 GiB.")
    expected = item.get("expected_sha256")
    if expected is not None and (
        not isinstance(expected, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", expected)
    ):
        raise ValueError("expected_sha256 debe contener 64 caracteres hexadecimales.")

    if dry_run:
        print(f"[SIMULACIÓN] {item_id}: {url}")
        return "dry_run"

    session = requests.Session()
    session.trust_env = False
    response = None
    temp = destination.with_name(destination.name + ".part")
    try:
        response = _request_public_resource(session, url)
        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if not any(value == content_type for value in ALLOWED_CONTENT_TYPES):
            raise ValueError(f"Tipo de contenido no permitido: {content_type}")
        raw_length = response.headers.get("Content-Length")
        if raw_length:
            try:
                declared = int(raw_length)
            except ValueError as error:
                raise ValueError("Content-Length inválido.") from error
            if declared < 0 or declared > limit:
                raise ValueError("El archivo supera el tamaño máximo permitido.")

        initial_used = used_bytes()
        received = 0
        with temp.open("xb") as stream:
            for block in response.iter_content(64 * 1024):
                if not block:
                    continue
                received += len(block)
                if received > limit:
                    raise ValueError("Se superó el límite del recurso.")
                if initial_used + received > MAX_BYTES:
                    raise ValueError("Se alcanzó el límite global de 2 GB.")
                stream.write(block)

        if received < 100:
            raise ValueError("Respuesta demasiado pequeña para ser un recurso.")
        if destination.suffix.lower() == ".pdf" or content_type in {"application/pdf", "application/x-pdf"}:
            with temp.open("rb") as check:
                if b"%PDF-" not in check.read(1024):
                    raise ValueError("El contenido no tiene una cabecera PDF válida.")

        digest = sha256(temp)
        if expected is not None and digest.lower() != expected.lower():
            raise ValueError("El SHA-256 descargado no coincide con el esperado.")
        temp.replace(destination)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    finally:
        if response is not None:
            response.close()
        session.close()

    state.update({
        "status": "downloaded", "url": url,
        "final_host": host,
        "file": str(destination.relative_to(ROOT)),
        "bytes": received, "sha256": sha256(destination),
        "content_type": content_type, "downloaded_at": now(),
        "updated_at": now(), "license": item.get("license", "REVISAR"),
    })
    return "downloaded"


def _run(args):

    catalog = load_json(CATALOG, {"areas": [], "resources": []})
    manifest = load_json(MANIFEST, {
        "version": 1, "created_at": now(), "updated_at": now(),
        "global_limit_bytes": MAX_BYTES, "resources": {},
    })
    if not isinstance(manifest.get("resources"), dict) or any(
        not isinstance(value, dict) for value in manifest["resources"].values()
    ):
        raise ValueError("El manifiesto no contiene un mapa de recursos válido.")

    resources = catalog.get("resources", [])
    if not isinstance(resources, list):
        raise ValueError("El catálogo debe contener una lista de recursos.")
    invalid_resources = sum(not isinstance(item, dict) for item in resources)
    errors = invalid_resources
    if invalid_resources:
        print(f"Recursos inválidos omitidos: {invalid_resources}")
    resources = [item for item in resources if isinstance(item, dict)]
    if args.area:
        resources = [item for item in resources if item.get("area_id") == args.area]

    verified_count = sum(1 for item in resources if item.get("verified_for_download") is True)
    print(f"Recursos en catálogo: {len(resources)}")
    print(f"Fuentes verificadas: {verified_count}")
    print(f"Espacio usado por la biblioteca: {used_bytes() / 1024**2:.1f} MB")
    print(f"Límite de descarga: {MAX_BYTES / 1024**3:.1f} GB")

    for item in resources:
        if not isinstance(item, dict):
            print("[ERROR] Recurso inválido en catálogo")
            continue
        if item.get("verified_for_download") is not True:
            print(f"[NO VERIFICADO] {item.get('id', 'sin-id')}: se omite")
            continue
        state = manifest["resources"].get(item.get("id"), {})
        if state.get("status") == "downloaded":
            print(f"[OMITIDO] {item['id']}: ya descargado")
            continue
        if state.get("status") == "failed" and not args.retry_failed:
            print(f"[PENDIENTE DE REINTENTO] {item['id']}")
            continue
        try:
            result = download(item, manifest, args.dry_run)
            print(f"[{result.upper()}] {item['id']}")
        except Exception as error:
            errors += 1
            if not args.dry_run:
                manifest["resources"].setdefault(item.get("id", "invalid"), {}).update({
                    "status": "failed", "error": str(error), "updated_at": now(),
                })
            print(f"[ERROR] {item.get('id', 'sin-id')}: {error}")
        finally:
            if not args.dry_run:
                manifest["updated_at"] = now()
                save_json(MANIFEST, manifest)
            time.sleep(0.3)

    if args.dry_run:
        print("\nSimulación finalizada; no se modificó el manifiesto.")
    else:
        print(f"\nRegistro actualizado: {MANIFEST}")
    return 1 if errors else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--area", help="Descargar solo un identificador de área")
    parser.add_argument("--retry-failed", action="store_true")
    args = parser.parse_args(argv)

    lock_path = MANIFEST.with_suffix(MANIFEST.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            return _run(args)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


if __name__ == "__main__":
    main()
