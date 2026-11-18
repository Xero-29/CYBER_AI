# Escritura segura de artefactos locales

Los archivos generados por herramientas de dependencias, SBOM y biblioteca no deben escribirse siguiendo un symlink preparado en la ruta de salida.

`safe_io.atomic_write_text` proporciona una escritura temporal y sustitución atómica para los siguientes flujos:

- `wheel_lock_generator.py`: locks generados desde wheelhouses verificados.
- `dependency_artifact_manifest.py`: manifiestos de wheels enlazados al hash del lock.
- `sbom_generator.py`: SBOM CycloneDX.
- `knowledge_downloader.py`: manifiesto de descargas y estado de la biblioteca.

La función:
- valida que los componentes existentes de la ruta no sean symlinks ni puntos de reanálisis;
- rechaza destinos existentes que no sean archivos regulares;
- crea el temporal de forma exclusiva en el mismo directorio;
- escribe y sincroniza el contenido antes de reemplazar el destino;
- usa permisos restrictivos `0600` en POSIX;
- permite crear directorios padre solo cuando el llamador lo solicita expresamente.

Las pruebas `tests/test_safe_io.py` cubren escritura/reemplazo, destino symlink, padre symlink, creación explícita de directorios y destinos no regulares.

## Límites

Esto evita clases comunes de sobrescritura por symlink y evita seguir rutas que ya contienen componentes enlazados al validarlas. No constituye una frontera frente a un atacante local con capacidad de modificar simultáneamente los directorios padre ni sustituye permisos de filesystem, sandbox, WORM o almacenamiento externo. La custodia, retención y recuperación de artefactos siguen siendo responsabilidades operativas.
