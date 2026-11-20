# Protocolo de ejecución y aceptación del conocimiento en frío — CYBER_AI

**Estado:** obligatorio para las 48 especialidades.
**Etapa:** conocimiento en frío; no certifica ejecución en caliente.
**Orden:** Foundations → AI Red Team → las otras 46 especialidades, una por una.
**Normas relacionadas:** `knowledge/EXPERT_RESEARCH_STANDARD.md` y `knowledge/THEORETICAL_LIBRARY_COMPLETION_PROGRAM_48.md`.

## 1. Regla de aceptación

Una especialidad no se aprueba por número de archivos, palabras, referencias, encabezados, temas iniciales ni por declarar cubiertas sus doce capas. Se aprueba únicamente cuando existe evidencia específica y revisable de que el conocimiento permite:

1. **Enseñar:** construir una progresión didáctica desde prerrequisitos hasta conceptos avanzados, detectar concepciones erróneas y comprobar aprendizaje.
2. **Explicar:** reconstruir mecanismos, modelos, arquitectura, algoritmos, protocolos y causalidad con precisión suficiente para que otro especialista pueda seguir el razonamiento.
3. **Analizar:** resolver escenarios no triviales, identificar supuestos, límites, fallos, incertidumbre, interacciones y trade-offs; justificar conclusiones y distinguir hechos, inferencias e hipótesis.
4. **Diseñar:** producir soluciones completas y contextualizadas, con requisitos, arquitectura, alternativas, controles, decisiones, riesgos residuales, verificación y criterios de aceptación.

Las cuatro capacidades son obligatorias. Un tema que solo describe conceptos o enumera herramientas no demuestra dominio.

## 2. Secuencia de ejecución invariable

### Paso 0 — Congelar y comprobar la línea base
- Registrar rama, commit base, estado del PR y que `main` permanece intacta.
- Leer el estándar, el programa, el catálogo, la matriz JSON/Markdown, el dossier del módulo y el registro de fuentes.
- No sobrescribir contenido útil: primero mapearlo y conservarlo; después corregir o ampliar.
- Registrar archivos, afirmaciones, fuentes, pruebas y brechas existentes. No inferir cobertura por existencia del archivo.

### Paso 1 — Definir el perfil disciplinar
Para la especialidad actual, especificar objeto de estudio, alcance, exclusiones, vocabulario, problemas que resuelve, responsabilidades, dependencias con otras especialidades, prerrequisitos y competencias terminales. Distinguir lo transversal de lo propio del dominio.

### Paso 2 — Completar el mapa curricular (G1)
- Partir de los temas de línea base, sin tratarlos como lista exhaustiva.
- Descomponer cada tema en subtemas, mecanismos, familias tecnológicas, variantes, contextos, casos de uso y problemas de frontera.
- Incluir fundamentos históricos cuando expliquen decisiones actuales, así como tecnologías vigentes y emergentes con su grado de madurez.
- Construir un grafo de dependencias y detectar duplicaciones, vacíos y solapamientos.
- Justificar inclusiones, exclusiones y elementos no aplicables. No ocultar una brecha dentro de un tema demasiado amplio.
- Versionar el currículo y vincular cada unidad a sus doce capas y a las cuatro capacidades.

**Salida:** perfil disciplinar, taxonomía jerárquica, mapa de dependencias, matriz de cobertura y registro de exclusiones justificadas.

### Paso 3 — Investigar y revisar fuentes (G2)
- Definir preguntas de búsqueda, fuentes primarias, repositorios académicos, estándares, RFC, especificaciones y documentación oficial.
- Registrar autor/editor, título, edición/versión, fecha, URL canónica, licencia, fecha de consulta, alcance leído y temas respaldados.
- Leer integralmente las fuentes críticas cuando el texto esté disponible. Abstract, metadatos, resumen de terceros o referencia bibliográfica no equivalen a lectura integral.
- Comparar fuentes que discrepen; identificar obsolescencia, erratas, límites de aplicabilidad y conflictos de versiones.
- Vincular afirmaciones técnicas importantes a evidencia concreta. Separar requisito normativo, recomendación, observación, inferencia e hipótesis.
- Registrar fuentes inaccesibles y qué afirmaciones no pueden sostenerse todavía; no inventar citas ni estados de lectura.

**Salida:** revisión crítica de literatura/estándares, registro de fuentes y mapa afirmación→fuente→alcance de lectura.

### Paso 4 — Desarrollar cada unidad y sus doce capas (G3/G4)
Para cada tema y subtema, desarrollar contenido propio y específico:
1. Fundamentos teóricos.
2. Modelos matemáticos/formales pertinentes, con derivaciones y supuestos; justificar no aplicabilidad cuando proceda.
3. Arquitectura y funcionamiento interno, con diagramas y flujos específicos.
4. Estándares y metodologías, versiones, alcance, diferencias y límites.
5. Implementación técnica, algoritmos, pseudocódigo/código/configuración y ejemplos revisables estáticamente.
6. Análisis avanzado: variantes, casos límite, fallos, causa raíz, rendimiento, compatibilidad y trade-offs.
7. Seguridad: amenazas, controles, detección, respuesta y riesgo residual, adaptados al dominio.
8. Investigación: estado del arte, preguntas, brechas, hipótesis y método; no presentar diseños como resultados.
9. Laboratorios/datasets: protocolo, entorno, datos, licencia, esquema, ground truth, particiones, baseline, hashes y resultados esperados; marcar ejecución pendiente.
10. Evaluación: objetivos, rúbricas, métricas, baselines, umbrales propuestos, incertidumbre y falsos positivos/negativos.
11. Skills en borrador: precondiciones, permisos, entradas/salidas, pasos, validaciones, límites, parada y rollback; no promover sin validación.
12. Trazabilidad y mantenimiento: procedencia, versiones, dependencias, responsables, revisión y obsolescencia.

No todas las disciplinas necesitan la misma matemática o el mismo tipo de laboratorio. La adaptación debe justificarse técnicamente; no se permite rellenar con texto genérico ni copiar una capa de otro tema.

### Paso 5 — Probar las cuatro capacidades en frío (G6)
Cada tema esencial debe incluir como mínimo:

**A. Prueba de enseñanza**
- Explicación progresiva para un lector con prerrequisitos declarados.
- Objetivos observables y mapa conceptual.
- Dos o más errores conceptuales frecuentes, por qué son incorrectos y cómo corregirlos.
- Ejercicios graduados y soluciones razonadas.

**B. Prueba de explicación**
- Reconstrucción del mecanismo paso a paso.
- Ejemplo completo y contraejemplo.
- Diagrama, formalismo o traza cuando aporte claridad.
- Identificación de supuestos, condiciones previas y límites.

**C. Prueba de análisis**
- Al menos un escenario nuevo no copiado del texto.
- Análisis de caso límite o fallo.
- Comparación de al menos dos alternativas cuando existan.
- Justificación de decisión, incertidumbre, riesgos residuales y condiciones que cambiarían la conclusión.

**D. Prueba de diseño**
- Enunciado de requisitos y restricciones.
- Arquitectura/solución propuesta y justificación.
- Alternativas descartadas y motivos.
- Plan de implementación conceptual, controles, verificación, aceptación, observabilidad, recuperación/rollback y riesgos residuales.
- Revisión de coherencia, seguridad y dependencias.

Las respuestas deben ser completas y explicadas, no solo una clave de respuestas. El banco de evaluación debe incluir preguntas nuevas o variantes para evitar que memorizar el dossier sea suficiente.

### Paso 6 — Evaluación experta estática y corrección iterativa
- Aplicar rúbrica por tema y por capacidad.
- Revisar exactitud técnica, profundidad, coherencia, cobertura, trazabilidad y utilidad para resolver problemas.
- Buscar contradicciones, generalizaciones no sustentadas, pasos omitidos, supuestos ocultos, código conceptualmente incorrecto y métricas mal definidas.
- Realizar revisión cruzada entre temas y especialidades dependientes.
- Registrar cada no conformidad con severidad, evidencia, causa, corrección, prueba de cierre y estado.
- Corregir y repetir la evaluación hasta que no queden fallos críticos ni mayores abiertos.

No se puede convertir automáticamente una autoevaluación del autor en revisión independiente. La madurez T4 requiere revisión por especialista independiente conforme al estándar.

### Paso 7 — Cerrar puertas y registrar madurez
- G1: mapa curricular exhaustivo y brechas/exclusiones justificadas.
- G2: fuentes suficientes, pertinentes, versionadas y revisadas en el alcance declarado.
- G3: mecanismos, modelos, supuestos, límites y análisis demostrados.
- G4: soluciones y procedimientos conceptuales completos, seguros y verificables.
- G5: experimentación real; se difiere a la etapa caliente si no se ejecuta. Nunca simular aprobación.
- G6: evaluación en frío administrada y corregida con rúbrica y evidencias.
- G7: reproducibilidad de experimentos; se difiere cuando dependa de ejecución. La reproducibilidad documental/estática se registra separadamente.
- G8: revisión independiente; bloqueada hasta disponer de un revisor cualificado.

Una especialidad puede alcanzar cierre documental de etapa fría con G5/G7 operativas pendientes, pero no puede etiquetarse T4 sin G8 independiente. Mantener T y O separados.

### Paso 8 — Actualizar índice, matriz y registro
- Actualizar catálogo, README, índice, perfiles, dependencias, fuentes, evaluaciones y matriz canónica.
- Cada estado debe apuntar a evidencia concreta: archivo, sección, prueba, fuente y no conformidad cerrada.
- No marcar `passed` por inferencia. Si la evidencia no existe o no es accesible, usar `in_progress`, `not_assessed` o `blocked` según corresponda.
- Generar vista legible y comprobar que JSON y Markdown coincidan.
- Ejecutar validadores estáticos y CI disponibles; registrar qué se ejecutó y qué no.

### Paso 9 — Gate de salida y siguiente especialidad
La especialidad solo sale del ciclo cuando:
- el currículo ampliado está justificado;
- todas las unidades esenciales y subtemas están evaluados;
- las doce capas contienen material disciplinar útil o una no aplicabilidad argumentada;
- las cuatro capacidades tienen evidencias aprobadas;
- no hay no conformidades críticas/mayores abiertas;
- las fuentes y afirmaciones son trazables;
- la matriz refleja exactamente la evidencia;
- las limitaciones de revisión independiente y ejecución están declaradas.

Entonces se inicia la siguiente especialidad. No se avanza para ocultar brechas del módulo actual.

## 3. Rúbrica común de evaluación

Puntuar cada dimensión de 0 a 4, con evidencia y justificación:

| Puntuación | Criterio |
|---|---|
| 0 — Ausente | No existe contenido o evidencia evaluable. |
| 1 — Superficial | Enumera términos/recetas; no explica ni justifica. |
| 2 — Funcional | Explica el caso común, pero omite límites, alternativas o escenarios difíciles. |
| 3 — Avanzado | Mecanismo reconstruible, análisis sólido, casos límite, decisiones justificadas y trazabilidad. |
| 4 — Experto defendible | Dominio profundo, síntesis crítica, tratamiento de incertidumbre, contraejemplos, diseño robusto y revisión disciplinar independiente. |

Dimensiones obligatorias: enseñanza, explicación, análisis, diseño, exactitud, profundidad, fuentes/trazabilidad, cobertura curricular y evaluación.

**Umbral interno para cerrar una unidad en etapa fría:** mínimo 3 en cada dimensión, sin ningún 0–2 en una dimensión crítica; el nivel 4 debe estar respaldado para afirmar desempeño experto del contenido. Este umbral no sustituye la revisión independiente exigida para T4.

**Fallos críticos automáticos:** afirmación técnica falsa que pueda inducir una decisión insegura; fuente inventada o mal atribuida; código/procedimiento con riesgo no declarado; confusión entre diseño y ejecución; ausencia de límites relevantes; solución que no satisface sus propios requisitos; fuga de secretos/datos reales en ejemplos; aprobación sin evidencia.

## 4. Registro mínimo por unidad

Cada registro debe contener:
- ID de especialidad, tema y subtema.
- Alcance, prerrequisitos y competencias.
- Evidencias para L1–L12, con enlaces y estado real.
- Evidencias de enseñar, explicar, analizar y diseñar.
- Fuentes y alcance de lectura.
- Evaluación, rúbrica, respuestas y resultados.
- No conformidades, correcciones y retest.
- Madurez T y O por separado.
- Revisión independiente: nombre/rol o pendiente; nunca fingir independencia.
- Limitaciones y próximos pasos.

## 5. Orden maestro

1. Foundations.
2. AI Red Team.
3. Las 46 especialidades restantes, en el orden del catálogo versionado.

La prioridad no permite saltarse pasos internos. Foundations debe completar su mapa curricular ampliado y cerrar las brechas antes de AI Red Team; AI Red Team debe hacer lo mismo antes de pasar a la tercera especialidad. Las 48 se mantienen visibles en el tracker desde el primer día.

## 6. Informe de avance obligatorio

Cada ciclo de trabajo informa:
- qué unidad/subtema se auditó;
- qué contenido se agregó o corrigió;
- qué fuente se revisó y hasta qué profundidad;
- qué pruebas estáticas se aplicaron;
- qué falló y cómo se corrigió;
- qué evidencia quedó enlazada;
- qué estados cambiaron y por qué;
- qué queda pendiente;
- qué no se ejecutó.

No informar porcentajes de “conocimiento completado” a partir de palabras, archivos o encabezados. Los porcentajes solo pueden representar estados de evidencia auditados y deben mostrar denominador, reglas y limitaciones.
