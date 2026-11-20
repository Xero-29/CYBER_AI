# Programa de completitud teórica de las 48 especialidades — CYBER_AI

**Estado:** norma de ejecución para la primera etapa de la biblioteca.  
**Rama de trabajo:** `knowledge/develop-foundations`.  
**Alcance:** 48 especialidades del catálogo, sin excluir dominios ni reducirlos a una plantilla común.  
**Secuencia:** módulo por módulo; el módulo actual no se da por cerrado hasta superar sus criterios de completitud teórica.  
**Límite:** esta etapa no declara validación operativa, eficacia en producción ni resultados experimentales no ejecutados.

## Protocolo obligatorio de ejecución

La ejecución paso a paso, la rúbrica de enseñanza/explicación/análisis/diseño, los criterios de no conformidad y el gate de salida se rigen por [`knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md`](COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md). Ese protocolo es normativo para cada una de las 48 especialidades y prevalece sobre cualquier interpretación basada en volumen documental o presencia de encabezados.

## 1. Objetivo

Construir primero una biblioteca teórica, técnica y analítica de profundidad experta para todas las especialidades de ciberseguridad de CYBER_AI. La IA conectada debe poder consultar el conocimiento, reconstruir mecanismos, razonar sobre escenarios, comparar alternativas, diseñar soluciones y explicar sus límites sin depender de que el sistema haya ejecutado previamente cada herramienta.

La etapa fría debe terminar con conocimiento disciplinar profundo, trazable, estructurado, actualizado y evaluado. La ejecución de laboratorios y sistemas reales pertenece a una etapa posterior, salvo que una prueba estática o un cálculo reproducible sea necesario para verificar una afirmación teórica concreta.

## 2. Alcance cuantificado de la línea base

La auditoría inicial registra:
- 48 especialidades.
- 7 unidades temáticas iniciales por especialidad (336 unidades de línea base).
- 12 capas por unidad temática (4.032 comprobaciones tema×capa).
- 8 puertas de calidad por especialidad.

Las siete unidades actuales son una línea base, no un límite curricular. En G1 se deben descubrir y añadir subtemas esenciales que falten, dependencias, variantes tecnológicas y especializaciones; no se puede declarar cobertura total por limitarse a los siete temas iniciales.

La matriz canónica es `knowledge/research/DOMAIN_LAYER_AUDIT_48.json`; su vista humana es `knowledge/research/DOMAIN_LAYER_AUDIT_48.md`.

## 3. Dos ejes de madurez que no deben mezclarse

### 3.1 Madurez teórica (T)

- **T0 — No evaluada:** no existe mapa y evidencia suficiente para juzgar el tema.
- **T1 — Fundamental:** conceptos, terminología, alcance, fuentes y límites correctos.
- **T2 — Técnica:** mecanismos, arquitectura, estándares, variantes, ejemplos y procedimientos diseñados con detalle.
- **T3 — Avanzada:** análisis de casos límite, fallos, trade-offs, modelos formales pertinentes, ejercicios resueltos y síntesis crítica de literatura.
- **T4 — Experta teórica:** cobertura disciplinar defendible, fuentes primarias revisadas en profundidad, afirmaciones trazables, razonamiento avanzado, comparaciones críticas y revisión independiente por especialista.
- **T5 — Investigación teórica:** contribución original o síntesis científica de alto rigor, método explícito, argumentación/proposición formal o análisis conceptual novedoso, límites demostrados y revisión independiente. Si la contribución requiere evidencia empírica, no se declara T5 hasta ejecutar y analizar el estudio.

T4/T5 califican el conocimiento y razonamiento teórico. No implican que herramientas, integraciones, laboratorios o procedimientos hayan sido ejecutados.

### 3.2 Madurez operativa (O)

- **O0 — No ejecutada.**
- **O1 — Diseño de prueba y laboratorio especificado.**
- **O2 — Ejecución controlada en laboratorio con evidencia.**
- **O3 — Integración e interoperabilidad verificadas.**
- **O4 — Operación representativa, recuperación y rendimiento evaluados.**
- **O5 — Reproducción independiente y validación externa del desempeño.**

No asignar O2–O5 sin evidencia de ejecución correspondiente. Una configuración escrita, un script no ejecutado o un resultado esperado no constituyen ejecución.

Cada tema debe mostrar ambos ejes, por ejemplo: **T4 / O0** significa conocimiento teórico experto revisado, sin validación operativa todavía. No promediar T y O ni convertir uno en el otro.

## 4. Las doce capas: entregables de la etapa fría

Todas las capas se desarrollan durante la etapa teórica. El alcance de cada una se interpreta así:

1. **Fundamentos teóricos:** definiciones precisas, principios, taxonomías, supuestos, alcance, límites y evolución histórica.
2. **Fundamentos matemáticos y formales:** modelos, lógica, estadística, probabilidad, grafos, teoría de información, complejidad, criptografía formal o métodos pertinentes; justificar explícitamente la no aplicabilidad.
3. **Arquitectura y funcionamiento interno:** componentes, flujos, protocolos, estados, interfaces, dependencias, límites de confianza y diagramas específicos.
4. **Estándares y metodologías:** normas, RFC, guías, marcos, versiones, requisitos, diferencias, alcance, conflictos y mapeos sin asumir equivalencias.
5. **Implementación técnica:** algoritmos, código, configuraciones, consultas, reglas, comandos y ejemplos completos revisables estáticamente; indicar requisitos y resultados esperados sin afirmar ejecución.
6. **Análisis avanzado:** casos límite, fallos, condiciones de carrera, compatibilidad, rendimiento teórico, trade-offs, restricciones, causa raíz y contraejemplos.
7. **Perspectiva de seguridad:** amenazas, abuso, prevención, detección, respuesta, recuperación, seguridad residual y límites, adaptados al dominio.
8. **Investigación científica:** estado del arte, estrategia de búsqueda, síntesis crítica, preguntas, hipótesis, diseños, variables, controles, amenazas a validez y agenda futura. Separar protocolo propuesto de resultados observados.
9. **Laboratorios y datasets:** diseño completo de entornos, corpus/datasets, procedencia, licencia, esquema, particiones, ground truth, baseline, scripts, hashes y resultados esperados. Marcar ejecución como pendiente hasta que exista.
10. **Evaluación y benchmarks:** rúbricas, métricas, baselines, casos, umbrales propuestos, incertidumbre, falsos positivos/negativos y protocolo de evaluación. No inventar puntuaciones.
11. **Conocimiento operativo y Skills:** especificaciones de procedimiento, precondiciones, permisos, entradas/salidas, validaciones, parada, rollback y riesgos; las Skills permanecen en estado draft/no promovidas hasta pruebas.
12. **Trazabilidad y mantenimiento:** fuentes por afirmación, autoría, edición, fecha, licencia, hash cuando exista, revisión, versión, obsolescencia, dependencias y changelog.

No se acepta reemplazar una capa por un encabezado o texto genérico. Cada contenido debe ser disciplinar, específico al tema y útil para reconstruir el mecanismo.

## 5. Criterios de cierre teórico por tema

Un tema solo puede declararse **teóricamente completo** cuando:
- Su mapa de alcance incluye los subtemas esenciales y dependencias, no solo los siete títulos iniciales.
- Las doce capas contienen contenido específico o una justificación sólida de no aplicabilidad.
- Los mecanismos pueden reconstruirse desde la explicación, los modelos y los diagramas.
- Los estándares y versiones se contrastan con fuentes primarias.
- Los ejemplos están resueltos paso a paso y tienen contraejemplos/casos límite.
- Los procedimientos especifican precondiciones, pasos, resultados esperados, verificación, limpieza y rollback.
- Las afirmaciones importantes tienen fuente y estado epistemológico: hecho, inferencia, hipótesis o recomendación.
- Las fuentes relevantes se han leído en el alcance declarado; los resúmenes no se presentan como lectura integral.
- Hay evaluación conceptual y problemas avanzados con respuestas razonadas y rúbrica.
- Las brechas restantes, incertidumbres y aspectos que requieren ejecución están declarados.
- Un revisor con competencia disciplinar puede seguir la argumentación y cuestionar sus fuentes.

La aprobación teórica no exige que el usuario ejecute CYBER_AI ni que cada laboratorio haya sido corrido. Sí exige que el diseño de laboratorio, datasets, métricas y Skills esté desarrollado y que su estado pendiente sea explícito.

## 6. Protocolo secuencial obligatorio por especialidad

Para cada módulo, sin avanzar al siguiente hasta cerrar la revisión teórica del actual:

1. **Reconstrucción independiente:** elaborar el mapa disciplinar desde fuentes y conocimiento técnico externo a la estructura existente.
2. **Inventario curricular:** descomponer el dominio en temas y subtemas esenciales, incluyendo dependencias y áreas emergentes.
3. **Contraste:** comparar tema por tema con los archivos actuales; clasificar completo, parcial, ausente, obsoleto, contradictorio o duplicado.
4. **Investigación de brechas:** localizar fuentes primarias y literatura técnica/científica; registrar estrategia, fecha, versión y estado real de lectura.
5. **Desarrollo:** completar únicamente las carencias verificadas, sin duplicar contenido válido, aplicando las doce capas.
6. **Evaluación en frío:** ejercicios fundamentales, técnicos y avanzados; problemas resueltos, escenarios, preguntas de diagnóstico y rúbricas.
7. **Auditoría adversarial documental:** buscar errores, afirmaciones sin soporte, contradicciones, generalizaciones, omisiones y contenido genérico.
8. **Corrección y repetición:** corregir hallazgos y repetir la auditoría hasta satisfacer todos los criterios teóricos.
9. **Registro:** actualizar la matriz, fuentes, changelog y tracker con evidencia; no promover puertas operativas por documentación.
10. **Salida del módulo:** publicar T-level sustentado, O-level real, brechas pendientes y decisión de avanzar o bloquear.

## 7. Evaluación en frío obligatoria

Cada módulo debe incluir, según su naturaleza:
- Prueba de comprensión de conceptos y terminología.
- Resolución razonada de problemas.
- Análisis de arquitectura, protocolos o artefactos.
- Diagnóstico de escenarios y casos límite.
- Comparación crítica de estándares y tecnologías.
- Diseño de una solución con supuestos y trade-offs.
- Revisión de código/configuración por análisis estático cuando aplique.
- Detección de afirmaciones falsas o evidencia insuficiente.
- Preguntas de transferencia a escenarios no vistos.
- Rúbrica y respuestas justificadas.

No confundir el cuestionario escrito con una evaluación administrada a personas. Hasta que se aplique, su estado es instrumento diseñado.

## 8. Secuencia de módulos

La secuencia se toma del inventario de la auditoría granular, empezando por `ai_red_team` como primer módulo de trabajo actual. El orden completo y los identificadores se conservan en `DOMAIN_LAYER_AUDIT_48.json`; no crear un segundo catálogo divergente.

El módulo `ai_red_team` ya cuenta con un informe inicial de brechas en `knowledge/research/domain_investigations/AI_RED_TEAM_GAP_RESEARCH_2026-11-19.md`. Ese informe es una base de investigación, no cierre: su propia conclusión identifica los siete temas con desarrollo insuficiente, fuentes pendientes de lectura integral y protocolo experimental aún no ejecutado. El trabajo actual debe contrastar el informe con el compendio y desarrollar el módulo, no limitarse a repetir el informe.

## 9. Estados y reglas de honestidad

Estados teóricos por tema: `not_assessed`, `in_progress`, `blocked`, `theory_complete_pending_review`, `theory_reviewed`.

Estados operativos por tema: `not_started`, `designed_not_executed`, `executed_local`, `integrated`, `independently_reproduced`.

Reglas:
- No marcar teoría completa por volumen, estructura o existencia de archivos.
- No marcar fuente leída por encontrar su URL, abstract o metadatos.
- No convertir resultados esperados en resultados observados.
- No presentar código estático como integración funcional.
- No promover Skills candidatas a aprobadas sin validación.
- No asignar T4/T5 sin revisión disciplinar independiente.
- No asignar O2–O5 sin evidencia de ejecución.
- Mantener las brechas visibles; un módulo puede ser T4/O0 y seguir pendiente de operación.

## 10. Primera tarea activa

**Módulo:** `ai_red_team`.  
**Objetivo inmediato:** auditar sus siete temas y ampliar el currículo donde falten subtemas; reemplazar las secciones genéricas repetidas por desarrollos específicos; completar las doce capas de cada tema; revisar integralmente fuentes prioritarias; añadir ejercicios resueltos, contraejemplos, rúbricas y especificaciones de laboratorios/benchmarks.  
**Condición de salida:** todos los temas esenciales con doce capas justificadas y revisión documental adversarial sin hallazgos críticos abiertos. La revisión independiente externa puede seguir pendiente y debe bloquear T4, pero no impide completar el borrador teórico.  
**Siguiente módulo:** solo después de registrar el cierre teórico de `ai_red_team`.

## 11. Relación con la etapa caliente

Tras completar la etapa fría de las 48 especialidades, se planifica la etapa caliente de forma separada: ejecución de laboratorios, integración de herramientas, benchmarks, pruebas de carga/fallo, operación controlada, reproducibilidad y revisión externa de resultados. Los protocolos se preparan ahora, pero no se inventan resultados ni se exige ejecución para cerrar la primera etapa teórica.
