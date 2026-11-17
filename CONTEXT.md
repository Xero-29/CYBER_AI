# CYBER_AI — Contexto vigente del proyecto

## Objetivo
Sistema modular de investigación y ciberseguridad para análisis de código, informes, vulnerabilidades y evidencias, con ejecución limitada a activos propios o expresamente autorizados. La IA es intercambiable; conocimiento, memoria, Skills, políticas y ledger permanecen en el proyecto.

## Restricciones de diseño
- Mantener consumo y dependencias razonables para equipos modestos.
- Reutilizar herramientas especializadas en vez de crear sustitutos innecesarios.
- Separar planificación, autorización, ejecución, evidencia y revisión.
- No interpretar la salida de una herramienta como verdad verificada.
- No ejecutar herramientas ni escaneos activos sin autorización explícita y alcance definido.
- Mantener datos locales y credenciales fuera del control de los proveedores LLM.

## Entradas principales
- `python cyber_ai.py --ask "tarea"`: DIRECTOR, especialistas, memoria y recuperación de conocimiento.
- `python cyber_ai.py --team "tarea"`: planificador, capacidades y orquestación multiagente supervisada.
- `python cyber_ai.py --report archivo.txt`: análisis de un informe y referencias CVE.
- `python cyber_ai.py --batch carpeta/`: procesamiento por lotes de informes TXT/Markdown.
- `python cyber_ai.py --scan https://objetivo-autorizado`: escaneo Nuclei con autorización local específica.
- `python cyber_ai.py --self-test`: comprobación superficial de archivos; no sustituye la suite de pruebas.

## Subsistemas con función identificada
- Agentes y proveedores: `director.py`, `team_orchestrator.py`, `agent_runner.py`, `llm_providers.py`.
- Capacidades y ejecución: `capability_inventory.py`, `capability_selector.py`, `task_planner.py`, `tool_adapters.py`, `tool_execution_pipeline.py`.
- Autorización y trazabilidad: `execution_policy.py`, `tool_allowlist.py`, `execution_ledger.py`, validadores y evidencia.
- Conocimiento: `knowledge_*.py`, `data/knowledge_sources/`, `knowledge/packs/`.
- Memoria y Skills: `learning_memory.py`, `model_memory_manager.py`, `skillbook.py`.
- Informes y CVE: `report_analyzer.py`, `nvd_client.py`, `batch_analyzer.py`, `report_manager.py`.
- Escaneo remoto: `nuclei_scanner.py` y `scan_result_validator.py`.

## Límites conocidos
- La validación de evidencia comprueba integridad/estructura y alcance declarado; no demuestra por sí sola la veracidad ni explotabilidad de hallazgos.
- La ejecución de adaptadores locales ocurre en el host; el aislamiento de red del proceso no está forzado.
- Nuclei conserva un flujo de autorización independiente; no hereda permisos del planificador local.
- Las capacidades declaradas o catalogadas no implican que una herramienta esté instalada, adaptada o lista para ejecutarse.
- El estado de CI y las pruebas debe comprobarse en el commit actual; no reutilizar resultados de commits anteriores como si validaran cambios nuevos.

## Reglas para mantener el repositorio
1. Cada módulo nuevo debe tener un propósito concreto, un punto de entrada o consumidor identificable y pruebas apropiadas.
2. No mantener prototipos, demos ni duplicados sin uso como si fueran subsistemas activos.
3. Antes de eliminar un archivo, comprobar sus referencias, pruebas y documentación; conservar utilidades independientes si aportan una función distinta y documentada.
4. Actualizar esta página cuando cambie la arquitectura real. No acumular cronologías antiguas como estado vigente.
5. No declarar el sistema listo para producción sin superar los gates documentados y una revisión independiente.
