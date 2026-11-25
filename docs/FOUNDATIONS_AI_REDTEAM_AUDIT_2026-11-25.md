# Auditoría de profundidad y evidencia — Foundations + AI Red Team

Fecha: 2026-11-25
Base examinada: PR #21 (e7e0f4c108eb7ac4fb86f3dacd8c28055291597f) y PR #22 (f7ed69ea625142a679956767f7af9d91cb5b2348).
Rama de remediación: codex/foundations-ai-redteam-audit-remediation-2026-11-25.
Estado: auditoría parcial reproducible; no aceptación experta ni validación operativa.

## 1. Dictamen

Foundations y AI Red Team tienen una estructura curricular y contenido técnico sustancialmente mejor que los borradores iniciales. Aún no alcanzan nivel experto verificable.

- Foundations: el mapa V2 delimita 102 subtemas. El documento de ingeniería del riesgo cubre FND-04.01–FND-04.12 con modelos de escenario, métodos cuantitativos/ordinales, incertidumbre, assurance, tratamiento y preguntas. LAB-FND-14A comprueba aritmética de EAL con valores sintéticos; no estima riesgo de una organización.
- AI Red Team: el dossier teórico desarrolla siete temas en doce capas y el catálogo define nueve casos. El harness determinista ejecuta controles de referencia en memoria. El adaptador ejecuta cuatro probes sobre la salida de un modelo, sin RAG, herramientas ni agente integrado.
- Evidencia: los registros consultados distinguen páginas/fichas de lectura integral. No hay claims aprobados ni revisión independiente acreditada en la línea base revisada. Ningún PASS sintético cambia T/O.

## 2. Hallazgos técnicos de PR #22

### ART-04 — autenticidad del origen insuficiente en la versión auditada

Severidad: alta para el objetivo de assurance del caso.
La versión anterior aceptaba un documento por hash esperado y un identificador textual de firmante incluido en una allowlist. Ese identificador no probaba posesión de una clave ni ligaba criptográficamente al supuesto firmante con el contenido.

Remediación en esta rama: ART-04 calcula y verifica HMAC-SHA256 con una clave sintética asociada al identificador de origen; incluye casos de contenido alterado, origen desconocido y firma falsificada. La guía declara que HMAC no es firma digital asimétrica ni PKI.

Pendiente: integración con un esquema real de firma/provenance, gestión y rotación de claves, revocación, protección del almacén de claves y verificación de cadena de build.

### Probes de canary — cobertura limitada de codificaciones

Severidad: alta para interpretar resultados de extracción.
El detector previo buscaba el canary literal o una versión con separadores eliminados. Podía omitir divulgaciones en codificaciones sencillas.

Remediación en esta rama: detector finito para literal, separadores, reverso, ROT13, Base64, hexadecimal y URL encoding; pruebas unitarias de cada variante y de respuesta negativa.

Pendiente: no detecta todas las transformaciones posibles, cifrado, paráfrasis semántica, esteganografía ni toda divulgación parcial. Un PASS no prueba ausencia de fuga.

### ART-01…ART-09 — harness de controles, no evaluación end-to-end

Severidad: bloqueador de promoción operativa, no defecto del propósito declarado.
Los controles son funciones Python y fixtures en memoria. ART-03 no se conecta a un almacén multi-tenant real; ART-05 no invoca un broker productivo; ART-08 usa contadores deterministas; ART-09 usa un dataset mínimo sintético. ART-01/02 prueban decisiones de autorización de referencia, no el comportamiento de un agente real.

Acción requerida: conservar el nombre y la salida como harness sintético; crear adaptadores de integración aislados para retrieval, broker, memoria, caché, identidad y loop del agente. Medir efectos observables, denominadores y telemetría independiente. No traducir sus nueve PASS a “nueve ataques bloqueados en CYBER_AI”.

### ART-09 — integridad del benchmark incompleta

El fixture detecta intersección de IDs entre train/holdout y texto exactamente duplicado, pero el dataset contiene dos ejemplos por partición. No evalúa near-duplicates, contaminación por plantillas, duplicados dentro de cada partición, procedencia ni validez estadística.

Acción requerida: dataset versionado con IDs únicos, deduplicación normalizada y semántica, splits por origen/grupo, ground truth revisado, clases representativas, manifiesto/hash, licencia y revisión de contaminación.

## 3. Foundations — límites del contenido y del laboratorio

Fortalezas observadas:
- Distingue amenaza, evento, vulnerabilidad, exposición, consecuencia, control y riesgo residual.
- Advierte que matrices ordinales no son probabilidades cardinales y que CVSS no equivale a riesgo empresarial.
- Incluye escenarios falsables, incertidumbre aleatoria/epistémica/de modelo/medición/juicio, dependencias, assurance y autoridad de aceptación.
- LAB-FND-14A declara supuestos sintéticos y reproduce EAL basal/residual, pérdida evitada, coste y sensibilidad.

Brechas:
- La sensibilidad actual cambia frecuencia y pérdida por factores proporcionales prefijados; no es distribución probabilística, Monte Carlo ni análisis de dependencia.
- No existen datos empíricos para frecuencia, severidad, eficacia de controles ni coste.
- No modela pérdidas de cola, correlación, eventos extremos, cambios de régimen, intervalos de confianza ni incertidumbre de parámetros.
- El código de laboratorio comprueba la aritmética de un caso; no prueba el proceso de evaluación de riesgos de un sistema real.
- El documento registra fuentes candidatas, pero no afirma lectura integral ni claims trazados a localizadores.

Acción requerida: añadir ejercicios con datos públicos versionados y licencia comprobada, rangos y distribuciones justificadas, análisis de sensibilidad multidimensional, dependencias, pruebas de calibración y revisión por especialistas de riesgo.

## 4. Cobertura curricular y estado de aceptación

| Dimensión | Estado observado | Consecuencia |
|---|---|---|
| Foundations | Mapa de 102 subtemas; documentos profundos parciales | No afirmar cierre del currículo |
| AI Red Team | 7 temas base, dossier de 12 capas, 9 protocolos | No afirmar cobertura de todo el ciclo de vida del agente |
| Labs Foundations | runner EAL sintético reproducible | No valida datos ni eficacia de controles |
| Labs AI Red Team | 9 controles sintéticos y 4 probes de salida de modelo | No valida RAG, broker, memoria ni agente real |
| Claims respaldados | 0 en la línea base revisada | No hay afirmaciones aceptadas por evidencia |
| Lectura integral de fuentes | 0 registrada en la línea base revisada | referencias no equivalen a respaldo |
| Revisión independiente | no iniciada en la línea base revisada | sin aceptación experta |
| Madurez | T0/O0 en los registros previos | mantener sin promoción |

## 5. Criterios obligatorios para cerrar Foundations

Cada uno de los 102 subtemas debe tener, como mínimo:

1. Definiciones precisas, límites y conceptos que suelen confundirse.
2. Fundamento formal/matemático cuando aplique, con supuestos y derivación.
3. Arquitectura, mecanismos, protocolos y modos de fallo con versiones.
4. Estándares primarios mapeados a requisitos concretos y localizadores.
5. Ejemplos de diseño, configuración o análisis con decisiones justificadas.
6. Contraejemplos, trade-offs, fallos, incertidumbre y límites.
7. Laboratorio reproducible con baseline, ataque/fallo, detección, mitigación y retest.
8. Preguntas en frío con rúbrica y respuestas razonadas reservadas al evaluador.
9. Fuentes leídas integralmente o secciones justificadas, licencia y procedencia.
10. Revisión independiente, desacuerdos resueltos y evidencia de aceptación.

Las doce capas y las capacidades deben evaluarse una por una. El texto o un test de estructura no puede marcar una celda como aprobada.

## 6. Criterios obligatorios para cerrar AI Red Team

La cobertura debe incluir modelo, aplicación, RAG, ingestión, chunking/embeddings, vector store, memoria corta/larga, herramientas, broker, IAM, delegación, agentes multi-etapa, multimodalidad, supply chain, evaluación, observabilidad, respuesta, limpieza y retest.

Por caso se exige arquitectura/versión y alcance autorizado; precondiciones, actor, capacidad y activo; baseline benigno y control negativo; acción/efecto observable, no solo respuesta textual; ground truth, denominador, repeticiones y criterio de inconcluso; logs saneados, hashes y telemetría de cada frontera; mitigación y retest con misma configuración; falsos positivos, utilidad, latencia, coste y límites de generalización; revisión independiente.

## 7. Secuencia de trabajo

1. Ejecutar pruebas de regresión y CI en el HEAD de esta rama.
2. Ejecutar probes contra el modelo local elegido y registrar salida completa saneada; un FAIL se conserva como hallazgo, no se oculta.
3. Integrar el harness con componentes reales en sandbox aislado, comenzando por RAG/tenant y broker de herramientas.
4. Completar Foundations granularmente, sin saltar subtemas.
5. Completar AI Red Team con cobertura end-to-end y revisión independiente.
6. Repetir el método para las otras 46 especialidades.
7. Solo después realizar pruebas calientes del sistema completo y decidir promoción.

## 8. No conformidades abiertas

- NC-FND-01: falta evidencia empírica para calibrar estimaciones de riesgo.
- NC-FND-02: falta tratamiento cuantitativo de dependencia, colas e incertidumbre de parámetros.
- NC-FND-03: falta cierre y evaluación granular de los 102 subtemas.
- NC-ART-01: falta integración con retrieval y aislamiento multi-tenant reales.
- NC-ART-02: falta broker real con autorización, idempotencia, audit trail y rollback.
- NC-ART-03: falta evaluación de memoria, persistencia, multimodalidad y loops multi-turn.
- NC-ART-04: el detector de canary es finito y no cubre transformaciones arbitrarias.
- NC-ART-05: el benchmark sintético no demuestra validez estadística ni ausencia de contaminación.
- NC-EVID-01: claims respaldados y revisión independiente siguen pendientes.
- NC-EVID-02: la lectura integral, licencias y vigencia de fuentes debe completarse por claim y subtema.

Decisión: PR #21 y PR #22 pueden seguir como entregas de desarrollo, pero la biblioteca de Foundations y AI Red Team no está aprobada como experta ni operativamente validada.


## 9. Remediación ART-09 posterior a esta auditoría — 2026-11-25

En una rama posterior se amplió el fixture de ART-09 para comprobar esquema, unicidad global de IDs, separación train/holdout, duplicados tras normalización Unicode, candidatos a near-duplicate por similitud de secuencia, separación de grupos de origen y denominadores por clase. Se añade manifiesto versionado con SHA-256 sobre JSON canónico. La licencia queda pendiente de revisión explícita.

Esta mejora reduce omisiones estructurales del fixture anterior, pero no cierra NC-ART-05: el dataset sigue siendo pequeño y sintético; no se ha demostrado tamaño estadístico adecuado, ground truth independiente, representatividad, potencia, validez externa ni ausencia de contaminación semántica. La similitud de secuencia es una heurística finita, no un detector semántico. El resultado ART-09 debe seguir interpretándose como control estructural, nunca como benchmark científicamente validado.
