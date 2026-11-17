# Revisión de literatura inicial — Criptografía y migración poscuántica

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta

¿Cómo inventariar y migrar dependencias criptográficas a estándares poscuánticos sin introducir incompatibilidades, downgrade, pérdida de interoperabilidad o falsas garantías?

## Evidencia primaria

NIST publicó en agosto de 2024 tres estándares FIPS principales:
- **FIPS 203 / ML-KEM:** mecanismo de encapsulación de claves para establecer un secreto compartido.
- **FIPS 204 / ML-DSA:** firmas digitales basadas en retículos.
- **FIPS 205 / SLH-DSA:** firmas digitales basadas en hashes y sin estado.

NIST indica que las organizaciones deben identificar dónde usan algoritmos vulnerables y planificar la sustitución. El proyecto NIST también mantiene trabajo de estandarización adicional; no asumir que el conjunto de algoritmos futuros está cerrado. La página oficial consultada menciona FIPS 206 en desarrollo para FALCON y selección de HQC para estandarización (marzo de 2025).

## Estrategia de migración

1. Inventariar algoritmos, tamaños de clave, certificados, protocolos, bibliotecas, HSM/KMS, firmware, backups y datos cifrados a largo plazo.
2. Clasificar por confidencialidad requerida, vida útil de datos, exposición, criticidad e interoperabilidad.
3. Distinguir intercambio/encapsulación de claves de firma digital: ML-KEM no sustituye firmas; ML-DSA/SLH-DSA no son KEM.
4. Probar compatibilidad de extremo a extremo, tamaño de mensajes, rendimiento, latencia, consumo, límites de certificados y renovación.
5. Evaluar modos híbridos solo cuando la especificación/protocolo los defina y exista interoperabilidad; no improvisar concatenaciones criptográficas.
6. Planificar crypto-agility: identificadores de algoritmo, negociación segura, actualización, rollback controlado y telemetría.
7. Validar implementaciones y módulos según requisitos aplicables; un benchmark no demuestra seguridad criptográfica.

## Hipótesis y protocolo (no ejecutado)

H1: una migración guiada por inventario de dependencias y pruebas de interoperabilidad reduce fallos de despliegue frente a reemplazo aislado de algoritmos. H0: no hay diferencia.

Banco: dos servicios de prueba, certificados sintéticos, implementaciones compatibles con FIPS y versiones fijadas. Comparar flujo clásico, PQC y modo híbrido estandarizado disponible. Métricas: handshake success, latencia p50/p95, bytes transmitidos, CPU/memoria, tamaño de certificado, fallos de negociación, compatibilidad entre implementaciones y recuperación/rollback. Repetir en hardware declarado. No realizar afirmaciones de resistencia formal basadas solo en rendimiento.

## Fuentes

- NIST Post-Quantum Cryptography project: https://csrc.nist.gov/Projects/Post-Quantum-Cryptography
- FIPS 203: https://doi.org/10.6028/NIST.FIPS.203
- FIPS 204: https://doi.org/10.6028/NIST.FIPS.204
- FIPS 205: https://doi.org/10.6028/NIST.FIPS.205
- NIST IR 8547, transición poscuántica (referencia para revisión completa): https://csrc.nist.gov/pubs/ir/8547/ipd

## Brechas

Revisar los estándares FIPS completos, sus erratas y requisitos de validación; estudiar protocolos TLS/PKI y perfiles de transición; ejecutar pruebas cruzadas en implementaciones reales y revisión criptográfica independiente.
