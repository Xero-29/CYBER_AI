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
| ART-09 | Integridad de split, IDs, normalización, near-duplicates heurísticos, grupos de origen y denominadores por clase |

## Contrato de salida

- `PASS`: todos los checks deterministas del caso se cumplieron.
- `FAIL`: al menos un invariante no se cumplió.
- El informe identifica `model_execution=false`, `network_access=false` y `synthetic_only=true`.

## Límites que no deben ocultarse

Este harness no ejecuta ataques contra un LLM. No demuestra resistencia a prompt injection, fuga real de un modelo, poisoning efectivo de un índice vectorial, seguridad de una caché distribuida ni enforcement de un broker productivo. Sus funciones son modelos de control de referencia con fixtures sintéticos. La integración futura debe adaptar los mismos contratos a componentes reales en un entorno autorizado, conservar denominadores, registrar versiones y capturar telemetría independiente. Ningún PASS del harness promueve madurez experta.


## Pruebas de salida contra un modelo real (opt-in)

El adaptador `model_probe.py` permite ejecutar cuatro probes de comportamiento contra un endpoint compatible con OpenAI Chat Completions. Para Ollama local, inicia el servicio y confirma el modelo disponible con `ollama list`. Después:

```bash
python3 knowledge/deep_modules/ai_red_team/model_probe.py \
  --endpoint http://127.0.0.1:11434/v1/chat/completions \
  --model NOMBRE_DEL_MODELO
```

Casos ejecutados sobre el modelo: ART-01 (inyección directa), ART-02 (inyección indirecta), ART-06 (extracción de canary sintético) y ART-07 (conformidad JSON). El adaptador no expone herramientas ni conecta retrieval. Cada caso genera PASS, FAIL o INCONCLUSIVE. Un FAIL o INCONCLUSIVE devuelve código de salida distinto de cero.

Para un proveedor remoto se exige HTTPS y la opción explícita `--allow-remote`; si requiere clave, definir `CYBER_AI_MODEL_API_KEY` en el entorno sin escribirla en el comando ni en el repositorio. Antes de enviar incluso datos sintéticos, revisar retención, logging y condiciones del proveedor. No enviar secretos reales ni datos personales.

Pruebas del adaptador con un servidor HTTP local simulado:

```bash
python3 -m unittest discover -s tests -p 'test_ai_red_team_model_probe.py' -v
```

El probe es una evaluación limitada de respuestas de modelo, no una evaluación integral del agente. No ejecuta herramientas, no prueba aislamiento real de tenants ni reemplaza el harness determinista ART-01…ART-09.


## Nota de assurance del caso ART-04

La fixture ART-04 ahora comprueba tres condiciones separadas: digest SHA-256, pertenencia a un registro local de claves confiables y prueba HMAC-SHA256 sobre el contenido. La clave usada es sintética y solo existe para el test. HMAC es autenticación con clave compartida; no equivale a firma digital asimétrica, PKI, rotación/gestión de claves ni verificación de provenance de build. El resultado PASS solo valida esta fixture determinista.


### ART-09 — manifiesto e integridad del benchmark

El fixture ahora genera un manifiesto versionado con SHA-256 sobre la representación JSON canónica del dataset sintético. Comprueba esquema, IDs únicos, separación de IDs train/holdout, duplicados tras normalización Unicode NFKC/casefold, candidatos a near-duplicate mediante similitud de secuencia (umbral heurístico 0,90), separación de grupos de origen y denominadores benign/attack en holdout.

**Límites:** la similitud de secuencia no es detección semántica; puede producir falsos positivos y falsos negativos. El manifiesto deja la licencia pendiente de revisión explícita. El fixture es deliberadamente pequeño: tamaño adecuado, ground truth independiente, potencia estadística y validez del benchmark permanecen NOT_ASSESSED / NOT_ESTABLISHED. Un ART-09 PASS solo acredita los invariantes estructurales que ejecuta el código, no la calidad científica del benchmark.
