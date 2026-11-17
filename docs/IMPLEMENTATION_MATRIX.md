# Matriz de cierre verificable — CYBER_AI

Esta matriz separa implementación, verificación automatizada y validación operacional. Una capacidad no se considera cerrada solo por existir en el código.

## Reglas de estado

- **Implementado:** código y pruebas versionados.
- **CI aprobado:** workflows verdes sobre el SHA exacto que contiene el cambio.
- **Operacional pendiente:** requiere host, proveedor, credenciales, red, infraestructura o revisión humana.
- **Bloqueado por decisión:** requiere autorización del propietario o una política organizacional.

## Brechas que admiten trabajo en el repositorio

| Área | Estado | Evidencia / criterio de aceptación |
|---|---|---|
| Regresión de Skills | Implementada; CI aprobado en SHA `5e2e85c` | `skill_regression.py` evalúa Recall@K, Precision@K, MRR@K y hit rate; verifica hash-chain y estado activo de cada Skill esperada; no altera contadores de uso. Suite Python de 456 pruebas aprobada en el SHA exacto. Falta dataset curado con Skills reales y umbrales aprobados por dominio. |
| Dependencias reproducibles | Parcial | `requirements.lock` fija versiones; CI calcula hashes de wheels y los publica en SBOM por plataforma. Falta lock con `--require-hashes` y hashes oficiales verificados para cada plataforma/arquitectura soportada. No inventar hashes. |
| Procedencia e integridad de herramientas | Parcial; allowlist HMAC implementada | Se registra ruta, versión y SHA-256 antes/después; `tool_allowlist.py` valida manifiesto HMAC y SHA-256 aprobado antes de ejecutar cuando se configura. `CYBER_AI_TOOL_ALLOWLIST_REQUIRED=1` fuerza modo fail-closed. Falta enrolamiento confiable, custodia/rotación externa de clave y CI del HEAD actual. |
| Permisos Windows | Pendiente | Los controles POSIX verifican 0700/0600; Windows requiere comprobación y configuración de ACL mediante APIs nativas y pruebas en runner Windows. No presentar mode bits como verificación ACL. |
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

- SHA exacto: `5e2e85cec0c2f4cb3627e87617be0c244f83cd27`.
- Python tests: [success, 456 pruebas](https://github.com/Xero-29/CYBER_AI/actions/runs/44111423059).
- Docker sandbox: [success](https://github.com/Xero-29/CYBER_AI/actions/runs/44111420579).
- Estos resultados no validan commits posteriores ni sustituyen pruebas operacionales externas.

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
