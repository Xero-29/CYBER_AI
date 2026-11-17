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
