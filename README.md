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
```

Si Ollama ya se ejecuta como servicio, no inicies una segunda instancia con `ollama serve`.

Para usar otro proveedor, configura su bloque en `config/model_roles.json`, activa `enabled` y proporciona la credencial mediante la variable de entorno declarada. No guardes claves en Git. Para cualquier API no incluida de forma nativa, instala un adaptador como entry point `cyber_ai.providers`; el contrato está documentado en [docs/PROVIDER_PLUGIN_CONTRACT.md](docs/PROVIDER_PLUGIN_CONTRACT.md). Esto requiere un plugin compatible, no cambios en el núcleo.

```bash
export CYBER_AI_LLM_API_KEY="..."
```

Los proveedores remotos están deshabilitados por defecto. Anthropic no ofrece embeddings en este adaptador; usa un proveedor de embeddings compatible para indexar y recuperar vectores.

## Herramientas locales y sandbox

El inventario de 21 herramientas distingue disponibilidad del binario y adaptadores realmente registrados. Hay adaptadores locales para Ruff, Bandit, Semgrep, Syft, Trivy, Checkov, detect-secrets, Hadolint, ShellCheck, actionlint, kube-linter, YARA y TShark; pip-audit permanece bloqueado por requerir red. La presencia en el catálogo no significa que la herramienta esté instalada. Genera el informe con `python capability_inventory.py`.

El registro de herramientas se encuentra en `tool_adapters.py`. Para ejecutar directamente un adaptador local:

```bash
python tool_executor.py --tool ruff --target tests/fixtures/sandbox_sample.py
python tool_executor.py --tool ruff --target tests/fixtures/sandbox_sample.py --execute
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

Para medir la calidad de recuperación tras indexar, ejecuta el benchmark inicial de 12 consultas:

```bash
python knowledge_eval.py --top-k 5 --output reports/knowledge-eval.json
```

El informe calcula Recall@K, Precision@K y MRR@K. Los resultados dependen del modelo de embeddings y del contenido indexado; el benchmark no presupone que la calidad sea aceptable. Anthropic está integrado para chat, no para embeddings; si lo usas, configura además un proveedor compatible de embeddings.

## Conocimiento y Skills

- Ingesta TXT, Markdown, HTML, CSV, JSON/JSONL y código: disponible con las dependencias base. PDF, DOCX, XLSX y PPTX requieren `pip install -r requirements-documents.txt`. Los PDF escaneados necesitan OCR externo; el importador no ejecuta OCR.
- Recuperación e indexación: revisa `knowledge_library.py`, `knowledge_embeddings.py` y `knowledge_reindex.py`.
- Fuentes externas: el catálogo requiere revisión de licencia y verificación antes de habilitar descargas.
- Skills: `propose_skill_from_ledger` crea candidatas no ejecutables; solo la promoción firmada por VERITAS las hace recuperables. El historial de versiones es append-only. Una coincidencia recuperada no concede permisos de ejecución.

Los extractores de Office validan el tamaño de los paquetes comprimidos, pero siguen procesando archivos en el proceso local; importa solo documentos confiables hasta que se ejecute la extracción en una sandbox dedicada.

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

Consulta la integridad del ledger y el historial registrado:

```bash
python ledger_cli.py verify
python ledger_cli.py namespaces
python ledger_cli.py history --namespace local-tools
```

- `PROJECT_STATUS.md`: capacidades, limitaciones y brechas conocidas.
- `docs/EXECUTION_LEDGER.md`: modelo de evidencia y límites del ledger.
- `docs/CYBERSECURITY_KNOWLEDGE_ATLAS.md`: mapa de áreas y referencias catalogadas.
- `data/`: bases de conocimiento, memoria, Skills y eventos locales (no incluidos en el repositorio por defecto).
- `reports/`: resultados y evidencias generadas.

Al informar un fallo, conserva el comando, versión de Python, salida completa y el identificador de ejecución de CI si aplica.
