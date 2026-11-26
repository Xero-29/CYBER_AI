# Estado canónico de CYBER_AI — 2026-11-20


# Remediación disciplinar Foundations y AI Red Team — 2026-11-24

**Rama de trabajo:** `codex/foundations-ai-redteam-remediation-2026-11-24`  
**Base:** `codex/reconcile-knowledge-pr13-pr14-2026-11-20` (PR #18; PR #18 continúa Draft).  
**Regla de integración:** no se modifica `main`, no se fusiona PR #18 ni se altera la rama `codex/security-integrity-audit`.

## Trabajo incorporado

- Foundations: nuevo `knowledge/deep_modules/foundations/FOUNDATIONS_RISK_ENGINEERING_V1.md`, con escenarios de pérdida, estimación cuantitativa y ordinal, incertidumbre, assurance, análisis de controles, ejemplo de CI/CD, evaluación y preguntas en frío. El texto declara explícitamente que las fuentes no se han leído integralmente y que el laboratorio propuesto no se ha ejecutado.
- AI Red Team: sustituido `TECHNICAL_COMPENDIUM.md` que repetía bloques genéricos por un mapa disciplinar con siete líneas específicas y navegación a los dossiers. Reescritas las siete áreas temáticas del README para eliminar el placeholder común.
- AI Red Team: nuevo `AI_RED_TEAM_TEST_CATALOG_V1.md` con nueve casos ART-01…ART-09: inyección directa/indirecta, persistencia RAG, aislamiento multi-tenant, poisoning, abuso de herramientas, canaries, salida insegura, consumo/bucles y validez del benchmark. Incluye fixtures sintéticos, invariantes, evidencia, métricas y estados PASS/FAIL/INCONCLUSIVE/NOT RUN. Son protocolos; no se reportan como ejecutados.
- Advanced gap development: reemplazados los siete bloques de plantilla en cuatro temas de Foundations y cuatro de AI Red Team por análisis disciplinar específico. Los otros 46 dominios no se modificaron.
- Auditoría exacta del documento después del cambio: 48 dominios, 192 temas y 1.344 bloques conservados. Los pares de duplicación exacta bajaron de 84.015 a 77.338 (-6.677); los pares entre dominios bajaron de 82.208 a 75.610 (-6.598). La duplicación residual sigue siendo alta; esta remediación no la resuelve globalmente.
- Se añadieron pruebas de regresión para evitar el retorno de placeholders, comprobar que los cinco bloques centrales de los ocho temas remediados son únicos por tema y verificar el estado honesto de las fuentes. Se ajustó la expectativa del auditor: la reutilización máxima del bloque de arquitectura baja de 192 a 184.
- Se actualizaron los registros canónico y de field studies con OWASP LLM Top 10 2026, OWASP Top 10 for Agentic Applications 2026, OWASP GenAI Red Teaming Guide y NIST AI 200-3 ARIA. Se registraron como páginas/fichas consultadas; no como lectura integral ni claims respaldados.

## Estado de evidencia y pendientes

- **CI verde en HEAD `ce82f4dd7318f093cbdc0f1926f6ac2bd50a866b`:** [Actions run 45453949310](https://github.com/Xero-29/CYBER_AI/actions/runs/45453949310) concluyó `success`. `verify.sh` ejecutó 694 pruebas (1 skipped); reproducibilidad Foundations pasó en Python 3.11, 3.12 y 3.13; Windows allowlist smoke pasó. El artefacto `results.json` fue alineado con el orden determinista del runner.
- En ese mismo HEAD, `knowledge_bootstrap.py --dry-run` seleccionó 334 documentos.
- Auditoría de profundidad: 77.338 pares de duplicación exacta, 75.610 entre dominios, 0 claims respaldados, 192 experimentos no evaluados, 192 revisiones independientes no iniciadas, 0 brechas expert-ready.
- Auditoría de investigación: 48 agendas completas, 48 revisiones bibliográficas, 226 fuentes en el registro canónico; 5 solo con metadatos revisados, 52 páginas/documentos revisados y 63 referencias de catálogo sin revisión de contenido.
- Auditoría de validación: 48 dominios, 192 módulos, 96 fuentes en el registro de field studies; 0 afirmaciones respaldadas y 0 fuentes con lectura integral registrada. Integridad estructural OK; estado `structurally_valid_needs_research`.
- Auditoría global: 48 áreas con referencias asociadas; 336 requisitos, 432 artefactos y 336 puertas, todos con 0 evaluados; 0 especialidades validadas y cobertura exhaustiva no demostrada.
- Auditoría de procedencia: `needs_review`, 138 fuentes, 0 revisadas, 276 pendientes y 0 errores. La revisión de página/ficha en el registro bibliográfico no sustituye aprobación de licencia, fecha de revisión ni intervalo de vigencia de cada fuente de módulo.
- Los dos documentos nuevos están registrados como `supplemental_documents` del manifiesto (Foundations risk engineering y AI Red Team test catalog); el bootstrap offline los selecciona con IDs estables por ruta y SHA-256. El total declarado de documentos seleccionables pasa de 332 a 334.
- No se añadieron afirmaciones a `CLAIM_EVIDENCE_REGISTER.json`; continúa vacío. Las 192 tareas de investigación mantienen estado experimental no evaluado y revisión independiente no iniciada.
- Ningún subtema de Foundations o AI Red Team se promueve de T0/O0 por este trabajo. Los ocho temas remediados son contenido editorial específico, no aceptación experta.
- Los nueve casos AI Red Team y el ejemplo de riesgo Foundations no se han ejecutado. No hay resultados experimentales ni revisión independiente asociados a estos documentos.
- Pendiente: ejecutar CI en el HEAD final de esta rama, revisar fallos, continuar los 98 subtemas restantes de Foundations (102 total; solo cuatro temas avanzados de este documento y contenido previo no implican cierre granular), desarrollar las restantes brechas de AI Red Team, reducir la duplicación de los otros 40 dominios y realizar lectura integral de fuentes.


**Repositorio:** https://github.com/Xero-29/CYBER_AI  
**Rama principal:** `main` — sin modificar durante esta secuencia.  
**HEAD de main auditado:** `387104756d0f8307c39a46a1ea2df07671bd81c9`.

## Integración encadenada

| PR | Rama | Estado | Función |
|---|---|---|---|
| #16 | `codex/cold-phase-baseline-2026-11-20` | Draft | Línea base; corregida la granularidad de Foundations |
| #17 | `codex/reconcile-pr11-pr12-2026-11-20` | Draft | Locks SHA-256, SBOM, safe I/O, wheelhouse y pruebas |
| #18 | `codex/reconcile-knowledge-pr13-pr14-2026-11-20` | Draft | Currículo, biblioteca, trazabilidad y gates de profundidad |
| #19 | — | Cerrado sin fusionar | Intento de integrar PR #14 completo; se detectó conflicto, se pasó a integración selectiva |

PR #18 tiene como base la rama de PR #17. No se debe fusionar #18 antes de integrar #17. Los PR originales #11–#14 siguen separados; no se fusionaron en bloque.

## Evidencia de software

- PR #17: [Python Tests](https://github.com/Xero-29/CYBER_AI/actions/runs/44795901916) y [Docker Sandbox](https://github.com/Xero-29/CYBER_AI/actions/runs/44795901820) terminaron en éxito sobre el HEAD de esa rama.
- PR #18, HEAD actual de integración: [CI 44801690723](https://github.com/Xero-29/CYBER_AI/actions/runs/44801690723) — 683 pruebas unitarias, allowlist Windows y laboratorios Foundations en Python 3.11/3.12/3.13, todos en éxito.
- El gate `knowledge_depth_audit.py` se ejecuta en CI y detecta reutilización de boilerplate; no concede aceptación experta.

## Estado real de la biblioteca

- 48/48 paquetes con estructura base; 48 estudios `RESEARCH_STUDY.md`; 48 `DEEP_SECTIONS.md`.
- 20.588 palabras en estudios y 218 referencias HTTPS. Son borradores con umbral editorial mínimo; no implican lectura integral ni verificación de afirmaciones.
- 48/48 agendas estructuralmente completas; 226 IDs de fuente registrados (16 añadidos en FND-01.01/01.02/01.03); 0 fuentes con lectura integral registrada en la worklist; 192 tareas siguen con fuentes candidatas, no claims verificados.
- Registro de claims: 0 claims aprobados.
- Las 192 brechas tienen 1.344 bloques de sección, 77 variantes únicas y reutilización de boilerplate. La auditoría encontró 84.015 pares de duplicación exacta, 82.208 entre dominios; cero brechas elegibles como expertas.
- Foundations: 102 subtemas; 1.224 comprobaciones de capa (36 en progreso, 1.188 no evaluadas); 408 comprobaciones de capacidad (12 en progreso, 396 no evaluadas); 0 aprobadas; todos los subtemas T0/O0.
- AI Red Team: siete temas base, 84 celdas en progreso, 0 aprobadas; G5/G7 sin iniciar y G8 bloqueada.
- Seis reescrituras disciplinares importadas como borradores: identity, malware, forensics, incident_response, threat_intel y reverse. Otras 40 áreas tienen expansión específica pendiente.
- El bootstrap offline valida e indexa 334 documentos: 48 paquetes, 48 dossiers DEEP_SECTIONS, 48 estudios RESEARCH_STUDY, 48 compendios técnicos, 48 agendas, 48 revisiones bibliográficas, 43 documentos suplementarios y 3 Skills candidatas. Las candidatas no son Skills activas.
- FND-01.01, FND-01.02 y FND-01.03 tienen ampliaciones teóricas, instrumentos de evaluación en frío preparados y seis laboratorios sintéticos nuevos; ningún instrumento se ha administrado.
- Los laboratorios sintéticos incluyen conflictos safety/security, privacidad vs confidencialidad, recuperación confiable, causa común y autenticidad/integridad vs verdad. CI no equivale a prueba física u operacional.
- Los gates de estructura no son gates de aceptación experta. La madurez editorial M2 no equivale a T4/T5 ni a O4/O5.

## Siguiente orden obligatorio

1. Cerrar revisión de PR #17 y después PR #18, sin saltarse gates.
2. Foundations: cerrar sus 102 subtemas y no conformidades, uno por uno.
3. AI Red Team: currículo granular, evidencia, validación y revisión independiente.
4. Las otras 46 especialidades, en secuencia y con el mismo estándar.
5. Validación caliente y pruebas operativas reales después de completar la fase en frío.

## Historial anterior

El contenido histórico que sigue registra estados de 2026-11-18 y commits anteriores. Se conserva por trazabilidad, pero no reemplaza este estado canónico ni debe interpretarse como estado actual de `main`.

---

# Estado de integración — 2026-11-18

**Rama de integración:** `codex/integration-hash-locks-2026-11-17-v2`  
**PR existente:** [#11](https://github.com/Xero-29/CYBER_AI/pull/11), abierto en draft; no se creó un PR duplicado.  
**HEAD previo:** `ba4c8e61319a1f2320c0d0dcf9f72149aec594f2`. **main:** `9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea`.  
**Divergencia previa:** 39 commits propios y 477 commits de main desde el merge-base `c9c794c984b3fff5ff2032d0831f7f161205afc0`. Se detectó solapamiento en los dos workflows, README y PROJECT_STATUS. La nueva revisión conserva main como base del árbol e incorpora los cambios de integración; main no se modifica.

**Rama fuente de auditoría:** `codex/security-integrity-audit`, HEAD `3f83ed5bcf42f1ae3e1b1c38fc48a8a4c1f94781`; 35 commits adelante y 573 detrás de main desde el merge-base `cae816d6037b56f017c2fbdb3e98ef00df58c1d`. El commit histórico `7b5ed033f1f6461b5780a10ac4ada67a444b93e5` es ancestro común y está preservado.

## Cambios de integración

- Se conservan las capacidades recientes de main: sandbox YARA/TShark, contratos de ejecución, Nuclei, orquestación y biblioteca ampliada.
- Se mantienen locks SHA-256 para runtime, Ruff/Bandit y extractores documentales; CI verifica wheels, instala extractores y genera SBOM separados con provenance.
- Se portan del branch de auditoría los límites/Unicode en datasets, entorno host efímero para adaptadores, límites de manifiesto/archivos de backup y límite de 2 MiB para METADATA de wheels.
- El smoke de repositorio exige el entrypoint canónico `preflight.py` y `verify.sh`, no el antiguo `verifier.py` eliminado de main.

## Evidencia y validación

- main HEAD `9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea`: Python Tests **success, 605 pruebas** ([run 44198470095](https://github.com/Xero-29/CYBER_AI/actions/runs/44198470095)); Docker Sandbox **success, 605 pruebas y Ruff** ([run 44198470143](https://github.com/Xero-29/CYBER_AI/actions/runs/44198470143)).
- Rama de auditoría HEAD `3f83ed5bcf42f1ae3e1b1c38fc48a8a4c1f94781`: Python Tests **success, 481 pruebas** ([run 44327499508](https://github.com/Xero-29/CYBER_AI/actions/runs/44327499508)); Docker Sandbox **success** ([run 44327500029](https://github.com/Xero-29/CYBER_AI/actions/runs/44327500029)).
- PR #11 HEAD anterior falló en evento `pull_request` porque una prueba exigía `verifier.py`, eliminado en main. Se actualizó para comprobar `preflight.py` y `verify.sh`.
- El nuevo merge commit requiere checks de push y pull_request sobre el SHA exacto. No se extrapola CI de los padres.
- PR #11 permanece en draft; no se fusiona automáticamente.

---

# Estado canónico vigente — 2026-11-18

**Rama:** `main`  
**Último commit verificado en CI:** `9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea`.  
**CI Python:** [run 44198470095](https://github.com/Xero-29/CYBER_AI/actions/runs/44198470095) — **605 pruebas aprobadas**.  
**CI Docker sandbox:** [run 44198470143](https://github.com/Xero-29/CYBER_AI/actions/runs/44198470143) — **success, 605 pruebas y Ruff en sandbox**.  
**Plan de cierre:** [docs/PROJECT_COMPLETION_PLAN.md](docs/PROJECT_COMPLETION_PLAN.md).  
**Matriz vigente:** [docs/IMPLEMENTATION_MATRIX.md](docs/IMPLEMENTATION_MATRIX.md).  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17`, sin modificar.

## Estado real resumido

- El HEAD `9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea` pasó 605 pruebas en Python Tests y 605 en Docker Sandbox; los workflows exactos están enlazados en el encabezado de este estado. El resultado valida ese SHA, no cambios posteriores.
- Herramientas: 21 declaradas, 20 IDs `TOOL_SPECS`, 17 adaptadores host (16 local/offline y Nmap scoped), pip-audit bloqueado, YARA/TShark en Docker y Nuclei con runner separado. El catálogo no garantiza instalación.
- Conocimiento: 48 paquetes, perfiles, agendas y dossiers exploratorios; profundidad aún no validada. El preflight registró 138 fuentes de investigación, 0 revisadas y 276 verificaciones pendientes en el commit probado.
- Agentes y proveedores están implementados, pero falta evaluar calidad semántica, robustez y coste con proveedores reales.
- Memoria y Skillbook verifican evidencia local; faltan firmante externo, identidad y doble aprobación.
- Adaptadores host no tienen aislamiento general; Nmap no fuerza aislamiento egress del sistema operativo; Nuclei requiere DNS pinning y egress enforcement.
- No se han validado operacionalmente todos los binarios, modelos, escáneres, laboratorios, restauración DR ni cargas reales.
- Windows continúa aplazado.

**Interpretación:** CI verde demuestra que el código y los contratos probados pasan en ese entorno. No demuestra cobertura experta de los dominios, eficacia de hallazgos, aislamiento frente a cargas hostiles ni preparación para producción.

## Historial de cambios

El contenido histórico que sigue registra implementaciones y validaciones de commits anteriores. No debe leerse como estado del HEAD actual si no enlaza explícitamente un SHA y un workflow vigentes.

## Integración de dominios, herramientas y Skills

- Se añadió `domain_capability_matrix.py`: exige correspondencia exacta entre los 48 paquetes del manifiesto offline y sus 48 perfiles de enrutamiento.
- Cada perfil enlaza el paquete de conocimiento con las herramientas declaradas para esa especialidad. La matriz diferencia herramientas disponibles, adaptadores registrados, runners separados y herramientas solo catalogadas.
- `task_planner.py` añade dominios coincidentes, herramientas candidatas por dominio y Skills activas potencialmente relacionadas. La consulta de Skills usa `record_usage=False`; planificar no altera sus métricas de uso.
- `capability_inventory.py` informa la consistencia de los 48 perfiles y deja explícito que esto no acredita cobertura operativa.
- Nuevas pruebas: `tests/test_domain_capability_matrix.py` y ampliación de `tests/test_task_planner_fallback.py` y `tests/test_capability_inventory.py`. La matriz pasó la comprobación exacta 48/48 en CI; el workflow Docker ejecutó 510 pruebas con éxito en SHA `d560a11cc890a02a0388ebbb27c36044832f8d02`.
- **Límite:** la matriz conecta y enruta; no implementa adaptadores ausentes, no descarga conocimiento externo y no convierte automáticamente Skills candidatas en Skills verificadas.

## Cambio reciente: perfiles y herramientas personalizadas

- Se incorporó `config/tool_execution_profiles.json` con perfiles `standard`, `extended` y `restricted`; el perfil se selecciona con `--tool-profile` en `cyber_ai.py --team`, o con `CYBER_AI_TOOL_PROFILE`.
- Los perfiles configuran el máximo de herramientas, timeout, permiso de objetivos externos y activación de herramientas personalizadas. No pueden omitir confirmación ni allowlist HMAC.
- Se incorporó un registro declarativo de herramientas personalizadas. Se definen ejecutable, argumentos argv, palabras clave y timeout en el JSON; el planificador puede proponerlas y el runner las ejecuta sin shell.
- Cada herramienta personalizada exige hash SHA-256 firmado en la allowlist HMAC; su evidencia se valida y registra en el ledger como las herramientas nativas.
- Los objetivos externos requieren simultáneamente el perfil `extended` (o uno equivalente que los permita) y el flag `--allow-external-targets`.
- La ejecución arbitraria de shell continúa deshabilitada. El runner personalizado no impone aislamiento de red; la evidencia declara `network_access=not_enforced`.
- Documentación: `docs/TOOL_EXECUTION_PROFILES.md`. Pruebas nuevas: `tests/test_tool_execution_profiles.py`.




## Aislamiento y Nuclei (cambios en curso de validación)

- YARA y TShark ahora se delegan en `isolated_tool_runner.py`; ya no se intenta ejecutarlos directamente en el host.
- Se añadió `Dockerfile.analysis-sandbox` y `build-analysis-sandbox.sh` para construir una imagen local con YARA/TShark.
- El contenedor aplica `--network=none`, root filesystem de solo lectura, mounts de muestras/reglas de solo lectura, capacidades eliminadas, `no-new-privileges`, límites de CPU/memoria/PIDs y no monta el socket Docker.
- La imagen se valida por SHA-256 mediante la allowlist HMAC. El daemon Docker y el kernel siguen dentro de la base de confianza; esto no es una MicroVM.
- Nuclei dejó de usar dos rutas de plantillas codificadas. Ahora acepta un directorio de plantillas HTTP completo, severidades configurables, exclusión de plantillas no firmadas y etiquetas de alto impacto, límites de tasa/concurrencia y límite de tamaño de evidencia.
- La CLI Nuclei exige autorización y ledger, y permite IP públicas, privadas o loopback únicamente con un permiso exacto, vigente y local. Los nombres DNS siguen bloqueados hasta implementar DNS pinning.
- Nuclei sigue separado de la ejecución local: requiere `--scan`, confirmación e ID de autorización; el plan multiagente no puede iniciar escaneos de red.
- Documentación: `docs/NUCLEI_INTEGRATION.md` y `docs/TOOL_EXECUTION_PROFILES.md`.
- Pruebas añadidas/actualizadas: `tests/test_isolated_tool_runner.py` (incluye smoke real condicional en CI), `tests/test_nuclei_scanner.py`, `tests/test_execution_policy.py`, `tests/test_capability_inventory.py`, `tests/test_tool_adapters.py`.

## Auditoría estructural y funcional

- La limpieza anterior retiró seis prototipos/demos sin consumidores de producción: `audit_target.py`, `test_api.py`, `agent_benchmark.py`, `agent_core.py`, `tests/test_agent_core.py` y `verifier.py`.
- Se conservaron herramientas CLI y subsistemas independientes con finalidad concreta, aunque no sean imports directos del orquestador.
- La revisión detectó un fallo real de portabilidad: `knowledge_downloader.py` importaba `fcntl` incondicionalmente, por lo que el comando no podía arrancar en Windows. La corrección reutiliza el bloqueo POSIX/Windows de `knowledge_bootstrap.py` y la comprobación Windows se conserva como tarea aplazada y se ejecutará en una ronda posterior.
- Se detectó además que el downloader confiaba en el estado `downloaded` del manifiesto y omitía el recurso sin verificar el archivo. La corrección fuerza la comprobación SHA-256 y permite recuperar archivos ausentes o alterados; se añadió una prueba de regresión.
- No se eliminan los `pass` encontrados de forma automática: los observados pertenecen a limpieza de temporales o manejo de fallos secundarios, no a implementaciones vacías.
- Los resultados de CI se deben asociar al SHA exacto. El último CI Python confirmado corresponde al SHA anterior `cd5a3b1c84448c4365c773100414b919250e4a23` (run `44125948782`); no valida los cambios posteriores. El nuevo workflow Docker incluye pruebas adicionales y su resultado para este HEAD aún no está confirmado.

## Funciones mantenidas

- Entradas: `cyber_ai.py --ask`, `--team`, `--report`, `--batch`, `--scan`, `--self-test`.
- Orquestación/proveedores: agentes, DIRECTOR, planificador, equipo multiagente y adaptadores.
- Autorización y trazabilidad: allowlist HMAC, política de ejecución, validadores, evidencia y ledger.
- Conocimiento: catálogo, bootstrap offline, ingestión, índice, búsqueda híbrida, embeddings, procedencia y evaluación.
- Memoria y Skills: memoria de aprendizaje, gestor de memoria de modelos, Skillbook y regresión.
- Informes y vulnerabilidades: análisis, NVD, lotes, registro de duplicados y Nuclei.

## Límites que siguen abiertos

- La validación de evidencia comprueba integridad/estructura y alcance declarado; no demuestra por sí sola veracidad, explotabilidad ni exhaustividad.
- El aislamiento Docker cubre YARA y TShark; los adaptadores locales generales y herramientas personalizadas aún no tienen aislamiento de red/sistema obligatorio (`network_access=not_enforced`).
- Nuclei dispone de CLI operativa separada del planificador local; faltan pruebas E2E con Nuclei real y objetivos de laboratorio.
- El catálogo de herramientas no garantiza instalación, adaptación ni disponibilidad operativa.
- Custodia/rotación externa de claves, ACL Windows completas, aislamiento de parsers, KMS/HSM, RBAC/IdP/MFA, WORM/offsite, DR, MicroVM, proveedores IA reales, observabilidad, pruebas de carga y revisión independiente requieren infraestructura y validación externas.

**Conclusión:** la ejecución aislada de YARA/TShark y el flujo configurable de Nuclei están implementados en código. No están comprobados el CI de este SHA, el build real de la imagen, la allowlist de imagen en el entorno de despliegue ni la ejecución real de Nuclei. El aislamiento no cubre todos los adaptadores y la salida de red de Nuclei no está filtrada a nivel de firewall. Se requieren pruebas E2E autorizadas antes de declarar el repositorio listo para producción.


## Ampliación de biblioteca de conocimiento — 2026-11-17

- Se incorporó un currículo técnico versionado para las 48 áreas de conocimiento en `knowledge/curricula/domain_curriculum.json`.
- Cada área define temas especializados, niveles L0–L4, artefactos, laboratorio seguro, criterios de evaluación y política de referencias.
- Se añadió `knowledge_quality.py` para auditar consistencia y medir cobertura estructural base/profunda; se añadieron pruebas en `tests/test_knowledge_quality.py`.
- Se corrigió la detección de encabezados de la auditoría para aceptar espacios y texto adicional en títulos de sección.
- El currículo no se contabiliza como contenido experto ya validado. Los paquetes actuales requieren ampliación editorial por dominio, revisión técnica independiente y referencias con licencia/procedencia verificadas.
- CI disparado para el nuevo código; los resultados deben asociarse al SHA exacto antes de declarar las pruebas superadas.


## Módulos de profundización de la biblioteca — 2026-11-17

- Se crearon 48 módulos en `knowledge/deep_modules/<area>/README.md`, uno por cada ID del currículo y del manifiesto de conocimiento.
- Cada módulo contiene propósito/límites, competencias, expansión de temas técnicos, procedimiento operativo, laboratorio reproducible seguro, evaluación y requisitos de procedencia de fuentes.
- Índice: `knowledge/deep_modules/README.md`; guía editorial: `knowledge/curricula/README.md`.
- Se verificó mediante lecturas del repositorio la existencia de los 48 archivos.
- **Madurez real:** los 48 son borradores estructurados (`draft_structured_not_expert_validated`), no manuales expertos completos. Sus descripciones de trabajo por tema aún requieren desarrollo técnico específico, diagramas, referencias primarias verificadas, casos prácticos y revisión independiente.
- No se declaran fuentes externas verificadas ni laboratorios ejecutados por la mera creación de estos documentos.


## Investigación de biblioteca — ampliación 2026-11-17

- Se añadió `knowledge/research/RESEARCH_PROTOCOL.md`: método de investigación, revisión de literatura, formulación de hipótesis, diseño experimental, métricas, análisis de incertidumbre, amenazas a validez, reproducibilidad, ética y puertas M0–M5.
- Se añadió `knowledge/research/source_registry.json` con seis recursos oficiales NIST cuyos metadatos se revisaron. El estado es de metadatos oficiales revisados, no lectura integral ni validación de cada afirmación técnica.
- Se añadieron agendas de investigación específicas para los 48 dominios en `knowledge/deep_modules/<area>/RESEARCH_AGENDA.md`, con preguntas por tema, hipótesis provisionales, método, métricas, entregables y salvaguardas.
- El índice de la biblioteca enlaza las 48 agendas. Se añadió `knowledge_research_audit.py` y pruebas en `tests/test_knowledge_research_audit.py` para auditar estructura, no validez científica.
- **Madurez real:** 48/48 agendas de investigación creadas. Ninguna se declara M4/M5: aún faltan revisiones bibliográficas ejecutadas, lectura integral de fuentes, experimentos, resultados, análisis y reproducción independiente.
- Las agendas son planes de investigación específicos, no papers ni resultados. La auditoría no certifica calidad semántica, cumplimiento legal ni competencia de agentes.
- **Pruebas:** pendientes de ejecución CI para el SHA que incorpore estos cambios. No se declara CI verde hasta revisar el run y sus logs.


## Desarrollo de investigación y revisiones bibliográficas — actualización 2026-11-17

- Se ampliaron las revisiones bibliográficas iniciales de **7 a 13 de las 48 áreas**: AppSec/API, respuesta a incidentes, DevSecOps/supply chain, gestión de vulnerabilidades, OT/ICS, arquitectura segura, criptografía, identidad, inteligencia de amenazas, SOC/SIEM, forense digital, contenedores y malware.
- Cada revisión incorpora pregunta delimitada, síntesis de fuentes primarias, taxonomía/implicaciones técnicas, hipótesis falsables, diseño experimental propuesto, métricas, límites y brechas pendientes. Los experimentos **no se han ejecutado**.
- El registro creció de 6 a **33 fuentes**. Distingue páginas oficiales revisadas, metadatos/abstract revisados, documentos parcialmente inspeccionados, borradores y referencias de catálogo. No se contabilizan todas como lectura integral.
- Se inspeccionaron secciones concretas del PDF NIST SP 800-61 Rev. 3 (portada, resumen ejecutivo, ciclo de vida y fragmentos de contención); el resto de fuentes se limita al alcance de revisión declarado en cada registro. La lectura completa de estándares y documentos sigue pendiente.
- Los 13 dossiers enlazan IDs de fuente del registro. El auditor `knowledge_research_audit.py` ahora comprueba estructura, URLs HTTPS, unicidad y existencia de IDs referenciados, y separa revisiones bibliográficas de agendas.
- Se añadieron ocho pruebas `unittest` para la auditoría. `verify.sh` ejecuta ahora el auditor antes de la suite automatizada.
- **Cobertura documental de investigación:** 13/48 (27,1%). Las otras 35 áreas mantienen agenda de investigación, pero no revisión bibliográfica desarrollada.
- **Madurez real:** M1 documental en los 13 dossiers; no se declara M3/M4/M5. No existen resultados experimentales ni reproducción independiente en esta ampliación.
- **Pendiente:** completar revisiones de las 35 áreas, lectura integral y crítica de las fuentes, laboratorios seguros, resultados cuantitativos, análisis de incertidumbre, revisión por pares y reproducción externa.
- **CI:** los cambios disparan workflows por push. No declarar aprobado hasta comprobar el resultado de los runs asociados al SHA final de esta actualización.


## Validación CI de la ampliación de investigación — 2026-11-17

- SHA validado: `31726b15a8555f558bfcb739fb04b9e51d357908`.
- Python workflow `44140837562`: **success**. `verify.sh` completó preflight, compilación, self-test, procedencia, auditoría de investigación y suite de **522 pruebas**. Se generaron SBOM CycloneDX y metadatos de provenance, y se subieron como artefactos.
- Docker workflow `44140837454`: **success**. Construyó el sandbox general y la imagen de análisis YARA/TShark; ejecutó `verify.sh` con pruebas Docker habilitadas y Ruff dentro del sandbox endurecido; evidencia subida como artefacto.
- La auditoría de investigación confirmó 48/48 agendas estructuralmente completas, 13/48 revisiones bibliográficas trazables y 33 registros de fuentes. Las 35 revisiones faltantes siguen pendientes; la auditoría no convierte agendas ni revisiones documentales en investigación empírica.
- Estos resultados corresponden al SHA indicado. Este commit añade únicamente el registro documental de esos resultados.


## Ampliación de las 35 revisiones restantes — 2026-11-17

- Se añadieron 35 dossiers exploratorios: IA red team, seguridad IA, API, automoción, bug bounty/VDP, continuidad, cloud, forense cloud, datos, bases de datos, EDR/XDR, correo/DNS, fundamentos, fraude, gobierno, hardware, IoT, Linux, ML, matemáticas, móvil, redes, seguridad física, PKI/HSM, PQC, privacidad, Red Team, ingeniería inversa, satélites, ingeniería de software, 5G, threat hunting, investigación de vulnerabilidades, Windows/AD y wireless.
- Cada dossier contiene pregunta, síntesis preliminar, taxonomía, hipótesis, protocolo experimental, métricas, amenazas a la validez, brechas y trazabilidad de una referencia institucional.
- Se incorporaron 35 referencias nuevas con estado `official_reference_catalogued_not_content_reviewed`: localizadas en sitios de emisores, no leídas íntegramente.
- Cobertura editorial: **48/48 dossiers exploratorios** y 48/48 agendas. No significa 48 revisiones sistemáticas, 48 documentos leídos ni investigaciones empíricas completadas.
- Madurez: M1; no se declara M3/M4/M5. Los experimentos propuestos no se han ejecutado.
- Pendiente: lectura integral, revisión sistemática de literatura académica, síntesis de evidencia, laboratorios, análisis estadístico, revisión experta y reproducción independiente.
- Validación del contenido de los 35 dossiers y del auditor: Python workflow `44142729195` **success** y Docker sandbox workflow `44142729114` **success**, ambos sobre SHA `6b352c0e113a3b5c192473960985d0587b3a851c`. `verify.sh` reportó 48 áreas, 48 agendas completas, 48 revisiones trazables, 68 fuentes registradas, 25 páginas/documentos con estado de revisión verificable y **522 pruebas** aprobadas. Docker construyó ambas imágenes, ejecutó la verificación completa y Ruff dentro del sandbox endurecido.


## Auditoría global de cobertura — 2026-11-17

- Se añadió una matriz de contraste entre las **48 áreas** del manifiesto y **61 familias** de marcos, estándares, taxonomías, guías y especificaciones.
- Todas las 48 áreas tienen al menos una referencia asociada en la línea base. El cruce valida IDs y trazabilidad estructural, no profundidad.
- Los 48 dominios se mantienen como `not_assessed_by_this_crosswalk` en profundidad de contenido. No se declara cobertura total ni porcentaje global.
- Se registran 8 brechas transversales: regulación nacional/sectorial, literatura académica sistemática, catálogo vivo de herramientas, versiones/protocolos, experimentación, sistemas críticos, cobertura regional/español y vigilancia de cambios.
- Se añadió `knowledge_global_coverage_audit.py` y pruebas automatizadas. `verify.sh` incorpora el auditor.
- Fuentes y versiones deben leerse y fijarse antes de afirmar cumplimiento. El registro actual es una línea base de referencias catalogadas, no lectura integral.
- Informe: `knowledge/research/GLOBAL_COVERAGE_AUDIT.md`; matriz: `knowledge/research/global_coverage_matrix.json`.
- **Límite:** esta auditoría demuestra que el cruce de 48 áreas y 61 referencias es estructuralmente consistente; no demuestra que CYBER_AI abarque todo el conocimiento existente, que los módulos estén completos ni que herramientas/laboratorios funcionen.


## Matriz de cobertura y validación por especialidad — 2026-11-17

- Se amplió `knowledge/research/global_coverage_matrix.json` a esquema 1.1.0. La matriz ahora deriva requisitos de los 48 currículos y enumera **336 requisitos temáticos**, **432 artefactos** y **336 puertas de validación** (7 por especialidad).
- Cada requisito tiene estado explícito, referencias de evidencia, revisor y fecha. Los estados iniciales permanecen en `not_assessed`; no se ha marcado ninguna especialidad como validada.
- `knowledge_global_coverage_audit.py` ahora comprueba la correspondencia exacta manifiesto–currículo–matriz, la conservación de temas y artefactos, los estados permitidos y la evidencia mínima exigida para declarar algo validado.
- Se ampliaron las pruebas para comprobar la matriz de requisitos y evitar validaciones sin evidencia.
- **Alcance real:** se desarrolló la estructura de auditoría y aceptación, no se completó la investigación ni el contenido profundo de los 48 dominios. Los 61 grupos de referencia siguen siendo una selección curada, no un censo exhaustivo. No se calcula porcentaje total.
- **CI para SHA `3457879a930ef8df23691889e167a1b17d24dbee`:** Python run `44144894444` y Docker sandbox run `44144894391` quedaron disparados; su resultado debe consultarse en GitHub Actions. No se declaran aprobados mientras estén pendientes/en ejecución.


## Desarrollo de compendios técnicos de las 48 especialidades — 2026-11-17

- Se añadieron 48 archivos `knowledge/deep_modules/<area>/TECHNICAL_COMPENDIUM.md`, uno por cada especialidad.
- Cada cuaderno desarrolla los subtemas como unidades técnicas: fundamentos/modelo, amenazas y fallos, controles, validación, análisis crítico y entregables.
- Cada especialidad incluye un diseño de laboratorio con cuatro casos (baseline, fallo sintético, detección y mitigación/regresión), salvaguardas, métricas, preguntas de investigación y artefactos de aceptación.
- Se añadió el índice de los 48 compendios.
- **Límite:** son cuadernos técnicos y planes de trabajo, no libros exhaustivos ni revisiones sistemáticas completas. Los laboratorios están diseñados, no ejecutados; no se elevó la madurez de ninguna especialidad.


## Remediación ejecutable Foundations + AI Red Team — 2026-11-24 (seguimiento)

- Se abrió una rama de seguimiento basada exactamente en el HEAD de PR #21: `codex/foundations-ai-redteam-executable-labs-2026-11-24`. No modifica `main`, no integra PR #18 y no altera el worktree local anterior.
- AI Red Team: se añadió `knowledge/deep_modules/ai_red_team/lab_runner.py`, harness determinista sintético para ART-01…ART-09. Incluye aislamiento de tenant, integridad de corpus, allowlist/ownership/idempotencia de herramientas, canaries, validación de salida estructurada, límites de presupuesto y separación train/holdout. No ejecuta LLM ni pruebas contra infraestructura real.
- Foundations: se añadió `knowledge/deep_modules/foundations/labs/risk_engineering.py` (LAB-FND-14A) con cálculo EAL basal/residual, pérdida evitada, coste de equilibrio y sensibilidad. Las cifras son supuestos sintéticos, no datos observados.
- Se añadieron pruebas unitarias para ambos runners y guías de ejecución. CI run `45458382690` concluyó `success` en el SHA funcional `7de199e54a439d3d7807d8eb5b9337c0172ad49a`: 702 pruebas, 1 skipped, suite principal y suite con extractores documentales; jobs Python 3.11/3.12/3.13 y Windows allowlist smoke en success. El harness sigue limitado a simulación sintética, no a pruebas de modelo real.
- La madurez no cambia: no hay lectura integral acreditada de las fuentes, claims respaldados ni revisión independiente. Los resultados sintéticos no demuestran robustez de un LLM ni eficacia de controles productivos.


## Probes de modelo AI Red Team — 2026-11-24 (seguimiento)

- Se añadió `knowledge/deep_modules/ai_red_team/model_probe.py`: adaptador opt-in OpenAI-compatible para ejecutar probes de inyección directa/indirecta, extracción de canary sintético y conformidad JSON contra un modelo local o endpoint remoto autorizado.
- Por defecto, HTTP solo se permite en loopback. Endpoints remotos requieren HTTPS y `--allow-remote`; la clave se lee desde `CYBER_AI_MODEL_API_KEY`. No se exponen herramientas ni se envían datos reales.
- Se añadieron pruebas del cliente HTTP con servidor local simulado, incluyendo rechazo de redirecciones y query parameters en el endpoint. No ejecutan un modelo real; la ejecución Ollama/proveedor queda para la validación local del usuario.
- El adaptador mide cuatro casos a nivel de salida del modelo. No prueba retrieval real, aislamiento multi-tenant, ejecución de herramientas, memoria ni loops del agente.
- Se indexaron en `knowledge/packs/manifest.json` los runners de Foundations, el harness AI Red Team, el adaptador de probes y la guía de ejecución; una prueba de regresión comprueba que el bootstrap los incluye.
- CI run `45459225819` concluyó `success` en el SHA funcional `da5e8c096b36cf5e793856ce227dfa4d7b669176`: 709 pruebas, 1 skipped, suite principal y suite con extractores documentales; Python 3.11/3.12/3.13 y Windows allowlist smoke en success. Este registro de estado es un commit documental posterior y requiere su propia verificación CI antes de integrar.


# Auditoría y remediación adicional Foundations + AI Red Team — 2026-11-25

**Rama:** codex/foundations-ai-redteam-audit-remediation-2026-11-25  
**Base:** PR #22, HEAD f7ed69ea625142a679956767f7af9d91cb5b2348. Esta rama no modifica main, PR #21, PR #22 ni la rama comercial PR #23.

- Se creó docs/FOUNDATIONS_AI_REDTEAM_AUDIT_2026-11-25.md con hallazgos, no conformidades y criterios granulares de cierre.
- ART-04: la versión auditada solo comprobaba hash y etiqueta de firmante allowlisted. Se cambió la fixture para verificar digest SHA-256 y HMAC-SHA256 con clave sintética, incluyendo contenido alterado, firmante desconocido y firma falsificada. HMAC no es firma digital/PKI de producción.
- Model probes: el detector de canary ahora contempla literal, separadores, reverso, ROT13, Base64, hexadecimal y URL encoding. Las pruebas cubren las variantes. Es un detector finito; no garantiza detectar cifrado, paráfrasis, esteganografía o divulgaciones arbitrarias.
- La guía AI Red Team documenta los límites de assurance de ART-04.
- No se promueve T/O ni se aprueba ninguna especialidad. ART-01…09 siguen siendo controles sintéticos en memoria; cuatro probes solo evalúan salida del modelo. Falta integración real con RAG, tenant store, broker, memoria, cache y loop de agente.
- Foundations mantiene 102 subtemas en el mapa; el contenido FND-04 y LAB-FND-14A no cierra el currículo. LAB-FND-14A usa supuestos sintéticos de EAL y no calibra frecuencia, pérdida, eficacia o dependencias reales.
- Evidencia: no hay claims aprobados ni revisión independiente en la línea base examinada; lectura integral y licencias deben trazarse por claim y subtema.
- CI del HEAD de base PR #22 f7ed69e no se considera verde completo: el registro más reciente consultado contiene unit-tests cancelado, aunque reproducibilidad Python 3.11/3.12/3.13 y Windows allowlist smoke concluyeron success. La rama nueva requiere CI completo en su HEAD exacto.

## Próximos gates obligatorios

1. CI completo en el HEAD final de esta rama y regresiones específicas ART-04/canary.
2. Ejecutar el probe con modelo local y preservar PASS/FAIL/INCONCLUSIVE sin filtrar resultados.
3. Integrar ART-03/05/08 con retrieval, autorización y broker reales en sandbox aislado.
4. Cerrar los 102 subtemas Foundations con evidencia y revisión por capa/capacidad.
5. Completar AI Red Team end-to-end y revisión independiente.
6. Aplicar la misma metodología a las otras 46 especialidades.
7. Solo después pasar a pruebas calientes del sistema completo.


## Remediación ART-09 benchmark — 2026-11-25

- Rama: `codex/foundations-ai-redteam-benchmark-remediation-2026-11-25`, apilada sobre PR #24; no modifica `main` ni integra PR #21–#24.
- El harness ART-09 ahora valida esquema, IDs únicos, separación de splits, duplicados normalizados, near-duplicates heurísticos, separación de grupos de origen y denominadores por clase.
- Se incorpora manifiesto sintético versionado y SHA-256 canónico. La licencia no se presume: queda pendiente de revisión explícita.
- Se añaden regresiones para duplicados dentro de un split, IDs repetidos y fuga de grupos de origen.
- Límite: el fixture sigue siendo pequeño y sintético. Ground truth independiente, tamaño/potencia estadística, representatividad y validez externa no están demostrados. ART-09 PASS solo valida los controles estructurales implementados.
- **CI pendiente de comprobar en el HEAD final de esta rama.** No declarar esta remediación aprobada hasta revisar todos los jobs y resultados exactos.


## Remediación LAB-FND-14A — 2026-11-25

- Rama: `codex/foundations-risk-uncertainty-remediation-2026-11-25`, apilada sobre PR #25. No modifica `main` ni integra PR #21–#25.
- El cálculo EAL ahora rechaza entradas booleanas, no numéricas, NaN, infinitas y negativas.
- Se añade una cuadrícula factorial determinista de 27 escenarios para frecuencia basal, pérdida basal y frecuencia residual relativa; pruebas verifican tamaño, método y caso base.
- Documentación distingue explícitamente sensibilidad de escenarios de Monte Carlo, distribuciones, intervalos de confianza y análisis de dependencia.
- Límites: supuestos sintéticos, sin calibración empírica, colas, correlaciones ni eficacia observada; no cierra NC-FND-01/02/03 ni eleva T/O.
- **CI pendiente de comprobar en el HEAD final de esta rama.**


## Laboratorio autónomo de adquisición de skills — 2026-11-26

- Rama experimental apilada sobre el HEAD de PR #27: `codex/autonomous-skill-lab-2026-11-26`. No modifica `main` ni fusiona PRs anteriores.
- Se añade un ciclo local Planner 9B → Executor pequeño → sandbox Rust → evidencia → revisión limitada del Planner. Modelos configurables por variables de entorno.
- El agente pequeño genera un proyecto Rust y documenta el procedimiento; no puede emitir comandos de shell. Solo se aceptan `Cargo.toml`, `src/main.rs` y `src/lib.rs`; se bloquean dependencias y build scripts.
- Se añade una imagen Docker específica con Rust. El contenedor ejecuta `cargo test --offline`, sin red, con root filesystem read-only, usuario no privilegiado, capacidades eliminadas y límites de CPU/memoria/procesos. El workspace es temporal.
- Se limita la iteración a tres rondas. Los resultados se clasifican como passed/failed/inconclusive; se genera un candidato de skill, nunca una promoción automática.
- Se añaden pruebas unitarias de allowlist, aislamiento, JSON, URL loopback y ciclo de reintento. La suite completa y el build Docker quedan pendientes de CI en el HEAD exacto y de ejecución caliente del usuario.
- Límite crítico: el modelo no reentrena sus pesos; el aprendizaje implementado es procedimental. Los tests generados por el propio agente no constituyen un oráculo independiente. La promoción al Skillbook requiere revisión externa y repetición independiente.
- La imagen instala Rust desde repositorios Debian Bookworm sin fijar versión exacta de paquetes; se debe fijar la cadena de suministro antes de producción.
