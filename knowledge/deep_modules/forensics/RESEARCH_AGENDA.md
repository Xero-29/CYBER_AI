# Agenda de investigación: forensics

**Dominio:** forensics · **Corte:** 2026-11-19 · **Madurez:** M2 editorial; no M3/M4/M5 · **Estado:** `research_agenda_defined`, protocolo propuesto; no ejecutado.
**Objetivo de diseño:** L4; la madurez efectiva permanece M2 editorial hasta disponer de fuentes leídas y resultados.  
**Hipótesis central:** ¿Qué procedimientos de adquisición, preservación y análisis producen evidencia digital íntegra, reproducible y correctamente limitada en su interpretación?

## Pregunta central

¿Qué procedimientos de adquisición, preservación y análisis producen evidencia digital íntegra, reproducible y correctamente limitada en su interpretación?

## Alcance, exclusiones y ética

Los estudios se limitan a datos sintéticos, datasets con licencia y activos propios o expresamente autorizados. No se ejecutarán acciones contra terceros, no se usarán credenciales ni datos personales reales y no se desplegarán muestras/payloads operativos fuera de entornos controlados. Cada experimento debe declarar responsable, autorización, límites de recursos, regla de parada y procedimiento de rollback.

## Protocolos específicos

### R1 — Cadena de custodia

Unidad: expediente sintético y cada transferencia. Variar operador, reloj, hash, medio y evento de custodia. Comparar checklist manual con registro estructurado. Métricas: omisiones, inconsistencias y reproducibilidad.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R2 — Adquisición/write blocker

Unidad: imagen de disco virtual con ground truth. Variar errores de lectura, conexión, herramienta y write blocker. Medir integridad, sectores omitidos, cambios en origen y repetibilidad.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R3 — Filesystems/timeline

Unidad: eventos generados en NTFS/ext4/APFS de laboratorio. Variar timezone, precisión, journal y manipulación de timestamps. Medir exactitud temporal y ambigüedad.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R4 — Memoria/procesos

Unidad: dump de memoria de entrenamiento. Comparar perfiles correctos e incorrectos, arquitectura y herramienta. Medir artefactos recuperados y errores interpretativos.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R5 — Red/correo/browser

Unidad: PCAP, email y perfil de navegador sintéticos. Inyectar pérdida de paquetes, headers falsos y perfiles múltiples. Medir integridad, cobertura y atribuciones erróneas.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R6 — Cloud/móvil/informe

Unidad: exportación de audit logs/snapshot de tenant demo. Variar paginación, retención y zonas. Evaluar trazabilidad, completitud y consistencia entre analistas.

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
