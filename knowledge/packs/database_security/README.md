# Seguridad de bases de datos — Guía de dominio

**ID:** `database_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege motores relacionales, NoSQL, caches, data warehouses y bases embebidas. Cubre identidad, autorización, consultas, cifrado, backups, auditoría, replicación y configuración. El acceso de administración debe estar separado de las cuentas de aplicación.

## Competencias
- Revisar roles, grants, usuarios, service accounts y privilegios.
- Prevenir SQL/NoSQL injection y abuso de procedimientos.
- Proteger secretos, conexiones y certificados.
- Evaluar cifrado, KMS, TDE y cifrado a nivel de campo.
- Configurar auditoría, logs y monitoreo de consultas.
- Proteger replicación, backups, snapshots y restore.
- Gestionar parches, extensiones, configuración y hardening.

## Controles
- Cuentas de aplicación dedicadas y privilegios mínimos.
- Secret manager y rotación de credenciales.
- Consultas parametrizadas y validación de entrada.
- TLS entre cliente, aplicación y base.
- Cifrado de backup y control de claves.
- Auditoría de cambios privilegiados y acceso a datos sensibles.
- Segmentación de red y acceso por bastión.
- Parches y extensiones aprobadas.
- Backups con restore probado y retención.

## Metodología
1. Inventariar motor, versión, instancias, datos y propietarios.
2. Revisar roles, grants, cuentas huérfanas y accesos remotos.
3. Analizar consultas, procedimientos y conexiones.
4. Evaluar cifrado, claves, logs y auditoría.
5. Revisar exposición de puertos y segmentación.
6. Verificar backup, replicación y recuperación.
7. Probar con dataset sintético y usuarios de roles distintos.
8. Remediar con cambios revisables y rollback.
9. Repetir auditoría y documentar riesgo residual.

## Laboratorio
Instancia local PostgreSQL/SQLite con usuarios ficticios. Crear roles de solo lectura/escritura, probar inyección sobre fixture vulnerable y validar backup/restore.

## Evaluación
Privilegios mínimos, conexiones cifradas, consultas seguras, auditoría y restore comprobados.

## Referencias
CIS Benchmarks, OWASP SQL Injection Prevention, NIST SP 800-123, PostgreSQL Security, MongoDB Security Checklist y SQLite security guidance.

## Instrucciones para agentes IA
No consultes datos reales ni exportes tablas completas. Usa esquemas y fixtures sintéticos. No ejecutes cambios de esquema o grants en producción sin aprobación.

## Arquitectura
El plano de datos incluye clientes, proxies/pools, motor de base de datos, autenticación, autorización, esquemas, almacenamiento, réplicas, backups, auditoría y consumidores analíticos. Trazar conexiones, cuentas técnicas, roles, secretos, cifrado, procedimientos almacenados, extensiones y rutas administrativas. Separar entornos y tenants; restringir acceso de red y privilegios por esquema/operación. Las réplicas, exportaciones, snapshots, logs y backups pueden contener el mismo dato sensible que el primario y deben incluirse en el inventario y ciclo de vida.
