# Preflight local

Ejecuta `python preflight.py` después de instalar dependencias. La comprobación no inicia Ollama, Docker ni escáneres, y no realiza llamadas de red.

- **Errores:** bloquean la preparación básica (Python anterior a 3.12, archivos base ausentes, configuración inválida o dependencias base ausentes).
- **Advertencias:** integraciones opcionales no instaladas, extractores documentales opcionales ausentes o ledger aún no creado.
- **Ledger existente:** si existe, se verifica su cadena hash; un fallo de integridad bloquea la comprobación.
- **Allowlist de ejecutables:** se valida la firma HMAC y el número de binarios aprobados cuando se configura. Si `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1`, la ausencia o invalidez de la política bloquea el preflight. Sin modo obligatorio, la ausencia se muestra como advertencia y los adaptadores conservan compatibilidad.
- **Política del ledger:** `tool_executor.py`, `task_runner.py` y `agent_runner.py` exigen trazabilidad por defecto. `CYBER_AI_ALLOW_UNLOGGED_EXECUTION=1` es una excepción explícita y el preflight la marca como advertencia.

Para automatización:

```bash
python preflight.py --json
```

Una salida `ready` significa que el entorno supera las comprobaciones locales básicas. No significa que proveedores externos, modelos, Docker, escáneres o el sistema completo hayan sido probados en esa máquina.

## Lock de dependencias

La instalación principal usa `pip --require-hashes` y hashes SHA-256 fijados para wheels verificados por CI. El lock actual soporta CPython 3.12.x, Linux x86_64 y glibc >= 2.26. `setup.sh` rechaza otras plataformas para evitar una instalación sin hashes compatibles. Para ampliar plataformas se deben incorporar hashes verificados de sus wheels y añadir pruebas CI específicas; no se deben reutilizar hashes de otra arquitectura.

## Dependencias del sandbox

Las herramientas de análisis dentro de la imagen Docker usan `sandbox/requirements.lock`, con hashes SHA-256 de Ruff, Bandit y sus dependencias. La construcción instala con `pip --require-hashes`. El workflow descarga los wheels, valida sus hashes contra el lock y publica un SBOM CycloneDX separado para el sandbox. Para regenerar el lock: descargar wheels con `sandbox/requirements.in`, ejecutar `wheel_lock_generator.py` y revisar el diff antes de incorporarlo.

## Extractores documentales opcionales

PDF, DOCX, XLSX y PPTX usan dependencias opcionales separadas del entorno base. Para reproducir el entorno validado en CI:

```bash
python -m pip install --require-hashes -r requirements-documents.lock
```

`requirements-documents.in` fija las dependencias directas; `requirements-documents.lock` fija también las transitivas y hashes SHA-256. El lock se valida descargando exclusivamente wheels y comparando el manifiesto de artefactos antes de generar un SBOM CycloneDX independiente. Su plataforma de referencia es CPython 3.12, Linux x86_64 y glibc >= 2.26. No reutilices esos hashes en otras plataformas; genera y revisa un lock específico.
