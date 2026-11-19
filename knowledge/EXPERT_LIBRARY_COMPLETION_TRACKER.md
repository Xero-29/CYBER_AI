> **Actualización normativa 2026-11-19:** se incorpora `knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md`. Desde este corte, las 48 especialidades se evalúan explícitamente por enseñanza, explicación, análisis y diseño, además de las doce capas. El orden obligatorio es Foundations → AI Red Team → las otras 46. No se promueve ninguna celda por volumen, encabezados o presencia de archivos. La madurez T/O permanece separada. Este protocolo no cambia retroactivamente estados a `passed`.

# Seguimiento de aplicación del estándar experto — Biblioteca CYBER_AI

**Corte editorial:** 2026-11-19  
**Áreas:** 48/48 inspeccionadas; 336 unidades temáticas iniciales y 4.032 comprobaciones tema×capa registradas en la auditoría granular. Seis módulos P0 recibieron reescritura disciplinar específica; Foundations recibió además un desarrollo general ampliado. Los otros 41 conservan desarrollo inicial y requieren ampliación profunda.  
**Estado global:** M2 editorial; auditoría estructural aplicada, pero cobertura por capa todavía no demostrada. Investigación documental, experimentación y validación independiente pendientes.

## Alcance aplicado
Los seis módulos P0 (identity, malware, forensics, incident_response, threat_intel y reverse) fueron reescritos para sustituir bloques genéricos por mecanismos, casos límite, pruebas negativas, métricas y laboratorios específicos. Cada uno dispone ahora de agenda experimental y revisión exploratoria de literatura. Esto es avance editorial M2, no validación disciplinar. Las otras 41 áreas, aparte de Foundations, conservan el estado editorial previo y requieren ampliación disciplinar tema por tema. Foundations ya recibió auditoría documental individual de sus siete temas contra doce capas por tema (84/84 en progreso, ninguna aprobada). La corrección se registra en `knowledge/deep_modules/foundations/FOUNDATIONS_DEEP_DEVELOPMENT_V1.md`, la agenda se alinea a esos siete IDs y las matrices Markdown/JSON registran los estados. Falta ampliar lectura integral de fuentes, ejecutar laboratorios con implementaciones reales aisladas, réplica independiente y revisión externa.

## Matriz de áreas
| ID | Área | Compendio | Agenda específica | Fuentes integrales | Laboratorio ejecutado | Revisión independiente |
|---|---|---|---|---|---|---|
| `foundations` | Fundamentos | Siete temas auditados documentalmente contra 12 capas; 84/84 en progreso; M2 | Agenda alineada a los siete temas; siete protocolos específicos | Secciones primarias pertinentes revisadas y trazadas; lectura lineal completa pendiente | 7 labs sintéticos ejecutados localmente; 8 tests pasan; réplica y revisión independiente pendientes | Pendiente |
| `appsec` | Seguridad de aplicaciones | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `api` | Seguridad de API | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `network` | Seguridad de redes | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `linux` | Linux y Unix | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `windows_ad` | Windows y Active Directory | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `cloud` | Seguridad cloud | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `containers` | Contenedores y Kubernetes | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `mobile` | Seguridad móvil | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `crypto` | Criptografía | Ampliado con siete capítulos técnicos específicos, agenda experimental y mapa de fuentes; borrador M2 | Protocolo por subtema definido; ejecución pendiente | Metadatos de 15 fuentes primarias/RFC registradas; lectura integral pendiente | 7 protocolos de laboratorio diseñados; no ejecutados | Revisión independiente pendiente |
| `identity` | Identidad y acceso | Reescrito por 7 temas; borrador M2 | 6 protocolos específicos | Fuentes registradas; lectura integral pendiente | 6 labs diseñados, no ejecutados | Pendiente |
| `malware` | Análisis de malware | Reescrito por 7 temas; borrador M2 | 6 protocolos específicos | Fuentes registradas; lectura integral pendiente | 7 labs fríos diseñados, no ejecutados | Pendiente |
| `forensics` | Informática forense | Reescrito por 7 temas; borrador M2 | 6 protocolos específicos | Fuentes registradas; lectura integral pendiente | 7 labs fríos diseñados, no ejecutados | Pendiente |
| `incident_response` | Respuesta a incidentes | Reescrito por 7 temas; borrador M2 | 6 protocolos específicos | Fuentes registradas; lectura integral pendiente | 7 labs fríos diseñados, no ejecutados | Pendiente |
| `threat_intel` | Inteligencia de amenazas | Reescrito por 7 temas; borrador M2 | 6 protocolos específicos | Fuentes registradas; lectura integral pendiente | 7 labs fríos diseñados, no ejecutados | Pendiente |
| `reverse` | Ingeniería inversa | Reescrito por 7 temas; borrador M2 | 7 protocolos específicos | Fuentes registradas; lectura integral pendiente | 7 labs fríos diseñados, no ejecutados | Pendiente |
| `iot_hardware` | IoT y hardware | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `devsecops` | DevSecOps | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `ai_security` | Seguridad de IA | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `governance` | Gobierno y riesgo | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `vuln_management` | Gestión de vulnerabilidades | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `bug_bounty` | Bug bounty | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `secure_arch` | Arquitectura segura | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `data_security` | Seguridad de datos | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `software_engineering` | Ingeniería de software | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `machine_learning` | Seguridad de ML | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `hardware_security` | Seguridad de hardware | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `mathematics` | Matemáticas para ciberseguridad | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `soc_siem` | SOC y SIEM | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `edr_xdr` | EDR/XDR | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `red_team` | Red Team | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `wireless_security` | Seguridad inalámbrica | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `ot_ics` | Seguridad OT/ICS | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `telecom_5g` | Telecomunicaciones 5G | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `automotive_security` | Seguridad automotriz | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `satellite_security` | Seguridad satelital | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `physical_security` | Seguridad física | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `email_dns_security` | Correo y DNS | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `fraud_abuse` | Fraude y abuso | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `privacy_engineering` | Ingeniería de privacidad | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `cloud_forensics` | Forense cloud | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `ai_red_team` | Red Team de IA | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `pki_hsm` | PKI y HSM | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `post_quantum_crypto` | Criptografía poscuántica | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `business_continuity` | Continuidad de negocio | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `database_security` | Seguridad de bases de datos | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |
| `vulnerability_research` | Investigación de vulnerabilidades | Ampliado, borrador | Definida en matriz común | Pendiente | Pendiente | Pendiente |

## Lo que NO significa este avance
- No significa que cada tema haya alcanzado profundidad K4/K5.
- No significa que todas las fuentes registradas hayan sido descargadas y leídas íntegramente.
- No significa que los laboratorios estén ejecutados.
- No significa que las herramientas o recomendaciones hayan sido probadas en entornos reales.
- No significa que se haya obtenido validación científica, certificación ni revisión externa.

## Evidencia pendiente por área
1. Mapa de cobertura de subtemas contra el perfil experto y el currículo.
2. Registro de fuentes primarias/secundarias con edición, fecha, licencia, páginas leídas y hash.
3. Síntesis crítica por fuente, método, población, resultados, sesgos y contradicciones.
4. Matriz amenaza→control→prueba→resultado→riesgo residual.
5. Laboratorios versionados, reproducibles, con ground truth y controles negativos.
6. Evaluación cuantitativa con denominadores, intervalos y análisis de falsos positivos/negativos.
7. Revisión disciplinar independiente y corrección de hallazgos.
8. Reproducción externa para M5.

## Regla de aceptación
Ningún área se declara completa hasta satisfacer las ocho puertas G1–G8 con evidencia trazable. La presencia de un compendio o una agenda no equivale a aprobación.

## Remediación P0 — corte 2026-11-19

| Módulo | Compendio específico | Agenda | Revisión de literatura | Laboratorios |
|---|---|---|---|---|
| identity | 7 temas reescritos | 6 protocolos | Mapa de fuentes; lectura integral pendiente | 6 diseñados, no ejecutados |
| malware | 7 temas reescritos | 6 protocolos | Mapa de fuentes; lectura integral pendiente | 7 diseñados, no ejecutados |
| forensics | 7 temas reescritos | 6 protocolos | Mapa de fuentes; lectura integral pendiente | 7 diseñados, no ejecutados |
| incident_response | 7 temas reescritos | 6 protocolos | Mapa de fuentes; lectura integral pendiente | 7 diseñados, no ejecutados |
| threat_intel | 7 temas reescritos | 6 protocolos | Mapa de fuentes; lectura integral pendiente | 7 diseñados, no ejecutados |
| reverse | 7 temas reescritos | 7 protocolos | Mapa de fuentes; lectura integral pendiente | 7 diseñados, no ejecutados |

**Límite:** el número de temas/protocolos/laboratorios describe artefactos de diseño, no pruebas completadas. No asignar M3/M4/M5 ni declarar biblioteca completa.


## Auditoría granular del estándar — corte 2026-11-19

Se inspeccionaron los 48 compendios técnicos y se creó una línea base legible por humanos y máquinas:
- `knowledge/research/DOMAIN_LAYER_AUDIT_48.md`
- `knowledge/research/DOMAIN_LAYER_AUDIT_48.json`

La matriz contiene 48 especialidades, 7 unidades temáticas iniciales por especialidad, 12 capas por tema (4.032 estados) y ocho puertas G1–G8 por especialidad. Los estados restantes se mantienen `not_assessed` cuando no hay comprobación trazable; Foundations es la excepción actual, con sus 84 celdas `in_progress` por desarrollo documental mapeado, sin aprobación.

### Hallazgo de la inspección
- Seis módulos (identity, malware, forensics, incident_response, threat_intel y reverse) tienen reescritura disciplinar inicial. Foundations tiene siete dossiers tema×capa documentados; los seis módulos P0 y Foundations aún requieren evidencia de lectura, experimentación y revisión independiente.
- Los otros 42 compendios contienen rutas temáticas iniciales, pero presentan bloques metodológicos repetidos y profundidad insuficiente para afirmar aplicación exhaustiva del estándar.
- Los 48 módulos permanecen en M2 editorial. No se elevan niveles K ni puertas G por presencia de documentos, títulos o palabras clave.

### Siguiente ejecución
1. Desarrollar en profundidad los 42 módulos restantes, tema por tema y con perfil disciplinar propio.
2. Auditar también los seis módulos ya reescritos contra las 12 capas.
3. Vincular cada afirmación relevante a fuentes realmente consultadas.
4. Ejecutar laboratorios y evaluaciones; conservar evidencia y resultados negativos.
5. Solicitar revisión independiente y reproducción externa antes de declarar K4/K5.


## Ejecución secuencial del estándar — Foundations (2026-11-19)

**Cambio documental:** commit `3588344959da3cd50d923670d4f81d5de821e7a6` añadió `knowledge/deep_modules/foundations/FOUNDATIONS_DEEP_DEVELOPMENT_V1.md`. Commit `8c7ac8df9bbe2fe7ee079b49a9a633b057c65196` actualizó el índice README del módulo.

**Contenido añadido:** ontología de seguridad; modelos de grafos y estados; probabilidad condicionada e incertidumbre; ingeniería de sistemas seguros; pérdidas y consecuencias; análisis de amenazas y fallos; assurance; gobierno y supply chain; privacidad, safety y resiliencia; alcance de marcos; métricas; cuatro casos integradores; cinco protocolos de laboratorio; evaluación y Skills candidatas.

**Verificación documental posterior:** el nuevo desarrollo contiene una matriz explícita FND-01 a FND-15 y una evaluación de L1–L12. Las brechas tienen tratamiento documental, pero varias permanecen abiertas por necesitar evidencia no generable mediante redacción: lectura integral de fuentes, ejecución experimental, benchmark, revisión independiente y reproducción externa.

**Resultado de la puerta de salida:** Foundations NO se declara cerrado bajo el estándar completo. Madurez conservadora M2 editorial ampliado. K4/K5, M4/M5 y G1–G8 aprobadas no reclamadas. No avanzar al módulo 2 hasta cerrar las evidencias bloqueantes según el criterio del estándar.


## Cierre de auditoría documental de Foundations — 2026-11-19

- Siete temas identificados por sus IDs `foundations-01` a `foundations-07`.
- Doce capas desarrolladas explícitamente por tema en `FOUNDATIONS_DEEP_DEVELOPMENT_V1.md`.
- Agenda de investigación alineada uno a uno con los siete temas.
- Matriz JSON: 84/84 celdas `in_progress`; ninguna `passed`.
- G1–G7 `in_progress`; G8 `blocked` por revisión independiente pendiente.
- Se registraron y revisaron por secciones NIST SP 800-160 Vol. 1 Rev. 1, SP 800-30 Rev. 1, SP 800-37 Rev. 2, SP 800-61 Rev. 3, SP 800-88 Rev. 2, CSF 2.0, RFC 9700, FIPS 204/205, ATT&CK v20.1 y OWASP ASVS 5.0.0. Lectura integral de algunas fuentes y revisión de FIPS 203/SP 800-57/800-53 5.2.0 siguen pendientes.
- Siete laboratorios sintéticos ejecutados localmente; 8 pruebas unitarias pasan. Réplica independiente y pruebas de implementación real pendientes. Las siete Skills siguen candidatas, no validadas.
- Madurez se mantiene M2. No declarar K3/K4/K5 ni validación científica.


### Evidencia experimental local de Foundations — 2026-11-19

- Runner: `knowledge/deep_modules/foundations/labs/runner.py`.
- Pruebas: `tests/test_foundations_labs.py` (8/8 pasan en ejecución local).
- Resultados: `knowledge/deep_modules/foundations/labs/results.json`.
- Semilla: `20261119`; solo datos sintéticos.
- G5–G7: `in_progress`, no `passed`; G8: `blocked`.
- Límite: los resultados no prueban eficacia real, interoperabilidad, seguridad de implementaciones criptográficas, validez externa ni revisión experta. Requiere CI del HEAD, réplica en segundo entorno y revisión independiente.
- Revisión de fuentes: `knowledge/deep_modules/foundations/SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md`.


## Programa de completitud teórica para las 48 especialidades — 2026-11-19

Se establece una primera etapa obligatoria de capacidades en frío para las 48 especialidades. La matriz de 48 áreas × 7 temas iniciales × 12 capas (4.032 comprobaciones) es línea base, no techo curricular: G1 debe descubrir subtemas, dependencias y especializaciones ausentes.

La madurez se reportará en dos ejes separados: teórico T0–T5 y operativo O0–O5. El objetivo de esta etapa es completar el conocimiento teórico, no afirmar que herramientas o laboratorios ya fueron ejecutados. Las capas de implementación, laboratorio, evaluación y Skills se documentan con código revisable, protocolos, datasets diseñados, métricas y especificaciones; la ejecución queda pendiente y explícita.

**Secuencia:** módulo por módulo; no avanzar hasta cerrar la auditoría documental adversarial del módulo actual. El primer módulo activo es `ai_red_team`, con investigación de brechas inicial ya registrada en `knowledge/research/domain_investigations/AI_RED_TEAM_GAP_RESEARCH_2026-11-19.md`. Esa investigación no cierra el módulo: hay que profundizar sus siete temas, corregir contenido genérico y completar las doce capas con fuentes, explicaciones, casos resueltos y evaluación en frío.

**Regla de estado:** no asignar T4 sin revisión independiente; no asignar O2–O5 sin evidencia de ejecución. Un módulo puede quedar T3/O0 o T4/O0, sin confundir profundidad teórica con capacidad operativa.

Norma y secuencia completas: [THEORETICAL_LIBRARY_COMPLETION_PROGRAM_48.md](THEORETICAL_LIBRARY_COMPLETION_PROGRAM_48.md).


### Primer módulo bajo el programa teórico — AI Red Team (2026-11-19)

- Se creó `knowledge/deep_modules/ai_red_team/AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md`, con desarrollo diferenciado de doce capas para los siete temas de línea base.
- Se identificaron límites de confianza, modelos de amenaza, arquitectura, controles, trade-offs, preguntas de investigación, diseño de laboratorios/datasets, métricas, especificaciones de Skills y evaluación en frío.
- Se enlazó el dossier desde el README y el compendio técnico previo.
- **Estado:** avance documental sustancial, todavía incompleto. El inventario de siete temas debe ampliarse, la lectura integral de fuentes sigue pendiente, no se ha completado la auditoría adversarial de las 84 celdas y no hay revisión independiente ni laboratorios nuevos ejecutados.
- **Madurez:** M2 editorial; no declarar T4, G1–G8 aprobadas ni madurez operativa. La salida del módulo permanece bloqueada hasta cerrar su completitud teórica.
