# Estado real y plan de cierre de CYBER_AI

**Actualizado:** 2026-11-13  
**Rama:** `codex/security-integrity-audit`  
**Base:** `main` (sin merge ni despliegue)

## Verificación de CI

En el commit `6985d5b11a0d79c32ac46c76e6fe46878283a482` se confirmaron:
- Python tests: éxito.
- Docker sandbox: éxito; imagen construida, suite unitaria y smoke test de Ruff dentro del contenedor.

Esto valida los workflows de ese commit, no certifica seguridad institucional ni aislamiento frente a malware.

## Capacidades ya implementadas

- Inventario de 20 herramientas, selección explicable y adaptadores parciales.
- Sandbox Docker endurecido, limitado a Ruff y Bandit en la imagen actual.
- Atlas de 28 áreas y 98 referencias catalogadas.
- Biblioteca SQLite con fragmentos comprimidos, SHA-256, metadatos, separación shared/tenant y búsqueda semántica.
- Ingestión de TXT/Markdown, registro de recursos/versiones, descubrimiento local, catálogo y downloader con controles de adquisición.
- Reindexación con staging, backup y publicación transaccional.
- Proveedores Ollama, OpenAI-compatible, Anthropic chat y Gemini chat/embeddings.
- Skillbook persistente con aprobación de VERITAS, metodología, prerequisitos, validación, evidencias y búsqueda.
- Memoria de lecciones verificadas con aislamiento por namespace e inyección de contexto al agente.

## Brechas que siguen abiertas

1. **Adquisición de conocimiento:** el catálogo contiene referencias, no un corpus completo. Licencias y procedencia deben revisarse por recurso; la descarga está deshabilitada por defecto.
2. **Formatos:** la ingestión operativa directa admite TXT/Markdown. PDF, HTML, Office, código y datasets necesitan extracción especializada, análisis de contenido y pruebas.
3. **Recuperación:** la búsqueda vectorial actual recorre candidatos SQLite; no es un índice ANN/FTS híbrido adecuado para corpus grande. Faltan evaluación de relevancia, deduplicación y citas de fragmento obligatorias en cada respuesta.
4. **Skills:** existen Skills verificadas y reutilización contextual, pero la promoción sigue siendo explícita/manual. Los contadores de éxito no deben ser autodeclarados por el modelo; falta vincularlos a ejecuciones firmadas/inmutables, resultados y validadores independientes.
5. **Aprendizaje:** la memoria conserva lecciones verificadas; falta un registro estructurado de cada ejecución, fallos, costes, duración, modelo, herramienta, entorno y outcome con retención y controles de privacidad.
6. **Herramientas:** 20 están catalogadas; solo una fracción tiene adaptador. Faltan adaptadores, imágenes fijadas, SBOM, hashes de dependencias y pruebas de aislamiento por herramienta.
7. **Sandbox:** Docker comparte kernel. Para muestras hostiles se requiere microVM/VM desechable bajo infraestructura que garantice aislamiento.
8. **Proveedores IA:** el contrato es extensible, pero no cubre automáticamente cualquier proveedor; Anthropic no aporta embeddings en este adaptador y la administración de modelos sigue centrada en Ollama.
9. **Operación institucional:** faltan threat model formal, revisión de licencias, políticas de retención, redacción de datos, control de acceso por rol, auditoría de cambios y pruebas de recuperación/backup.

## Criterio de cierre

No declarar CYBER_AI terminado ni certificado hasta que cada brecha tenga implementación, pruebas, evidencia reproducible y revisión independiente. No promover automáticamente una Skill por una respuesta plausible: exige ejecuciones independientes, validadores deterministas, trazabilidad y aprobación humana/VERITAS.
