# Skill candidata — Análisis integrado de propiedades de sistema

**ID:** SKILL-FND-01-01-INTEGRATED-PROPERTY-ANALYSIS  
**Estado:** draft_candidate_not_registered  
**Área:** Foundations / FND-01.01  
**Tipo:** metodología de análisis; no ejecutable ni activa.

## Patrón de tarea
Analizar un sistema socio-técnico y construir una matriz coherente de seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia.

## Precondiciones
- Autorización y alcance explícitos.
- Sistema, misión, funciones esenciales, actores y límites identificados.
- No realizar cambios en producción ni pruebas intrusivas.
- Fuentes y versión de estándares declaradas.
- Identificar datos personales, sectores regulados y autoridad de aceptación de riesgo.

## Entradas
Descripción del sistema; arquitectura y dependencias; flujos de datos; activos; perfiles de actor; requisitos de misión; peligros; amenazas; modos de fallo; restricciones legales/contractuales; tolerancia al riesgo.

## Método
1. Delimitar sistema, misión, fronteras y personas afectadas.
2. Identificar activos, funciones esenciales, interfaces y dependencias.
3. Separar peligros de safety, amenazas de security, fallos de reliability, interrupciones de availability/resilience y acciones de datos de privacy.
4. Construir la matriz de propiedades: definición, actor, objeto, condición, fallo, consecuencia, requisito y evidencia.
5. Identificar conflictos fail-safe/fail-secure/fail-operational, logging/privacy, patching/reliability, redundancy/common-cause y backup/trust.
6. Seleccionar métodos adecuados: HAZOP, FMEA/FMECA, FTA, STPA, threat modeling, attack trees, TARA y privacy threat modeling. Justificar aplicabilidad.
7. Mapear estándares por alcance; no inferir equivalencia ni obligatoriedad.
8. Construir claims, argumentos, evidencia, supuestos, incertidumbre y riesgos residuales.
9. Definir verificación, métricas, criterios de rechazo y plan de revisión.
10. Registrar límites, fuentes no leídas, dependencias y preguntas sin resolver.

## Salidas
- Matriz integrada de propiedades.
- Registro de hazard/threat/failure/privacy actions.
- Mapa de controles y trade-offs.
- Assurance case con claim-argument-evidence.
- Registro de fuentes y estados de revisión.
- Lista de brechas, supuestos y tareas de validación.

## Validación
- No confunde seguridad con safety.
- No confunde privacidad con confidencialidad.
- No infiere verdad de hash/firma.
- No infiere resiliencia de uptime/backup.
- Toda afirmación crítica tiene fuente y estado de revisión.
- Cada control tiene método de verificación y criterio de rechazo.
- Riesgo residual requiere autoridad competente.
- La aplicabilidad legal requiere revisión profesional.

## Límites
No es certificación, concepto jurídico, hazard analysis formal aprobado ni prueba operativa. No usar para decidir sobre un sistema crítico sin especialistas de safety/security/privacy y autoridad responsable.

## Promoción
Solo puede proponerse desde ledger con dos ejecuciones completadas, evidencia íntegra, revisión independiente por rol distinto y firma de aprobación externa según docs/SKILL_PROMOTION.md.
