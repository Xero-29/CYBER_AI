# Estado real y plan de cierre de CYBER_AI

**Actualizado:** 2026-11-15  
**Rama:** codex/security-integrity-audit
**CI:** Actions fijadas por SHA, checkout v5/setup-python v6/upload-artifact v5 (Node 24)  
**Base:** main (sin merge ni despliegue)

## Avance de esta iteración

Se añadió `knowledge_eval.py` con un conjunto inicial de 12 consultas y métricas Recall@K, Precision@K y MRR@K. El arnés y los datos están versionados; aún falta ejecutar el benchmark con modelos reales, fijar umbrales por dominio y ampliar el conjunto con evaluaciones revisadas por expertos.

Se reforzó el bootstrap de la biblioteca offline: IDs deterministas por ruta y SHA-256, bloqueo entre procesos, rechazo de rutas absolutas/traversal/symlinks, estados `processing/completed/failed`, reanudación tras fallos y prevención de duplicados. La indexación identifica el espacio vectorial del proveedor ECO y reindexa el contenido cuando cambia el modelo/proveedor, evitando mezclar vectores incompatibles en las búsquedas. Se añadieron pruebas de reintento, rutas, fallos y espacios de embeddings.

El descargador ahora exige `CYBER_AI_KNOWLEDGE_EGRESS_PROXY` para cualquier descarga real; sin gateway configurado falla antes de resolver el destino o abrir conexiones. El gateway debe imponer allowlist de hosts, pinning DNS y bloqueo de redes privadas. Esto no sustituye la validación de seguridad del proxy externo.

Se amplió `tool_adapters.py` con comandos locales acotados para Checkov, detect-secrets, Hadolint, ShellCheck, actionlint, kube-linter, YARA (requiere reglas locales) y TShark (solo PCAP/PCAPNG). El inventario distingue herramientas catalogadas, adaptadores registrados y binarios realmente disponibles. La presencia de un adaptador no implica que el binario esté instalado; las herramientas activas de red siguen fuera de esta ejecución local.

Se incorpora execution_ledger.py: registro SQLite transaccional append-only de ejecuciones con namespace, huella de tarea, estado, herramienta/versión, modelo, entorno, duración, coste opcional, resultados de validadores y hash SHA-256 de evidencia. Incluye cadena hash verificable, redacción de campos con nombres sensibles y bloqueo ordinario de UPDATE/DELETE. Se añaden pruebas específicas.

Límite: es evidencia tamper-evident, no almacenamiento WORM ni prueba criptográfica de identidad. Requiere checkpoints firmados fuera del host, KMS/HSM y pruebas operativas de restauración. La captura previa al inicio, la cobertura de todas las rutas de error y el comportamiento fail-closed ante caída del ledger siguen pendientes; también la promoción autónoma de Skills.

## Validación más reciente

- Commit `3032550a2a9a6e8e40ffd355e89d0dddb3af2904`: CI Python **success**, 278 pruebas. La ejecución Docker de ese commit se encontraba en curso en la última consulta.
- Commit `eded0518354b191ecf649c3f6e895819b6200ed9`: CI Python **success**, 267 pruebas. La ejecución Docker de ese commit se encontraba en curso en la última consulta.
- Commit `819645225ba47549e90e5d6092f388594241b739`: timeout Nuclei con terminación del grupo de procesos y pruebas para ambas rutas.
- GitHub Actions Python tests: **success**, 257 pruebas, incluyendo compilación, autopruebas y suite completa.
- Docker sandbox: **success** también en el commit `819645225ba47549e90e5d6092f388594241b739`; ambos workflows (Python y Docker) pasaron en esa revisión.
- La validación CI no equivale a pruebas con Ollama, proveedores remotos, objetivos reales autorizados, cargas adversariales ni aislamiento microVM.

## Capacidades existentes (no equivalen a cierre institucional)

- Inventario de 21 herramientas, selección explicable y 14 especificaciones de adaptador; 13 tienen rutas de ejecución local y pip-audit permanece bloqueado por red. El inventario separa registro, disponibilidad del binario y cobertura de adaptador.
- Sandbox Docker endurecido con timeout del cliente y limpieza forzada del contenedor ante timeout; comparte kernel y no es aislamiento para malware hostil.
- Atlas de 48 áreas y 138 referencias externas catalogadas; además, 48 paquetes metodológicos propios incluidos offline. Las referencias externas no están descargadas ni ingeridas.
- Biblioteca SQLite con fragmentos comprimidos, SHA-256, metadatos, separación shared/tenant y búsqueda semántica.
- Ingestión transaccional (publicación de todos los fragmentos en una única transacción), límite de 2 MiB por fragmento y descompresión acotada de TXT/Markdown, HTML, CSV, JSON/JSONL y código; extractores opcionales PDF/DOCX/XLSX/PPTX con límites de tamaño, expansión ZIP y extracción incremental acotada para evitar acumulación descontrolada de texto. OCR de PDF escaneado y ejecución aislada de extractores siguen pendientes. Catálogo, descubrimiento y downloader con manifiesto serializado por lock; dry-run sin DNS ni escrituras. La descarga ahora falla cerrada sin proxy de salida explícito; la garantía contra DNS rebinding depende de que el gateway configurado implemente allowlist, pinning DNS y bloqueo de redes privadas.
- Reindexación con staging, backup y publicación transaccional.
- Proveedores Ollama, OpenAI-compatible, Anthropic chat y Gemini chat/embeddings, con extensiones instalables mediante entry points `cyber_ai.providers`; HTTP solo en loopback, HTTPS remoto y redirecciones bloqueadas para proteger credenciales.
- Skillbook con propuestas candidatas desde dos eventos independientes, activación solo con firma HMAC VERITAS, versiones inmutables y exclusión de candidatas de la búsqueda ejecutable. La clave sigue siendo un secreto operativo externo, no una identidad de modelo.
- Memoria de lecciones con HMAC VERITAS vinculado a dos ejecuciones con revisiones objetivas de un agente revisor distinto y hashes del ledger, validación de firma al leer, aislamiento por namespace, lock y permisos 0600. El registro directo se bloquea; las lecciones v1 sin firma se ignoran. HMAC no autentica por sí solo la identidad del modelo.
- Dependencias base fijadas en `requirements.lock` para instalaciones repetibles (sin hashes de artefactos; la verificación de procedencia/hash queda pendiente).
- `preflight.py` para revisar dependencias, configuración, herramientas opcionales y ledger local sin iniciar servicios ni usar red.
- CLI `ledger_cli.py` para verificar integridad, listar namespaces y consultar historial.
- Ledger de ejecuciones: integrado con `agent_runner.py`, `tool_executor.py`, `nuclei_scanner.py`, `task_runner.py` y `team_orchestrator.py` para registrar respuestas, ejecuciones locales, timeouts, denegaciones y revisiones objetivas independientes. `agent_runner` marca la autocompletitud como no independiente. La escritura del ledger emite una advertencia si falla y no oculta el resultado original. El ciclo de Skills autónomas y el almacenamiento externo WORM siguen pendientes.

## Avance de biblioteca offline

- Catálogo ampliado a 48 especialidades.
- 48 paquetes base propios en español incluidos en `knowledge/packs/`, con competencias, metodología, controles, laboratorio y evaluación.
- Las referencias externas siguen pendientes de licencia/procedencia y no se declaran descargadas ni ingeridas.

- `knowledge_bootstrap.py` valida e indexa paquetes offline con ECO. El dry-run no requiere IA. La ingestión real requiere un proveedor con embeddings configurado. El proceso es reanudable, idempotente y detecta cambios de espacio vectorial para reindexar. No se inicia automáticamente por conectar un chat.

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
