# FND-01.01 — Matriz disciplinar de seguridad, safety, privacidad, confiabilidad y resiliencia

**Fecha de revisión:** 2026-11-20  
**Estado:** ampliación teórica dirigida; borrador documental, no aceptación experta.  
**Propósito:** corregir la tendencia a tratar propiedades distintas como sinónimos o como una lista plana de “CIA+”.

## 1. Tesis central

Seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia son propiedades relacionadas, pero no intercambiables. Se evalúan sobre objetos, funciones, actores, contextos y horizontes temporales diferentes. Un sistema puede:

- preservar confidencialidad y aun así procesar datos personales de forma incompatible con la finalidad legítima;
- tener integridad criptográfica y aun así contener datos falsos, incorrectos, incompletos o desactualizados;
- estar disponible y ejecutar una función peligrosa;
- ser confiable en operación nominal y fallar ante una causa común;
- ser redundante sin ser resiliente;
- recuperarse técnicamente y volver a operar desde un estado comprometido;
- ser seguro frente a atacantes y no ser funcionalmente seguro frente a fallos accidentales.

La unidad de análisis no es “el producto” en abstracto: se delimita el sistema de interés, la misión, las funciones esenciales, las personas afectadas, los activos, las interfaces, las dependencias, el entorno operacional y el ciclo de vida.

NIST SP 800-160 Vol. 1 Rev. 1 trata la seguridad como una propiedad de ingeniería del sistema y exige justificar afirmaciones mediante assurance y evidencia. NIST SP 800-160 Vol. 2 Rev. 1 aborda la resiliencia cibernética mediante objetivos de anticipar, resistir, recuperar y adaptar. NISTIR 8062 separa el riesgo de privacidad del mero acceso no autorizado a información. Estas fuentes se complementan; ninguna sustituye a las demás.

## 2. Definiciones operativas y límites

### 2.1 Seguridad de la información y ciberseguridad

En esta unidad, seguridad es la capacidad del sistema, sus componentes y su operación de proteger activos y funciones frente a acciones no autorizadas, maliciosas o indebidas, preservando objetivos de protección definidos para un contexto. La ciberseguridad se trata como gestión del riesgo que afecta sistemas, redes, datos, servicios y misión; no se reduce a instalar controles.

La seguridad es una propiedad emergente del sistema de interés. No se demuestra sumando declaraciones de seguridad de componentes. Las interfaces, estados, transiciones, dependencias, configuración, operadores, proveedores y modos degradados pueden invalidar la confianza que parecía existir en cada componente aislado.

### 2.2 Safety o seguridad funcional

Safety se refiere a controlar riesgos de daño inaceptable a personas, ambiente, bienes o misión debido al comportamiento del sistema, incluidos fallos accidentales, errores humanos, condiciones ambientales y fallos sistemáticos. El peligro (hazard) no requiere un adversario: puede surgir de una combinación de condiciones y decisiones de diseño.

La seguridad funcional es una parte de la safety relacionada con que los sistemas eléctricos, electrónicos o electrónicos programables realicen correctamente las funciones de seguridad requeridas. IEC 61508 es una norma básica de functional safety para sistemas E/E/PE; no es un estándar general de ciberseguridad. La propia documentación IEC distingue las amenazas maliciosas y remite a IEC 62443/ISO/IEC 27000 para security y a IEC TR 63069 para coordinación entre safety y security.

### 2.3 Privacidad

La privacidad no equivale a confidencialidad. La confidencialidad busca evitar divulgación no autorizada; la privacidad también examina si la recolección, inferencia, combinación, retención, uso, compartición o eliminación de datos crea riesgos para personas, incluso cuando el tratamiento fue autorizado y los datos no se filtraron.

NISTIR 8062 propone tres objetivos de ingeniería de privacidad:
- Predictability: permitir que las personas, propietarios y operadores tengan una comprensión fiable de cómo se procesan los datos.
- Manageability: permitir que los datos personales sean administrados de acuerdo con las preferencias, políticas y obligaciones aplicables.
- Disassociability: permitir procesar datos sin asociarlos innecesariamente a individuos o dispositivos.

Estos objetivos son una guía de ingeniería, no una ley colombiana ni un sustituto de análisis jurídico.

### 2.4 Confiabilidad

Confiabilidad (reliability) es la probabilidad de que un sistema o componente realice la función requerida, bajo condiciones especificadas, durante un intervalo definido. La definición solo es útil si se declaran:
- función y criterio de éxito;
- condiciones de operación y ambiente;
- perfil de carga y uso;
- horizonte temporal;
- modos de fallo considerados;
- supuestos de reparación, mantenimiento y dependencia.

Un sistema puede ser altamente confiable al ejecutar de forma consistente una configuración insegura. La confiabilidad no demuestra seguridad, integridad semántica ni ausencia de riesgo.

### 2.5 Disponibilidad

Disponibilidad (availability) es la capacidad de prestar el servicio requerido cuando se necesita, dentro de condiciones y tiempos definidos. La definición debe incorporar quién está autorizado, qué función se presta, con qué calidad y bajo qué límite temporal.

En un modelo reparable simple de estados operativos y reparación, puede aproximarse como A = MTBF / (MTBF + MTTR). Esta relación requiere supuestos de estacionariedad, definición estable de fallo/reparación y un modelo de servicio apropiado; no debe aplicarse automáticamente a sistemas con mantenimiento preventivo, fallos dependientes, degradación gradual, redundancia compleja o fallos adversariales.

Disponibilidad alta no significa continuidad segura de misión: puede ser preferible una parada controlada ante una condición peligrosa o un compromiso de integridad.

### 2.6 Resiliencia

La resiliencia cibernética es la capacidad de sostener funciones esenciales ante adversidad, incluidos fallos, ataques, estrés y compromisos, y de recuperar y adaptar capacidades. NIST SP 800-160 Vol. 2 Rev. 1 organiza los objetivos en:
- Anticipate: anticipar condiciones adversas y sus efectos.
- Withstand: continuar funciones esenciales durante la adversidad.
- Recover: restaurar funciones y capacidades a un estado aceptable.
- Adapt: ajustar el sistema y sus prácticas ante cambios y lecciones.

Resiliencia no es sinónimo de uptime, backup, redundancia o recuperación de proceso. El criterio de recuperación incluye volver a un estado confiable: identidad, integridad, configuración, claves, dependencias, telemetría y misión.

### 2.7 Confianza y assurance

Trustworthiness es una afirmación contextual sobre la confianza justificada en que el sistema cumple su propósito y sus propiedades relevantes. No es una puntuación universal ni una certificación automática. Una afirmación de confianza requiere:
- claim delimitado;
- contexto y supuestos;
- argumento que conecta el claim con la evidencia;
- evidencia pertinente, exacta, creíble y suficiente;
- tratamiento de incertidumbre, límites y cambios.

Un assurance case no es un checklist ni un conjunto de declaraciones de conformidad. Si cambian arquitectura, proveedor, amenaza, operación o entorno, debe revisarse el argumento y su evidencia.

## 3. Modelo de propiedades: no crear una falsa lista CIA+

| Propiedad | Pregunta de ingeniería | Fallo representativo | Evidencia útil | Inferencia que no se permite |
|---|---|---|---|---|
| Confidentiality | ¿Quién puede conocer el dato y bajo qué autorización? | Divulgación, inferencia, exposición lateral | políticas, pruebas de acceso, análisis de flujo, auditoría | confidencialidad no demuestra privacidad |
| Integrity | ¿Qué cambios son autorizados y cómo se detecta corrupción? | alteración, replay, truncamiento, inconsistencia | hashes, firmas, validaciones, reconciliación, procedencia | integridad criptográfica no demuestra verdad |
| Availability | ¿La función correcta está accesible al actor autorizado en el tiempo requerido? | DoS, fallo, agotamiento, dependencia caída | SLI/SLO, pruebas de carga, capacidad, MTTR | disponibilidad no demuestra seguridad ni safety |
| Authenticity | ¿La entidad, origen o mensaje es genuino? | suplantación, credenciales robadas, firma inválida | identidad, certificados, atestación, validación de claves | autenticidad no demuestra que el contenido sea correcto |
| Accountability | ¿Puede atribuirse una acción a una identidad y contexto con evidencia fiable? | cuenta compartida, logs incompletos, reloj alterado | identidad individual, logs protegidos, tiempo confiable | trazabilidad no debe justificar vigilancia ilimitada |
| Non-repudiation | ¿Qué evidencia soporta una atribución y bajo qué supuestos jurídicos/técnicos? | compromiso de clave, identidad débil, firma sin contexto | gestión de claves, sellado temporal, auditoría, procedimiento | una firma no prueba por sí sola intención humana ni efecto jurídico |
| Reliability | ¿La función se ejecuta correctamente durante el horizonte especificado? | fallos aleatorios, sistemáticos, degradación | modelos de fiabilidad, FMEA, datos de campo | fiabilidad no demuestra resistencia a adversarios |
| Safety | ¿Se evita o controla el riesgo de daño inaceptable? | hazard, control inseguro, error humano | hazard log, HAZOP, FTA, STPA, safety case | seguridad informática no demuestra safety |
| Privacy | ¿El tratamiento de datos afecta indebidamente a personas? | finalidad incompatible, inferencia, retención excesiva | mapa de datos, análisis de privacidad, minimización, evaluación de impacto | ausencia de fuga no demuestra privacidad |
| Resilience | ¿La misión esencial puede anticipar, resistir, recuperar y adaptarse? | causa común, recuperación comprometida, pérdida de función | escenarios, ejercicios, pruebas de recuperación, métricas de misión | redundancia no demuestra resiliencia |

CIA son objetivos fundamentales de seguridad de la información. Autenticidad, accountability y non-repudiation son propiedades relacionadas que requieren modelos y supuestos propios. Safety, privacy, reliability y resilience son dimensiones distintas del comportamiento del sistema y no deben presentarse como simples subcategorías de CIA.

## 4. Modelos formales y métricas

### 4.1 Riesgo de safety

Un modelo de safety parte de peligros, condiciones de exposición, secuencias causales, severidad y barreras. Una representación inicial puede ser:
R_safety = función(hazard, exposición, secuencia, severidad, salvaguardas, incertidumbre).

No se debe asumir que una escala ordinal de probabilidad multiplicada por severidad produce una probabilidad calibrada. Los métodos cualitativos y cuantitativos tienen supuestos distintos. El riesgo residual debe ser aceptado por la autoridad competente dentro del contexto normativo y organizacional.

### 4.2 Riesgo de seguridad

Un modelo de ciberseguridad considera activos/funciones, amenaza, capacidad e intención del adversario, vulnerabilidad, exposición, consecuencias, controles y riesgo residual:
R_security = función(misión, amenaza, vulnerabilidad, exposición, consecuencia, controles, incertidumbre).

El modelo debe distinguir amenaza, evento, vulnerabilidad, exposición, impacto y pérdida. No todas las vulnerabilidades son explotables; no todo evento adversarial produce el mismo impacto. La probabilidad suele tener incertidumbre alta y puede ser desconocida.

### 4.3 Riesgo de privacidad

El modelo de privacidad parte de acciones de datos y del contexto de personas, no solo de un atacante:
R_privacy = función(acción de datos, tipo de dato, persona, finalidad, escala, contexto, consecuencia, control).

Las acciones relevantes incluyen recolección, generación, observación, inferencia, agregación, retención, transferencia, uso, divulgación y eliminación. Un tratamiento autorizado puede seguir generando riesgo para la persona.

### 4.4 Confiabilidad y disponibilidad

Para una variable de tiempo hasta fallo T, la función de confiabilidad puede expresarse como R(t) = P(T > t). La tasa de fallo y la distribución dependen de la población, perfil de carga, ambiente, edad, mantenimiento y mecanismo de fallo. MTBF no es vida útil garantizada ni probabilidad de que una unidad concreta sobreviva hasta ese tiempo.

La disponibilidad debe definirse para el servicio y su frontera. Una cifra de disponibilidad que excluye dependencias críticas, mantenimiento, degradación parcial, errores de datos o incidentes de seguridad puede ser engañosa.

### 4.5 Resiliencia de misión

La resiliencia debe expresarse como un vector de objetivos y medidas, no como un único porcentaje:
- tiempo hasta detectar condición adversa;
- fracción de función esencial sostenida;
- degradación máxima tolerada;
- tiempo hasta recuperar función segura;
- integridad del estado recuperado;
- capacidad de adaptación y aprendizaje;
- dependencia de terceros y causa común.

RTO y RPO son parámetros de continuidad/recuperación, no pruebas completas de resiliencia. Un RTO cumplido con datos comprometidos no satisface recuperación confiable.

## 5. Interacciones y conflictos de diseño

### 5.1 Fail-safe, fail-secure y fail-operational

- Fail-safe: ante ciertos fallos, el sistema transita a un estado que reduce el riesgo de daño.
- Fail-secure: ante ciertos fallos, preserva restricciones de seguridad, por ejemplo no conceder acceso.
- Fail-operational: mantiene una función esencial durante un fallo, con degradación controlada.

No son sinónimos y pueden entrar en conflicto. Una puerta de emergencia bloqueada por un control fail-secure puede crear un hazard. Un proceso industrial que sigue operando durante una intrusión puede propagar daño. La elección requiere análisis conjunto de hazard, amenaza, misión, modo de fallo y autoridad de operación.

### 5.2 MFA, acceso de emergencia y disponibilidad

MFA reduce ciertos riesgos de suplantación, pero una implementación sin recuperación segura puede impedir acceso de emergencia o generar cuentas compartidas. Diseñar rutas de emergencia exige identidad individual, autorización temporal, doble control cuando corresponda, registro, expiración, revisión posterior y pruebas de recuperación. La excepción no debe convertirse en bypass permanente.

### 5.3 Telemetría y privacidad

Más telemetría puede mejorar detección y análisis forense, pero también aumentar el riesgo de privacidad, retención, reidentificación y uso secundario. Diseñar por finalidad: campos necesarios, minimización, separación de identificadores, seudonimización, controles de acceso, retención limitada, auditoría y reglas de divulgación. No se debe recopilar “todo por si acaso”.

### 5.4 Redundancia y causa común

Dos componentes no son independientes solo porque sean dos. Pueden compartir proveedor, firmware, identidad, DNS, red, energía, zona física, proceso de actualización, operador o credenciales. La independencia debe argumentarse y comprobarse. FMEA, FTA, análisis de causa común y análisis de dependencias ayudan a evitar que redundancia nominal se confunda con resiliencia.

### 5.5 Backup y recuperación confiable

El backup protege frente a pérdida, pero puede contener malware, datos manipulados, configuraciones vulnerables, identidades comprometidas o claves expuestas. La recuperación exige procedencia, integridad, aislamiento, validación de imágenes, rotación de secretos, reconstrucción de confianza y comprobación de la función de misión. Restaurar un servicio no equivale a restaurar un sistema confiable.

## 6. Método de ingeniería integrada

1. Definir sistema de interés, misión, funciones esenciales, fronteras, actores y personas afectadas.
2. Modelar activos, datos, interfaces, dependencias, modos de operación y transiciones.
3. Identificar peligros (safety), amenazas (security), fallos (reliability), interrupciones (availability/resilience) y acciones de datos (privacy).
4. Analizar escenarios causales y adversariales con métodos apropiados: HAZID/HAZOP, FMEA/FMECA, FTA, STPA, threat modeling, attack trees, TARA y privacy threat modeling. Ningún método es universal ni sustituye juicio experto.
5. Definir requisitos verificables y controles por escenario, con criterios de aceptación y supuestos explícitos.
6. Analizar interacciones, efectos secundarios, degradación, modos seguros, failover, recuperación y causas comunes.
7. Construir assurance case: claims, argumentos, evidencia, supuestos, límites y responsables.
8. Evaluar riesgo residual, incertidumbre, sensibilidad, dependencias y autoridad de aceptación.
9. Mantener trazabilidad entre requisitos, diseño, implementación, pruebas, evidencia, cambios y operación.

## 7. Alcance real de los estándares consultados

| Fuente | Uso válido en esta unidad | Lo que no debe inferirse |
|---|---|---|
| NIST SP 800-160 Vol. 1 Rev. 1 | ingeniería de sistemas seguros, propiedades emergentes, assurance, evidencia y ciclo de vida | no es una certificación automática ni sustituye normas sectoriales |
| NIST SP 800-160 Vol. 2 Rev. 1 | ingeniería de resiliencia cibernética; anticipar, resistir, recuperar, adaptar | resiliencia no se reduce a uptime o backup |
| FIPS PUB 199 | categorización de impacto para información/sistemas federales de EE. UU. usando C/I/A | no es una taxonomía universal de safety, privacidad y resiliencia |
| NIST CSF 2.0 | resultados para gobernar y gestionar riesgo cibernético; seis funciones | no prescribe procedimientos ni controles únicos |
| NISTIR 8062 | objetivos y modelo de ingeniería de privacidad en sistemas federales | no es ley colombiana ni norma final universal |
| IEC 61508 | functional safety de sistemas E/E/PE y ciclo de vida de funciones de seguridad | no cubre por sí sola requisitos normativos completos contra acción maliciosa |
| IEC 62443-2-1:2024 | programa de seguridad del propietario/operador de IACS, políticas, procedimientos y tratamiento de legado | no sustituye análisis de safety |
| IEC 62443-3-3:2013 | requisitos técnicos de seguridad de sistemas IACS y niveles de seguridad | no es una norma de functional safety |
| IEC TR 63069:2019 | guía para aplicar conjuntamente IEC 61508 e IEC 62443 en automatización/control industrial | no sustituye las normas base |
| ISO 26262-1:2018 | vocabulario y marco de functional safety para sistemas E/E de vehículos de carretera en su ámbito | no es una norma general para todo sistema ni norma de ciberseguridad |
| ISO 22316:2017 | guía de resiliencia organizacional, no específica de sector | no es una norma técnica de resiliencia cibernética de producto |
| NASA/SP-2014-612 | conceptos, guías y ejemplos de ingeniería de safety y safety cases | no es una obligación legal general fuera de su contexto |

### Control de vigencia al 2026-11-20

- IEC 61508-1:2010 aparece como edición válida; IEC 61508-1:2026 PRV es una pre-release/FDIS con publicación final prevista para 2027-01-22. No tratar el PRV como edición final publicada.
- ISO/FDIS 22316, edición 2, está en fase de aprobación con fecha prevista 2027-01. Hasta publicación, ISO 22316:2017 sigue siendo la edición publicada.
- ISO/DIS 26262-1, edición 3, está en fase de consulta/enquiry (40.20); ISO 26262-1:2018 sigue siendo la edición publicada.
- La página NIST CSF 2.0 es una publicación final de 2024; el CSF es una taxonomía de resultados y debe complementarse con estándares y prácticas apropiadas.

## 8. Aplicabilidad colombiana: condiciones, no automatismos

- Ley 1581 de 2012: analizar si los datos son personales o hacen identificable a una persona, si existe tratamiento dentro del ámbito aplicable, quién es responsable/encargado y cuál es la finalidad. No todo dato de proceso es dato personal.
- Decreto 1575 de 2007 y Resolución 2115 de 2007: aplicar solo cuando el sistema participa en el ámbito regulado de protección, control, suministro o distribución de agua para consumo humano. No extenderlos a cualquier proceso industrial que use agua.
- Normas IEC/ISO no se convierten automáticamente en ley colombiana por existir. Verificar adopción NTC, reglamento técnico, contrato, licencia, autoridad competente y sector antes de afirmar obligatoriedad.
- Este mapeo es preliminar y no es concepto jurídico ni certificación sanitaria.

## 9. Casos de razonamiento experto

### Caso A — Dosificación remota

Una actualización autenticada y con hash válido modifica un parámetro de dosificación. La autenticidad e integridad de los bytes no demuestran que el parámetro sea correcto ni que su efecto sea seguro. Se requieren validación semántica, límites operativos, hazard analysis, aprobación independiente, rollback confiable y evidencia de prueba.

### Caso B — SaaS multi-tenant

El cifrado y aislamiento protegen confidencialidad, pero una telemetría que combina identificadores, ubicación y actividad puede crear perfiles no esperados. La privacidad requiere finalidad, minimización, retención, transparencia y control del uso secundario; no basta con que no haya fuga.

### Caso C — OT con segmentación

La segmentación reduce rutas de ataque, pero una regla fail-closed puede bloquear una función de seguridad o impedir respuesta de emergencia. El análisis conjunto de IEC 62443 y functional safety debe considerar zonas/conduits, modos degradados, bypass controlado, procedimientos y autoridad.

### Caso D — Recuperación tras ransomware

El sistema vuelve a responder dentro del RTO, pero el backup contiene una cuenta administrativa comprometida y una configuración antigua. La disponibilidad se recuperó; la confianza y la resiliencia no. La aceptación exige reconstruir identidad, claves, configuración, procedencia y estado de datos.

## 10. Evaluación en frío y límites

El estudiante debe poder:
1. distinguir safety, security, privacy, reliability, availability y resilience con contraejemplos;
2. modelar un escenario con hazard, threat, fallo y acción de datos sin mezclarlos;
3. explicar por qué CIA no equivale a trustworthiness;
4. seleccionar estándares según alcance y justificar qué no cubren;
5. construir un argumento claim-argument-evidence y reconocer evidencia insuficiente.

**Estado de fuentes:** revisión dirigida de secciones y metadatos oficiales. No se ha realizado lectura lineal integral de todos los documentos. Las normas ISO/IEC de pago no se han ingerido ni resumido más allá de metadatos/alcance oficiales. No se han ejecutado laboratorios ni pruebas físicas. No se ha obtenido revisión jurídica o disciplinar independiente.

**Dictamen:** esta ampliación fortalece el contenido teórico y corrige equivalencias conceptuales. No cierra las no conformidades de lectura integral, evaluación supervisada ni revisión independiente; no promueve T0/O0.
