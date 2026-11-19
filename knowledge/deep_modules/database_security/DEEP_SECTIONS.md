# Secciones de profundización — Seguridad de bases de datos

## Modelo de amenazas
Incluir motor, cuentas, roles, aplicaciones, drivers, procedimientos, extensiones, backups, réplicas, ETL, BI y administradores. Amenazas: SQL injection, privilege escalation, abuso de DBA, exposición de snapshots, extracción masiva, alteración de integridad, ransomware y credenciales en connection strings. Considerar datos temporales y logs.

## Detección
Auditar autenticaciones, grants, DDL, cambios de esquema, consultas privilegiadas, exportaciones, acceso a tablas sensibles y cambios de backup. Detectar volumen anómalo, uso de cuentas compartidas, desactivación de auditoría y conexiones desde workloads inesperados. Correlacionar usuario, aplicación, query fingerprint y dataset.

## Respuesta a incidentes
Revocar credenciales, limitar conexiones, preservar logs y snapshots consistentes, identificar tablas y filas potencialmente afectadas, proteger integridad y revisar réplicas. Corregir SQL/roles, rotar secretos y restaurar desde backup validado. Probar consistencia y permisos antes de reabrir acceso.

## Casos prácticos
Crear base sintética multi-tenant con un rol de aplicación demasiado amplio. Detectar consulta cruzada, demostrar impacto con datos falsos, restringir grants y aplicar row-level security cuando corresponda. Verificar backups, restauración y auditoría tras la corrección.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para CIS Database Benchmarks, OWASP SQL Injection, NIST SP 800-53 y documentación oficial del motor. Fijar versión y extensiones.
