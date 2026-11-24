# AI Red Team — guía de ejecución del harness sintético V1

**Runner:** `lab_runner.py`  
**Casos:** ART-01 a ART-09  
**Estado:** controles de referencia ejecutables; integración con un modelo/agente real pendiente.

## Ejecución

Desde la raíz del repositorio:

```bash
python3 knowledge/deep_modules/ai_red_team/lab_runner.py
python3 knowledge/deep_modules/ai_red_team/lab_runner.py --json
python3 -m unittest discover -s tests -p 'test_ai_red_team_lab.py' -v
```

El runner usa únicamente la biblioteca estándar de Python. No hace llamadas de red, no inicia un modelo, no lee secretos del host y no ejecuta herramientas externas. Produce nueve resultados por caso, con estado, checks, métricas y evidencia sintética.

## Cobertura

| Caso | Control comprobado por el harness |
|---|---|
| ART-01 | La entrada del usuario no concede permisos server-side |
| ART-02 | El texto recuperado se conserva como dato no confiable |
| ART-03 | El filtro de tenant se aplica en la función de retrieval |
| ART-04 | Hash y allowlist de firmantes detectan alteración/origen no autorizado |
| ART-05 | Broker mock aplica allowlist, ownership e idempotencia |
| ART-06 | Detección de canaries y redacción de logs |
| ART-07 | Validador estricto rechaza campos extra y payloads inválidos |
| ART-08 | Presupuesto duro limita pasos, llamadas y tokens |
| ART-09 | Separación train/holdout, deduplicación y denominadores por clase |

## Contrato de salida

- `PASS`: todos los checks deterministas del caso se cumplieron.
- `FAIL`: al menos un invariante no se cumplió.
- El informe identifica `model_execution=false`, `network_access=false` y `synthetic_only=true`.

## Límites que no deben ocultarse

Este harness no ejecuta ataques contra un LLM. No demuestra resistencia a prompt injection, fuga real de un modelo, poisoning efectivo de un índice vectorial, seguridad de una caché distribuida ni enforcement de un broker productivo. Sus funciones son modelos de control de referencia con fixtures sintéticos. La integración futura debe adaptar los mismos contratos a componentes reales en un entorno autorizado, conservar denominadores, registrar versiones y capturar telemetría independiente. Ningún PASS del harness promueve madurez experta.
