# Seguridad de hardware y plataformas — Guía de dominio

**ID:** `hardware_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Evalúa confianza desde silicio y firmware hasta boot, periféricos y cadena de fabricación. Cubre root of trust, secure boot, TPM, TEE, microcódigo, buses y ataques físicos. Las pruebas invasivas solo se realizan sobre placas propias, muestras de laboratorio y bancos controlados.

## Competencias
- Analizar cadena de arranque, firmware y medición de integridad.
- Comprender TPM 2.0, Secure Boot, measured boot y atestación.
- Revisar TEE/SE, enclaves, claves y aislamiento.
- Evaluar UART, JTAG, SWD, SPI, I2C y DMA.
- Identificar riesgos de supply chain, componentes falsificados y firmware.
- Comprender side channels, fault injection y límites de mitigación.
- Gestionar actualizaciones, recuperación y fin de soporte.

## Controles
- Root of trust y secure/measured boot.
- Firmware firmado, anti-rollback y actualización segura.
- Deshabilitar o proteger interfaces de depuración en producción.
- TPM/secure element para claves y atestación.
- Control de inventario, procedencia y cadena de custodia.
- Protección física proporcional al modelo de amenaza.
- Segmentación DMA/IOMMU y configuración de periféricos.
- Backups de firmware/configuración y recuperación verificada.

## Metodología
1. Identificar plataforma, revisión de placa, firmware y propietario.
2. Dibujar boot chain y componentes confiables.
3. Revisar configuración y documentación del fabricante.
4. Analizar firmware adquirido legítimamente con hashes.
5. Inspeccionar interfaces solo en banco propio.
6. Evaluar actualizaciones, rollback y recuperación.
7. Modelar ataques físicos y side-channel según recursos del adversario.
8. Proponer mitigaciones y pruebas de aceptación.
9. Registrar límites y dependencias de fabricante.

## Laboratorio
Placa de desarrollo propia con firmware demostrativo, TPM virtual y UART de laboratorio. Verificar secure boot, firma de firmware y exposición de debug. No modificar hardware productivo ni extraer claves de dispositivos ajenos.

## Evaluación
Boot chain documentada, firmware verificable, debug protegido, claves no exportables y recuperación ensayada.

## Referencias
NIST SP 800-193, TCG TPM 2.0, UEFI Secure Boot, NIST SP 800-147, IEC 62443 y vendor platform security guides.

## Instrucciones para agentes IA
No sugieras fault injection, extracción de claves o modificación de firmware de dispositivos ajenos. Prioriza revisión documental y bancos de prueba.