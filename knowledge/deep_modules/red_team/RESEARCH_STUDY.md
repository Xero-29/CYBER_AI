# Investigación técnica: Red Team autorizado y emulación de adversarios

**ID:** red_team · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Ejercicios reales pendientes.

## Propósito y límites
Red Team evalúa capacidad de prevenir, detectar y responder mediante escenarios adversariales autorizados. No equivale a pentest de vulnerabilidades ni a ejecutar payloads sin límite. Debe existir Rules of Engagement, scope, autorización escrita, objetivos, exclusiones, ventanas, contactos, stop conditions, manejo de datos y plan de recuperación.

## Diseño
Partir de objetivos de negocio y threat model. Elegir adversario/escenario, ATT&CK techniques, supuestos, controles esperados y señales observables. Definir emulación segura, simulación o purple team. No copiar TTP sin evaluar riesgo y seguridad operacional.

## Fases
Planning, scoping, threat intelligence, attack path hypothesis, controlled execution, detection/response observation, evidence, deconfliction, cleanup, reporting y retest. Cada paso debe tener precondition, expected effect, potential impact, approval, rollback y evidencia.

## Seguridad de ejecución
Usar infraestructura de laboratorio o targets autorizados, cuentas sintéticas, payloads benignos, egress control, rate limits, logging y kill switch. Prohibir persistencia destructiva, exfiltración de datos reales y movimiento a terceros no incluidos. En OT/sistemas físicos usar simulación y aprobación safety.

## Métricas
Objetivos logrados, detecciones, time-to-detect/respond, control failures, false negatives, blast radius, operational impact, cleanup success y remediation closure. No usar “compromised” sin evidencia suficiente ni atribuir éxito solo por ejecución de comando.

## Purple team
Convertir cada observación en detección/mitigación verificable, test de regresión y owner. Registrar qué telemetría faltó, qué alerta no escaló y qué control no impidió la acción.

## Fuentes
- MITRE ATT&CK: https://attack.mitre.org/
- NIST SP 800-115: https://doi.org/10.6028/NIST.SP.800-115
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- CISA Rules of Engagement resources: https://www.cisa.gov/

**Límite:** SP 800-115 es de 2008 y no es programa exhaustivo; adaptar a normas actuales y reglas de autorización.
