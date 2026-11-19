# Compendio técnico: Criptografía

ID: `crypto` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Criptografía; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. Entropía, aleatoriedad y DRBG

**Distinciones formales.** Una fuente de ruido produce observaciones físicas/no físicas; el estimador de min-entropía caracteriza el peor caso de probabilidad de una salida; un componente de conditioning transforma muestras; un DRBG expande una semilla en una secuencia determinista computacionalmente impredecible bajo sus supuestos. No confundir longitud de salida con entropía: 256 bits emitidos no implican 256 bits de entropía.

Para una variable discreta (X), la min-entropía de Shannon en su forma clásica es:
[
H_\infty(X)=-\log_2\left(\max_x P[X=x]\right).
]
En fuentes correlacionadas o con atacante, la evaluación debe considerar el modelo de amenaza y estimadores conservadores; no basta asumir independencia.

**Arquitectura de generación.** Documentar fuente, health tests, estimación de entropía, conditioning, acumulación de seed material, instanciación, generación, reseed, límites de request y zeroization. SP 800-90A describe DRBG basados en hash/HMAC/cifrado; SP 800-90B aborda fuentes de entropía y pruebas de salud; SP 800-90C especifica construcciones RBG que integran esas piezas. SP 800-90C fue finalizada en septiembre de 2025; SP 800-90A Rev. 2 sigue siendo borrador/pre-draft en el catálogo consultado, por lo que no se debe citar como norma final.

**Fallos de sistema.** Semilla constante; baja entropía al arranque; clonación de VM/snapshot; fork sin reseed; rollback de estado; fallos de health test ignorados; fallback silencioso a PRNG débil; reutilización de estado en contenedores; lectura de reloj como única fuente. Un test estadístico de uniformidad no prueba impredecibilidad criptográfica ni ausencia de backdoor.

**Controles y pruebas.** Usar CSPRNG del sistema operativo y API de alto nivel. En pruebas reproducibles, inyectar un RNG determinista únicamente en el entorno de test, nunca en producción. Comprobar errores de inicialización/reseed, límites de salida, fork/snapshot y fallo de fuente. Conservar versión del kernel, runtime, biblioteca, fuente, política de reseed y logs sin material secreto.

### 2. Hashes, MAC, KDF, derivación de contraseñas y firmas

**Hash criptográfico.** Una función (H:{0,1}^*\to{0,1}^n) debe evaluarse por resistencia a preimagen, segunda preimagen y colisión. Para un hash ideal de (n) bits, búsqueda genérica de preimagen cuesta aproximadamente (2^n), y colisión por cumpleaños aproximadamente (2^{n/2}); estas cotas no sustituyen análisis del algoritmo concreto. SHA-2/SHA-3 son familias diferentes. MD5 y SHA-1 no deben elegirse para nuevas firmas o integridad resistente a colisiones.

**MAC.** HMAC combina hash y secreto; CMAC deriva de cifrado por bloques. MAC proporciona autenticidad/integridad entre partes que comparten clave, no no-repudio. Comparar etiquetas en tiempo constante y validar longitud/codificación antes de comparar. No diseñar MAC ad hoc ni usar hash(secret || message) como sustituto universal de HMAC.

**KDF.** HKDF (RFC 5869) separa Extract y Expand: extrae material pseudorrandom de IKM con salt y deriva subclaves etiquetadas mediante info/contexto. KDF de contraseña deben ser costosas y resistentes a GPU/memoria según el riesgo: Argon2id (RFC 9106), scrypt o PBKDF2 en perfiles que lo requieran. Cada contraseña debe tener salt aleatorio único; almacenar algoritmo, versión y parámetros para permitir rehash. El pepper es secreto adicional que se custodia separado, no reemplaza salt.

**Firmas.** Separar generación de clave, codificación del mensaje, hash, firma, validación de parámetros y verificación. RSA-PSS, ECDSA y EdDSA tienen supuestos y riesgos diferentes. ECDSA requiere nonce secreto y único; un fallo de RNG puede revelar la clave privada. EdDSA evita la aleatoriedad por firma en su diseño determinista, pero sigue requiriendo implementación correcta, validación de puntos/encoding y protección contra side channels. Una firma válida prueba posesión de clave bajo el protocolo, no identidad legal del titular sin PKI/enrollment confiable.

**Pruebas.** Vectores conocidos, longitud límite, mensaje vacío, codificaciones ambiguas, firmas alteradas, claves incorrectas, truncamiento, replay y comparación temporal. Para contraseñas medir coste CPU/memoria y latencia con hardware objetivo; documentar parámetros y política de migración.

### 3. Cifrado simétrico, modos y AEAD

**Modelo.** Cifrado simétrico usa una clave compartida; cifrado por bloques opera sobre bloques fijos y requiere un modo para datos arbitrarios. AES (FIPS 197 actualizado editorialmente en 2023, sin cambio algorítmico) define bloques de 128 bits y claves de 128/192/256 bits. ChaCha20-Poly1305 es una construcción AEAD especificada en RFC 8439.

**Modos y propiedades.** ECB revela patrones y no es apropiado para datos estructurados. CBC requiere IV impredecible y autenticación separada correctamente compuesta; padding oracle puede revelar plaintext. CTR convierte el bloque en flujo y exige unicidad del counter/nonce por clave. GCM ofrece AEAD y alto rendimiento, pero la reutilización de nonce bajo la misma clave puede comprometer confidencialidad e integridad. XTS se orienta a cifrado de sectores de almacenamiento y no ofrece autenticación de datos. Elegir modo según el caso y perfil normativo, no solo benchmark.

**AEAD.** Una API AEAD recibe key, nonce, plaintext y associated data (AAD); devuelve ciphertext y tag. AAD queda autenticado pero no cifrado. El descifrado debe fallar cerrado si la etiqueta no valida y no debe exponer plaintext parcial antes de autenticar. AAD útil: versión de formato, tenant, identificador de objeto y contexto, evitando campos mutables no canónicos.

**Disciplina de nonce.** Mantener unicidad por clave de acuerdo con el modo. Diseñar contador persistente y seguro ante concurrencia, crash, restore y multi-región; o usar esquema aleatorio solo si el límite probabilístico y volumen están justificados. Rotar claves antes de exceder límites de invocaciones/datos del estándar. Nunca “arreglar” una colisión cambiando nonce después de cifrar.

**Pruebas.** Vectores oficiales, nonce repetido en test controlado, AAD alterado, tag truncado, ciphertext bit-flip, mensajes de longitud cero, bloques parciales y fallo de autenticación. No incluir claves ni plaintext sensible en logs.

### 4. Intercambio de claves, KEM y criptografía asimétrica

**Problemas matemáticos.** RSA se apoya en dificultad de factorización; Diffie–Hellman clásico en logaritmo discreto; ECC en logaritmo discreto sobre curvas; ML-KEM en Module Learning With Errors (Module-LWE). La seguridad depende de parámetros, implementación, codificación y modelo de ataque; el tamaño de clave no se compara linealmente entre familias.

**DH/ECDH.** Las partes intercambian valores públicos y derivan un secreto compartido; el secreto bruto debe pasar por KDF y quedar ligado al transcript, identidades y contexto. DH sin autenticación es vulnerable a MITM. Revisar validación de parámetros/puntos, pequeños subgrupos, claves efímeras, key confirmation y forward secrecy. SP 800-56A Rev. 3 cubre esquemas de establecimiento basados en logaritmo discreto; NIST anunció en enero de 2026 que será actualizado, por lo que registrar ese plan al fijar perfiles.

**KEM.** Un KEM expone KeyGen, Encaps y Decaps: una parte obtiene public key; encapsulación genera ciphertext y shared secret; decapsulación reconstruye el secreto. El secreto debe derivarse/combinarse mediante KDF según protocolo. ML-KEM-512/768/1024 se especifican en FIPS 203. El estándar tiene una nota NIST de noviembre de 2025 sobre un problema que será corregido en una revisión; antes de despliegue consultar errata vigente y no asumir que el texto de 2024 es inmutable.

**RSA y curvas.** Para nuevas firmas RSA preferir esquemas con padding moderno (p. ej. PSS) según perfil; evitar RSA textbook y padding legado no aprobado. En ECC, fijar curvas/perfiles aprobados y validar puntos/codificación canónica. No aceptar parámetros negociados débiles por compatibilidad silenciosa.

**Pruebas.** Interoperabilidad entre implementaciones independientes, clave/ciphertext malformados, claves inválidas, error de decapsulación, downgrade, transcript alterado y límites de tamaño. Confirmar que el error no filtra oráculos distinguibles.

### 5. Protocolos: TLS, SSH, IPsec y composición criptográfica

**TLS 1.3.** Estudiar ClientHello/ServerHello, key share, transcript hash, HKDF key schedule, certificados, CertificateVerify, Finished, alertas, resumption y PSK. Separar autenticación del servidor, autenticación del cliente y autorización de aplicación. TLS 1.3 reduce suites y elimina construcciones antiguas, pero configuración, validación de certificado, endpoint y aplicación siguen siendo críticos. Evaluar 0-RTT como datos potencialmente replayables; no usarlo para operaciones no idempotentes sin mitigación.

**SSH.** Verificar host key y política de known_hosts; revisar algoritmos de intercambio, firma y cifrado, agent forwarding, túneles, certificados SSH, expiración y rotación. Deshabilitar algoritmos heredados conforme a inventario de compatibilidad. Una conexión cifrada a host no autenticado no es segura.

**IPsec/IKE.** Distinguir transporte/túnel, IKE SA y Child SA, identidad, selectors, rekey, PFS, anti-replay y NAT traversal. Evaluar rutas, solapamiento de redes, política de cifrado y continuidad. Un túnel correcto puede proteger el canal equivocado si selectors/rutas están mal definidos.

**Composición.** Usar protocolos estandarizados, no diseñar handshake propio. La composición debe vincular identidad, transcript, propósito, algoritmo, versión y contexto para prevenir unknown key-share, downgrade y cross-protocol attacks. Modelar estados y eventos adversariales; considerar análisis formal cuando el protocolo sea crítico.

**Pruebas.** Certificados expirados/no confiables, hostname mismatch, downgrade, suite prohibida, renegociación/resumption, replay 0-RTT, host key cambiada, peer identity errónea, rekey y pérdida de paquetes. Registrar versión de biblioteca y configuración efectiva, no solo el archivo declarativo.

### 6. Gestión, ciclo de vida, custodia y rotación de claves

**Inventario.** Cada clave necesita ID, propósito, algoritmo, tamaño/parámetros, dueño, sistema, clasificación, fecha de creación, activación, expiración, rotación, dependencias, ubicación, estado, respaldo y política de destrucción. Separar claves de cifrado de datos (DEK) y claves de cifrado de claves (KEK); usar envelope encryption para escalar y permitir rotación de KEK sin recifrar todo el volumen cuando el diseño lo permite.

**Estados.** Generación → distribución/provisioning → activación → uso → rotación → suspensión/revocación → archivo/retención → destrucción. Especificar transiciones autorizadas, doble control para operaciones críticas, segregación de funciones y evidencia de auditoría. Rotar no es solo generar nueva clave: definir re-encryption, rewrapping, periodo de solapamiento, clientes atrasados y rollback.

**HSM/KMS.** Distinguir HSM, KMS administrado, TPM, enclave y software keystore. Evaluar límites de confianza, certificación aplicable, control de acceso, quorum, backup, recuperación, export policy, HA, logging, tenancy y dependencia del proveedor. Certificación FIPS 140-3 aplica a módulos criptográficos dentro de alcance/versiones concretos, no al sistema completo ni a cualquier uso del producto.

**Incidentes.** Ante compromiso: determinar claves afectadas, ventana temporal, ciphertext/datos expuestos, certificados emitidos, dependencias y posibilidad de descifrado retroactivo; revocar/rotar, invalidar sesiones, reemitir certificados, migrar datos y preservar evidencia. La rotación no elimina el riesgo de datos ya exfiltrados con clave comprometida.

**Pruebas.** Simular expiración, revocación, pérdida de KMS, restore, quorum incompleto, clave huérfana, rotación parcial, reloj desfasado y rollback de backup. Medir RTO/RPO, objetos recuperables, porcentaje de clientes migrados y exposición residual.

### 7. Fallos de implementación, side channels y assurance

**Errores de API y protocolo.** Nonce/IV repetido; comparación no constante; validación incompleta de certificados; parser con ambigüedad; padding oracle; error distinguishability; falta de domain separation; uso de clave para varios propósitos; downgrade; key reuse; zeroization incompleta; RNG débil; excepciones que filtran material; manejo incorrecto de errores de autenticación.

**Side channels.** Timing, cache, branch prediction, power, electromagnetic emanations, consumo, acceso a memoria, errores inducidos y fault injection. El análisis debe declarar atacante, distancia, equipo, repetibilidad, presupuesto, mitigaciones y residual. Las pruebas invasivas solo en hardware propio y laboratorio especializado; no extrapolar un resultado de emulador a hardware real.

**Assurance.** Revisión de código y dependencias; fuzzing de parsers/protocolos; sanitizers; static analysis; constant-time analysis; vectores conocidos; formal verification cuando sea viable; pruebas diferenciales entre implementaciones; reproducible builds y cadena de suministro. Separar algoritmo aprobado, implementación validada, módulo certificado y despliegue correctamente configurado: son afirmaciones distintas.

**Respuesta ante vulnerabilidad.** Inventariar versiones afectadas, primitives, protocolos, claves/certificados y datos; establecer exposición y exploitability; definir mitigación compatible, rotación, revocación y migración; probar rollback y clientes legacy. Mantener crypto-agility sin habilitar negociación débil.

## Laboratorio reproducible
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Caso | Evidencia exigida |
|---|---|---|
| crypto-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| crypto-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| crypto-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| crypto-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

Diseño definido; ejecución pendiente.

## Métricas
Elegir métricas específicas: cobertura, tasa de detección, falsos positivos/negativos, latencia, disponibilidad, impacto colateral, tiempo de remediación y repetibilidad. Toda cifra exige unidad de análisis, muestra, baseline, versiones, repeticiones y método de análisis.

## Investigación bibliográfica
- Registrar bases, cadenas de búsqueda, fecha, idiomas y criterios de inclusión/exclusión.
- Priorizar normas, especificaciones, documentación primaria y literatura revisada por pares.
- Leer texto completo antes de usar `full_text_reviewed`.
- Extraer método, población, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y enfoques; separar evidencia, inferencia e hipótesis.
- Registrar edición, URL canónica, licencia, fecha y hash cuando el archivo pueda archivarse legalmente.

## Preguntas de investigación candidatas
1. ¿Qué controles reducen el riesgo de los escenarios priorizados frente a un baseline?
2. ¿Qué condiciones de versión/entorno explican diferencias entre resultados publicados y reproducidos?
3. ¿Qué combinación de señales y criterios mejora la detección sin impacto operacional inaceptable?

Cada estudio debe definir H0/H1, variables, muestra, comparadores, refutación, análisis, ética, seguridad y límites.

## Artefactos de aceptación
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos/datos/identidades/versiones.
- [ ] Modelo de amenazas y escenarios.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimientos con precondiciones, rollback y parada.
- [ ] Laboratorio y casos medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencias, edición, fecha y hashes.
- [ ] Incertidumbre, falsos positivos/negativos y validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No demuestra cobertura profunda ni M3/M4/M5. Próxima puerta: revisar fuentes completas, producir artefactos específicos, ejecutar pruebas y registrar evidencia.


## Profundización técnica específica: Criptografía

### Seguridad como propiedad de sistema
Distinguir confidencialidad, integridad, autenticidad, no repudio, forward secrecy, key confirmation y resistencia a replay. Los algoritmos no compensan generación débil de claves, nonce repetido, validación incorrecta, side channels o gestión deficiente. Toda selección debe partir del modelo de amenaza, vida útil de datos, jurisdicción, interoperabilidad, rendimiento y política criptográfica. Evitar algoritmos propietarios y diseñar criptografía propia.

### Entropía, DRBG y generación de claves
Distinguir fuente física de entropía, conditioning component, DRBG y API de aleatoriedad del sistema. Revisar inicialización, reseeding, fork behavior, snapshots/VM cloning, arranque temprano, fallos de hardware y pruebas de salud. NIST SP 800-90A/B/C estructura DRBG, fuentes y construcción de generadores; superar tests estadísticos no demuestra por sí solo entropía impredecible. Nunca usar PRNG no criptográfico para secretos.

### Primitivas y composición
Hash: resistencia a preimagen, segunda preimagen y colisión; MAC autentica con secreto compartido; KDF deriva claves separadas por contexto; firmas vinculan clave privada y mensaje; AEAD ofrece confidencialidad e integridad autenticada. Preferir suites AEAD modernas y APIs de alto nivel. Nonces deben cumplir unicidad/requisitos del modo; reutilización puede destruir seguridad. Separar claves por propósito, protocolo y entorno con domain separation. Evitar comparar hashes de contraseña rápidos: usar KDF de contraseña con salt y coste ajustable, y parámetros versionados.

### Protocolos, TLS y autenticación
Evaluar handshake, transcript binding, downgrade resistance, certificate validation, hostname, revocation, resumption, 0-RTT replay, key schedule y forward secrecy. TLS protege canal, no datos en endpoints ni autorización. En SSH revisar host key verification, algoritmos, agent forwarding y rotación. En IPsec analizar IKE, identidad, PFS, rekey y selectores. Las implementaciones deben usar bibliotecas mantenidas y configuraciones aprobadas; no copiar suites antiguas por compatibilidad sin riesgo documentado.

### PKI y ciclo de vida de claves
Definir raíz, intermediarias, políticas, perfiles, emisión, validación, revocación, OCSP/CRL, CT cuando aplique y renovación. HSM protege operaciones y material bajo límites certificados; no elimina abuso de autorización ni errores de backup. Separar custodia, uso, administración y auditoría. Modelar estados: generación, distribución, activación, rotación, suspensión, revocación, archivo y destrucción. Probar recuperación de HSM, quorum, backup y continuidad sin exportar material prohibido.

### Criptografía poscuántica
FIPS 203 define ML-KEM para establecimiento de claves; FIPS 204 ML-DSA y FIPS 205 SLH-DSA para firmas. NIST SP 800-227 proporciona recomendaciones para KEM (publicado 2025). Inventariar algoritmos, certificados, protocolos, bibliotecas, appliances y datos de larga confidencialidad; priorizar crypto-agility, pruebas híbridas y migración gradual. Registrar tamaños de claves/firmas, latencia, ancho de banda, memoria, interoperabilidad y riesgos de downgrade. Verificar erratas y revisiones de cada FIPS antes de fijar perfil. No afirmar que PQC resuelve riesgos de implementación o side-channel.

### Pruebas criptográficas
Aplicar vectores de prueba oficiales, known-answer tests, negative tests, fuzzing de parsers, test de interoperabilidad y análisis de uso de nonce/IV. Separar validación de algoritmo de validación de módulo criptográfico certificado. Evaluar timing, cache, power/EM y fault injection solo en hardware propio y laboratorio especializado, con límites de seguridad. Medir tasas de fallo, cobertura, latencia, memoria y compatibilidad; publicar versión exacta de biblioteca, compilador y flags.

### Laboratorios específicos
- Comparar KDF de contraseñas con parámetros controlados y medir coste/uso de memoria.
- Verificar TLS con certificados de prueba, expiración, hostname incorrecto y revocación simulada.
- Evaluar unicidad de nonce en implementación didáctica AEAD y casos de fallo.
- Interoperabilidad ML-KEM/ML-DSA/SLH-DSA con vectores oficiales y bibliotecas aprobadas.
- Ensayo de rotación/revocación/recuperación de claves en PKI aislada.
No crear cifrados propios para producción ni usar claves reales en ejercicios.

## Estado de validación de la ampliación
Contenido técnico editorial añadido para orientar revisión disciplinar; no implica lectura integral de fuentes, revisión externa ni ejecución de laboratorio. Mantener madurez M1/M2 hasta completar puertas G1–G8 con evidencias.