# CYBER_AI

Sistema modular de investigación técnica y ciberseguridad con agentes LLM, biblioteca de conocimiento, memoria verificada, Skills, adaptadores de herramientas y registro auditable de ejecuciones.

> Estado: rama de integración `codex/security-integrity-audit`. No es una versión certificada para producción. Algunas capacidades están implementadas pero requieren validación local; consulta [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Requisitos

- Linux recomendado (Ubuntu), Python 3.12 o superior.
- Git.
- Para agentes locales: Ollama instalado y ejecutándose.
- Para el sandbox: Docker Engine/CLI.
- Conexión a Internet solo para instalar dependencias, descargar modelos o usar proveedores remotos. Los escáneres locales no deben recibir acceso de red salvo autorización explícita.

El núcleo Python usa dependencias ligeras declaradas en `requirements.txt`. Ollama, Docker y las herramientas de seguridad son componentes externos opcionales.

## Descargar

```bash
git clone --branch codex/security-integrity-audit https://github.com/Xero-29/CYBER_AI.git
cd CYBER_AI
```

## Instalar dependencias Python

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
```

También puedes usar el instalador incluido:

```bash
bash setup.sh
source .venv/bin/activate
```

El instalador crea el entorno virtual e instala dependencias Python. No instala Ollama, Docker, modelos ni herramientas de seguridad.

## Comprobaciones iniciales

```bash
python cyber_ai.py --self-test
python -m compileall -q .
python -m unittest discover -s tests -v
python preflight.py
# O, en una sola ejecución local:
bash verify.sh
```

El preflight revisa Python, archivos, dependencias, herramientas opcionales y la integridad del ledger existente; no inicia servicios ni realiza llamadas de red. Las advertencias de Docker/Ollama/escáneres son opcionales según las funciones que quieras probar.

La suite automatizada no requiere conectar un modelo real; los tests de red y proveedores deben usar dobles/simulaciones salvo que un test indique expresamente lo contrario.

## Ejecutar el análisis de informes

```bash
python cyber_ai.py --report reports/mi_informe.txt
python cyber_ai.py --batch reports
```

## Ejecutar agentes LLM locales

1. Instala Ollama siguiendo su documentación oficial y arranca el servicio.
2. Revisa `config/model_roles.json`: cada agente declara su modelo, proveedor y permisos.
3. Descarga únicamente el modelo que vayas a usar. Los nombres por defecto se encuentran en ese archivo; no es necesario descargar todos los modelos.
4. Consulta el estado y ejecuta una tarea:

```bash
ollama serve
# En otra terminal, descarga el modelo configurado para el agente que usarás:
ollama pull qwen3.5:4b-q4_K_M
python agent_runner.py status
python agent_runner.py ask NEXO "Analiza este problema y propone una metodología verificable."

# Exigir ledger antes de ejecutar y al registrar el resultado:
export CYBER_AI_LEDGER_REQUIRED=1
python agent_runner.py ask NEXO "Analiza este problema y propone una metodología verificable."
```

Si Ollama ya se ejecuta como servicio, no inicies una segunda instancia con `ollama serve`.

Para usar otro proveedor, configura su bloque en `config/model_roles.json`, activa `enabled` y proporciona la credencial mediante la variable de entorno declarada. Puedes enrutar por capacidad con `capability_providers` y configurar alternativas explícitas en `fallback_providers`; este fallback resuelve incompatibilidades de capacidad, no fallos transitorios de red. No guardes claves en Git. Para cualquier API no incluida de forma nativa, instala un adaptador como entry point `cyber_ai.providers`; el contrato está documentado en [docs/PROVIDER_PLUGIN_CONTRACT.md](docs/PROVIDER_PLUGIN_CONTRACT.md). Esto requiere un plugin compatible, no cambios en el núcleo.

```bash
export CYBER_AI_LLM_API_KEY="..."
```

Los proveedores remotos están deshabilitados por defecto. Anthropic no ofrece embeddings en este adaptador; usa un proveedor de embeddings compatible para indexar y recuperar vectores.

## Herramientas locales y sandbox

El inventario de 21 herramientas distingue disponibilidad del binario y adaptadores realmente registrados. Hay 14 especificaciones de adaptador: 11 herramientas de ejecución local acotada; YARA y TShark quedan bloqueadas en el host hasta disponer de sandbox aislado; pip-audit queda bloqueado por requerir red. El informe separa adaptador registrado de ejecución realmente habilitada. La presencia en el catálogo no significa que la herramienta esté instalada. Genera el informe con `python capability_inventory.py`.

El registro de herramientas se encuentra en `tool_adapters.py`. Para ejecutar directamente un adaptador local:

```bash
python tool_executor.py --tool ruff --target tests/fixtures/sandbox_sample.py
python tool_executor.py --tool ruff --target tests/fixtures/sandbox_sample.py --execute
# Para exigir registro de inicio y resultado antes de permitir la ejecución:
python tool_executor.py --tool ruff --target tests/fixtures/sandbox_sample.py --execute --require-ledger
```

La ejecución real requiere `--execute`. Para el contenedor:

```bash
docker build -t cyber-ai-tool-sandbox:local -f sandbox/Dockerfile .
python sandbox_runner.py --tool ruff --target tests/fixtures/sandbox_sample.py --execute
```

La imagen Docker actual solo incluye Ruff y Bandit. Semgrep, Syft y Trivy están registrados, pero no disponibles dentro de esa imagen. Docker comparte el kernel del host y no equivale a una microVM; no ejecutes código hostil confiando únicamente en este aislamiento.

## Biblioteca de conocimiento offline y Skills

El repositorio incluye paquetes metodológicos propios en español para todas las especialidades del catálogo. Consulta `knowledge/packs/manifest.json` y `knowledge/packs/<area>/README.md`. Son una base inicial, no una enciclopedia ni sustituyen corpus especializados. Las referencias externas solo se descargan tras validar licencia, procedencia e integridad. Además, toda descarga real exige `CYBER_AI_KNOWLEDGE_EGRESS_PROXY` apuntando a un gateway de salida que aplique allowlist de hosts, pinning DNS y bloqueo de redes privadas; el descargador falla cerrado si no está configurado.

Después de configurar un proveedor con embeddings, valida e indexa la biblioteca offline:

```bash
python knowledge_bootstrap.py --dry-run
python knowledge_bootstrap.py
```

La primera orden valida rutas y hashes sin IA ni escrituras. La segunda genera embeddings con ECO, ingiere paquetes nuevos/modificados y registra hash y clasificación. El bootstrap es reanudable e idempotente; si cambia el proveedor/modelo de embeddings, vuelve a indexar los paquetes en el nuevo espacio vectorial.

Para reconstruir el índice textual FTS5 de una biblioteca existente sin generar embeddings:

```bash
python knowledge_bootstrap.py --rebuild-text-index
```

La recuperación combina búsqueda semántica y texto completo mediante Reciprocal Rank Fusion (RRF), respetando el aislamiento por tenant. Si SQLite no incluye FTS5, el sistema conserva el modo semántico. Para bibliotecas existentes, `--rebuild-text-index` reconstruye FTS5 verificando SHA-256 de cada fragmento.

Crea y verifica copias locales de las bases SQLite y archivos de datos. Detén los procesos que escriben en `data/` antes de copiar/restaurar:

```bash
python data_backup.py backup --destination /ruta/segura/cyber-ai-backup --confirm-quiesced
python data_backup.py verify --snapshot /ruta/segura/cyber-ai-backup
# La restauración conserva el directorio anterior como .pre-restore-*:
python data_backup.py restore --snapshot /ruta/segura/cyber-ai-backup --confirm-quiesced --confirm-replace
```

Este backup verifica integridad y usa snapshots SQLite consistentes, pero **no cifra** los datos. No lo copies a almacenamiento externo sin cifrado y controles de acceso; no sustituye WORM ni una estrategia de recuperación institucional.

Genera un SBOM CycloneDX determinista a partir de las dependencias fijadas:

```bash
python sbom_generator.py --output reports/cyber-ai-sbom.cdx.json
```

El SBOM distingue dependencias directas y transitivas y registra el hash del lock. El lock actual no contiene hashes de artefactos ni un grafo transitivo completo; el SBOM no afirma verificar esos elementos.

Para medir la recuperación por especialidad después de indexar, ejecuta el benchmark por defecto de 48 consultas (una por área). El conjunto de 12 consultas anteriores queda disponible como smoke test rápido:

```bash
python knowledge_eval.py --top-k 5 --output reports/knowledge-eval.json
# Smoke test reducido:
python knowledge_eval.py --dataset knowledge/evaluation/smoke_queries.jsonl --top-k 5
```

El informe calcula Recall@K, Precision@K y MRR@K. Los resultados dependen del modelo de embeddings y del contenido indexado; el benchmark no presupone que la calidad sea aceptable. Anthropic está integrado para chat, no para embeddings; si lo usas, configura además un proveedor compatible de embeddings.

## Conocimiento y Skills

- Ingesta TXT, Markdown, HTML, CSV, JSON/JSONL y código: disponible con las dependencias base. PDF, DOCX, XLSX y PPTX requieren `pip install -r requirements-documents.txt`. Los PDF escaneados necesitan OCR externo; el importador no ejecuta OCR.
- Recuperación e indexación: revisa `knowledge_library.py`, `knowledge_embeddings.py` y `knowledge_reindex.py`.
- Fuentes externas: el catálogo requiere revisión de licencia y verificación antes de habilitar descargas.
- Skills: `propose_skill_from_ledger` crea candidatas no ejecutables; solo la promoción firmada por VERITAS las hace recuperables. El CLI `skillbook_cli.py` permite proponer desde un manifiesto ligado a dos ejecuciones, exportar el payload canónico para firma independiente, promover con firma y generar/aplicar rollback. El historial de versiones es append-only. Una coincidencia recuperada no concede permisos de ejecución.

Ejemplo de flujo (el manifiesto JSON contiene los campos requeridos por la API):

```bash
python skillbook_cli.py propose --manifest reports/skill-candidate.json
python skillbook_cli.py approval-payload --manifest reports/skill-candidate.json
# Un aprobador independiente firma el payload fuera del proceso de generación.
python skillbook_cli.py promote --manifest reports/skill-candidate.json --signature-file reports/veritas-signature.txt
```

No firmes automáticamente la salida del mismo agente que propuso la Skill. Mantén `CYBER_AI_VERITAS_APPROVAL_KEY` fuera del repositorio y delega su uso en un servicio o aprobador independiente.

Los extractores de Office validan el tamaño de los paquetes comprimidos, pero siguen procesando archivos en el proceso local; importa solo documentos confiables hasta que se ejecute la extracción en una sandbox dedicada.

Los ejecutores `tool_executor.py` y `task_runner.py` admiten `--require-ledger`: si el ledger no puede registrar el inicio o el resultado, la operación se bloquea o termina con código 3. `agent_runner.py` permite exigirlo con `CYBER_AI_LEDGER_REQUIRED=1`; `nuclei_scanner.scan_target` acepta `require_ledger=True`; `team_orchestrator.py` exige registrar inicio y resultado. Sin exigencia configurada, los ejecutores que lo permiten emiten advertencias y continúan. Los eventos `started` se enlazan a un evento terminal; no se usan como evidencia de éxito para promocionar Skills. Una excepción inesperada todavía puede dejar un inicio sin evento terminal.

Los datos locales, bases SQLite, historiales y reportes se guardan fuera del control de versiones mediante `.gitignore`. Haz copias de seguridad antes de borrar o recrear `data/`.

## Seguridad operativa

- Analiza únicamente activos propios o con autorización explícita y vigente.
- Los comandos de escaneo externo requieren autorización local específica; no uses un objetivo de terceros sin permiso.
- El modo dry-run es el predeterminado en los ejecutores.
- No introduzcas credenciales en prompts, reportes, logs o archivos versionados.
- Revisa manualmente los hallazgos; la salida de una herramienta o un modelo no confirma por sí sola una vulnerabilidad.
- El ledger local es tamper-evident, no tamper-proof. Para uso institucional requiere checkpoints firmados y almacenamiento inmutable independiente.
- Los datos locales no se sincronizan automáticamente al descargar el repositorio.

## Evidencia y diagnóstico

Consulta la integridad del ledger, el historial y ancla su cabeza con una clave externa:

```bash
export CYBER_AI_LEDGER_CHECKPOINT_KEY="secreto-de-al-menos-32-bytes-guardado-fuera-del-repo"
python ledger_checkpoint.py create --output /ruta/externa/checkpoint.json
python ledger_checkpoint.py verify --checkpoint /ruta/externa/checkpoint.json
```

Guarda los checkpoints fuera del host/volumen del ledger y protege la clave mediante un gestor de secretos o KMS. El HMAC local no sustituye WORM ni una identidad de operador independiente.

Consulta la integridad del ledger y el historial registrado:

```bash
python ledger_cli.py verify
python ledger_cli.py namespaces
python ledger_cli.py history --namespace local-tools
```

- `PROJECT_STATUS.md`: capacidades, limitaciones y brechas conocidas.
- `docs/THREAT_MODEL.md`: baseline STRIDE, límites de confianza, amenazas y pruebas de aceptación pendientes.
- `docs/EXECUTION_LEDGER.md`: modelo de evidencia y límites del ledger.
- `docs/CYBERSECURITY_KNOWLEDGE_ATLAS.md`: mapa de áreas y referencias catalogadas.
- `data/`: bases de conocimiento, memoria, Skills y eventos locales (no incluidos en el repositorio por defecto).
- `reports/`: resultados y evidencias generadas.

Al informar un fallo, conserva el comando, versión de Python, salida completa y el identificador de ejecución de CI si aplica.
