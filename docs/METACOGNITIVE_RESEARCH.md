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
- La investigación autónoma requiere herramientas de búsqueda y acceso a fuentes habilitadas; el agente no debe afirmar que consultó fuentes si no tuvo acceso a ellas.

## Pruebas

Ejecutar:

```bash
python3 -m unittest tests.test_metacognition -v
python3 -m py_compile metacognition.py researcher_agent.py
```

El flujo completo con modelos reales debe probarse después en el equipo de ejecución, verificando los modelos configurados, la conectividad del proveedor y el acceso a las fuentes.
