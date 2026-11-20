# Foundations FND-01.01 / FND-01.02 — Desarrollo integrado por las doce capas

**Fecha:** 2026-11-20  
**Estado:** desarrollo teórico ampliado en borrador; pendiente auditoría de contenido, lectura integral, evaluación administrada y revisión independiente.  
**Subtemas:** FND-01.01 y FND-01.02.  
**Regla:** este documento mapea las doce capas obligatorias. No cambia los estados de madurez ni convierte evidencia sintética en validación operacional.

## L1 — Fundamentos teóricos

### FND-01.01
El sistema debe analizarse como un sistema socio-técnico con funciones, personas, software, hardware, datos, operadores, proveedores, infraestructura y entorno. Security protege activos y misión frente a acciones no autorizadas; safety controla riesgos de daño inaceptable; privacy controla riesgos del tratamiento de datos; reliability se refiere al desempeño correcto bajo condiciones/tiempo definidos; availability a la prestación oportuna; resilience a sostener, recuperar y adaptar funciones esenciales.

Estas propiedades son emergentes y dependientes del contexto. No se infieren de un componente, una certificación aislada o una métrica única. Una arquitectura puede cumplir C/I/A y generar un hazard; una función de safety puede fallar por una actualización auténtica; un backup puede restaurar disponibilidad y conservar credenciales comprometidas.

### FND-01.02
CIA describe objetivos de protección de información y servicios:
- C: evitar divulgación a actores no autorizados.
- I: evitar modificación/destrucción impropia y preservar estados/transiciones definidos.
- A: asegurar acceso/uso oportuno por actores autorizados bajo requisitos de servicio.

Las propiedades extendidas deben clasificarse, no sumarse de forma acrítica: autenticidad, autorización, accountability, non-repudiation, provenance y freshness son propiedades de identidad, evidencia o estado; privacy, safety, reliability y resilience pertenecen a modelos relacionados pero distintos. “CIA+” es una etiqueta didáctica, no una norma universal.

## L2 — Modelos matemáticos y formales

### FND-01.01
Definir el riesgo de safety, security y privacy por separado:
- Safety: R_s = f(hazard, exposición, secuencia causal, severidad, salvaguardas, incertidumbre).
- Security: R_c = f(misión, amenaza, vulnerabilidad, exposición, consecuencia, controles, incertidumbre).
- Privacy: R_p = f(acción de datos, persona, finalidad, contexto, escala, consecuencia, controles).

No asumir que escalas ordinales son cardinales ni que probabilidad × impacto produce una probabilidad calibrada. Documentar intervalos, incertidumbre, supuestos y dependencias.

Para una función de tiempo hasta fallo T, reliability R(t)=P(T>t). La disponibilidad simple A=MTBF/(MTBF+MTTR) requiere estados operativos/reparación bien definidos y supuestos de estacionariedad; no es universal. Resilience debe medirse como vector: función esencial sostenida, degradación, tiempo de detección, recuperación confiable y adaptación.

### FND-01.02
Expresar propiedades como invariantes o predicados sobre actor, objeto, operación, estado y tiempo:
- C(a,o,t): actor a no obtiene información o inferencias protegidas de o sin autorización vigente.
- I(o,s0→s1): toda transición de estado de o está autorizada, validada y preserva invariantes.
- A(f,a,t): función f está disponible al actor autorizado dentro del plazo y calidad definidos.
- Authenticity(m): el origen declarado del mensaje m está vinculado a una identidad válida bajo una cadena de confianza.
- Freshness(m): m pertenece a la ventana/contador esperado y no es replay.
- Accountability(e): evento e puede atribuirse con identidad, contexto, tiempo e integridad de registro suficientes.

Estas expresiones son esquemas de requisitos, no una especificación formal completa. Cada proyecto debe definir semántica, modelo de amenaza, política, trust anchors y condiciones de fallo.

## L3 — Arquitectura y funcionamiento

### FND-01.01
Arquitectura de referencia conceptual:

1. Capa de misión y personas afectadas: objetivos, funciones esenciales, límites de daño, requisitos de privacidad.
2. Capa física/proceso: actuadores, sensores, interlocks, energía y condiciones ambientales.
3. Capa de control: controladores de seguridad, controladores operativos y modos degradados.
4. Capa de seguridad: identidad, autorización, segmentación, protección de configuración y monitorización.
5. Capa de datos: clasificación, flujos, almacenamiento, telemetría, backups y retención.
6. Capa de resiliencia: redundancia, recuperación, reconstrucción de confianza y adaptación.
7. Capa de assurance: claims, requisitos, pruebas, evidencias, responsables y revisión.

Los límites de confianza deben señalarse en cada interfaz: operador-controlador, proveedor-cliente, nube-OT, identidad-servicio, telemetría-SIEM, backup-producción y soporte remoto. Las dependencias compartidas deben representarse explícitamente.

### FND-01.02
Arquitectura de datos y confianza:
- productor/sensor → validación de origen → transporte autenticado → validación de integridad/frescura → autorización → procesamiento → registro de auditoría → almacenamiento/retención → consumidor.
- El canal criptográfico protege propiedades del canal; no sustituye validación semántica, autorización de negocio ni verificación de safety.
- La identidad requiere ciclo de vida: proofing, emisión, almacenamiento, rotación, revocación, expiración y recuperación.
- El log requiere identidad individual, reloj confiable, integridad, control de acceso, retención y minimización.

## L4 — Estándares, marcos y metodologías

### FND-01.01
Seleccionar por alcance:
- NIST SP 800-160 Vol. 1 Rev. 1: ingeniería de sistemas seguros y assurance.
- NIST SP 800-160 Vol. 2 Rev. 1: resiliencia cibernética.
- NIST CSF 2.0: resultados de gestión del riesgo cibernético.
- NISTIR 8062: objetivos de ingeniería de privacidad.
- IEC 61508: functional safety de sistemas E/E/PE.
- IEC 62443: seguridad de sistemas de automatización y control industrial.
- IEC TR 63069: coordinación safety/security.
- ISO 26262: safety funcional en su ámbito automotriz.
- ISO 22316: resiliencia organizacional.

No inferir obligatoriedad en Colombia sin verificar adopción, regulación sectorial, contrato o autoridad competente. Los estados de edición y acceso se consultan en source_registry.json.

### FND-01.02
- FIPS PUB 199: C/I/A y niveles de impacto para información/sistemas federales de EE. UU.; no es una taxonomía universal.
- NIST CSF 2.0: seis funciones de resultados; no prescribe controles únicos.
- NIST SP 800-53 Rev. 5: catálogo de controles de seguridad y privacidad.
- NIST SP 800-160: ingeniería y assurance del sistema.
- NISTIR 8062: privacidad por acciones de datos.
- IEC 62443: requisitos de seguridad para IACS.
- RFC y estándares criptográficos deben seleccionarse por protocolo, algoritmo, ciclo de vida y modelo de confianza, no por popularidad.

## L5 — Implementación técnica

### FND-01.01
Patrón de decisión para un estado de emergencia:
1. detectar condición de emergencia mediante fuente definida y validada;
2. activar política de seguridad física;
3. preservar egress seguro mediante mecanismo independiente;
4. restringir ingress no autorizado;
5. registrar el evento con minimización de datos;
6. exigir revisión posterior y restablecimiento controlado.

No depender de un único controlador o proveedor para safety y security si una causa común puede anular ambas. La separación física/lógica debe justificarse mediante análisis de independencia.

Patrón de recuperación confiable:
1. aislar entorno de restauración;
2. verificar procedencia y hashes de artefactos;
3. reconstruir identidad y rotar secretos;
4. validar configuración y estado de datos;
5. comprobar dependencias y telemetría;
6. habilitar misión por fases;
7. mantener criterio de parada y rollback.

### FND-01.02
Patrón de verificación de un artefacto:
1. validar formato y algoritmo permitido;
2. verificar cadena de certificados y propósito de clave;
3. verificar estado de revocación y ventana temporal;
4. verificar firma y hash;
5. validar versión, procedencia y política de build;
6. analizar contenido y dependencias;
7. probar comportamiento en entorno autorizado;
8. comprobar efecto de misión y safety.

La firma y el hash cubren solo partes de la afirmación. No autorizan el despliegue por sí solos.

Patrón de evento auditable:
- identidad individual y contexto;
- acción y recurso;
- decisión de autorización;
- timestamp con fuente confiable;
- integridad y retención del registro;
- minimización de datos;
- correlación y revisión.
Los logs no deben capturar secretos ni datos personales innecesarios.

## L6 — Análisis avanzado y casos límite

### FND-01.01
Analizar como mínimo:
- Fail-secure que bloquea egress durante incendio: seguridad de acceso puede crear hazard.
- MFA sin recuperación de emergencia: reduce suplantación, pero puede impedir respuesta crítica.
- Patching urgente en sistema de control: reduce exposición, pero puede introducir fallo sistemático o indisponibilidad.
- Redundancia con identidad/DNS/energía compartidos: causa común invalida independencia.
- Backup con credenciales persistentes: restaura servicio sin restaurar confianza.
- Telemetría completa: mejora detección pero aumenta riesgo de privacidad y reidentificación.

### FND-01.02
Analizar como mínimo:
- Firma válida de software vulnerable: autenticidad sí, seguridad no.
- Hash válido de dato de sensor mal calibrado: integridad del archivo sí, verdad física no.
- Datos cifrados reutilizados para perfilado no esperado: confidencialidad sí, privacidad no.
- Servicio con uptime alto que permite acción no autorizada: disponibilidad sí, security no.
- Logs completos con cuenta compartida: trazabilidad parcial, accountability insuficiente.
- Non-repudiation basada en clave comprometida: atribución no concluyente.

## L7 — Perspectiva de seguridad

### FND-01.01
El threat model debe incluir adversario externo, insider, proveedor, error humano, fallo de componente, condición ambiental y combinación de eventos. La hazard analysis debe identificar daño y secuencias causales; la threat analysis debe identificar acciones intencionales y rutas de abuso. La privacy analysis debe identificar acciones de datos y consecuencias para personas.

El modelo integrado debe enlazar:
hazard/threat/failure/data action → escenario → función afectada → consecuencia → control → método de verificación → evidencia → riesgo residual.

### FND-01.02
Evaluar ataques contra:
- identidad y credenciales;
- emisión y revocación de certificados;
- replay, downgrade y sustitución de claves;
- manipulación de logs y tiempo;
- abuso de privilegios;
- exfiltración e inferencia;
- agotamiento de recursos;
- datos falsos firmados por fuente comprometida;
- uso secundario de datos y reidentificación.

Los controles se asignan a escenarios concretos. “Cifrado” no es respuesta suficiente para todas las amenazas.

## L8 — Investigación científica

### FND-01.01
Preguntas investigables:
1. ¿Qué patrones arquitectónicos reducen conflictos safety/security sin introducir dependencias comunes?
2. ¿Qué métricas de resiliencia predicen recuperación confiable y no solo restauración de servicio?
3. ¿Cómo cuantificar el coste de privacidad de la telemetría de seguridad?
4. ¿Qué evidencias permiten demostrar independencia de redundancia?
5. ¿Cómo cambian los resultados cuando se combinan fallos accidentales y adversariales?

Hipótesis deben especificar población/sistema, variable, métrica, comparación, confusores y criterio de falsación. Threat models y hazard logs no son datos empíricos por sí mismos.

### FND-01.02
Preguntas investigables:
1. ¿Qué controles detectan mejor replay y pérdida de freshness bajo relojes no confiables?
2. ¿Cómo medir la diferencia entre integridad de registro y exactitud semántica?
3. ¿Qué diseños de logging preservan accountability y minimizan datos personales?
4. ¿Qué condiciones de gestión de claves hacen defendible una afirmación de non-repudiation?
5. ¿Cómo cambia la disponibilidad bajo ataques de agotamiento y dependencias compartidas?

Amenazas a validez: datasets sintéticos, sesgo de selección, ground truth incompleto, distribución distinta a producción, supuestos de independencia, reloj y claves simuladas.

## L9 — Laboratorios y datasets

El runner incluye LAB-FND-01A a LAB-FND-12A. Para FND-01.01/01.02 son especialmente relevantes:
- LAB-FND-08A: safety/security y egress.
- LAB-FND-09A: privacidad/confidencialidad.
- LAB-FND-10A: recuperación y confianza.
- LAB-FND-11A: redundancia y causa común.
- LAB-FND-12A: integridad/autenticidad frente a verdad.

Dataset sintético mínimo por escenario:
- scenario_id;
- system_boundary;
- actor/role;
- asset/function;
- threat/hazard/failure/data_action;
- preconditions;
- expected_safe_state;
- observed_state;
- evidence_refs;
- ground_truth;
- limitations.

Los resultados de CI validan determinismo y aserciones del modelo. No validan la física, la ley, el entorno operacional ni la seguridad de un producto real.

## L10 — Evaluación y benchmarks

Para ambos subtemas, la evaluación en frío debe puntuar:
- precisión conceptual;
- calidad del modelo y supuestos;
- selección de estándares por alcance;
- diseño de controles y trade-offs;
- evidencia, métricas e incertidumbre;
- detección de contraejemplos;
- trazabilidad y límites.

Criterios críticos de rechazo: confundir safety/security, privacy/confidentiality, authenticity/truth, integrity/correctness o availability/resilience. Una respuesta que no identifica supuestos no puede obtener puntuación máxima.

Los instrumentos FND-01.01 V2 y FND-01.02 V1 están preparados; no administrados. No hay respuestas originales, puntuación individual, segundo evaluador ni adjudicación. Por tanto, no existe resultado de evaluación.

## L11 — Conocimiento operativo y Skills

Las especificaciones de Skills candidatas están en knowledge/skills/candidates:
- SKILL-FND-01-01-INTEGRATED-PROPERTY-ANALYSIS.
- SKILL-FND-01-02-CIA-PROPERTY-ASSESSMENT.

Cada candidata declara patrón de tarea, precondiciones, entradas, método, salidas, validación, límites y promoción. Se indexan como documentos de conocimiento, pero no se registran en skillbook ni se ejecutan como Skills activas.

La promoción requiere evidencia de ledger, dos ejecuciones supervisadas exitosas, revisión por rol distinto, evidencia íntegra y aprobación firmada según docs/SKILL_PROMOTION.md. No inferir competencia a partir de un documento.

## L12 — Trazabilidad, mantenimiento y ciclo de vida

Cada claim debe incluir:
- identificador estable;
- subtema y capa;
- fuente y versión;
- sección/página revisada;
- tipo de revisión (metadatos, abstract, secciones, texto integral);
- licencia y restricciones;
- método de verificación;
- evidencia y hash;
- limitación y fecha de revisión;
- responsable de aprobación.

Estados de fuente:
- official_metadata_only_content_not_accessed;
- official_metadata_and_abstract_reviewed;
- selected_sections_reviewed;
- full_text_reviewed;
- superseded/withdrawn.

No colapsar esos estados en “fuente validada”. Programar revisión cuando cambien estándares, vulnerabilidades, regulación, proveedores o supuestos. Mantener historial de versiones y no sobrescribir evidencia previa.

## Matriz de evidencia por subtema

| Elemento | FND-01.01 | FND-01.02 |
|---|---|---|
| Topic base | SECURITY_SAFETY_PRIVACY_RELIABILITY_RESILIENCE.md | SECURITY_PROPERTIES_CIA_EXTENDED.md |
| Crosswalk/síntesis | FND_01_01_SAFETY_SECURITY_PRIVACY_RELIABILITY_RESILIENCE_CROSSWALK_2026-11-20.md | FND_01_02_PRIMARY_SOURCE_SYNTHESIS_2026-11-20.md |
| Evaluación | FND-01-01_COLD_ASSESSMENT_V2.md | FND_01_02_COLD_ASSESSMENT_V1.md |
| Labs | LAB-FND-08A, 10A, 11A | LAB-FND-09A, 12A |
| Skill candidata | INTEGRATED_PROPERTY_ANALYSIS | CIA_PROPERTY_ASSESSMENT |
| Estado | L1–L12 in_progress; T0/O0 | L1–L12 in_progress; T0/O0 |

## Dictamen de esta expansión

La presencia de contenido en las doce capas está documentada para ambos subtemas. Esto no equivale a cerrar sus no conformidades. La lectura integral, la evaluación administrada, la revisión independiente y la validación operacional siguen pendientes. No promover T0/O0 ni marcar capas passed en esta revisión.
