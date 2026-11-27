# Política de backup y restauración

## Defaults y confirmaciones

- Crear un backup exige `CYBER_AI_BACKUP_HMAC_KEY` (mínimo 32 bytes) y firma HMAC-SHA256 del manifiesto.
- `allow_unsigned=True` es una excepción explícita solo para desarrollo. La API exige un booleano real; valores truthy como `"true"` o `1` se rechazan.
- La verificación exige firma por defecto. `require_signature` debe ser un booleano real.
- La restauración exige `confirm_quiesced=True`, y sustituir un directorio existente exige `confirm_replace=True`. Las tres opciones son booleanos estrictos; no se interpretan cadenas como confirmaciones.
- Crear un backup por API exige `confirm_quiesced=True`; la CLI exige `--confirm-quiesced`. La confirmación debe ser un booleano real y no sustituye la comprobación operativa de los procesos.
- El llamador debe detener y comprobar los escritores antes de crear o restaurar. El programa no puede demostrar por sí mismo que todos los procesos externos estén quiescentes.

## Integridad y publicación

El manifiesto enumera rutas relativas canónicas, tipo de artefacto, tamaño y SHA-256. La creación, verificación y restauración imponen un máximo agregado de 50 GiB por snapshot; las copias de archivos se detienen al consumir el presupuesto restante y SQLite comprueba el tamaño estimado antes del snapshot. Se rechazan enlaces simbólicos/puntos de reanálisis, archivos especiales, rutas fuera del snapshot, entradas duplicadas, archivos no declarados y cambios detectados durante lectura/copia. Para que el backup sea portable, también se rechazan nombres reservados de Windows, caracteres de Alternate Data Streams, componentes con puntos/espacios finales, longitudes incompatibles y colisiones sin distinción de mayúsculas/minúsculas, equivalencias Unicode canónicas o conflictos archivo/directorio. Las colisiones se comprueban después de recolectar las rutas, sin volver a recorrer el conjunto completo por cada entrada del manifiesto. Los snapshots SQLite se validan con `PRAGMA integrity_check`. El origen se abre en modo solo lectura; el destino y la restauración usan la guarda de SQLite privado, con directorio `0700`, archivo `0600` en POSIX y `trusted_schema=OFF`, `secure_delete=ON`, `foreign_keys=ON`. El parser del manifiesto también rechaza claves JSON duplicadas, constantes no estándar y exponentes que desbordan o subdesbordan el rango `float`.

En POSIX, el árbol de origen y el snapshot deben ser privados: directorios propiedad del usuario sin acceso de grupo/otros (normalmente `0700`) y archivos regulares del mismo usuario sin acceso de grupo/otros (normalmente `0600`). Los directorios deben conservar lectura/recorrido para el propietario y los archivos lectura para el propietario. Los errores de enumeración y los árboles que superen 100.000 entradas fallan cerrados; no se acepta una copia parcial por directorios inaccesibles. Se rechazan hardlinks, symlinks y archivos especiales. En Windows la política ACL debe verificarse aparte.

La restauración verifica el backup antes de preparar un directorio temporal privado. Comprueba de nuevo el manifiesto y los hashes antes de publicar mediante reemplazo atómico. Si sustituye datos existentes, conserva el directorio anterior con un nombre `pre-restore`; ante un fallo intenta restaurarlo y, si no puede hacerlo con seguridad, lo deja preservado en su ubicación anterior.

En POSIX, los archivos copiados se sincronizan antes de publicar; el snapshot SQLite y el manifiesto también se vacían a disco. Antes del reemplazo, se valida el árbol privado y se sincronizan sus directorios en orden descendente; después del rename se sincroniza el directorio padre. La restauración aplica el mismo orden y sincroniza el padre al preservar el directorio anterior y al publicar el nuevo. Si falla un `fsync`, la operación falla y no presenta el backup/restauración como éxito. En Windows no se afirma una garantía equivalente de sincronización de entradas de directorio; deben verificarse ACL y durabilidad con pruebas específicas de esa plataforma.

## Límites operativos

- Los backups actuales **no están cifrados** (`encrypted: false`). El HMAC autentica integridad, no confidencialidad.
- No se implementan almacenamiento offsite/WORM, replicación, retención inmutable, rotación automática ni recuperación ante pérdida de la clave.
- La clave HMAC debe custodiarse fuera del repositorio, preferiblemente mediante KMS/HSM o un gestor de secretos con control de acceso y rotación.
- Deben probarse RPO/RTO, restauración completa, corrupción, pérdida de clave, caída de almacenamiento y recuperación en un host limpio.
- No se declara DR probado por crear o verificar un archivo de backup; se requiere una restauración real y evidencia independiente.

## Pruebas

`tests/test_data_backup.py` cubre hashes y firmas, rutas POSIX/Windows, colisiones case-insensitive y Unicode canónico, cambios de identidad de ruta, nombres de dispositivo, symlinks, archivos especiales, presupuestos de bytes (incluido SQLite), límites de entradas, errores de enumeración, permisos, publicación/restauración y confirmaciones explícitas por API y CLI. La suite completa y la restauración en infraestructura de despliegue siguen pendientes de ejecución.
