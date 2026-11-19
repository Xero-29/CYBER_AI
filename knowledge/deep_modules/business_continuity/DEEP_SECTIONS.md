# Secciones de profundización — Continuidad y recuperación

## Modelo de amenazas
Mapear procesos críticos, personas, instalaciones, proveedores, energía, telecomunicaciones, identidad, aplicaciones, datos y dependencias compartidas. Amenazas: ransomware, pérdida de región, proveedor caído, corrupción de backups, pérdida de credenciales de recuperación y crisis simultánea. Definir BIA, RTO/RPO, tolerancia y modos degradados.

## Detección
Monitorizar disponibilidad de servicios, integridad de backups, replicación, capacidad, dependencias, pruebas de restauración y cambios de runbooks. Detectar backup fallido, borrado masivo, credenciales compartidas, drift de réplica y pérdida de acceso al plano de recuperación. Una copia existente no demuestra recuperabilidad.

## Respuesta a incidentes
Activar crisis según impacto y BIA, priorizar servicios, usar canal alternativo, proteger backups y credenciales, restaurar desde punto limpio y validar integridad antes de reconectar. Coordinar negocio, IT, proveedores y comunicación. Registrar RTO/RPO reales, desviaciones y decisiones.

## Casos prácticos
Simular cifrado de entorno de prueba y pérdida de credenciales administrativas. Restaurar identidad y servicio desde backup aislado, medir RTO/RPO, validar datos y controles de seguridad. Repetir con backup corrupto y dependencia de proveedor indisponible; documentar estrategia alternativa.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para ISO 22301, NIST SP 800-34, NIST SP 800-61 y CISA ransomware guidance. Registrar alcance, criticidad y última prueba real.
