# Auditoría y reconciliación de conocimiento — PR #13 y #14

**Fecha:** 2026-11-20  
**Repositorio:** `Xero-29/CYBER_AI`  
**Base encadenada:** `codex/reconcile-pr11-pr12-2026-11-20`  
**HEAD de PR #13:** `d0a3934a473e3d1117c7410df253f659d5f475c3`  
**HEAD de PR #14:** `efa9108fe48c376b55b431f9078cf929ffd0a661`  
**Estado:** auditoría documental completada; integración selectiva pendiente. Ninguno de los dos PR originales se fusiona automáticamente.

## 1. Dictamen ejecutivo

PR #13 aporta una infraestructura útil de trazabilidad de investigación, 48 estudios iniciales, 48 dossiers de cinco secciones y una cola de 192 brechas. PR #14 aporta el estándar de investigación experto, el mapa curricular de 48 áreas, auditorías granulares, trabajo específico de Foundations y un dossier inicial de AI Red Team.

Los dos PR tienen CI verde en sus HEADs exactos, pero ese CI demuestra que los tests y validadores de software ejecutan correctamente. No certifica la exactitud semántica, lectura integral de fuentes, profundidad disciplinar ni revisión independiente de la biblioteca.

**Decisión:** conservar los sistemas de auditoría, el estándar, los mapas curriculares y los documentos disciplinares como borradores con estado explícito. No promover los 48 dominios ni las 192 brechas a nivel experto. Reconciliar primero manifiestos, fuentes y workflow; después desarrollar y evaluar subtema por subtema.

## 2. Evidencia verificada de PR #13

### 2.1 Estudios y dossiers

- Hay 48 archivos `RESEARCH_STUDY.md`, uno por especialidad.
- Hay 48 archivos `DEEP_SECTIONS.md`, con cinco secciones: modelo de amenazas, detección, respuesta, casos prácticos y referencias.
- Los ejemplos inspeccionados son específicos al dominio, pero breves: Foundations 2.297 bytes; AI Red Team 1.773 bytes; Crypto 1.911 bytes. Son fichas técnicas iniciales, no compendios de investigación expertos.
- El validador `knowledge_quality.py` comprueba encabezados, umbrales de 20 palabras por sección profunda, mínimo de 250 palabras por estudio, dos referencias HTTPS y presencia de campos curriculares. No mide similitud entre dominios, corrección técnica, suficiencia de mecanismos, calidad metodológica ni si una referencia respalda una afirmación.
- Los comentarios del PR reportan 48/48 estudios y 240/240 comprobaciones estructurales en un HEAD anterior. Ese resultado es un umbral editorial automatizado; no se interpreta como profundidad experta.

### 2.2 Las 192 brechas

`ADVANCED_GAP_DEVELOPMENT.md` tiene 618.752 bytes y 192 encabezados de tema distintos. La inspección de secciones de Foundations y otros dominios detectó párrafos metodológicos idénticos o casi idénticos reutilizados entre brechas, incluidos propósito genérico, modelo de amenazas, controles y procedimiento reproducible. Cambia parte del texto de implementación por dominio, pero no equivale a 192 investigaciones independientes.

La propia declaración del archivo lo clasifica como borrador técnico estructurado, sin afirmar lectura integral, experimentos ejecutados ni revisión independiente.

La nueva auditoría automatizada de reutilización cuantifica el problema: 1.344 bloques de sección distribuidos en 192 brechas, solo 77 variantes únicas y 84.015 pares de duplicación exacta (82.208 pares entre dominios). En “Arquitectura y modelo de amenazas”, “Procedimiento reproducible”, “Laboratorio y evaluación” y “Evidencia y limitaciones” existe una sola variante reutilizada en los 192 temas. “Desarrollo técnico y controles” tiene siete variantes (máxima reutilización 55); “Fuentes de partida”, 18 variantes (máxima 120); “Propósito y alcance”, 48 variantes (máxima 4). La herramienta `knowledge_depth_audit.py` bloquea la promoción: 0 claims respaldados, 192 experimentos sin evaluar, 192 revisiones independientes sin iniciar y 0 brechas elegibles como expertas.

El registro `VALIDATION_WORKLIST_192.json` confirma:
- 48 dominios, 192 tareas y 92 fuentes candidatas.
- 192/192 tareas con fuentes candidatas mapeadas, no con claims verificados.
- 192/192 con estado experimental `not_assessed`.
- 192/192 con revisión independiente `not_started`.
- `CLAIM_EVIDENCE_REGISTER.json` contiene cero afirmaciones.

**Conclusión:** 192/192 significa 192 borradores/filas de trabajo. No significa 192 módulos expertos ni 192 investigaciones validadas. Mantenerlos como backlog hasta desarrollar contenido único y verificar afirmaciones.

### 2.3 Validación y trazabilidad

`research_validation.py` aporta controles útiles: valida IDs, tareas, fuentes, localizadores, extractos, tipo de evidencia, fecha y revisión; no pretende juzgar automáticamente la semántica de la cita. Debe conservarse como infraestructura de trazabilidad, después de revisar rutas, límites de entrada y correspondencia de registros.

El registro central de fuentes de PR #13 tiene 154 IDs únicos; el registro de fuentes de field studies contiene 92 candidatos usados por la worklist.

## 3. Evidencia verificada de PR #14

### 3.1 Estándar y cobertura global

PR #14 incorpora:
- estándar experto de doce capas por tema;
- separación de madurez teórica T0–T5 y operativa O0–O5;
- ocho puertas G1–G8;
- programa de finalización para 48 especialidades;
- tracker y protocolo de ejecución en frío.

La auditoría global cubre 48 áreas y siete temas iniciales por área (336 temas). Los estados de capa y puerta siguen siendo de trabajo; la existencia del estándar no certifica su cumplimiento.

### 3.2 Foundations — precisión obligatoria de granularidad

Hay dos matrices con granularidad distinta y no se deben mezclar:

1. El dictamen coarse-grained de Foundations informa siete temas × doce capas = 84 celdas, todas `in_progress`.
2. `FOUNDATIONS_SUBTOPIC_AUDIT_V2.json` amplía el currículo a 102 subtemas × doce capas = 1.224 comprobaciones y 408 capacidades.

En la matriz granular V2:
- 24/1.224 comprobaciones de capa están `in_progress`, correspondientes únicamente a FND-01.01 y FND-01.02.
- 1.200/1.224 están `not_assessed`.
- 8/408 comprobaciones de capacidad están `in_progress`; 400/408 están `not_assessed`.
- Los 102 subtemas permanecen T0/O0.
- Aprobados: 0.

Por tanto, **Foundations no tiene 84/84 subtemas o capas del currículo completo desarrollados**. El 84/84 pertenece exclusivamente a la matriz antigua de siete temas base. El currículo granular de 102 subtemas está mayoritariamente sin evaluar.

El dossier de 83 KB contiene contenido sustantivo para los fundamentos y materiales de evaluación, pero la matriz V2 y el dictamen identifican no conformidades abiertas: lectura integral de fuentes, revisión jurídica/sectorial cuando aplique, administración supervisada, doble calificación y revisión disciplinar independiente.

Los siete laboratorios son sintéticos y deterministas. Su resultado registrado 7/7 y las ocho pruebas unitarias prueban el comportamiento de esos fixtures, no generalización a sistemas reales, interoperabilidad con IdP/KMS/SIEM ni eficacia de controles en producción.

### 3.3 AI Red Team

`AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md` tiene 45.520 bytes y desarrolla siete temas con doce capas. Se declara explícitamente borrador técnico profundo, no T4 ni validación operativa.

La matriz global marca 84/84 celdas de los siete temas base como `in_progress`, ninguna como `passed`. G1–G4 y G6 siguen `in_progress`; G5/G7 `not_started`; G8 `blocked`. El propio informe señala currículo ampliado/subtemas faltantes, revisión de fuentes y auditoría adversarial pendientes.

**Conclusión:** es un avance conceptual útil, no un módulo experto aprobado.

### 3.4 CI de los HEADs exactos

- PR #13, SHA `d0a3934a473e3d1117c7410df253f659d5f475c3`: checks Python y Docker Sandbox en éxito ([Python](https://github.com/Xero-29/CYBER_AI/actions/runs/44446910361), [Docker](https://github.com/Xero-29/CYBER_AI/actions/runs/44446910359)).
- PR #14, SHA `efa9108fe48c376b55b431f9078cf929ffd0a661`: nueve check-runs consultados en éxito, incluidos Python, Docker Sandbox y laboratorios Foundations en Python 3.11, 3.12 y 3.13.

La evidencia de CI no se extrapola a validación científica ni a madurez experta.

## 4. Conflictos de integración identificados

### 4.1 Manifiesto de paquetes

Ambos PR incluyen 48 IDs de áreas y no falta ninguna especialidad. Pero:
- PR #13 tiene `research_study_path` para las 48 áreas.
- PR #14 tiene 14 campos de calidad/estado adicionales (estándar, perfil experto, puertas, estado de compendio, agenda, revisión bibliográfica, laboratorio, validación y nota de madurez), pero no contiene `research_study_path`.

**Resolución requerida:** usar los campos de calidad más detallados de PR #14 y añadir los 48 `research_study_path` de PR #13. Validar que todas las rutas existan, permanezcan dentro del repositorio y correspondan al ID correcto.

### 4.2 Registro de fuentes

- PR #13: 154 IDs únicos.
- PR #14: 127 IDs únicos.
- Intersección: 74 IDs.
- Exclusivos PR #13: 80.
- Exclusivos PR #14: 53.
- En 14 de los 74 IDs compartidos hay cambios de estado o metadatos. En general PR #14 registra un alcance de revisión más específico (p. ej., secciones seleccionadas, metadatos y erratas) y añade localizadores/fecha cuando corresponde.

**Resolución requerida:** unión de registros con deduplicación por ID; en las 14 discrepancias preservar el alcance y fecha documentados de PR #14, sin convertir revisión de metadatos o secciones seleccionadas en lectura integral. Revisar posibles alias de IDs antes de dar por cerrada la unión. No convertir fuentes candidatas en fuentes probatorias.

### 4.3 README de módulos y packs

Los README de PR #13 enlazan los 48 estudios; los de PR #14 describen el estándar, el estado de los compendios y la auditoría de profundidad. Para rutas compartidas, combinar enlaces y metadatos sin perder las declaraciones de borrador y limitaciones. El README de Foundations de PR #14 es más reciente (2.1.0 frente a 2.0.0); no sobrescribirlo con la versión antigua de PR #13.

### 4.4 Workflow Python

Se deben conservar simultáneamente:
- del PR #17 (reconciliación #11/#12): `--require-hashes`, locks runtime/sandbox/documentales, captura de artefactos y SBOMs;
- del PR #13: `knowledge_bootstrap.py --dry-run`, auditoría de estudios y trazabilidad;
- del PR #14: reproducibilidad de los laboratorios Foundations en Python 3.11/3.12/3.13 y comparación exacta de `results.json`.

No copiar un workflow completo sobre otro. Construir uno solo y probar cada job en el SHA integrado.

## 5. Política de integración selectiva

### Integrar como infraestructura/documentación de control
- `EXPERT_RESEARCH_STANDARD.md`, protocolo, tracker y programa de cierre de 48 áreas.
- `research_validation.py` y sus pruebas, tras revisión de rutas y robustez.
- Worklist de 192 y registro de claims vacíos, conservando estados pendientes.
- Matriz global de 48 áreas y auditoría granular Foundations.
- Estudios y dossiers por dominio como borradores versionados, nunca como material validado automáticamente.
- Labs sintéticos y sus pruebas, manteniendo límites de alcance.

### Integrar con reconciliación manual
- Workflow Python.
- `knowledge/packs/manifest.json`.
- `knowledge/research/source_registry.json`.
- `knowledge/deep_modules/README.md` y README compartidos de packs.
- Currículo global, especialmente la relación entre 336 temas base y 102 subtemas granulares de Foundations.

### No promover ni presentar como terminado
- Las 192 brechas avanzadas.
- Los 48 estudios por cumplir umbrales de palabras/URLs.
- Los 240 bloques profundos por superar mínimos de 20 palabras.
- Foundations por el 84/84 de la matriz coarse-grained.
- AI Red Team por sus 84 celdas en progreso.
- Ninguna puerta G1–G8 sin evidencia específica y revisión correspondiente.

## 6. Secuencia de remediación

1. Reconciliar workflow, manifiesto y source registry; validar integridad de rutas/IDs.
2. Integrar estándar, tracker, protocolo, matriz granular y validadores como infraestructura de aceptación.
3. Reforzar `knowledge_quality.py`: detectar texto repetido, evaluar especificidad por dominio y diferenciar integridad editorial de suficiencia técnica. No permitir que mínimos de palabras se presenten como profundidad.
4. Cerrar Foundations subtema por subtema (102), comenzando por FND-01.01 y FND-01.02, cerrando no conformidades con evidencia.
5. Auditar AI Red Team con el mismo nivel granular; definir currículo completo y no solo siete temas base.
6. Después de Foundations y AI Red Team, desarrollar las otras 46 especialidades.
7. Validar individualmente las afirmaciones de las 192 brechas; no autoaprobar.


## 8. Material de evaluación reservado

No se copia `FOUNDATIONS_ASSESSOR_KEY_V1.md` al paquete público de conocimiento. El archivo se identifica explícitamente como clave de corrección para evaluadores y advierte que no debe entregarse antes de la prueba. Exponerlo junto al material de estudio permitiría memorizar respuestas y contaminar la evaluación. Debe mantenerse en un repositorio/área de evaluadores con control de acceso, o entregarse solo después de la evaluación. La guía de evaluación y el protocolo pueden permanecer públicos; la clave de respuestas no.

## 9. Estado final de esta auditoría

La estructura de PR #13 y PR #14 es útil y sus CI exactos están verdes. La biblioteca aún no alcanza aceptación experta. Se recomienda integración selectiva y encadenada sobre la rama de reconciliación de PR #17, manteniendo ambos PR originales en draft hasta que el contenido, manifiestos, fuentes y workflow hayan sido reconciliados y auditados.

**No se fusiona PR #13 ni PR #14 en bloque. No se cambia ningún estado de madurez a partir de volumen, encabezados, referencias o CI solamente.**


## 6. Actualización de Foundations — 2026-11-20

FND-01.01 incorpora un crosswalk disciplinar de safety/security/privacy/reliability/availability/resilience y 11 fuentes oficiales adicionales con estados de revisión diferenciados. FND-01.02 incorpora una síntesis CIA y propiedades extendidas, contraejemplos y un instrumento en frío V1 no administrado. El bootstrap ahora valida e indexa 332 documentos: 328 documentos: 48 paquetes, 48 dossiers DEEP_SECTIONS, 48 estudios RESEARCH_STUDY, 48 compendios técnicos, 48 agendas, 48 revisiones bibliográficas, 41 documentos suplementarios y 3 Skills candidatas. Se añadieron cinco laboratorios sintéticos (LAB-FND-08A a LAB-FND-12A); se ejecutan en CI, pero no son pruebas físicas ni validación operacional.

Los dos subtemas siguen con sus 12 capas en progreso, 0 aprobadas y madurez T0/O0. El mapa de cobertura por doce capas registra explícitamente los faltantes. Las Skills candidatas se indexan como conocimiento provisional; no se registran en skillbook ni se activan.


## FND-01.03 — Tercer subtema de Foundations

Se incorporó el desarrollo de activo/sujeto/objeto/recurso/dato/proceso/servicio/misión/stakeholder, el instrumento en frío V1, la Skill candidata no activa y LAB-FND-13A. El registro de subtemas refleja 12 capas y 4 capacidades en progreso, sin aprobación. El bootstrap pasa a 332 documentos.
