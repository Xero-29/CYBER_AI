# Investigación técnica: Seguridad IoT y dispositivos conectados

**ID:** iot_hardware · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de dispositivos físicos pendiente.

## Modelo de dispositivo
Analizar hardware, boot ROM, bootloader, firmware, RTOS/Linux, radio, sensores/actuadores, interfaces físicas, protocolos, cloud backend, app móvil, identidad y cadena de suministro. El dispositivo tiene ciclo de vida y soporte del fabricante; documentar end-of-life, actualización, recuperación, inventario y propietario.

## Capacidades básicas
NISTIR 8259A define una línea base de capacidades técnicas: identificación del dispositivo, configuración, protección de datos, control lógico de interfaces, actualización de software, awareness del estado de ciberseguridad y protección del dispositivo. NISTIR 8259B cubre capacidades no técnicas del fabricante, como documentación, recepción de consultas, divulgación y educación. NISTIR 8259 Rev. 1 (2026) actualiza actividades fundacionales para fabricantes.

## Interfaces y amenazas
UART/JTAG/SWD, USB, BLE, Wi-Fi, Zigbee/Thread, NFC, cellular, Ethernet, debug ports, boot mode, OTA update, default credentials, insecure pairing, weak RNG, hardcoded secrets, insecure storage, supply chain, physical tampering y cloud API. La seguridad física puede ser parte del modelo, pero no asumir que el dispositivo es invulnerable a acceso físico.

## Firmware y actualización
Secure boot, measured boot, signed update, rollback protection, A/B updates, recovery, key provisioning, debug lock, SBOM, vulnerability disclosure y soporte de parches. Validar firma, versión, anti-rollback, recuperación ante corte de energía y continuidad. No actualizar equipos en servicio crítico sin pruebas y ventana aprobada.

## Evaluación
Inventario de modelo/firmware, documentación de soporte, interfaces expuestas, credenciales, protocolos, certificados, update mechanism, permisos, privacidad, logs y comportamiento ante fallo. Usar instrumentación no destructiva y autorización explícita.

## Laboratorios
Placa de desarrollo de bajo costo, firmware propio, emulador, UART/JTAG de prueba, OTA firmado y backend mock. Evaluar secure boot/update, credenciales, interfaces y restore. No conectar radios o dispositivos experimentales a redes ajenas.

## Fuentes
- NISTIR 8259A: https://doi.org/10.6028/NIST.IR.8259A
- NISTIR 8259B: https://doi.org/10.6028/NIST.IR.8259B
- NISTIR 8259 Series (incluye Rev. 1 de 2026): https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program/nistir-8259-series
- NIST SP 800-193 Firmware Resiliency: https://doi.org/10.6028/NIST.SP.800-193

**Límite:** no se inspeccionó hardware ni firmware; los controles dependen de fabricante, chip, boot chain y modelo de soporte.
