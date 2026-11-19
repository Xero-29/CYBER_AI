# Investigación técnica: SOC, SIEM y SOAR

**ID:** soc_siem · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Evaluación con telemetría real pendiente.

## Modelo operacional
SOC combina personas, procesos, fuentes de datos, detecciones, casos, respuesta y mejora. SIEM ingiere/normaliza/correlaciona; SOAR orquesta tareas; ambos dependen de calidad de fuentes, identidad, reloj, retención, reglas, runbooks y analistas. La herramienta no sustituye modelo operacional.

## Telemetría
Inventariar endpoint, identidad, DNS, DHCP, proxy, firewall, network flow, cloud control plane, email, application, database, OT y SaaS. Definir schema, parser, timestamp, source identity, retention, sensitivity, owner, completeness y integrity. ATT&CK Data Sources fue deprecado en v18; diseñar detecciones con Detection Strategies/Analytics y telemetría realmente disponible.

## Ingeniería de detección
Definir hipótesis, amenaza, fuente, query, ventana temporal, baseline, threshold, suppression, severity, response y owner. Probar datos benignos, maliciosos y edge cases. Usar Sigma como formato portable si es apropiado, pero validar traducción al SIEM y semántica del backend. Correlación debe manejar late events, duplicate, timezone y missing logs.

## SOAR
Playbooks con preconditions, approvals, idempotency, timeout, rollback, evidence capture y escalation. Acciones destructivas (disable identity, isolate host, block network) requieren policy y aprobación conforme al impacto. Evitar loops automáticos y retries no acotados.

## Métricas
Alert precision, recall estimado, false positives per analyst-hour, alert backlog, MTTD/MTTA/MTTR, coverage de logs, detection latency, playbook success, rollback, analyst workload y incident recurrence. ATT&CK coverage no equivale a detection effectiveness.

## Laboratorios
Dataset de logs sintéticos, SIEM local, reglas Sigma, pipeline de parsing, correlación de identity/network/endpoint y SOAR mock. Inyectar eventos con retraso, duplicados, campos ausentes y timestamps erróneos; medir robustez.

## Fuentes
- NIST SP 800-94 IDPS (2007; guía antigua): https://doi.org/10.6028/NIST.SP.800-94
- NIST SP 800-137 Continuous Monitoring: https://doi.org/10.6028/NIST.SP.800-137
- MITRE ATT&CK: https://attack.mitre.org/
- MITRE D3FEND: https://d3fend.mitre.org/
- Sigma: https://sigmahq.io/

**Límite:** SP 800-94 es antiguo y su borrador Rev. 1 fue retirado; complementar con plataformas, detecciones y threat intel actuales.
