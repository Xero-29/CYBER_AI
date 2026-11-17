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

## Aislamiento de YARA y TShark

YARA y TShark ya no se ejecutan directamente en el host. Se delegan a `isolated_tool_runner.py`, que usa la imagen Docker construida con:

```bash
./build-analysis-sandbox.sh
```

El runner exige la imagen local `cyber-ai-analysis-sandbox:1.0` (o `CYBER_AI_ANALYSIS_SANDBOX_IMAGE`) y la incluye en la allowlist HMAC por su ID de imagen SHA-256. La huella se obtiene con:

```bash
docker image inspect --format '{{.Id}}' cyber-ai-analysis-sandbox:1.0
```

Incluye el hash sin el prefijo `sha256:` en las entradas de allowlist para `yara` y `tshark`. El contenedor se ejecuta con red deshabilitada, root filesystem de solo lectura, objetivo/reglas en solo lectura, sin capacidades, no-new-privileges, límite de procesos, memoria y CPU, y sin montar el socket Docker. YARA recibe reglas locales mediante `CYBER_AI_YARA_RULES`.

La imagen debe construirse y revisarse en un entorno confiable. El Docker daemon y el kernel del host siguen formando parte de la base de confianza; esto no equivale a una MicroVM.

## Límites no resueltos

- El runner Docker aislado cubre YARA y TShark, no todas las herramientas.
- Las herramientas personalizadas siguen ejecutándose como procesos del host: argv sin shell, allowlist HMAC, timeout y hashes no equivalen a aislamiento de sistema operativo ni de red.
- Los adaptadores locales generales no tienen aislamiento de red obligatorio.
- La contención de procesos Windows y la validación Windows siguen pendientes.
- No hay MicroVM ni garantía frente a escape del contenedor, vulnerabilidades del kernel o del daemon Docker.
- La allowlist y la clave HMAC deben administrarse fuera del repositorio y protegerse como secretos.
