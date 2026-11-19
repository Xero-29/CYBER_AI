# Compendio técnico: Criptografía

ID: `crypto` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Criptografía; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema
### 1. entropía y aleatoriedad

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. hash, MAC, KDF y firmas

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. cifrado simétrico y AEAD

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. intercambio de claves y criptografía asimétrica

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. TLS, SSH e IPsec

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. gestión y rotación de claves

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. fallos de implementación

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

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