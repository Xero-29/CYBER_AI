#!/usr/bin/env python3
"""Descargador verificable y reanudable de conocimientos para CYBER_AI."""

import argparse
import hashlib
import json
import os
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "data/knowledge_sources/download_catalog.json"
MANIFEST = ROOT / "data/knowledge_sources/download_manifest.json"
BASE = ROOT / "data/knowledge_base"
MAX_BYTES = 2 * 1024**3
HEADERS = {"User-Agent": "CYBER_AI-Knowledge-Downloader/1.0"}
TIMEOUT = 30


def now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp.replace(path)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def used_bytes():
    total = 0
    for path in BASE.rglob("*"):
        if path.is_file():
            total += path.stat().st_size
    return total


def download(item, manifest, dry_run=False):
    if item.get("verified_for_download") is not True:
        return "not_verified"
    item_id = item["id"]
    target_dir = BASE / item["folder"]
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / item["filename"]
    state = manifest["resources"].setdefault(item_id, {
        "status": "pending",
        "url": item["url"],
        "updated_at": now(),
    })

    if destination.exists() and state.get("sha256"):
        if sha256(destination) == state["sha256"]:
            state.update(status="downloaded", updated_at=now())
            return "already_verified"

    if dry_run:
        print(f"[SIMULACIÓN] {item_id}: {item['url']}")
        return "dry_run"

    response = requests.get(
        item["url"], headers=HEADERS, stream=True, timeout=TIMEOUT
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()
    allowed_types = (
        "text/html",
        "text/plain",
        "application/pdf",
        "application/x-pdf",
        "application/octet-stream",
    )
    if not any(value in content_type for value in allowed_types):
        raise ValueError(f"Tipo de contenido no permitido: {content_type}")

    declared = int(response.headers.get("Content-Length", "0") or 0)
    if declared and declared > item.get("max_bytes", 20 * 1024**2):
        raise ValueError("El archivo supera el tamaño máximo permitido.")

    temp = destination.with_suffix(destination.suffix + ".part")
    received = 0
    limit = item.get("max_bytes", 20 * 1024**2)
    initial_used = used_bytes()

    try:
        with temp.open("wb") as stream:
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

        if destination.suffix.lower() == ".pdf":
            with temp.open("rb") as check:
                header = check.read(1024)
            if b"%PDF-" not in header:
                raise ValueError("El archivo tiene extensión PDF, pero no contiene una cabecera PDF válida.")
        elif "application/pdf" in content_type or "application/x-pdf" in content_type:
            with temp.open("rb") as check:
                header = check.read(1024)
            if b"%PDF-" not in header:
                raise ValueError("El servidor indicó PDF, pero el contenido no es un PDF válido.")

        temp.replace(destination)
    except Exception:
        temp.unlink(missing_ok=True)
        raise

    state.update({
        "status": "downloaded",
        "url": item["url"],
        "file": str(destination.relative_to(ROOT)),
        "bytes": received,
        "sha256": sha256(destination),
        "content_type": content_type,
        "downloaded_at": now(),
        "updated_at": now(),
        "license": item.get("license", "REVISAR"),
    })
    return "downloaded"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--area", help="Descargar solo un identificador de área")
    parser.add_argument("--retry-failed", action="store_true")
    args = parser.parse_args()

    catalog = load_json(CATALOG, {"areas": [], "resources": []})
    manifest = load_json(MANIFEST, {
        "version": 1,
        "created_at": now(),
        "updated_at": now(),
        "global_limit_bytes": MAX_BYTES,
        "resources": {},
    })

    resources = catalog.get("resources", [])
    if args.area:
        resources = [r for r in resources if r["area_id"] == args.area]

    verified_count = sum(
        1 for item in resources
        if item.get("verified_for_download") is True
    )
    print(f"Recursos en catálogo: {len(resources)}")
    print(f"Fuentes verificadas: {verified_count}")
    print(f"Espacio usado por la biblioteca: {used_bytes() / 1024**2:.1f} MB")
    print(f"Límite de descarga: {MAX_BYTES / 1024**3:.1f} GB")

    for item in resources:
        if item.get("verified_for_download") is not True:
            print(f"[NO VERIFICADO] {item['id']}: se omite")
            continue
        state = manifest["resources"].get(item["id"], {})
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
            manifest["resources"].setdefault(item["id"], {}).update({
                "status": "failed",
                "error": str(error),
                "updated_at": now(),
            })
            print(f"[ERROR] {item['id']}: {error}")
        finally:
            manifest["updated_at"] = now()
            save_json(MANIFEST, manifest)
            time.sleep(0.3)

    print(f"\nRegistro actualizado: {MANIFEST}")


if __name__ == "__main__":
    main()
