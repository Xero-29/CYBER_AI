# Promoción verificable de Skills

CYBER_AI ofrece `skillbook.register_skill_from_ledger` como ruta de promoción más estricta que el registro manual heredado.

## Condiciones exigidas

1. El ledger debe superar `ExecutionLedger.verify()`.
2. Se exigen al menos dos eventos distintos en el mismo namespace.
3. Ambos eventos deben tener la misma huella de tarea y marcas temporales distintas.
4. Todas las ejecuciones registradas para esa huella, dentro del historial consultado, deben estar completadas.
5. Cada ejecución seleccionada debe incluir al menos un validador con `passed=true`.
6. Cada evento debe incluir un SHA-256 de evidencia válido.
7. El documento canónico que contiene la Skill y los IDs de evidencia debe tener una firma HMAC válida.

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

Después llama a `register_skill_from_ledger(..., approval_signature=signature)`.

## Límite de confianza

HMAC autentica posesión de la clave, no demuestra por sí mismo que un modelo VERITAS haya revisado el contenido. La clave debe estar bajo control de un proceso aprobador separado. Para nivel institucional se debe reemplazar o complementar esta clave local por un servicio de firma independiente, KMS/HSM, identidad del aprobador, política de doble control y registro externo inmutable.

La función `register_verified_skill` existente se conserva por compatibilidad y pruebas; no debe usarse para promoción automática basada en agentes.
