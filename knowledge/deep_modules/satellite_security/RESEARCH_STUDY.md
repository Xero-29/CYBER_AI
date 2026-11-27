# Investigación técnica: Seguridad de satélites y sistemas espaciales

**ID:** satellite_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Revisión sectorial y safety pendiente.

## Arquitectura
Modelar segmento espacial (satélite, payload, bus, avionics, firmware), segmento terrestre (mission control, gateways, ground stations), enlaces RF/ópticos, operadores, proveedores, usuarios y cadena de mando. Identificar uplink/downlink, TT&C, payload data, GNSS, timing, key provisioning, update paths y crosslinks.

## Amenazas
Jamming, spoofing, command injection, replay, key compromise, ground station compromise, supply chain, firmware tampering, physical access, RF exposure, denial of service, orbital debris/availability dependencies y insider. Diferenciar amenaza cibernética, interferencia intencional, fallo físico y riesgo operacional.

## Controles
Autenticación fuerte de comandos, anti-replay, key lifecycle, command authorization, cryptographic agility, secure boot/update, segmentation, ground station hardening, telemetry anomaly detection, secure time, least privilege, offline recovery, key escrow policy y incident response coordinado. Diseñar modos seguros ante pérdida de enlace y limitar comandos críticos por estado del vehículo.

## Operación y safety
Simular antes de pruebas RF; coordinar frecuencia/licencia y autoridad. Las acciones de respuesta deben considerar dinámica orbital, ventana de contacto, energía, thermal, attitude control y safety. No enviar comandos a activos reales sin autorización operacional expresa.

## Laboratorios
Emulador de enlace, telemetría sintética, command protocol mock, key rotation, replay test, loss-of-link recovery y ground station virtual. Medir command authentication, latency, availability, recovery, false alarm y crypto resource overhead.

## Fuentes
- CCSDS Publications: https://ccsds.org/publications/
- CCSDS Reference Architecture for Space Data Systems: https://ccsds.org/Pubs/311x0m2.pdf
- NIST SP 800-193 Firmware Resiliency: https://doi.org/10.6028/NIST.SP.800-193
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29

**Límite:** los estándares espaciales y perfiles de misión son específicos; validar edición, licencia, misión y regulación RF.
