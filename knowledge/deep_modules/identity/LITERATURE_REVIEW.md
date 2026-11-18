# Revisión de literatura inicial — Identidad y acceso

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta
¿Cómo establecer niveles de confianza apropiados en identidad digital, autenticación y federación sin equiparar MFA con seguridad completa?

## Síntesis primaria
NIST SP 800-63-4 (final, julio de 2025) reemplaza SP 800-63-3 y separa identidad digital en prueba de identidad/enrolamiento (63A-4), autenticación y gestión de autenticadores (63B-4), y federación/assertions (63C-4). La selección de controles debe derivarse del riesgo y del nivel de garantía requerido, no de una preferencia de producto. La federación añade confianza entre proveedor de identidad y relying parties; validación de issuer, audience, firma, expiración, nonce/state y ciclo de vida de claves son superficies independientes.

## Modelo de amenazas
Suplantación durante prueba de identidad; enrolamiento fraudulento; robo/reutilización de autenticadores; phishing; recuperación débil; sesión/token robado; errores de federación; cuentas huérfanas; privilegios persistentes; compromiso de IdP o de claves de firma.

## Hipótesis y experimento (no ejecutado)
H1: un proceso de alta, recuperación y baja que verifica el ciclo completo del autenticador reduce cuentas recuperadas indebidamente frente a controles limitados al login. H0: sin diferencia.
Banco: IdP de laboratorio, dos aplicaciones relying party, identidades sintéticas y escenarios de phishing simulado, token expirado/revocado, cambio de dispositivo, recovery y firma inválida. Métricas: tasa de aceptación indebida, falsos rechazos, tiempo de revocación, cobertura de eventos de ciclo de vida, latencia y trazabilidad. No utilizar identidades reales.

## Brechas
Leer SP 800-63-4 y sus tres volúmenes completos; mapear OIDC/OAuth2/SAML a requisitos concretos; ensayar recuperación y revocación en un IdP real de pruebas; revisar privacidad y accesibilidad del proceso de identidad.

## Fuentes
- NIST SP 800-63-4 (2025): https://doi.org/10.6028/NIST.SP.800-63-4
- NIST SP 800-63B-4 (2025): https://doi.org/10.6028/NIST.SP.800-63b-4
- NIST SP 800-63C-4 (2025): https://doi.org/10.6028/NIST.SP.800-63c-4

## Identificadores del registro de fuentes
- `NIST-SP-800-63-4`
- `NIST-SP-800-63B-4`
- `NIST-SP-800-63C-4`


## Identificadores del registro de fuentes

- `NIST-SP-800-63-4`
- `NIST-SP-800-63B-4`
- `NIST-SP-800-63C-4`
