# FND-01.02 — Propiedades de seguridad: CIA y propiedades ampliadas

**Estado:** borrador disciplinar en desarrollo; no aprobado. **Madurez:** T0/O0. **Prerrequisito:** FND-01.01.

## Resultados de aprendizaje
El lector debe definir con precisión confidencialidad, integridad y disponibilidad (CIA); distinguir autenticidad, autenticación, accountability, trazabilidad, auditabilidad, no repudio, frescura, privacidad y resiliencia; traducir objetivos a invariantes y requisitos verificables; analizar conflictos; diseñar controles y evaluación.

## L1. Fundamentos teóricos

**Confidencialidad** es impedir que información se revele a sujetos, procesos o entidades no autorizados. Debe precisar dato, actor, operación, contexto y excepciones. No equivale a cifrado: también intervienen autorización, aislamiento, minimización, control de exportación y copias.

**Integridad** es preservar exactitud, completitud y estado autorizado de datos, configuración y procesos frente a modificaciones/destrucción indebidas. Distinguir integridad en reposo, tránsito, ejecución, configuración, transacciones, procedencia y secuencia. Un hash solo detecta cambios si el valor de referencia y el procedimiento están protegidos; no prueba que el dato original fuera verdadero.

**Disponibilidad** es que una función o recurso sea utilizable por entidades autorizadas dentro de condiciones y tiempos especificados. Distinguir disponibilidad de host, servicio, función de negocio, población y dependencias. Uptime de infraestructura no equivale a disponibilidad de misión.

**Autenticidad** es que una entidad, mensaje o dato sea genuino y atribuible al origen afirmado. **Autenticación** es el proceso de verificar una afirmación de identidad/procedencia con un nivel de confianza. Una sesión autenticada no vuelve auténtico todo dato recibido; una firma válida tampoco demuestra autorización.

**Accountability** exige atribución de acciones y decisiones a responsables, con gobierno y consecuencias. **Trazabilidad** enlaza origen, transformaciones y destino. **Auditabilidad** permite examinar evidencia suficiente y fiable. Logs sin identidad individual, reloj confiable, integridad, contexto y retención no garantizan accountability.

**No repudio** es un objetivo probatorio que dificulta negar una acción. Una firma digital no lo garantiza por sí sola: requiere identidad, autoridad, control de clave, intención, custodia, tiempo, revocación y contexto probatorio.

**Frescura, secuencia y unicidad** impiden aceptar mensajes antiguos, repetidos o fuera de orden cuando ello importa. Nonces, contadores, timestamps, IDs idempotentes y ventanas anti-replay tienen supuestos y fallos distintos.

Privacidad y resiliencia no se reducen a CIA. Privacidad aborda problemas que las personas pueden experimentar por el procesamiento de datos; resiliencia aborda continuidad, recuperación y adaptación de funciones esenciales.

## L2. Fundamentos matemáticos y formales

Sea un sistema de estados S, acciones A y transiciones T. Una invariante I(s) debe cumplirse en todo estado inicial admisible y preservarse en cada transición permitida. Ejemplo: toda lectura read(u,o) exige authorized(u,o,read,context). La verificación debe cubrir cada ruta de acceso, no solo la interfaz.

Una propiedad formal de *safety* dice “nunca ocurre un estado prohibido”; una propiedad de *liveness* dice “algo requerido ocurre eventualmente”, bajo hipótesis explícitas de progreso/fairness. No confundir *safety property* en verificación formal con la disciplina de safety funcional.

Ejemplos esquemáticos en lógica temporal:
- G(no_autorizado implica no_lectura): ninguna lectura no autorizada ocurre.
- G(solicitud implica F(respuesta)): cada solicitud válida obtiene eventualmente respuesta, si se cumplen las hipótesis de progreso.
- G(commit implica autorizado_y_valido): todo commit está autorizado y preserva invariantes.

Para disponibilidad por función f, población P y ventana W, definir numerador como tiempo en que la función cumple el criterio de servicio y denominador como tiempo elegible de W. Declarar mantenimiento, latencia, errores parciales, exclusiones y degradación. No ocultar una función crítica fallida detrás de un promedio global.

## L3. Arquitectura y mecanismos

Mapear propiedades en identidad/autoridad, aplicación, almacenamiento, comunicaciones, infraestructura, operación, observabilidad y terceros.

Mecanismos típicos:
- Confidencialidad: autorización, segmentación, cifrado, minimización, aislamiento y control de exportación.
- Integridad: validación, transacciones, firmas/MAC, control de cambios, secuenciación y reconciliación.
- Disponibilidad: redundancia, capacidad, rate limiting, colas, degradación controlada, recuperación y diversidad de dependencias.
- Autenticidad: autenticación, firmas, atestación, provenance y certificados.
- Accountability: identidad individual, logs protegidos, sincronización temporal, correlación y retención gobernada.
- Frescura: nonce, contador monotónico, expiración, challenge-response y detección de replay.

Ningún mecanismo aislado garantiza una propiedad. La arquitectura debe incluir ciclo de vida de claves, secretos, políticas, excepciones, errores y recuperación.

## L4. Estándares y metodologías

- NIST SP 800-53: catálogo de controles de acceso, auditoría, integridad, contingencia, identificación y protección. Seleccionar un control no prueba implementación ni eficacia.
- NIST SP 800-160 Vol. 1 Rev. 1: ingeniería de seguridad como subdisciplina de ingeniería de sistemas; trata seguridad como propiedad emergente y exige decisiones de trade-off con safety, reliability, availability y maintainability. Final, noviembre de 2022.
- ISO/IEC 27000: vocabulario y sistema de gestión; verificar edición y alcance.
- RFCs y estándares criptográficos: consultar textos normativos específicos.
- Common Criteria / ISO/IEC 15408: evalúa claims dentro de un Security Target y alcance definido; no demuestra ausencia universal de vulnerabilidades.
- Model checking, theorem proving, análisis estático, testing y review cubren propiedades y modelos diferentes.

## L5. Implementación y requisitos verificables

Confidencialidad: cada lectura de expediente evalúa autorización vigente para principal, recurso, acción y contexto; un rechazo no revela contenido protegido.

Integridad: operaciones financieras son atómicas, autorizadas, idempotentes cuando se reintentan y reconciliables con el ledger; toda modificación registra actor, tiempo, motivo y versión.

Disponibilidad: una función cumple SLO por región y población; el modo degradado preserva operaciones críticas y rechaza las no seguras.

Autenticidad/frescura: órdenes se vinculan a origen, autorización, contexto, nonce/secuencia y período válido; mensajes repetidos o fuera de secuencia se rechazan.

Cada requisito define owner, alcance, método de verificación, datos de prueba, aceptación, excepciones y evidencia. “Debe ser muy seguro” no es verificable.

## L6. Análisis avanzado y trade-offs

1. Confidencialidad vs disponibilidad: una clave central inaccesible bloquea datos; la recuperación de claves crea una ruta de abuso. Diseñar recuperación con separación de funciones y pruebas.
2. Integridad vs latencia: firmas, validaciones y consenso cuestan; omitirlos puede permitir corrupción/replay. Decidir según amenaza y consecuencia.
3. Disponibilidad vs consistencia: ante partición, definir por función qué operaciones pueden continuar y qué consistencia es obligatoria.
4. Trazabilidad vs privacidad: logs detallados ayudan a investigar, pero pueden crear vigilancia y una nueva base sensible. Minimizar y limitar finalidad/acceso/retención.
5. No repudio vs compromiso de claves: una firma demuestra uso de una clave, no necesariamente voluntad, autoridad o control exclusivo.
6. Frescura vs tolerancia a fallos: contadores pueden bloquear operaciones tras rollback, snapshot o failover; modelar recuperación.
7. Defensa en profundidad vs complejidad: controles adicionales pueden crear bypasses y fallos de configuración; medir cobertura y coste operacional.

## L7. Perspectiva adversarial

- Confidencialidad: IDOR, escalada, exfiltración, canal lateral, fuga en logs/backups.
- Integridad: tampering, race condition, replay, rollback, supply-chain compromise y alteración de logs.
- Disponibilidad: agotamiento, DDoS, dependencia común, ransomware y corrupción.
- Autenticidad: spoofing, robo de claves, certificado indebido y token confusion.
- Accountability: cuentas genéricas, reloj manipulado y borrado de evidencia.
- Frescura: replay, nonce reuse, retraso y reordenamiento.

Cada abuso debe registrar precondiciones, capacidad adversaria, activo, transición, detección, impacto, mitigación, residual y evidencia.

## L8. Investigación

Pregunta: ¿qué combinación preserva integridad y disponibilidad bajo particiones, reintentos y recuperación sin abrir una ventana de replay?

Hipótesis falsable: para un workload y modelo de fallos definidos, idempotency keys + secuenciación persistente + reconciliación reducen operaciones duplicadas frente a reintentos sin esos controles, con coste medible de latencia/almacenamiento.

Variables independientes: secuenciación, idempotencia, persistencia, failover. Dependientes: duplicados, pérdida, latencia y recuperación. Controlar carga, topología, tasa de particiones, versión y patrón de reintento. Amenazas a validez: workload sintético, modelo incompleto, sesgo de implementación y pocas repeticiones. No presentar hipótesis como resultado.

## L9. Laboratorio conceptual

Servicio de órdenes ficticio: cliente autenticado, API de autorización/frescura, motor transaccional, ledger, auditoría, réplica y backup. Escenarios: orden repetida, nonce reutilizado, timeout tras commit, failover desactualizado, reloj desincronizado, clave revocada, lectura no autorizada y saturación.

Dataset: escenario, estado inicial, acción, precondiciones, ground truth, resultado esperado, traza, métrica, criterio y limitaciones. Separar desarrollo y evaluación. Diseño conceptual no cuenta como laboratorio ejecutado.

## L10. Evaluación

- Confidencialidad: lecturas no autorizadas exitosas / intentos relevantes; cobertura de rutas.
- Integridad: alteraciones no detectadas, transacciones inconsistentes, duplicados y corrupción no recuperada.
- Disponibilidad: SLO por función/población y ventana.
- Autenticidad: mensajes falsificados o claves inválidas aceptados.
- Accountability: acciones críticas atribuibles y evidencia íntegra.
- Frescura: replay o mensajes fuera de ventana aceptados.
- Privacidad: problemas para individuos derivados de acciones de datos.
- Resiliencia: funciones preservadas, RTO/RPO logrados e integridad tras recuperación.

Reportar denominadores, condiciones, incertidumbre, falsos positivos/negativos, cobertura y sesgos. No colapsar propiedades en un único score.

## L11. Skill conceptual

**FOUNDATIONS.SECURITY-PROPERTY-REQUIREMENTS**

Entradas: misión, activo, función, actor, contexto, amenaza, impacto y restricciones. Proceso: identificar propiedad; formular invariante; enumerar mecanismos; modelar conflictos; definir pruebas/evidencia; documentar residual. Salidas: requisitos verificables, matriz propiedad-control-evidencia, amenazas y plan de evaluación. Errores: requisito no medible, confundir mecanismo con garantía, asumir independencia y omitir excepciones. Parada: falta de autoridad para aceptar riesgo, experto safety/legal ausente o modelo incompleto. Estado: conceptual, no promovida ni ejecutada.

## L12. Trazabilidad

Vincular requisito, propiedad, amenaza, control, implementación, prueba, resultado, fuente y versión. Reabrir ante cambios de arquitectura, protocolo, amenaza, estándar o incidente.

## Enseñar

Secuencia: sistema bancario de órdenes; identificar CIA; añadir orden firmada; analizar autenticidad, autorización y no repudio; repetir solicitud tras timeout; introducir idempotencia/replay; simular pérdida regional; derivar invariantes y pruebas negativas.

Ejercicio: explicar por qué una firma válida no garantiza autorización, integridad del estado final ni no repudio jurídico completo.

## Explicar

Contraejemplos que el estudiante debe razonar:
- Hash correcto no prueba que el dato original fuera verdadero.
- TLS no garantiza autorización sobre cada objeto.
- Firma válida no demuestra autoridad del firmante.
- Dos regiones no garantizan disponibilidad si comparten identidad, DNS o plano de control.
- Log append-only no garantiza accountability con cuentas compartidas o reloj manipulable.
- Backup cifrado no garantiza recuperación si se pierde la clave.

## Analizar

Caso: despacho de ambulancias firma órdenes, replica en dos regiones y registra acciones. Tras una partición llegan dos órdenes incompatibles con la misma secuencia; un operador usa una cuenta compartida para restaurar el servicio.

Analizar propiedades preservadas/perdidas, significado probatorio de la firma, replay/split-brain, accountability, prioridad contextual entre disponibilidad e integridad, reconciliación, modo degradado, autoridad de decisión y pruebas.

## Diseñar

Diseñar flujo con identidad individual, autorización por función/atributo, firma/MAC y gestión de claves, nonce/sequence e idempotency key, transacción/ledger, logs protegidos y sincronizados, límites de tasa, modo degradado, recuperación de claves/estado y segregación de funciones.

Entregables: modelo de estados, invariantes, DFD, amenazas, requisitos, pruebas positivas/negativas, trade-offs y argumento de assurance.

## Rúbrica en frío

| Dimensión | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Enseñar | Ausente | Enumera | Define | Secuencia y corrige | Transfiere a dominio nuevo |
| Explicar | Incorrecto | Sin causalidad | Parcial | Mecanismos y supuestos | Formalismo, contraejemplos y límites |
| Analizar | Ausente | Superficial | Un fallo | Dependencias y trade-offs | Alternativas, incertidumbre y sensibilidad |
| Diseñar | Genérico | Lista controles | Parcial | Requisitos y verificación | Solución demostrable y residual |
| Fuentes | Sin fuentes | Referencias vagas | Localizadas | Alcance y trazabilidad | Crítica y revisión independiente |

Umbral interno: mínimo 3 en cada dimensión; 4 y revisión independiente para sostener pericia. No se ha administrado la evaluación.

## Fuentes y limitaciones

1. NIST SP 800-160 Vol. 1 Rev. 1 final (noviembre 2022): página oficial, abstract, alcance y relación entre seguridad como propiedad emergente y safety/reliability/availability. Lectura integral pendiente. https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final
2. NIST SP 800-53 Rev. 5 / Release 5.2.0: consultar controles concretos antes de derivar requisitos.
3. NIST Privacy Framework 1.0 (2020): versión final consultada parcialmente.
4. NIST Privacy Framework 1.1 Initial Public Draft, CSWP 40 IPD (14 abril 2025): secciones 1.2.1–1.2.3, Core y Appendix D consultados. Es borrador, no versión final ni obligación legal. Explica que el riesgo de privacidad puede surgir sin incidente cibernético y que IA puede introducir problemas de privacidad en su ciclo de vida. https://doi.org/10.6028/NIST.CSWP.40.ipd
5. NIST CSRC Glossary: entradas seleccionadas; interpretar cada definición en contexto de su publicación fuente.

Pendiente: lectura integral de SP 800-160/800-53 y normas sectoriales; legislación colombiana; evaluación administrada; revisión independiente. Sin evidencia experimental u operacional.
