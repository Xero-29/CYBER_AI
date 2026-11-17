# Perfiles y herramientas personalizadas

La ejecución local se configura en `config/tool_execution_profiles.json`.

## Perfiles

- `standard`: perfil predeterminado; herramientas registradas, objetivos internos y sin herramientas personalizadas.
- `extended`: permite objetivos externos (además del flag explícito), herramientas personalizadas y hasta 300 s por proceso.
- `restricted`: limita a tres herramientas y 90 s.

Selecciona un perfil desde la CLI principal:

```bash
python cyber_ai.py --team "Revisar el código" \
  --execute-tools --confirm-tool-execution \
  --tool-target "/ruta/al/proyecto" --tool-profile extended
```

Para analizar una ruta externa también se exige `--allow-external-targets`. La configuración del perfil nunca sustituye la confirmación del operador ni la allowlist HMAC. La allowlist sigue necesitando una entrada con el ID de la herramienta y el SHA-256 exacto del ejecutable.

También puede seleccionarse mediante `CYBER_AI_TOOL_PROFILE`; el archivo se puede cambiar con `CYBER_AI_TOOL_CONFIG`.

## Registrar una herramienta personalizada

Añade una entrada a `custom_tools` y activa `enable_custom_tools: true` en el perfil elegido. Ejemplo:

```json
{
  "id": "custom_python_check",
  "description": "Comprobación Python personalizada",
  "category": "quality",
  "keywords": ["custom check", "comprobación personalizada"],
  "executable": "python3",
  "argv": ["-m", "mi_paquete.check", "--target", "{target}"],
  "timeout_seconds": 120,
  "enabled": true
}
```

Reglas:
- `argv` es una lista de argumentos; no se usa shell, expansión de variables ni tuberías.
- Debe incluir el marcador `{target}`. No se admiten otros marcadores.
- El identificador debe estar en la allowlist HMAC con el hash SHA-256 del ejecutable real.
- La herramienta solo se propone cuando una de sus palabras clave coincide con la tarea y el ejecutable está disponible.
- Las salidas se guardan como evidencia y se registran en el ledger.
- Los comandos personalizados son responsabilidad del operador: el runner no puede demostrar que un binario arbitrario no use red. La evidencia marca `network_access=not_enforced`; no se debe interpretar como aislamiento de red.
- No registrar herramientas que ejecuten acciones destructivas, exploten objetivos o modifiquen el objetivo analizado. El runner comprueba hashes antes/después y marca cambios como error de integridad, pero eso no revierte modificaciones.

## Límites no resueltos

Estos perfiles no son un sandbox del sistema operativo. No implementan aislamiento de red, contención de procesos en Windows, MicroVM ni garantías de seguridad frente a ejecutables maliciosos. El registro de herramientas no elimina la necesidad de revisión del ejecutable y de su hash antes de firmar la allowlist.
