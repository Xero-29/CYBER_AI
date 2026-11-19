# Secciones de profundización — Seguridad satelital

## Modelo de amenazas
Modelar segmento espacial, segmento terreno, enlaces uplink/downlink, telemetría, tracking, comando, payload, estaciones, proveedores y software de misión. Amenazas: interferencia, spoofing, replay, comando no autorizado, compromiso de estación, supply chain y pérdida de disponibilidad. Considerar ventanas de contacto, latencia, recursos limitados y safety de misión.

## Detección
Correlacionar autenticación de comandos, telemetría, integridad de software, anomalías RF, estado orbital/operativo, acceso a estaciones y cambios de configuración. Detectar comandos fuera de ventana, patrones de replay, degradación de enlace y desviaciones de telemetría. Distinguir interferencia ambiental de actividad deliberada.

## Respuesta a incidentes
Aplicar procedimientos de misión aprobados: suspender comandos no esenciales, cambiar credenciales/llaves, usar canal alternativo validado y preservar telemetría. Coordinar operador, fabricante y autoridad competente. No improvisar comandos de recuperación; validar consecuencias físicas y ventana de contacto.

## Casos prácticos
En simulador de enlace, inyectar mensajes de telemetría repetidos y comandos con autenticación inválida. Verificar rechazo, alarma, preservación de trazas y recuperación de sesión. Medir latencia y pérdida de enlace; documentar que el resultado no valida hardware espacial real.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para CCSDS security, NIST, documentos de agencia espacial y estándares aplicables. Diferenciar recomendación, estándar y política de misión.
