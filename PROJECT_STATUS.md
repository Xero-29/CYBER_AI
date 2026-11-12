# Estado del proyecto CYBER_AI

**Actualizado:** 2026-11-11  
**Rama de trabajo:** `codex/security-integrity-audit`  
**Rama base:** `main`  
**Estado:** cambios iniciales implementados; validación de ejecución pendiente.

## Resumen

Se creó una rama de trabajo independiente para aplicar correcciones de seguridad e integridad sin modificar `main`. Los cambios se concentran en autorización explícita, preservación de evidencias, validación de identificadores y pruebas automatizadas.

## Cambios implementados

- **Escaneos Nuclei:** `scan_target` exige `authorized=True`; la CLI ofrece `--confirm-authorized`. Cada escaneo usa un JSONL con identificador único para no truncar ni mezclar evidencias anteriores.
- **Informes:** el índice de duplicados falla de forma segura si está corrupto, en vez de reemplazarlo por un índice vacío. La escritura del índice es atómica.
- **Procesamiento por lotes:** los nombres de salida incorporan una huella de la ruta de origen para evitar colisiones entre archivos con el mismo nombre base.
- **CLI:** `--self-test` ejecuta el descubrimiento de pruebas unitarias en `tests/`; los informes de escaneo usan nombres únicos.
- **NVD:** los identificadores CVE se validan con el formato esperado antes de realizar solicitudes.
- **Motor de agentes:** el texto generado por el agente ya no dispara acciones HTTP o de archivos automáticamente. Las propuestas requieren aprobación; la inspección HTTP exige confirmación explícita y la inspección de archivos queda confinada al proyecto.
- **Ejecutor de tareas:** se eliminan plantillas fuera de las familias previstas y cada escaneo conserva sus propios archivos de resultados.
- **Dependencias:** se declara `requests`, utilizada por la utilidad de auditoría local.
- **Pruebas:** se amplían las pruebas de autorización de Nuclei, corrupción del índice, validación CVE y acciones del motor de agentes. Se añadió un workflow de GitHub Actions para ejecutar la suite con Python 3.12.

- **IA desacoplada:** se añadió resolución de modelos por proveedor y por especialista en `llm_providers.py`. `agent_runner.py` usa esa resolución tanto para chat como para embeddings, sin cambiar el formato de memoria ni el Skillbook.
- **Configuración de proveedores:** un proveedor puede definir `models` por rol, `default_model` y `embedding_model`; las credenciales siguen llegando por variables de entorno.
- **Adaptadores de IA:** se integraron Ollama, OpenAI-compatible, Anthropic Messages (chat) y Google Gemini (chat y embeddings) detrás de un contrato normalizado.
- **Selección de modelos:** se puede mapear cada especialista a un modelo remoto o usar un modelo predeterminado del proveedor. Las claves se leen de variables de entorno.
- **Embeddings desacoplados:** ECO usa el proveedor seleccionado. Los vectores remotos se etiquetan como `proveedor::modelo` para no mezclar espacios; los vectores Ollama conservan su identificador histórico para compatibilidad.
- **Reindexación guiada:** `knowledge_reindex.py` ofrece inventario de solo lectura y migración explícita con `--apply --confirm`. Verifica integridad de cada fragmento, crea backup SQLite, genera en staging y publica los nuevos vectores en una transacción.
- **Integración de historial:** el registro de uso conserva proveedor y modelo efectivos. Los proveedores remotos ya no intentan comprobar sus modelos contra el catálogo local de Ollama.
- **Embeddings individuales:** la CLI envía una lista de un solo elemento al adaptador, registra el espacio vectorial y valida que el proveedor devuelva exactamente un vector.
- **Normalización Anthropic:** los mensajes de sistema múltiples se concatenan con saltos de línea reales.
- **Pruebas de adaptadores y reindexación:** se añadieron pruebas para selección y cambio de proveedor, respuestas normalizadas de Anthropic/Gemini, credenciales, historial local/remoto, embeddings individuales y reindexación SQLite de extremo a extremo con verificación de recuperación semántica.
- **CI:** el workflow cancela ejecuciones antiguas de la misma rama para evitar que cada commit deje una cola de pruebas obsoletas.
- **Documentación:** `docs/AI_PROVIDER_ARCHITECTURE.md` y `docs/AI_PROVIDER_CONFIGURATION.md` describen configuración, protocolos, credenciales y límites.

## Cómo validar

Desde la raíz del proyecto, con las dependencias instaladas:

```bash
python -m pip install -r requirements.txt
python cyber_ai.py --self-test
```

Para un escaneo Nuclei, además de indicar una URL dentro del alcance autorizado, hay que confirmar explícitamente:

```bash
python cyber_ai.py --scan https://objetivo-autorizado.example --confirm-authorized
```

No se debe ejecutar un escaneo contra sistemas de terceros sin permiso verificable.

## Pendiente

1. Ejecutar la suite completa en un entorno Python 3.12 y registrar los resultados reales, incluidas las nuevas pruebas de proveedores.
2. Revisar todas las rutas de ejecución de herramientas para aplicar un modelo uniforme de autorización y alcance.
3. Revisar concurrencia y recuperación del índice de informes.
4. Completar auditoría de secretos, validación de entradas y manejo de errores en los módulos restantes.
5. Añadir adaptadores nativos para otros proveedores y mejorar el descubrimiento/diagnóstico de capacidades.
6. Probar la reindexación completa con una base SQLite de laboratorio y validar recuperación ante interrupciones. La implementación tiene staging y publicación transaccional, pero aún requiere validación de extremo a extremo.
7. Unificar la administración/descarga de modelos remotos y locales; hoy el flujo de inferencia está desacoplado, pero la administración de modelos sigue centrada en Ollama.
8. Ejecutar el diff completo y abrir un Pull Request para revisión antes de integrar en `main`.

## Limitaciones de esta entrega

Los archivos se modificaron mediante GitHub. No se dispuso de un entorno de ejecución local del repositorio. GitHub Actions sí inició la suite de Python 3.12 para los commits recientes, pero la ejecución más nueva aún no ha publicado un resultado final; por tanto, **las pruebas siguen pendientes de confirmación y no se afirma que estén pasando**. Los cambios deben considerarse una primera corrección revisable, no una auditoría completa ni una certificación de seguridad.


## Ampliación de herramientas y conocimientos (2026-11-12)

- Catálogo declarativo ampliado a 20 herramientas: SAST, dependencias, SBOM/supply chain, IaC, secretos, contenedores, CI/CD, Kubernetes, malware, análisis forense y red.
- Nuevo `tool_registry.py`: selección explicable de herramientas candidatas por tarea.
- `task_planner.py` incorpora las herramientas candidatas al plan, sin ejecutarlas.
- Atlas de conocimiento v1.1.0: 28 áreas y 98 referencias registradas; 44 referencias nuevas. Áreas nuevas: ingeniería de software, aprendizaje automático, hardware/firmware y matemáticas.
- Las referencias permanecen pendientes de revisión de licencia y descarga; no se afirma que estén ingeridas.
- Pruebas nuevas: integridad del catálogo, inventario de herramientas y selección segura.
- Documentación: `docs/TOOL_ECOSYSTEM.md` y actualización de `docs/CYBERSECURITY_KNOWLEDGE_ATLAS.md`.

Límite explícito: las herramientas nuevas se detectan y recomiendan; salvo los adaptadores que ya existían, todavía no se ejecutan desde CYBER_AI. La siguiente fase es implementar adaptadores seguros y tipados, uno por uno.
