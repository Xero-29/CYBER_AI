# Compendio técnico: SOC, SIEM y SOAR

ID: `soc_siem` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de SOC, SIEM y SOAR; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Esta guía organiza el trabajo técnico y experimental; no declara cobertura exhaustiva ni lectura completa de fuentes. Solo usar sistemas propios o autorizados, datos sintéticos y laboratorios aislados. No realizar pruebas activas fuera del alcance autorizado.

## Desarrollo por subtema
### 1. telemetría y normalización

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 2. SIEM y retención

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 3. correlación y detección

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 4. ATT&CK coverage

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 5. SOAR y aprobaciones

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 6. triage y gestión de casos

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 7. detección como código

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

## Laboratorio reproducible
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Caso | Evidencia |
|---|---|---|
| soc_siem-LAB-01 | Baseline | Configuración, versiones, hashes y salida |
| soc_siem-LAB-02 | Fallo sintético | Precondiciones, entrada, logs y resultado |
| soc_siem-LAB-03 | Detección | Señal, regla, cobertura y limitaciones |
| soc_siem-LAB-04 | Mitigación y retest | Diff, antes/después, rollback |

Diseño definido; ejecución no realizada.

## Métricas
Elegir según hipótesis: cobertura, precisión/recall, falsos positivos/negativos, latencia, disponibilidad, impacto colateral, coste operativo, tiempo de remediación y reproducibilidad. Registrar muestra, unidad de análisis, baseline, versiones, repeticiones e incertidumbre.

## Método bibliográfico
- Registrar bases, consultas, fechas e inclusión/exclusión.
- Priorizar estándares, especificaciones, documentación primaria y literatura revisada por pares.
- No marcar texto completo revisado sin haberlo inspeccionado.
- Extraer método, resultados, población, limitaciones, sesgos y amenazas a validez.
- Comparar enfoques y resultados divergentes; separar evidencia, inferencia e hipótesis.
- Conservar metadatos, licencia, edición, fecha y SHA-256 cuando proceda.

## Preguntas de investigación
1. ¿Qué control o metodología mejora el resultado frente a un baseline explícito?
2. ¿Qué factores explican divergencias de reproducibilidad entre estudios y laboratorio?
3. ¿Qué compensaciones aparecen entre seguridad, disponibilidad, privacidad, coste y usabilidad?

Definir H0/H1, variables, población, comparadores, criterio de refutación, análisis, ética y limitaciones.

## Artefactos obligatorios
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos, datos, identidades y dependencias.
- [ ] Modelo de amenazas y abuso.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimiento reproducible con rollback y parada.
- [ ] Laboratorio aislado y casos medidos.
- [ ] Caso práctico con hallazgo, impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencias, versiones, fechas y hashes.
- [ ] Incertidumbre, sesgos, falsos positivos/negativos y validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No acredita profundidad ni M3/M4/M5. Para avanzar: revisar fuentes completas, elaborar artefactos específicos, ejecutar casos y registrar evidencia auditable.


## Profundización técnica específica: SOC y SIEM

### Arquitectura de datos
Mapear fuentes, collectors, forwarders, parsers, queues, storage hot/warm/cold, search, detections, case management, SOAR e integraciones. Definir schema común, timezone UTC, identidad de host/usuario, deduplicación, enrichment, retención y control de acceso. Medir ingest lag, pérdida, parsing failures y coste por GB.

### Ingeniería de detección
Cada regla necesita objetivo, amenaza, fuente, query, ventana, umbral, agrupación, suppression, severity, owner, test cases y revisión. Distinguir indicador estático, secuencia, anomalía y correlación. Controlar data quality, baselines, drift y falsos positivos. ATT&CK mapping debe reflejar comportamiento detectado y evidencia, no solo etiqueta.

### Triage y casos
Normalizar alerta con contexto, activos, identidad, criticidad, eventos relacionados, confidence y playbook. Documentar hipótesis, evidencia, decisiones, escalamiento y cierre. Separar incidente, benign true positive, false positive y insufficient data. La automatización debe ser idempotente, auditable y reversible.

### SOAR y automatización
Limitar permisos por integración, validar inputs, evitar command injection, proteger secretos y exigir aprobación en acciones de alto impacto. Implementar timeouts, retries, rate limits, dedupe, rollback y circuit breakers. Simular errores de API, token expirado y datos malformados. Registrar quién/qué autorizó cada acción.

### Métricas y capacidad
Medir MTTD, MTTA, MTTR, alert-to-case ratio, precision/recall, backlog, SLA, coverage, ingest lag, data loss y toil. No premiar cierre rápido sin calidad. Normalizar por severidad, turno, volumen y fuente; auditar métricas y sesgo de muestreo.

### Laboratorios
- Pipeline de logs sintéticos con parsing y normalización.
- Detección por secuencia con ground truth y tuning.
- Playbook SOAR simulado con aprobación y rollback.
- Caída de collector y medición de pérdida/recuperación.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.