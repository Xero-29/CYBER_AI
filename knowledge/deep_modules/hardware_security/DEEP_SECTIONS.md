# Secciones de profundización — Seguridad de hardware

## Modelo de amenazas
Analizar silicio, firmware, boot chain, ROM, TPM/TEE, buses, interfaces debug, memoria, sensores, cadena de fabricación y aprovisionamiento. Amenazas: root of trust comprometida, firmware malicioso, fault injection, side channels, manipulación física, counterfeits, supply chain y extracción de secretos. Diferenciar capacidades del diseño y garantías efectivamente evaluadas.

## Detección
Verificar mediciones de boot, attestation, hashes de firmware, estado de debug, cambios de configuración, inventario de componentes y señales físicas disponibles. Detectar firmware fuera de baseline, identidad duplicada, arranque no medido y cambios en cadena de suministro. La telemetría no detecta todos los ataques físicos; declarar límites de observabilidad.

## Respuesta a incidentes
Aislar unidades afectadas, preservar firmware y logs de attestation, revocar certificados/identidades, detener aprovisionamiento y coordinar con fabricante. Evaluar exposición de claves y posibilidad de reflash seguro; reemplazar hardware cuando la raíz de confianza no sea recuperable. Mantener trazabilidad de lote, revisión y componente.

## Casos prácticos
En placa de desarrollo, verificar secure boot y medición de firmware; probar que una imagen no firmada se rechaza y que el modo debug está bloqueado en perfil de producción. Simular firmware alterado y documentar detección, recuperación y límites de attestation.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-193, TPM 2.0, TCG, Arm PSA y documentación del fabricante. No extrapolar resultados de una placa a todo un lote.
