# Línea base de cierre en frío — 2026-11-20

**Proyecto:** CYBER_AI  
**Repositorio:** https://github.com/Xero-29/CYBER_AI  
**Rama auditada:** `main`  
**HEAD auditado:** `387104756d0f8307c39a46a1ea2df07671bd81c9`  
**Rama de trabajo:** `codex/cold-phase-baseline-2026-11-20`  
**Tipo:** inspección documental y de metadatos GitHub; no es auditoría de penetración ni validación operacional.

## 1. Resultado ejecutivo

La línea base de `main` está identificada y los workflows Python y Docker Sandbox más recientes terminaron correctamente sobre el mismo HEAD. La biblioteca contiene estructura para 48 especialidades, pero el estado de `main` no permite afirmar que las 48 estén desarrolladas a nivel experto.

El trabajo de profundización y reconciliación más relevante sigue en PRs draft. Se conserva sin fusionar. Las evidencias consultadas muestran que Foundations y AI Red Team siguen sin superar las puertas de aceptación experta, y que los 192 desarrollos avanzados son borradores estructurados, no 192 investigaciones validadas.

**Decisión:** mantener `main` intacta, usar esta rama como registro de la línea base y reconciliar cada PR mediante comparación de archivos, revisión de seguridad y pruebas sobre el resultado integrado. No fusionar PRs por el hecho de ser mergeables.

## 2. Línea base verificable

| Elemento | Observación |
|---|---|
| Repositorio | Público, accesible; rama por defecto `main` |
| HEAD | `387104756d0f8307c39a46a1ea2df07671bd81c9` |
| Árbol versionado | 573 entradas; árbol recursivo no truncado |
| Python Tests | Éxito en run [44786328908](https://github.com/Xero-29/CYBER_AI/actions/runs/44786328908) |
| Docker Sandbox | Éxito en run [44786328754](https://github.com/Xero-29/CYBER_AI/actions/runs/44786328754) |
| Último commit | `feat: add metacognitive research loop` |
| Estado de los workflows | Evidencia de CI para ese SHA; no acredita calidad semántica ni seguridad operacional |

El commit actual de `main` incorpora `metacognition.py`, `researcher_agent.py` y pruebas asociadas. El investigador usa un backend intercambiable y declara sus informes como pendientes de verificación independiente. La presencia del código y el CI verde no demuestra todavía calidad de investigación con proveedores reales ni corrección semántica de las decisiones.

## 3. PRs pendientes de reconciliación

Todos los PRs siguientes estaban abiertos, en draft y con destino a `main` al momento de la consulta:

| PR | Rama / HEAD | Aporte declarado | Decisión de esta línea base |
|---|---|---|---|
| [#11](https://github.com/Xero-29/CYBER_AI/pull/11) | `codex/integration-hash-locks-2026-11-17-v2` / `04c001a206cde98613cf9c151ce4f6a95fb86a21` | Locks de dependencias, hashes, SBOM y reproducibilidad | No fusionar sin comparar con #12 y con `main`; revisar locks por plataforma y excepciones |
| [#12](https://github.com/Xero-29/CYBER_AI/pull/12) | `codex/reconcile-main-security-audit-2026-11-18` / `c2a397caf36f2661b6f0307168a0a24eee2f6d38` | Reconciliación selectiva de activos de seguridad e integridad | Revisar diff de tres vías; no copiar archivos compartidos a ciegas |
| [#13](https://github.com/Xero-29/CYBER_AI/pull/13) | `codex/deep-research-library-2026-11-18` / `d0a3934a473e3d1117c7410df253f659d5f475c3` | 192 desarrollos avanzados, worklist y registro de evidencia | Conservar como borradores; auditar especificidad y trazabilidad antes de integrar |
| [#14](https://github.com/Xero-29/CYBER_AI/pull/14) | `knowledge/develop-foundations` / `efa9108fe48c376b55b431f9078cf929ffd0a661` | Estándar experto para 48 áreas, profundización de Foundations y AI Red Team | Rama principal de trabajo curricular; integrar selectivamente después de auditoría |

Los estados de PR y sus SHAs son una fotografía de esta revisión. Deben actualizarse antes de cualquier integración.

## 4. Hallazgos de conocimiento

### 4.1 Cobertura de las 48 especialidades

La rama de desarrollo #14 contiene una auditoría de los 48 compendios. Su dictamen identifica:

- 41 compendios todavía iniciales y necesitados de desarrollo disciplinar profundo.
- Seis reescrituras disciplinares iniciales: identity, malware, forensics, incident_response, threat_intel y reverse.
- Foundations con una auditoría individual de sus siete temas base y 84 celdas tema × capa en estado `in_progress`; ninguna aprobada.
- AI Red Team con siete temas y 84 celdas en `in_progress`; ninguna aprobada.
- Ninguna base suficiente para declarar aprobadas globalmente las puertas G1–G8 o madurez experta.

La existencia de 48 carpetas, compendios, agendas y revisiones bibliográficas no equivale a profundidad validada. El inventario curricular ampliado de Foundations (nueve unidades / 102 subunidades, según el PR) debe reconciliarse explícitamente con la matriz disciplinar de siete temas y 84 celdas; no se deben mezclar denominadores.

### 4.2 Foundations

El compendio técnico ampliado tiene contenido sustantivo, modelos de seguridad, terminología y convenciones epistemológicas. El PR #14 también contiene dossiers, evaluaciones, soluciones, guías de evaluador y laboratorios sintéticos.

El dictamen interno de Foundations se declara **cerrado — no aprobado para promoción**, con madurez editorial M2. El dictamen coarse-grained registra 84/84 celdas en progreso para siete temas × doce capas. Sin embargo, la matriz granular V2 amplía el currículo a 102 subtemas y 1.224 comprobaciones de capa: solo 24 están en `in_progress` (FND-01.01 y FND-01.02), 1.200 están `not_assessed`, las 408 comprobaciones de capacidad tienen 8 `in_progress` y 400 `not_assessed`, y los 102 subtemas permanecen T0/O0. Ninguna comprobación está aprobada. Los denominadores describen dos niveles de granularidad distintos y no deben mezclarse. Por tanto, el módulo no se considera terminado. La siguiente iteración debe cerrar no conformidades concretas y completar la evaluación granular sin promover estados por inferencia.

### 4.3 AI Red Team

El dossier `AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md` es un avance técnico de aproximadamente 45 KB. Tiene un modelo sociotécnico de amenazas, límites de confianza, activos, autoridad, trazabilidad y siete temas con desarrollo teórico.

Su propia declaración lo clasifica como borrador profundo, no T4 ni validación operativa. La auditoría de 48 áreas registra 84 celdas `in_progress`, ninguna `passed`; G1–G4 y G6 en progreso, G5/G7 pendientes de etapa caliente y G8 bloqueada por revisión independiente. Se debe auditar tema por tema y capa por capa; el tamaño del dossier no basta para aprobarlo.

### 4.4 Las 192 brechas avanzadas

El PR #13 contiene `ADVANCED_GAP_DEVELOPMENT.md` (aprox. 618 KB) y una cola de 192 tareas. El registro de evidencia está vacío: no hay afirmaciones aprobadas como `supported`. La cola contiene 92 fuentes candidatas y declara expresamente que la asociación temática no constituye evidencia.

La inspección de una muestra confirma bloques metodológicos repetidos entre brechas distintas. Por tanto, el recuento 192/192 solo significa que hay 192 borradores estructurados. No significa 192 investigaciones específicas, fuentes leídas, afirmaciones demostradas ni módulos aceptados. La integración deberá exigir contenido propio por brecha y trazabilidad claim-to-source.

## 4.5 Precisión de la matriz granular de Foundations

La revisión posterior del archivo `FOUNDATIONS_SUBTOPIC_AUDIT_V2.json` del HEAD de PR #14 detectó una diferencia de granularidad que debe preservarse en todos los informes: el dictamen de 84 celdas corresponde a siete temas base × doce capas; la matriz V2 contiene 102 subtemas × doce capas (1.224 checks). En esa matriz solo FND-01.01 y FND-01.02 están en progreso (24/1.224 capas y 8/408 capacidades); los otros 100 subtemas no han sido evaluados. Los 102 subtemas siguen T0/O0 y el contador de aprobados es cero. Esta precisión sustituye cualquier lectura de “84/84” como si cubriera el currículo granular completo.

## 5. Reglas de reconciliación

1. No modificar `main` directamente durante la reconciliación.
2. Comparar cada PR contra el HEAD actual, no contra una base histórica.
3. Clasificar cada archivo como nuevo, modificación compatible, conflicto, duplicado o prototipo huérfano.
4. Revisar cambios de seguridad y dependencias antes de integrar.
5. Preservar versiones funcionales de `main` cuando una rama contenga una versión antigua.
6. Ejecutar pruebas de regresión después de cada integración selectiva.
7. Registrar el SHA exacto y los workflows que validan el resultado.
8. Mantener borradores de conocimiento en estados editoriales; solo revisión y evidencia permiten promoción.
9. No declarar G8 superada sin revisión independiente identificable.
10. Mantener T0–T5 y O0–O5 separados.

## 6. Próximas acciones obligatorias

### P0 — Cerrar la línea base

- Comparar #11 y #12 entre sí y con `main`; resolver solapamientos de locks, SBOM, safe I/O y archivos compartidos.
- Revisar #13 y #14 por separado; no fusionar documentos masivos sin auditoría de contenido.
- Actualizar el estado canónico y la matriz con el HEAD `387104756d0f8307c39a46a1ea2df07671bd81c9`, los dos workflows verdes y los PRs reales.
- Identificar todos los módulos, manifiestos y consumidores de conocimiento afectados por los cambios.

### P0 — Foundations

- Reconciliar currículo de 102 subunidades con siete temas base y sus capas.
- Usar el dictamen de no conformidad como lista de remediación.
- Trabajar cada tema y subtema con contenido disciplinar propio, problemas resueltos, diseño, evaluación y trazabilidad.
- Repetir auditoría hasta cerrar no conformidades documentales críticas; mantener revisión externa como bloqueo explícito cuando aplique.

### P0 — AI Red Team

- Auditar sus siete temas y doce capas, verificando profundidad específica.
- Completar mecanismos, modelos, casos de abuso sintéticos, detección, mitigación, verificación y regresión.
- No promover el módulo mientras queden no conformidades.

### P1 — Otras 46 especialidades y 192 brechas

- Avanzar secuencialmente después de cerrar Foundations y AI Red Team.
- Reescribir compendios genéricos y brechas repetitivas con investigación específica.
- Validar fuentes y afirmaciones individualmente; no autoaprobar el registro de evidencia.

## 7. Estado y límites de esta revisión

Esta línea base acredita acceso al repositorio, metadatos de Git, contenido de los archivos citados y resultados de dos workflows de CI sobre el HEAD indicado. No acredita:

- lectura integral de todas las fuentes primarias;
- validación científica de todo el corpus;
- revisión independiente externa;
- recuperación semántica con embeddings/proveedores reales;
- calidad de razonamiento de modelos conectados;
- aislamiento efectivo frente a cargas hostiles;
- pruebas de herramientas, laboratorios o infraestructura real;
- madurez operativa de las 48 especialidades.

**Conclusión:** el proyecto dispone de una arquitectura y una base documental considerable, pero el trabajo de conocimiento sigue en desarrollo editorial. La siguiente prioridad es reconciliar cambios sin dañar `main` y cerrar Foundations con evidencia, seguido de AI Red Team. Ninguna especialidad se declara experta por su estructura o volumen.
