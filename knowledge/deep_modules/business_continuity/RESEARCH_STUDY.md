# Investigación técnica: Continuidad de negocio, resiliencia y recuperación ante desastres

**ID:** business_continuity · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas de recuperación pendientes.

## Gobierno y análisis de impacto
Definir servicios críticos, dependencias, procesos, personas, instalaciones, proveedores, datos, RTO, RPO, MTPD/MAO, tolerancia y owner. Business Impact Analysis debe considerar impacto financiero, legal, safety, cliente, reputación y operación a lo largo del tiempo.

## Estrategias
Alta disponibilidad no sustituye backup; backup no sustituye DR; DR no sustituye continuidad de negocio. Diseñar redundancy, failover, alternate sites, offline backups, immutable copies, data replication, manual workarounds, alternate suppliers y crisis communication. Evaluar shared failure domains y credential isolation.

## Recuperación cibernética
NIST SP 800-184 guía planificación, playbooks, pruebas y mejora de recuperación tras eventos cibernéticos. Definir clean-room restore, golden images, identity recovery, key recovery, dependency order, malware eradication, integrity verification y heightened monitoring. Recuperar desde backup comprometido puede reintroducir persistencia.

## Pruebas
Tabletop, component restore, application restore, site failover, cyber recovery simulation y full DR exercise. Medir RTO/RPO real, restore success, data integrity, dependencies, operator workload y time-to-safe-service. Un backup job successful no demuestra que el dato sea recuperable.

## Métricas
Service availability, RTO/RPO achieved, backup age, restore success, immutable backup coverage, recovery dependencies, exercise findings, supplier resilience y time to validate clean state.

## Fuentes
- NIST SP 800-184 Cybersecurity Event Recovery: https://doi.org/10.6028/NIST.SP.800-184
- NIST SP 800-34 Rev. 1: https://doi.org/10.6028/NIST.SP.800-34r1
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29

**Límite:** SP 800-34 Rev. 1 es antiguo; adaptar a cloud, ransomware, identidad y requisitos sectoriales actuales.
