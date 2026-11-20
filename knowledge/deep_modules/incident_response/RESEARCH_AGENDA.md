# Agenda de investigación: incident_response

**Dominio:** incident_response · **Corte:** 2026-11-19 · **Madurez:** M2 editorial; no M3/M4/M5 · **Estado:** `research_agenda_defined`, protocolo propuesto; no ejecutado.
**Objetivo de diseño:** L4; la madurez efectiva permanece M2 editorial hasta disponer de fuentes leídas y resultados.  
**Hipótesis central:** ¿Qué diseño de playbook reduce el tiempo y el impacto de respuesta sin producir acciones irreversibles, pérdida de evidencia o interrupción innecesaria?

## Pregunta central

¿Qué diseño de playbook reduce el tiempo y el impacto de respuesta sin producir acciones irreversibles, pérdida de evidencia o interrupción innecesaria?

## Alcance, exclusiones y ética

Los estudios se limitan a datos sintéticos, datasets con licencia y activos propios o expresamente autorizados. No se ejecutarán acciones contra terceros, no se usarán credenciales ni datos personales reales y no se desplegarán muestras/payloads operativos fuera de entornos controlados. Cada experimento debe declarar responsable, autorización, límites de recursos, regla de parada y procedimiento de rollback.

## Protocolos específicos

### R1 — Preparación y severidad

Unidad: escenario tabletop. Variar criticidad, autoridad, roles y dependencia de proveedor. Comparar matriz de severidad contra criterios explícitos. Métricas: consistencia de clasificación, escalamiento y tiempo de decisión.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R2 — Detección y triage

Unidad: alerta sintética etiquetada. Variar ruido, duplicados, telemetría ausente y contexto de activo. Métricas: precision/recall, tiempo de triage y confianza calibrada.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R3 — Contención y preservación

Unidad: incidente simulado en tenant/host demo. Comparar playbook lineal con gates de autorización/evidencia. Métricas: acciones fuera de alcance, evidencia preservada, reversibilidad y tiempo.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R4 — Erradicación/recuperación

Unidad: snapshots y backups sintéticos. Variar vector no corregido, backup contaminado simulado, dependencia y RTO/RPO. Métricas: recuperación, recurrencia y cumplimiento de objetivos.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R5 — Ransomware/BEC/cloud/supply chain

Unidad: escenario de mesa separado por tipo. Medir decisiones, alcance, revocación, comunicación y coordinación.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R6 — Postmortem/mejora

Unidad: informe de ejercicio. Revisores ciegos califican causalidad, evidencia, acciones y métricas. Medir concordancia entre revisores y cierre de acciones.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

## Método

Diseño experimental controlado, con hipótesis falsable, unidad de análisis, variables, baseline, controles, corpus versionado y criterios de exclusión definidos antes de ejecutar.

## Protocolo común de ejecución

1. Congelar pregunta, hipótesis, unidad de análisis, métrica primaria y criterio de exclusión antes de ejecutar.
2. Registrar versiones de OS, herramientas, librerías, datasets, configuración y hardware.
3. Fijar corpus y su procedencia, licencia, etiquetas, hash y particiones; evitar fuga entre train/test o entre versiones.
4. Construir baseline reproducible y controles positivos/negativos.
5. Aislar entorno, registrar reloj y verificar salvaguardas antes de introducir casos.
6. Ejecutar piloto para comprobar instrumentación; no mezclar resultados del piloto con la muestra confirmatoria sin declararlo.
7. Ejecutar repeticiones predefinidas y conservar salidas brutas, logs saneados y errores.
8. Analizar incertidumbre, sesgo de selección, variables de confusión y resultados negativos.
9. Reproducir desde entorno limpio y registrar diferencias.

## Métricas y análisis

Cada protocolo define su métrica primaria. Cuando se evalúe clasificación, reportar matriz de confusión, precision, recall, F1 cuando sea pertinente y prevalencia; no usar accuracy aislada con clases desbalanceadas. Para tiempos, informar mediana, p50/p95, tamaño muestral y condiciones. Para reproducibilidad, declarar qué constituye una repetición válida. Los resultados deben incluir falsos positivos, falsos negativos, intervalos y casos no concluyentes.

## Amenazas a la validez

- **Interna:** versiones, reloj, instrumentación, operador, orden de pruebas y variables no controladas.
- **Externa:** muestras sintéticas o un proveedor no representan todos los entornos.
- **Constructo:** cobertura, alerta o puntuación no equivalen automáticamente a seguridad.
- **Selección:** corpus sesgado, duplicados y contaminación entre particiones.
- **Reproducibilidad:** cambios de herramienta, firmware, dependencias o datos.
- **Ética/legal:** autorización, privacidad, licencias, divulgación y retención.

## Reproducibilidad

Conservar scripts, datos, hashes, versiones, configuración, logs y pasos de ejecución para permitir repetición independiente.

## Entregables

- Protocolo preregistrado y baseline.
- Dataset/corpus con procedencia, licencia, hash y ground truth.
- Scripts, configuración y versiones fijadas.
- Resultados brutos, métricas y análisis estadístico.
- Registro de falsos positivos/negativos y casos no concluyentes.
- Limitaciones, amenazas a validez y plan de reproducción.
- Revisión independiente.

## Puertas de madurez

- **M2:** contenido específico y protocolo reproducible diseñado.
- **M3:** fuentes primarias leídas con extracción de requisitos y síntesis crítica.
- **M4:** experimentos ejecutados, resultados conservados y reproducción interna.
- **M5:** revisión independiente y reproducción por un segundo operador.

**Estado actual:** agenda M2 propuesta. No se declaran experimentos ejecutados ni validación científica.
