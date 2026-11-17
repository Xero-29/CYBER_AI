# Revisión de literatura inicial — Arquitectura segura y Zero Trust

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta

¿Cómo diseñar una arquitectura que aplique decisiones de acceso explícitas a sujetos, dispositivos y recursos, manteniendo trazabilidad, disponibilidad y control de riesgo?

## Síntesis

NIST SP 800-207 (2020) describe Zero Trust como un cambio desde perímetros estáticos hacia protección de usuarios, activos, servicios y recursos. No concede confianza implícita por ubicación de red o propiedad del dispositivo; autenticación y autorización de sujeto/dispositivo se realizan antes de establecer la sesión. Esto no significa «eliminar la red» ni instalar un producto ZTNA: es un modelo arquitectónico que requiere identidad, contexto, políticas, telemetría y puntos de aplicación.

El borrador NIST SP 800-82 Rev. 4 de 2026 incluye orientación de arquitectura OT centrada en proteger funciones de gestión y aplicar principios Zero Trust; para OT deben conservarse restricciones de seguridad funcional y disponibilidad.

## Componentes y controles a evaluar

- Plano de control de políticas: autoridad, reglas versionadas, evaluación y auditoría.
- Puntos de decisión/aplicación: enforcement en recursos y sesiones.
- Identidad de usuario, workload y dispositivo; ciclo de vida y revocación.
- Contexto: postura, sensibilidad del recurso, riesgo y señales de telemetría.
- Segmentación como defensa complementaria, no sustituto de autorización por recurso.
- Acceso privilegiado temporal, just-in-time y separación de funciones.
- Observabilidad de decisiones, fallos de política y degradación ante pérdida del plano de control.

## Hipótesis / protocolo (no ejecutado)

H1: una política contextual por recurso detecta y bloquea más accesos indebidos en escenarios de identidad comprometida que un control basado solo en ubicación de red. H0: no hay diferencia medible.

Banco sintético: dos aplicaciones, usuarios, dispositivos gestionados/no gestionados, recursos de distinta sensibilidad y proveedor de identidad de pruebas. Comparar perímetro/VPN simple, control por identidad y política contextual por recurso. Medir accesos no autorizados aceptados, falsos rechazos, latencia p95, disponibilidad ante fallo del PDP, tiempo de revocación y calidad de auditoría. Repetir con pérdida de señal, dispositivo obsoleto y token robado simulado. No usar credenciales reales.

## Limitaciones

SP 800-207 es una arquitectura de referencia de alto nivel, no receta universal ni certificación. El resultado depende de cobertura de identidad, integridad del dispositivo, enforcement real y calidad de políticas. No inferir Zero Trust por tener MFA o microsegmentación.

## Fuentes

- NIST SP 800-207, Zero Trust Architecture (2020): https://doi.org/10.6028/NIST.SP.800-207
- NIST SP 800-82 Rev. 4 initial public draft (2026): https://csrc.nist.gov/pubs/sp/800/82/r4/ipd
\n\n## Identificadores del registro de fuentes\n\n- `NIST-SP-800-207`\n- `NIST-SP-800-82r4-IPD`\n