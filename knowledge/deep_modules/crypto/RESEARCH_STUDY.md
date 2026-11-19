# Investigación técnica: Criptografía, PKI y gestión de claves

**ID:** crypto · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 en elaboración · **Revisión criptográfica independiente:** pendiente.

## Modelo de seguridad
La criptografía no es sinónimo de seguridad. La garantía depende del algoritmo, parámetros, implementación, aleatoriedad, protocolo, gestión de claves, endpoint, identidad y modelo de amenaza. Cada uso debe especificar propiedades buscadas: confidencialidad, integridad, autenticación, no repudio cuando corresponda, forward secrecy, protección ante replay y disponibilidad.

Antes de seleccionar primitivas, definir adversario, capacidades, horizonte temporal, datos protegidos, volumen, ciclo de vida, requisitos regulatorios, interoperabilidad y consecuencias de compromiso. Separar criptografía de transporte, almacenamiento, identidad, firma de software, backup y comunicación máquina-a-máquina.

## Primitivas y composición
### Hash, MAC y KDF
Un hash es determinista y no autentica por sí solo. Un MAC autentica integridad/origen entre partes que comparten secreto, pero no ofrece firma pública ni no repudio. Una KDF deriva claves independientes de un secreto de entrada y contexto; usar separación de dominios. Para contraseñas usar password hashing lento y parametrizable (Argon2id, scrypt, bcrypt o PBKDF2 según requisitos), nunca SHA-256 simple. No diseñar primitivas propias ni reutilizar claves entre cifrado, MAC, firma y derivación.

### Cifrado simétrico y AEAD
Preferir modos AEAD estandarizados y bibliotecas mantenidas; entender nonce/IV, unicidad, tag, associated data y límites de uso. En AES-GCM, reutilizar nonce con la misma clave puede destruir garantías de confidencialidad e integridad. Gestionar unicidad con garantías y rotación. Cifrado autenticado no resuelve control de acceso, borrado seguro, filtración de metadatos o compromiso del endpoint.

### Criptografía asimétrica y firmas
Diferenciar acuerdo/encapsulación de claves de firma digital. Una firma verifica integridad y vinculación a clave pública; la identidad depende de PKI, enrolamiento y validación. Validar cadena, nombre, uso de clave, extensiones, vigencia, revocación y políticas de confianza. Firmas de artefactos deben cubrir manifiestos canónicos, identidad del emisor, contexto, versión y política de confianza.

### Intercambio de claves y TLS
TLS 1.3 realiza autenticación y negociación en handshake y protege registros con claves derivadas; revisar reanudación, PSK, key update, 0-RTT, certificados y validación del nombre. RFC 9846 (julio de 2026) reemplaza RFC 8446 y aclara requisitos. 0-RTT introduce riesgo de repetición de datos tempranos; restringirlo a operaciones idempotentes o aplicar mitigación de replay. Cifrado de canal no equivale a cifrado extremo a extremo, autenticación mutua ni protección en reposo.

## Gestión del ciclo de vida de claves
NIST SP 800-57 ofrece un marco para generación, distribución, almacenamiento, activación, uso, rotación, backup, recuperación, revocación, compromiso, destrucción y auditoría.

Controles mínimos:
- Generación con CSPRNG/DRBG y fuentes de entropía adecuadas.
- Inventario con propietario, algoritmo, parámetros, propósito, consumidor, fecha, expiración y clasificación.
- Separación por ambiente, servicio, finalidad y tenant.
- Protección en KMS/HSM cuando el riesgo lo justifique; acceso por identidad de workload y mínimo privilegio.
- Rotación por política y por compromiso; definir migración de datos cifrados con claves antiguas.
- Backup de claves con custodia y recuperación probada.
- Revocación y distribución de estado a todos los verificadores.
- Registro de uso sin registrar secretos ni material privado.

HMAC compartido no ofrece identidad individual: todos los poseedores de la clave pueden producir firmas válidas. Para evidencia institucional considerar firma asimétrica, KMS/HSM, identidad federada, timestamps confiables y doble aprobación.

## Criptografía poscuántica
NIST FIPS 203 especifica ML-KEM para encapsulación/acuerdo de secreto; FIPS 204 especifica ML-DSA para firmas; FIPS 205 especifica SLH-DSA, firma hash-based sin estado. Son estándares finales, pero NIST ha publicado notas de errata/potential updates para FIPS 203 y 204: fijar versión, revisar erratas y usar implementaciones mantenidas.

La migración requiere inventariar protocolos, certificados, bibliotecas, HSM, dispositivos y datos de vida larga; clasificar riesgo harvest-now-decrypt-later; identificar componentes no actualizables; diseñar crypto-agility; evaluar tamaños, latencia, memoria, ancho de banda e interoperabilidad; ensayar transición híbrida solo según perfiles estandarizados. No inventar modos híbridos ni combinar algoritmos fuera de especificaciones.

## Amenazas y pruebas
| Amenaza | Fallo típico | Prueba/control |
|---|---|---|
| Nonce repetido | Reutilización de IV/nonce | Unicidad bajo concurrencia, crash/restart y restore |
| Clave expuesta | Secretos en logs, env o repositorio | Escaneo, permisos, KMS y rotación ensayada |
| Downgrade | Negociación débil o fallback | Test de versiones/suites y política de rechazo |
| Certificado inválido | No validar SAN/cadena/uso | Casos negativos de hostname, expiración y CA |
| Replay | Repetición de mensajes | Nonces, ventanas, idempotencia y detección |
| Side channel | Timing/cache/power/fault | Revisión de implementación y pruebas específicas |
| Randomness débil | Entropía insuficiente/estado clonado | Pruebas de fork, reboot, VM clone y DRBG |
| Lifecycle defectuoso | No rotación, revocación o recuperación | Ejercicios de compromiso y recuperación |

## Laboratorios reproducibles
- AEAD con mensajes alterados, nonce repetido y associated data incorrecta.
- Mini-PKI offline: CA raíz/intermedia/leaf, expiración, revocación y validación SAN.
- Rotación de claves de datos con envelope encryption y restore de backup.
- Benchmarks de ML-KEM/ML-DSA en implementaciones verificadas; no presentarlos como prueba de seguridad.
- TLS lab con certificados de prueba, validación de nombre, PSK y 0-RTT controlado.
- Firmas de manifiestos y rechazo de firma con contexto/identidad/versión incorrectos.

Registrar CPU, biblioteca, build flags, versión, parámetros, vector de prueba, comando, salida, hash y desviaciones. No usar claves reales ni secretos productivos.

## Criterios de aceptación
Modelo de amenaza y propiedades declaradas; algoritmos ligados a estándar vigente; gestión de claves y recuperación probadas; test vectors positivos/negativos; interoperabilidad; erratas revisadas; revisión criptográfica independiente antes de producción.

## Fuentes primarias
- NIST SP 800-57 Part 1 Rev. 5: https://doi.org/10.6028/NIST.SP.800-57pt1r5
- NIST FIPS 203 ML-KEM: https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204 ML-DSA: https://csrc.nist.gov/pubs/fips/204/final
- NIST FIPS 205 SLH-DSA: https://csrc.nist.gov/pubs/fips/205/final
- IETF RFC 9846 TLS 1.3 (2026): https://www.rfc-editor.org/rfc/rfc9846.html

**Estado de evidencia:** se inspeccionaron páginas oficiales, metadatos y alcances; no se afirma revisión criptográfica completa, certificación FIPS de una implementación ni evaluación formal de código.
