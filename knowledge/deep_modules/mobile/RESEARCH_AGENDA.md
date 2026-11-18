# Agenda de investigación: Seguridad móvil

**Dominio:** `mobile` · **Objetivo:** L4 · **Estado:** agenda de investigación propuesta.

## Pregunta central

¿Cómo medir y comparar la seguridad, robustez, privacidad y operabilidad de mobile OS trust boundaries, app sandbox, permissions and secure storage en Seguridad móvil, bajo modelos de amenaza y restricciones documentadas?

## Preguntas de investigación por tema

### R1 — Android sandbox, permisos y Keystore

**Pregunta:** ¿Qué propiedades de seguridad de Android sandbox, permisos y Keystore se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

### R2 — iOS sandbox, entitlements y Keychain

**Pregunta:** ¿Qué propiedades de seguridad de iOS sandbox, entitlements y Keychain se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

### R3 — almacenamiento local y backups

**Pregunta:** ¿Qué propiedades de seguridad de almacenamiento local y backups se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

### R4 — TLS y confianza del dispositivo

**Pregunta:** ¿Qué propiedades de seguridad de TLS y confianza del dispositivo se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

### R5 — deep links, IPC y WebView

**Pregunta:** ¿Qué propiedades de seguridad de deep links, IPC y WebView se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

### R6 — MASVS/MSTG y análisis

**Pregunta:** ¿Qué propiedades de seguridad de MASVS/MSTG y análisis se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

### R7 — MDM/MAM y respuesta

**Pregunta:** ¿Qué propiedades de seguridad de MDM/MAM y respuesta se mantienen bajo cambios de configuración, carga, versiones y condiciones adversas? ¿Qué fallos residuales permanecen?

**Hipótesis falsable inicial:** el control o diseño evaluado reduce una tasa de fallo/abuso definida frente a una baseline, sin exceder el presupuesto de coste/latencia/usabilidad predefinido.

**Diseño:** especificar amenaza y alcance; fijar versiones; preparar baseline y comparador; aislar variables; generar casos normales, límite y adversos; repetir con semillas registradas; medir resultados y conservar artefactos.

**Métricas:** cobertura y eficacia, error de detección, falsos positivos/negativos, rendimiento, coste, robustez y tasa de reproducción. Definir fórmula y unidad antes de medir.

**Entregable:** protocolo, matriz de evidencia, datos sintéticos o autorizados, análisis estadístico, incertidumbre, limitaciones, scripts y hashes.

## Revisión de literatura y estado del arte

Buscar estándares, especificaciones, artículos revisados por pares, tesis, advisories y documentación primaria. Registrar bases, consultas exactas, fecha, filtros, criterios de inclusión/exclusión y duplicados. Clasificar calidad metodológica, actualidad, sesgo, reproducibilidad y aplicabilidad. Sintetizar enfoques, resultados en conflicto y vacíos; no extrapolar resultados fuera de su contexto.

## Protocolo experimental

1. Definir población/sistemas, pregunta, hipótesis nula/alternativa y criterios de refutación.
2. Definir variables independientes/dependientes, confusores, muestras y comparadores.
3. Predefinir métricas, método estadístico, intervalos de confianza y tratamiento de datos faltantes.
4. Registrar entorno, hardware, software, versiones, configuración, semillas y dependencias.
5. Ejecutar pruebas aisladas, autorizadas y de bajo impacto; registrar desviaciones.
6. Repetir, analizar resultados y evaluar validez interna, externa, de constructo y conclusión.
7. Publicar datos permitidos, código, configuración, SBOM, hashes y procedimiento de reproducción.

## Requisitos éticos y de seguridad

Autorización escrita, alcance, exclusiones, límites de impacto y parada. No evaluar sistemas de terceros ni producción crítica sin permiso explícito y plan de seguridad. Minimizar datos, anonimizar y proteger evidencia. Aplicar divulgación coordinada cuando corresponda.

## Criterios M4/M5

M4 requiere revisión bibliográfica documentada, experimento ejecutado, análisis y limitaciones. M5 requiere revisión técnica independiente y reproducción por otro operador. La agenda por sí sola no satisface ninguno de esos niveles.

**Madurez actual:** `research_agenda_defined`.
