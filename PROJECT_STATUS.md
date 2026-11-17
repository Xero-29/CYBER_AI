# Estado actual verificado — 2026-11-17

**HEAD verificado:** `6fd37146aa249aef11aee40fb56d0d578352d4f2`  
**Rama:** `codex/security-integrity-audit`  
**Comparación con main:** 350 commits adelante, 0 detrás (según el PR abierto).  
**CI de este HEAD:** Python tests — [success, 377 pruebas](https://github.com/Xero-29/CYBER_AI/actions/runs/43997173079); Docker sandbox — [success](https://github.com/Xero-29/CYBER_AI/actions/runs/43997173115).  
**PR #2:** abierto, en borrador; no fusionado. `main` no fue modificado.

## Cambio de seguridad de esta iteración

- `knowledge_audit.py` ahora rechaza rutas absolutas, traversal y symlinks en el manifiesto; no sigue directorios raíz symlink durante el inventario.
- Los manifiestos ausentes o inválidos producen diagnósticos en vez de interrumpir abruptamente la auditoría.
- La auditoría SQLite abre la base en modo solo lectura y devuelve un diagnóstico si el esquema no es válido.
- `tests/test_knowledge_audit.py` añade cobertura para rutas externas, symlinks de archivo/directorio, manifiestos inválidos y lectura SQLite.
- Validación de este cambio: 377 pruebas Python y Docker sandbox aprobados en el SHA exacto indicado arriba.

**Límite:** esto cierra una brecha del auditor local; no cierra las brechas institucionales de KMS/HSM, cifrado, WORM, RBAC, microVM, proveedores reales, evaluación experta de fuentes ni recuperación ante pérdida de host. Las secciones históricas siguientes documentan iteraciones anteriores; si contradicen este bloque, prevalece la evidencia del HEAD aquí indicado.

---

# Estado real y plan de cierre de CYBER_AI

**Actualizado:** 2026-11-17  
**Rama:** codex/security-integrity-audit
**CI:** Actions fijadas por SHA, checkout v5/setup-python v6/upload-artifact v5 (Node 24)  
**Base:** main (sin merge ni despliegue)

## Avance de esta iteración

## Recuperación transaccional del ledger — 2026-11-17

- `execution_ledger.py`: se incorpora el estado terminal `interrupted` y una reconciliación atómica de inicios sin evento terminal correlacionado por `metadata.start_event_id`.
- La reconciliación verifica la cadena hash completa dentro de la transacción antes de escribir. Si hay secuencias, enlaces o hashes inválidos, aborta sin añadir eventos.
- Los eventos recuperados declaran `outcome: unknown`; no se atribuye éxito ni fallo al trabajo que pudo quedar ejecutándose. Los IDs deterministas y la transacción evitan cierres duplicados o carreras entre reconciliadores.
- CLI: `python ledger_cli.py reconcile --confirm-no-active-runs` (opcional `--namespace NOMBRE` y `--older-than-seconds 300`). Exige confirmación de que los trabajadores están detenidos y omite inicios recientes por defecto; no se ejecuta automáticamente al iniciar el sistema.
- Pruebas añadidas: recuperación idempotente, no duplicación cuando ya existe terminal, migración de esquema antiguo y rechazo de reconciliación sobre cadena corrupta.
- **Límite:** solo se reconcilian inicios con `start_event_id` correlacionable y más antiguos que el umbral configurado. La CLI exige confirmar que no hay ejecuciones activas. Esto registra el estado desconocido en el ledger; no recupera procesos del sistema operativo, resultados perdidos ni datos de almacenamiento físicamente dañado.
- **CI del código:** Python tests — [success](https://github.com/Xero-29/CYBER_AI/actions/runs/43996430032) y Docker sandbox — [success](https://github.com/Xero-29/CYBER_AI/actions/runs/43996436845), ambos en `2fe9ede3d5d2c49bbc45551ee9d0325893bc6b25`. La actualización documental posterior vuelve a disparar CI y debe validarse por separado.


## Corrección de trazabilidad de ejecuciones (16-11-2026)

- `tool_executor.py`: el evento terminal se intenta escribir en `finally` cuando existe evento inicial; captura excepciones inesperadas y clasifica el resultado como fallido/denegado/timeout/completado. Con `--require-ledger`, un fallo al persistir el resultado devuelve código no cero.
- `task_runner.py`: las excepciones inesperadas posteriores al inicio generan un resultado fallido y se intenta cerrar el evento en el ledger.
- `agent_runner.py`: un guard externo a la implementación detecta un evento inicial sin terminal asociado y añade un evento fallido ante excepciones no controladas, evitando duplicar cierres ya registrados.
- Se añadieron pruebas unitarias para las rutas de excepción, denegación, fallo de ledger y prevención de cierres duplicados.
- **Estado de validación:** cambios publicados en la rama de auditoría; no se declara CI aprobado hasta disponer de resultados de GitHub Actions para el HEAD actual. Esta corrección no resuelve por sí sola el anclaje externo WORM/KMS ni la identidad criptográfica del aprobador.

El ledger incorpora eventos `started` y terminales, con migración transaccional de bases existentes que conserva eventos y hashes. `tool_executor.py`, `task_runner.py` y `agent_runner.py` enlazan inicio/resultado y cierran excepciones capturables; admiten fail-closed mediante `--require-ledger` o `CYBER_AI_LEDGER_REQUIRED=1`. `nuclei_scanner.scan_target` admite `require_ledger=True`; `team_orchestrator.py` exige registrar inicio y resultado. Tras dos ejecuciones supervisadas correctas de la misma tarea, `team_orchestrator.py` propone automáticamente una Skill candidata basada en las etapas del flujo y los IDs del ledger. Las propuestas ignoran eventos `started`; la candidata no es ejecutable hasta revisión/firma VERITAS externa. Un apagado abrupto, pérdida del almacenamiento o fallo del propio ledger todavía puede impedir el cierre; el hash-chain local no sustituye un anclaje WORM externo.

`knowledge_eval.py` mide Recall@K, Precision@K y MRR@K con un benchmark por defecto de 48 consultas sintéticas (una por especialidad) y un smoke test reducido de 12. La biblioteca incorpora recuperación híbrida FTS5 + vectores con Reciprocal Rank Fusion (RRF), filtro de namespace/tenant y reconstrucción verificable del índice textual. Si SQLite no tiene FTS5, se conserva la recuperación semántica. La calidad aún debe medirse con embeddings reales y conjuntos revisados por expertos; faltan umbrales por dominio y evaluaciones validadas por especialistas.

La integración de proveedores ahora exige declarar capacidades reales para plugins; valida chat/embeddings/model_listing, selecciona proveedores por capacidad y permite fallbacks configurados cuando un proveedor no tiene la capacidad solicitada. Se añadieron endpoints por defecto seguros para proveedores nativos. El fallback de configuración no cubre fallos de red, cuotas o errores durante una petición.

Se reforzó el bootstrap de la biblioteca offline: IDs deterministas por ruta y SHA-256, bloqueo entre procesos, rechazo de rutas absolutas/traversal/symlinks, estados `processing/completed/failed`, reanudación tras fallos y prevención de duplicados. La indexación identifica el espacio vectorial del proveedor ECO y reindexa el contenido cuando cambia el modelo/proveedor, evitando mezclar vectores incompatibles en las búsquedas. Se añadieron pruebas de reintento, rutas, fallos y espacios de embeddings.

El descargador ahora exige `CYBER_AI_KNOWLEDGE_EGRESS_PROXY` para cualquier descarga real; sin gateway configurado falla antes de resolver el destino o abrir conexiones. El gateway debe imponer allowlist de hosts, pinning DNS y bloqueo de redes privadas. Esto no sustituye la validación de seguridad del proxy externo.

Se amplió `tool_adapters.py` con comandos locales acotados para Checkov, detect-secrets, Hadolint, ShellCheck, actionlint, kube-linter, YARA (requiere reglas locales) y TShark (solo PCAP/PCAPNG). El inventario distingue herramientas catalogadas, adaptadores registrados y binarios realmente disponibles. La presencia de un adaptador no implica que el binario esté instalado; las herramientas activas de red siguen fuera de esta ejecución local.

Se incorpora execution_ledger.py: registro SQLite transaccional append-only de ejecuciones con namespace, huella de tarea, estado, herramienta/versión, modelo, entorno, duración, coste opcional, resultados de validadores y hash SHA-256 de evidencia. Incluye cadena hash verificable, redacción de campos con nombres sensibles y bloqueo ordinario de UPDATE/DELETE. Se añaden pruebas específicas.

Límite: es evidencia tamper-evident, no almacenamiento WORM ni prueba criptográfica de identidad. Existe `ledger_checkpoint.py` para anclajes HMAC; falta desplegar la clave y almacenar checkpoints en un sistema independiente (KMS/HSM/WORM), además de pruebas operativas de restauración. La captura de inicio/resultado y el cierre de excepciones capturables están implementados en los ejecutores principales descritos arriba; los fallos abruptos del proceso o del almacenamiento aún pueden dejar eventos `started` abiertos. El modo fail-closed es opt-in en tool_executor, task_runner, nuclei_scanner y agent_runner; team_orchestrator lo exige en su ruta normal. No existe una política global obligatoria para todo el sistema. La propuesta automática de Skills ya se activa tras dos flujos supervisados correctos y revisión independiente; la activación sigue bloqueada hasta firma VERITAS externa. La promoción automática, KMS/HSM, regresión y obsolescencia siguen pendientes.

## Validación más reciente

- Commit `c2b7d65ed4b4a2510bd3065d1b6f102a38b5f5e7`: GitHub Actions Python tests **success**, 336 pruebas; Docker sandbox **success**.
- Commit `53b04787ca0b84865e81ad70ea9256cdca30adc5`: Python tests **success** y Docker sandbox **success**.
- Commit `05986653249dcdb77df39082fffeadb5657e75df`: Python tests **success** y Docker sandbox **success**.
- La validación CI no equivale a pruebas con Ollama/proveedores remotos, objetivos reales autorizados, cargas adversariales ni aislamiento microVM.

## Capacidades existentes (no equivalen a cierre institucional)

- Inventario de 21 herramientas, selección explicable y 14 especificaciones de adaptador; 11 tienen ejecución local acotada; YARA y TShark requieren aislamiento aún no disponible y pip-audit permanece bloqueado por red. El inventario expone `execution_ready` y `requires_isolation` para no confundir adaptador con permiso de ejecución. El inventario separa registro, disponibilidad del binario y cobertura de adaptador.
- Sandbox Docker endurecido con timeout del cliente y limpieza forzada del contenedor ante timeout; comparte kernel y no es aislamiento para malware hostil.
- Atlas de 48 áreas y 138 referencias externas catalogadas; además, 48 paquetes metodológicos propios incluidos offline. Las referencias externas no están descargadas ni ingeridas.
- Biblioteca SQLite con fragmentos comprimidos, SHA-256, metadatos, separación shared/tenant y búsqueda semántica.
- Ingestión transaccional (publicación de todos los fragmentos en una única transacción), límite de 2 MiB por fragmento y descompresión acotada de TXT/Markdown, HTML, CSV, JSON/JSONL y código; extractores opcionales PDF/DOCX/XLSX/PPTX con límites de tamaño, expansión ZIP y extracción incremental acotada para evitar acumulación descontrolada de texto. OCR de PDF escaneado y ejecución aislada de extractores siguen pendientes. Catálogo, descubrimiento y downloader con manifiesto serializado por lock; dry-run sin DNS ni escrituras. La descarga ahora falla cerrada antes de resolver DNS si no hay proxy de salida explícito; la garantía contra DNS rebinding depende de que el gateway configurado implemente allowlist, pinning DNS y bloqueo de redes privadas.
- Reindexación con staging, backup y publicación transaccional.
- Proveedores Ollama, OpenAI-compatible, Anthropic chat y Gemini chat/embeddings, con extensiones instalables mediante entry points `cyber_ai.providers`; HTTP solo en loopback, HTTPS remoto y redirecciones bloqueadas para proteger credenciales.
- Skillbook con propuestas automáticas de candidatas tras dos ejecuciones supervisadas independientes, activación solo con firma HMAC VERITAS, versiones inmutables y exclusión de candidatas de la búsqueda ejecutable. La clave sigue siendo un secreto operativo externo, no una identidad de modelo.
- Memoria de lecciones con HMAC VERITAS vinculado a dos ejecuciones con revisiones objetivas de un agente revisor distinto y hashes del ledger, validación de firma al leer, aislamiento por namespace, lock y permisos 0600. El registro directo se bloquea; las lecciones v1 sin firma se ignoran. HMAC no autentica por sí solo la identidad del modelo.
- Dependencias base fijadas en `requirements.lock` para instalaciones repetibles (sin hashes de artefactos; la verificación de procedencia/hash queda pendiente).
- `preflight.py` para revisar dependencias, configuración, herramientas opcionales y ledger local sin iniciar servicios ni usar red.
- `sbom_generator.py` genera SBOM CycloneDX 1.5 determinista desde los requirements fijados, separa dependencias directas/transitivas y registra el hash del lock. No inventa hashes de artefactos ni relaciones transitivas no declaradas.
- `ledger_checkpoint.py` firma/verifica con HMAC la cabeza de la cadena del ledger; sirve para anclar checkpoints fuera del host. Requiere clave externa y almacenamiento separado; no es WORM.
- `data_backup.py` crea snapshots SQLite consistentes, copia archivos con confirmación de procesos detenidos, verifica SHA-256 y restaura conservando el directorio anterior. No cifra ni firma el backup.
- `docs/THREAT_MODEL.md` contiene el baseline STRIDE, límites de confianza, amenazas y pruebas de aceptación para revisión independiente.
- CLI `ledger_cli.py` para verificar integridad, listar namespaces y consultar historial.
- Ledger de ejecuciones: registra respuestas, ejecuciones locales, timeouts, denegaciones y revisiones objetivas independientes. Los eventos `started` y terminales se enlazan en `tool_executor.py`, `task_runner.py`, `nuclei_scanner.py`, `agent_runner.py` y `team_orchestrator.py`. Los dos primeros admiten `--require-ledger`; Nuclei admite `require_ledger=True`; agent_runner usa `CYBER_AI_LEDGER_REQUIRED=1`; team_orchestrator falla si no registra inicio o resultado. La base existente se migra al esquema nuevo conservando filas y hashes. `ledger_checkpoint.py` crea/verifica anclajes HMAC de la cabeza del ledger para guardarlos fuera del host; la clave debe permanecer en gestor externo y el almacenamiento WORM/identidad independiente siguen pendientes. El cierre ante apagados abruptos o fallos del ledger no está garantizado; el ciclo de aprobación y regresión de Skills aún requiere infraestructura externa.

## Avance de biblioteca offline

- Catálogo ampliado a 48 especialidades.
- 48 paquetes propios en español incluidos en `knowledge/packs/`; 48 ampliados con guías de dominio, metodología, controles, laboratorio y criterios de evaluación. No equivalen a corpus experto exhaustivo ni a documentación oficial de fabricantes.
- Las referencias externas siguen pendientes de licencia/procedencia y no se declaran descargadas ni ingeridas.

- `knowledge_bootstrap.py` valida e indexa paquetes offline con ECO. El dry-run no requiere IA. La ingestión real requiere un proveedor con embeddings configurado. El proceso es reanudable, idempotente y detecta cambios de espacio vectorial para reindexar. No se inicia automáticamente por conectar un chat.

## Pendientes de cierre

1. **Ejecución y aprendizaje:** probar en CI el cierre de excepciones en los ejecutores; cubrir apagados abruptos y fallos de almacenamiento con recuperación/reconciliación; almacenar artefactos en repositorio controlado; desplegar checkpoints firmados externamente (CLI HMAC implementada; falta clave/almacenamiento independiente); costes reales por proveedor; retención y privacidad.
2. **Skills verificadas:** provisionar firma desde KMS/HSM o servicio independiente; cerrar el circuito de aprobación independiente, pruebas de regresión automáticas por versión, rollback probado y detección de obsolescencia.
3. **Biblioteca documental:** validar extractores PDF/Office en fixtures adversariales y sandbox; OCR cuando aplique; deduplicación/versionado; evaluación de recuperación con embeddings reales y especialistas; ANN/performance a escala; citas por fragmento; revisión de licencias/procedencia.
4. **Herramientas:** completar adaptadores según utilidad y riesgo, fijar versiones e imágenes por digest, añadir hashes verificables de artefactos y procedencia completa; existe SBOM CycloneDX inicial basado en el lock, pero no sustituye hashes ni attestation. No habilitar herramientas de red sin política explícita; el downloader aún requiere mitigación externa del riesgo DNS rebinding.
5. **Sandbox:** Docker solo para código confiable/acotado; microVM/VM desechable requiere infraestructura externa y pruebas de aislamiento; gestión de secretos y permisos.
6. **IA:** contrato de capacidades común, embeddings equivalentes, detección de capacidades, selección/fallback de modelos, pruebas de compatibilidad y gestión segura de credenciales.
7. **Operación institucional:** existe baseline STRIDE en `docs/THREAT_MODEL.md`, pero requiere revisión independiente contra el despliegue; faltan RBAC, auditoría inmutable externa, cifrado de backups, almacenamiento externo/WORM y restauración operacional probada (existe backup local con hashes, no cifrado), retención, redacción, migraciones, concurrencia, observabilidad y pruebas de carga.

## Criterio de cierre

No declarar el sistema completo ni certificado hasta que cada brecha tenga código, pruebas automatizadas, evidencia reproducible y validación operacional. No descargar indiscriminadamente el atlas, no ejecutar herramientas de red por defecto y no promover Skills por respuestas plausibles.

## Revisión de integración adicional (16-11-2026)

- Comparación directa con `main`: rama de auditoría **298 commits ahead / 1 behind**; estado GitHub `diverged`.
- El único commit exclusivo de `main` es `7b5ed033f1f6461b5780a10ac4ada67a444b93e5` (`fix: repair sandbox policy tests`), que modifica `tests/test_sandbox_runner.py`.
- La versión de ese test en la rama de auditoría ya contiene las comprobaciones de ese commit y añade regresiones para el ledger obligatorio, allowlist de herramientas de sandbox, timeout del proceso Docker, imagen fijada por digest y validación de rutas de evidencia. Por tanto, no se debe reemplazar la versión de la rama por el archivo más antiguo de `main`.
- La divergencia se mantiene explícita; no se ha hecho merge ni force-push. Antes de integrar, revisar el grafo completo y confirmar que no existen otros efectos del commit exclusivo fuera del archivo comparado.
- Revisión del flujo de excepciones: la firma de `_run_agent_impl` coloca `task_id` en el quinto argumento posicional; el wrapper lo propaga en esa posición o como keyword, y la correlación se realiza por `metadata.task_id`, no por el prompt redactado.
- **CI de la rama durante esta revisión: no verificado** (las consultas de ejecuciones asociadas a PR y estados combinados devolvieron listas vacías para los commits consultados). Los resultados CI históricos indicados arriba no deben interpretarse como validación del HEAD actual.

## Verificación de cierre — 2026-11-16 (actualización)

- Se verificó que el commit `d325796f2732a5a6fb7bb34d39f8b7a2cb494e0c` existe en GitHub y añade pruebas para validar la duración reportada por adaptadores y el fallback monotónico.
- Se inspeccionó `tool_executor.py`: `_duration_ms` acepta únicamente números finitos no booleanos y no negativos; ante evidencia inválida usa el reloj monotónico local.
- **CI de ese commit: no verificado.** Las consultas de ejecuciones asociadas al commit y de estados combinados no devolvieron ejecuciones ni estados. Esto no demuestra éxito ni fallo; no se debe marcar como verde.
- La rama sigue divergida respecto de `main`: 301 commits por delante y 1 por detrás según la comparación consultada. No se hizo merge ni force-push.
- La ejecución de la suite completa, Docker, proveedores externos, restauración y pruebas de aislamiento deben confirmarse mediante ejecuciones reproducibles. Los resultados históricos no sustituyen la validación del HEAD actual.
- No se declara cierre institucional: permanecen las dependencias de infraestructura y validación externa enumeradas en este documento.


## Cierre incremental y evidencia CI — 2026-11-16

- HEAD de esta validación: `9e08af07c88b34aacf21ac43ca3dfc265022d53d` (`test: cover restore destination safety and missing parents`).
- GitHub Actions para ese SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43921744002). Instalación, validación de sintaxis y paso `Run complete local verification` completados correctamente.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43921743898). Construcción de imagen, verificación completa, Ruff dentro del sandbox y carga de evidencia completados correctamente.
- `data_backup.py`: el manifiesto ahora exige esquema y metadatos coherentes, entradas con tipo/tamaño/SHA-256 válidos, rutas POSIX canónicas, tipos de archivo permitidos y coincidencia exacta entre archivos declarados y existentes. Rechaza rutas duplicadas/conflictivas, symlinks, archivos extra y el uso de `manifest.json` como entrada.
- Restauración: rechaza destinos que se solapan con el backup y crea directorios padre ausentes antes de preparar el reemplazo. La restauración sigue requiriendo escritores detenidos y confirmación explícita para sustituir datos.
- Se añadieron pruebas para manifiestos manipulados, archivos no declarados, rutas no canónicas, symlinks, destinos solapados y restauración en directorios nuevos.
- **Límite persistente:** los backups siguen sin cifrado ni firma criptográfica externa. La protección de integridad SHA-256 detecta alteraciones respecto del manifiesto, pero no autentica el origen si un atacante puede reemplazar ambos. La clave/almacenamiento externo, WORM y pruebas de recuperación operacional siguen pendientes.
- Comparación actual con `main`: `codex/security-integrity-audit` está divergida, **306 commits adelante y 1 detrás**. El commit exclusivo de `main` sigue siendo `7b5ed033f1f6461b5780a10ac4ada67a444b93e5`; no se hizo merge ni force-push.
- La evidencia CI anterior sustituye la anotación histórica de “CI no verificado” solo para el SHA indicado. No demuestra compatibilidad con proveedores remotos, aislamiento microVM, recuperación ante pérdida física, cifrado/KMS ni certificación institucional.


## Validación de Skillbook y HEAD actualizado — 2026-11-16

- HEAD de código validado: `ece33eb64ee9de098fbf63d7147122107f65b3a0`.
- Se corrigió la promoción repetida de una Skill: la aprobación firmada conserva la huella del payload y una repetición idéntica devuelve la Skill/version ya activada, sin crear una segunda Skill activa. La prueba cubre la repetición y confirma que el historial sigue siendo `proposed → approved`.
- CI para ese SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922107708). El paso de verificación completa terminó correctamente.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922107770). Construcción, verificación completa, Ruff en el sandbox y carga de evidencia terminaron correctamente.
- Comparación con `main` después de estos commits: **310 commits adelante / 1 detrás**, estado `diverged`. Se mantiene la decisión de no hacer merge ni force-push sin resolver el commit exclusivo de `main`.
- Esta validación confirma las suites y el sandbox CI del código de esta revisión; no sustituye pruebas operacionales con proveedores remotos, despliegue KMS/HSM/WORM, cifrado de backups, microVM ni pruebas de recuperación ante fallos físicos.


## Integridad autenticada y restauración resistente a TOCTOU — 2026-11-16

- HEAD de código validado: `2350069ab15597cac0699a49ea084163a8265892`.
- `data_backup.py` admite firma HMAC-SHA256 opcional del manifiesto mediante `CYBER_AI_BACKUP_HMAC_KEY` (mínimo 32 bytes). Cuando existe la clave, los backups se firman automáticamente; `verify` y `restore` aceptan `--require-signature`. Una copia firmada no se valida si falta la clave o no coincide. El modo sin firma sigue disponible para compatibilidad.
- La restauración vuelve a comprobar la huella del manifiesto después de la verificación y calcula tamaño/SHA-256 de cada archivo copiado antes de publicar el directorio restaurado. Esto detecta cambios de origen entre verificación y copia (TOCTOU).
- README actualizado con el flujo de firma, verificación y restauración. HMAC no cifra, no equivale a identidad individual ni sustituye KMS/HSM, rotación de claves o almacenamiento WORM.
- Prueba de regresión que muta el archivo de origen entre verificación y copia; la restauración debe abortar y conservar intacto el directorio de datos existente.
- CI para este SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922727386): verificación completa, **352 pruebas**.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922727384): build, verificación completa, Ruff dentro del sandbox y carga de evidencia.
- Comparación actual con `main`: **316 commits adelante / 1 detrás**, estado `diverged`. No se ha fusionado ni sobrescrito `main`.
- Pendiente externo: provisionar y custodiar la clave HMAC desde un gestor de secretos, definir rotación/recuperación, habilitar cifrado de backup y almacenar copias/checkpoints fuera del host. No declarar restauración institucional hasta ejecutar simulacros reales de pérdida y recuperación.


## Auditoría de proveedores y procedencia — 2026-11-16

- HEAD de código validado: `08d5f51e133908e3d6586af6cc29102ccc47e505`.
- `llm_providers.py`: se valida el timeout (finito, mayor que cero y máximo 600 s), la estructura de respuesta normalizada, la cantidad de embeddings solicitados, dimensiones/valores finitos y contadores de uso no negativos. Se añadieron pruebas de límites y respuestas malformadas.
- Nuevo `knowledge_provenance.py`: auditoría de IDs, URLs HTTPS, editor declarado, licencia/evidencia, compuerta de descarga y fechas/intervalos de revisión. `verify.sh` lo ejecuta y `docs/KNOWLEDGE_PROVENANCE.md` documenta los criterios.
- Resultado del catálogo actual: **138 referencias externas, 0 aprobadas/revisadas por este control, 276 hallazgos pendientes, 0 errores estructurales y 0 vencidas**. No se marcan como confiables ni descargables por defecto. Las referencias necesitan revisión real de licencia, procedencia y vigencia.
- CI de este SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43957123521): verificación completa, **365 pruebas**.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43957123616): build, verificación completa, Ruff dentro del sandbox y carga de evidencia.
- La historia se reconcilió con el commit exclusivo de `main` mediante un commit de merge que conserva el árbol de la rama auditada. Comparación: **327 commits adelante / 0 detrás**. PR #2 queda mergeable/clean, pero sigue draft y no se fusionó en `main`.
- Esto no certifica proveedores reales, seguridad jurídica del corpus, KMS/HSM, cifrado/WORM, microVM, RBAC, recuperación ante pérdida de host ni carga/estrés operacional. Esas pruebas requieren servicios, infraestructura y revisión humana externos.



## Trabajo de cierre adicional — 2026-11-16

- HEAD de la rama: `b5974450f8341a30d5197707cf2997296b4d2223`.
- Se añadieron `.github/dependabot.yml` para proponer actualizaciones semanales de dependencias Python y GitHub Actions, `SECURITY.md` con canal/proceso de reporte responsable y `docs/RELEASE_GATES.md` con criterios verificables de build, seguridad, conocimiento/IA, resiliencia y autorización de release.
- La rama no tiene protección habilitada (`protected=false`); branch protection y required checks siguen siendo una configuración administrativa pendiente. No se activaron porque el acceso disponible no permite garantizar que los permisos de administración estén concedidos.
- PR #2 permanece abierto y en draft; no se fusionó.
- CI disparada por los cambios: para el commit `60148e426e9e1c61edcd543de9320d213f1bd97b`, Python tests estaba `in_progress` y Docker sandbox `queued` al momento de esta actualización. Los resultados verdes del SHA anterior `4dfca8889ab84bd0345dce80dd084f95faecec16` no validan los nuevos archivos ni el HEAD actual.
- Dependabot solo crea propuestas; no aprueba ni fusiona actualizaciones automáticamente.
- No se ha añadido una licencia: es una decisión legal del propietario del repositorio, no algo que deba inventarse.
- El lock `requirements.lock` sigue sin hashes de artefactos. Añadir hashes no verificados sería inseguro; debe generarse desde un entorno de resolución confiable y fijarse para todas las plataformas objetivo.
- Próximas brechas implementables: hash-locked reproducible con verificación de artefactos, pruebas de estrés/concurrencia automatizadas, política de release y cobertura adicional de fallo abrupto. Las brechas que dependen de servicios/decisiones externas siguen abiertas: KMS/HSM, cifrado y rotación, WORM externo, RBAC/IdP, microVM, licencias y restauración real.
