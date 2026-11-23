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
- en POSIX, sincroniza también el directorio padre después del `rename` para persistir la entrada publicada;
- usa permisos restrictivos `0600` en POSIX;
- permite crear directorios padre solo cuando el llamador lo solicita expresamente.

Las pruebas `tests/test_safe_io.py` cubren escritura/reemplazo, destino symlink, padre symlink, creación explícita de directorios y destinos no regulares.


## Evidencia de adaptadores de herramientas

`tool_adapters.write_evidence` confina por defecto los artefactos al repositorio y exige que `allow_external` sea un booleano real. Valores truthy como `"false"` o `1` se rechazan; no pueden activar accidentalmente la salida externa. `allow_external=True` es una excepción explícita de ruta, no una autorización de ejecución ni un control de aislamiento: el destino sigue sujeto a permisos privados, validación de directorios y publicación atómica.


## Límites

Esto reduce el riesgo de sustitución por symlink y de escritura desde directorios compartidos o modificables por terceros. La validación de rutas sigue siendo sensible a carreras frente a procesos con el mismo UID o privilegios equivalentes; no es una frontera de aislamiento frente a un atacante local del mismo usuario. En Windows no se verifica la ACL efectiva: debe validarse en el entorno de despliegue. Esto tampoco sustituye sandbox, WORM o almacenamiento externo. La custodia, retención y recuperación de artefactos siguen siendo responsabilidades operativas.

## Flujos adicionales cubiertos

Además de los generadores anteriores:

- `knowledge_downloader.py` crea directorios de biblioteca privados y usa `tempfile.mkstemp` en el mismo directorio para cada descarga binaria; el temporal nace con permisos restrictivos, se sincroniza y se publica con reemplazo atómico. No usa un nombre `.part` predecible.
- `report_manager.py` protege el índice de informes; `batch_analyzer.py` y `cyber_ai.py` publican resultados JSON mediante `atomic_write_text` y redactan campos/texto sensible.
- `web_research.py` y `experiment_engine.py` escriben artefactos JSON/Markdown con directorios privados y archivos `0600`; las salidas externas se redactan antes de persistirlas. Los hashes de stdout/stderr de experimentos siguen calculándose sobre los bytes originales, mientras el texto almacenado se redacta.
- Las CLI de backups, checkpoints, proveedores, manifiestos, herramientas, investigación y DIRECTOR redactan errores antes de imprimirlos. Las regresiones verifican que los valores de prueba no aparezcan en stdout/stderr ni en artefactos.

La redacción es una defensa adicional, no un gestor de secretos ni una garantía de detección de todos los formatos. No se deben introducir credenciales en prompts, reportes o artefactos; los secretos operativos deben permanecer en variables/servicios externos. Las ACL efectivas de Windows siguen pendientes de validación.
