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

El endpoint público `register_verified_skill` está deshabilitado para impedir que un caller se autodeclare VERITAS. Las candidatas no aparecen en `search_skills` ni se inyectan al contexto del agente. El historial de versiones bloquea UPDATE/DELETE ordinarios; aún faltan rollback, regresión automática y firma independiente KMS/HSM.
