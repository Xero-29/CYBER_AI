# Investigación técnica: Seguridad y protección de datos

**ID:** data_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas de privacidad y recuperación pendientes.

## Modelo de datos
Inventariar datos estructurados/no estructurados, secretos, PII, datos sensibles, logs, backups, telemetría, embeddings, modelos, exports y copias. Clasificar por sensibilidad, propósito, propietario, jurisdicción, retención, flujo, ubicación y riesgo de reidentificación. Mapear creación, ingestión, uso, compartición, archivo y destrucción.

## Controles de protección
- Minimización y purpose limitation: recolectar solo lo necesario.
- Access control: autorización por identidad, recurso, tenant y contexto.
- Encryption in transit/at rest con gestión de claves independiente.
- Tokenization/pseudonymization cuando proceda; no confundir con anonimización.
- DLP y egress control con validación de falsos positivos.
- Retention schedules, legal hold y borrado verificable.
- Backups cifrados, pruebas de restore y separación de credenciales.
- Logging con redacción, acceso restringido y retención definida.
- Data integrity, lineage, versionado y provenance.

## Bases de datos y almacenamiento
Revisar permisos, roles, row/column-level security, encryption, backups, replicas, snapshots, object ACLs, bucket policies, query logs, secrets, connection pooling y datos de prueba. Proteger exportaciones y caches; borrar en origen no elimina necesariamente réplicas, snapshots, logs o backups.

## Privacidad y analítica
Evaluar reidentificación, linkage, membership inference, inference attacks, sensitive attributes, telemetry leakage y transferencias. Privacy by design requiere modelar amenazas y medir utilidad vs privacidad. Differential privacy solo ofrece garantías bajo parámetros, composición y modelo definidos; no es un interruptor genérico.

## Data lifecycle y respuesta
Definir clasificación, acceso, retención, archivado, exportación, eliminación, recuperación y notificación. En brechas identificar datos, sujetos, alcance, tiempo, acceso, exfiltración probable, controles, jurisdicción y obligación de notificar; coordinar legal y privacidad.

## Laboratorios
Dataset sintético multi-tenant, policies por fila/columna, export, cache, logs y backup. Probar aislamiento cross-tenant, redaction, retention expiry, restore y borrado en réplicas. Medir precision/recall DLP y leakage rate.

## Fuentes
- NIST Privacy Framework: https://www.nist.gov/privacy-framework
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST AI RMF: https://doi.org/10.6028/NIST.AI.100-1

**Límite:** síntesis general; determinar jurisdicción, base jurídica y controles sectoriales antes de tratamiento real.
