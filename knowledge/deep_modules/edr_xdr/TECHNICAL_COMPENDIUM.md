# Compendio técnico: EDR, XDR y endpoints

ID: `edr_xdr` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de EDR, XDR y endpoints; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Esta guía organiza el trabajo técnico y experimental; no declara cobertura exhaustiva ni lectura completa de fuentes. Solo usar sistemas propios o autorizados, datos sintéticos y laboratorios aislados. No realizar pruebas activas fuera del alcance autorizado.

## Desarrollo por subtema
### 1. telemetría endpoint

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 2. procesos, memoria y filesystem

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 3. detecciones conductuales

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 4. aislamiento y respuesta controlada

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 5. integración y correlación XDR

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 6. tuning y falsos positivos

- **Fundamentos:** describir modelo, arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas y fallos:** enumerar abuso, debilidades, errores de configuración, dependencias, fallos de proceso y precondiciones.
- **Controles:** mapear prevención, detección, respuesta y recuperación; declarar cobertura, residual y efectos secundarios.
- **Pruebas:** diseñar casos positivos, negativos, límites y regresión con datos sintéticos, resultados esperados, logs y criterio de parada.
- **Investigación:** comparar alternativas y evidencia publicada; declarar supuestos, desacuerdos y límites.
- **Resultado exigido:** análisis técnico original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento y limitaciones.

### 7. forense y recuperación

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
| edr_xdr-LAB-01 | Baseline | Configuración, versiones, hashes y salida |
| edr_xdr-LAB-02 | Fallo sintético | Precondiciones, entrada, logs y resultado |
| edr_xdr-LAB-03 | Detección | Señal, regla, cobertura y limitaciones |
| edr_xdr-LAB-04 | Mitigación y retest | Diff, antes/después, rollback |

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
