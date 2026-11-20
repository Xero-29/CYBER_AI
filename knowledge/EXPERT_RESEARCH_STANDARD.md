# Estándar de conocimiento experto e investigación CYBER_AI

**Estado:** estándar normativo de diseño. No certifica por sí mismo que las especialidades estén completas.  
**Aplicación:** obligatorio para las 48 especialidades del catálogo.  
**Principio:** una especialidad se desarrolla por temas y evidencias; no se considera experta por volumen de texto, cantidad de archivos o referencias catalogadas.

## 1. Modelo de conocimiento por especialidad

Cada especialidad mantiene un perfil disciplinar propio y desarrolla sus temas con estas doce capas. Las capas se adaptan: no se fuerza matemática irrelevante, explotación innecesaria ni experimentos que no sean seguros o científicamente útiles.

1. **Fundamentos teóricos:** terminología precisa, definiciones, principios, taxonomías, supuestos y límites.
2. **Fundamentos matemáticos y formales:** lógica, probabilidad, estadística, teoría de la información, grafos, álgebra, modelos de estados, complejidad o métodos numéricos cuando sean pertinentes. Explicar por qué una herramienta formal aplica; declarar cuando no aplica.
3. **Arquitectura y funcionamiento interno:** componentes, flujos, protocolos, interfaces, estados, dependencias, límites de confianza y superficies de fallo.
4. **Estándares y metodologías:** fuentes normativas, versiones, alcance, requisitos, criterios de selección, diferencias entre marcos y mapeos sin asumir equivalencia.
5. **Implementación técnica:** código, configuración, algoritmos, consultas, reglas, diagramas, herramientas, instrucciones reproducibles y resultados esperados.
6. **Análisis avanzado:** casos límite, fallos, condiciones de carrera, degradación, compatibilidad, rendimiento, restricciones, trade-offs y análisis de causa raíz.
7. **Perspectiva de seguridad:** amenazas, abuso, prevención, detección, respuesta, recuperación y validación. En áreas no ofensivas, adaptar la perspectiva a su objeto y no inventar escenarios de ataque.
8. **Investigación científica:** estado del arte, pregunta, brecha, hipótesis falsable, protocolo, variables, controles, análisis, amenazas a validez y agenda futura.
9. **Laboratorios y datasets:** entornos aislados/autorizados, datos sintéticos o con licencia, procedencia, esquema, particiones, baseline, scripts, hashes y resultados. Diferenciar diseño de ejecución.
10. **Evaluación y benchmarks:** objetivos, cobertura, métricas justificadas, datasets, baselines, umbrales, incertidumbre, falsos positivos/negativos y criterios de aprobación.
11. **Conocimiento operativo:** Skills versionadas, precondiciones, permisos, entradas/salidas, límites, validaciones, rollback, evidencias y casos de no aplicación.
12. **Trazabilidad y mantenimiento:** fuentes, autoría, versión, fecha, licencia, hashes, historial, revisión, obsolescencia, dependencias y cambios.

## 2. Plantilla obligatoria por tema

Cada tema del currículo debe tener una unidad identificable y los siguientes apartados, incluso cuando un apartado se marque justificadamente como no aplicable:

- Objetivo, alcance, prerrequisitos y vocabulario.
- Explicación técnica original con profundidad suficiente para reconstruir el mecanismo.
- Modelo conceptual/formal y supuestos.
- Arquitectura, flujo y diagrama pertinente.
- Variantes, implementaciones y compatibilidad.
- Amenazas, modos de fallo y límites.
- Controles o mitigaciones y su riesgo residual.
- Procedimiento reproducible con precondiciones, pasos, expected output, verificación, limpieza y rollback.
- Ejemplos completos y contraejemplos.
- Preguntas abiertas, literatura y evidencia.
- Evaluación conceptual y práctica con respuestas/rúbrica.
- Fuentes primarias versionadas y estado real de revisión.

No usar texto de relleno ni copiar la misma explicación entre dominios. Una referencia enlazada no significa que el documento se haya leído; una prueba diseñada no significa que se haya ejecutado.

## 3. Investigación reproducible

Todo trabajo que se presente como investigación debe registrar:

1. Problema y motivación.
2. Pregunta de investigación acotada.
3. Estado del arte y estrategia de búsqueda (bases, consultas, fecha, inclusión/exclusión).
4. Brecha respecto de trabajos existentes.
5. Hipótesis nula y alternativa, o pregunta exploratoria justificada.
6. Diseño: población/unidad de análisis, muestra, variables, controles, comparadores y amenazas.
7. Protocolo, entorno, herramientas y versiones.
8. Dataset: procedencia, licencia, esquema, limpieza, sesgos, particiones y hashes.
9. Resultados brutos y procesados, scripts y trazabilidad.
10. Análisis adecuado: incertidumbre, intervalos, pruebas estadísticas cuando procedan, tamaños de efecto y limitaciones.
11. Reproducción independiente o estado explícito de reproducción pendiente.
12. Conclusión proporcional a la evidencia, resultados negativos y trabajo futuro.

No inventar resultados, métricas, muestras, revisiones por pares ni reproducibilidad. Las hipótesis no son conclusiones.

## 4. Escala de madurez: teoría y operación por separado

La madurez se registra por tema en dos ejes independientes. La antigua escala única K1–K5 mezclaba conocimiento con ejecución y queda sustituida por T (teoría) y O (operación).

### 4.1 Madurez teórica (T)

| Nivel | Significado | Evidencia mínima |
|---|---|---|
| T0 — No evaluada | Sin evidencia suficiente para juzgar el tema | Estado y brechas declarados |
| T1 — Fundamental | Conceptos, terminología, alcance, fuentes y límites correctos | Fuentes identificadas y contrastadas; vocabulario y supuestos precisos |
| T2 — Técnica | Mecanismos, arquitectura, estándares, variantes y procedimientos diseñados | Explicación reconstruible, diagramas, ejemplos completos y análisis estático |
| T3 — Avanzada | Casos límite, fallos, trade-offs, modelos pertinentes, ejercicios resueltos y síntesis crítica | Evidencia trazable, comparaciones, contraejemplos, evaluación en frío y revisión documental |
| T4 — Experta teórica | Dominio disciplinar defendible y revisión independiente por especialista | Fuentes primarias revisadas en profundidad, cobertura esencial, razonamiento avanzado, afirmaciones trazables y cierre de hallazgos |
| T5 — Investigación teórica | Contribución original o síntesis científica de alto rigor | Método explícito, argumentación/proposición formal o análisis conceptual novedoso, límites demostrados y revisión independiente; si requiere datos empíricos, ejecutar y analizar el estudio |

T4/T5 describen conocimiento y razonamiento teórico; no implican que herramientas o laboratorios hayan sido ejecutados. No asignar T4 sin revisión disciplinar independiente.

### 4.2 Madurez operativa (O)

| Nivel | Significado | Evidencia mínima |
|---|---|---|
| O0 — No ejecutada | No hay ejecución acreditada | Estado explícito |
| O1 — Diseño | Prueba/laboratorio especificado | Alcance, entorno, datos, controles, resultados esperados y parada |
| O2 — Laboratorio | Ejecución controlada | Logs, datos, versiones, resultados observados y limpieza |
| O3 — Integración | Interoperabilidad verificada | Integraciones reales, pruebas de contrato y fallos |
| O4 — Operación representativa | Rendimiento, recuperación y operación evaluados | Carga, resiliencia, rollback, observabilidad y riesgos residuales |
| O5 — Reproducción independiente | Réplica externa y validación de desempeño | Segundo entorno/operador, método y resultados comparables |

No asignar O2–O5 sin evidencia de ejecución correspondiente. Una configuración escrita, un script no ejecutado o un resultado esperado no constituyen ejecución.

Ejemplo: **T4/O0** significa conocimiento teórico experto revisado, todavía sin validación operativa. No promediar T y O ni convertir uno en el otro. La madurez editorial M2/M3 es un estado de desarrollo del artefacto y no sustituye T u O.

## 5. Ocho puertas de calidad

- **G1 Cobertura:** mapa de alcance, dependencias y brechas; temas esenciales identificados.
- **G2 Fuentes:** procedencia, autoridad, versión, fecha, licencia y estado de lectura.
- **G3 Profundidad:** mecanismos, supuestos, límites, variantes y errores explicados.
- **G4 Aplicación:** implementación y procedimientos completos, seguros y verificables.
- **G5 Experimentación:** laboratorio ejecutado, datos, baseline, controles y resultados.
- **G6 Evaluación:** pruebas conceptuales/prácticas y métricas pertinentes.
- **G7 Reproducibilidad:** scripts, entorno, versiones, hashes y posibilidad de réplica.
- **G8 Revisión independiente:** revisión técnica/científica, correcciones y registro de desacuerdos.

Cada puerta admite: `not_started`, `in_progress`, `passed`, `blocked` o `not_applicable` con justificación. Una puerta pendiente no se interpreta como aprobada.

## 6. Evidencia, fuentes y confianza

Toda afirmación relevante debe distinguirse como:
- **Hecho respaldado:** fuente identificable y pertinente.
- **Resultado observado:** evidencia experimental adjunta.
- **Inferencia:** razonamiento derivado, con premisas visibles.
- **Hipótesis:** proposición pendiente de prueba.
- **Recomendación:** decisión contextual con criterios y trade-offs.

El registro de fuentes debe incluir identificador estable, título, autor/editor, URL canónica, tipo, versión/edición, fecha de publicación/consulta, licencia, SHA-256 del artefacto archivado cuando exista, estado de lectura y temas respaldados. Estados recomendados: `discovered`, `metadata_reviewed`, `abstract_reviewed`, `full_text_reviewed`, `experimentally_used`, `superseded`. No marcar `full_text_reviewed` sin leer el texto completo.

## 7. Laboratorios, datasets y seguridad

- Usar sistemas propios, deliberadamente vulnerables o expresamente autorizados.
- Preferir datos sintéticos; documentar licencia y restricciones de uso de datasets externos.
- Aislar red, identidades, secretos y recursos; aplicar mínimos privilegios y límites.
- Definir alcance, precondiciones, pasos, resultados esperados, criterios de parada, limpieza y rollback.
- Preservar evidencia saneada; no almacenar credenciales ni datos personales innecesarios.
- En OT, automoción, telecom, satélite y hardware, priorizar simulación, emulación y bancos aislados; no realizar pruebas disruptivas en sistemas productivos.
- Los escenarios ofensivos son exclusivamente para análisis autorizado y validación defensiva; no ampliar el alcance por inferencia.

## 8. Skills y memoria operativa

Una Skill solo se promueve a reutilizable tras revisión y validación. Debe contener: identificador, versión, propósito, dominio, precondiciones, permisos, entradas/esquema, pasos, herramientas, salida esperada, validaciones, riesgos, parada, rollback, evidencia, pruebas, historial y responsable de aprobación. Una ejecución fallida se conserva como aprendizaje negativo saneado; no se convierte en procedimiento exitoso. La memoria distingue contexto, resultado observado y generalización.

## 9. Estructura lógica de archivos

La estructura física puede variar por dominio, pero el índice debe poder representar:

```text
specialty/
  README.md                       # alcance, mapa, estado y dependencias
  profile.yaml                    # perfil disciplinar, niveles y puertas
  topics/<topic_id>/
    theory.md
    formal_models.md              # si aplica
    architecture.md
    standards_methods.md
    implementation/
    advanced_analysis.md
    security_analysis.md          # adaptado al dominio
    research/
      literature_review.md
      research_questions.md
      hypotheses.md
      experimental_design.md
    laboratories/<lab_id>/
      protocol.md
      environment/
      data/
      results/
    datasets/<dataset_id>/
      metadata.json
    evaluation/
      rubric.yaml
      tests/
      benchmarks/
    skills/<skill_id>/
      SKILL.md
      tests/
  references/
    source_registry.json
  CHANGELOG.md
```

No crear archivos vacíos para simular cobertura. Mantener los documentos existentes si son válidos y migrar su contenido sin pérdida.

## 10. Regla de publicación

Una especialidad solo puede declararse:
- **Estructurada:** perfil y mapa de temas definidos.
- **Desarrollada teóricamente:** los temas esenciales tienen las doce capas específicas o justificadamente no aplicables, fuentes revisadas en el alcance declarado, ejemplos y evaluación en frío; la ejecución puede seguir en O0/O1.
- **Teóricamente experta (T4):** los temas esenciales cumplen evidencias T4 y revisión disciplinar independiente.
- **Investigación teórica (T5):** existe contribución original o síntesis científica rigurosa, método explícito, límites y revisión independiente; los resultados empíricos requieren experimentación real.
- **Operativamente validada (O2–O5):** solo cuando existen pruebas ejecutadas e integraciones/reproducciones acreditadas según el nivel.

El estado global debe mostrar distribución por tema en ambos ejes T/O y puertas pendientes. Nunca resumir el estado como “completo” si hay brechas críticas o validaciones no ejecutadas. El cierre teórico no certifica operación.

## 11. Separación obligatoria entre madurez teórica y operativa

La biblioteca se construye en dos etapas. La primera cierra el conocimiento teórico (capacidades en frío) de todas las especialidades; la segunda desarrolla y valida la ejecución (capacidades en caliente). No mezclar los dos resultados en una sola etiqueta.

- **Madurez teórica T0–T5:** mide cobertura disciplinar, precisión, profundidad, trazabilidad, razonamiento, síntesis crítica y revisión experta del conocimiento. T4 exige revisión independiente por especialista. T5 exige contribución o síntesis de investigación de alto rigor; si la contribución depende de datos experimentales, estos deben existir y analizarse.
- **Madurez operativa O0–O5:** O0 no ejecutada; O1 diseño especificado; O2 laboratorio ejecutado con evidencia; O3 integración/interoperabilidad verificada; O4 operación representativa y recuperación evaluadas; O5 reproducción independiente y validación externa del desempeño.

Un tema puede ser T4/O0: conocimiento teórico experto revisado, aún sin validación operativa. Esto no autoriza a afirmar que las herramientas funcionan en producción. Tampoco se puede asignar T4 solo por contenido escrito: exige fuentes primarias revisadas, cobertura disciplinar, afirmaciones trazables, análisis avanzado y revisión independiente.

### Interpretación de las doce capas en la etapa teórica

Las doce capas se desarrollan desde la primera etapa. En implementación se documentan algoritmos, código, configuraciones y ejemplos revisables estáticamente; en laboratorios/datasets se diseña el protocolo, corpus, ground truth y resultados esperados; en evaluación se definen rúbricas, métricas y benchmarks; en Skills se redactan especificaciones no promovidas. No se presentan estos artefactos como ejecución, medición o validación operativa.

### Criterio de salida de la etapa fría

Una especialidad puede declararse **teóricamente completa pendiente de revisión independiente** cuando sus temas esenciales tienen las doce capas desarrolladas o justificadas, mapa disciplinar ampliado, fuentes revisadas en el alcance declarado, ejemplos y contraejemplos resueltos, ejercicios con rúbrica, procedimientos detallados y brechas explícitas. Solo tras revisión independiente puede alcanzar T4. Las puertas G5/G7 y la madurez O no se aprueban por completar documentación.

El procedimiento de aplicación a las 48 especialidades está en [THEORETICAL_LIBRARY_COMPLETION_PROGRAM_48.md](THEORETICAL_LIBRARY_COMPLETION_PROGRAM_48.md).
