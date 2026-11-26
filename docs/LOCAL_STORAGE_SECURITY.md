# Seguridad de almacenamiento SQLite local

## Controles aplicados

Los almacenes locales que contienen conocimiento privado, memoria comprimida o Skills utilizan `private_sqlite.py` antes de abrir SQLite:

- Directorio de datos privado en POSIX: propietario igual al usuario efectivo y permisos `0700`.
- Base de datos y sidecars `-journal`, `-wal` y `-shm`: archivos regulares, sin symlinks/reparse points ni hardlinks, propiedad del usuario efectivo y permisos `0600`.
- Apertura con comprobación de identidad del archivo antes/después de conectar; las rutas padre se validan y los cambios detectados fallan de forma cerrada. Cada conexión aplica `trusted_schema=OFF`, `secure_delete=ON` y `foreign_keys=ON`.
- Aplicado a `knowledge_library.py`, `knowledge_registry.py`, `skillbook.py` y `compressed_store.py`. El ledger de ejecución mantiene su propia validación de almacenamiento y aplica en cada conexión `trusted_schema=OFF`, `secure_delete=ON` y `foreign_keys=ON`. El almacén comprimido limita cada bloque a 2 MiB, metadata a 64 KiB, comprueba longitudes SQL antes de materializar BLOBs, descomprime con tope de salida y valida JSON sin claves duplicadas ni números no finitos.

## Límites

- En Windows se rechazan reparse points detectables, pero este helper no verifica ni configura ACL NTFS. Antes de uso multiusuario deben comprobarse ACL explícitas y aislamiento de cuentas.
- Los permisos de archivo no son cifrado en reposo. Los volúmenes con datos sensibles requieren cifrado de disco o almacenamiento gestionado por KMS/HSM, con rotación y recuperación probadas.
- El hash local y los triggers append-only no protegen contra un administrador/usuario con control total del host. La integridad del ledger necesita checkpoints externos firmados y almacenamiento independiente.
- La protección local no sustituye backups cifrados, offsite/WORM, pruebas de restauración, RPO/RTO ni segregación de funciones.
- `tenant_id` y `session_id` son filtros de ámbito, no autenticación. Una API expuesta debe derivarlos de identidad RBAC/IdP confiable y no de parámetros controlados por el cliente.

## Pruebas

`tests/test_private_sqlite.py` comprueba permisos, symlinks, hardlinks y sidecars. Las pruebas de biblioteca, registro, Skillbook y almacén comprimido verifican la integración. Estas comprobaciones no sustituyen la auditoría de ACL Windows ni las pruebas de recuperación en infraestructura real.
