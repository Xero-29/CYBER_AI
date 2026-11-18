# Estado de reconciliación — 2026-11-18

**Rama de integración:** `codex/reconcile-security-integrity-2026-11-18`  
**HEAD verificado antes de esta actualización:** `f86279386dc7c55ec23161accaf063f346e48bf5`.  
**Base:** `main` en `9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea`; comparación: **115 commits adelante, 0 detrás**, 48 rutas cambiadas.  
**Merge-base con main:** `9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea`. Main permanece intacta.  
**Merge controlado en esta rama:** `2585b99be752bef3276ce5721690542c9f05e7d2`, con segundo padre PR #11 en `04c001a206cde98613cf9c151ce4f6a95fb86a21`. Se conservó el árbol validado de PR #11 y se sobrepusieron rutas revisadas; no hubo merge en main ni rebase/force-push.

**Rama fuente de auditoría:** `codex/security-integrity-audit`, HEAD inspeccionado `8104739d542e3264166eb0e7b1b493aa26e9ce0a`. Sigue divergente de main: 112 commits exclusivos de auditoría y 573 exclusivos de main desde `cae816d6037b56f017c2fbdb3e98ef00df58c1d`. Los cambios se portan por funcionalidad, no copiando el diff completo.

## Cambios integrados y endurecimiento portado

- Locks/SBOM de PR #11, manifiestos separados por entorno y soporte `--lock-file`.
- Manifiesto de wheels: hashes contrastados con el lock, límites de tamaño/cantidad/entradas, rechazo de symlinks y validación estricta de METADATA.
- Generador de locks: validación de wheelhouse y requisitos, límites y publicación atómica.
- `safe_io.atomic_write_text` integrado en locks, manifiestos de artefactos, SBOM, manifiestos de descargas y reportes de evaluación de conocimiento.
- Ledger: protección de ruta y archivos DB/WAL/SHM, directorio POSIX privado, archivos `0600`, límites SQLite signed 64-bit y umbrales de recuperación representables.
- Backups: límites de cantidad de archivos y tamaño del manifiesto, comprobados antes y después de leer.
- Evaluación de conocimiento: lectura protegida contra symlinks, identidad estable, límites de bytes y Unicode; escritura atómica de informes y códigos de salida CLI comprobables.
- Allowlist HMAC: lectura resistente a reemplazo de ruta, validación de firma/configuración en preflight y pruebas de denegación antes de iniciar procesos.
- Los adaptadores convierten denegaciones de allowlist en errores de ejecución tipados; preflight informa política de allowlist y ledger sin exponer secretos.
- Agentes, ejecutor de herramientas y task runner exigen ledger por defecto; el modo sin registro requiere excepción explícita.
- Runner Docker: montaje de evidencias `0700`; workflow instala con `pip --require-hashes` y protege el directorio de datos.
- Pruebas de regresión para las correcciones anteriores; documentación de allowlist y preflight actualizada.

## Evidencia de CI

**HEAD `f86279386dc7c55ec23161accaf063f346e48bf5`:**
- Python Tests — **success**, 675 pruebas, 2 omitidas en cada ejecución (base y extractores documentales); Windows allowlist smoke — **success**: [run 44365409653](https://github.com/Xero-29/CYBER_AI/actions/runs/44365409653).
- Docker Sandbox — **success**, verificación completa, smoke Ruff y evidencia publicada: [run 44365409654](https://github.com/Xero-29/CYBER_AI/actions/runs/44365409654).

**PR #11:** sigue abierto en draft, sin duplicarlo: [PR #11](https://github.com/Xero-29/CYBER_AI/pull/11). Su HEAD `04c001a206cde98613cf9c151ce4f6a95fb86a21` pasó Python Tests ([run 44359934767](https://github.com/Xero-29/CYBER_AI/actions/runs/44359934767)) y Docker Sandbox ([run 44359934228](https://github.com/Xero-29/CYBER_AI/actions/runs/44359934228)).

**PR #2:** cerrado y fusionado en `478c6ddc676221e4c07b8c5780f127bc5a9e749e`; no se duplicó.

## Próximas tareas de reconciliación

1. Revisar los cambios restantes de la rama de auditoría por archivo y conservar las capacidades nuevas de main (agentes, simulación, atlas, currículos, módulos de conocimiento y runners).
2. Revisar contratos de adaptadores/proveedores, integridad de evidencias y documentación cruzada para detectar componentes desconectados.
3. Repetir Python, Docker, SBOM y locks sobre el HEAD final después de la siguiente actualización documental.
4. No abrir un PR solapado mientras PR #11 siga cubriendo locks/SBOM.
5. Mantener como pendientes externos KMS/HSM, WORM/offsite, RBAC/IdP/MFA, simulacros restore/DR, microVM/egress/escape, proveedores reales y revisión experta de fuentes.

**Estado:** Python y Docker están verdes en el HEAD indicado. La reconciliación técnica continúa; esto no es autorización de integración ni declaración de preparación de producción.


---

# Estado canónico vigente — 2026-11-17

**Rama:** `main`  
**Último commit verificado en CI:** `0767cd68d418f7bfbb69bbe336106a9e869de563` (plan maestro).  
**CI Python:** [run 44181807943](https://github.com/Xero-29/CYBER_AI/actions/runs/44181807943) — **594 pruebas aprobadas, 1 omitida**.  
**CI Docker sandbox:** [run 44181807961](https://github.com/Xero-29/CYBER_AI/actions/runs/44181807961) — **success**.  
**Plan de cierre:** [docs/PROJECT_COMPLETION_PLAN.md](docs/PROJECT_COMPLETION_PLAN.md).  
**Matriz vigente:** [docs/IMPLEMENTATION_MATRIX.md](docs/IMPLEMENTATION_MATRIX.md).  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17`, sin modificar.

## Estado real resumido

- El último cambio funcional de memoria, Skills y adaptadores sigue siendo `6fa5da29c23f2d39c79ea93adb3a1fbb1018a0bf`; el commit `0767cd68` añadió el plan maestro. La suite Python del commit del plan ejecutó 594 pruebas, con 1 omitida; Docker sandbox terminó correctamente.
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
