# Allowlist firmada de ejecutables

Los adaptadores locales pueden validar el SHA-256 del ejecutable contra una allowlist HMAC antes de iniciarlo.

## Configuración

1. Genera un manifiesto fuera del repositorio, en un proceso de enrolamiento controlado, con `sign_tool_allowlist` de `tool_allowlist.py`.
2. Cada entrada tiene el identificador de herramienta y el SHA-256 exacto del binario aprobado.
3. Protege el manifiesto y la clave por separado. No guardes la clave en Git ni dentro del mismo manifiesto.
4. Configura `CYBER_AI_TOOL_ALLOWLIST_PATH` y `CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY` en el entorno de ejecución.
5. Activa `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1` para que la ausencia de política también bloquee la ejecución.

Ejemplo de estructura antes de firmar:

```json
{
  "schema_version": 1,
  "tools": {
    "ruff": {
      "sha256": "REEMPLAZAR_POR_SHA256_REAL_DEL_BINARIO"
    }
  }
}
```

La firma es HMAC-SHA256 sobre el JSON canónico sin el campo `signature`. La validación rechaza symlinks, archivos no regulares, manifiestos mayores de 64 KiB, campos inesperados, firmas inválidas y binarios no aprobados.

## Límites

- La allowlist es opcional para compatibilidad; en despliegues controlados debe activarse el modo obligatorio.
- HMAC no es firma asimétrica: todos los verificadores que poseen la clave pueden firmar. La custodia, rotación y distribución de la clave requieren un gestor externo.
- La política autentica la correspondencia entre herramienta y hash, pero no demuestra por sí sola que el binario provenga del editor legítimo. El enrolamiento debe verificar el origen del artefacto antes de firmarlo.
- La comprobación por ruta no elimina por completo una carrera TOCTOU frente a un atacante local capaz de reemplazar el ejecutable entre la verificación y su inicio. No uses esta allowlist como frontera contra un administrador/atacante con control concurrente del host; usa artefactos inmutables, permisos de instalación restrictivos y aislamiento externo.
- El hash se toma del ejecutable resuelto en el host. Esto no aísla el proceso, no impide egress y no sustituye sandbox/VM.
