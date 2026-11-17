# Matriz de cierre verificable — CYBER_AI

Esta matriz separa implementación, verificación automatizada y validación operacional. Una capacidad no se considera cerrada solo por existir en el código.

## Reglas de estado

- **Implementado:** código y pruebas versionados.
- **CI aprobado:** workflows verdes sobre el SHA exacto que contiene el cambio.
- **Operacional pendiente:** requiere host, proveedor, credenciales, red, infraestructura o revisión humana.
- **Bloqueado por decisión:** requiere autorización del propietario o una política organizacional.

## Integración del flujo principal

| Área | Estado | Evidencia / criterio de aceptación |
|---|---|---|
| Entrada principal → DIRECTOR → agente → Skills/memoria/conocimiento | Implementación añadida; CI pendiente | `cyber_ai.py --ask` delega en `director.py`; DIRECTOR enruta la tarea y activa `agent_runner.py --knowledge` por defecto. La entrada principal ofrece `--no-knowledge` como exclusión explícita. `cyber_ai.py --team` delega en `team_orchestrator.py` con supervisión de objetivos; el orquestador genera y adjunta al informe un plan de capacidades y herramientas candidatas, y recupera conocimiento por defecto en las etapas y revisiones, con exclusión por configuración explícita. El plan no ejecuta herramientas. El runner recupera Skills y lecciones aprobadas y, cuando ECO/embeddings están configurados, fragmentos de la biblioteca. `--no-knowledge` permite desactivar explícitamente la recuperación. Tests de enrutamiento añadidos; falta CI sobre el HEAD y prueba local con proveedor/índice reales. La ejecución local es opt-in, exige confirmación y allowlist HMAC, y no habilita escaneo remoto. |

| Escaneo remoto autorizado → Nuclei → evidencia común → validador → ledger | Implementación añadida; CI pendiente | `nuclei_scanner.py` normaliza el contrato `cyber-ai.remote-scan.v1`, conserva el ID de autorización y del evento de ledger, rechaza salida JSONL malformada, exige estado/código de salida correctos y comprueba que cada `matched-at` permanezca en el origen autorizado. La validación estructural no certifica veracidad ni explotabilidad. Sigue siendo una ruta explícita y separada: no se activa desde el planificador multiagente ni hereda permisos de herramientas locales. |\n| Orquestador → planificador → adaptadores locales → evidencia → validador → ledger → agentes | Implementación añadida; CI pendiente | `--team --execute-tools --confirm-tool-execution --tool-target` ejecuta hasta tres adaptadores locales elegibles; exige allowlist HMAC, limita el objetivo al repositorio, guarda evidencia estructurada y referencia eventos del ledger. El validador independiente rechaza hashes inconsistentes, binarios/objetivos modificados, salida truncada, código distinto de cero o allowlist no aplicada. Los resultados se incluyen en el contexto de los agentes y en el informe final. No valida la veracidad del hallazgo ni impone aislamiento de red del host. |

## Brechas que admiten trabajo en el repositorio

| Área | Estado | Evidencia / criterio de aceptación |
|---|---|---|
| Regresión de Skills | Implementada; CI aprobado en SHA `5e2e85c` | `skill_regression.py` evalúa Recall@K, Precision@K, MRR@K y hit rate; verifica hash-chain y estado activo de cada Skill esperada; no altera contadores de uso. Suite Python de 456 pruebas aprobada en el SHA exacto. Falta dataset curado con Skills reales y umbrales aprobados por dominio. |
| Dependencias reproducibles | Parcial | `requirements.lock` fija versiones; CI calcula hashes de wheels y los publica en SBOM por plataforma. Falta lock con `--require-hashes` y hashes oficiales verificados para cada plataforma/arquitectura soportada. No inventar hashes. |
| Procedencia e integridad de herramientas | Parcial; allowlist HMAC implementada | Se registra ruta, versión y SHA-256 antes/después; `tool_allowlist.py` valida manifiesto HMAC y SHA-256 aprobado antes de ejecutar cuando se configura. `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1` fuerza modo fail-closed. Falta enrolamiento confiable, custodia/rotación externa de clave, mitigación TOCTOU mediante artefactos inmutables y CI del HEAD actual. |
| Permisos Windows | Pendiente; smoke test de allowlist añadido | El workflow ejecuta pruebas de lectura/validación de allowlist en `windows-latest`; esto no verifica ACL de datos, secretos ni evidencias. Los controles POSIX 0700/0600 no prueban ACL Windows. Falta aplicar y verificar DACL mediante APIs nativas y runner Windows. |
| Resiliencia del almacenamiento | Parcial | Hay pruebas de transacciones, bloqueo, corrupción lógica y crash de proceso simulado. Faltan pruebas de estrés prolongado, disco lleno, terminación del host y recuperación desde almacenamiento real. |
| Evaluación de conocimiento | Parcial; entradas endurecidas y CI aprobado en SHA `5e2e85c` | El benchmark valida JSONL y listas en memoria, normaliza IDs/categorías, limita recursos, valida vectores finitos y forma de resultados; mide Recall@K, Precision@K y MRR@K. Falta corpus etiquetado revisado por expertos, embeddings reales y umbrales de aceptación por área. |
| Extracción documental | Parcial | Extracción de formatos soportados con límites y marcadores de página PDF. OCR y ejecución aislada de parsers no están integrados. |
| Integración de proveedores | Parcial | Adaptadores y tests simulados. Faltan pruebas con cuentas reales, cuotas, latencia, errores, costes y políticas de datos de cada proveedor. |

## Validación externa u operativa

| Área | Evidencia necesaria | Responsable |
|---|---|---|
| Secretos y claves | KMS/HSM/gestor externo, rotación, revocación, recuperación y segregación de funciones probadas | Propietario/operaciones |
| Identidad y acceso | RBAC, IdP, MFA, roles y auditoría de acceso demostrados | Propietario/seguridad |
| Integridad externa | Checkpoints fuera del host y almacenamiento WORM/offsite administrado independientemente | Operaciones |
| Backups y DR | Cifrado, claves independientes, restauración, RPO/RTO y simulacro de pérdida de host | Operaciones |
| Aislamiento | MicroVM/VM desechable y pruebas de escape; Docker no sustituye una frontera de VM | Plataforma/seguridad |
| Calidad del conocimiento | Licencia, procedencia, vigencia y exactitud revisadas para cada fuente externa | Especialistas |
| Producción | Carga, soak, alertas, observabilidad, respuesta a incidentes y aceptación de riesgos | Propietario |
| Release | Revisión independiente, protección de rama, required checks, licencia y autorización de publicación | Propietario |

## Validación reciente de código

- SHA histórico exacto: `5e2e85cec0c2f4cb3627e87617be0c244f83cd27`; no valida el HEAD actual de `main` (`18aa78dfc33dab5b14523dd2d653eba1abc45f78`).
- Python tests: [success, 456 pruebas](https://github.com/Xero-29/CYBER_AI/actions/runs/44111423059).
- Docker sandbox: [success](https://github.com/Xero-29/CYBER_AI/actions/runs/44111420579).
- Estos resultados no validan commits posteriores ni sustituyen pruebas operacionales externas. El workflow Python ahora incluye un smoke test Windows de la allowlist y el workflow Docker se ejecuta también en pushes a `main`; los resultados de ambos workflows sobre el HEAD actual siguen sin estar disponibles.

## Evidencia por commit

Toda afirmación de CI debe indicar SHA completo y enlace a cada workflow. Si el HEAD cambia, la evidencia del commit anterior no valida el nuevo HEAD. Los estados **pendiente**, **en curso** o sin ejecución asociada nunca se describen como aprobados.

## Protocolo de cierre

1. Identificar una brecha y su criterio de aceptación.
2. Implementar el cambio en la rama autorizada por el propietario. En esta etapa, el alcance solicitado incluye directamente `main`; conservar el respaldo previo y registrar cada cambio.
3. Añadir pruebas negativas, límites y regresiones.
4. Ejecutar CI sobre el SHA resultante.
5. Inspeccionar fallos y corregirlos; repetir hasta obtener evidencia verde.
6. Actualizar esta matriz y `PROJECT_STATUS.md` con SHA, enlaces y límites residuales.
7. Si requiere infraestructura externa, dejarlo como pendiente operativo con evidencia concreta requerida.


## Matriz transversal de dominios

| Criterio | Estado | Evidencia / límite |
|---|---|---|
| 48 paquetes offline ↔ 48 perfiles | Implementado en código; CI pendiente | `domain_capability_matrix.py` compara IDs exactos contra `knowledge/packs/manifest.json`; prueba de integridad de cobertura añadida. |
| Dominio ↔ herramientas candidatas | Implementado en código; CI pendiente | Cada perfil declara IDs del catálogo; el plan informa disponibilidad, adaptador y estado de integración. La selección no autoriza ni ejecuta. |
| Dominio ↔ Skills activas | Integrado en planificación; CI pendiente | Se consultan Skills activas por tarea/dominio sin modificar contadores; solo se sugieren, no se promueven. |
| Cobertura operativa de las 48 áreas | Pendiente | Los perfiles de enrutamiento no sustituyen herramientas específicas, corpus experto, laboratorios, pruebas ni aceptación de resultados por dominio. |
