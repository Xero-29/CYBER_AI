# Autoconocimiento e investigación metacognitiva

## Estado de implementación

Este subsistema añade un controlador que hace explícita la secuencia:

1. La IA principal evalúa si tiene conocimiento suficiente para la tarea.
2. Si no lo tiene, identifica brechas, incertidumbres y prerrequisitos.
3. El controlador delega la investigación a un agente separado y configurable.
4. VERITAS revisa el informe de forma independiente.
5. Solo los informes aprobados se registran como conocimiento **conocido/provisional**.
6. La IA principal vuelve a evaluar sus brechas.
7. Aunque la investigación sea aprobada, el dominio no se marca como adquirido hasta superar evaluaciones de comprensión y aplicación; la ejecución de la tarea original sigue pendiente.

## Componentes

- `metacognition.py`: ciclo de diagnóstico, delegación, verificación y reevaluación.
- `researcher_agent.py`: contrato neutral del backend; permite sustituir el proveedor sin cambiar el controlador.
- `data/metacognition/competency_map.json`: mapa persistente de competencias y estados.
- `data/metacognition/research_log.jsonl`: historial auditable de solicitudes, informes y verificaciones.
- `INVESTIGADOR`: rol pequeño separado en `config/model_roles.json`.

## Acceso a la biblioteca y artefactos de investigación

- DIRECTOR activa este ciclo por defecto cuando `metacognition.enabled=true`; puede omitirse explícitamente con `--no-metacognition`.
- La evaluación principal y la tarea posterior reciben recuperación de conocimiento mediante `agent_runner.py --knowledge`.
- `knowledge_bootstrap.py` indexa los paquetes base y los documentos Markdown de `knowledge/deep_modules/<area>/`: README, agendas, revisiones y compendios. El índice conserva IDs de documento estables por ruta y SHA-256.
- La carpeta `knowledge/evaluation/` se mantiene fuera de la recuperación operativa para evitar contaminar respuestas con consultas/etiquetas de evaluación.
- INVESTIGADOR recibe evidencia web curada por `web_research.py`; las páginas se filtran mediante `config/trusted_sources.json` y pasan por revisión antes de llegar al investigador.
- Un informe aprobado se guarda como Markdown en `knowledge/research_generated/` y se indexa como `research_provisional`.
- Un informe con similitud semántica muy alta respecto a conocimiento existente se guarda en `knowledge/research_candidates/` y no se indexa automáticamente: requiere fusión/revisión para evitar duplicados o pérdida de información nueva.
- Un SHA-256 idéntico ya presente en la biblioteca no se vuelve a insertar. La deduplicación semántica usa un umbral conservador (0.965); es un detector de candidatos, no una prueba de equivalencia.
- Los artefactos generados se crean localmente. Para compartirlos en Git, deben revisarse y añadirse/confirmarse explícitamente; no se hace push automático.

Comandos:

```bash
python knowledge_bootstrap.py --dry-run
python knowledge_bootstrap.py
python director.py "Resuelve esta tarea y detecta qué conocimiento falta"
```

## Estados de conocimiento

- `unknown`: no hay evidencia suficiente para evaluar el tema.
- `insufficient`: la tarea supera el conocimiento demostrado o hay brechas críticas.
- `known`: existe contenido revisado independientemente, todavía sin dominio demostrado.
- `mastered`: reservado para una evaluación práctica y teórica independiente; este ciclo nunca lo asigna.

## Intercambio de modelo

El contrato `ModelBackend(name, model, generate)` acepta cualquier función que implemente generación de texto. La lógica de investigación no depende de Ollama, OpenAI, Anthropic, Gemini ni de un modelo concreto. La configuración de CYBER_AI selecciona el rol y el proveedor.

## Límites explícitos

- La confianza declarada por el modelo no se trata como probabilidad calibrada ni como prueba.
- La verificación de VERITAS sigue siendo una revisión basada en modelo; no sustituye comprobaciones externas de URLs, DOI, publicaciones ni experimentos.
- El informe aprobado se intenta indexar en la biblioteca como categoría `research_provisional`, con etiquetas de provisionalidad. Si ECO o la base no están disponibles, se conserva en el registro y se entrega directamente al principal para la reevaluación; el mapa indica `library_indexed=false`.
- El ciclo se limita a dos rondas por defecto para evitar bucles y costes sin control.
- La adquisición de fuentes usa `web_research.py`, que consulta dominios de `config/trusted_sources.json`, y `review_web_report.py`, que aplica revisión por NEXO, FILTRO y VERITAS. Si la búsqueda no devuelve páginas registradas consultables, el sistema registra la limitación y no simula investigación.
- El informe aceptado se intenta indexar mediante ECO y `knowledge_library.store_chunks` como `research_provisional`. Si la indexación falla, DIRECTOR bloquea la ejecución original para no perder el contexto aprendido.

## Pruebas

Ejecutar:

```bash
python3 -m unittest tests.test_metacognition -v
python3 -m py_compile metacognition.py researcher_agent.py
```

El flujo completo con modelos reales debe probarse después en el equipo de ejecución, verificando los modelos configurados, la conectividad del proveedor y el acceso a las fuentes.
