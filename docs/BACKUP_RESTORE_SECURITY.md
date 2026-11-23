# Política de backup y restauración

## Defaults y confirmaciones

- Crear un backup exige `CYBER_AI_BACKUP_HMAC_KEY` (mínimo 32 bytes) y firma HMAC-SHA256 del manifiesto.
- `allow_unsigned=True` es una excepción explícita solo para desarrollo. La API exige un booleano real; valores truthy como `"true"` o `1` se rechazan.
- La verificación exige firma por defecto. `require_signature` debe ser un booleano real.
- La restauración exige `confirm_quiesced=True`, y sustituir un directorio existente exige `confirm_replace=True`. Las tres opciones son booleanos estrictos; no se interpretan cadenas como confirmaciones.
- El llamador debe detener y comprobar los escritores antes de crear o restaurar. El programa no puede demostrar por sí mismo que todos los procesos externos estén quiescentes.

## Integridad y publicación

El manifiesto enumera rutas relativas canónicas, tipo de artefacto, tamaño y SHA-256. Se rechazan enlaces simbólicos/puntos de reanálisis, archivos especiales, rutas fuera del snapshot, entradas duplicadas, archivos no declarados y cambios detectados durante lectura/copia. Los snapshots SQLite se validan con `PRAGMA integrity_check`.

La restauración verifica el backup antes de preparar un directorio temporal privado. Comprueba de nuevo el manifiesto y los hashes antes de publicar mediante reemplazo atómico. Si sustituye datos existentes, conserva el directorio anterior con un nombre `pre-restore`; ante un fallo intenta restaurarlo y, si no puede hacerlo con seguridad, lo deja preservado en su ubicación anterior.

## Límites operativos

- Los backups actuales **no están cifrados** (`encrypted: false`). El HMAC autentica integridad, no confidencialidad.
- No se implementan almacenamiento offsite/WORM, replicación, retención inmutable, rotación automática ni recuperación ante pérdida de la clave.
- La clave HMAC debe custodiarse fuera del repositorio, preferiblemente mediante KMS/HSM o un gestor de secretos con control de acceso y rotación.
- Deben probarse RPO/RTO, restauración completa, corrupción, pérdida de clave, caída de almacenamiento y recuperación en un host limpio.
- No se declara DR probado por crear o verificar un archivo de backup; se requiere una restauración real y evidencia independiente.

## Pruebas

`tests/test_data_backup.py` cubre hashes, firmas, rutas, symlinks, archivos especiales, SQLite, publicación/restauración y confirmaciones explícitas. La suite completa y la restauración en infraestructura de despliegue siguen pendientes de ejecución.
