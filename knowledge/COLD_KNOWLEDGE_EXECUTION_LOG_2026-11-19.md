# Registro de ejecución — conocimiento en frío CYBER_AI

## Corte 2026-11-19 — ciclo inicial

### Estado de repositorio comprobado
- Repositorio: `Xero-29/CYBER_AI`.
- Rama de trabajo: `knowledge/develop-foundations`.
- PR: #14, abierto. No se fusionó.
- `main`: no se realizaron escrituras.
- La rama fue localizada y se usó como destino de los cambios.
- Los commits de este ciclo se incorporaron secuencialmente mediante GitHub Contents API.

### Paso 0 — línea base y estándar
**Estado:** completado para la inspección documental inicial.

Archivos inspeccionados:
- `knowledge/EXPERT_RESEARCH_STANDARD.md`
- `knowledge/THEORETICAL_LIBRARY_COMPLETION_PROGRAM_48.md`
- `knowledge/research/DOMAIN_LAYER_AUDIT_48.json`
- `knowledge/deep_modules/foundations/FOUNDATIONS_DEEP_DEVELOPMENT_V1.md`
- `knowledge/deep_modules/ai_red_team/AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md`
- Índices README de Foundations y AI Red Team.
- Tracker global.

Hallazgos:
- El estándar ya separa madurez teórica T0–T5 y operativa O0–O5.
- La matriz histórica contiene 48 especialidades, 336 temas iniciales y 4.032 celdas tema×capa.
- Foundations: siete temas base × doce capas = 84 celdas coarse; todas `in_progress`, ninguna aprobada. La matriz granular V2 cubre 102 subtemas × 12 capas = 1.224 checks: 24 `in_progress` (FND-01.01/FND-01.02), 1.200 `not_assessed`; 8/408 capacidades en progreso y 400 no evaluadas; 0 aprobadas, 102 subtemas T0/O0. No interpretar 84/84 como cobertura del currículo granular.
- AI Red Team: siete temas base × doce capas = 84 celdas; todas siguen `in_progress`, ninguna aprobada.
- El dossier Foundations tiene 795 líneas y el dossier AI Red Team 418 líneas al corte de inspección. Estos tamaños no se usan como métrica de completitud.
- AI Red Team ya reconoce explícitamente que su currículo ampliado, lectura integral de fuentes y revisión independiente están pendientes.
- Foundations contiene material técnico específico y protocolos por tema, pero la matriz sigue en progreso y la evaluación no acredita por sí sola dominio experto.
- Los siete temas actuales son línea base; no bastan para demostrar exhaustividad disciplinar.

### Cambios aplicados
1. Se creó `knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md` con el proceso obligatorio paso a paso, las cuatro capacidades (enseñar, explicar, analizar y diseñar), rúbrica 0–4, fallos críticos, no conformidades y gate de salida.
2. Se vinculó el programa de las 48 especialidades al protocolo obligatorio.
3. Se actualizaron los índices Foundations y AI Red Team para aplicar la nueva regla y corregir la referencia obsoleta a K1–K5 por los ejes T/O.
4. Se actualizó el tracker global para registrar la regla y el orden Foundations → AI Red Team → otras 46.
5. Se creó `knowledge/deep_modules/foundations/FOUNDATIONS_CURRICULUM_MAP_V2.md` con nueve unidades curriculares y 102 subunidades identificables, dependencias y correspondencia con los siete temas históricos.

### Paso 1 — perfil y mapa curricular Foundations
**Estado:** mapa V2 incorporado; G1 sigue `in_progress`.

Evidencia:
- Nueve unidades curriculares FND-01 a FND-09.
- 102 subunidades identificadas.
- Matriz granular añadida: 1.224 comprobaciones subunidad×capa y 408 comprobaciones de enseñanza/explicación/análisis/diseño; todas `not_assessed` como línea base.
- Dependencias conceptuales y correspondencia con los siete IDs históricos.
- Frontera explícita entre Foundations y las especialidades que profundizan IAM, Crypto, Network, AppSec, OT, AI, etc.

Brechas abiertas:
- Validación de exhaustividad por especialista independiente.
- Descomposición de cada subunidad en objetivos, prerrequisitos, exclusiones y evidencias.
- Vinculación granular de cada subunidad con doce capas y cuatro capacidades.
- Revisión de solapamientos con los módulos especializados.
- Desarrollo y evaluación del contenido por subunidad.

### Estados que deliberadamente NO cambiaron
- No se marcó ninguna celda como `passed`.
- No se declaró T4 ni T5.
- No se declaró G1–G8 aprobada.
- No se promovieron Skills.
- No se atribuyeron resultados empíricos nuevos.
- No se declaró validación operativa ni científica.

### Siguiente paso obligatorio
Continuar Foundations, no saltar a AI Red Team: convertir FND-01 a FND-09 en unidades auditables, mapear sus subunidades a evidencia y detectar omisiones; después desarrollar y evaluar la primera unidad, iterando hasta cerrar no conformidades. Solo tras superar el gate completo de Foundations se inicia AI Red Team.

### Paso 2 — primera unidad Foundations FND-01.01
**Estado:** borrador disciplinar incorporado; todas las evidencias siguen en progreso.

- Documento: `knowledge/deep_modules/foundations/topics/FND-01-01_SECURITY_SAFETY_PRIVACY_RELIABILITY_RESILIENCE.md`.
- Desarrolla las doce capas y contiene una secuencia didáctica, errores conceptuales, explicación, escenario de análisis, desafío de diseño y rúbrica.
- Se registró revisión parcial de NIST Privacy Framework 1.0 y de dos entradas del NIST CSRC Glossary; no se afirma lectura integral.
- La fuente de privacidad existente se actualizó con alcance de revisión parcial; se añadió el registro del glosario NIST.
- La matriz granular refleja FND-01.01 en `in_progress` para doce capas y cuatro capacidades. Madurez T permanece T0 hasta evaluación; O0.

No conformidades abiertas: lectura integral de fuentes primarias; normas de safety sectoriales; análisis de aplicabilidad legal colombiana; administración de evaluación en frío; revisión disciplinar independiente. No se aprobó la unidad.

### Verificación automatizada del ciclo
- La matriz JSON se volvió a leer y parsear correctamente: 102 subunidades, 1.224 comprobaciones de capas, 408 comprobaciones de capacidades y 0 aprobaciones.
- La fila FND-01.01 coincide entre JSON y Markdown: 12 capas y 4 capacidades en progreso.
- Las ejecuciones CI asociadas a un commit intermedio de este ciclo terminaron canceladas; el commit más reciente de documentación no tiene ejecuciones CI asociadas al momento de esta verificación. Por tanto, no se declara CI verde ni validación automatizada del ciclo completo.
- La rama `knowledge/develop-foundations` sigue existiendo. No se fusionó PR #14 y no se escribió en `main`.

### Paso 3 — FND-01.02: propiedades CIA y ampliadas
**Estado:** borrador de doce capas y cuatro capacidades incorporado; no aprobado.

- Documento: `knowledge/deep_modules/foundations/topics/FND-01-02_SECURITY_PROPERTIES_CIA_EXTENDED.md`.
- Desarrolla confidencialidad, integridad, disponibilidad, autenticidad, autenticación, accountability, trazabilidad, auditabilidad, no repudio, frescura, secuencia y unicidad; incluye invariantes, lógica temporal esquemática, arquitectura, trade-offs, amenazas, pregunta de investigación, laboratorio conceptual, métricas, Skill conceptual y evaluación.
- Se actualizó el registro de fuentes: se identificó NIST Privacy Framework 1.1 CSWP 40 IPD (14-04-2025) como borrador público inicial, distinto de PF 1.0 final. Se revisaron secciones 1.2.1–1.2.3, Core y Appendix D por líneas; no se afirma lectura integral.
- FND-01.01 recibió una actualización documental que diferencia PF 1.0 final de PF 1.1 IPD y explica que el riesgo de privacidad puede surgir sin incidente cibernético.
- La matriz granular refleja FND-01.01 y FND-01.02 en progreso: 24/1.224 comprobaciones de capas y 8/408 capacidades; 0 aprobadas. Las otras 100 subunidades permanecen sin evaluar.
- No conformidades de FND-01.02: lectura integral de estándares; evaluación en frío; revisión independiente; aplicabilidad sectorial/colombiana.

### Paso 4 — instrumento de evaluación en frío para FND-01.01
**Estado:** instrumento y guía del evaluador preparados; no administrados.

- `knowledge/deep_modules/foundations/topics/FND-01-01_COLD_ASSESSMENT_V1.md`: prueba de transferencia con bloques de enseñanza, explicación, análisis, diseño e integración, más fallos críticos y criterios de evaluación.
- `knowledge/deep_modules/foundations/topics/FND-01-01_ASSESSOR_GUIDE_V1.md`: criterios de corrección, elementos esperados y límites de la guía.
- La matriz registra ambos documentos como evidencia. La no conformidad de evaluación sigue abierta porque no se ha administrado ni calificado por un evaluador independiente.
- El instrumento no cambia T0/O0 ni aprueba la subunidad.

## Ciclo adicional — FND-01.01 profundización técnica

- Añadido `knowledge/deep_modules/foundations/topics/FND-01-01_TECHNICAL_DEEPENING_CASEBOOK_V1.md`.
- Contenido: delimitación de propiedades; modelos de confiabilidad/disponibilidad con supuestos; árbol de fallos; análisis de safety y privacidad; caso hipotético de dosificación de agua; escenarios causales; requisitos verificables; modos degradados; variantes de evaluación en frío y diseño de investigación.
- Verificación editorial estática: estructura de nueve secciones, cuatro variantes nuevas, cinco requisitos de ejemplo y límites de evidencia explícitos.
- Matriz: el anexo se enlaza como evidencia; FND-01.01 permanece con 12 capas y 4 capacidades `in_progress`, T0/O0; se añade NC-FND-01.01-05.
- No se declara lectura integral de fuentes, cumplimiento legal colombiano, revisión sectorial, evaluación administrada, revisión independiente ni ejecución de laboratorio.

## Ciclo de investigación primaria — NIST SP 800-160 Vol. 1/2

- Inspeccionadas secciones oficiales seleccionadas de los PDF NIST SP 800-160 Vol. 1 Rev. 1 (195 páginas) y Vol. 2 Rev. 1 (310 páginas).
- Hallazgos aplicados: seguridad como propiedad emergente; contexto y assurance case; confianza composicional; protección continua en transiciones; objetivos de resiliencia anticipar/resistir/recuperar/adaptar; complementariedad con CIA.
- Añadido `knowledge/deep_modules/foundations/SOURCE_REVIEW_ADDENDUM_NIST_800_160_2026-11-19.md` y actualizado `knowledge/research/source_registry.json` con estado `selected_sections_reviewed`.
- No se afirma lectura lineal integral, ni revisión de todas las referencias, ni ejecución. FND-01.01 sigue T0/O0 y no aprobado.

## Ciclo de alcance colombiano — FND-01.01

- Consultadas fuentes oficiales: Ley Estatutaria 1581/2012 (arts. 1–4, 6 y 8–10), Decreto 1575/2007 (arts. 1–2) y Resolución 2115/2007 (arts. 1–5 y tablas iniciales).
- Añadido `knowledge/deep_modules/foundations/COLOMBIA_APPLICABILITY_FND_01_01_2026-11-19.md`, con árbol condicional de aplicabilidad y límites.
- Registradas las tres fuentes en `knowledge/research/source_registry.json` como `selected_articles_reviewed`.
- NC-FND-01.01-02 se reduce parcialmente: privacidad y agua de consumo humano tienen un mapa inicial; safety funcional y obligaciones sectoriales siguen sin determinarse para un caso concreto y requieren revisión competente.
- No se emite dictamen legal ni se declara cumplimiento; T0/O0 sin cambios.

## Ciclo de demostración de capacidades — FND-01.01

- Añadido `knowledge/deep_modules/foundations/topics/FND-01-01_CAPABILITY_WORKED_SOLUTIONS_V1.md`.
- Enseñar: resultados observables, progresión, errores conceptuales y ejercicios graduados con solución.
- Explicar: reconstrucción del flujo funcional, autorización, estados y propiedades emergentes.
- Analizar: escenario nuevo de pérdida de IdP, discrepancia de sensores, regiones con causa común y telemetría personal; alternativas y condiciones de decisión.
- Diseñar: requisitos trazables, arquitectura, plan de verificación por etapa y argumento de assurance con claims/evidencia/derrotadores.
- Matriz enlaza el documento, pero las cuatro capacidades siguen `in_progress`; la evaluación ciega y la revisión independiente no se han realizado.

## Ciclo de corrección del instrumento — FND-01.01

- Auditoría detectó error aritmético en V1: los pesos 20+20+30+30+10 sumaban 110, pese a indicar 100 normalizados.
- Añadido `topics/FND-01-01_COLD_ASSESSMENT_V2.md`: pesos 15+15+30+30+10=100, cinco capacidades, tres variantes nuevas, criterios de transferencia y fallas críticas.
- Añadido `topics/FND-01-01_INDEPENDENT_ASSESSOR_PROTOCOL_V1.md`: separación autor/evaluador, anonimización, calibración, doble puntuación, adjudicación y evidencia mínima.
- V1 marcada como supersedida. Matriz enlaza V2 y protocolo; NC-FND-01.01-03 permanece abierta porque no se ha administrado la prueba ni existen evaluadores externos cualificados/independientes.
- T0/O0 sin cambios. No se declara competencia demostrada.

## Verificación de metadatos oficiales NIST — FND-01.01

- Consultadas las páginas oficiales CSRC de SP 800-160 Vol. 1 Rev. 1 Final (noviembre de 2022) y Vol. 2 Rev. 1 Final (diciembre de 2021).
- Se verificaron título, revisión, estado final, fecha, DOI y URL oficial de descarga; el registro refleja `official_metadata_reviewed_on` y `publication_status: final`.
- Esta comprobación confirma versión y procedencia de las publicaciones; no equivale a lectura integral de sus PDF ni cierra NC-FND-01.01-01/06.


## Ciclo de remediación de trazabilidad y evaluación — FND-01.01

- Añadido `FND_01_01_PRIMARY_SOURCE_SYNTHESIS_2026-11-19.md`: contraste explícito de NIST SP 800-160 Vol. 1 Rev. 1, Vol. 2 Rev. 1 y NISTIR 8062; se documentan secciones inspeccionadas, consecuencias para el contenido y límites de lectura.
- Se confirmó en el PDF oficial de Vol. 1 Rev. 1 la cobertura de propiedades emergentes, confianza composicional y assurance cases. Para Vol. 2 Rev. 1 se consultaron abstract, marco, goals/objectives y técnicas seleccionadas. Para NISTIR 8062 se consultaron objetivos de privacidad y modelo de acciones problemáticas de datos.
- Añadido `topics/FND-01-01_ASSESSOR_GUIDE_V2.md`: anclas de corrección, expectativas por variante, criterios observables para fallas críticas, puntuación y adjudicación. Es material reservado; no es pilotaje ni validación psicométrica.
- Actualizados el documento principal, la matriz JSON/Markdown y el registro de fuentes. La matriz conserva FND-01.01 en 12 capas y 4 capacidades `in_progress`, T0/O0; no se cambió ninguna celda a `passed`.
- Persisten las brechas no resolubles por edición documental: lectura integral de fuentes/referencias, determinación de normas sectoriales según alcance concreto, revisión jurídica competente, administración supervisada con dos evaluadores independientes cualificados, pilotaje y revisión disciplinar independiente.


## Normalización de no conformidades — FND-01.01

- Se detectó solapamiento entre NC-FND-01.01-01 (lectura integral de fuentes primarias) y NC-FND-01.01-06 (lectura integral específica de NIST SP 800-160).
- Se consolidó el alcance de NC-01 para incluir expresamente NIST SP 800-160 y referencias críticas; se retiró NC-06 como duplicado. No se cerró ninguna brecha sustantiva.
- NC-05 permanece separada porque exige contraste disciplinar de modelos de confiabilidad/safety, no solo lectura de publicaciones.
- El número de NC abiertas de FND-01.01 pasa de seis a cinco por eliminación de duplicidad administrativa, no por aprobación de evidencia.
