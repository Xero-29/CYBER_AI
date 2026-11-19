# Agenda de investigación: Criptografía

**Dominio:** `crypto` · **Objetivo:** L4 · **Estado:** protocolo específico propuesto; no ejecutado.  
**Corte:** 2026-11-19.  
**Método:** protocolo experimental controlado por subtema; búsqueda de fuentes primarias y reproducción con versiones fijadas.  
**Entregables:** corpus/vector versionado, scripts, logs, análisis, incertidumbre y plan de reproducción.  
**Estado de madurez:** `research_agenda_defined` (agenda propuesta; experimentos pendientes).

## Pregunta central

¿Qué clases de fallos de integración, configuración y ciclo de vida degradan las garantías de primitivas criptográficas estandarizadas en sistemas reales, y qué controles detectan esos fallos con menor coste y menor tasa de falsos positivos?

## Alcance y exclusiones

Incluye aleatoriedad, hash/MAC/KDF, cifrado simétrico/AEAD, intercambio de claves/KEM, protocolos, PKI/gestión de claves y fallos de implementación. Los experimentos se limitan a implementaciones propias o de laboratorio, vectores públicos y datos sintéticos. Se excluyen ataques contra terceros, extracción de secretos reales y pruebas invasivas sobre hardware ajeno.

## R1 — Entropía y DRBG

**Pregunta:** ¿Qué condiciones de inicialización, clonación de entorno y reseed producen repetición de salida o degradación detectable en una arquitectura RBG?

**H0:** la condición experimental no incrementa la tasa de fallos frente al baseline.  
**H1:** al menos una condición controlada (snapshot/clone, fork, fallo de health test o seed insuficiente simulado) produce una desviación reproducible.

**Unidad de análisis:** instanciación DRBG y secuencia de eventos de ciclo de vida.  
**Variables:** método de instanciación, fuente/seed sintética, reseed interval, fork/snapshot y fallo inyectado.  
**Controles:** CSPRNG del sistema sin inyección; generador determinista solo para pruebas.  
**Métricas:** repetición de bloques entre instancias, errores de health test, frecuencia de reseed, disponibilidad y latencia. Los tests estadísticos son indicadores, no prueba de seguridad.  
**Artefactos:** configuración, semilla sintética, versión de runtime/kernel, eventos, hashes y script.

## R2 — Hash, MAC, KDF, password hashing y firmas

**Pregunta:** ¿Qué errores de selección de primitivas, parámetros, encoding o manejo de nonce pueden detectarse mediante vectores, pruebas negativas y revisión automatizada?

**H0:** el conjunto de pruebas no distingue implementaciones correctas de fallos inyectados.  
**H1:** vectores oficiales y pruebas negativas identifican las clases de fallo definidas.

**Corpus:** vectores públicos de SHA-2/SHA-3, HMAC, HKDF, RSA-PSS/ECDSA/EdDSA y Argon2id; entradas sintéticas y claves efímeras de test.  
**Variables:** mensaje vacío/largo, encoding, salt, coste/memoria de KDF, clave incorrecta, firma alterada y nonce ECDSA simulado defectuoso solo en implementación didáctica.  
**Métricas:** pass rate de known-answer tests, fallos detectados, falsos positivos, cobertura de casos y coste de KDF en hardware declarado.  
**Seguridad:** nunca generar firmas con claves reales ni registrar secretos; medir tiempos sin usarlos como único criterio de side-channel.

## R3 — Cifrado simétrico y AEAD

**Pregunta:** ¿Las APIs y wrappers impiden fallos de nonce, AAD, truncamiento de tag y liberación de plaintext no autenticado?

**H0:** los wrappers no difieren del baseline en la tasa de aceptación de ciphertext alterado.  
**H1:** un wrapper correctamente diseñado rechaza todos los casos negativos del corpus y no expone plaintext antes de validar tag.

**Corpus:** vectores NIST para AES-GCM y RFC 8439 para ChaCha20-Poly1305; mensajes sintéticos de longitud 0, 1, bloque−1, bloque, bloque+1 y grandes.  
**Variables:** nonce válido/duplicado en test, AAD modificada, ciphertext bit-flip, tag truncado, clave incorrecta y fallo de almacenamiento de contador.  
**Métricas:** tasa de rechazo de mensajes alterados, errores de interoperabilidad, throughput, latencia p50/p95 y memoria.  
**Criterio crítico:** no tratar la reutilización de nonce como un escenario aceptable en producción; se simula únicamente para demostrar el fallo y documentar impacto.

## R4 — Intercambio de claves y KEM

**Pregunta:** ¿Las implementaciones y protocolos validan correctamente claves públicas, transcript, contexto y errores de decapsulación?

**H0:** pruebas de claves/ciphertexts inválidos no encuentran diferencia respecto al caso válido.  
**H1:** validaciones y manejo uniforme de error impiden aceptación y oráculos distinguibles en el corpus definido.

**Corpus:** vectores oficiales de DH/ECDH y ML-KEM, claves/ciphertexts inválidos sintéticos, implementaciones interoperables.  
**Variables:** parámetros, clave pública, ciphertext, contexto, transcript, versión y algoritmo negociado.  
**Métricas:** tasa de interoperabilidad, aceptación indebida, error distinguible, bytes, latencia y consumo.  
**Nota de vigencia:** comprobar errata de FIPS 203; NIST anunció actualización de SP 800-56A Rev. 3 en enero de 2026.

## R5 — TLS, SSH e IPsec

**Pregunta:** ¿Qué configuraciones de protocolo producen downgrade, autenticación incompleta, replay o fallo de validación de identidad?

**Corpus:** dos endpoints de laboratorio, certificados de CA privada, certificados expirados, nombres DNS de test y configuraciones declarativas versionadas.  
**Variables:** versión, suite, cadena de confianza, hostname, resumption, 0-RTT, host key, identidad IKE, rekey y pérdida de paquetes.  
**Controles:** configuración de referencia documentada y versiones de biblioteca fijadas.  
**Métricas:** handshake success, fallos de validación correctamente rechazados, downgrade aceptado, replay, latencia, bytes y recuperación.  
**Criterio de seguridad:** 0-RTT no se usa para operaciones no idempotentes sin protección específica.

## R6 — Gestión y rotación de claves

**Pregunta:** ¿Qué fallos de coordinación durante rotación, revocación y recuperación dejan datos inaccesibles o protegidos por claves comprometidas?

**Banco:** KMS simulado o de pruebas, DEK/KEK sintéticas, almacenamiento de objetos local y servicio consumidor.  
**Variables:** rotación parcial, caída de KMS, pérdida de quorum, expiración, revocación, backup antiguo, reloj desfasado y rollback.  
**Métricas:** porcentaje de objetos recuperables, clientes migrados, tiempo de rotación, RTO/RPO, claves huérfanas y exposición residual.  
**Criterio:** no exportar material secreto real; documentar transición y rollback antes de ejecutar.

## R7 — Fallos de implementación y side channels

**Pregunta:** ¿Qué combinación de análisis estático, fuzzing, pruebas diferenciales y medición de tiempo encuentra defectos reproducibles sin confundir ruido de medición con fuga?

**Corpus:** parsers de mensajes y certificados de laboratorio, bibliotecas open source fijadas, vectores conocidos y mutaciones generadas.  
**Variables:** longitud, encoding, límites, errores, compilador, flags, plataforma y carga.  
**Métricas:** cobertura, crashes, divergencias diferenciales, defectos confirmados, distribución de tiempo, tamaño de efecto y reproducibilidad.  
**Amenazas a validez:** ruido de CPU, mitigaciones de hardware, virtualización, warm-up, compilador, scheduler y diferencias entre arquitectura.  
**Límite:** análisis de potencia/EM/fault injection solo en laboratorio propio y con procedimientos de seguridad.

## Protocolo común de ejecución

1. Registrar autorización, objetivo, exclusiones, responsable y regla de parada.
2. Fijar hardware, OS, kernel, runtime, compilador, bibliotecas, versiones, configuración y SBOM.
3. Descargar vectores desde su emisor oficial y guardar URL, fecha, licencia y hash.
4. Definir baseline, casos positivos, negativos, límites y controles negativos.
5. Ejecutar primero en contenedor/VM aislada, con datos sintéticos y sin acceso a secretos.
6. Repetir cada medición; justificar tamaño de muestra y método estadístico antes de interpretar.
7. Conservar salidas brutas, logs saneados, scripts, hashes y fallos.
8. Realizar análisis de incertidumbre y amenazas a validez.
9. Reproducir desde entorno limpio y registrar diferencias.

## Métricas y fórmulas

- **Tasa de rechazo negativa:** (TN/(TN+FP)), especificando qué se considera aceptación indebida.
- **Tasa de aceptación positiva:** (TP/(TP+FN)).
- **Interoperabilidad:** intercambios exitosos / intercambios válidos ejecutados.
- **Latencia:** p50 y p95; informar número de repeticiones y hardware.
- **Coste KDF:** tiempo, CPU y memoria por derivación; no comparar sin igualar nivel de seguridad/parametrización.
- **Reproducibilidad:** ejecuciones que replican resultado / ejecuciones válidas.

No usar métricas estadísticas como sustituto de argumentos criptográficos o pruebas de seguridad formales.

## Revisión bibliográfica

Bases y emisores: NIST CSRC, IETF RFC Editor, documentación de fabricantes de bibliotecas criptográficas, IEEE/ACM, USENIX, IACR e investigaciones revisadas por pares. Registrar consultas exactas, fecha, criterios de inclusión/exclusión, versiones, erratas y conflictos entre recomendaciones. Leer texto completo antes de marcar una fuente como revisada integralmente.

## Criterios de salida

- **M2:** compendio técnico específico y protocolo de investigación detallado.
- **M3:** fuentes primarias leídas con extracción de requisitos, vectores y análisis crítico.
- **M4:** laboratorios ejecutados, resultados brutos, scripts, análisis, limitaciones y reproducción interna.
- **M5:** revisión independiente y reproducción por un segundo operador.

**Estado actual:** M2 editorial/propuesto. Los experimentos no se han ejecutado; no afirmar M3/M4/M5.
