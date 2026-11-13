# Memoria de aprendizaje verificada

## Flujo de aprobación

El registro directo `save_verified_lesson` está deshabilitado. Una lección solo se almacena mediante `save_verified_lesson_from_ledger` y exige:

1. Ledger con cadena hash íntegra.
2. Dos ejecuciones distintas del mismo fingerprint y namespace.
3. Todas las ejecuciones conocidas para ese fingerprint completadas.
4. Cada ejecución con validadores estructurados aprobados y SHA-256 de evidencia.
5. Firma HMAC-SHA256 de VERITAS sobre el contenido de la lección y las referencias de evidencia.

## Firma

La clave se provisiona fuera del repositorio mediante `CYBER_AI_VERITAS_APPROVAL_KEY` y debe tener al menos 32 bytes. Para construir el payload:

```python
payload = build_lesson_approval_payload(
    topic=..., error=..., correction=..., evidence=...,
    source_urls=..., tags=..., namespaces=...,
    namespace=..., event_ids=...,
)
signature = hmac.new(
    os.environ["CYBER_AI_VERITAS_APPROVAL_KEY"].encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()
```

Después se llama a `save_verified_lesson_from_ledger(..., approval_signature=signature)`.

La firma se valida nuevamente en cada lectura. Si la clave no está configurada, no se recuperan lecciones; es un comportamiento fail-closed. El archivo se escribe con permisos 0600, bloqueo exclusivo, append y fsync. Se rechazan enlaces simbólicos.

## Compatibilidad y límites

- Los registros antiguos schema v1 sin firma no se recuperan. Deben revisarse y volver a aprobarse; no se migran automáticamente.
- HMAC demuestra posesión de una clave compartida, no identidad criptográfica del modelo VERITAS ni revisión independiente.
- La clave debe estar bajo control de un proceso aprobador separado. Para nivel institucional se requiere firma asimétrica/KMS/HSM, identidad autenticada, doble control y auditoría externa inmutable.
- La firma preserva la referencia al ledger; la integridad actual del ledger debe verificarse mediante preflight/operación antes de confiar en evidencia histórica.
