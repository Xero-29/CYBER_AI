# Agenda de investigación: Fraude digital y abuso

**Dominio:** `fraud_abuse` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta, sin resultados empíricos declarados.

## Pregunta central

¿Qué mecanismos y arquitecturas permiten verificar seguridad y resiliencia de Fraude digital y abuso frente a amenazas específicas, restricciones de entorno y fallos de componentes, y qué limitaciones quedan sin resolver?

## Líneas de estudio

### 1. modelos de abuso y trust/safety

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de modelos de abuso y trust/safety están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 2. identidad sintética y bots

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de identidad sintética y bots están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 3. grafos y anomalías

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de grafos y anomalías están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 4. account takeover

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de account takeover están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 5. detección y fricción adaptativa

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de detección y fricción adaptativa están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 6. privacidad y falsos positivos

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de privacidad y falsos positivos están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 7. apelación y métricas

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de apelación y métricas están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
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
