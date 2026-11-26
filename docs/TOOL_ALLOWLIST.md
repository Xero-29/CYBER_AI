# Allowlist HMAC de ejecutables y plantillas Nuclei

Los adaptadores locales exigen por defecto que el SHA-256 del ejecutable coincida con una política HMAC-SHA256 antes de iniciar el proceso. La verificación ocurre después de resolver el binario y antes de ejecutar la herramienta. Sin política válida, la ejecución se bloquea.

La salida capturada se limita a 2.000.000 bytes (máximo 1.000.000 por flujo). Cualquier truncamiento marca el resultado como incompleto y bloquea el estado exitoso, aunque el proceso termine con código 0. Además, el ejecutor termina el grupo POSIX si observa más de 8.000.000 bytes de salida total. Estos límites no sustituyen cgroups ni una cuota de CPU/memoria del sistema operativo. En Windows el fallback solo termina el proceso hijo directo y marca `output_limit_termination_failed`; no se presenta como terminación completa del árbol. La garantía requiere Job Objects y validación en el host Windows.

La salida JSONL de Nuclei se lee mediante un lector común con límites duros de archivo, línea y cantidad de hallazgos. La lectura rechaza symlinks, puntos de reanálisis, hardlinks POSIX y cambios de identidad/tamaño detectados por el lector seguro; el parser rechaza JSON con claves duplicadas, constantes no finitas, exponentes que desbordan o subdesbordan el rango `float`, UTF-8 inválido y registros que no sean objetos. Ante evidencia inválida o inestable no se aceptan hallazgos parciales. Los dos entry points (`nuclei_scanner.py` y `task_runner.py`) comparten esta ruta de lectura. La salida de consola también escapa caracteres Unicode de control y formato, incluidos ESC/OSC y controles bidireccionales, antes de imprimir texto no confiable.

Los objetivos se resuelven por componentes desde la raíz del repositorio: se rechazan symlinks y puntos de reanálisis en cualquier ancestro, archivos objetivo con hardlinks y entradas especiales dentro de árboles recursivos. La huella se calcula con descriptores abiertos sin seguir el enlace final y se vuelve a comprobar la identidad, el tamaño, los tiempos y el número de enlaces antes y después de leer. Esto reduce alias y sustituciones durante la lectura, pero no convierte el host en una frontera frente a un administrador o un proceso concurrente con los mismos privilegios.

La ejecución Docker no monta la raíz completa del repositorio. Antes de iniciar crea un árbol temporal de solo lectura con los siete módulos de runtime necesarios y monta por separado únicamente el objetivo seleccionado (y, si aplica, el archivo de configuración explícito). El árbol temporal rechaza archivos adicionales, enlaces, hardlinks y rutas con delimitadores de montaje. La evidencia de cada ejecución se escribe en un subdirectorio privado, único y vacío; el contenedor no ve informes anteriores ni el directorio padre. La ruta del subdirectorio se muestra en la salida del runner. La referencia local de imagen se resuelve antes del arranque a su ID de contenido `sha256:...`; `docker run` usa ese ID inmutable con `--pull=never`, no una etiqueta mutable. El `.dockerignore` limita el contexto de build al Dockerfile y al lock de la sandbox; los datos y archivos locales del repositorio no se envían al daemon durante la construcción. Esto reduce la exposición accidental de archivos `.env`, datos, informes y otros archivos locales que no forman parte del objetivo.

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

La firma se calcula sobre el JSON canónico sin el campo `signature`. El mismo manifiesto incluye también las plantillas Nuclei aprobadas: cada entrada usa el ID determinista `template_allowlist_id(ruta_relativa)` y el SHA-256 exacto del archivo. Nuclei exige esas entradas incluso si `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=0`; el modo de compatibilidad nunca autoriza plantillas de red.

Para firmar durante un proceso de enrolamiento controlado, inspecciona primero el contenido y el alcance de cada plantilla, calcula sus hashes y agrega las entradas al mismo diccionario `tools`:

```python
import json
import os
from pathlib import Path
from tool_allowlist import sign_tool_allowlist

from template_integrity import hash_selected_templates, template_allowlist_id

tools = {"ruff": {"sha256": "SHA256_REAL_DEL_BINARIO"},
         "nuclei": {"sha256": "SHA256_REAL_DEL_BINARIO_NUCLEI"}}
template_root = Path.home() / "nuclei-templates"
template_paths = [
    "http/technologies/bulma-detect.yaml",
    "http/misconfiguration/http-missing-security-headers.yaml",
    "http/technologies/tech-detect.yaml",
    "http/technologies/favicon-detect.yaml",
    "http/misconfiguration/cookies-without-secure.yaml",
    "http/misconfiguration/cookies-without-httponly.yaml",
    "http/misconfiguration/missing-cookie-samesite-strict.yaml",
]
evidence = hash_selected_templates(
    [{"path": str(template_root / item)} for item in template_paths],
    template_root,
)
for item in evidence:
    tools[template_allowlist_id(item["path"])] = {"sha256": item["sha256"]}

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
- `nuclei_scanner.py` y `task_runner.py` exigen IDs `nuclei_template_*` y hashes exactos para todas las plantillas seleccionadas; vuelven a comprobar la firma y los hashes antes de aceptar resultados.
- `preflight.py` valida la firma/configuración sin iniciar herramientas ni usar red. En modo obligatorio, una política ausente o inválida bloquea el preflight.
- El preflight muestra el número de ejecutables aprobados, nunca el secreto HMAC.
- Las pruebas `tests/test_tool_allowlist.py`, `tests/test_tool_adapters_allowlist.py` y `tests/test_preflight_tool_allowlist.py` cubren firma, manipulación, claves duplicadas, límites, symlinks, denegación previa al proceso y diagnóstico.

## Límites

- HMAC es simétrico: cualquier verificador que posea la clave también puede firmar. Custodia, rotación, revocación y segregación de funciones requieren un gestor externo/KMS/HSM. Para separar firmantes y verificadores, se necesita una firma asimétrica y una política de claves públicas.
- La allowlist autentica la correspondencia entre ID de herramienta/plantilla y hash; no prueba por sí sola que el contenido sea seguro. El enrolamiento debe revisar manualmente el origen, la licencia y el comportamiento de red de cada plantilla antes de firmarla.
- La comprobación de hash no elimina todas las carreras TOCTOU frente a un atacante con control concurrente del host. Usa directorios de instalación inmutables y permisos restrictivos; no confíes en ella como frontera frente a administradores maliciosos.
- No aísla el proceso, no impide egress y no sustituye Docker endurecido, microVM o VM desechable.
- La política no activa automáticamente la ejecución de herramientas ni autoriza objetivos externos; los controles de objetivo y confirmación siguen siendo independientes.
