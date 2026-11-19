# Investigación técnica: Criptografía poscuántica y migración criptográfica

**ID:** post_quantum_crypto · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas interoperables pendientes.

## Amenaza y horizonte
El riesgo harvest-now-decrypt-later afecta información capturada hoy cuya confidencialidad debe durar años. La prioridad depende de vida útil, sensibilidad, exposición y horizonte de migración, no de una fecha especulativa única de llegada de computadores cuánticos.

## Estándares NIST
FIPS 203 define ML-KEM para establecimiento de secreto compartido; FIPS 204 define ML-DSA; FIPS 205 define SLH-DSA. Revisar erratas/potential updates de NIST para FIPS 203/204. No tratar algoritmos en selección o drafts como estándares finales.

## Matemáticas y límites
Comprender Module-LWE, lattices, hash-based signatures, parameter sets, failure probability, key/signature sizes, randomness, side channels, chosen-ciphertext security y implementation leakage. No inferir seguridad solo por complejidad de problema ni por tamaño de clave.

## Migración
1. Inventariar certificados, protocolos, HSM, firmware, libraries, data archives y dependencies.
2. Clasificar confidentiality lifetime y harvest-now-decrypt-later.
3. Identificar cryptographic agility y sistemas legacy.
4. Diseñar perfiles de transición con estándares y protocolos compatibles.
5. Medir tamaño, handshake latency, CPU, memory, bandwidth y MTU.
6. Validar interoperabilidad, downgrade resistance, key lifecycle y fallback.
7. Planear rollback y crypto inventory updates.

## Laboratorios
Implementaciones verificadas de ML-KEM/ML-DSA/SLH-DSA, vectors, interoperability harness, TLS/PKI prototypes y performance on constrained devices. No diseñar esquemas híbridos propios ni usar algoritmos experimentales en producción.

## Fuentes
- NIST FIPS 203: https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204: https://csrc.nist.gov/pubs/fips/204/final
- NIST FIPS 205: https://csrc.nist.gov/pubs/fips/205/final
- NIST SP 800-131A Rev. 2: https://doi.org/10.6028/NIST.SP.800-131Ar2
- NIST SP 800-57: https://doi.org/10.6028/NIST.SP.800-57pt1r5

**Límite:** fijar implementaciones, parámetros, erratas y perfiles; los microbenchmarks no prueban seguridad.


## Actualización de hoja de ruta de migración — NIST IR 8547 (2026-10-27)
NIST publicó IR 8547 Final el 27 de octubre de 2026. El documento establece la hoja de ruta oficial para transición desde algoritmos vulnerables a computación cuántica hacia estándares PQC, identificando algoritmos afectados y estándares de destino. La biblioteca debe tratarlo como referencia central de planificación, no inferir fechas de migración de cada activo sin inventario y análisis de criticidad.

### Requisitos que faltaban en el currículo operativo
- Inventario criptográfico automatizable (algoritmo, tamaño/parámetro, biblioteca, protocolo, certificado, propietario, ubicación, uso, fecha de expiración y dependencia).
- Clasificación por vida útil de confidencialidad, sensibilidad y exposición a captura; priorizar riesgo HNDL.
- Mapa de dependencias criptográficas y terceros (PKI, HSM, firmware, appliances, SaaS, backups y archivos históricos).
- Política de cripto-agilidad: negociación de algoritmos, perfiles permitidos, desactivación de algoritmos heredados, actualización de certificados y pruebas de downgrade.
- Plan de transición con hitos, responsables, criterios de salida, excepciones, compensaciones y rollback.
- Ensayos de interoperabilidad híbrida y de rendimiento en MTU, latencia, CPU, memoria, tamaño de certificados/firmas y dispositivos restringidos.
- Gobernanza del riesgo de algoritmos legado y gestión de excepciones con fecha de caducidad.

### Evidencia y límites
- NIST IR 8547 Final: https://doi.org/10.6028/NIST.IR.8547
- Ficha de publicación: https://csrc.nist.gov/pubs/ir/8547/final
La ficha oficial y el resumen fueron revisados; el informe completo y sus hitos deben extraerse y revisarse antes de crear una política de fechas. No se ejecutaron pruebas de interoperabilidad.
