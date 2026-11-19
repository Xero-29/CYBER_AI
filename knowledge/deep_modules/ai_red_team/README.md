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

### 1. plan de pruebas y threat model

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

### 2. prompt injection

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

### 3. abuso de herramientas y agencia

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

### 4. RAG poisoning y cross-tenant

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

### 5. exfiltración y extracción

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

### 6. evaluación adversarial

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

### 7. retest y reporte

Investigar arquitectura y dependencias; conceptos y variantes; configuraciones relevantes; fallos frecuentes y escenarios de abuso; controles y telemetría; criterios de prueba y regresión. Producir un esquema, procedimiento reproducible, resultado esperado/observado, análisis de impacto y limitaciones.

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

Pendiente de curación. Registrar título, editor, URL canónica, versión, fechas de publicación/consulta, licencia, SHA-256 del artefacto cuando aplique, temas respaldados y revisor. Priorizar documentación primaria oficial. No declarar verificada una fuente por su mera inclusión.

## Criterios de publicación

- [ ] Explicación técnica original y específica por tema y niveles L0–L4.
- [ ] Diagramas, tablas, configuraciones y ejemplos versionados.
- [ ] Fuentes primarias con vigencia, licencia y procedencia comprobadas.
- [ ] Caso de estudio y laboratorio con resultados esperados.
- [ ] Ejercicios con rúbrica y respuestas razonadas.
- [ ] Revisión técnica independiente y pruebas de reproducibilidad.

**Madurez:** `draft_structured_not_expert_validated`.


## Protocolo obligatorio de aceptación en frío

Aplicar [`knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md`](../../COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md): el dossier no se aprueba por sus 12 capas. Cada tema debe demostrar enseñanza, explicación, análisis y diseño, con evaluación estática, fuentes trazables y cierre de no conformidades.

## Desarrollo teórico profundo

El dossier disciplinar de 12 capas para los siete temas base se encuentra en [AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md](AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md). Incluye modelos, arquitectura, estándares, análisis avanzado, seguridad, investigación, diseño de laboratorios/datasets, métricas, especificaciones de Skills y evaluación en frío. Su estado sigue siendo V1 en desarrollo: el currículo ampliado, lectura integral de fuentes, auditoría de 84 celdas y revisión independiente permanecen pendientes. No declara ejecución de laboratorios.
