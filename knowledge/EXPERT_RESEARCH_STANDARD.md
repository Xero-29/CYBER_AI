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

## 4. Escala de madurez del conocimiento

| Nivel | Significado | Evidencia mínima |
|---|---|---|
| K1 — Fundamental | Vocabulario y fundamentos correctos | Fuentes identificadas, conceptos contrastados, alcance y límites |
| K2 — Técnico | Mecanismos e implementación | Ejemplos completos, configuraciones/código, pruebas de comprensión |
| K3 — Avanzado | Diagnóstico y aplicación compleja | Casos límite, análisis de fallos, laboratorios ejecutados y evaluación práctica |
| K4 — Experto | Dominio técnico demostrado | Revisión experta independiente, benchmarks pertinentes, trade-offs y resultados reproducibles |
| K5 — Investigación | Conocimiento nuevo o síntesis científica rigurosa | Estado del arte, método explícito, datos/resultados trazables, análisis crítico y reproducción independiente |

La madurez se asigna **por tema**, no por promedio ni por especialidad completa. Se puede usar un estado mixto, por ejemplo: K2 con laboratorios pendientes. No elevar un tema por tener muchas páginas.

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
- **Desarrollada:** contenido técnico real en sus temas prioritarios.
- **Validada:** fuentes y pruebas revisadas, con brechas explícitas.
- **Experta (K4):** los temas esenciales cumplen las evidencias K4 y las puertas aplicables.
- **Investigación (K5):** existe investigación con método y evidencia reproducible.

El estado global debe mostrar distribución por tema y puertas pendientes. Nunca resumir el estado como “completo” si hay brechas críticas o validaciones no ejecutadas.
