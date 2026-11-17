# Agenda de investigación: Satélites y sistemas espaciales

**Dominio:** `satellite_security` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta, sin resultados empíricos declarados.

## Pregunta central

¿Qué mecanismos y arquitecturas permiten verificar seguridad y resiliencia de Satélites y sistemas espaciales frente a amenazas específicas, restricciones de entorno y fallos de componentes, y qué limitaciones quedan sin resolver?

## Líneas de estudio

### 1. segmentos espacial y terrestre

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de segmentos espacial y terrestre están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 2. TT&C y telemetría

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de TT&C y telemetría están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 3. RF y espectro

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de RF y espectro están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 4. firmware y estaciones terrestres

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de firmware y estaciones terrestres están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 5. resiliencia y anti-jamming

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de resiliencia y anti-jamming están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 6. identidad y criptografía

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de identidad y criptografía están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 7. simulación y coordinación

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de simulación y coordinación están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

## Revisión de evidencia

Registrar fuentes primarias, estándares, documentos regulatorios, papers y advisories con versión, fecha, jurisdicción y aplicabilidad. Diferenciar evidencia experimental de recomendaciones normativas. Mantener registro de contradicciones y vacíos de literatura.

## Diseño y análisis

Predefinir pregunta, hipótesis, variables, baseline, comparadores, condiciones, métricas y criterios de parada. Documentar hardware, software, versiones, simulador y configuración. Evaluar validez, incertidumbre, generalización y factores de confusión. No inferir seguridad total a partir de pruebas parciales.

## Seguridad

No probar sistemas espaciales, físicos, telecomunicaciones ni infraestructura crítica en producción. Usar simuladores, emuladores y bancos aislados; autorización escrita; límites de potencia/tráfico; parada de emergencia y supervisión especializada.

## Entregables

Estado del arte; taxonomía; mapa de estándares; arquitectura; threat model; protocolo; simulador/lab; datos y scripts; hashes; resultados; limitaciones; revisión independiente.

**Madurez:** `research_agenda_defined`. M4 requiere investigación ejecutada; M5 requiere reproducción independiente.
