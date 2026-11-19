# Revisión dirigida ampliada de fuentes primarias — FND-01.01

**Fecha de consulta:** 2026-11-19.  
**Alcance:** inspección dirigida de secciones y pasajes oficiales; no equivale a lectura lineal integral de todas las publicaciones ni a revisión de toda su bibliografía.  
**Objetivo:** reforzar las afirmaciones centrales de FND-01.01 y separar lo que está respaldado de lo que aún requiere evidencia.

## 1. NIST SP 800-160 Vol. 1 Rev. 1 — Engineering Trustworthy Secure Systems

**Fuente primaria:** https://doi.org/10.6028/NIST.SP.800-160v1r1  
**Estado:** final, noviembre de 2022; PDF oficial de 195 páginas inspeccionado por secciones.

Pasajes consultados:
- Tabla de contenido y alcance, páginas preliminares i–vii.
- Conceptos de sistema y propiedades emergentes: §2 y referencias a la definición de emergencia; el texto incluye safety, security, reliability, resilience y availability como propiedades que solo tienen sentido atribuidas al conjunto (PDF p. 43 / página impresa 31).
- Confianza composicional: Appendix E, §E.7 (PDF p. 102 / impresa 87). La confiabilidad/confianza de una composición debe analizarse sobre el agregado que implementa una función; no se deriva sumando declaraciones de componentes.
- Protección continua: Appendix E, §E.8 (PDF p. 102 / impresa 87).
- Assurance: Appendix F, §F.2 (PDF pp. 121–123 / impresas 106–108). Distingue enfoques axiomático, analítico y sintético; la conformidad declarativa no basta como única base en escenarios complejos. Un assurance case vincula claims, argumentos, evidencia y supuestos.
- Ciclo de vida: Appendices G–K, índice y procesos técnicos/gestión/acuerdo; se consultó la estructura y pasajes seleccionados, no cada proceso completo.

Aplicaciones que se incorporan a la unidad:
1. Las propiedades de sistema son emergentes y deben evaluarse sobre el sistema de interés y su composición, no por atributos aislados de componentes.
2. Dos regiones o sensores nominalmente redundantes no prueban independencia ni confianza composicional; hay que analizar dependencias, interfaces, modos, transiciones y causas comunes.
3. La protección debe ser continua durante estados normales, degradados, mantenimiento y recuperación.
4. Una afirmación “el sistema es seguro/confiable” necesita claim delimitado, argumento, evidencia pertinente y supuestos explícitos. Una certificación o checklist no sustituye el análisis de eficacia para la función concreta.
5. La intensidad de assurance debe corresponder a la pérdida potencial, complejidad, incertidumbre y decisión que se pretende soportar.

## 2. NIST SP 800-160 Vol. 2 Rev. 1 — Developing Cyber-Resilient Systems

**Fuente primaria:** https://doi.org/10.6028/NIST.SP.800-160v2r1  
**Estado:** final, diciembre de 2021; PDF oficial de 310 páginas inspeccionado por secciones.

Pasajes consultados:
- Abstract, autoridad y aplicabilidad (PDF pp. i–ii).
- §2.1, marco de ingeniería de resiliencia: goals, objectives, techniques, implementation approaches y design principles (PDF pp. 8–12).
- §2.1.1 y Table 2: cuatro objetivos de alto nivel anticipate, withstand, recover y adapt (página impresa 9).
- §3.1: selección y priorización de técnicas conducidas por objetivos de misión y prioridades de stakeholders.
- Appendix D: relaciones entre constructos, técnicas, enfoques y ejemplos, con inspección selectiva de tablas y técnicas.
- Appendix G: relación con tecnologías operacionales, inspección selectiva.

Aplicaciones:
1. Resiliencia no es un sinónimo de uptime, redundancia ni backup; se refiere a sostener funciones de misión ante adversidad y recuperar/adaptar capacidades.
2. Los cuatro goals son categorías de alto nivel; el análisis de ingeniería debe partir de objetivos específicos, contexto, misión y requisitos medibles.
3. Las técnicas y controles son medios, no objetivos. No deben elegirse por moda ni copiarse sin tailoring.
4. El análisis debe considerar amenazas adversariales y no adversariales, fallos y condiciones adversas.
5. Recuperar un proceso no prueba recuperar un estado confiable; el criterio de aceptación debe incorporar identidad, integridad, configuración, claves, dependencias y función.

**Control de versión:** SP 800-160 Vol. 2 de 2019 está retirado y sustituido en su totalidad por Rev. 1 desde 2021-12-09. No citar el PDF de 2019 como referencia vigente. La publicación final correcta es Vol. 2 Rev. 1.

## 3. NISTIR 8062 — An Introduction to Privacy Engineering and Risk Management in Federal Systems

**Fuente primaria:** https://doi.org/10.6028/NIST.IR.8062  
**Estado:** final, enero de 2017; PDF oficial de 49 páginas inspeccionado en abstract, Executive Summary, §2.1, §3.1, §3.2 y pasajes seleccionados de sus objetivos y modelo de riesgo.

Pasajes consultados:
- Executive Summary: relación y distinción entre seguridad de la información y privacidad; riesgos para individuos que exceden el acceso no autorizado a PII.
- §2.1: la protección contra acceso no autorizado es una parte de seguridad y privacidad, pero no cubre todos los problemas de privacidad.
- §3.1.1: predictability, manageability y disassociability.
- §3.2: el modelo de riesgo de privacidad se organiza alrededor de acciones de datos problemáticas y sus efectos sobre individuos, no solo alrededor de amenazas de intrusión.
- §3.2.2: las acciones de datos incluyen recolección, retención, logging, análisis, generación, transformación, combinación, divulgación, transferencia y disposición; el contexto determina cuándo pueden ser problemáticas.

Aplicaciones:
1. Cifrado y autorización son controles importantes, pero no demuestran por sí solos que la finalidad, cantidad, retención, inferencia o divulgación de datos sea apropiada.
2. El modelo de privacidad debe identificar operación de datos, población, contexto, expectativa y posible daño a individuos.
3. Los logs de operadores, telemetría y patrones de presencia deben evaluarse como acciones de datos, no como subproducto inocuo de observabilidad.
4. No trasladar automáticamente este informe federal estadounidense a obligaciones legales colombianas; su valor aquí es técnico-conceptual.

## 4. Contraste de los tres modelos

| Pregunta | SP 800-160 Vol. 1 Rev. 1 | SP 800-160 Vol. 2 Rev. 1 | NISTIR 8062 |
|---|---|---|---|
| Objeto principal | Ingeniería de sistemas seguros y confianza | Resiliencia cibernética de misión/sistema | Ingeniería y riesgo de privacidad |
| Unidad de razonamiento | Sistema, elementos, composición y ciclo de vida | Misión, sistema, adversidad y objetivos | Acciones de datos, personas y contexto |
| Evidencia | Claims, argumentos, análisis, pruebas e inspección | Objetivos, técnicas, requisitos y evidencia adaptada | Identificación de acciones problemáticas, likelihood/impact contextual |
| Error que evita | Inferir confianza del componente aislado o de checklist | Confundir resiliencia con control puntual o disponibilidad | Reducir privacidad a confidencialidad |
| Límite | No sustituye norma sectorial ni aceptación de riesgo | Requiere tailoring a misión y entorno | Marco conceptual federal, no norma legal colombiana |

No son marcos intercambiables ni tres checklists que se suman. Se complementan: ingeniería de seguridad proporciona estructura de sistema y assurance; resiliencia orienta continuidad/adaptación de misión ante adversidad; privacidad analiza impactos de acciones de datos sobre individuos.

## 5. Correcciones conceptuales exigidas en FND-01.01

- Sustituir cualquier afirmación de que una arquitectura redundante “garantiza” disponibilidad por una afirmación condicionada a topología, independencia, fallos comunes, cobertura y criterios de misión.
- No usar MTBF/MTTR como sustitutos de un modelo de disponibilidad del servicio sin hipótesis explícitas.
- No usar disponibilidad como proxy de confiabilidad, safety o seguridad.
- No usar confidencialidad como proxy de privacidad.
- No usar NIST CSF, SP 800-53 o NIST Privacy Framework como certificación de eficacia.
- No llamar “seguro” a un sistema por ausencia de incidentes observados.
- No equiparar resiliencia a RTO/RPO o backups; son medidas/elementos parciales.
- No tratar una evaluación en frío autogenerada como validación independiente.

## 6. Brechas que permanecen abiertas

1. Lectura lineal integral de las tres publicaciones y revisión crítica de referencias seleccionadas: pendiente. Esta inspección no permite marcar `full_text_reviewed`.
2. Bibliografía primaria adicional de confiabilidad, análisis de causa común, safety de sistemas y seguridad de sistemas ciberfísicos: pendiente.
3. Selección de normas sectoriales: no se puede determinar sin fijar industria, función, jurisdicción y alcance. Para safety funcional pueden ser pertinentes IEC 61508 y normas derivadas/sectoriales; su edición, alcance y requisitos deben verificarse con acceso autorizado y especialista.
4. Aplicabilidad colombiana: el mapeo existente es condicional y no sustituye revisión jurídica ni identificación del sector.
5. Revisión disciplinar independiente y administración del instrumento V2: pendiente.

**Conclusión de auditoría:** la base conceptual está mejor sustentada y se han reducido ambigüedades de alcance, pero las NC de lectura integral, normas sectoriales/legales y revisión independiente no pueden declararse cerradas con esta inspección dirigida. T0/O0 permanece hasta evaluación y revisión válidas.
