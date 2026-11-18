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


### Entorno del runner personalizado

Cada ejecución crea un `HOME` y directorios temporales efímeros con permisos privados. El proceso recibe un entorno mínimo: `PATH` limitado al directorio del ejecutable y rutas de sistema, sin heredar variables de credenciales del operador; en Windows solo se conservan variables de sistema necesarias para arrancar procesos. stdout/stderr se drenan con límite de salida y se cierran al terminar; si un descendiente conserva los pipes, el runner intenta terminar el grupo de procesos en POSIX.

Esto reduce exposición accidental de secretos y fugas de descriptores, pero no impone aislamiento de egress ni convierte un ejecutable personalizado en sandbox.

## Aislamiento de YARA y TShark

YARA y TShark ya no se ejecutan directamente en el host. Se delegan a `isolated_tool_runner.py`, que usa la imagen Docker construida con:

```bash
sh build-analysis-sandbox.sh
```

El runner exige la imagen local `cyber-ai-analysis-sandbox:1.0` (o `CYBER_AI_ANALYSIS_SANDBOX_IMAGE`) y la incluye en la allowlist HMAC por su ID de imagen SHA-256. Obtén el ID con:

```bash
docker image inspect --format '{{.Id}}' cyber-ai-analysis-sandbox:1.0
```

Incluye el hash sin el prefijo `sha256:` en las entradas de allowlist para `yara` y `tshark`. La firma debe generarse con `sign_tool_allowlist` y una clave de al menos 32 bytes, mantenida fuera del repositorio. Configura `CYBER_AI_TOOL_ALLOWLIST_PATH` y `CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY` antes de ejecutar. El contenedor se ejecuta con red deshabilitada, root filesystem de solo lectura, objetivo/reglas en solo lectura, sin capacidades, no-new-privileges, límite de procesos, memoria y CPU, y sin montar el socket Docker. YARA recibe reglas locales mediante `CYBER_AI_YARA_RULES`.

Ejemplo para incorporar esos dos IDs a una allowlist existente sin perder las entradas firmadas anteriores (requiere que `CYBER_AI_TOOL_ALLOWLIST_PATH` y `CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY` ya estén configuradas):

```bash
IMAGE_ID="$(docker image inspect --format '{{.Id}}' cyber-ai-analysis-sandbox:1.0)"
export CYBER_AI_SANDBOX_IMAGE_SHA256="${IMAGE_ID#sha256:}"
python - <<'PY'
import json, os
from pathlib import Path
from tool_allowlist import load_signed_tool_allowlist, sign_tool_allowlist

path = Path(os.environ["CYBER_AI_TOOL_ALLOWLIST_PATH"])
key = os.environ["CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY"].encode()
digest = os.environ["CYBER_AI_SANDBOX_IMAGE_SHA256"]
tools = load_signed_tool_allowlist(path, key) if path.exists() else {}
tools.update({
    "yara": {"sha256": digest},
    "tshark": {"sha256": digest},
})
signed = sign_tool_allowlist(tools, key)
temporary = path.with_name(path.name + ".new")
if temporary.exists() or temporary.is_symlink():
    raise SystemExit("El archivo temporal ya existe; revísalo antes de continuar.")
fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as stream:
    json.dump(signed, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
os.replace(temporary, path)
os.chmod(path, 0o600)
PY
```

Para YARA define también `CYBER_AI_YARA_RULES` con la ruta de un archivo de reglas local revisado. El ejecutor de YARA/TShark exige que la ruta objetivo y las reglas sean legibles por el usuario que se ejecuta dentro del contenedor. El pipeline continúa exigiendo confirmación explícita.

La imagen debe construirse y revisarse en un entorno confiable. El Docker daemon y el kernel del host siguen formando parte de la base de confianza; esto no equivale a una MicroVM.

## Límites no resueltos

- El runner Docker aislado cubre YARA y TShark, no todas las herramientas.
- Las herramientas personalizadas siguen ejecutándose como procesos del host: argv sin shell, allowlist HMAC, timeout y hashes no equivalen a aislamiento de sistema operativo ni de red.
- Los adaptadores locales generales no tienen aislamiento de red obligatorio.
- La contención de procesos Windows y la validación Windows siguen pendientes.
- No hay MicroVM ni garantía frente a escape del contenedor, vulnerabilidades del kernel o del daemon Docker.
- La allowlist y la clave HMAC deben administrarse fuera del repositorio y protegerse como secretos.
