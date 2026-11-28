# Matriz de cierre verificable — CYBER_AI

Esta matriz separa implementación en código, verificación automatizada y validación operacional. Una capacidad no se considera cerrada solo por existir en el código o en documentación.

## Reglas de estado

- **Implementado:** código y pruebas versionados.
- **CI aprobado:** workflows verdes sobre el SHA exacto que contiene el cambio.
- **Operacional pendiente:** requiere host, proveedor, credenciales, red, infraestructura o revisión humana.
- **Bloqueado por decisión:** requiere autorización del propietario o una política organizacional.

## Brechas que admiten trabajo en el repositorio

| Área | Estado | Evidencia / criterio de aceptación |
|---|---|---|
| Autorización de objetivos | Implementada en el núcleo; cobertura operativa parcial | `execution_policy.py` valida IP literal, destino exacto, acción, ID de autorización, expiración y política local protegida. Nuclei y el runner de tareas revalidan antes/durante la ejecución. Los hostnames se rechazan hasta disponer de transporte con DNS fijado; no se debe inferir que todos los adaptadores de red usan esta política. RBAC/IdP siguen externos. |
| Allowlist e integridad de herramientas | Parcialmente implementadas | `tool_allowlist.py` valida manifiestos HMAC privados; `binary_integrity.py` calcula hashes antes/después y `require_approved_executable` bloquea binarios no aprobados en flujos que lo invocan (Nuclei/runner). No existe todavía un broker universal que obligue a todos los adaptadores a pasar por esa frontera. Enrolamiento, custodia/rotación de claves y ACL Windows requieren trabajo adicional. |
| Aislamiento de procesos | Parcial | `process_isolation.py` usa grupo POSIX, entorno explícito, timeout y captura acotada; declara `process_tree_isolation_enforced=false`. Docker sin red se aplica a herramientas concretas de CI (Ruff/Bandit), no a todos los adaptadores host. Faltan cgroups/cuotas, Job Objects de Windows y microVM/VM para cargas hostiles. |
| Dependencias reproducibles | Parcial, con hashes obligatorios en CI Linux | `requirements.lock`, `sandbox/requirements.lock` y `requirements-documents.lock` fijan versiones y SHA-256 para Linux x86_64 / CPython 3.12. CI instala con `--require-hashes`, vuelve a descargar wheels, calcula manifiestos de artefactos y genera SBOM CycloneDX/provenance. No equivale a locks verificados para todas las arquitecturas, sistemas operativos y versiones Python soportadas. |
| Permisos Windows | Pendiente | Se detectan puntos de reanálisis, pero los controles POSIX 0700/0600 no verifican ni configuran ACL NTFS. Se requieren APIs nativas y pruebas en runner Windows con identidades/ACL reales. |
| Backups y restauración local | Implementados con límites; DR parcial | `data_backup.py` usa manifiesto estricto, SHA-256 por archivo, firma HMAC opcional/obligatoria por defecto en CLI, límites de entradas/bytes, rechazo de enlaces, staging privado, fsync y publicación/restauración atómica; conserva el directorio anterior al reemplazo. La salida declara `encrypted=false`: no hay cifrado, KMS, WORM ni offsite. La quiescencia es una atestación del operador, no una detección automática de todos los escritores. |
| Resiliencia del almacenamiento | Parcial | Hay pruebas de transacciones, bloqueo, corrupción lógica, identidad de rutas y crash de proceso simulado. Faltan pruebas de estrés prolongado, disco lleno, terminación del host y recuperación desde almacenamiento real. |
| Ledger y trazabilidad | Parcial | Eventos y cadena hash local permiten auditar operaciones; redacción de secretos y eventos de inicio/terminal existen en flujos principales. Checkpoints externos firmados/WORM, identidad de operador, observabilidad central y cobertura global de excepciones siguen pendientes. |
| Evaluación de conocimiento | Parcial | El evaluador comprueba esquema, secciones, fuentes verificadas, evidencia de laboratorio y revisión independiente ligada a hashes. Las 48 áreas de esta rama no deben declararse expert-ready sin fuentes primarias, laboratorios reproducibles y revisiones confiables; el volumen documental no es criterio de aprobación. Falta corpus etiquetado por especialistas y umbrales por dominio. |
| Extracción documental | Parcial | Formatos soportados con límites y marcadores de página PDF. OCR y ejecución aislada de parsers no están integrados. |
| Integración de proveedores IA | Parcial | Adaptadores integrados/plugins, validación de capacidades, endpoints, payloads, respuestas, límites y transporte HTTP. Se añadieron regresiones para URL base ambigua y contrato Ollama. Faltan pruebas con cuentas reales, cuotas, latencia, errores, costes y políticas de datos de cada proveedor. Los plugins ejecutan código dentro del proceso Python y no están aislados por el núcleo. |

## Validación externa u operacional

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

## Evidencia histórica de CI

- SHA histórico: `5e2e85cec0c2f4cb3627e87617be0c244f83cd27`.
- Python tests: [success, 456 pruebas](https://github.com/Xero-29/CYBER_AI/actions/runs/44111423059).
- Docker sandbox: [success](https://github.com/Xero-29/CYBER_AI/actions/runs/44111420579).
- Estos resultados son históricos y no validan commits posteriores ni sustituyen pruebas operacionales externas.

## Evidencia por commit

Toda afirmación de CI debe indicar SHA completo y enlace a cada workflow. Si el HEAD cambia, la evidencia del commit anterior no valida el nuevo HEAD. Los estados **pendiente**, **en curso** o sin ejecución asociada nunca se describen como aprobados.

## Protocolo de cierre

1. Identificar una brecha y su criterio de aceptación.
2. Implementar el cambio en la rama de trabajo, sin modificar `main`.
3. Añadir pruebas negativas, límites y regresiones.
4. Ejecutar CI sobre el SHA resultante.
5. Inspeccionar fallos y corregirlos; repetir hasta obtener evidencia verde.
6. Actualizar esta matriz y `PROJECT_STATUS.md` con SHA, enlaces y límites residuales.
7. Si requiere infraestructura externa, dejarlo como pendiente operativo con evidencia concreta requerida.
