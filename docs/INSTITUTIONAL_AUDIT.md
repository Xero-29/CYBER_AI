# Auditoría arquitectónica institucional de CYBER_AI

**Fecha:** 2026-11-12  
**Rama auditada:** `codex/security-integrity-audit`  
**Alcance:** revisión estática inicial del árbol, documentación, workflow y registros de GitHub Actions.  
**Estado:** diagnóstico preliminar; no es certificación de seguridad ni auditoría exhaustiva.

## 1. Criterio de evaluación

El objetivo de producto considerado es una plataforma modular y autónoma que pueda incorporar proveedores de IA sin modificar su núcleo, conservar memoria y conocimiento propios, reutilizar metodologías verificadas, aprender de resultados y ejecutar herramientas bajo políticas controladas.

La revisión distingue:
- **Observado:** respaldado directamente por archivos o resultados consultados.
- **Riesgo:** consecuencia plausible que requiere prueba o inspección adicional.
- **Pendiente:** no hay evidencia suficiente para concluir.

## 2. Hallazgos iniciales

### AUD-001 — La prueba de autoevaluación se invoca a sí misma
**Severidad:** crítica para CI  
**Evidencia:** `tests/test_entrypoint.py::EntryPointTests.test_self_test` ejecuta `cyber_ai.py --self-test`. En `cyber_ai.py`, `--self-test` ejecuta `unittest discover -s tests`, que vuelve a descubrir y ejecutar `test_self_test`.  
**Impacto:** recursión de procesos de prueba; puede consumir tiempo y recursos hasta que el runner interrumpa la ejecución.  
**Corrección propuesta:** `--self-test` debe validar dependencias/estructura o ejecutar un conjunto explícitamente acotado que no incluya la prueba que lo invoca. La suite completa debe ser ejecutada por CI directamente.  
**Estado:** defecto confirmado por inspección estática; falta corrección y prueba.

### AUD-002 — CI más reciente falló y no dejó trazas completas de dos errores
**Severidad:** alta  
**Evidencia:** ejecución GitHub Actions `43080801222`, job `130732667715`, Python 3.12.16. Las pruebas `test_assembles_three_fragments_without_losing_text` y `test_stops_and_preserves_checkpoint_when_paragraph_repeats` reportaron `ERROR`. La ejecución terminó con señal de apagado del runner y código 143 durante `test_self_test`. Los logs recuperables no contienen tracebacks para los dos errores.  
**Impacto:** la suite no está validada; la causa de los errores de checkpoint sigue abierta.  
**Corrección propuesta:** primero eliminar la recursión de AUD-001, volver a ejecutar CI y capturar el traceback completo de las pruebas de checkpoint. No corregir a ciegas.  
**Estado:** fallo confirmado; causas parciales pendientes.

### AUD-003 — El objetivo declarado en documentación no está alineado con la visión de plataforma
**Severidad:** alta para dirección del producto  
**Evidencia:** `CONTEXT.md` define el proyecto como herramienta ligera de ciberseguridad para Bug Bounty y auditoría autorizada. La arquitectura de proveedores y el Skillbook apuntan a una plataforma más general.  
**Impacto:** nuevos módulos pueden crecer en direcciones incompatibles; los criterios de aceptación no reflejan el producto deseado.  
**Corrección propuesta:** establecer un documento canónico de visión, límites y principios; distinguir el dominio inicial de ciberseguridad del núcleo general de agentes, memoria, conocimiento, skills y políticas.  
**Estado:** desalineación documental confirmada.

### AUD-004 — La aprobación de memoria se representa mediante campos declarativos
**Severidad:** alta para integridad del aprendizaje  
**Evidencia:** `learning_memory.py` acepta `verified_by="VERITAS"` y un veredicto textual como condiciones de aprobación; el registro JSONL conserva esas cadenas.  
**Impacto:** el módulo no verifica por sí mismo quién produjo la aprobación ni que la evidencia corresponda a una ejecución real e independiente.  
**Corrección propuesta:** introducir eventos de aprobación autenticables y vinculados a ejecución, hashes de evidencia, identidad de agente/versión/política, decisión y cadena de auditoría append-only. La memoria solo debe aceptar una referencia verificable a ese evento.  
**Estado:** debilidad de diseño confirmada; alcance de explotación pendiente.

### AUD-005 — Selección de capacidades y recuperación de memoria basadas en coincidencias léxicas
**Severidad:** media-alta  
**Evidencia:** `learning_memory.py` clasifica relevancia por intersección de tokens; `capability_selector.py` usa palabras clave y puntuaciones textuales.  
**Impacto:** falsos positivos, falsos negativos y selección de metodología/herramienta inadecuada.  
**Corrección propuesta:** búsqueda híbrida (metadatos + lexical + vectorial), filtros obligatorios de compatibilidad, prerrequisitos, permisos y versión; reranking y umbral de confianza; abstención cuando no haya evidencia suficiente. Medir precisión/recobrado con un conjunto de consultas etiquetadas.  
**Estado:** limitación observada; rendimiento real no medido.

### AUD-006 — La abstracción de proveedores es parcial, no universal
**Severidad:** media-alta para extensibilidad  
**Evidencia:** `llm_providers.py` contiene adaptadores implementados en el mismo módulo y lógica específica por protocolo; la documentación indica que un protocolo nuevo requiere un adaptador/código nuevo.  
**Impacto:** cambiar entre proveedores ya soportados puede ser configuración; incorporar cualquier proveedor futuro todavía puede requerir cambios en el código.  
**Corrección propuesta:** contrato formal de adaptador, registro/carga de plugins, declaración de capacidades, validación de compatibilidad y pruebas de contrato. Mantener el núcleo independiente de SDK y protocolo.  
**Estado:** limitación documentada.

### AUD-007 — Estado institucional de CI y control de cambios insuficiente
**Severidad:** alta  
**Evidencia:** la rama auditada fue reportada sin protección; el workflow ejecuta unittest, pero no se ha demostrado un conjunto de quality gates, cobertura, análisis estático, dependencias, seguridad de supply chain ni reglas obligatorias de revisión.  
**Impacto:** regresiones y cambios no revisados pueden incorporarse sin controles suficientes.  
**Corrección propuesta:** protección de rama, revisiones obligatorias, checks requeridos, pruebas deterministas, lint/type-check, análisis de dependencias/secretos, SBOM y artefactos con procedencia. Aplicar cambios de configuración solo con autorización explícita del propietario.  
**Estado:** brecha de gobernanza; configuración actual debe volver a verificarse antes de cambiarla.

## 3. Plan de trabajo priorizado

### Fase 0 — Recuperar una base verificable
1. Romper la recursión de `--self-test`.
2. Ejecutar la suite completa en Python 3.12 y conservar logs/tracebacks.
3. Resolver los errores de checkpoints con pruebas reproducibles.
4. Establecer CI verde repetible antes de ampliar funcionalidad.

**Criterio de salida:** suite completa repetible, sin procesos recursivos, resultados trazables y fallos reproducibles.

### Fase 1 — Contratos y arquitectura del núcleo
1. Especificar contratos de agentes, proveedores, herramientas, memoria, biblioteca y skills.
2. Definir capacidades declarativas y negociación de capacidades.
3. Separar núcleo, adaptadores y plugins.
4. Establecer versionado y migraciones de esquemas/datos.
5. Definir límites de confianza y flujos de autorización.

**Criterio de salida:** añadir un proveedor compatible y una herramienta como plugin sin modificar la lógica del núcleo; pruebas de contrato para cada adaptador.

### Fase 2 — Memoria, conocimiento y Skillbook
1. Inventario indexado y reconciliación entre índice y recursos.
2. Búsqueda híbrida con procedencia, filtros y umbrales.
3. Skill lifecycle: propuesta, sandbox, evaluación, aprobación, versionado, despliegue, rollback y retirada.
4. Vincular lecciones y skills con ejecuciones y evidencias verificables.
5. No reutilizar una skill si cambian versión, prerrequisitos, permisos o contexto material.

**Criterio de salida:** cada recuperación muestra por qué fue seleccionada; el sistema puede abstenerse; ninguna skill se promueve solo por una afirmación del modelo.

### Fase 3 — Seguridad y confiabilidad operativa
1. Autorización centralizada y deny-by-default para todas las herramientas.
2. Aislamiento de procesos, filesystem, red, secretos y sesiones.
3. Protección contra prompt injection y contenido externo no confiable.
4. Límites de recursos, timeouts, cancelación e idempotencia.
5. Recuperación probada ante caída, corrupción, concurrencia y reinicio.
6. Auditoría append-only y controles de retención.

**Criterio de salida:** pruebas de abuso, fallos e interrupciones pasan; operaciones privilegiadas requieren autorización verificable.

### Fase 4 — Calidad institucional y operación
1. Logging estructurado, métricas, trazas y correlación de tareas.
2. SLO/SLI, latencia, coste, tasa de error y calidad de recuperación.
3. SBOM, pinning y revisión de dependencias, escaneo de secretos.
4. Backups con restauraciones probadas y procedimientos de recuperación.
5. Matriz de riesgos, threat model, ADRs y documentación operativa.
6. Pruebas de carga, aislamiento multiusuario y compatibilidad.

**Criterio de salida:** se puede operar, auditar, recuperar y actualizar el sistema con procedimientos reproducibles.

## 4. Reglas de ejecución de esta auditoría

- Trabajar únicamente en `codex/security-integrity-audit`.
- No modificar `main`, no hacer merge, no desplegar.
- No ejecutar escaneos contra objetivos externos.
- No declarar corregido un hallazgo sin prueba y verificación posterior.
- No añadir complejidad o dependencias sin una necesidad demostrada.
- Registrar cada cambio con evidencia, pruebas y commit.
- Mantener separados hechos confirmados, hipótesis y pendientes.

## 5. Limitaciones de esta revisión

Esta primera pasada es estática y selectiva. No se ejecutó el repositorio localmente, no se inspeccionaron todavía todos los módulos ni todas las rutas de herramientas, no se hizo threat modeling completo y no se probaron fallos de almacenamiento, concurrencia, aislamiento ni restauración. Los hallazgos anteriores no equivalen a una certificación ni a una afirmación de que el sistema sea inseguro en todos esos aspectos.
