# FND-01.02 — Síntesis de fuentes primarias y modelo ampliado de propiedades de seguridad

**Fecha:** 2026-11-20  
**Estado:** ampliación teórica dirigida; pendiente lectura integral y evaluación supervisada.  
**Relación:** Foundations → FND-01 → FND-01.02, propiedades de seguridad y CIA extendida.

## 1. Delimitación

Confidencialidad, integridad y disponibilidad (CIA) son objetivos fundamentales de seguridad de la información. No constituyen una teoría completa de la confianza, de la seguridad funcional, de la privacidad, de la confiabilidad o de la resiliencia. Las propiedades adicionales deben clasificarse por el tipo de afirmación que expresan y por la evidencia necesaria para sostenerlas.

FIPS PUB 199 define C/I/A para categorizar el impacto de una pérdida de confidencialidad, integridad o disponibilidad sobre información y sistemas federales de Estados Unidos. Es una referencia primaria útil para precisión conceptual y categorización, pero su ámbito no es universal. NIST CSF 2.0 organiza resultados de gestión del riesgo cibernético en seis funciones; no prescribe un conjunto único de controles ni reemplaza la ingeniería del sistema. NIST SP 800-160 aporta ingeniería de sistemas seguros y assurance. NISTIR 8062 trata los riesgos de privacidad como una dimensión distinta del acceso no autorizado.

## 2. CIA con semántica precisa

### 2.1 Confidencialidad

Preservar restricciones autorizadas de acceso y divulgación. El objeto protegido puede ser información en reposo, en tránsito, en uso, metadatos, credenciales, claves, secretos operacionales o inferencias derivables.

Preguntas:
- ¿Qué actor puede acceder, con qué propósito y bajo qué autoridad?
- ¿Qué canal, copia, caché, log, backup, soporte o tercero expone la información?
- ¿Puede inferirse un dato sensible desde metadatos o combinaciones de datos aparentemente inocuos?
- ¿Cómo se revoca el acceso y se demuestra la eliminación o expiración?

Controles: clasificación, mínimo privilegio, separación de funciones, cifrado, gestión de claves, control de exportación, minimización de datos, segmentación, retención limitada y revisión de terceros.

Límite: cifrar o restringir acceso no garantiza que el tratamiento sea justo, necesario, transparente o compatible con la finalidad. Por tanto, confidencialidad no implica privacidad.

### 2.2 Integridad

Proteger frente a modificación o destrucción impropia. Debe especificarse qué entidad, atributo, transición, secuencia o estado necesita permanecer íntegro, quién puede modificarlo y cómo se detecta una alteración.

Dimensiones que se deben distinguir:
- integridad de bits o estructura;
- integridad de registros y relaciones;
- consistencia transaccional;
- frescura y protección contra replay;
- procedencia y cadena de custodia;
- exactitud y validez semántica;
- integridad de configuración y estado de ejecución.

Hash, MAC y firma pueden aportar detección de alteración bajo supuestos de algoritmo, clave, implementación y custodia. No demuestran que el dato de origen fuera verdadero, que el sensor estuviera calibrado, que el software firmado sea benigno ni que la configuración sea segura.

### 2.3 Disponibilidad

Asegurar acceso y uso oportuno y confiable por actores autorizados. El requisito debe expresar función, actor, ventana temporal, calidad mínima, capacidad, degradación admisible y prioridad de misión.

Controles: tolerancia a fallos, redundancia con independencia demostrada, límites de tasa, protección DDoS, colas y backpressure, capacidad, monitoreo, mantenimiento, recuperación, failover y procedimientos manuales seguros.

Límite: un servicio puede estar disponible mientras ejecuta una acción no autorizada o peligrosa. En sistemas críticos, una parada controlada puede ser preferible a disponibilidad continua.

## 3. Propiedades relacionadas que no deben confundirse con CIA

| Propiedad | Significado técnico | Mecanismos/evidencia | Contraejemplo |
|---|---|---|---|
| Autenticidad | origen, entidad o mensaje corresponde a la identidad declarada | autenticación, certificados, firma, atestación, validación de trust anchors | un paquete firmado por un proveedor auténtico puede contener una función defectuosa |
| Autorización | actor autenticado puede realizar una acción concreta en un contexto | políticas, atributos, roles, condiciones, evaluación de permisos | autenticar a un administrador no autoriza toda acción en cualquier sistema |
| Accountability | acciones pueden atribuirse a entidades y contexto con evidencia fiable | identidad individual, logs protegidos, tiempo confiable, revisión | logs completos con cuentas compartidas no permiten atribución individual |
| Non-repudiation | evidencia técnica y procedimental apoya una atribución frente a una negación | firma, gestión de claves, sello temporal, identidad probada, custodia | una firma no prueba por sí sola intención humana, control exclusivo de clave ni efecto jurídico |
| Provenance | historial de origen, transformación y custodia de datos/artefactos | lineage, hashes, firmas, registros de build, SBOM, attestations | procedencia trazable no demuestra corrección semántica |
| Freshness | dato o mensaje corresponde a una ventana/estado actual | nonce, contador, timestamp confiable, secuencia, expiración | un mensaje auténtico y no modificado puede ser un replay antiguo |
| Auditability | capacidad de reconstruir y revisar eventos relevantes | registros completos, consistentes, protegidos, sincronización y controles de acceso | registrar todo sin minimización puede violar privacidad |
| Privacy | tratamiento de datos no produce riesgos indebidos para personas | finalidad, minimización, transparencia, gestión, disociación, evaluación de impacto | no hubo filtración, pero hubo perfilado secundario no esperado |
| Safety | se controla el riesgo de daño inaceptable | hazard analysis, FMEA, FTA, STPA, safety case | el acceso fue autorizado, pero el comando provocó un estado peligroso |
| Reliability | función correcta se presta bajo condiciones y tiempo definidos | modelos, datos de fallo, FMEA, pruebas de fiabilidad | un sistema puede fallar de forma segura o ser fiable al ejecutar un diseño inseguro |
| Resilience | función esencial resiste, recupera y se adapta ante adversidad | escenarios, ejercicios, recuperación verificada, métricas de misión | backup restaurado con credenciales comprometidas no constituye recuperación confiable |

## 4. Autenticidad, integridad y verdad: tres afirmaciones distintas

Considérese un paquete de software:
1. Su hash coincide con el manifiesto: evidencia de integridad de bytes respecto del manifiesto.
2. La firma valida con un certificado y cadena de confianza aceptados: evidencia de autenticidad del firmante bajo el modelo de PKI y estado de revocación.
3. El proveedor y el proceso de build son confiables: afirmación distinta que requiere procedencia, controles de build, revisión y evidencia.
4. El código es correcto y seguro: afirmación semántica que exige análisis, pruebas, revisión y límites de uso.
5. El despliegue es seguro para la función y el entorno: afirmación de sistema que exige análisis de hazard/threat, configuración y operación.

No se puede saltar del punto 1 o 2 al 4 o 5.

## 5. Autenticidad, accountability y non-repudiation

### 5.1 Autenticidad

Debe distinguirse autenticación de usuario, autenticación de dispositivo, autenticación de servicio, autenticación de mensaje y atestación de estado. Cada una requiere una cadena de identidad, credenciales, algoritmos, claves, validación de certificados, revocación, tiempo y política de confianza.

### 5.2 Accountability

La atribución requiere más que logs: identidad no compartida, contexto de sesión, reloj sincronizado y protegido, integridad del registro, control de acceso, retención, correlación y procedimiento de revisión. La minimización de datos debe limitar la captura de información personal no necesaria.

### 5.3 Non-repudiation

No es una propiedad absoluta que un algoritmo “garantiza”. La fuerza de la evidencia depende de:
- identidad y prueba de control de la clave;
- protección, exclusividad y ciclo de vida de la clave;
- algoritmo y parámetros válidos en el momento de uso;
- estado de revocación y confianza;
- sellado temporal y sincronización;
- integridad del proceso de firma y del documento;
- jurisdicción, contrato, procedimiento y reglas probatorias.

La firma digital es una pieza de evidencia, no una conclusión jurídica automática.

## 6. Taxonomía de control y evidencia

| Objetivo | Controles de diseño | Verificación | Evidencia |
|---|---|---|---|
| C | clasificación, autorización, cifrado, minimización | pruebas de acceso, revisión de flujos, análisis de inferencia | políticas, resultados, logs y configuración |
| I | validación, transacciones, hashes/MAC/firmas, control de cambios, procedencia | pruebas de manipulación, replay, reconciliación y consistencia | registros de validación, firmas, hashes, cadena de custodia |
| A | redundancia, límites, capacidad, degradación controlada, protección DDoS | carga, failover, recuperación, pruebas de dependencia | SLI/SLO, tiempos, errores, resultados de ejercicios |
| Autenticidad | identidad, PKI, MFA, mTLS, atestación | validación de certificados, revocación, spoofing y claves | cadenas de confianza, logs y resultados de prueba |
| Accountability | identidad individual, logs protegidos, tiempo confiable, revisión | correlación de eventos, alteración de logs, atribución | evidencia de eventos y procedimientos |
| Privacy | minimización, finalidad, retención, gestión y disociación | pruebas de reidentificación, revisión de propósito y acceso | mapa de datos, evaluación de impacto, decisiones de retención |
| Safety | interlocks, límites, safe states, independencia, supervisión | HAZOP/FMEA/FTA/STPA y validación de funciones | hazard log, safety case y verificación |
| Reliability | tolerancia a fallos, mantenimiento, calidad de componentes | ensayos, análisis de fallos, modelos y datos de campo | distribuciones, supuestos, intervalos y registros |
| Resilience | anticipación, continuidad, recuperación limpia, adaptación | escenarios adversariales, restore, failover y ejercicios | tiempos, estado de confianza, función de misión y lecciones |

## 7. Fallos de razonamiento que deben detectarse

1. “Está cifrado, por tanto es privado.” Falso: puede existir uso secundario, retención excesiva, inferencia o finalidad incompatible.
2. “Tiene firma válida, por tanto es seguro.” Falso: la firma acredita una relación criptográfica, no benignidad o corrección.
3. “El hash coincide, por tanto el dato es verdadero.” Falso: solo se compara con una referencia bajo supuestos.
4. “Tiene 99,99 % de disponibilidad, por tanto es resiliente.” Falso: el servicio puede no recuperarse de un compromiso o perder misión.
5. “Tiene dos servidores, por tanto es redundante.” Falso: puede existir causa común.
6. “Fail-closed es siempre más seguro.” Falso: puede crear un hazard o bloquear una función de emergencia.
7. “No hay acceso no autorizado, por tanto hay privacidad.” Falso: el tratamiento autorizado también puede producir riesgo.
8. “Los logs permiten no repudio.” Falso: sin identidad, tiempo, integridad y custodia no hay atribución robusta.

## 8. Aplicación de fuentes

- FIPS PUB 199: definiciones CIA y niveles de impacto para categorización federal estadounidense; alcance limitado.
- NIST CSF 2.0: seis funciones de resultados de riesgo cibernético; no prescribe una implementación única.
- NIST SP 800-160 Vol. 1 Rev. 1: ingeniería de seguridad del sistema y assurance a través del ciclo de vida.
- NIST SP 800-160 Vol. 2 Rev. 1: resiliencia cibernética y funciones esenciales bajo adversidad.
- NIST SP 800-53 Rev. 5: catálogo de controles de seguridad y privacidad; la selección debe basarse en contexto y riesgo.
- NISTIR 8062: objetivos de ingeniería de privacidad; no sustituye ley o evaluación jurídica.
- IEC 62443-2-1 y 3-3: programa y requisitos técnicos de ciberseguridad para IACS.
- IEC 61508: functional safety; no debe citarse como control completo de ciberseguridad.
- IEC TR 63069: coordinación safety/security en automatización industrial.

## 9. Criterios de aceptación teórica para FND-01.02

Un estudiante no supera el subtema si:
- trata autenticidad como verdad;
- trata integridad criptográfica como corrección;
- trata privacidad como confidencialidad;
- trata disponibilidad como resiliencia;
- trata seguridad como safety;
- usa non-repudiation sin describir supuestos de identidad, clave, tiempo y contexto;
- presenta “CIA+” como una norma universal;
- no puede enlazar cada afirmación con evidencia y límites.

La evaluación debe exigir un modelo de propiedades, un escenario integrado, una selección justificada de controles y una matriz claim-evidence. La existencia de esta síntesis no equivale a que el instrumento haya sido administrado.

## 10. Límites de revisión

FIPS 199 y páginas oficiales NIST/IEC/ISO se revisaron en las secciones y metadatos relevantes indicados en el registro. No se ha completado lectura lineal de todos los estándares ni se han adquirido los textos ISO/IEC protegidos. No hay prueba supervisada ni revisión independiente. El estado teórico continúa como borrador ampliado, no aprobado.
