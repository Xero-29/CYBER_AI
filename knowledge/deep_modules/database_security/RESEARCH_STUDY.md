# Investigación técnica: Seguridad de bases de datos

**ID:** database_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas en motores objetivo pendientes.

## Modelo
Inventariar motor/version, topology, nodes, replication, backups, users/roles, schemas, extensions, network endpoints, encryption, logs, data classification, applications y DBA access. Incluir SQL y NoSQL: PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, MongoDB, Redis, Cassandra, DynamoDB y servicios gestionados.

## Control de acceso
Least privilege, separation of duties, role hierarchy, row/column-level security, tenant isolation, privileged access, service identity, secret rotation y audit. Evitar cuentas compartidas y roles DBA para aplicaciones. Validar autorización en query, stored procedures, views, exports, caches y replicas.

## Integridad y aplicación
Parameterized queries, prepared statements, stored procedure safe usage, input validation, ORM pitfalls, SQL injection, NoSQL operator injection, mass assignment, unsafe deserialization, query complexity y business logic. Validar migraciones y schema changes con review y rollback.

## Protección de datos
TLS, encryption at rest, KMS/HSM, TDE, column encryption, tokenization, backups, snapshots, logs, replication, key rotation y retention. Cifrado en reposo no protege de una aplicación autorizada comprometida ni de DBA con privilegios suficientes.

## Operación
Patch management, secure configuration, network isolation, audit logging, monitoring, backup restore, replication consistency, failover, secure disposal y secrets management. Servicios gestionados tienen responsabilidad compartida.

## Laboratorios
Instancias desechables con datos sintéticos; probar privilege matrix, SQL/NoSQL injection safe payloads, row-level tenant isolation, backup/restore, TLS, key rotation, audit trails y resource exhaustion. No usar datos reales.

## Fuentes
- OWASP Database Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**Límite:** cada motor y versión tiene mecanismos distintos; verificar configuración efectiva, no solo defaults documentados.
