# Investigación técnica: EDR, XDR y seguridad de endpoints

**ID:** edr_xdr · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Prueba multi-plataforma pendiente.

## Modelo
EDR observa y responde en endpoints; XDR correlaciona señales de múltiples capas. Documentar sensores, kernel/userland hooks, event pipeline, cloud console, identity integration, policy, agent update, isolation, retention y response actions. Evaluar cobertura por OS, versión, arquitectura, servidor, VDI, container y OT.

## Telemetría y detección
Process tree, command line, module load, file events, registry/config, network, auth, script, memory, persistence, driver, USB y security control state. Revisar integridad, timestamp, tampering resistance, privacy, sensor overhead y gaps. Correlacionar con ATT&CK pero validar cada técnica con evidencia.

## Respuesta
Containment, kill process, quarantine file, isolate host, collect triage package, rollback, live response y policy changes. Cada acción requiere autorización, scope, audit trail, timeout, rollback y break-glass. Aislamiento de endpoint puede romper OT, medical o procesos críticos; evaluar impacto antes.

## Evasión y límites
Tampering, driver abuse, log clearing, living-off-the-land, process injection, signed binary proxy, sensor bypass, kernel rootkit y cloud console compromise. No asumir que EDR ve todo; combinar network, identity, application y cloud telemetry. Validar privacidad y proporcionalidad de monitoreo.

## Evaluación
Test corpus controlado con comportamientos benignos/adversariales autorizados, ATT&CK emulation, detection fidelity, alert latency, sensor overhead, false positive, containment success y recovery. Medir visibilidad por OS/version y comportamiento; no usar solo porcentaje de ATT&CK.

## Laboratorios
VM Windows/Linux aisladas, endpoint agent de evaluación, event forwarder y test harness benigno. Simular process creation, script execution, autoruns, network callbacks locales, credential access simulada y log gaps. No ejecutar malware real ni payloads destructivos en endpoints productivos.

## Fuentes
- MITRE ATT&CK: https://attack.mitre.org/
- NIST SP 800-94 IDPS: https://doi.org/10.6028/NIST.SP.800-94
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1

**Límite:** EDR/XDR son categorías de producto no uniformes; comparar por evidencia, cobertura, privacidad, coste y response safety.
