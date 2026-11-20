# Secciones de profundización — Inteligencia de amenazas

## Modelo de amenazas
Definir decisiones que la inteligencia debe apoyar, adversarios relevantes, activos y horizonte temporal. Separar strategic, operational, tactical y technical intelligence. Amenazas: fuentes manipuladas, indicadores caducos, sesgo de confirmación, atribución débil, duplicados y automatización de bloqueos sin contexto. Registrar procedencia, confianza, observación, primera/última vez y restricciones de redistribución.

## Detección
Convertir hipótesis y TTP en consultas sobre telemetría interna; evaluar cobertura de ATT&CK y calidad de fuentes. Correlacionar IOC con contexto temporal, prevalencia, infraestructura compartida y falsos positivos. Detectar cambios de comportamiento más allá de hashes o IP. Medir tiempo desde publicación hasta ingestión, porcentaje de indicadores útiles y tasa de alertas confirmadas.

## Respuesta a incidentes
Enriquecer incidente con inteligencia contextual, validar observables en entorno propio, priorizar contención por confianza e impacto y evitar bloqueos automáticos de IOC compartidos sin revisión. Expirar indicadores, conservar fuente y rationale, compartir hallazgos con equipos autorizados y retroalimentar requisitos de inteligencia.

## Casos prácticos
Recibir un feed de prueba con dominios duplicados y un IOC benigno compartido por CDN. Normalizar, deduplicar, enriquecer, asignar confianza y caducidad; correlacionar con DNS interno; decidir qué observables generan alerta y cuáles no deben bloquearse. Evaluar falsos positivos y trazabilidad de cada decisión.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para MITRE ATT&CK, STIX 2.1, TAXII 2.1, FIRST TLP y documentación de fuentes. Una etiqueta de confianza no sustituye la evaluación de procedencia.
