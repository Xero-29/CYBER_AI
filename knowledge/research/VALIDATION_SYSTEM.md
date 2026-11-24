# Sistema de validación de investigación

## Qué se integró

El repositorio ya disponía de ingestión documental, biblioteca indexada, registro de recursos/versiones, auditoría de procedencia/licencias, búsqueda, grafo de evidencia y motor de experimentos. Esta ampliación conecta esas piezas con una cola explícita de validación para los 192 módulos avanzados.

## Archivos

- \`VALIDATION_WORKLIST_192.json\`: 192 tareas (48 dominios × 4 temas), cada una enlazada a fuentes candidatas del mapa de dominio.
- \`CLAIM_EVIDENCE_REGISTER.json\`: registro de afirmaciones técnicas con localizador exacto, extracto de evidencia, tipo, revisor y estado. Empieza vacío deliberadamente.
- \`research_validation.py\`: auditor estructural y validador de registros de afirmaciones.
- \`tests/test_research_validation.py\`: pruebas de integridad, trazabilidad y puertas de validación.

## Uso

\`\`\`bash
python research_validation.py
python research_validation.py --json
python research_validation.py --strict
python -m unittest tests.test_research_validation -v
\`\`\`

El modo normal comprueba que la cola de 192 módulos y las fuentes candidatas estén completas. \`--strict\` falla mientras no existan afirmaciones respaldadas con evidencia admisible; no se debe usar como gate de CI inicial porque la revisión documental es un trabajo progresivo.

## Flujo por afirmación

1. Identificar una afirmación concreta y falsable dentro de un módulo.
2. Registrar la fuente realmente consultada, su ID del registro, versión y fecha.
3. Registrar página/sección/fragmento estable y un extracto breve suficiente para auditar el contexto.
4. Evaluar autoridad, vigencia, método, sesgos, alcance, contradicciones y limitaciones.
5. Registrar el revisor y fecha; no confundir resumen automático con lectura humana.
6. Si es una afirmación experimental, adjuntar el informe real, hashes, entorno, comandos, datos permitidos, métricas y resultados.
7. Solicitar revisión independiente antes de elevar a M5.

## Estados

- \`candidate\`: afirmación detectada, sin evaluar.
- \`needs_review\`: evidencia incompleta o ambigua.
- \`supported\`: evidencia admisible y revisada respalda la afirmación dentro de un alcance explícito.
- \`contradicted\`: evidencia admisible contradice la afirmación.
- \`inconclusive\`: evidencia insuficiente, conflicto no resuelto o resultado no concluyente.

Una fuente con estado \`official_*_reviewed\` en el registro actual solo indica revisión de ficha, versión, alcance o metadatos. No equivale a lectura integral. Para registrar una afirmación como respaldada por fuente documental, el registro exige estado \`full_text_reviewed\` o evidencia experimental asociada. La herramienta comprueba requisitos estructurales, no la semántica de la cita: un revisor debe confirmar que el extracto realmente respalda la afirmación.

## Límites y seguridad

- Las 95 referencias del registro de estudios de campo son fuentes candidatas; el mapeo temático no demuestra que respalden cada módulo.
- No se descargaron automáticamente documentos protegidos ni se modificaron licencias. El descargador existente mantiene su compuerta de licencia, proxy de salida seguro y verificación SHA-256.
- La ingestión existente extrae y fragmenta documentos; la indexación semántica depende del proveedor de embeddings configurado y de la política de datos.
- El motor de experimentos existente ejecuta únicamente pruebas dentro de \`tests/\`; un resultado pytest no es por sí mismo una conclusión de seguridad.
- Los laboratorios de ciberseguridad deben usar entornos aislados, datos sintéticos/autorizados y objetivos expresamente permitidos.
- Ningún estado de este sistema constituye certificación profesional o revisión por pares.

## Resultado inicial esperado

La auditoría debe reportar 48 dominios, 192 tareas y 92 fuentes, con 0 afirmaciones respaldadas y 0 fuentes marcadas como lectura integral hasta que exista evidencia real. Esto es intencional: el sistema hace visible el trabajo pendiente en vez de fabricar madurez.
