# IoT y hardware embebido — Guía de dominio

**ID:** `iot_hardware` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Protege dispositivos conectados, sensores, gateways, firmware, interfaces de depuración y cadenas de actualización. IoT combina ciberseguridad, seguridad física, disponibilidad y privacidad. No conectar herramientas de análisis a equipos de terceros ni escribir firmware o comandos en dispositivos en servicio.

## Arquitectura y amenazas
Inventariar MCU/SoC, bootloader, firmware, secure element, sensores, radios, gateway, nube, móvil y backend. Riesgos: credenciales por defecto, firmware sin firma, debug UART/JTAG abierto, OTA sin autenticación, claves compartidas, protocolos inseguros, actualización rollback, exposición de datos y ausencia de soporte.

## Competencias específicas
- Analizar BOM, SBOM, componentes y ciclo de vida del dispositivo.
- Revisar secure boot, root of trust, firmware signing y anti-rollback.
- Evaluar UART, JTAG, SWD, SPI, I2C y buses expuestos.
- Analizar Wi-Fi, BLE, Zigbee, Thread, MQTT y CoAP.
- Proteger provisión, identidad única y rotación de credenciales.
- Diseñar OTA segura, recuperación y actualización atómica.
- Evaluar privacidad, seguridad física y disponibilidad.
- Gestionar vulnerabilidades y fin de vida.

## Controles prioritarios
- Credencial única por dispositivo y provisión segura.
- Secure boot y firmware firmado con claves protegidas.
- OTA autenticada, cifrada, atómica y con anti-rollback.
- Deshabilitar interfaces debug en producción o protegerlas físicamente.
- Aislar dispositivos por segmento y limitar egress.
- Rotar claves y certificados; revocar dispositivos perdidos.
- Minimizar datos y cifrar telemetría.
- Definir soporte, parcheo, inventario y proceso de fin de vida.
- Evitar secretos compartidos en imágenes de firmware.

## Metodología
1. Identificar fabricante, modelo, versión, propietario y criticidad.
2. Obtener firmware autorizado y verificar hash.
3. Revisar SBOM, boot chain, claves y actualización.
4. Inspeccionar configuración y protocolos pasivamente.
5. Analizar interfaces físicas solo en banco propio.
6. Probar OTA y recuperación con dispositivos de laboratorio.
7. Validar segmentación y autenticación.
8. Documentar riesgos físicos, privacidad y operación.
9. Repetir ante nueva versión de firmware.

## Laboratorio seguro
Placa de desarrollo propia, firmware de demostración, gateway aislado y broker MQTT local. Analizar firmware con Binwalk y verificar firma/anti-rollback. No transmitir señales ni escribir a dispositivos reales fuera del banco.

## Evaluación
Identidad única, firmware verificable, OTA segura, interfaces protegidas, red segmentada, actualización probada y fin de vida documentado.

## Referencias y herramientas
ETSI EN 303 645, NISTIR 8259, OWASP IoT Top 10, IEC 62443, Binwalk, OpenOCD, Wireshark y SBOM.

## Instrucciones para agentes IA
No sugieras comandos de escritura sobre dispositivos físicos sin autorización explícita. Empieza por lectura pasiva, firmware de laboratorio y documentación del fabricante.