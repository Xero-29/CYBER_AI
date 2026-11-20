# Secciones de profundización — IoT y hardware conectado

## Modelo de amenazas
Trazar dispositivo, MCU/SoC, boot ROM, firmware, sensores, buses, radio, gateway, cloud, app móvil y cadena de fabricación. Amenazas: firmware sin firma, credenciales compartidas, interfaces debug abiertas, provisioning débil, actualización maliciosa, extracción física y dependencia del fabricante. Considerar seguridad física, disponibilidad y safety.

## Detección
Recolectar inventario y versión/firmware, estado de secure boot, cambios de configuración, autenticación, tráfico de red, comportamiento de sensores y telemetría del gateway. Detectar dispositivos nuevos, certificados inválidos, firmware fuera de baseline, comunicación a destinos desconocidos y cambios de consumo anómalos. La falta de logs del dispositivo debe compensarse en gateway/red.

## Respuesta a incidentes
Aislar dispositivo o segmento sin afectar funciones críticas; preservar firmware, configuración y registros; revocar certificados/credenciales; bloquear comunicación de mando; coordinar con fabricante y operador. Validar actualización firmada, rollback seguro, integridad de identidad y reaprovisionamiento. No reflashear ni resetear antes de preservar evidencia.

## Casos prácticos
En banco aislado, desplegar dos dispositivos de prueba con credencial compartida y firmware firmado. Detectar clonación de identidad y conexión a gateway no autorizado; rotar credenciales por dispositivo, cerrar interfaz debug y ensayar actualización y rollback. Medir tiempo de detección, cobertura y recuperación sin afectar equipos productivos.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para ETSI EN 303 645, NISTIR 8259, OWASP IoT y documentación del fabricante. Registrar modelo, revisión de hardware y firmware.
