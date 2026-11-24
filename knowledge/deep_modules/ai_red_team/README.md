# Módulo de profundización: Red teaming de IA y agentes

> **Estado:** borrador estructurado para desarrollo; no es contenido experto validado ni acredita fuentes verificadas. **ID:** `ai_red_team`.

## Propósito y límites

Currículo técnico de Red teaming de IA y agentes; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Las pruebas activas requieren autorización escrita, alcance, ventana, límites de impacto y criterio de parada. Los laboratorios usan datos sintéticos y entornos aislados.

## Competencias

- Explicar arquitectura, componentes, dependencias, protocolos y límites de confianza.
- Inventariar activos, identidades, datos, interfaces y propietarios.
- Modelar amenazas, precondiciones, impacto, probabilidad e incertidumbre.
- Seleccionar controles preventivos, detectivos y correctivos con evidencia verificable.
- Ejecutar procedimientos reproducibles, analizar falsos positivos y verificar mitigaciones.
- Comunicar hallazgos con alcance, evidencia mínima, impacto, limitaciones, remediación y retest.

## Temas técnicos del dominio

### 1. Plan de pruebas y threat model
Delimitar el sistema, activos, actores, capacidades, objetivos, rutas y reglas de parada. Producir manifiesto de alcance, diagrama de arquitectura/flujo de datos y matriz amenaza-control-evidencia. No iniciar pruebas sin autorización y baseline.

### 2. Prompt injection
Evaluar entradas directas, documentos indirectos, contenido multimodal, salidas de herramientas, memoria y persistencia multi-turn. Conservar etiquetas de origen e integridad; demostrar que el contenido no confiable no adquiere autoridad ni activa efectos privilegiados.

### 3. Abuso de herramientas y agencia
Probar exceso de funcionalidad, permisos y autonomía. Validar principal confiable, autorización server-side, esquemas cerrados, validación semántica, aprobación humana, idempotencia, límites de destino y kill switch.

### 4. RAG poisoning y aislamiento entre tenants
Probar ingestión no autorizada, alteración de corpus, chunking, embeddings, filtros ACL, caché, citas y memoria derivada. El aislamiento debe comprobarse en el servicio de datos, no solo por instrucciones del prompt.

### 5. Exposición y extracción
Usar canaries sintéticos para medir fuga por respuesta, citas, logs, errores, herramientas y canales laterales permitidos por el harness. Distinguir divulgación de datos, extracción de modelo y exposición de contexto interno; no usar secretos reales.

### 6. Evaluación adversarial
Construir datasets versionados y no contaminados, con ground truth, splits, denominadores y métricas por clase. Medir acciones no autorizadas, fuga, falsos positivos/negativos, utilidad, coste y latencia; evitar scores agregados que oculten fallos críticos.

### 7. Retest y reporte
Repetir el mismo caso tras mitigación con versiones fijadas. Comparar baseline, efecto, regresiones, falsos positivos, rollback y límites de generalización. PASS solo aplica a la configuración y casos ejecutados.

**Desarrollo por capas:** [dossier teórico de doce capas](AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md).  
**Protocolo de laboratorio:** [catálogo de nueve pruebas adversariales](AI_RED_TEAM_TEST_CATALOG_V1.md).  
**Compendio y mapa de navegación:** [TECHNICAL_COMPENDIUM.md](TECHNICAL_COMPENDIUM.md).

## Procedimiento operativo

1. Registrar autorización, objetivo, propietario, alcance, exclusiones, ventana y parada.
2. Inventariar componentes, versiones, configuraciones, identidades y flujos de datos.
3. Representar arquitectura, límites de confianza y escenarios de amenaza.
4. Elegir pruebas proporcionales; justificar herramientas, parámetros y límites de impacto.
5. Separar hechos, inferencias e hipótesis; correlacionar evidencia y falsos positivos.
6. Priorizar mitigaciones, responsables, reversión y riesgo residual.
7. Repetir pruebas, ejecutar regresión y sanear evidencias.
8. Documentar cobertura, exclusiones, incertidumbre y fecha de revisión.

## Laboratorio reproducible

Entorno local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros; snapshots, privilegios mínimos y límites de recursos. Establecer baseline, introducir un fallo sintético del dominio, detectarlo, analizarlo, corregirlo reversiblemente y repetir la prueba. Entregar diagrama, inventario, modelo de amenazas, procedimiento, datos sintéticos, resultados esperados/observados y evidencia.

## Evaluación

Evaluar precisión, cobertura, reproducibilidad, calidad de evidencia, seguridad, análisis de falsos positivos y verificación de mitigación. No aprobar si falta autorización, procedencia, evidencia reproducible o retest. Incluir preguntas conceptuales, escenario, laboratorio y respuestas razonadas.

## Fuentes y procedencia

Fuentes candidatas registradas en `knowledge/research/source_registry.json` y `knowledge/research/field_studies/SOURCE_REGISTER_2026-11-18.json`. Se consultaron a nivel de página OWASP LLM Top 10 2026, OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10), OWASP GenAI Red Teaming Guide y la ficha NIST AI 200-3. La lectura integral, licencia, localizadores por afirmación y revisión independiente siguen pendientes. Registrar título, editor, URL canónica, versión, fechas, SHA-256 del artefacto cuando aplique y alcance. La mera inclusión no convierte una fuente en evidencia verificada.

## Criterios de publicación

- [ ] Explicación técnica original y específica por tema y niveles L0–L4.
- [ ] Diagramas, tablas, configuraciones y ejemplos versionados.
- [ ] Fuentes primarias con vigencia, licencia y procedencia comprobadas.
- [ ] Caso de estudio y laboratorio con resultados esperados.
- [ ] Ejercicios con rúbrica y respuestas razonadas.
- [ ] Revisión técnica independiente y pruebas de reproducibilidad.

**Madurez:** `draft_structured_not_expert_validated`.


## Harness sintético ejecutable

Se añadió `lab_runner.py` y la guía `LAB_EXECUTION_GUIDE_V1.md`. Desde la raíz del repositorio:

```bash
python3 knowledge/deep_modules/ai_red_team/lab_runner.py
python3 knowledge/deep_modules/ai_red_team/lab_runner.py --json
python3 -m unittest tests.test_ai_red_team_lab -v
```

El runner cubre ART-01…ART-09 con fixtures sintéticos, modelos deterministas de controles server-side y evidencia estructurada. No invoca un LLM, no accede a red y no prueba un agente desplegado. Sus PASS significan únicamente que los controles de referencia y las pruebas del harness se comportan como se definieron; la integración con un modelo, RAG, broker y caché reales sigue pendiente.


### Probes opt-in contra un modelo

Para probar comportamiento de un modelo compatible con OpenAI Chat Completions, el adaptador local `model_probe.py` ejecuta ART-01, ART-02, ART-06 y ART-07 con un canary sintético, sin herramientas. Ejemplo con Ollama local:

```bash
python3 knowledge/deep_modules/ai_red_team/model_probe.py \
  --endpoint http://127.0.0.1:11434/v1/chat/completions \
  --model NOMBRE_DEL_MODELO
```

Por defecto solo acepta HTTP en loopback. Un endpoint remoto requiere HTTPS y `--allow-remote`. El reporte distingue PASS/FAIL/INCONCLUSIVE. No equivale a probar un sistema RAG, broker de herramientas, aislamiento multi-tenant o agente productivo; revisar `LAB_EXECUTION_GUIDE_V1.md`.
