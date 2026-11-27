# Investigación técnica: Ciberseguridad automotriz y redes vehiculares

**ID:** automotive_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de vehículo/banco HIL pendiente.

## Modelo
Vehículo conectado: ECUs, gateways, CAN/CAN-FD, LIN, FlexRay, Automotive Ethernet, infotainment, telematics, ADAS, sensors, actuators, OTA, backend, mobile app, charging, V2X y supply chain. Analizar safety, availability, timing, integrity, privacy y lifecycle.

## Estándares y regulación
ISO/SAE 21434:2021 cubre cybersecurity engineering del ciclo de vida E/E; ISO ha aprobado un work item de segunda edición en desarrollo durante 2026, por lo que no presentarlo como final. UNECE UN R155 establece requisitos de Cybersecurity Management System para aprobación de tipo; R156 aborda software updates. Revisar texto y modificaciones oficiales aplicables al país/mercado.

## Amenazas
CAN spoofing/injection, diagnostic abuse, ECU compromise, gateway bypass, key theft, OTA compromise, supply chain, telematics API, GNSS spoofing, V2X abuse, charging infrastructure, physical port access y privacy leakage. Un ID CAN no equivale a autenticación criptográfica del emisor.

## Controles
Secure boot, HSM, key provisioning, message authentication donde soporte, segmentation gateways, IDS vehicular, secure diagnostics, OTA signing, rollback protection, SBOM, vulnerability management, incident response y safety engineering. Diseñar degradación segura y validación HIL antes de despliegue.

## Laboratorios
CAN simulator, ECU dev board, gateway mock, OTA update server, HIL bench y traffic dataset sintético. Probar replay, message spoofing, diagnostic access, key rotation, update tampering y recovery. No conectar herramientas de prueba a vehículo en movimiento ni sistemas safety-critical sin autorización.

## Fuentes
- ISO/SAE 21434:2021: https://www.iso.org/standard/70918.html
- ISO/SAE 21434 Edition 2 work item: https://www.iso.org/es/contents/data/standard/09/54/95437.html
- UNECE UN Regulation No. 155: https://treaties.un.org/Pages/ViewDetails.aspx?chapter=11&clang=_en&mtdsg_no=XI-B-16-155&src=TREATY
- NIST SP 800-193: https://doi.org/10.6028/NIST.SP.800-193

**Límite:** safety, type approval y regulación dependen de mercado y OEM; requiere especialistas de automoción y seguridad funcional.
