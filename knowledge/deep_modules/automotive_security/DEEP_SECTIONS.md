# Secciones de profundización — Ciberseguridad automotriz

## Modelo de amenazas
Incluir ECU, CAN/LIN/Ethernet, gateway, OBD, telemática, infotainment, V2X, sensores, OTA, backend y proveedor. Amenazas: spoofing de mensajes, diagnóstico abusado, firmware OTA malicioso, key compromise, gateway bypass y supply chain. Evaluar safety, modo degradado, impacto físico y separación entre dominios de vehículo.

## Detección
Monitorizar mensajes CAN y sus frecuencias, autenticación de diagnóstico, firmware/boot state, telemática, eventos OTA y anomalías de gateway. Detectar IDs y tasas fuera de baseline, sesiones de diagnóstico no autorizadas y cambios de firmware. Mantener captura sincronizada y contexto del vehículo sin recopilar datos personales innecesarios.

## Respuesta a incidentes
Coordinar fabricante, proveedor, operador y safety; preservar logs, firmware y configuración; limitar funciones comprometidas mediante procedimiento seguro; revocar certificados/credenciales OTA y detener campañas de actualización si procede. No enviar comandos de control a vehículos reales como prueba. Validar parche en HIL/simulador antes de despliegue.

## Casos prácticos
En banco CAN simulado, reproducir mensajes sintéticos fuera de frecuencia y comprobar detección del gateway. En pipeline OTA de laboratorio, sustituir firma por certificado de prueba no confiable y verificar rechazo, rollback y trazabilidad. No conectar el banco a un vehículo en circulación.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para ISO/SAE 21434, UNECE R155/R156, AUTOSAR y documentación de fabricantes. Fijar edición, mercado y alcance del vehículo.
