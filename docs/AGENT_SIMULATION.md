# Simulación multiagente sin modelos reales

`workflow_contracts.py` contiene el contrato estructural compartido por `team_orchestrator.py` y `agent_simulation.py`. Ambos validan los mismos modos, etapas, límites, presupuestos de tokens, opciones de recuperación y flags antes de operar. El simulador no se conecta a Ollama ni a proveedores externos y no ejecuta herramientas. También reproduce el límite de contexto del orquestador: descarta etapas antiguas hasta respetar `max_context_chars` y reporta cuántas quedaron fuera.

## Uso

```bash
python agent_simulation.py --workflow investigacion --task "Simular revisión de una aplicación de laboratorio"
```

El informe JSON se guarda por defecto en `reports/agent_simulations/`. Se puede indicar una ruta explícita con `--output`.

## Qué comprueba

- Que el catálogo JSON tenga una estructura válida y una versión compatible.
- Que el identificador del flujo sea seguro y exista en el catálogo.
- Que el flujo tenga pasos y que cada paso tenga agente, objetivo y modo válido.
- Que los límites opcionales del flujo sean enteros positivos.
- Que las fixtures solo correspondan a agentes del flujo y sean textos no vacíos.
- Que cada respuesta simulada cumpla el prefijo y las secciones declaradas en el contrato.
- Que el flujo se detenga al detectar una salida inválida.
- Que el contexto se transfiera secuencialmente entre etapas y respete el límite de caracteres configurado, descartando primero las etapas más antiguas como hace el orquestador.
- Que el informe declare expresamente cero llamadas reales a modelos y herramientas.

Las pruebas pueden inyectar respuestas por agente en `simulate_workflow(workflow, task, responses)` para comprobar escenarios conformes, incompletos y adversariales. Una secuencia de fixtures permite respuestas diferentes cuando un agente aparece en más de una etapa. Las secuencias vacías y los agentes desconocidos se rechazan como errores de configuración. Una fixture malformada no se sustituye silenciosamente por una respuesta sintética: se registra como salida inválida y detiene las etapas posteriores.

## Validación automatizada

La suite unitaria del contrato comprueba los límites, opciones y tipos; la suite del simulador comprueba los tres flujos existentes en el catálogo: `investigacion`, `critica_corta` y `revision_tecnica`. También cubre identificadores inseguros, catálogos malformados, modos inválidos, límites incorrectos, fixtures vacías/desconocidas/no textuales, transferencia y recorte de contexto, equivalencia del recorte frente a `team_orchestrator.build_prompt`, parada ante incumplimiento y escritura del informe CLI.

## Límites

La simulación usa respuestas sintéticas o fixtures. No prueba razonamiento, precisión técnica, disponibilidad de modelos, latencia de proveedores, adaptadores, permisos, aislamiento ni resultados de herramientas. Un flujo aprobado aquí solo supera controles de contrato y coordinación básica. Antes de producción se requieren pruebas de integración con modelos reales, herramientas autorizadas y laboratorios controlados.

La simulación no cambia el comportamiento de `team_orchestrator.py` ni habilita ejecución automática de herramientas.
