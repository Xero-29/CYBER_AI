# Investigación técnica: Arquitectura segura y modelado de amenazas

**ID:** secure_arch · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 · **Revisión arquitectónica externa:** pendiente.

## Principios y método
La arquitectura segura comienza por activos, objetivos, contexto y límites de confianza. No se reduce a checklist. Documentar componentes, identidades, datos, flujos, estados, dependencias, interfaces, administradores, proveedores y rutas de actualización.

Aplicar mínimo privilegio, deny-by-default, separación de funciones, defensa en profundidad, fail-safe defaults, secure by design, reducción de superficie, aislamiento, verificabilidad, recuperación y privacidad por diseño. Registrar trade-offs y riesgo residual.

## Modelado de amenazas
1. Definir sistema, contexto, alcance y objetivos de seguridad.
2. Descomponer arquitectura y flujos de datos.
3. Identificar activos, actores, trust boundaries y superficies.
4. Enumerar amenazas mediante STRIDE, attack trees, misuse cases, PASTA u otra técnica adecuada.
5. Estimar riesgo con impacto, probabilidad, exposición, controles y supuestos.
6. Elegir mitigación, aceptación o transferencia con owner y fecha.
7. Definir pruebas que puedan refutar que el control funciona.
8. Actualizar el modelo cuando cambie arquitectura, proveedor, dependencia o amenaza.

STRIDE ayuda a enumerar spoofing, tampering, repudiation, information disclosure, denial of service y elevation of privilege; no es una métrica de riesgo ni prueba de exhaustividad. Combinar métodos según contexto.

## Zero Trust
NIST SP 800-207 enfatiza proteger recursos y no conceder confianza implícita por ubicación de red o propiedad del dispositivo. Una arquitectura debe separar policy engine, policy administrator y policy enforcement points, además de fuentes de identidad, postura del dispositivo, contexto, telemetría y recursos.

Implementación: inventariar identidades humanas/workloads/dispositivos/recursos; definir políticas por recurso, acción y contexto; autenticar y autorizar explícitamente; aplicar MFA, device posture, segmentación y credenciales cortas; registrar decisiones; reevaluar ante cambios de contexto; mantener modo degradado seguro y recuperación ante fallo del IdP. Zero Trust no es un producto ni implica microsegmentar todo inmediatamente.

## Requisitos verificables
Cada requisito incluye ID, activo, amenaza, objetivo, riesgo, componente responsable, mecanismo preventivo/detectivo/recuperación, prueba positiva y negativa, evidencia, métrica, owner, fecha, riesgo residual y excepción.

Ejemplo: “identidad A no puede leer datos del tenant B” debe probarse en API, query layer, caché, index, logs y backup; no basta ocultar registros en UI.

## Patrones y anti-patrones
Patrones: API gateway con identidad end-to-end; control plane separado de data plane; secret broker; workload identity; immutable artifacts; queues idempotentes; tenant isolation por capa; audit log protegido; circuit breaker; staged rollout; break-glass con revisión.

Anti-patrones: confiar en red interna; confiar en prompt para autorización; cuenta admin compartida; panel de gestión expuesto; secretos en logs; fail-open por disponibilidad; controles sin propietario; excepciones permanentes; aceptar un escaneo como prueba completa.

## Validación y métricas
Cobertura de activos/interfaces/flujos modelados; amenazas con mitigación, owner y prueba; pruebas negativas de aislamiento/ACL; tiempo de revocación; trust boundaries sin enforcement; riesgo residual aceptado y expiración de excepciones; regresiones arquitectónicas y drift.

## Fuentes
- NIST SP 800-207 Zero Trust: https://doi.org/10.6028/NIST.SP.800-207
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- OWASP Threat Modeling: https://owasp.org/www-project-threat-modeling/
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1

**Estado de evidencia:** se revisaron páginas oficiales y abstracts de NIST/CIS; la arquitectura debe adaptarse al sistema real y no se declara certificada ni revisada por tercero.
