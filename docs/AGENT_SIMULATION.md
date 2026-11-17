# Simulación multiagente sin modelos reales

`agent_simulation.py` permite validar la estructura y los contratos de los flujos definidos en `config/workflows.json` sin conectarse a Ollama ni a proveedores externos y sin ejecutar herramientas.

## Uso

```bash
python agent_simulation.py --workflow investigacion --task "Simular revisión de una aplicación de laboratorio"
```

El informe JSON se guarda por defecto en `reports/agent_simulations/`. Se puede indicar una ruta explícita con `--output`.

## Qué comprueba

- Que el flujo tenga pasos y que cada paso tenga agente, objetivo y modo válido.
- Que cada respuesta simulada cumpla el prefijo y las secciones declaradas en el contrato.
- Que el flujo se detenga al detectar una salida inválida.
- Que el contexto se transfiera secuencialmente entre etapas.
- Que el informe declare expresamente cero llamadas reales a modelos y herramientas.

Las pruebas pueden inyectar respuestas por agente en `simulate_workflow(workflow, task, responses)` para comprobar escenarios conformes, incompletos y adversariales.

## Límites

La simulación usa respuestas sintéticas o fixtures. No prueba razonamiento, precisión técnica, disponibilidad de modelos, latencia de proveedores, adaptadores, permisos, aislamiento ni resultados de herramientas. Un flujo aprobado aquí solo supera controles de contrato y coordinación básica. Antes de producción se requieren pruebas de integración con modelos reales, herramientas autorizadas y laboratorios controlados.

La simulación no cambia el comportamiento de `team_orchestrator.py` ni habilita ejecución automática de herramientas.
