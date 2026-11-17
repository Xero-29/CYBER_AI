# Promoción verificable de Skills

CYBER_AI separa la propuesta de una Skill de su activación. `propose_skill_from_ledger` crea una candidata no ejecutable a partir de ejecuciones verificadas; `register_skill_from_ledger` la activa únicamente con aprobación HMAC VERITAS. Las versiones quedan en `skill_versions` como snapshots append-only.

## Condiciones exigidas

1. El ledger debe superar `ExecutionLedger.verify()`.
2. Se exigen al menos dos eventos distintos en el mismo namespace.
3. Ambos eventos deben tener la misma huella de tarea y marcas temporales distintas.
4. Todas las ejecuciones registradas para esa huella, dentro del historial consultado, deben estar completadas.
5. Cada ejecución seleccionada debe proceder de `team_orchestrator`, declarar `objective_supervision=true` y contener una revisión conforme, fundamentada y emitida por un rol distinto (`VERITAS`/`FILTRO`). El propio `agent_runner` marca su finalización como `independent=false`.
6. Cada evento debe incluir un SHA-256 de evidencia válido.
7. El documento canónico de aprobación v2 contiene la Skill, los IDs de eventos y los hashes SHA-256 de evidencia del ledger. Debe tener una firma HMAC válida; si cambia cualquier hash entre la firma y la promoción, la firma deja de ser válida.

Si el historial alcanza el límite de 1.000 eventos, la promoción se bloquea porque no puede garantizarse una revisión exhaustiva.

## Firma

La clave debe existir fuera del repositorio en `CYBER_AI_VERITAS_APPROVAL_KEY` y tener al menos 32 bytes. Nunca se debe incluir en prompts, archivos versionados, logs o el ledger.

El firmante construye el documento canónico:

```python
payload = skillbook.skill_approval_payload(**skill_fields)
```

Y calcula HMAC-SHA256 sobre los bytes UTF-8 de ese documento:

```python
signature = hmac.new(
    os.environ["CYBER_AI_VERITAS_APPROVAL_KEY"].encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()
```

Después llama a `register_skill_from_ledger(..., approval_signature=signature)`. Si existe una candidata con la misma huella de tarea, eventos y hash del payload firmado, se activa esa candidata y avanza su versión; de lo contrario, se crea una Skill activa nueva respaldada por los mismos eventos.

## Límite de confianza

HMAC autentica posesión de la clave, no demuestra por sí mismo que un modelo VERITAS haya revisado el contenido. La clave debe estar bajo control de un proceso aprobador separado. Para nivel institucional se debe reemplazar o complementar esta clave local por un servicio de firma independiente, KMS/HSM, identidad del aprobador, política de doble control y registro externo inmutable.

El endpoint público `register_verified_skill` está deshabilitado para impedir que un caller se autodeclare VERITAS. Las candidatas no aparecen en `search_skills` ni se inyectan al contexto del agente. La recuperación de Skills activas verifica la cadena de versiones y el snapshot actual antes de devolver una metodología; una Skill alterada o con historial roto queda excluida. El historial de versiones bloquea UPDATE/DELETE ordinarios. El rollback firmado y el benchmark de regresión ya están implementados; aún falta firma independiente KMS/HSM y validación semántica/operativa de metodologías.


## Rollback firmado de Skills

Una versión activa anterior puede restaurarse sin reescribir el historial. Primero se obtiene el documento canónico que vincula la versión actual, la versión objetivo y los hashes de ambos snapshots:

```python
payload = skillbook.skill_rollback_payload(skill_id, target_version=1)
signature = hmac.new(
    os.environ["CYBER_AI_VERITAS_APPROVAL_KEY"].encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()
result = skillbook.rollback_skill_version(
    skill_id, target_version=1, approval_signature=signature
)
```

El rollback exige una versión objetivo que estuvo activa, con dos ejecuciones exitosas y cero fallos sin resolver. La firma queda invalidada si cambia la versión actual o cualquiera de los snapshots. La restauración crea una versión nueva con `change_type=rollback`; nunca modifica ni elimina versiones anteriores. La clave sigue siendo HMAC local y no sustituye una firma independiente KMS/HSM.

## Regresión de recuperación

`skill_regression.py` evalúa un dataset JSONL de consultas con IDs de Skills relevantes y calcula Recall@K, Precision@K, MRR@K y hit-rate. Comprueba la integridad y el estado activo de las Skills relevantes, no incrementa contadores de uso y devuelve código de salida distinto de cero si no alcanza los umbrales configurados. El dataset debe construirse con juicios de relevancia revisados; no se deben inventar etiquetas para inflar métricas.

```bash
python skill_regression.py --dataset /ruta/privada/skill_queries.jsonl --top-k 5 --min-recall 0.80 --min-mrr 0.70 --output reports/skill_regression.json
```

## Auditoría de ciclo

`python learning_cycle_audit.py` revisa ledger, referencias de memoria, cadenas de versiones, eventos interrumpidos y Skills que requieren revisión. No altera los registros. Consulta [LEARNING_CYCLE_AUDIT.md](LEARNING_CYCLE_AUDIT.md).
