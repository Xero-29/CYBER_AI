# Investigación técnica: Forense digital en cloud

**ID:** cloud_forensics · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Ejercicio multi-cloud pendiente.

## Readiness
La evidencia cloud depende de provider logs, control plane, API events, identity, network, storage, snapshots, containers, serverless y SaaS. Diseñar forensic readiness antes del incidente: logging, retention, immutable storage, time sync, request IDs, permissions, legal hold, export procedures y contacto con proveedor.

## Retos
Multi-tenancy, elastic resources, ephemeral workloads, shared responsibility, provider-controlled infrastructure, region/residency, log delay, deletion, clock skew, API throttling y proprietary export formats. No asumir que el cliente puede adquirir memoria física o discos del host en servicios PaaS/SaaS.

## Arquitectura NIST SP 800-201
NIST SP 800-201 (final, julio 2024) ofrece Cloud Computing Forensic Reference Architecture para entender desafíos y mitigaciones de forensic readiness. Adaptar metodología a proveedor, servicio y caso; no tratar arquitectura de referencia como implementación automática.

## Adquisición
Preservar identity audit, management plane, object versions, flow logs, snapshots, image digests, serverless traces, key management events, email/SaaS audit y provider request IDs. Registrar API, cuenta, región, actor, timestamp, tool version, hash y chain of custody. Evitar cambios de estado que destruyan evidencia.

## Laboratorios
Cuenta de prueba multi-region, audit logs, storage versions, snapshot, serverless trace, container registry y evidence export. Simular key compromise, public bucket, IAM change y log retention gap. Medir evidence completeness, export latency, integrity, chain-of-custody and repeatability.

## Fuentes
- NIST SP 800-201 Cloud Forensic Reference Architecture: https://doi.org/10.6028/NIST.SP.800-201
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3
- NIST SP 800-144: https://doi.org/10.6028/NIST.SP.800-144

**Límite:** el procedimiento varía por proveedor/servicio y jurisdicción; preservar evidencia temprano y coordinar con legal/proveedor.
