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

`requirements-documents.txt` todavía declara rangos de versión sin hashes. Esas dependencias no están cubiertas por el lock base ni por el SBOM de CI. Para entornos de alta garantía, no las instales hasta generar y revisar un lock SHA-256 por plataforma, y añadir su verificación/SBOM al workflow.
