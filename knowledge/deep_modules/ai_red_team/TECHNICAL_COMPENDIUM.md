# Compendio técnico: Red Team de IA y agentes

ID: `ai_red_team` · Versión: 1.0.0 · Idioma: español.  
**Estado:** mapa disciplinar y guía de navegación. El contenido técnico por tema vive en `AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md`; el protocolo ejecutable propuesto vive en `AI_RED_TEAM_TEST_CATALOG_V1.md`. Este archivo no duplica esos capítulos ni declara validación operativa.

## 1. Alcance del dominio

El Red Team de IA evalúa el sistema sociotécnico completo: modelo y versión, aplicación, instrucciones, ensamblado de contexto, RAG, corpus, memoria, herramientas, agentes, conectores, identidad, infraestructura, proveedor, personas y gobierno.

La unidad de resultado es el efecto observable, no la respuesta textual. Una negativa del modelo no demuestra seguridad si una herramienta ya se invocó, un dato ya se recuperó o un estado ya cambió.

### Fuera de alcance

- Auditoría de seguridad de un proveedor externo sin autorización contractual.
- Uso de secretos, datos personales o modelos de terceros no autorizados.
- Pruebas que ejecuten acciones externas, destructivas o con impacto físico.
- Certificación de seguridad universal de un modelo a partir de un benchmark.

## 2. Mapa de siete líneas de trabajo

| Línea | Pregunta central | Evidencia mínima específica |
|---|---|---|
| 1. Plan y threat model | ¿Qué activos, actores, capacidades y rutas están dentro del alcance? | scope manifest, arquitectura, DFD, trust boundaries y escenarios |
| 2. Prompt injection | ¿Contenido no confiable altera decisiones o acciones? | provenance, corpus/control de memoria, llamadas y efectos |
| 3. Tool misuse y agencia | ¿Puede el agente exceder función, permiso o autonomía? | principal, decisión server-side, schema, efecto y aprobación |
| 4. RAG poisoning y aislamiento | ¿Se altera corpus/recuperación o se cruza tenant? | hashes, ACL, filtros, IDs recuperados, cache keys y citas |
| 5. Exposición/extracción | ¿Se divulgan datos, secretos o contexto oculto? | canaries, canales probados, logs redactados y permisos |
| 6. Evaluación adversarial | ¿El resultado es válido, reproducible y no está contaminado? | dataset versionado, splits, denominadores, métricas por clase |
| 7. Retest y reporte | ¿La mitigación corrige el efecto sin romper utilidad? | baseline, diff, pruebas repetidas, regresiones y límites |

Cada línea está desarrollada en doce capas en el dossier teórico. El catálogo de pruebas contiene nueve casos con fixtures sintéticos, resultados esperados y criterios de fallo.

## 3. Arquitectura de referencia para evaluación

`Usuario/tenant → aplicación → ensamblador de contexto → modelo`

`                                             ↘ RAG/memoria`

`Modelo → broker de herramientas → PEP/autorización → servicio mock`

`                                     ↘ auditoría/provenance`

Las flechas representan flujos de datos o autoridad que deben evaluarse. El modelo no es un punto de enforcement. La autorización se aplica en un componente determinista fuera del modelo, con principal obtenido de identidad confiable.

## 4. Modelo de amenazas mínimo

Activos: datos y documentos, secretos, prompts privilegiados, identidad, scopes, permisos, memoria, corpus, modelos, configuración, herramientas, presupuesto, logs y reputación.

Actores: usuario malicioso, documento indirecto, proveedor comprometido, insider, tenant vecino, dependencia alterada y agente/herramienta defectuosos.

Superficies: entradas textuales y multimodales, retrieval, memoria, resultados de herramientas, serialización, conectores, APIs, pipelines de ingestión, cachés, logs, evaluación y actualización de modelos.

Para cada ruta: acceso, precondición, transición, activo, efecto, control esperado, telemetría, evidencia y regla de parada.

## 5. Controles arquitectónicos

- Autorizar cada operación en el servidor con identidad y política independientes del texto del modelo.
- Aplicar ACL por tenant en el servicio de datos; filtrar de nuevo resultados y citas.
- Etiquetar procedencia e integridad de cada fragmento de contexto.
- Reducir permisos, herramientas y autonomía a la mínima capacidad necesaria.
- Validar argumentos mediante esquemas cerrados y reglas semánticas.
- Requerir aprobación para efectos de alto impacto y verificar el aprobador fuera del modelo.
- Separar secretos del contexto y redactar logs.
- Limitar tokens, llamadas, tiempo, concurrencia y presupuesto.
- Mantener kill switch, revocación, rollback y preservación de evidencia.

No existe una mitigación única que elimine prompt injection. La estrategia es limitar consecuencias y detectar fallos de frontera.

## 6. Evaluación y reporte

Reportar por caso, modelo, versión, configuración y clase de riesgo. Incluir denominadores, intentos, efectos, severidad, falsos positivos, casos no aplicables, latencia, coste y limitaciones. No mezclar resultados de modelos o arquitecturas distintas sin estratificar.

El resultado se clasifica como PASS, FAIL, INCONCLUSIVE o NOT RUN. PASS se limita a la prueba y configuración exactas. Cero fallos en una muestra finita no equivale a riesgo cero.

## 7. Fuentes y control de versiones

Usar como mínimo:
- OWASP Top 10 for LLM Applications 2026 (taxonomía LLM).
- OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10; taxonomía separada): https://genai.owasp.org/top-10-for-agentic-applications-2026/.
- OWASP GenAI Red Teaming Guide/Manual (metodología de evaluación).
- NIST AI RMF y NIST AI 600-1 (gestión de riesgos).
- NIST AI 200-3 (planificación de evaluación ARIA).
- MITRE ATLAS (conocimiento adversario vivo).

Las fuentes candidatas, fechas de consulta y estados de lectura se registran en `knowledge/research/field_studies/SOURCE_REGISTER_2026-11-18.json`. Referencia o consulta de página no significa lectura integral ni respaldo automático de una afirmación.

## 8. Puertas de madurez

- Teórica: T0–T5.
- Operativa: O0–O5.
- Las dimensiones se evalúan por separado.
- El contenido de este compendio y del dossier es un borrador técnico; los laboratorios del catálogo están propuestos, no ejecutados.
- No elevar a T3/O3 sin pruebas repetibles con evidencia; no elevar a T4 sin revisión independiente cualificada; no elevar a T5 por volumen editorial.

## 9. Navegación

- [Desarrollo teórico profundo V1](AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md)
- [Catálogo de pruebas reproducibles V1](AI_RED_TEAM_TEST_CATALOG_V1.md)
- [Agenda de investigación](RESEARCH_AGENDA.md)
- [Estudio de investigación](RESEARCH_STUDY.md)
- [Secciones de profundización](DEEP_SECTIONS.md)
