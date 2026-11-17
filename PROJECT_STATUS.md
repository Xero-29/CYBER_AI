# Estado canónico vigente — 2026-11-17

> Esta sección describe el HEAD auditado; los bloques históricos inferiores son contexto.

**Rama:** `main`  
**Último cambio funcional de integración:** `d560a11cc890a02a0388ebbb27c36044832f8d02` (matriz de dominios, planificación y pruebas de regresión). Docker sandbox CI: aprobado en run `44130731532`, con 510 pruebas, build del sandbox YARA/TShark y smoke Ruff aprobados sobre este SHA. El workflow Python independiente `44130731618` fue cancelado por commits posteriores mientras esperaba runner; no aporta un resultado de pruebas. Las pruebas Windows siguen aplazadas.  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17`, sin modificar.

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
