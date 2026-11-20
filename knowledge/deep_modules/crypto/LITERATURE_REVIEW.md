# Revisión de literatura — Criptografía aplicada

**Corte:** 2026-11-19  
**Estado:** revisión documental inicial de metadatos y alcance oficial; no revisión sistemática ni lectura integral de todas las fuentes.  
**Madurez:** M2 editorial; no M3/M4/M5: fuentes integrales, experimentos y revisión independiente pendientes.

## Pregunta

¿Cómo preservar las garantías de confidencialidad, integridad y autenticidad al integrar primitivas, protocolos y gestión de claves en sistemas de software y hardware, considerando errores de implementación, cambios de estándares y transición poscuántica?

Se cubren: generación aleatoria, hashes, MAC, KDF, password hashing, cifrado simétrico y AEAD, firmas, intercambio de claves/KEM, TLS/SSH/IPsec, PKI, gestión de claves, módulos criptográficos, side channels y criptoagilidad.

## 2. Método y límites de la revisión

Se consultaron registros y páginas oficiales NIST y RFC Editor para verificar identificación, alcance, estado y avisos de revisión de documentos. Se registraron URLs canónicas e IDs en `knowledge/research/source_registry.json`. Esta revisión no equivale a:
- lectura integral de cada documento;
- revisión sistemática con doble cribado;
- evaluación de todas las implementaciones;
- validación FIPS de un producto;
- experimento ejecutado ni reproducción externa.

Las fuentes normativas deben leerse en su edición y erratas vigentes antes de derivar requisitos de producción.

## Síntesis

### 3.1 Aleatoriedad y entropía

La serie NIST SP 800-90 separa tres problemas: mecanismos deterministas DRBG (SP 800-90A), fuentes de entropía y health tests (SP 800-90B), y construcciones completas RBG (SP 800-90C). SP 800-90C fue publicada como final el 25 de septiembre de 2025. El catálogo NIST muestra SP 800-90A Rev. 2 como borrador/pre-draft en 2025, mientras Rev. 1 sigue siendo la versión final listada. Esto obliga a registrar el estado exacto y no citar un borrador como estándar final.

Implicación técnica: la seguridad de la salida depende del seed material, estimación de entropía, conditioning, DRBG, reseed y estado operativo. Las pruebas de frecuencia o uniformidad no demuestran por sí solas impredecibilidad ni entropía suficiente. El compendio exige pruebas de fork/snapshot, arranque, fallo de fuente y reseed.

### 3.2 Primitivas, contraseñas y firmas

La selección de primitivas debe considerar propiedades diferentes: resistencia a preimagen/colisión de hashes, autenticación de MAC, separación de contexto en KDF, resistencia a fuerza bruta de password hashing y validación de firmas. HKDF (RFC 5869) es una KDF extract-and-expand; Argon2 (RFC 9106) especifica una función memory-hard para hashing de contraseñas. EdDSA está descrita en RFC 8032. Las propiedades de algoritmo no sustituyen encoding canónico, validación, protección de claves y manejo correcto de errores.

### 3.3 Cifrado simétrico y AEAD

FIPS 197 define AES; la actualización de 2023 fue editorial y NIST indicó que no modificó técnicamente el algoritmo. Los modos de operación tienen requisitos distintos de IV/nonce y autenticación. RFC 8439 especifica ChaCha20 y Poly1305 para protocolos IETF. La reutilización de nonce en construcciones AEAD como GCM puede comprometer confidencialidad e integridad; los wrappers deben garantizar unicidad, fallar cerrado y no liberar plaintext no autenticado. Los vectores conocidos deben complementarse con pruebas negativas y límites.

### 3.4 Establecimiento de claves y KEM

NIST SP 800-56A Rev. 3 cubre establecimiento de claves sobre logaritmo discreto, incluyendo DH y curvas elípticas. El 6 de enero de 2026 NIST anunció que actualizará esta publicación; los perfiles que la utilicen deben comprobar el proceso de revisión.

FIPS 203 especifica ML-KEM con parámetros 512, 768 y 1024. La página NIST consultada contiene una nota del 17 de noviembre de 2025 sobre un problema identificado que será corregido en una actualización/revisión. Esto es un aviso de mantenimiento que debe rastrearse; no permite inferir por sí solo el impacto en una implementación concreta. FIPS 204 y 205 definen ML-DSA y SLH-DSA. KEM y firmas resuelven problemas distintos y no son intercambiables.

### 3.5 Protocolos y composición

RFC 8446 especifica TLS 1.3. Su key schedule, transcript binding y autenticación de pares deben analizarse como un protocolo completo, no como una lista de algoritmos. 0-RTT puede ser replayable; la aplicación debe restringirlo según semántica de operaciones. HPKE (RFC 9180) define composición de KEM, KDF y AEAD con modos establecidos; no autoriza improvisar protocolos ni concatenar secretos sin análisis.

### 3.6 Gestión de claves y assurance

La gestión cubre generación, distribución, activación, almacenamiento, uso, rotación, revocación, backup, recuperación y destrucción. La certificación de un módulo criptográfico, la validación de un algoritmo, la revisión de código y la configuración correcta de un despliegue son niveles de evidencia diferentes. HSM/KMS no eliminan errores de autorización, exposición de plaintext, recuperación deficiente ni abuso de identidades.

## 4. Cambios de estado y alertas normativas que deben rastrearse

- **SP 800-90C:** final, septiembre de 2025; incluir en los diseños actuales de arquitectura RBG.
- **SP 800-90A Rev. 2:** borrador/pre-draft en el catálogo consultado; no presentarlo como final.
- **SP 800-56A Rev. 3:** NIST anunció actualización el 6 de enero de 2026.
- **FIPS 203:** NIST publicó nota el 17 de noviembre de 2025 sobre un problema que será corregido en una actualización/revisión; revisar hoja de erratas vigente.
- **FIPS 197:** actualización editorial de mayo de 2023, sin cambios técnicos declarados.
- **FIPS 204/205:** estándares finales publicados en agosto de 2024; mantener vigilancia de erratas y guías de implementación.

## 5. Preguntas abiertas

1. ¿Qué mecanismos de detección identifican fallos de nonce y de estado DRBG sin generar falsos positivos inaceptables?
2. ¿Cómo comparar configuraciones de password hashing con presupuestos de CPU/memoria y amenazas de hardware diferentes?
3. ¿Qué controles evitan errores de validación y oráculos en wrappers de KEM?
4. ¿Qué impacto medible tiene PQC en certificados, handshake, firmware, HSM, ancho de banda y latencia en distintos entornos?
5. ¿Qué arquitectura de rotación minimiza exposición y riesgo de indisponibilidad en sistemas distribuidos?
6. ¿Qué métodos de evaluación de side channels son reproducibles y comparables entre hardware?

## 6. Fuentes primarias registradas

- [NIST SP 800-90A Rev. 1](https://doi.org/10.6028/NIST.SP.800-90Ar1) — DRBG.
- [NIST SP 800-90B](https://doi.org/10.6028/NIST.SP.800-90B) — fuentes de entropía.
- [NIST SP 800-90C](https://doi.org/10.6028/NIST.SP.800-90C) — construcciones RBG.
- [FIPS 197](https://doi.org/10.6028/NIST.FIPS.197) — AES.
- [NIST SP 800-56A Rev. 3](https://doi.org/10.6028/NIST.SP.800-56Ar3) — establecimiento de claves.
- [NIST SP 800-57 Part 1 Rev. 5](https://doi.org/10.6028/NIST.SP.800-57pt1r5) — gestión de claves.
- [FIPS 203](https://doi.org/10.6028/NIST.FIPS.203) — ML-KEM.
- [FIPS 204](https://doi.org/10.6028/NIST.FIPS.204) — ML-DSA.
- [FIPS 205](https://doi.org/10.6028/NIST.FIPS.205) — SLH-DSA.
- [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869) — HKDF.
- [RFC 8439](https://www.rfc-editor.org/rfc/rfc8439) — ChaCha20-Poly1305.
- [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) — TLS 1.3.
- [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106) — Argon2.
- [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032) — EdDSA.
- [RFC 9180](https://www.rfc-editor.org/rfc/rfc9180) — HPKE.

IDs de registro: `NIST-SP-800-90A-r1`, `NIST-SP-800-90B`, `NIST-SP-800-90C`, `NIST-FIPS-197`, `NIST-SP-800-56A-r3`, `NIST-SP-800-57p1r5`, `NIST-FIPS-203`, `NIST-FIPS-204`, `NIST-FIPS-205`, `RFC-5869`, `RFC-8439`, `RFC-8446`, `RFC-9106`, `RFC-8032`, `RFC-9180`.

## Brechas

- Obtener y leer texto íntegro de cada norma/RFC; capturar versión, secciones, erratas y hash del archivo cuando la licencia lo permita.
- Extraer requisitos por afirmación y enlazarlos con subtemas y pruebas.
- Revisar literatura revisada por pares sobre side channels, fallos de implementación, composiciones y PQC.
- Implementar banco de pruebas con vectores oficiales y casos negativos.
- Comparar al menos dos implementaciones independientes donde proceda.
- Registrar resultados negativos, incertidumbre y amenazas a validez.
- Solicitar revisión independiente por especialista en criptografía aplicada.

**Conclusión limitada:** la base editorial cubre las principales familias de criptografía y sus superficies de integración. La evidencia consultada sustenta el mapa de estándares y las alertas de vigencia descritas, pero no certifica seguridad de un producto ni madurez científica M3/M4/M5.


## Identificadores del registro de fuentes
- `NIST-SP-800-90A-r1`
- `NIST-SP-800-90B`
- `NIST-SP-800-90C`
- `NIST-FIPS-197`
- `NIST-SP-800-56A-r3`
- `NIST-SP-800-57p1r5`
- `NIST-FIPS-203`
- `NIST-FIPS-204`
- `NIST-FIPS-205`
- `RFC-5869`
- `RFC-8439`
- `RFC-8446`
- `RFC-9106`
- `RFC-8032`
- `RFC-9180`
