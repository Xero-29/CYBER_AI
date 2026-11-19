# Secciones de profundización — Respuesta a incidentes

## Modelo de amenazas
Considerar intrusión, ransomware, robo de identidad, fuga de datos, abuso interno, cloud compromise, proveedor comprometido y fallos de disponibilidad. Modelar dependencias entre activos críticos, canales de mando, herramientas de respuesta, backups e identidades privilegiadas. El propio plano de respuesta puede estar comprometido; definir canal alternativo y autoridad de emergencia.

## Detección
Convertir hipótesis y señales en casos de uso con fuentes, umbrales, contexto y criterios de escalado. Correlacionar endpoint, identidad, red, cloud, aplicaciones y terceros. Distinguir alerta, evento e incidente confirmado. Medir MTTD, tiempo de triage, cobertura de telemetría, tasa de falsos positivos y porcentaje de casos con evidencia suficiente.

## Respuesta a incidentes
Aplicar ciclo preparación, detección/análisis, contención, erradicación, recuperación y lecciones. Definir playbooks por ransomware, credenciales, exfiltración y cloud. Cada acción especifica autorización, impacto, reversibilidad, evidencia a preservar y rollback. Verificar recuperación con integridad, control de persistencia, rotación de secretos y monitoreo reforzado.

## Casos prácticos
Ejercicio tabletop de ransomware que afecta identidad y backups: decidir aislamiento, preservar evidencia, cambiar canal de mando, recuperar identidad desde estado confiable y restaurar servicio prioritario. Medir tiempos reales, decisiones bloqueadas, dependencias omitidas y comunicación. Repetir con un backup comprometido para comprobar independencia de recuperación.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-61, CISA StopRansomware, FIRST CSIRT Services Framework y MITRE ATT&CK. Fijar edición, fecha y jurisdicción.
