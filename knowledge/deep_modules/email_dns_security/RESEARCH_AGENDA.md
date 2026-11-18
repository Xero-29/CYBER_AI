# Agenda de investigación: Correo, DNS y dominios

**Dominio:** `email_dns_security` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta, sin resultados empíricos declarados.

## Pregunta central

¿Qué mecanismos y arquitecturas permiten verificar seguridad y resiliencia de Correo, DNS y dominios frente a amenazas específicas, restricciones de entorno y fallos de componentes, y qué limitaciones quedan sin resolver?

## Líneas de estudio

### 1. SPF, DKIM y DMARC

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de SPF, DKIM y DMARC están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 2. DNSSEC y delegación

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de DNSSEC y delegación están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 3. TLS, MTA-STS y DANE

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de TLS, MTA-STS y DANE están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 4. phishing y BEC

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de phishing y BEC están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 5. dominios y certificados

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de dominios y certificados están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 6. reputación y detección

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de reputación y detección están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
- **Hipótesis provisional:** la evaluación contextual con threat model y controles medibles revela brechas que una revisión de cumplimiento o configuración aislada no detecta.
- **Diseño:** revisar especificaciones y literatura; crear taxonomía; definir activos y dependencias; construir simulación/laboratorio aislado; establecer baseline; probar escenarios controlados y límites; repetir.
- **Métricas:** cobertura de amenazas, integridad, disponibilidad, tiempo de recuperación, tasa de fallo, interoperabilidad y reproducibilidad, según aplique.
- **Artefacto:** threat model, protocolo, datos sintéticos, scripts, registros, resultados, análisis y guía de reproducción.

### 7. recuperación de cuentas

- **Pregunta:** ¿Qué amenazas, supuestos y modos de fallo de recuperación de cuentas están respaldados por evidencia y cuáles siguen insuficientemente estudiados?
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
