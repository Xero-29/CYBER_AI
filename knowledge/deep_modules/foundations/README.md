# Módulo de profundización: Fundamentos

> **Estado editorial:** borrador estructurado para desarrollo y revisión. No equivale a contenido experto validado ni a fuente externa verificada.
> **Dominio:** `foundations` · **Currículo:** 2.0.0

## Propósito y límites

Currículo técnico de Fundamentos; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Este módulo amplía el currículo con una ruta de estudio y validación por tema. Toda actividad activa debe limitarse a activos propios o expresamente autorizados, con alcance, ventana, límites de impacto y criterio de parada documentados. Los laboratorios deben usar entornos aislados y datos sintéticos.

## Competencias que deben demostrarse

Al completar el módulo, el analista debe poder:
- Explicar la arquitectura, los componentes, las dependencias y los límites de confianza del dominio.
- Construir un inventario de activos, identidades, datos, interfaces y propietarios.
- Modelar amenazas y priorizar riesgos según contexto e impacto, sin confundir puntuaciones técnicas con riesgo empresarial.
- Seleccionar controles proporcionales y asociarlos a evidencia verificable.
- Ejecutar un procedimiento reproducible, documentar incertidumbres y verificar la remediación.
- Comunicar hallazgos con alcance, precondiciones, impacto, evidencia mínima, mitigación y retest.

## Ruta técnica por temas

### 1. Modelos de seguridad y confianza
Distinguir propiedades, políticas, mecanismos, controles y garantías. Comparar DAC, MAC, RBAC y ABAC; analizar mediación completa, separación de funciones, Zero Trust y límites de confianza. No confundir autenticación con autorización ni una VLAN con una frontera de seguridad.

### 2. Inventario y clasificación de activos
Reconciliar fuentes de descubrimiento con identificadores estables y procedencia. Asignar propietario, custodio, entorno, criticidad, clasificación de datos, dependencias y frescura. Explicar sesgo de observación, shadow IT, activos efímeros y límites del CMDB.

### 3. Superficie de ataque y modelado de amenazas
Construir DFD y grafos de activos/identidades; aplicar STRIDE, misuse cases y árboles de ataque según la pregunta. Toda ruta debe contener actor, precondiciones, transición, activo, efecto, control, telemetría e incertidumbre. Una ruta en un grafo no demuestra explotabilidad.

### 4. Identidad, privilegios y autenticación
Distinguir identificación, autenticación, autorización y auditoría. Analizar ciclo de vida, sesión, token, scopes, audience, revocación, privilegios, cuentas de servicio y acceso de emergencia. Los detalles de protocolos y configuración avanzada pertenecen al módulo Identity.

### 5. Seguridad de redes y sistemas
Razonar sobre capas, procesos, interfaces, servicios, segmentación, configuración, dependencias y telemetría. Identificar límites administrativos y fallos comunes; derivar controles verificables sin sustituir las especialidades de Network, Linux, Windows/AD y Cloud.

### 6. Gestión de vulnerabilidades
Distinguir vulnerabilidad, exposición, severidad técnica, explotación y riesgo contextual. Validar inventario, aplicabilidad, exposición, KEV, ventana de parcheo, mitigación compensatoria y retest. CVSS no equivale automáticamente a prioridad de negocio.

### 7. Telemetría, respuesta y recuperación
Diseñar cobertura de eventos, sincronización temporal, integridad, retención, correlación, escalamiento y preservación de evidencia. Separar contención, erradicación, recuperación y reconstrucción de confianza. Un backup existente no demuestra que la restauración sea íntegra ni oportuna.

### Profundización específica
- [Ingeniería del riesgo y assurance V1](FOUNDATIONS_RISK_ENGINEERING_V1.md): escenarios de pérdida, incertidumbre, estimación, control y ejemplo resuelto.
- [Compendio técnico general](TECHNICAL_COMPENDIUM.md): modelos, activos, arquitectura, amenaza, control, assurance y recuperación.
- [Mapa curricular de 102 subtemas](FOUNDATIONS_CURRICULUM_MAP_V2.md): frontera y desglose disciplinar.

## Procedimiento de trabajo del dominio

1. **Preparación:** registrar autorización, objetivo, propietario, alcance, exclusiones, ventana y criterios de parada.
2. **Descubrimiento:** inventariar activos, versiones, configuraciones, identidades, datos y dependencias sin ampliar el alcance.
3. **Modelo:** representar arquitectura y flujos; identificar límites de confianza, escenarios de abuso y controles existentes.
4. **Evaluación:** seleccionar pruebas proporcionales y reproducibles; justificar herramientas, parámetros y límites de impacto.
5. **Análisis:** separar observaciones, inferencias e hipótesis; correlacionar evidencia y registrar falsos positivos.
6. **Tratamiento:** proponer mitigación priorizada, responsable, riesgo residual y plan de reversión.
7. **Verificación:** repetir la prueba pertinente, comprobar regresiones y conservar evidencia saneada.
8. **Cierre:** documentar cobertura, exclusiones, incertidumbre, versiones y fecha de próxima revisión.

## Laboratorio de referencia

**Entorno:** laboratorio local o tenant/cuenta de pruebas aislado, sin datos reales ni objetivos de terceros. Usar snapshots, privilegios mínimos, límites de CPU/memoria/tiempo y salida de red deshabilitada salvo necesidad justificada.

**Escenarios mínimos:**
1. Establecer una línea base segura y conservar configuración/evidencia inicial.
2. Introducir una condición defectuosa sintética representativa del dominio.
3. Detectar y analizar la condición mediante un procedimiento documentado.
4. Aplicar una corrección reversible y repetir la prueba.
5. Ejecutar regresión para verificar que la corrección no rompe controles relacionados.

**Artefactos:** diagrama, inventario, modelo de amenazas, matriz de controles, procedimiento, datos sintéticos, resultados esperados, resultados observados, registro de riesgos y prueba de regresión.

## Evaluación y criterios de aceptación

Evaluar precisión técnica, cobertura, reproducibilidad, calidad de evidencia, seguridad/proporcionalidad, análisis de falsos positivos y verificación de mitigación. La evaluación no se aprueba si falta autorización, procedencia de datos, evidencia reproducible o retest.

La rúbrica debe incluir preguntas conceptuales, análisis de un escenario, ejecución de laboratorio, revisión de evidencia y explicación de decisiones. Las respuestas deben justificar por qué otras opciones son incorrectas.

## Fuentes y procedencia pendientes de verificación

No se declaran fuentes verificadas por la mera inclusión de nombres o enlaces. Para cada referencia que se incorpore, registrar: título, editor, URL canónica, versión/edición, fecha de publicación o actualización, fecha de consulta, licencia/condiciones de uso, SHA-256 del artefacto descargado cuando corresponda, temas respaldados y revisor. Priorizar documentación primaria de estándares, fabricantes y proyectos oficiales; usar investigación secundaria solo como complemento.

**Estado de referencias de este módulo:** pendiente de curación, verificación de vigencia, licencia y correspondencia con cada tema.

## Lista de control de publicación

- [ ] Desarrollar explicación técnica original y específica para cada tema.
- [ ] Añadir diagramas, tablas de protocolos/configuración y ejemplos reproducibles.
- [ ] Incorporar referencias primarias con procedencia y licencia comprobadas.
- [ ] Añadir al menos un caso de estudio y un laboratorio con datos sintéticos.
- [ ] Revisar comandos y configuraciones contra versiones concretas.
- [ ] Añadir pruebas de conocimiento con respuestas razonadas.
- [ ] Obtener revisión técnica independiente y registrar cambios.
- [ ] Actualizar fecha de revisión y estado de madurez solo con evidencia.

## Madurez

`draft_structured_not_expert_validated` — este documento organiza el trabajo de profundización; no acredita dominio experto, exactitud de todos los procedimientos ni validación operacional.


## Actualización de desarrollo — 2026-11-20

### Subtemas iniciales ampliados
- FND-01.01: crosswalk de seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia; modelos de riesgo, métricas, interacciones, límites de estándares y aplicabilidad colombiana condicionada.
- FND-01.02: modelo CIA y propiedades extendidas; autenticidad, autorización, accountability, non-repudiation, provenance, freshness, privacy, safety, reliability y resilience.
- Instrumentos en frío: FND-01.01 V2 y FND-01.02 V1 preparados, ninguno administrado.

### Laboratorios sintéticos
El runner contiene 13 laboratorios sintéticos. LAB-FND-08A a LAB-FND-12A amplían la cobertura:
- LAB-FND-08A: conflicto fail-safe/fail-secure y salida de emergencia.
- LAB-FND-09A: cifrado y control de acceso no equivalen a privacidad.
- LAB-FND-10A: recuperar servicio no equivale a recuperar confianza.
- LAB-FND-11A: dependencia común puede anular redundancia nominal.
- LAB-FND-12A: firma/hash válidos no prueban verdad ni calibración.
- LAB-FND-13A: inventario orientado a misión detecta ownership ausente, registros obsoletos, datos sin clasificar, logging insuficiente y soporte desconocido.

Los modelos se ejecutan en CI con datos sintéticos. No son pruebas físicas, certificación de safety ni validación operacional de un sistema real.

### Skills candidatas
Dos especificaciones se indexan desde knowledge/skills/candidates. No están activas ni registradas en skillbook. Requieren evidencia de ledger, ejecuciones repetidas y revisión independiente para promoción.

### Madurez
Solo dos de 102 subtemas tienen esta ampliación documental. L1–L12 continúan in_progress; 0 capas/capacidades aprobadas; T0/O0. La matriz de doce capas y el log de remediación identifican lo que sigue pendiente.


### FND-01.03 — Ontología e inventario de activos

Se añadió el tercer subtema del orden curricular: ontología activo/recurso/sujeto/objeto/dato/proceso/servicio/misión/stakeholder, grafo de dependencias, esquema de inventario, fuentes NIST/CISA/ISO, evaluación en frío V1 y laboratorio sintético LAB-FND-13A. Sigue en progreso y T0/O0.


## Laboratorio de ingeniería del riesgo

El ejemplo cuantitativo del dossier se ejecuta con:

```bash
python3 knowledge/deep_modules/foundations/labs/risk_engineering.py
python3 -m unittest discover -s tests -p 'test_foundations_risk_lab.py' -v
```

Produce LAB-FND-14A: EAL basal/residual, pérdida evitada, beneficio neto simplificado y sensibilidad bajo supuestos sintéticos. No sustituye calibración con datos reales ni aceptación formal del riesgo. La integración y el resultado CI de esta ampliación deben verificarse en el SHA correspondiente antes de registrar el laboratorio como validado.


### LAB-FND-14A — sensibilidad de riesgo ampliada

El runner valida entradas finitas y genera una cuadrícula determinista de 27 combinaciones de frecuencia basal, pérdida basal y frecuencia residual relativa. La cuadrícula es análisis factorial de escenarios, no Monte Carlo ni estimación probabilística; todos los factores siguen siendo hipotéticos y no elevan la madurez del módulo.
