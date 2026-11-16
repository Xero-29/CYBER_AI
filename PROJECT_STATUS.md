# Estado real y plan de cierre de CYBER_AI

**Actualizado:** 2026-11-16  
**Rama:** codex/security-integrity-audit
**CI:** Actions fijadas por SHA, checkout v5/setup-python v6/upload-artifact v5 (Node 24)  
**Base:** main (sin merge ni despliegue)

## Avance de esta iteración

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

- Comparación directa con `main`: rama de auditoría **296 commits ahead / 1 behind**; estado GitHub `diverged`.
- El único commit exclusivo de `main` es `7b5ed033f1f6461b5780a10ac4ada67a444b93e5` (`fix: repair sandbox policy tests`), que modifica `tests/test_sandbox_runner.py`.
- La versión de ese test en la rama de auditoría ya contiene las comprobaciones de ese commit y añade regresiones para el ledger obligatorio, allowlist de herramientas de sandbox, timeout del proceso Docker, imagen fijada por digest y validación de rutas de evidencia. Por tanto, no se debe reemplazar la versión de la rama por el archivo más antiguo de `main`.
- La divergencia se mantiene explícita; no se ha hecho merge ni force-push. Antes de integrar, revisar el grafo completo y confirmar que no existen otros efectos del commit exclusivo fuera del archivo comparado.
- Revisión del flujo de excepciones: la firma de `_run_agent_impl` coloca `task_id` en el quinto argumento posicional; el wrapper lo propaga en esa posición o como keyword, y la correlación se realiza por `metadata.task_id`, no por el prompt redactado.
- **CI del HEAD actual: no verificado.** La consulta de ejecuciones y estados para el SHA de `main` no devuelve checks, y no se obtuvo una referencia verificable al SHA actual de la rama en esta consulta. Los resultados CI históricos indicados arriba no deben interpretarse como validación del HEAD actual.

