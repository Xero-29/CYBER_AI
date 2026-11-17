# Compendio técnico: OT, ICS y SCADA

ID: `ot_ics` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de OT, ICS y SCADA; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Ruta de desarrollo técnico; no declara cobertura exhaustiva ni fuentes leídas íntegramente. Operar solo con autorización explícita, datos sintéticos y laboratorios aislados. En infraestructuras físicas o críticas, usar simulación/bancos de pruebas y no intervenir producción.

## Desarrollo por subtema
### 1. Purdue, zonas y conduits

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. PLC, RTU, HMI y SCADA

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. Modbus, DNP3 y OPC UA

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. safety y ventanas de cambio

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. segmentación y acceso remoto

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. inventario pasivo y detección

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. respuesta con operaciones

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

## Laboratorio
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Prueba | Evidencia |
|---|---|---|
| ot_ics-LAB-01 | Baseline | Versiones, configuración, hashes y salida |
| ot_ics-LAB-02 | Evento/fallo sintético | Entrada, precondiciones, logs y resultado |
| ot_ics-LAB-03 | Detección/diagnóstico | Señal, cobertura, precisión y límites |
| ot_ics-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después y retest |

Diseño propuesto; no ejecutado.

## Métricas
Definir métricas acordes al caso: cobertura, eficacia del control/detección, falsos positivos/negativos, latencia, disponibilidad, impacto, recuperación y repetibilidad. Publicar unidad de análisis, muestra, baseline, versiones, repeticiones e incertidumbre.

## Método de investigación
- Búsqueda reproducible: bases, consultas, fechas, idiomas e inclusión/exclusión.
- Fuentes: estándares, especificaciones, documentación primaria, advisories y artículos revisados por pares.
- Texto completo solo se marca revisado tras inspección real.
- Extraer método, población, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y separar evidencia, inferencia e hipótesis.
- Registrar versión, licencia, URL canónica, fecha y hash cuando sea legal archivar.

## Preguntas candidatas
1. ¿Qué controles mejoran la eficacia frente a un baseline y en qué condiciones?
2. ¿Qué factores explican divergencias entre el estado del arte y las pruebas reproducidas?
3. ¿Qué señales permiten detectar antes sin elevar falsos positivos o impacto operacional?

Cada estudio debe definir H0/H1, variables, muestra, comparadores, refutación, análisis, ética y limitaciones.

## Artefactos exigibles
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos, datos, identidades, versiones y dependencias.
- [ ] Modelo de amenazas.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimientos reproducibles con rollback y parada.
- [ ] Laboratorio y casos con resultados medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencia, edición, fecha y hashes.
- [ ] Incertidumbre, sesgos y amenazas a validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No prueba profundidad ni madurez M3/M4/M5. Avanzar exige lectura crítica, artefactos específicos, experimentos ejecutados y evidencia auditable.
