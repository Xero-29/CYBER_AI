# Investigación técnica: Seguridad de hardware, firmware y sistemas embebidos

**ID:** hardware_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Evaluación física de laboratorio pendiente.

## Root of trust
Modelar silicon, boot ROM, immutable root, firmware, bootloader, TPM/secure element, debug, memory, bus, DMA, peripherals, supply chain, manufacturing and update. Evaluar root of trust, measured boot, secure boot, attestation, anti-rollback, key storage, recovery y physical tampering.

## Amenazas
Firmware persistence, malicious peripherals, DMA attacks, debug port abuse, fault injection, voltage/clock glitching, side-channel leakage, supply-chain tampering, counterfeit components, insecure boot, firmware downgrade, insecure update y key extraction. Distinguir laboratorio invasivo de riesgo remoto.

## Resiliencia de firmware
NIST SP 800-193 organiza protección, detección y recuperación ante cambios no autorizados del firmware. Implementar signed update, protected recovery, anti-rollback, authenticated boot, secure configuration, hardware root of trust y recovery path independiente. Verificar proceso de fabricación y provisioning.

## Criptografía y hardware
TPM, HSM, secure element, key ladder, entropy source, PUF y hardware accelerators. Evaluar certificación, lifecycle, debug policy, tamper response y key zeroization. FIPS 140-3 aplica a módulos criptográficos bajo su alcance, no certifica dispositivo completo.

## Laboratorios
Development boards, QEMU/firmware emulator, UART/JTAG own devices, signed firmware update, secure boot test, debug lockdown, fault injection safe setup y measurement. No usar glitching/laser en equipos ajenos ni en hardware conectado a infraestructura crítica.

## Fuentes
- NIST SP 800-193: https://doi.org/10.6028/NIST.SP.800-193
- NIST FIPS 140-3: https://doi.org/10.6028/NIST.FIPS.140-3
- NISTIR 8259A: https://doi.org/10.6028/NIST.IR.8259A
- NIST SP 800-147 BIOS Protection Guidelines: https://csrc.nist.gov/pubs/sp/800/147/final

**Límite:** controles dependen de silicon/OEM/board revision y amenaza física; pruebas requieren laboratorio y equipo propio.
