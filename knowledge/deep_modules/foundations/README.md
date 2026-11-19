# Foundations — índice del módulo

**ID:** `foundations`  
**Versión del índice:** 1.4.0  
**Corte:** 2026-11-19  
**Madurez editorial:** M2 ampliado. No equivale a validación experta, experimental ni científica.

## Alcance

Foundations desarrolla los fundamentos transversales para analizar, diseñar y asegurar sistemas sociotécnicos. No sustituye los módulos especializados de identidad, redes, AppSec, criptografía, respuesta a incidentes, privacidad, safety o continuidad.

El desarrollo se organiza en doce bloques disciplinares:

1. Naturaleza de seguridad, safety, privacidad, confiabilidad y resiliencia.
2. Sistemas, misión, activos, stakeholders, pérdidas y consecuencias.
3. Confianza, políticas, mecanismos, estados, grafos y límites.
4. Ingeniería de sistemas seguros y ciclo de vida.
5. Amenazas adversariales, fallos, accidentes y análisis causal.
6. Debilidades, vulnerabilidades, exposición y riesgo contextual.
7. Probabilidad condicionada, incertidumbre, pérdida y sensibilidad.
8. Controles, verificación, validación y assurance cases.
9. Gobierno, responsabilidades, terceros y cadena de suministro.
10. Privacidad, safety, continuidad y recuperación.
11. Estándares y marcos: alcance, versiones y no equivalencia.
12. Observabilidad, métricas, evaluación y método científico.

## Documentos del módulo

- [Mapa curricular exhaustivo V2](FOUNDATIONS_CURRICULUM_MAP_V2.md): nueve unidades disciplinares, subunidades, dependencias, fronteras y brechas G1. Mapa en progreso; no es aprobación de cobertura.
- [Registro de ejecución en frío](../../COLD_KNOWLEDGE_EXECUTION_LOG_2026-11-19.md): línea base y cambios verificados.

- [Protocolo obligatorio de aceptación en frío](../../COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md): enseñanza, explicación, análisis, diseño, rúbrica, corrección iterativa y gate de salida.

- [Compendio técnico base](TECHNICAL_COMPENDIUM.md): modelos, procedimientos, ejemplos y laboratorio introductorio.
- [Desarrollo disciplinar ampliado y auditoría por tema](FOUNDATIONS_DEEP_DEVELOPMENT_V1.md): siete dossiers alineados con el currículo, doce capas, protocolos, métricas y límites.
- [Revisión de fuentes y trazabilidad](SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md): secciones primarias inspeccionadas, hallazgos aplicados, afirmación→fuente→capa y brechas abiertas.
- [Dictamen de auditoría interna](FOUNDATIONS_AUDIT_VERDICT_2026-11-19.md): resultado, evidencias CI/labs, no conformidades y criterios obligatorios para aceptación.
- [Remediación de no conformidades](NONCONFORMITY_REMEDIATION_2026-11-19.md): correcciones ejecutadas, evidencia nueva y bloqueos restantes.
- [Actualización de fuentes](SOURCE_UPDATE_ADDENDUM_2026-11-19.md): versiones, erratas y cambios oficiales recientes.
- [Evaluación de competencia](FOUNDATIONS_COMPETENCY_ASSESSMENT_V1.md): 21 ejercicios A/B/C para los siete temas.
- [Clave del evaluador](FOUNDATIONS_ASSESSOR_KEY_V1.md): criterios de corrección; mantener separada durante evaluación ciega.
- [Laboratorios reproducibles](labs/README.md): siete laboratorios de referencia local, pruebas, resultados y límites explícitos.
- [Agenda de investigación](RESEARCH_AGENDA.md): preguntas, hipótesis y diseños experimentales propuestos.
- [Revisión exploratoria de literatura](LITERATURE_REVIEW.md): mapa bibliográfico y estado real de lectura.
- [Pack de conocimiento](../../packs/foundations/README.md): guía de dominio para consumo por agentes y usuarios.
- [Estándar obligatorio](../../EXPERT_RESEARCH_STANDARD.md): doce capas, plantilla por tema, niveles T0–T5 y O0–O5 separados, y puertas G1–G8.
- [Auditoría de las 48 especialidades](../../research/DOMAIN_LAYER_AUDIT_48.md): línea base global de cobertura.

## Estado verificado

**Criterio de aceptación actualizado:** las 84 celdas siguen en progreso; ninguna se aprueba por estructura o presencia documental. La evaluación en frío debe demostrar enseñanza, explicación, análisis y diseño por tema. La nueva rúbrica común está en `knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md`.

| Elemento | Estado |
|---|---|
| Compendio base | Existe; ampliación editorial pendiente de auditoría tema×capa |
| Desarrollo disciplinar ampliado | Incorporado; revisión técnica independiente pendiente |
| Brechas FND-01–FND-15 | Tratamiento documental descrito; evidencias externas pendientes |
| Fuentes | Secciones pertinentes de fuentes primarias inspeccionadas y trazadas; lectura lineal integral de todas las obras no acreditada |
| Laboratorios | Siete labs locales con datos sintéticos; JWS HS256 y cadena HMAC implementados como prototipos de referencia; suite ampliada en CI multi-Python |
| Evaluación | Rúbrica y métricas diseñadas; aplicación y benchmark pendientes |
| Skills | Cinco especificaciones candidatas; no validadas ni promovidas |
| Auditoría 7 temas × 12 capas | 84 estados `in_progress`; dossiers y fuentes por secciones; ningún estado `passed` |
| Puertas G1–G8 | G1–G7 `in_progress`; G8 `blocked`; ninguna `passed` |

## Regla de cierre

No avanzar al módulo siguiente hasta cerrar cada tema con evidencia trazable. La auditoría documental por siete temas ya fue incorporada, pero sigue en progreso: falta ampliar lectura integral de fuentes, réplica independiente, integración con IdP/KMS/SIEM reales en laboratorio aislado y revisión independiente. Los experimentos sintéticos locales están ejecutados; réplica independiente, integración real aislada y revisión externa permanecen pendientes.

No declarar K4/K5, M4/M5 ni validación experta por la mera existencia de documentos, referencias, protocolos o Skills candidatas.
