#!/usr/bin/env python3
"""Auditoría de solo lectura del ciclo ledger -> memoria -> Skills."""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from execution_ledger import DEFAULT_DB, ExecutionLedger
import learning_memory
import skillbook


def _memory_line_count(path: Path) -> int:
    if path.is_symlink() or path.parent.is_symlink():
        raise OSError("La ruta de memoria contiene un enlace simbólico.")
    if not path.is_file():
        return 0
    with path.open("rb") as stream:
        return sum(1 for _ in stream)


def audit_learning_cycle(*, max_review_age_days: int = 180) -> dict:
    """Inspecciona integridad y coherencia sin modificar eventos ni Skills."""
    ledger_path = Path(os.environ.get("CYBER_AI_LEDGER_PATH", DEFAULT_DB))
    if ledger_path.is_symlink():
        raise OSError("El archivo del ledger no puede ser un enlace simbólico.")
    if ledger_path.is_file():
        ledger = ExecutionLedger(ledger_path, initialize=False)
        ledger_check = ledger.verify()
    else:
        ledger = None
        ledger_check = {"valid": False, "checked": 0, "reason": "database_missing"}
    namespaces = ledger.namespaces() if ledger and ledger_check.get("valid") else []
    event_counts = Counter()
    orphaned_starts = []
    history_truncated = []

    if ledger_check.get("valid"):
        for namespace in namespaces:
            events = ledger.history(namespace=namespace, limit=1000)
            event_counts.update(item.get("status", "unknown") for item in events)
            if len(events) == 1000:
                history_truncated.append(namespace)
            closed = {
                (item.get("metadata") or {}).get("start_event_id")
                for item in events
                if item.get("status") != "started"
            }
            for item in events:
                if item.get("status") == "started" and item.get("event_id") not in closed:
                    orphaned_starts.append({
                        "event_id": item.get("event_id"),
                        "namespace": namespace,
                        "created_at": item.get("created_at"),
                        "tool": item.get("tool"),
                    })

    memory_key_configured = len(
        os.environ.get(learning_memory.APPROVAL_KEY_ENV, "").encode("utf-8")
    ) >= 32
    memory = {
        "approval_key_configured": memory_key_configured,
        "status": "disabled_missing_approval_key",
        "records_on_disk": None,
        "verified_records": 0,
        "rejected_or_unverifiable_records": None,
    }
    try:
        records_on_disk = _memory_line_count(learning_memory.MEMORY_FILE)
        memory["records_on_disk"] = records_on_disk
        if memory_key_configured:
            verified = learning_memory.read_lessons()
            memory.update({
                "status": "verified" if len(verified) == records_on_disk else "degraded",
                "verified_records": len(verified),
                "rejected_or_unverifiable_records": max(0, records_on_disk - len(verified)),
            })
    except (OSError, RuntimeError, ValueError) as error:
        memory.update({"status": "error", "error": str(error)[:300]})

    skill_db_path = Path(skillbook.DB_PATH)
    if skill_db_path.is_symlink():
        raise OSError("La base de Skills no puede ser un enlace simbólico.")
    rows = []
    invalid_skills = []
    due_for_review = []
    if skill_db_path.is_file():
        with skillbook.connect() as db:
            tables = {
                row["name"] for row in db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
            if "skills" not in tables or "skill_versions" not in tables:
                invalid_skills.append({
                    "skill_id": None, "name": None, "status": None,
                    "reason": "skillbook_schema_missing", "fields": [],
                })
            else:
                rows = db.execute(
                    "SELECT skill_id,name,status,version,updated_at FROM skills ORDER BY skill_id"
                ).fetchall()
                for row in rows:
                    result = skillbook._verify_skill_history_in_db(db, row["skill_id"])
                    if not result.get("valid") or result.get("status") != row["status"]:
                        invalid_skills.append({
                            "skill_id": row["skill_id"],
                            "name": row["name"],
                            "status": row["status"],
                            "reason": result.get("reason", "status_mismatch"),
                            "fields": result.get("fields", []),
                        })
                cutoff = datetime.now(timezone.utc) - timedelta(days=max_review_age_days)
                for row in rows:
                    if row["status"] != "active":
                        continue
                    try:
                        updated = datetime.fromisoformat(
                            row["updated_at"].replace("Z", "+00:00")
                        )
                        if updated.tzinfo is None:
                            updated = updated.replace(tzinfo=timezone.utc)
                    except (TypeError, ValueError, AttributeError):
                        due_for_review.append({
                            "skill_id": row["skill_id"], "name": row["name"],
                            "version": row["version"], "reason": "invalid_review_timestamp",
                            "review_due_at": None,
                        })
                        continue
                    if updated < cutoff:
                        due_for_review.append({
                            "skill_id": row["skill_id"], "name": row["name"],
                            "version": row["version"], "reason": "review_age_exceeded",
                            "review_due_at": updated.isoformat(),
                        })
    skill_counts = Counter(row["status"] for row in rows)
    ledger_ok = bool(ledger_check.get("valid"))
    skills_ok = not invalid_skills
    memory_ok = (
        memory["status"] == "verified"
        or (
            memory["status"] == "disabled_missing_approval_key"
            and memory.get("records_on_disk") == 0
        )
    )
    status = "ok" if ledger_ok and skills_ok and memory_ok and not orphaned_starts else "degraded"

    return {
        "schema": "cyber-ai-learning-cycle-audit-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "read_only": True,
        "paths": {
            "ledger": str(ledger_path),
            "skillbook": str(skill_db_path),
            "memory": str(learning_memory.MEMORY_FILE),
        },
        "ledger": {
            **ledger_check,
            "namespaces": len(namespaces),
            "events_by_status": dict(sorted(event_counts.items())),
            "history_truncated_namespaces": history_truncated,
            "orphaned_started_events": orphaned_starts,
        },
        "memory": memory,
        "skills": {
            "total": len(rows),
            "by_status": dict(sorted(skill_counts.items())),
            "invalid_histories": invalid_skills,
            "due_for_review": due_for_review,
            "review_age_days": max_review_age_days,
        },
        "limitations": [
            "La auditoría verifica trazabilidad e integridad local; no juzga la calidad semántica de una lección o metodología.",
            "La ausencia de la clave VERITAS deshabilita la lectura de memoria, pero no demuestra que el archivo esté vacío.",
            "Los eventos iniciados recientes pueden ser ejecuciones activas; no se reconcilian ni modifican.",
        ],
    }


def write_report(report: dict, destination: Path) -> Path:
    """Escribe un informe JSON con publicación atómica y permisos privados."""
    if destination.is_symlink() or destination.parent.is_symlink():
        raise OSError("La ruta del informe no puede contener enlaces simbólicos.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.is_symlink():
        raise OSError("El directorio del informe no puede ser un enlace simbólico.")
    temporary = destination.with_name(destination.name + ".tmp")
    if temporary.is_symlink():
        raise OSError("El archivo temporal no puede ser un enlace simbólico.")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(temporary, flags, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
        if os.name == "posix":
            os.chmod(destination, 0o600)
    except Exception:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return destination


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-review-age-days", type=int, default=180)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = audit_learning_cycle(
            max_review_age_days=args.max_review_age_days
        )
        if args.output:
            path = write_report(report, args.output)
            print("Informe:", path)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "ok" else 1
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
