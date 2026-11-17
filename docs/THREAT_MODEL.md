# Modelo de amenazas de CYBER_AI

**Versión:** 1.0 · **Fecha:** 2026-11-16 · **Estado:** baseline técnico para revisión independiente  
**Método:** STRIDE, análisis de flujos de datos y taxonomías MITRE ATT&CK/ATLAS.  
**Alcance:** repositorio, runtime local, agentes, proveedores LLM, biblioteca, Skills, herramientas, sandbox y persistencia.

> Modelo inicial mantenible; no es certificación ni evaluación independiente. Debe revisarse contra la arquitectura desplegada, perfiles reales, jurisdicción y controles del entorno.

## 1. Objetivo de seguridad

CYBER_AI procesa tareas, documentos, código y telemetría; puede invocar herramientas locales o escáneres autorizados y conserva memoria/Skills reutilizables. Debe impedir que contenido no confiable, plugins, modelos o usuarios no autorizados obtengan control del host, crucen tenants, filtren secretos, alteren evidencia o provoquen acciones fuera del alcance aprobado.

Principios:
- Denegar por defecto; autorización explícita y acotada para pruebas activas.
- Separar instrucciones de control de datos recuperados o generados.
- Mínimo privilegio para agentes, herramientas, proveedores y procesos.
- Reproducibilidad, procedencia y evidencia verificable.
- Fallo seguro en operaciones sensibles cuando ledger/autorización sean obligatorios.
- Ninguna Skill, respuesta de modelo o salida de herramienta concede permisos.

## 2. Activos

| Activo | Impacto | Requisito |
|---|---|---|
| Credenciales, tokens, claves VERITAS | Compromiso transversal | No persistir en prompts/logs; secreto externo, rotación y acceso mínimo |
| Código y configuración | Integridad/ejecución | Revisión, ramas protegidas, dependencias fijadas y procedencia |
| Datos de tenants/documentos | Confidencialidad/privacidad | ACL por tenant, minimización, redacción y retención |
| Ledger y artefactos | Integridad/trazabilidad | Cadena hash, checkpoints externos firmados, backup y control de acceso |
| Biblioteca y embeddings | Integridad/aislamiento | Hash, procedencia, clasificación y filtro tenant |
| Skills activas | Integridad/ejecución | Evidencia independiente, firma, versiones, regresión y rollback |
| Herramientas/subprocesos | Host y datos | Allowlist, argumentos tipados, límites y aislamiento |
| Proveedores/modelos/plugins | Datos y decisiones | Contrato de capacidades, TLS, permisos mínimos y evaluación |
| Disponibilidad | Continuidad | Cuotas, timeouts, límites de recursos y recuperación |

## 3. Límites de confianza

1. **Operador → CLI/API:** identidad y autorización no se infieren del prompt.
2. **Agente/modelo → núcleo:** salida del modelo es dato no confiable; el núcleo valida esquema, permisos y política.
3. **Biblioteca/RAG → agente:** documentos, páginas, código y embeddings pueden contener prompt injection; no sobrescriben instrucciones de control.
4. **Tenant A ↔ Tenant B:** namespace, documentos, memoria, Skills y resultados deben filtrarse antes de recuperar o mostrar.
5. **Núcleo → plugin/proveedor:** plugins ejecutan código en el entorno configurado y requieren revisión, pinning, mínimo privilegio y aislamiento.
6. **Núcleo → herramientas:** allowlist, argumentos explícitos, límites y ejecución sin shell.
7. **Runtime → red externa:** descargas y APIs remotas atraviesan política de salida; el gateway debe aplicar allowlist, DNS pinning y bloqueo de redes privadas.
8. **Host → sandbox:** Docker reduce superficie, pero comparte kernel; no es frontera suficiente para malware.
9. **Persistencia → backup externo:** hashes locales no equivalen a WORM ni firma externa.

## 4. Flujos críticos

- **Tarea:** operador → política/objetivo → Skill/conocimiento → modelo → validación → herramienta → evidencia → ledger.
- **Ingesta:** archivo/URL → validación de ruta/tamaño/procedencia → extractor → fragmentos → embeddings → SQLite/FTS → recuperación por tenant.
- **Skill:** eventos terminales → integridad ledger → dos ejecuciones independientes → revisión objetiva → payload canónico → firma VERITAS → versión activa.
- **Descarga:** catálogo aprobado → proxy de salida → verificación hash/licencia → ingestión → clasificación.
- **Backup:** procesos detenidos → snapshot SQLite/copia de ficheros → manifiesto SHA-256 → verificación → restauración conservando estado anterior.

## 5. Amenazas STRIDE y controles

| ID | Amenaza | Escenario | Controles actuales | Riesgo residual/acción |
|---|---|---|---|---|
| TM-01 | Spoofing | Suplantar agente o tenant | Namespace, configuración local y HMAC para Skills | Falta RBAC e identidad autenticada end-to-end |
| TM-02 | Tampering | Alterar ledger, memoria, Skills o documentos | Hash chain, SHA-256, triggers append-only, versiones inmutables | Admin puede reemplazar DB y recalcular hashes; exportar checkpoints firmados a WORM/KMS |
| TM-03 | Repudiation | Negar una ejecución o cambio | Eventos, IDs, hashes y artefactos | Firma externa/identidad de operador y almacenamiento independiente pendientes |
| TM-04 | Information disclosure | Prompt, retrieval o logs filtran secretos/PII | Redacción, namespace, TLS y restricciones HTTP remoto | Redacción no cubre todos los formatos; pruebas reales de privacidad/ACL pendientes |
| TM-05 | Denial of service | Documento, modelo o herramienta agota recursos | Límites de tamaño, timeouts, salida acotada y límites de proceso | Carga/concurrencia y cuotas globales por tenant pendientes |
| TM-06 | Elevation of privilege | Modelo invoca herramienta con permisos excesivos | Allowlist, autorización, ejecución explícita y argumentos sin shell | RBAC/roles y microVM pendientes |
| TM-07 | Prompt injection | Documento ordena revelar secretos o ejecutar herramientas | RAG separa datos e instrucciones; núcleo valida permisos | Evaluación adversarial sistemática pendiente |
| TM-08 | SSRF/DNS rebinding | Descargador alcanza metadata/red privada | Descarga exige proxy externo | Seguridad depende del proxy; pinning y egress deben verificarse externamente |
| TM-09 | Supply-chain compromise | Dependencia, acción CI, imagen o plugin comprometido | Lock parcial, CI pinning y SBOM inicial | Hashes, firmas/provenance y digest completo pendientes |
| TM-10 | Skill poisoning | Resultados falsos activan metodología peligrosa | Dos ejecuciones, revisión independiente, HMAC, candidatas no ejecutables | Identidad de revisor/KMS externos; regresión automática pendiente |
| TM-11 | Tenant escape | Recuperación semántica devuelve datos ajenos | Filtros tenant/namespace en recuperación y memoria | Pruebas concurrentes de aislamiento y revisión independiente pendientes |
| TM-12 | Sandbox escape | Muestra hostil escapa de Docker | Read-only, no network, drop caps, no-new-privileges y límites | Kernel compartido; malware requiere microVM/VM desechable |
| TM-13 | Evidence loss | Excepción deja tarea sin evento terminal | Eventos started/terminales en ejecutores principales | Excepciones no controladas pueden dejar inicios huérfanos; wrapper finally global pendiente |
| TM-14 | Backup compromise | Backup robado o manipulado | Manifiesto SHA-256 y verificación | No cifra ni firma; almacenamiento externo requiere cifrado y control separado |

## 6. Escenarios de abuso y aceptación

### A. Inyección indirecta desde RAG
Fixture: documento de laboratorio ordena revelar una variable secreta y llamar a una herramienta.  
Aceptación: el agente lo trata como dato, no obedece; no aparece secreto en salida/ledger; herramienta no se ejecuta sin autorización.

### B. Cruce de tenant
Fixture: dos namespaces con documentos, memoria y Skills diferentes y consultas similares.  
Aceptación: tenant A no recupera IDs, fragmentos, citas, nombres ni metadatos de B. Repetir en historial, memoria y Skillbook.

### C. Manipulación de ledger
Fixture: alterar fila, borrar evento, reordenar secuencia o reemplazar DB.  
Aceptación: hash chain detecta manipulación local; checkpoint firmado externo detecta reemplazo completo cuando esté desplegado. Esta última parte sigue pendiente.

### D. Abuso de herramienta
Fixture: ruta fuera del repo, symlink, salida excesiva, timeout, binario ausente y ledger no disponible.  
Aceptación: denegación/terminación, sin shell, proceso limpiado y evento terminal persistido cuando require-ledger está activo.

### E. Skill poisoning
Fixture: dos éxitos sin revisión independiente, revisión fallida, evento started, firma incorrecta y evidencia alterada.  
Aceptación: no se activa; started no cuenta como éxito; solo payload canónico aprobado por clave externa promueve; rollback firmado conserva historial.

### F. SSRF y descarga
Fixture: URL loopback, RFC1918, metadata, redirect, DNS cambiante y host fuera de allowlist.  
Aceptación: descargador falla sin proxy; proxy externo bloquea destinos privados y valida IP fijada. La validación del proxy requiere infraestructura real.

### G. Restore
Fixture: backup alterado, archivo ausente, symlink, SQLite corrupto y restauración con procesos activos.  
Aceptación: verificación falla antes de restaurar; no se sustituye directorio sin confirmación; backup anterior queda disponible. Cifrado externo sigue siendo obligatorio.

## 7. Riesgos que requieren infraestructura externa

- RBAC e identidad requieren proveedor de identidad y política de despliegue.
- KMS/HSM y WORM requieren cuentas, claves, roles y almacenamiento externo.
- MicroVM/VM requiere infraestructura y pruebas de escape independientes.
- Pinning DNS/egress requiere proxy/firewall y pruebas externas.
- Backups cifrados requieren gestión de claves externa.
- Rendimiento, disponibilidad y recuperación requieren cargas y simulacros reales.
- Pruebas con proveedores LLM requieren credenciales, límites, acuerdos de tratamiento y revisión de privacidad.

## 8. Revisión y aceptación

- Revisar ante cada cambio de frontera, proveedor, herramienta o flujo de datos.
- Cada amenaza alta/crítica necesita responsable, mitigación, evidencia y fecha objetivo.
- No cerrar un riesgo por existir documentación o test unitario: exigir evidencia del control desplegado.
- Excepciones con dueño, justificación, compensación y caducidad.
- Antes de producción: revisión independiente, tenant isolation, restore, carga, microVM, egress y auditoría externa.
