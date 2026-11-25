# Allowlist firmada de ejecutables

Los adaptadores locales exigen por defecto que el SHA-256 del ejecutable coincida con una política HMAC-SHA256 antes de iniciar el proceso. La verificación ocurre después de resolver el binario y antes de ejecutar la herramienta. Sin política válida, la ejecución se bloquea.

La salida capturada se limita a 2.000.000 bytes (máximo 1.000.000 por flujo). Cualquier truncamiento marca el resultado como incompleto y bloquea el estado exitoso, aunque el proceso termine con código 0. Además, el ejecutor termina el grupo POSIX si observa más de 8.000.000 bytes de salida total. Estos límites no sustituyen cgroups ni una cuota de CPU/memoria del sistema operativo.

## Configuración

Define estas variables en el entorno del proceso:

- `CYBER_AI_TOOL_ALLOWLIST_PATH`: ruta al manifiesto firmado.
- `CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY`: clave HMAC de al menos 32 bytes.
- `CYBER_AI_TOOL_ALLOWLIST_REQUIRED`: está activado por defecto. Solo define `0` para un entorno de desarrollo/pruebas que acepte explícitamente el modo de compatibilidad.

Si solo se configura una de las dos primeras variables, la ejecución se deniega. Si no se configura ninguna, el comportamiento predeterminado es fail-closed. El opt-out explícito `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=0` permite compatibilidad y la evidencia marca `not_configured`; nunca equivale a una allowlist aprobada.

El manifiesto contiene el identificador de cada herramienta y el SHA-256 exacto del binario enrolado. Ejemplo de estructura sin firmar:

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

La firma se calcula sobre el JSON canónico sin el campo `signature`. Para firmar durante un proceso de enrolamiento controlado:

```python
import json
import os
from pathlib import Path
from tool_allowlist import sign_tool_allowlist

tools = {"ruff": {"sha256": "SHA256_REAL_DEL_BINARIO"}}
key = os.environ["CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY"].encode("utf-8")
document = sign_tool_allowlist(tools, key)
Path("tools.signed.json").write_text(
    json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
os.chmod("tools.signed.json", 0o600)
```

Protege la clave y el manifiesto por separado. No guardes la clave en Git, no la imprimas y no la incluyas en reportes. El archivo se limita a 64 KiB; en POSIX debe pertenecer al usuario efectivo, tener permisos privados (0600), no tener hardlinks y residir bajo directorios padre confiables. Se rechazan symlinks, puntos de reanálisis, archivos no regulares, claves JSON duplicadas, campos inválidos, firmas no válidas y hashes no aprobados.

## Integración y verificación

- `tool_adapters.run_local_tool` consulta la allowlist antes de iniciar cualquier adaptador host.
- `tool_executor.py` recibe la política a través de esa ruta y conserva su resultado en la evidencia y el ledger.
- `preflight.py` valida la firma/configuración sin iniciar herramientas ni usar red. En modo obligatorio, una política ausente o inválida bloquea el preflight.
- El preflight muestra el número de ejecutables aprobados, nunca el secreto HMAC.
- Las pruebas `tests/test_tool_allowlist.py`, `tests/test_tool_adapters_allowlist.py` y `tests/test_preflight_tool_allowlist.py` cubren firma, manipulación, claves duplicadas, límites, symlinks, denegación previa al proceso y diagnóstico.

## Límites

- HMAC es simétrico: cualquier verificador que posea la clave también puede firmar. Custodia, rotación, revocación y segregación de funciones requieren un gestor externo/KMS/HSM. Para separar firmantes y verificadores, se necesita una firma asimétrica y una política de claves públicas.
- La allowlist autentica la correspondencia entre ID de herramienta y hash; no prueba por sí sola la procedencia legítima del binario. El enrolamiento debe verificar origen, firma del proveedor, versión y licencia antes de aprobarlo.
- La comprobación de hash no elimina todas las carreras TOCTOU frente a un atacante con control concurrente del host. Usa directorios de instalación inmutables y permisos restrictivos; no confíes en ella como frontera frente a administradores maliciosos.
- No aísla el proceso, no impide egress y no sustituye Docker endurecido, microVM o VM desechable.
- La política no activa automáticamente la ejecución de herramientas ni autoriza objetivos externos; los controles de objetivo y confirmación siguen siendo independientes.
