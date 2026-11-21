# Escritura segura de artefactos locales

Los archivos generados por herramientas de dependencias, SBOM y biblioteca no deben escribirse siguiendo un symlink preparado en la ruta de salida.

`safe_io.atomic_write_text` proporciona una escritura temporal y sustitución atómica para los siguientes flujos:

- `wheel_lock_generator.py`: locks generados desde wheelhouses verificados.
- `dependency_artifact_manifest.py`: manifiestos de wheels enlazados al hash del lock.
- `sbom_generator.py`: SBOM CycloneDX.
- `knowledge_downloader.py`: manifiesto de descargas y estado de la biblioteca.

La función:
- valida que todos los componentes de la ruta sean directorios reales, sin symlinks ni puntos de reanálisis;
- en POSIX, exige que los directorios pertenezcan a root o al usuario efectivo y no sean escribibles por grupo/otros, salvo padres sticky propiedad de root (por ejemplo, `/tmp`);
- crea los directorios nuevos con modo `0700`;
- rechaza destinos existentes que no sean archivos regulares;
- crea el temporal de forma exclusiva en el mismo directorio;
- escribe y sincroniza el contenido antes de reemplazar el destino;
- usa permisos restrictivos `0600` en POSIX;
- permite crear directorios padre solo cuando el llamador lo solicita expresamente.

Las pruebas `tests/test_safe_io.py` cubren escritura/reemplazo, destino symlink, padre symlink, creación explícita de directorios y destinos no regulares.

## Límites

Esto reduce el riesgo de sustitución por symlink y de escritura desde directorios compartidos o modificables por terceros. La validación de rutas sigue siendo sensible a carreras frente a procesos con el mismo UID o privilegios equivalentes; no es una frontera de aislamiento frente a un atacante local del mismo usuario. En Windows no se verifica la ACL efectiva: debe validarse en el entorno de despliegue. Esto tampoco sustituye sandbox, WORM o almacenamiento externo. La custodia, retención y recuperación de artefactos siguen siendo responsabilidades operativas.
