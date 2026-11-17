#!/usr/bin/env python3
"""Crea/verifica checkpoints HMAC externos para anclar la cadena del ledger."""
import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from execution_ledger import ExecutionLedger, GENESIS

SCHEMA = "cyber-ai-ledger-checkpoint-v1"
KEY_ENV = "CYBER_AI_LEDGER_CHECKPOINT_KEY"


class CheckpointError(ValueError):
    pass


def _key(environ=None):
    environ = os.environ if environ is None else environ
    value = environ.get(KEY_ENV, "")
    if len(value.encode("utf-8")) < 32:
        raise CheckpointError(f"{KEY_ENV} debe contener al menos 32 bytes y mantenerse fuera del repositorio.")
    return value.encode("utf-8")


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def create_checkpoint(output, *, ledger=None, environ=None):
    key = _key(environ)
    ledger = ledger or ExecutionLedger()
    state = ledger.verify()
    if not state.get("valid") or state.get("checked", 0) < 1:
        raise CheckpointError("No se puede anclar un ledger vacío o con integridad inválida.")
    with ledger.connect() as db:
        row = db.execute(
            "SELECT sequence,event_hash FROM execution_events ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
    payload = {
        "schema": SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sequence": row["sequence"],
        "head_hash": row["event_hash"],
    }
    signature = hmac.new(key, _canonical(payload).encode("utf-8"), hashlib.sha256).hexdigest()
    document = {**payload, "hmac_sha256": signature}
    destination = Path(output)
    if destination.exists() or destination.is_symlink():
        raise CheckpointError("El archivo checkpoint ya existe; no se sobrescriben anclajes.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.chmod(temporary, 0o600)
        except OSError:
            pass
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return {"checkpoint": str(destination), "sequence": row["sequence"],
            "head_hash": row["event_hash"], "signed": True}


def verify_checkpoint(checkpoint, *, ledger=None, environ=None):
    key = _key(environ)
    path = Path(checkpoint)
    if path.is_symlink() or not path.is_file():
        raise CheckpointError("El checkpoint debe ser un archivo regular.")
    if path.stat().st_size > 16 * 1024:
        raise CheckpointError("Checkpoint demasiado grande.")
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        raise CheckpointError("Esquema de checkpoint inválido.")
    signature = document.get("hmac_sha256")
    payload = {k: v for k, v in document.items() if k != "hmac_sha256"}
    expected = hmac.new(key, _canonical(payload).encode("utf-8"), hashlib.sha256).hexdigest()
    if not isinstance(signature, str) or not hmac.compare_digest(expected, signature):
        raise CheckpointError("Firma HMAC del checkpoint inválida.")
    sequence = payload.get("sequence")
    head_hash = payload.get("head_hash")
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
        raise CheckpointError("Secuencia de checkpoint inválida.")
    if not isinstance(head_hash, str) or len(head_hash) != 64:
        raise CheckpointError("Hash de checkpoint inválido.")
    ledger = ledger or ExecutionLedger()
    state = ledger.verify()
    if not state.get("valid") or state.get("checked", 0) < sequence:
        raise CheckpointError("Ledger inválido o retrocedido respecto al checkpoint.")
    with ledger.connect() as db:
        row = db.execute(
            "SELECT event_hash FROM execution_events WHERE sequence=?", (sequence,)
        ).fetchone()
    if row is None or not hmac.compare_digest(row["event_hash"], head_hash):
        raise CheckpointError("La cadena actual no contiene el anclaje firmado.")
    return {"valid": True, "sequence": sequence, "head_hash": head_hash,
            "current_sequence": state["checked"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--output", type=Path, required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--checkpoint", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = (
            create_checkpoint(args.output) if args.command == "create"
            else verify_checkpoint(args.checkpoint)
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
