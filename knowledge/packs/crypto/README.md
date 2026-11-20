# Criptografía aplicada — Guía de dominio

**ID:** `crypto` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Evalúa uso correcto de primitivas, protocolos, claves, aleatoriedad, certificados y ciclos criptográficos. El riesgo suele provenir de composición incorrecta, gestión de claves, modos inseguros, parámetros débiles o uso de criptografía casera. No diseñar primitivas propias para producción.

## Conceptos y superficies
Distinguir cifrado simétrico, cifrado asimétrico, firmas, MAC, KDF, hash, intercambio de claves, AEAD, PKI y protocolos autenticados. Revisar TLS, SSH, IPsec, almacenamiento, backups, tokens, firma de software y comunicación entre servicios. Separar secreto, clave, nonce, IV, salt y material de derivación.

## Competencias específicas
- Elegir algoritmos y parámetros de estándares vigentes.
- Usar AEAD (AES-GCM o ChaCha20-Poly1305) con nonce único.
- Derivar claves con Argon2id/scrypt/PBKDF2 según contexto.
- Gestionar rotación, revocación, expiración y destrucción de claves.
- Validar certificados, cadena de confianza, hostname y revocación.
- Diseñar envelope encryption y separación de claves/datos.
- Reconocer side channels, downgrade, replay y errores de protocolo.
- Inventariar dependencias criptográficas y preparar criptoagilidad.

## Controles prioritarios
- Utilizar bibliotecas criptográficas mantenidas y APIs de alto nivel.
- Nunca reutilizar nonce en modos que lo prohíben ni usar ECB.
- No comparar MAC/firma con comparaciones de tiempo variable cuando aplique.
- Generar claves y nonces con CSPRNG.
- Proteger claves privadas en KMS/HSM/Keystore y controlar exportación.
- Separar claves de cifrado, firma y autenticación.
- Rotar certificados y secretos con solapamiento y prueba de rollback.
- Registrar identificadores y eventos de clave, nunca material secreto.
- Validar downgrade, expiración y revocación en protocolos.

## Metodología
1. Crear inventario criptográfico: algoritmo, versión, propósito, propietario y ubicación de clave.
2. Trazar ciclo de vida: generación, distribución, uso, rotación, backup y destrucción.
3. Revisar código y configuración para primitivas débiles o parámetros erróneos.
4. Verificar autenticación de certificados y protección de canales.
5. Probar recuperación de datos y rotación en entorno de prueba.
6. Evaluar exposición por logs, dumps, variables de entorno y copias.
7. Documentar dependencia de algoritmos y plan de transición.
8. Repetir revisión tras actualizar librerías o protocolos.

## Laboratorio seguro
Crear una aplicación de ejemplo con cifrado AEAD, KDF y firma digital usando biblioteca estándar de proyecto. Probar nonce repetido, tag inválido, certificado caducado y rotación de clave con datos sintéticos. No escribir un cifrador propio ni almacenar claves reales.

## Evaluación
Cada uso criptográfico tiene propósito y propietario; algoritmos y parámetros son aprobados; claves protegidas y rotables; certificados validados; fallos negativos probados.

## Referencias
NIST SP 800-57, SP 800-56A/B, SP 800-132, FIPS 140-3, RFC 8446, OWASP Cryptographic Storage Cheat Sheet y libsodium docs.

## Instrucciones para agentes IA
No inventes recomendaciones de algoritmos sin contexto de compatibilidad. No generes criptografía casera. Nunca imprimas, copies ni guardes claves, tokens o material secreto.

## Arquitectura
La arquitectura criptográfica comprende identidades y raíces de confianza, PKI, emisión/validación de certificados, negociación de protocolos, bibliotecas y módulos criptográficos, almacenamiento/uso de claves, rotación, revocación y destrucción. Trazar dónde se generan, transportan, derivan, almacenan y consumen claves; separar claves de datos y de envoltura; delimitar HSM/KMS, procesos consumidores y operadores. Definir inventario de algoritmos y protocolos, dependencias, modos de fallo y estrategia de agilidad criptográfica, incluida transición poscuántica cuando el horizonte de confidencialidad lo requiera.
