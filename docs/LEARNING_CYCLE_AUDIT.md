# Auditoría del ciclo de aprendizaje

`learning_cycle_audit.py` inspecciona el estado del ledger, la memoria verificada y Skillbook sin ejecutar modelos, agentes ni herramientas, y sin cambiar el estado de aprendizaje.

## Ejecución

```bash
python learning_cycle_audit.py
python learning_cycle_audit.py --max-review-age-days 90 --output reports/learning_cycle_audit.json
```

El comando devuelve:
- Integridad y número de eventos del ledger, por namespace y estado.
- Eventos `started` sin evento terminal correlacionado; no los reconcilia porque podrían pertenecer a tareas todavía activas.
- Si la clave VERITAS está configurada, cantidad de lecciones firmadas que además mantienen referencias válidas a eventos y hashes del ledger actual.
- Cantidad de Skills por estado, historiales de versión inválidos y Skills activas pendientes de revisión.
- Estado general `ok` o `degraded`; código de salida 0 o 1 respectivamente. Errores de configuración/lectura devuelven 2.

El informe no incluye prompts, contenido de evidencia ni secretos. El archivo JSON opcional se publica atómicamente con permisos privados en POSIX.

## Límites

- No juzga la calidad semántica de una metodología ni reemplaza revisión independiente.
- Sin `CYBER_AI_VERITAS_APPROVAL_KEY`, la memoria falla de forma cerrada. Si hay registros en disco, el informe marca el ciclo como degradado porque no puede validarlos.
- La auditoría no modifica el ledger, no reconcilia eventos interrumpidos, no activa ni revoca Skills y no corrige datos.
- La comprobación de integridad local no sustituye un checkpoint externo firmado ni almacenamiento inmutable.
