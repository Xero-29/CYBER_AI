# Investigación independiente y análisis de brechas — Foundations

Fecha de corte: 2026-11-19  
Especialidad: foundations — Fundamentos de ciberseguridad  
Rama: knowledge/develop-foundations  
Estado: investigación documental exploratoria contrastada. No es validación experta.

## 1. Método y límites

La investigación se inició desde la disciplina, sin tomar el compendio existente como mapa exhaustivo. Después se contrastó con README.md, TECHNICAL_COMPENDIUM.md, LITERATURE_REVIEW.md y RESEARCH_AGENDA.md de esta rama.

Fuentes primarias consultadas:
- NIST CSWP 29, Cybersecurity Framework 2.0: texto PDF consultado e inspeccionado.
- NIST SP 800-30 Rev. 1: PDF completo accesible; secciones sobre modelo de riesgo, eventos, vulnerabilidades, probabilidad e impacto inspeccionadas. No se declara lectura lineal de las 95 páginas.
- NIST SP 800-160 Vol. 1 Rev. 1: PDF completo accesible; fundamentos de sistemas, activos, pérdidas, assurance, principios de diseño y ciclo de vida inspeccionados. No se declara lectura lineal de las 195 páginas.
- NIST SP 800-61 Rev. 3: PDF completo accesible; resumen ejecutivo y modelo de ciclo de vida basado en CSF 2.0 inspeccionados. No se declara lectura lineal de las 48 páginas.
- MITRE ATT&CK: introducción oficial y taxonomía de tácticas consultadas.

Esto es una revisión técnica exploratoria, no una revisión sistemática ni lectura integral de todas las obras. No se atribuyen resultados experimentales a las fuentes.

## 2. Mapa disciplinar independiente

Foundations debe enseñar modelos transversales para razonar sobre cualquier sistema, sin sustituir los módulos especializados. El mapa de referencia debe incluir:

1. Naturaleza de la seguridad: propiedades, objetivos, seguridad como propiedad emergente, límites de protección y diferencias entre security, safety, reliability, privacy y resilience.
2. Sistemas, activos y misión: sistema de interés, contexto, stakeholders, activos tangibles/intangibles, dependencias, pérdidas, consecuencias y protección proporcional.
3. Confianza y control: sujetos, objetos, políticas, mecanismos, dominios de confianza, separación, aislamiento y composición.
4. Arquitectura y ciclo de vida: requisitos, arquitectura, diseño, implementación, integración, verificación, validación, operación, mantenimiento, adquisición y retiro.
5. Amenazas y adversarios: fuentes adversariales y no adversariales, eventos, capacidades, intención, oportunidad, TTP, superficie, rutas, DFD, STRIDE y árboles de ataque.
6. Debilidades y exposición: vulnerabilidad, debilidad, condición predisponente, exposición, exploitabilidad, severidad, probabilidad, impacto y riesgo residual.
7. Riesgo y decisión: contexto, apetito/tolerancia, incertidumbre, modelos cualitativos/cuantitativos, supuestos, sensibilidad, coste-beneficio, tratamiento, aceptación y comunicación.
8. Controles y assurance: controles preventivos/detectivos/correctivos, diseño y operación, eficacia, evidencia, assurance case, verificación y validación.
9. Gobierno y organización: responsabilidades, políticas, roles, riesgo empresarial, terceros, cadena de suministro, cumplimiento, auditoría y cultura.
10. Datos, privacidad y resiliencia: clasificación, ciclo de vida, minimización, continuidad, recuperación, degradación segura e impacto en personas.
11. Observabilidad y respuesta: telemetría, registros, detección, respuesta, aprendizaje y recuperación, sin sustituir SOC/IR/forense.
12. Método profesional y científico: problemas, evidencia, causalidad, métricas, sesgos, incertidumbre, experimentos, reproducibilidad y comunicación.

## 3. Contraste con lo que existe

| Artefacto | Contenido encontrado | Evaluación |
|---|---|---|
| README.md | Siete temas, competencias, procedimiento, laboratorio y evaluación | La estructura existe, pero las instrucciones de trabajo se repiten casi idénticas en los siete temas; no desarrollan su materia específica. |
| TECHNICAL_COMPENDIUM.md | Modelos de seguridad/confianza, inventario, superficie de ataque, amenazas, identidad, redes/sistemas, vulnerabilidades y telemetría/respuesta | Contiene explicaciones útiles y distinciones correctas; cobertura desigual y no exhaustiva. |
| LITERATURE_REVIEW.md | Revisión exploratoria, hipótesis y límites | Reconoce correctamente que no es revisión sistemática y que las fuentes no están leídas integralmente. |
| RESEARCH_AGENDA.md | Siete líneas con preguntas, hipótesis y diseños | Punto de partida; mezcla cuestiones que pertenecen a Identity, Network, Vulnerability Management e Incident Response. |
| Currículo | Siete unidades iniciales | No representa el mapa disciplinar de doce bloques descrito arriba. |

### Conocimiento existente que se conserva

- CIA y propiedades complementarias: autenticidad, trazabilidad, privacidad y resiliencia.
- Diferencias entre activo, componente, dato, servicio y dependencia.
- Inventario, clasificación, criticidad, propietario, frescura y reconciliación.
- Límites de confianza y DAC, MAC, RBAC y ABAC.
- Superficie de ataque, escenarios, STRIDE y árboles de ataque.
- Distinción inicial entre CVSS, EPSS y riesgo contextual.
- Identidad, autenticación, autorización y privilegio mínimo.
- Controles preventivos, detectivos y correctivos, evidencia y riesgo residual.
- Necesidad de autorización, aislamiento y reversibilidad en laboratorios.

No se reescribirá lo correcto por el simple hecho de ampliar el módulo.

## 4. Brechas verificadas

| ID | Brecha | Acción requerida |
|---|---|---|
| FND-01 | README repite metodología genérica | Reescribir cada tema con contenido, objetivos, modelos, ejemplos, límites y pruebas propios. |
| FND-02 | Fundamentos formales insuficientes | Añadir modelos de confianza, estados, grafos, probabilidad e incertidumbre cuando sean pertinentes. |
| FND-03 | Security engineering y ciclo de vida poco desarrollados | Integrar requisitos, arquitectura, trade-offs, verificación, validación, operación y retiro. |
| FND-04 | Teoría de pérdidas y consecuencias incompleta | Desarrollar activos, pérdidas, consecuencias, stakeholders y protección proporcional. |
| FND-05 | Riesgo e incertidumbre insuficientes | Explicar iniciación/ocurrencia, probabilidad condicional, impacto, supuestos, sensibilidad y límites de cuantificación. |
| FND-06 | Assurance poco desarrollado | Incorporar claims, argumentos, evidencias, verificación, validación y assurance cases. |
| FND-07 | Amenazas no adversariales y fallos sistémicos insuficientes | Integrar error humano, fallos, dependencias, eventos ambientales y causa raíz. |
| FND-08 | Gobierno y riesgo de terceros poco integrados | Añadir responsabilidades, adquisición, supply chain y comunicación de riesgo. |
| FND-09 | Privacy, safety y resilience requieren tratamiento propio | Desarrollar impacto en personas, seguridad física, continuidad y recuperación. |
| FND-10 | Marcos normativos sin matriz de alcance/versiones | Comparar propósito, alcance, audiencia, entradas, salidas y límites; no asumir equivalencia. |
| FND-11 | Métricas sin suficiente fundamento estadístico | Añadir validez de constructo, sesgo de muestreo, precisión/recall, incertidumbre y sensibilidad. |
| FND-12 | Faltan casos integrales | Construir casos de empresa híbrida, SaaS, pequeña organización, OT simulado y proveedor externo. |
| FND-13 | Investigación sin revisión sistemática | Definir búsqueda reproducible, inclusión/exclusión, cribado, extracción y síntesis crítica. |
| FND-14 | Laboratorios no ejecutados | Crear datasets sintéticos con ground truth, controles negativos, scripts, resultados y repetición. |
| FND-15 | Evaluación práctica insuficiente | Crear pruebas de transferencia, diagnóstico, diseño, crítica y rúbricas con respuestas razonadas. |

## 5. Hallazgos de fuentes primarias

### CSF 2.0

NIST CSF 2.0 organiza resultados en funciones, categorías y subcategorías, y utiliza perfiles y tiers para describir postura y rigor de gestión. El documento aclara que describe resultados deseables, no prescribe cómo alcanzarlos. Foundations debe enseñarlo como taxonomía y lenguaje común, no como receta de controles ni certificación automática.  
Fuente: https://doi.org/10.6028/NIST.CSWP.29

### Evaluación de riesgo

NIST SP 800-30 Rev. 1 estructura la evaluación en preparación, conducción y mantenimiento. Distingue fuentes de amenaza, eventos, vulnerabilidades/condiciones predisponentes, probabilidad, impacto y riesgo. La combinación depende del modelo definido por la organización; supuestos e incertidumbre deben explicitarse.  
Fuente: https://doi.org/10.6028/NIST.SP.800-30r1

### Ingeniería de sistemas seguros

NIST SP 800-160 Vol. 1 Rev. 1 desarrolla ingeniería de sistemas seguros, activos, pérdidas, necesidades de protección, assurance, principios de diseño y procesos del ciclo de vida. Foundations debe explicar cómo las necesidades de protección se traducen en requisitos, arquitectura, diseño, implementación, integración, verificación, validación, operación y mantenimiento.  
Fuente: https://doi.org/10.6028/NIST.SP.800-160v1r1

### Respuesta como gestión continua

NIST SP 800-61 Rev. 3 integra respuesta a incidentes con CSF 2.0. Preparación y mejora no se reducen al momento del incidente. Foundations debe presentar el modelo transversal y derivar los procedimientos especializados al módulo Incident Response.  
Fuente: https://doi.org/10.6028/NIST.SP.800-61r3

### MITRE ATT&CK

ATT&CK es una base de conocimiento de tácticas y técnicas basada en observaciones del mundo real. Debe caracterizar comportamiento adversario; no es probabilidad de ocurrencia, catálogo exhaustivo ni prueba de que una técnica ocurrió.  
Fuente: https://attack.mitre.org/resources/enterprise-introduction/

## 6. Cambios que requiere Foundations

1. Ampliar el currículo de siete unidades genéricas a los doce bloques disciplinares, con subtemas y prerrequisitos.
2. Conservar el compendio actual y ampliarlo con ingeniería de sistemas seguros, razonamiento de pérdidas, assurance, incertidumbre, gobierno, privacidad, resiliencia y método científico.
3. Sustituir en README las instrucciones repetidas por contenido y entregables específicos.
4. Rehacer la revisión bibliográfica con estrategia de búsqueda, matriz de evidencia y lectura por secciones.
5. Separar preguntas de investigación de fundamentos didácticos y eliminar solapamientos con módulos especializados.
6. Crear trazabilidad afirmación → fuente/sección → evidencia → tema/capa → prueba → estado.
7. Crear casos integradores y evaluación de transferencia.
8. Ejecutar laboratorios solo después de fijar protocolo, ground truth, métricas, controles negativos y entorno.

## 7. Estado inicial de las doce capas

| Capa | Estado observado | Brecha principal |
|---|---|---|
| 1. Fundamentos teóricos | Parcial | Seguridad, safety, privacidad, resiliencia, definiciones y límites. |
| 2. Matemáticos/formales | Insuficiente | Modelos explícitos de riesgo, incertidumbre, grafos y estados. |
| 3. Arquitectura/internos | Parcial | Ingeniería de sistemas y ciclo de vida integral. |
| 4. Estándares/metodologías | Parcial | Comparación crítica y matriz de alcance/versiones. |
| 5. Implementación | Parcial | Ejemplos y procedimientos específicos por tema. |
| 6. Análisis avanzado | Insuficiente | Fallos sistémicos, causa raíz, trade-offs y límites. |
| 7. Seguridad | Parcial | Amenazas no adversariales, supply chain, safety y riesgo residual. |
| 8. Investigación científica | Insuficiente | Revisión reproducible y estado del arte. |
| 9. Laboratorios/datasets | Diseñado, no ejecutado | Dataset sintético con ground truth y protocolo completo. |
| 10. Evaluación/benchmarks | Insuficiente | Benchmarks, rúbricas, pruebas negativas e incertidumbre. |
| 11. Conocimiento operativo | Parcial | Skills con precondiciones, permisos, validaciones y rollback. |
| 12. Trazabilidad/mantenimiento | Parcial | Trazabilidad por afirmación, secciones leídas, versiones y obsolescencia. |

Ninguna capa queda aprobada en esta auditoría inicial. Parcial significa que existe contenido útil, no que se haya demostrado cobertura completa.

## 8. Criterio de cierre

Foundations solo se declara desarrollado cuando cada bloque y subtema tiene explicación específica; las fuentes relevantes tienen estado de lectura real por sección; las afirmaciones importantes son trazables; los modelos se explican con supuestos y límites; los casos integradores se resuelven con rúbrica; los laboratorios definidos se ejecutan y conservan resultados; existe revisión crítica y las puertas G1–G8 se actualizan con evidencia.

**Madurez conservadora:** M2 editorial, con investigación documental exploratoria en curso. No K4/K5 ni M3/M4/M5. No validación experta.

## 9. Fuentes primarias inspeccionadas

- NIST CSWP 29, The NIST Cybersecurity Framework (CSF) 2.0, 2024: https://doi.org/10.6028/NIST.CSWP.29
- NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments, 2012: https://doi.org/10.6028/NIST.SP.800-30r1
- NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems, 2022: https://doi.org/10.6028/NIST.SP.800-160v1r1
- NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management, 2025: https://doi.org/10.6028/NIST.SP.800-61r3
- MITRE ATT&CK Enterprise Introduction: https://attack.mitre.org/resources/enterprise-introduction/

## 10. Siguiente ejecución

La siguiente modificación será sobre Foundations: ampliar currículo y compendio para resolver FND-01 a FND-15, empezando por las brechas conceptuales y estructurales críticas. Después se contrastará el contenido modificado con esta investigación y se publicará la lista cerrada de existe/falta/evidencia. Solo entonces se pasa al módulo 2.
