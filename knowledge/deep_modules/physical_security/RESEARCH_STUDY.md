# Investigación técnica: Seguridad física y sistemas ciberfísicos

**ID:** physical_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Evaluación de instalaciones pendiente.

## Modelo
La seguridad física protege personas, instalaciones, equipos, soportes, energía, refrigeración, cableado y medios de almacenamiento. Conectar modelo físico y lógico: perímetro, zonas, control de acceso, visitantes, guardias, CCTV, sensores, alarmas, HVAC, BMS, control de puertas, racks y salas técnicas.

## Riesgos
Tailgating, badge cloning, credential sharing, tampering, theft, rogue devices, cable tapping, power disruption, environmental failure, insider threat, camera blind spots y compromiso de sistemas de control físico. Las cámaras y logs también contienen datos personales y requieren política de privacidad/retención.

## Controles
Zonificación por criticidad, acceso por rol/tiempo, MFA o doble control para áreas críticas, visitor escort, anti-tailgating donde proceda, logging, alarmas, protección de racks, secure disposal, energía redundante, environmental monitoring, tamper evidence y respuesta ante pérdida de energía/conectividad. Probar fail-safe/fail-secure en conjunto con safety y evacuación.

## Integración ciberfísica
BMS/ACS/CCTV deben tener inventario, segmentación, credenciales únicas, firmware soportado, actualización, logging, backups y acceso remoto mediado. No conectar control de acceso o CCTV a red corporativa sin threat model y segmentación.

## Laboratorios
Modelo de acceso con credenciales sintéticas, eventos de puerta, alarmas, cámara simulada y failover. Validar permisos, logs, revocación, retención, acceso de emergencia y recuperación. Pruebas físicas requieren autorización y supervisión de seguridad.

## Fuentes
- NIST SP 800-53 Rev. 5, familias Physical and Environmental Protection: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-82 Rev. 3 OT Security: https://doi.org/10.6028/NIST.SP.800-82r3
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29

**Límite:** normas de seguridad física y building codes dependen de jurisdicción y sector.
