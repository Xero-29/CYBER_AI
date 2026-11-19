# FND-01.01 — Seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia

**Unidad curricular:** Foundations / FND-01 Propiedades, conceptos y modelos de seguridad  
**Estado:** desarrollo inicial evaluable; no aprobado.  
**Madurez:** T0 / O0. Borrador documental no evaluado; no se asigna T1 hasta cumplir los criterios de evidencia y evaluación en frío.  
**Norma:** `knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md`.

## Objetivos de aprendizaje

Al terminar esta unidad, el lector debe poder:
1. Diferenciar seguridad de la información/ciberseguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia sin tratarlas como sinónimos.
2. Identificar qué sujeto, activo, función, población y contexto protege cada propiedad.
3. Analizar conflictos y dependencias entre propiedades en un sistema concreto.
4. Derivar requisitos verificables y diseñar una solución con controles, métricas, evidencia y riesgo residual.

Prerrequisitos: sistema, activo, stakeholder, misión, dato, amenaza, evento, control y riesgo. La unidad debe enseñar estos términos si el lector aún no los domina.

## L1. Fundamentos teóricos

**Seguridad** es una condición de protección de sistemas, información y misión frente a circunstancias o eventos adversos. No se reduce a impedir intrusiones: incluye prevención, detección, corrección y recuperación. En ciberseguridad, la protección suele analizarse mediante confidencialidad, integridad y disponibilidad (CIA), pero autenticidad, responsabilidad, trazabilidad, privacidad, confiabilidad y safety pueden ser propiedades críticas adicionales. El glosario de NIST advierte que cada definición debe interpretarse en el contexto de su documento fuente; no existe una definición aislada que sustituya el contexto sectorial.

**Safety (seguridad funcional / ausencia de daño inaceptable)** trata los peligros y daños no aceptables a personas, bienes o ambiente, incluidos accidentes, fallos y combinaciones de condiciones. No presupone adversario. Un atacante puede provocar un peligro, pero un sistema puede ser inseguro para safety sin que exista ataque: por ejemplo, un sensor defectuoso puede producir una orden física peligrosa.

**Privacidad** trata el impacto del procesamiento de datos sobre individuos, su autonomía y sus expectativas legítimas. No es equivalente a secreto ni a confidencialidad. Un conjunto de datos puede estar cifrado y tener acceso restringido, pero su recolección, inferencia, retención o uso puede ser desproporcionado o inesperado. NIST Privacy Framework 1.0 organiza el tratamiento de riesgo de privacidad a lo largo del ciclo de vida de datos y define objetivos de ingeniería como predictability, manageability y disassociability. Estos objetivos no sustituyen obligaciones legales locales.

**Confiabilidad (reliability)** describe la probabilidad o capacidad de que un elemento cumpla una función especificada durante un intervalo y bajo condiciones definidas. Requiere función, condiciones, población, horizonte y criterio de éxito. Un servicio puede ser confiable en su comportamiento funcional y aun así inseguro frente a un adversario.

**Disponibilidad (availability)** se refiere a que un servicio o recurso sea accesible y utilizable cuando lo necesita una entidad autorizada. Debe expresarse con ventana temporal, población, servicio, dependencias, nivel de servicio y degradación aceptable. Un porcentaje sin denominador ni ventana no tiene interpretación operativa suficiente.

**Resiliencia** es la capacidad de anticipar, resistir, operar en modo degradado, recuperarse y adaptarse ante perturbaciones, preservando funciones esenciales dentro de límites temporales y de impacto aceptables. No equivale a tener backups: requiere que la organización pueda recuperar datos, identidades, claves, configuraciones, dependencias y procesos.

Estas propiedades se solapan, pero responden a preguntas distintas:
- Seguridad: ¿qué daños o compromisos debemos prevenir, detectar, contener y corregir?
- Safety: ¿qué peligros pueden causar daño físico/ambiental y cómo se mantienen dentro de límites tolerables?
- Privacidad: ¿qué efectos produce el procesamiento de datos sobre individuos y cómo se gobiernan?
- Confiabilidad: ¿la función cumple consistentemente lo especificado?
- Disponibilidad: ¿está utilizable cuando se necesita?
- Resiliencia: ¿qué funciones sobreviven y cómo se recupera/adapta el sistema tras una perturbación?

## L2. Fundamentos matemáticos y formales

Una propiedad debe expresarse respecto de un sistema (S), contexto (C), horizonte (T), población (P), función (F) y criterio (K). Sin estas variables, expresiones como “es seguro”, “es confiable” o “tiene alta disponibilidad” son incompletas.

### Confiabilidad
Para un sistema reparable/no reparable, bajo supuestos apropiados, la confiabilidad de misión puede expresarse como:
[
R(t)=P(	ext{función especificada sin fallo durante }[0,t]mid C)
]
No asumir tasa de fallo constante ni distribución exponencial sin evidencia. Si se usa (R(t)=e^{-lambda t}), declarar el supuesto de tasa de fallo constante y condiciones estacionarias.

### Disponibilidad
La disponibilidad estacionaria simplificada de un componente reparable puede aproximarse por:
[
A=rac{MTBF}{MTBF+MTTR}
]
Solo es una aproximación bajo definiciones y condiciones consistentes. No incluye automáticamente mantenimiento programado, dependencias, degradación parcial, fallos de causa común ni distribución de tiempos. La disponibilidad de un servicio compuesto depende de su topología y de la correlación entre fallos; no multiplicar disponibilidades de componentes si no se justifica independencia.

### Riesgo
No reducir riesgo a un producto universal de escalas. Para escenarios discretos y probabilidades defendibles:
[
E[Lmid C,T]=sum_i P(S_imid C,T)L_i
]
La pérdida esperada no representa por sí sola impactos extremos, distribución, incertidumbre epistémica ni consecuencias no monetizables.

### Safety
El análisis puede usar hazard, exposición, severidad, controlabilidad y barreras según el método sectorial. No importar una fórmula de riesgo cibernético a safety sin justificar el modelo, los supuestos y la autoridad competente.

### Privacidad
El riesgo de privacidad debe relacionar acciones de datos con problemas que pueden experimentar individuos y su impacto. No inferir riesgo individual solo a partir de una probabilidad de intrusión. Deben examinarse finalidad, contexto, expectativa, población, inferencias, correlación y posibilidad de asociación/reidentificación.

## L3. Arquitectura y funcionamiento interno

Las propiedades atraviesan capas técnicas y organizativas:
- Personas, roles, procesos y decisiones.
- Aplicaciones, servicios, APIs y flujos.
- Identidad, autorización y sesiones.
- Datos, metadatos, modelos, backups y logs.
- Infraestructura, red, energía, hardware y proveedores.
- Controles, telemetría, continuidad y recuperación.

Para cada flujo se debe identificar: origen, destino, propósito, tipo de dato, clasificación, actor, autoridad, transformación, almacenamiento, retención, dependencia, fallo posible y evidencia.

Un diagrama útil no es solo un dibujo de cajas: representa límites de confianza, flujos de datos y autoridad, dependencias, rutas de degradación y recuperación. Una solución de seguridad puede degradar disponibilidad; una solución de disponibilidad puede aumentar exposición; una optimización de observabilidad puede crear un nuevo repositorio de datos sensibles.

## L4. Estándares y metodologías

- **NIST CSRC Glossary:** reúne definiciones de distintas publicaciones. El propio glosario indica que cada término debe leerse en el contexto de su fuente y que la agregación no convierte todas las definiciones en una definición universal.
- **NIST Privacy Framework 1.0 (2020):** marco voluntario para gestionar riesgo de privacidad empresarial; introduce objetivos de ingeniería y ciclo de vida de datos. No es ley ni certificación.
- **NISTIR 8062 (2017):** introduce ingeniería de privacidad y modelo de riesgo de privacidad; útil para distinguir riesgo para individuos del riesgo organizacional.
- **NIST SP 800-160 Vol. 1 Rev. 1:** integra trustworthiness y seguridad en ingeniería de sistemas a lo largo del ciclo de vida.
- **NIST SP 800-37 Rev. 2:** integra gestión de seguridad y privacidad en ciclo de vida y decisiones de riesgo.
- **NIST SP 800-53 Rev. 5 / Release 5.2.0:** catálogo de controles adaptables; seleccionar un control no demuestra que esté implementado ni que sea eficaz.
- **Safety sectorial:** aplicar normas y métodos pertinentes a la industria (p. ej., proceso industrial, transporte, dispositivos médicos); verificar edición, jurisdicción y alcance antes de declarar conformidad.

No confundir marco de resultados, guía de ingeniería, catálogo de controles, norma certificable, regulación y método de análisis de peligros.

## L5. Implementación técnica

Convertir las propiedades en requisitos verificables. Ejemplos:
- Seguridad: “toda escritura sobre el recurso R exige autorización vigente del principal P y se registra una decisión trazable”.
- Safety: “si la señal del sensor supera el rango validado o pierde integridad, el controlador entra en estado seguro definido por el análisis de peligros”.
- Privacidad: “la aplicación no conserva el atributo X más allá del propósito y plazo aprobados; el borrado incluye réplicas y exportaciones bajo control”.
- Confiabilidad: “la función F cumple el comportamiento especificado durante el intervalo T bajo el perfil de carga C”.
- Disponibilidad: “el servicio S satisface el SLO para la población P en la ventana W, incluyendo dependencias acordadas”.
- Resiliencia: “tras pérdida del componente crítico D, la función esencial E se restaura dentro de RTO, con RPO y validación de integridad definidos”.

Para cada requisito especificar dueño, sistema, condición, métrica, método de verificación, evidencia, excepción y riesgo residual. El requisito no debe prescribir una solución prematuramente si hay alternativas.

## L6. Análisis avanzado

### Conflicto 1: MFA y disponibilidad
MFA resistente a phishing puede reducir apropiación de cuentas, pero la pérdida del autenticador o un proveedor de identidad indisponible puede bloquear funciones críticas. Diseñar recuperación segura, cuentas de emergencia limitadas, múltiples rutas de autenticación y pruebas de revocación; las excepciones no deben convertirse en bypass permanente.

### Conflicto 2: telemetría y privacidad
Registrar prompts, tokens, eventos, identificadores y payloads facilita detección y forense, pero puede aumentar recolección de datos, exposición y retención. Minimizar, seudonimizar, segregar, limitar acceso, definir retención y preservar solo evidencia necesaria. La solución no es “loguear todo”.

### Conflicto 3: fail-safe y continuidad
Un estado fail-closed puede proteger integridad/confidencialidad, pero detener una función esencial. Un fail-open puede preservar disponibilidad y permitir abuso. La decisión depende del activo, consecuencia, modo degradado, safety y autoridad; no existe una regla universal.

### Conflicto 4: redundancia y causa común
Dos instancias redundantes no garantizan resiliencia si comparten región, proveedor, identidad, firmware, configuración o plano de control. Modelar causas comunes y dependencias correlacionadas.

### Conflicto 5: backup y recuperación
Una copia puede estar cifrada con una clave inaccesible, contener corrupción, depender de identidad comprometida o no incluir configuración/metadata. La recuperación exige restauración, validación, aislamiento y confianza en el entorno recuperado.

## L7. Perspectiva de seguridad

La unidad debe reconocer que una propiedad puede ser comprometida por adversario, error, accidente, fallo, proveedor o decisión organizativa. Construir para cada escenario:
1. propiedad afectada;
2. activo, persona o función impactada;
3. causa/evento y precondiciones;
4. barreras preventivas;
5. detección y evidencia;
6. respuesta y contención;
7. recuperación;
8. riesgo residual y decisión responsable.

No confundir control de seguridad con mitigación de safety o privacidad. Puede haber controles comunes, pero cada objetivo necesita análisis de eficacia propio.

## L8. Investigación científica

Pregunta investigable: **¿qué arquitectura de controles permite mantener funciones críticas y minimizar efectos adversos sobre privacidad y seguridad durante fallos de identidad o telemetría?**

Diseño conceptual:
- Unidad de análisis: arquitectura de servicio multi-tenant simulada.
- Factores: estrategia de autenticación, modo fail-open/closed, minimización de logs, redundancia independiente.
- Resultados: acciones no autorizadas, indisponibilidad, exposición de datos, tiempo de recuperación y completitud de evidencia.
- Controles: carga, fallos inducidos, topología, versiones y perfiles de usuario.
- Amenazas a validez: simulación simplificada, dependencia entre fallos, representatividad del workload, sesgo de escenario y generalización.
- No presentar la hipótesis como resultado. La pregunta requiere protocolo y datos antes de cualquier conclusión empírica.

## L9. Laboratorios y datasets

Diseñar un sistema sintético con portal de atención, servicio de identidad, base de datos de perfiles, telemetría y dos dependencias. Crear escenarios controlados: pérdida del IdP, expiración de token, corrupción de backup, log con dato personal, fallo de región y pérdida de proveedor.

Dataset mínimo: escenario, condición inicial, propiedad afectada, ground truth, impacto esperado, controles, salida correcta, riesgo residual y criterio de parada. Usar identidades y datos ficticios; particionar escenarios de desarrollo y evaluación para evitar memorización. La ejecución no está acreditada por este diseño.

## L10. Evaluación y benchmarks

Evaluar por propiedad y escenario; no crear un único score que oculte daños:
- Seguridad: tasa de acciones no autorizadas, bypass, cobertura de rutas y tiempo de detección.
- Safety: peligros no mitigados, violaciones de restricciones y suficiencia de barreras según método sectorial.
- Privacidad: minimización, retención, exposición, reidentificación y cumplimiento de finalidad en el modelo de datos.
- Confiabilidad: probabilidad de cumplir función bajo condiciones/horizonte definidos.
- Disponibilidad: SLO, downtime, degradación, latencia y población afectada.
- Resiliencia: funciones mantenidas, tiempo de recuperación, pérdida de datos, integridad restaurada y recurrencia.

Cada métrica debe declarar fórmula, unidad, denominador, ventana, datos, incertidumbre y exclusiones. Métricas de proceso no prueban outcomes; el uptime no prueba seguridad y el cifrado no prueba privacidad.

## L11. Conocimiento operativo y Skills

Skill candidata: `FOUNDATIONS.PROPERTY-TRADEOFF-ANALYSIS`.

Entradas: misión, sistema, stakeholders, activos, población, funciones críticas, requisitos, dependencias y restricciones.  
Salidas: matriz propiedad–escenario–requisito–control–métrica–evidencia; trade-offs; supuestos; riesgos residuales.  
Precondiciones: alcance y propietario definidos, datos sensibles minimizados, contexto sectorial conocido.  
Validaciones: requisitos verificables, métricas con denominador, conflictos analizados y límites declarados.  
Parada: falta de contexto safety/legal, ausencia de autoridad, sistema crítico fuera de alcance o datos personales reales no autorizados.  
Rollback: retirar recomendaciones no aprobadas y restaurar la versión anterior del diseño.  
Estado: especificación conceptual; no promovida ni ejecutada.

## L12. Trazabilidad y mantenimiento

Registrar fuente, edición, alcance leído, fecha, afirmaciones soportadas, subunidad, requisitos derivados, decisiones, revisión y cambios. Reabrir la unidad ante nuevas definiciones normativas, cambios sectoriales, incidentes, cambios de arquitectura o nuevos requisitos legales. La fuente NIST Glossary es un índice contextual, no una autoridad única para todos los sectores.

## Capacidad 1 — Enseñar

### Secuencia didáctica
1. Presentar un sistema de ejemplo: una clínica digital.
2. Identificar función crítica, datos personales, usuario autorizado, equipo médico y servicio de identidad.
3. Preguntar qué puede salir mal: robo de cuenta, dato excesivo, fallo del servicio, error de sensor, pérdida de backup.
4. Clasificar cada consecuencia por propiedad y explicar solapamientos.
5. Derivar requisitos y métricas para cada propiedad.
6. Comparar una solución que maximiza una propiedad y perjudica otra.

### Errores conceptuales frecuentes
- “Si los datos están cifrados, existe privacidad”: falso; el tratamiento puede ser excesivo o ilegítimo.
- “Si el sistema tiene 99,99% de uptime, es seguro”: falso; disponibilidad no mide autorización ni confidencialidad.
- “Safety es lo mismo que ciberseguridad”: falso; safety analiza peligros y daños, incluso accidentales.
- “Tener backups equivale a resiliencia”: falso; restauración, integridad, identidad y dependencias deben funcionar.
- “Confiabilidad alta implica seguridad alta”: falso; un sistema puede ejecutar de forma muy confiable una función insegura.

### Ejercicio guiado
Una plataforma de telemedicina cifra historiales y tiene 99,95% de disponibilidad, pero conserva datos indefinidamente y el proceso de recuperación de cuenta permite suplantar pacientes. Clasificar al menos tres propiedades afectadas, explicar por qué los controles existentes no bastan y proponer requisitos verificables.

## Capacidad 2 — Explicar

Explica por qué cada afirmación es incorrecta o incompleta:
1. “La confidencialidad protege automáticamente la privacidad”.
2. “La redundancia elimina el riesgo de indisponibilidad”.
3. “Un fail-closed siempre es la opción más segura”.
4. “La confiabilidad es una propiedad absoluta del producto”.

Respuesta razonada esperada: identificar el contexto omitido, la propiedad real, el supuesto oculto, el modo de fallo y la evidencia necesaria. La explicación debe distinguir concepto, mecanismo y decisión contextual.

## Capacidad 3 — Analizar

**Caso nuevo:** una empresa de energía instala un portal remoto para mantenimiento. El portal requiere MFA, almacena grabaciones de sesiones, replica datos en dos regiones y depende de un proveedor de identidad común. Durante una caída regional, el acceso de mantenimiento se bloquea; un administrador propone desactivar MFA y conservar todas las grabaciones para facilitar auditoría.

Análisis exigido:
- Activos, misión y población afectados.
- Propiedades en conflicto: seguridad, safety, privacidad, disponibilidad, confiabilidad y resiliencia.
- Dependencia común entre regiones.
- Riesgos de desactivar MFA y de almacenar grabaciones sin límites.
- Opciones de modo degradado, acceso de emergencia y aprobación.
- Métricas y evidencia para comparar alternativas.
- Condiciones que obligarían a detener la intervención.

No se acepta una respuesta de “activar/desactivar MFA”; debe modelar la función y sus consecuencias.

## Capacidad 4 — Diseñar

Diseñar una arquitectura conceptual de acceso remoto de mantenimiento para un entorno de criticidad elevada:
- Identidades nominales, MFA resistente a phishing y autorización por función/activo/tiempo.
- Acceso de emergencia separado, temporal, auditado y con doble aprobación cuando proceda.
- Plano de identidad redundante o procedimiento degradado con límites explícitos.
- Telemetría minimizada, retención definida y protección de evidencia.
- Segmentación entre portal y redes de control.
- Controles de safety aprobados por ingeniería responsable; no permitir que el portal sea la única barrera de seguridad funcional.
- Recuperación de identidad, claves, configuración y registros.
- Pruebas estáticas de acceso permitido/denegado, pérdida de IdP, expiración, revocación, región caída y recuperación.
- Trade-off documentado, owner y riesgo residual.

Entregables: diagrama de contexto, DFD, flujo de autorización, matriz de requisitos, análisis de modos de fallo, plan de verificación, RTO/RPO propuestos y argumento de assurance.

## Rúbrica de evaluación de esta unidad

| Dimensión | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Enseñar | Ausente | Enumera | Explica caso común | Secuencia didáctica y corrige errores | Enseña transferencia a casos nuevos |
| Explicar | Incorrecto | Definiciones sueltas | Conceptos básicos | Mecanismos y supuestos | Explicación rigurosa con límites y contraejemplos |
| Analizar | No analiza | Opinión | Caso simple | Trade-offs, dependencias e incertidumbre | Caso nuevo complejo con alternativas y sensibilidad |
| Diseñar | No propone | Lista controles | Diseño parcial | Requisitos, arquitectura, verificación y residual | Diseño coherente, robusto, revisable y con assurance |
| Fuentes | Sin procedencia | Referencias vagas | Fuentes identificadas | Alcance leído y afirmaciones trazables | Lectura crítica contrastada y revisión independiente |

**Umbral:** mínimo 3 en cada dimensión para cierre interno de la unidad; 4 y revisión independiente para sostener afirmación de dominio experto. La unidad permanece abierta hasta administrar la evaluación, revisar fuentes críticas y cerrar no conformidades.

## Fuentes y estado de revisión

1. NIST CSRC Glossary, actualización indicada por el sitio: 2026-11-03. Se consultaron definiciones de security y system privacy requirement; el propio glosario advierte que cada definición depende del documento fuente. Consulta de referencia: https://csrc.nist.gov/glossary/term/security y https://csrc.nist.gov/glossary/term/system_privacy_requirement
2. NIST Privacy Framework 1.0 (2020-01-16). Se consultó el texto oficial y fragmentos de objetivos de ingeniería, ciclo de vida de datos y riesgo de privacidad; lectura integral pendiente. https://www.nist.gov/privacy-framework
3. NISTIR 8062 (2017-01). Referencia oficial localizada; lectura integral pendiente. https://csrc.nist.gov/pubs/ir/8062/final
4. NIST SP 800-160 Vol. 1 Rev. 1 (2022-11-16). El registro de Foundations indica secciones seleccionadas revisadas; lectura integral pendiente. https://doi.org/10.6028/NIST.SP.800-160v1r1
5. NIST SP 800-37 Rev. 2 (2018-12-20). El registro de Foundations indica secciones seleccionadas revisadas; lectura integral pendiente. https://doi.org/10.6028/NIST.SP.800-37r2

**Limitación:** no se revisaron en esta iteración normas sectoriales de safety ni el marco legal colombiano aplicable al caso. No declarar conformidad legal o safety. No se realizaron experimentos.


## Actualización de estado documental — Privacy Framework 1.1

La página oficial de NIST presenta PF 1.1 como Initial Public Draft (IPD), publicado el 14 de abril de 2025; PF 1.0 permanece disponible como versión 1.0 final. Por tanto, no se debe citar PF 1.1 como norma final ni asumir que sustituye formalmente a PF 1.0. La IPD alinea su estructura con CSF 2.0 y agrega una sección explícita sobre riesgos de privacidad asociados a IA. Su sección 1.2.1 declara que gestionar riesgo de ciberseguridad contribuye a gestionar riesgo de privacidad, pero no es suficiente: problemas de privacidad pueden surgir sin incidentes cibernéticos. Su sección 1.2.2 analiza problemas derivados de acciones de datos a lo largo del ciclo de vida de IA. Esta distinción fortalece la regla de esta unidad: cifrado y controles de acceso no demuestran por sí solos privacidad. La revisión de la IPD fue dirigida a secciones concretas, no integral; el registro de fuentes mantiene esa limitación.

Fuente: NIST CSWP 40 IPD, *NIST Privacy Framework 1.1*, 2025-04-14, secciones 1.2.1–1.2.3 y apéndices A/D, https://doi.org/10.6028/NIST.CSWP.40.ipd. Estado: revisión selectiva, no lectura integral ni revisión legal colombiana.


## Análisis preliminar de aplicabilidad colombiana

El mapeo condicional de Ley 1581/2012 y, cuando corresponda, Decreto 1575/2007 y Resolución 2115/2007 se documenta en [COLOMBIA_APPLICABILITY_FND_01_01_2026-11-19.md](../COLOMBIA_APPLICABILITY_FND_01_01_2026-11-19.md). La aplicabilidad depende del tratamiento real de datos y de que el proceso esté dentro del ámbito de agua para consumo humano. No es concepto jurídico ni norma general de seguridad funcional. La brecha de safety sectorial y revisión legal independiente permanece abierta.


Soluciones modelo ampliadas para las cuatro capacidades: [FND-01-01_CAPABILITY_WORKED_SOLUTIONS_V1.md](FND-01-01_CAPABILITY_WORKED_SOLUTIONS_V1.md). Estas soluciones son material de referencia para evaluación ciega, no respuestas de un candidato ni prueba de competencia.


## Control de versión de evaluación

La V1 de evaluación en frío queda supersedida: sus ponderaciones sumaban 110 puntos. La V2 corrige los pesos a 100 puntos, añade variantes de transferencia y se acompaña de un protocolo de doble calificación ciega. Ninguna versión se ha administrado; la no conformidad de evaluación sigue abierta.


## Síntesis de fuentes primarias y guía de evaluación V2

La revisión dirigida ampliada de NIST SP 800-160 Vol. 1 Rev. 1, Vol. 2 Rev. 1 y NISTIR 8062 se documenta en [FND_01_01_PRIMARY_SOURCE_SYNTHESIS_2026-11-19.md](../FND_01_01_PRIMARY_SOURCE_SYNTHESIS_2026-11-19.md). Se inspeccionaron secciones sobre propiedades emergentes, confianza composicional, assurance, resiliencia y riesgo de privacidad. Esta revisión mejora el soporte de las afirmaciones, pero no es lectura lineal integral ni revisión de todas las referencias.

La guía reservada de corrección [FND-01-01_ASSESSOR_GUIDE_V2.md](FND-01-01_ASSESSOR_GUIDE_V2.md) complementa el instrumento V2 con anclas por bloque, respuestas mínimas esperadas por variante, criterios de fallas críticas, hoja de puntuación y adjudicación. No debe entregarse al candidato. No es una validación psicométrica ni reemplaza el pilotaje y la doble evaluación independiente.
