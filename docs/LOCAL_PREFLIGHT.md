# Preflight local

Ejecuta `python preflight.py` después de instalar dependencias. La comprobación no inicia Ollama, Docker ni escáneres, y no realiza llamadas de red.

- **Errores:** bloquean la preparación básica (Python anterior a 3.12, archivos base ausentes, configuración inválida o dependencias base ausentes).
- **Advertencias:** integraciones opcionales no instaladas, extractores documentales opcionales ausentes o ledger aún no creado.
- **Ledger existente:** si existe, se verifica su cadena hash; un fallo de integridad bloquea la comprobación.

Para automatización:

```bash
python preflight.py --json
```

Una salida `ready` significa que el entorno supera las comprobaciones locales básicas. No significa que proveedores externos, modelos, Docker, escáneres o el sistema completo hayan sido probados en esa máquina.


## Allowlist de ejecutables y política del ledger

El preflight valida la allowlist HMAC de ejecutables cuando se configura. Define conjuntamente:

- `CYBER_AI_TOOL_ALLOWLIST_PATH`: ruta al manifiesto firmado.
- `CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY`: clave HMAC de al menos 32 bytes, entregada desde un gestor de secretos.
- `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1`: convierte la ausencia de allowlist en error bloqueante. Sin este requisito, la ausencia se informa como advertencia de compatibilidad.

Una configuración parcial o una firma inválida bloquea el preflight. La clave nunca se imprime en el informe.

El ledger es obligatorio por defecto en agentes, ejecutor de herramientas y task runner. El preflight emite una advertencia si se activa explícitamente `CYBER_AI_ALLOW_UNLOGGED_EXECUTION=1`; los CLI permiten la excepción solo con `--allow-unlogged-execution`. No uses estas excepciones en despliegues operativos.

## Lock de dependencias

La instalación principal usa `pip --require-hashes` y hashes SHA-256 fijados para wheels verificados por CI. El lock actual soporta CPython 3.12.x, Linux x86_64 y glibc >= 2.26. `setup.sh` rechaza otras plataformas para evitar una instalación sin hashes compatibles. Para ampliar plataformas se deben incorporar hashes verificados de sus wheels y añadir pruebas CI específicas; no se deben reutilizar hashes de otra arquitectura.

## Dependencias del sandbox

Las herramientas de análisis dentro de la imagen Docker usan `sandbox/requirements.lock`, con hashes SHA-256 de Ruff, Bandit y sus dependencias. La construcción instala con `pip --require-hashes`. El workflow descarga los wheels, valida sus hashes contra el lock y publica un SBOM CycloneDX separado para el sandbox. Para regenerar el lock en la misma plataforma de destino:

```bash
wheelhouse="$(mktemp -d)"
python -m pip download --only-binary=:all: --dest "$wheelhouse" -r sandbox/requirements.in
python wheel_lock_generator.py --wheelhouse "$wheelhouse" --requirements sandbox/requirements.in --output sandbox/requirements.lock
rm -rf "$wheelhouse"
```

El wheelhouse debe contener los wheels de las dependencias directas y transitivas para esa plataforma. Revisa versiones, hashes y procedencia antes de aceptar el diff; no generes un lock de producción desde un mirror no confiable.

## Dependencias documentales opcionales

Las versiones directas están fijadas en `requirements-documents.in`; el lock transitivo `requirements-documents.lock` contiene hashes SHA-256 de wheels para CPython 3.12.x/Linux x86_64/glibc >= 2.26. Instala con:

```bash
python -m pip install --require-hashes -r requirements-documents.lock
```

CI descarga los wheels con `--require-hashes`, compara el manifiesto, genera un SBOM CycloneDX independiente y ejecuta la suite con los extractores instalados. El lock no es válido para otras arquitecturas; genera y revisa un lock separado para cada plataforma soportada. `requirements-documents.txt` se conserva solo como alias de compatibilidad y no aplica hash enforcement por sí mismo.

Para regenerarlo en la plataforma de destino:

```bash
wheelhouse="$(mktemp -d)"
python -m pip download --only-binary=:all: --dest "$wheelhouse" -r requirements-documents.in
python wheel_lock_generator.py --wheelhouse "$wheelhouse" --requirements requirements-documents.in --output requirements-documents.lock
rm -rf "$wheelhouse"
```

Revisa versiones, hashes y procedencia antes de aceptar el diff.
