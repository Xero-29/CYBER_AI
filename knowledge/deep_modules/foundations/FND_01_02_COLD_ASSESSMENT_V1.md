# FND-01.02 — Instrumento de evaluación en frío V1

**Estado:** preparado; no administrado.  
**Uso:** evaluación teórica individual, sin ejecución de herramientas ni acceso a laboratorio real.  
**Tiempo sugerido:** 90–120 minutos.  
**Material permitido:** apuntes y fuentes primarias citadas.  
**No contiene clave de respuestas.** La guía del evaluador y la clave deben mantenerse separadas del paquete público.

## Instrucciones

Responda con definiciones precisas, supuestos, contraejemplos y evidencia. No se aceptan respuestas que solo enumeren controles. Cuando una afirmación dependa del contexto, identifique el contexto y los límites.

## Parte A — Distinciones conceptuales (20 puntos)

1. Defina confidencialidad, integridad y disponibilidad con el objeto protegido, el actor y el criterio temporal.
2. Explique por qué integridad criptográfica no demuestra exactitud ni verdad semántica.
3. Diferencie autenticación, autenticidad de mensaje, autorización y atestación.
4. Explique por qué privacidad puede fallar aunque no exista divulgación no autorizada.

## Parte B — Contraejemplos y límites (20 puntos)

5. Construya un caso donde un artefacto tenga hash y firma válidos, pero no sea seguro ni correcto.
6. Construya un caso donde un servicio tenga alta disponibilidad y aun así incumpla una función de safety.
7. Explique una situación en la que fail-closed incremente el riesgo de daño.
8. Demuestre por qué dos nodos redundantes pueden fallar por causa común.

## Parte C — Modelado y controles (30 puntos)

9. Para un SaaS multi-tenant, construya una matriz de propiedades C/I/A, autenticidad, accountability y privacidad; asigne amenaza/fallo, control y evidencia a cada una.
10. Para un controlador OT, modele un escenario con amenaza cibernética, hazard de safety y fallo de disponibilidad. Defina una transición segura y el criterio de recuperación.
11. Diseñe un proceso de non-repudiation para una aprobación crítica. Incluya identidad, custodia de claves, tiempo, revocación, logs, contexto y límites jurídicos.
12. Proponga métricas para reliability, availability y resilience. Declare los supuestos de cada métrica y explique qué no demuestra.

## Parte D — Síntesis de assurance (30 puntos)

13. Elabore un claim principal sobre la confianza en un sistema crítico y descompóngalo en subclaims de seguridad, safety, privacidad, confiabilidad y resiliencia.
14. Para cada subclaim, indique evidencia requerida, método de verificación, incertidumbre, supuestos y condición de rechazo.
15. Seleccione FIPS 199, NIST CSF 2.0, NIST SP 800-160, NISTIR 8062 e IEC 62443/61508 según el caso. Explique alcance, complementariedad y límites. No trate todos los documentos como equivalentes ni obligatorios en cualquier sector.

## Rúbrica de evaluación

| Dimensión | Puntos | Criterio |
|---|---:|---|
| Precisión conceptual | 25 | No confunde propiedades; define alcance, actor y contexto |
| Modelado de escenarios | 20 | Separa amenaza, hazard, fallo, acción de datos y consecuencia |
| Diseño de controles | 20 | Propone controles verificables y analiza efectos secundarios |
| Evidencia y métricas | 20 | Vincula claims, evidencia, supuestos, límites y métricas |
| Incertidumbre y criterio crítico | 15 | Reconoce lagunas, no extrapola estándares y define condiciones de rechazo |

## Fallos críticos

Cualquiera de estos errores impide aprobar, aunque el puntaje numérico supere el umbral:
- afirmar que firma válida equivale a software seguro;
- afirmar que hash válido equivale a dato verdadero;
- equiparar privacidad con confidencialidad;
- equiparar disponibilidad con resiliencia;
- equiparar seguridad informática con safety;
- tratar non-repudiation como garantía absoluta;
- presentar FIPS 199 o NIST CSF 2.0 como estándar universal obligatorio;
- aceptar una afirmación sin evidencia o sin supuestos explícitos.

## Resultado

Este instrumento solo permite preparar una evaluación en frío. Para emitir un resultado individual se requiere administración, respuestas originales, puntuación por criterio, segundo evaluador independiente y adjudicación de discrepancias. No asignar T1/T2 ni marcar capacidades aprobadas por el mero hecho de haber creado el instrumento.
