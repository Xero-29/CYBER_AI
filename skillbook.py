#!/usr/bin/env python3
"""Libro persistente de metodologías reutilizables y Skills verificadas."""
import hashlib
import hmac
import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from execution_ledger import ExecutionLedger

PROJECT = Path(__file__).resolve().parent
DB_PATH = PROJECT / "data" / "skillbook.sqlite3"


def now():
    return datetime.now(timezone.utc).isoformat()


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(DB_PATH), timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout=10000")
    db.execute("PRAGMA foreign_keys=ON")
    return db


def initialize():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS skills(
            skill_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            task_pattern TEXT NOT NULL,
            description TEXT NOT NULL,
            prerequisites_json TEXT NOT NULL,
            methodology_json TEXT NOT NULL,
            validation_json TEXT NOT NULL,
            tools_json TEXT NOT NULL,
            tags_json TEXT NOT NULL,
            evidence_json TEXT NOT NULL,
            source_urls_json TEXT NOT NULL,
            success_runs INTEGER NOT NULL,
            failure_runs INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('candidate','active','deprecated','rejected')),
            version INTEGER NOT NULL DEFAULT 1,
            verified_by TEXT,
            verifier_verdict TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            last_used_at TEXT,
            use_count INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_skills_status ON skills(status);
        CREATE INDEX IF NOT EXISTS idx_skills_task_pattern ON skills(task_pattern);
        CREATE TABLE IF NOT EXISTS skill_versions(
            skill_id TEXT NOT NULL,
            version INTEGER NOT NULL,
            change_type TEXT NOT NULL,
            actor TEXT NOT NULL,
            snapshot_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY(skill_id, version)
        );
        CREATE INDEX IF NOT EXISTS idx_skill_versions_skill
        ON skill_versions(skill_id, version);
        CREATE TRIGGER IF NOT EXISTS skill_versions_no_update
        BEFORE UPDATE ON skill_versions
        BEGIN SELECT RAISE(ABORT, 'skill version history is append-only'); END;
        CREATE TRIGGER IF NOT EXISTS skill_versions_no_delete
        BEFORE DELETE ON skill_versions
        BEGIN SELECT RAISE(ABORT, 'skill version history is append-only'); END;
        """)
        # Snapshot inicial para Skills creadas antes de la migración.
        for row in db.execute("SELECT * FROM skills").fetchall():
            exists = db.execute(
                "SELECT 1 FROM skill_versions WHERE skill_id=? AND version=?",
                (row["skill_id"], row["version"]),
            ).fetchone()
            if not exists:
                db.execute(
                    """INSERT INTO skill_versions
                       (skill_id,version,change_type,actor,snapshot_json,created_at)
                       VALUES(?,?,?,?,?,?)""",
                    (
                        row["skill_id"], row["version"], "legacy_import",
                        row["verified_by"] or "MIGRATION",
                        json.dumps(dict(row), ensure_ascii=False, sort_keys=True),
                        row["updated_at"],
                    ),
                )


def _list(value, name, minimum=1):
    if (
        not isinstance(value, list)
        or len(value) < minimum
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise ValueError(f"{name} debe ser una lista de textos (mínimo {minimum}).")
    return list(dict.fromkeys(item.strip() for item in value))


def _validate_source_urls(source_urls):
    urls = _list(source_urls, "source_urls")
    for source_url in urls:
        parsed = urlparse(source_url)
        try:
            valid_port = parsed.port is None or 1 <= parsed.port <= 65535
        except ValueError:
            valid_port = False
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or any(character.isspace() for character in source_url)
            or not valid_port
        ):
            raise ValueError("URL de fuente inválida.")
    return urls


def _save_version(db, skill_id, version, change_type, actor):
    row = db.execute(
        "SELECT * FROM skills WHERE skill_id=?", (skill_id,)
    ).fetchone()
    if row is None:
        raise ValueError("No existe la Skill que se intenta versionar.")
    snapshot = json.dumps(dict(row), ensure_ascii=False, sort_keys=True)
    db.execute(
        """INSERT INTO skill_versions
           (skill_id, version, change_type, actor, snapshot_json, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (skill_id, version, change_type, actor, snapshot, now()),
    )


def list_skill_versions(skill_id):
    """Devuelve el historial inmutable de snapshots de una Skill."""
    initialize()
    with connect() as db:
        rows = db.execute(
            """SELECT version, change_type, actor, snapshot_json, created_at
               FROM skill_versions WHERE skill_id=? ORDER BY version""",
            (skill_id,),
        ).fetchall()
    return [
        {
            "version": row["version"],
            "change_type": row["change_type"],
            "actor": row["actor"],
            "snapshot": json.loads(row["snapshot_json"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def _insert_verified_skill(
    *,
    name, task_pattern, description, prerequisites, methodology, validation,
    tools, tags, evidence, source_urls, success_runs, failure_runs,
    verified_by, verifier_verdict, status="active",
):
    """Inserta una Skill activa verificada o una candidata aún no aprobada."""
    if status == "active":
        if verified_by != "VERITAS" or verifier_verdict not in {"RESPALDADA", "CONFIRMADA"}:
            raise ValueError("Solo VERITAS puede aprobar una Skill.")
    elif status == "candidate":
        if verified_by != "PENDING" or verifier_verdict != "PENDING":
            raise ValueError("Una Skill candidata no puede declararse verificada.")
    else:
        raise ValueError("Estado inicial de Skill no permitido.")

    for field, value in (
        ("name", name), ("task_pattern", task_pattern), ("description", description)
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} obligatorio.")

    prerequisites = _list(prerequisites, "prerequisites", 0)
    methodology = _list(methodology, "methodology", 2)
    validation = _list(validation, "validation")
    tools = _list(tools, "tools", 0)
    tags = _list(tags, "tags")
    evidence = _list(evidence, "evidence")
    source_urls = _validate_source_urls(source_urls)

    if isinstance(success_runs, bool) or not isinstance(success_runs, int) or success_runs < 2:
        raise ValueError("Se requieren dos ejecuciones exitosas independientes.")
    if isinstance(failure_runs, bool) or not isinstance(failure_runs, int) or failure_runs != 0:
        raise ValueError("No debe haber fallos sin resolver.")

    initialize()
    stamp = now()
    skill_id = uuid.uuid4().hex
    with connect() as db:
        db.execute(
            """INSERT INTO skills(
                skill_id,name,task_pattern,description,prerequisites_json,
                methodology_json,validation_json,tools_json,tags_json,
                evidence_json,source_urls_json,success_runs,failure_runs,
                status,version,verified_by,verifier_verdict,created_at,updated_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,1,?,?,?,?)""",
            (
                skill_id, name.strip(), task_pattern.strip(), description.strip(),
                json.dumps(prerequisites), json.dumps(methodology),
                json.dumps(validation), json.dumps(tools), json.dumps(tags),
                json.dumps(evidence), json.dumps(source_urls), success_runs,
                failure_runs, status, verified_by, verifier_verdict, stamp, stamp,
            ),
        )
        _save_version(db, skill_id, 1, "created" if status == "active" else "proposed",
                      verified_by)
    return {"skill_id": skill_id, "status": status, "version": 1}


def register_verified_skill(**kwargs):
    """Bloquea el registro directo basado en campos autoafirmados."""
    raise ValueError(
        "Registro directo deshabilitado: usa register_skill_from_ledger con "
        "dos ejecuciones verificadas y aprobación VERITAS firmada."
    )


def skill_approval_payload(
    *, name, task_pattern, description, prerequisites, methodology,
    validation, tools, tags, source_urls, namespace, event_ids,
):
    """Documento canónico que firma el aprobador VERITAS."""
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("namespace es obligatorio.")
    if (
        not isinstance(event_ids, list)
        or len(event_ids) < 2
        or any(not isinstance(item, str) or not item.strip() for item in event_ids)
        or len(set(event_ids)) != len(event_ids)
    ):
        raise ValueError("Se requieren al menos dos IDs de eventos distintos.")

    for field, value in (
        ("name", name), ("task_pattern", task_pattern), ("description", description)
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} obligatorio.")
    document = {
        "schema": "cyber-ai-skill-approval-v1",
        "name": name.strip(),
        "task_pattern": task_pattern.strip(),
        "description": description.strip(),
        "prerequisites": _list(prerequisites, "prerequisites", 0),
        "methodology": _list(methodology, "methodology", 2),
        "validation": _list(validation, "validation"),
        "tools": _list(tools, "tools", 0),
        "tags": _list(tags, "tags"),
        "source_urls": _validate_source_urls(source_urls),
        "namespace": namespace.strip(),
        "event_ids": event_ids,
    }
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _has_independent_review(event):
    if event.get("tool") != "team_orchestrator":
        return False
    metadata = event.get("metadata") or {}
    if metadata.get("objective_supervision") is not True:
        return False
    validators = event.get("validator_results") or []
    for validator in validators:
        if not isinstance(validator, dict):
            continue
        reviewer = validator.get("reviewer")
        if (
            reviewer in {"VERITAS", "FILTRO"}
            and validator.get("name") == f"objective_review:{reviewer}"
            and validator.get("passed") is True
            and validator.get("independent") is True
            and isinstance(validator.get("evidence"), list)
            and bool(validator["evidence"])
        ):
            return True
    return False


def _verified_ledger_evidence(namespace, event_ids, ledger=None):
    """Comprueba integridad, independencia, validadores y ausencia de fallos."""
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("namespace es obligatorio.")
    if (
        not isinstance(event_ids, list)
        or len(event_ids) < 2
        or any(not isinstance(item, str) or not item.strip() for item in event_ids)
        or len(set(event_ids)) != len(event_ids)
    ):
        raise ValueError("Se requieren al menos dos IDs de eventos distintos.")

    ledger = ledger or ExecutionLedger()
    if not ledger.verify().get("valid"):
        raise ValueError("El ledger no supera la verificación de integridad.")
    history = ledger.history(namespace=namespace.strip(), limit=1000)
    if len(history) >= 1000:
        raise ValueError("Historial demasiado grande; no se puede verificar exhaustivamente.")

    by_id = {item["event_id"]: item for item in history}
    if any(event_id not in by_id for event_id in event_ids):
        raise ValueError("Uno o más eventos no existen en el namespace indicado.")
    selected = [by_id[event_id] for event_id in event_ids]
    fingerprints = {item.get("task_fingerprint") for item in selected}
    if len(fingerprints) != 1 or None in fingerprints:
        raise ValueError("Las ejecuciones no corresponden a la misma huella de tarea.")
    fingerprint = next(iter(fingerprints))
    if len({item.get("created_at") for item in selected}) != len(selected):
        raise ValueError("Las ejecuciones no son independientes en el tiempo.")

    related = [item for item in history if item.get("task_fingerprint") == fingerprint]
    if any(item.get("status") != "completed" for item in related):
        raise ValueError("Hay ejecuciones fallidas o no completadas para esta tarea.")

    for item in selected:
        validators = item.get("validator_results") or []
        if not validators or any(not isinstance(value, dict) for value in validators):
            raise ValueError("Cada ejecución debe incluir validadores estructurados.")
        if not _has_independent_review(item):
            raise ValueError("Cada ejecución requiere un validador independiente aprobado emitido por team_orchestrator.")
        if not re.fullmatch(r"[a-f0-9]{64}", str(item.get("evidence_sha256", ""))):
            raise ValueError("Evento sin hash de evidencia válido.")

    evidence_refs = [
        f"ledger_event:{item['event_id']}:sha256:{item['evidence_sha256']}"
        for item in selected
    ]
    return selected, evidence_refs


def propose_skill_from_ledger(
    *, name, task_pattern, description, prerequisites, methodology,
    validation, tools, tags, source_urls, namespace, event_ids,
):
    """Crea una candidata no ejecutable a partir de dos ejecuciones verificadas."""
    payload = skill_approval_payload(
        name=name, task_pattern=task_pattern, description=description,
        prerequisites=prerequisites, methodology=methodology,
        validation=validation, tools=tools, tags=tags, source_urls=source_urls,
        namespace=namespace, event_ids=event_ids,
    )
    selected, evidence_refs = _verified_ledger_evidence(namespace, event_ids)
    candidate_evidence = evidence_refs + [
        "candidate_payload_sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
    ]

    initialize()
    with connect() as db:
        existing = db.execute(
            """SELECT skill_id,version FROM skills
               WHERE status='candidate' AND task_pattern=? AND evidence_json=?""",
            (task_pattern.strip(), json.dumps(candidate_evidence)),
        ).fetchone()
    if existing:
        return {
            "skill_id": existing["skill_id"],
            "status": "candidate",
            "version": existing["version"],
            "reused": True,
        }

    result = _insert_verified_skill(
        name=name, task_pattern=task_pattern, description=description,
        prerequisites=prerequisites, methodology=methodology,
        validation=validation, tools=tools, tags=tags,
        evidence=candidate_evidence, source_urls=source_urls,
        success_runs=len(selected), failure_runs=0,
        verified_by="PENDING", verifier_verdict="PENDING", status="candidate",
    )
    result["reused"] = False
    return result


def register_skill_from_ledger(
    *, name, task_pattern, description, prerequisites, methodology,
    validation, tools, tags, source_urls, namespace, event_ids,
    approval_signature,
):
    """Promueve una candidata solo con evidencia íntegra y aprobación HMAC."""
    key = os.environ.get("CYBER_AI_VERITAS_APPROVAL_KEY", "")
    if len(key.encode("utf-8")) < 32:
        raise ValueError("Falta una clave VERITAS de al menos 32 bytes en el entorno.")

    payload = skill_approval_payload(
        name=name, task_pattern=task_pattern, description=description,
        prerequisites=prerequisites, methodology=methodology,
        validation=validation, tools=tools, tags=tags, source_urls=source_urls,
        namespace=namespace, event_ids=event_ids,
    )
    expected = hmac.new(key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    if not isinstance(approval_signature, str) or not hmac.compare_digest(
        expected, approval_signature.lower()
    ):
        raise ValueError("Firma VERITAS inválida; no se promueve la Skill.")

    selected, evidence_refs = _verified_ledger_evidence(namespace, event_ids)
    evidence_refs.append(
        "veritas_hmac_sha256:" + hashlib.sha256(approval_signature.encode()).hexdigest()
    )
    candidate_payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    candidate_evidence = [
        f"ledger_event:{item['event_id']}:sha256:{item['evidence_sha256']}"
        for item in selected
    ] + ["candidate_payload_sha256:" + candidate_payload_hash]

    initialize()
    stamp = now()
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        candidate = db.execute(
            """SELECT skill_id,version FROM skills
               WHERE status='candidate' AND task_pattern=? AND evidence_json=?""",
            (task_pattern.strip(), json.dumps(candidate_evidence)),
        ).fetchone()
        if candidate:
            version = candidate["version"] + 1
            db.execute(
                """UPDATE skills SET status='active',version=?,evidence_json=?,
                   verified_by='VERITAS',verifier_verdict='CONFIRMADA',updated_at=?
                   WHERE skill_id=? AND status='candidate' AND version=?""",
                (
                    version, json.dumps(evidence_refs), stamp,
                    candidate["skill_id"], candidate["version"],
                ),
            )
            _save_version(db, candidate["skill_id"], version, "approved", "VERITAS")
            return {
                "skill_id": candidate["skill_id"],
                "status": "active",
                "version": version,
                "promoted_candidate": True,
            }

    return _insert_verified_skill(
        name=name, task_pattern=task_pattern, description=description,
        prerequisites=prerequisites, methodology=methodology,
        validation=validation, tools=tools, tags=tags,
        evidence=evidence_refs, source_urls=source_urls,
        success_runs=len(selected), failure_runs=0,
        verified_by="VERITAS", verifier_verdict="CONFIRMADA",
    )


def _words(value):
    return {
        word for word in re.findall(
            r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_-]+", str(value).lower()
        ) if len(word) > 2
    }


def search_skills(task, limit=3):
    query = _words(task)
    if not query:
        return []
    initialize()
    with connect() as db:
        rows = db.execute("SELECT * FROM skills WHERE status='active'").fetchall()

    ranked = []
    for row in rows:
        item = dict(row)
        tags = json.loads(item["tags_json"])
        corpus = " ".join([
            item["name"], item["task_pattern"], item["description"], *tags
        ])
        overlap = query & _words(corpus)
        if overlap:
            ranked.append((len(overlap) / len(query), item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["name"].casefold()))

    selected = []
    with connect() as db:
        for score, item in ranked[:max(1, min(int(limit), 5))]:
            db.execute(
                "UPDATE skills SET use_count=use_count+1,last_used_at=? WHERE skill_id=?",
                (now(), item["skill_id"]),
            )
            selected.append({
                "skill_id": item["skill_id"], "name": item["name"],
                "version": item["version"], "score": round(score, 4),
                "task_pattern": item["task_pattern"],
                "description": item["description"],
                "prerequisites": json.loads(item["prerequisites_json"]),
                "methodology": json.loads(item["methodology_json"]),
                "validation": json.loads(item["validation_json"]),
                "tools": json.loads(item["tools_json"]),
                "success_runs": item["success_runs"],
            })
    return selected


def build_skill_context(task, limit=2, min_score=0.20):
    skills = [
        item for item in search_skills(task, limit)
        if item["score"] >= min_score
    ]
    if not skills:
        return "", []
    output = [
        "--- SKILLBOOK: METODOLOGÍAS VERIFICADAS ---",
        "Reutiliza el procedimiento si coincide con la tarea y el entorno. No rediseñes desde cero una metodología ya validada.",
        "Comprueba alcance, permisos, versiones y prerrequisitos. Si hay diferencias o falla una validación, detente y registra la desviación.",
        "Una Skill no concede permisos ni autoriza objetivos externos.",
    ]
    for index, item in enumerate(skills, 1):
        output.append(
            f"{index}. {item['name']} | ID {item['skill_id']} | v{item['version']}\n"
            f"Aplicación: {item['task_pattern']}\n"
            f"Prerrequisitos: {'; '.join(item['prerequisites']) or 'ninguno'}\n"
            f"Herramientas: {'; '.join(item['tools']) or 'no declaradas'}\n"
            + "\n".join(
                f"Paso {step}: {value}"
                for step, value in enumerate(item["methodology"], 1)
            )
            + "\nValidación: " + "; ".join(item["validation"])
            + f"\nÉxitos verificados: {item['success_runs']}"
        )
    output.append("--- FIN DEL SKILLBOOK ---")
    return "\n\n".join(output), [
        {
            "skill_id": item["skill_id"], "name": item["name"],
            "version": item["version"], "score": item["score"],
        }
        for item in skills
    ]


if __name__ == "__main__":
    initialize()
    with connect() as db:
        count = db.execute(
            "SELECT COUNT(*) FROM skills WHERE status='active'"
        ).fetchone()[0]
    print("Skills activas:", count)
