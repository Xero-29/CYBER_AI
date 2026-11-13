# Estado real y plan de cierre de CYBER_AI

**Actualizado:** 2026-11-13  
**Rama:** codex/security-integrity-audit
**CI:** Actions fijadas por SHA, checkout v5/setup-python v6/upload-artifact v5 (Node 24)  
**Base:** main (sin merge ni despliegue)

## Avance de esta iteración

Se incorpora execution_ledger.py: registro SQLite transaccional append-only de ejecuciones con namespace, huella de tarea, estado, herramienta/versión, modelo, entorno, duración, coste opcional, resultados de validadores y hash SHA-256 de evidencia. Incluye cadena hash verificable, redacción de campos con nombres sensibles y bloqueo ordinario de UPDATE/DELETE. Se añaden pruebas específicas.

Límite: es evidencia tamper-evident, no almacenamiento WORM ni prueba criptográfica de identidad. Requiere checkpoints firmados fuera del host, KMS/HSM y pruebas operativas de restauración. La captura previa al inicio, la cobertura de todas las rutas de error y el comportamiento fail-closed ante caída del ledger siguen pendientes; también la promoción autónoma de Skills.

## Capacidades existentes (no equivalen a cierre institucional)

- Inventario de 20 herramientas, selección explicable y adaptadores parciales; los adaptadores locales registran la versión instalada cuando puede consultarse sin red.
- Sandbox Docker endurecido con timeout del cliente y limpieza forzada del contenedor ante timeout; comparte kernel y no es aislamiento para malware hostil.
- Atlas de 28 áreas y 98 referencias catalogadas, no corpus completo ingerido.
- Biblioteca SQLite con fragmentos comprimidos, SHA-256, metadatos, separación shared/tenant y búsqueda semántica.
- Ingestión transaccional (publicación de todos los fragmentos en una única transacción), límite de 2 MiB por fragmento y descompresión acotada de TXT/Markdown, HTML, CSV, JSON/JSONL y código; extractores opcionales PDF/DOCX/XLSX/PPTX con límites de tamaño y expansión ZIP. OCR de PDF escaneado y ejecución aislada de extractores siguen pendientes. Catálogo, descubrimiento y downloader con manifiesto serializado por lock; dry-run sin DNS ni escrituras. Sigue pendiente resolver DNS rebinding/TOCTOU mediante proxy de salida o pinning de IP.
- Reindexación con staging, backup y publicación transaccional.
- Proveedores Ollama, OpenAI-compatible, Anthropic chat y Gemini chat/embeddings, con extensiones instalables mediante entry points `cyber_ai.providers`; HTTP solo en loopback, HTTPS remoto y redirecciones bloqueadas para proteger credenciales.
- Skillbook con propuestas candidatas desde dos eventos independientes, activación solo con firma HMAC VERITAS, versiones inmutables y exclusión de candidatas de la búsqueda ejecutable. La clave sigue siendo un secreto operativo externo, no una identidad de modelo.
- Memoria de lecciones con HMAC VERITAS vinculado a dos ejecuciones con revisiones objetivas de un agente revisor distinto y hashes del ledger, validación de firma al leer, aislamiento por namespace, lock y permisos 0600. El registro directo se bloquea; las lecciones v1 sin firma se ignoran. HMAC no autentica por sí solo la identidad del modelo.
- Dependencias base fijadas en `requirements.lock` para instalaciones repetibles (sin hashes de artefactos; la verificación de procedencia/hash queda pendiente).
- `preflight.py` para revisar dependencias, configuración, herramientas opcionales y ledger local sin iniciar servicios ni usar red.
- CLI `ledger_cli.py` para verificar integridad, listar namespaces y consultar historial.
- Ledger de ejecuciones: integrado con `agent_runner.py`, `tool_executor.py`, `nuclei_scanner.py`, `task_runner.py` y `team_orchestrator.py` para registrar respuestas, ejecuciones locales, timeouts, denegaciones y revisiones objetivas independientes. `agent_runner` marca la autocompletitud como no independiente. La escritura del ledger emite una advertencia si falla y no oculta el resultado original. El ciclo de Skills autónomas y el almacenamiento externo WORM siguen pendientes.

## Pendientes de cierre

1. **Ejecución y aprendizaje:** completar captura de inicio/fin y cobertura de fallos en todos los ejecutores; almacenar artefactos en repositorio controlado; checkpoints firmados externos; costes reales por proveedor; retención y privacidad.
2. **Skills verificadas:** conectar el ciclo automático de propuestas con la API de promoción firmada; provisionar firma desde KMS/HSM o servicio independiente; versionado, rollback, regresión y detección de obsolescencia.
3. **Biblioteca documental:** validar extractores PDF/Office en fixtures adversariales y sandbox; OCR cuando aplique; deduplicación/versionado; índice híbrido FTS + vector/ANN; evaluación de recuperación; citas por fragmento; revisión de licencias/procedencia.
4. **Herramientas:** completar adaptadores según utilidad y riesgo, fijar versiones e imágenes por digest, SBOM/procedencia, hashes y pruebas; no habilitar herramientas de red sin política explícita; el downloader aún requiere mitigación externa del riesgo DNS rebinding.
5. **Sandbox:** Docker solo para código confiable/acotado; microVM/VM desechable requiere infraestructura externa y pruebas de aislamiento; gestión de secretos y permisos.
6. **IA:** contrato de capacidades común, embeddings equivalentes, detección de capacidades, selección/fallback de modelos, pruebas de compatibilidad y gestión segura de credenciales.
7. **Operación institucional:** threat model formal, RBAC, auditoría inmutable externa, backups cifrados y restauración probada, retención, redacción, migraciones, concurrencia, observabilidad, carga y revisión independiente.

## Criterio de cierre

No declarar el sistema completo ni certificado hasta que cada brecha tenga código, pruebas automatizadas, evidencia reproducible y validación operacional. No descargar indiscriminadamente el atlas, no ejecutar herramientas de red por defecto y no promover Skills por respuestas plausibles.
