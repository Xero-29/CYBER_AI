# Estado vigente — 2026-11-23 (auditoría incremental)

> Estado de la rama de trabajo. La evidencia de CI siempre se vincula al SHA exacto; un resultado de otro commit no se reutiliza.

## Repositorio, ramas y PRs

- Repositorio: `Xero-29/CYBER_AI`; rama de trabajo: `codex/security-integrity-audit`.
- HEAD de código y pruebas antes de este registro: `fbc4e0df1ed57331245b9d434b90800cb9d1c270`. El commit de este registro es documental y vuelve a disparar CI.
- `main`: `658a565acd0a5568bb56a1a7482f44260cd9efd1`; ancestro común: `cae816d6037b56f017c2fbdbb3e98ef00df58c1d`.
- Comparación exacta antes de este registro: **351 commits exclusivos de la rama y 576 exclusivos de `main`**. El commit documental eleva la rama a 352 exclusivos; no hay base segura para merge/rebase directo.
- No existe un único commit exclusivo de `main` en el grafo completo: son 576 desde el ancestro común. La secuencia reciente que debe preservarse es `387104756d0f8307c39a46a1ea2df07671bd81c9` (bucle metacognitivo), `554ec1cdd45de3bb0e0f24156b0a9a8ac19193da` (perfil de modelos) y `658a565acd0a5568bb56a1a7482f44260cd9efd1` (perfil de hardware). No se copió ni descartó ninguno.
- PR #2 está **cerrado y fusionado**; merge commit `478c6ddc676221e4c07b8c5780f127bc5a9e749e`. No se crea PR duplicado.
- No hay PR abierto para esta rama. PR #17 sigue abierto; los runs asociados consultados son Python tests [44795901916](https://github.com/Xero-29/CYBER_AI/actions/runs/44795901916) y Docker sandbox [44795901820](https://github.com/Xero-29/CYBER_AI/actions/runs/44795901820), ambos success. PR #18 sigue abierto y apilado sobre #17, HEAD `888ac5863eea9554202f9dd66baf6024344e1200`; no se encontraron runs para ese HEAD. El último run conocido de #18 corresponde al SHA anterior `2ea257bdf75ce53905299e2571b8b5ea6d82b705`, no al actual.
- PR #11/#12 cubren locks/SBOM y reconciliación de activos; #13/#14/#18 cubren biblioteca. Se conservaron sin cambios. No se ejecutó merge, rebase, cherry-pick, force-push ni escritura en `main`.
- La protección de rama no pudo verificarse con los permisos/endpoints disponibles; no se afirma que esté configurada.

## Correcciones de seguridad y durabilidad

- `web_research.py`: consulta validada antes de cargar política o contactar proveedores; texto no vacío, máximo 1.000 caracteres, rechazo de controles C0/C1 antes de recortar espacios; `max_results` entero estricto 1–20; `include_untrusted` booleano real. URLs de resultados limitadas a 4.096 caracteres y sin controles.
- `load_sources()` ya no usa `Path.read_text()` sobre la política de confianza: lee con `safe_io.read_regular_file`, comprueba identidad/tipo, rechaza symlinks/puntos de reanálisis y hardlinks en POSIX, y limita el JSON a 1 MB.
- `safe_io.atomic_write_text()`: en POSIX publica el archivo con `os.replace` relativo a un descriptor de directorio verificado y sincroniza el directorio padre después de sincronizar el contenido. La publicación falla si no se puede confirmar la sincronización; Windows sigue sin ACL verificadas.
- Regresiones nuevas: consultas/URLs malformadas y grandes, controles C0/C1 al inicio/interior/final, política de confianza enlazada/FIFO/sobredimensionada y fsync del directorio con rename relativo a `dir_fd`.
- Documentación actualizada en `docs/WEB_RESEARCH_EGRESS.md` y `docs/SECURE_FILE_OUTPUTS.md`.
- Commits de código: [3577933](https://github.com/Xero-29/CYBER_AI/commit/357793381efd0410af2958a23a0b738417d539f8), [42d428b](https://github.com/Xero-29/CYBER_AI/commit/42d428bd843230c7d2b26ba9ced0987707ae35a6), [e3dae9d](https://github.com/Xero-29/CYBER_AI/commit/e3dae9dd94075de620cd834910a0f197083087b7), [9d7cf32](https://github.com/Xero-29/CYBER_AI/commit/9d7cf32d234c73357dc218c71b7bd63ed907b510), [c4e01f8](https://github.com/Xero-29/CYBER_AI/commit/c4e01f895d8d8f85933202913f8c7a28d5ba82d4), [5801af0](https://github.com/Xero-29/CYBER_AI/commit/5801af031d27331b7711683e7ea3bf7ed56ff310).
- Commits de regresiones: [ab50b81](https://github.com/Xero-29/CYBER_AI/commit/ab50b815280bfbc5b4783b8f34caed57d17ee814), [3280ef5](https://github.com/Xero-29/CYBER_AI/commit/3280ef5271c4b963e634d3417b83fb9ebf5f4eb1), [c3644dc](https://github.com/Xero-29/CYBER_AI/commit/c3644dc338cf820e2976abae8e3c2ae5df2e29bc), [a72c1bb](https://github.com/Xero-29/CYBER_AI/commit/a72c1bb170f7854b76d83fa571dac094356c463a), [9a50403](https://github.com/Xero-29/CYBER_AI/commit/9a5040372c857af0e2807b4bba60d1480884aeb1), [fbc4e0d](https://github.com/Xero-29/CYBER_AI/commit/fbc4e0df1ed57331245b9d434b90800cb9d1c270).
- Commits documentales: [8c940c9](https://github.com/Xero-29/CYBER_AI/commit/8c940c912692f7d6608efac174312a5c62867537), [c202572](https://github.com/Xero-29/CYBER_AI/commit/c202572d9c6317cd7aa8d58128c8034cf2c41435), [51a143e](https://github.com/Xero-29/CYBER_AI/commit/51a143e8a605fea4a96ed4298f4ab512e7115b15), [2b55510](https://github.com/Xero-29/CYBER_AI/commit/2b555106dd28421339baaea3c63671dde33c0724).

## CI, SBOM y evidencia exacta

- En el HEAD `fbc4e0df1ed57331245b9d434b90800cb9d1c270`, **Python tests** [45212327951](https://github.com/Xero-29/CYBER_AI/actions/runs/45212327951) terminó **success**; job `unit-tests`, **744 tests, 4 skipped**, incluyendo verificación de locks y generación de SBOM.
- En el mismo SHA, **Docker sandbox** [45212327718](https://github.com/Xero-29/CYBER_AI/actions/runs/45212327718) terminó **success**; job `sandbox-smoke`, **744 tests, 4 skipped**, Ruff terminó con código 0 y la evidencia se subió.
- SBOM/provenance artifact [14837780058](https://github.com/Xero-29/CYBER_AI/actions/runs/45212327951) contiene tres CycloneDX 1.5: core (9 componentes), sandbox (8) y documentos (9), sin PURLs duplicados en cada SBOM. Los tres manifiestos de artefactos enlazan hashes de wheels con sus respectivos locks; provenance identifica el commit `fbc4e0d` y el run `45212327951`.
- Evidencia sandbox artifact [14837475478](https://github.com/Xero-29/CYBER_AI/actions/runs/45212327718) contiene ledger SQLite (2 eventos start/completed enlazados por hash) y evidencia Ruff. El ejecutable Ruff figura aprobado por allowlist firmada. La evidencia del adaptador indica `network_isolation_enforced=false`; el workflow ejecutó el contenedor con `--network=none`, pero eso no demuestra aislamiento de red de procesos ejecutados directamente en el host.
- Este commit documental dispara nuevas ejecuciones; **no se atribuye success al SHA documental hasta consultar sus propios runs**.
- No hay checkout local de este repositorio en el entorno; no se afirma que se ejecutara `verify.sh` localmente.

## Pendiente real

- Verificar Python tests y Docker sandbox sobre el nuevo HEAD documental; revisar logs/artefactos de ese SHA.
- Reconciliar la divergencia únicamente en una rama separada con revisión de tres vías; preservar los 576 commits exclusivos de `main`, en particular `3871047`, `554ec1c` y `658a565`. No integrar directamente los 351/576 commits.
- La biblioteca sigue en **48 áreas, 0 expert_ready y 48 foundation_draft**. Faltan lectura de fuentes primarias, licencias verificadas, evidencia claim-to-source, laboratorios reproducibles, datasets expertos y revisión independiente firmada por canal confiable.
- Pendiente externo/operacional: gateway real con DNS pinning y egress controlado; Job Objects/ACL Windows y cgroups/namespaces o microVM; KMS/HSM, rotación y custodia; cifrado y backups WORM/offsite; RBAC/IdP/MFA; pruebas DR/RPO/RTO, carga y fallos físicos; proveedores reales y revisión disciplinar independiente.

**Conclusión:** el HEAD de código/pruebas `fbc4e0d` tiene Python y Docker CI exitosos y artefactos SBOM/evidencia revisados. El HEAD documental que genera este registro aún debe pasar sus propios checks. El proyecto no está listo para la validación final del usuario: quedan trabajo de ingeniería e integración que puede realizarse sin intervención externa. `main` permanece intacta.


# Estado de ingeniería y auditoría — 2026-11-21

**Repositorio:** \`Xero-29/CYBER_AI\`  
**Rama de trabajo:** \`codex/security-integrity-audit\`  
**HEAD de código antes de este registro:** \`dcfba05d15501cd597b012676d36ffec743bfe80\`  
**main verificado:** \`387104756d0f8307c39a46a1ea2df07671bd81c9\`  
**Ancestro común:** \`cae816d6037b56f017c2fbdbb3e98ef00df58c1d\`

## Estado de ramas e integración

- La comparación actual \`main...codex/security-integrity-audit\` está **divergida: 238 commits exclusivos de la rama y 574 exclusivos de main**. No es seguro integrar esta rama mediante un merge/rebase directo.
- Desde el corte anterior, \`main\` avanzó de \`9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea\` a \`387104756d0f8307c39a46a1ea2df07671bd81c9\` con un commit nuevo: **\`feat: add metacognitive research loop\`**. Añade \`metacognition.py\`, \`researcher_agent.py\`, \`director.py\`, \`config/model_roles.json\`, documentación y pruebas. Se conserva íntegro; no se ha copiado ni descartado.
- Hay **un commit nuevo de main desde la revisión anterior**, pero no un único commit exclusivo de main en el grafo completo: desde el ancestro común hay 574 commits exclusivos de main.
- La rama separada \`codex/reconcile-main-security-audit-2026-11-18\` (HEAD \`c2a397caf36f2661b6f0307168a0a24eee2f6d38\`) está 2 commits por delante y 1 por detrás de main, con base común \`9bab38f2092bcc46a0c1cf14eb3d79cdbba387ea\`. Es un port selectivo de activos, no una reconciliación completa de la rama de auditoría. No se fusionó.
- PR #2 está **cerrado y fusionado** desde el 2026-11-17; HEAD de aquel PR \`cae816d6037b56f017c2fbdbb3e98ef00df58c1d\`, merge commit \`478c6ddc676221e4c07b8c5780f127bc5a9e749e\`. No representa el HEAD actual.
- PR #11, #12, #13, #14, #16, #17 y #18 siguen abiertos en draft. #11/#12 cubren locks, SBOM y portabilidad selectiva; #13/#14 la biblioteca; #16 la línea base de conocimiento; #17 reconcilia #11/#12 y #18 reconcilia #13/#14. PR #18 usa #17 como base. No hay PR abierto asociado a la rama actual y no se creó uno duplicado.
- No se ejecutó merge, rebase, cherry-pick, force-push ni escritura en \`main\`. La integración requiere una rama separada, revisión de conflictos de tres vías y pruebas de regresión de ambos lados.

## Correcciones implementadas en este corte

- **Redacción de secretos:** \`secret_redaction.py\` reconoce valores entrecomillados con comillas escapadas y credenciales de URI con esquemas distintos de HTTP (por ejemplo, PostgreSQL). Las regresiones exigen JSON parseable y ausencia del valor secreto. Commits: [\`1a84813\`](https://github.com/Xero-29/CYBER_AI/commit/1a84813bfdfaacaea764576457c7ff42f8e25706), [\`8ba92e7\`](https://github.com/Xero-29/CYBER_AI/commit/8ba92e7d6c2d2812b9267d672ca8aaa49543ed1d).
- **Backups/restauración:** \`data_backup.py\` rechaza ancestros symlink/reparse, directorios no confiables o modificables por terceros (salvo padres sticky propiedad de root), y comprueba identidad de rutas de origen, snapshot y destino antes de publicar. Valida directorios reparse dentro del árbol, archivos regulares, estabilidad de origen y que el destino no aparezca durante la operación. Se añadieron regresiones para ancestros symlink, padres escribibles y restauración. Commits: [\`80d2d79\`](https://github.com/Xero-29/CYBER_AI/commit/80d2d798e4cf1e6f57131e47a7f92150baca8081), [\`09308dd\`](https://github.com/Xero-29/CYBER_AI/commit/09308ddef623438c63890ce06a179137636cfd94), [\`abc0bd0\`](https://github.com/Xero-29/CYBER_AI/commit/abc0bd0da6e3c3d2dba98bc916eb9670f0887c19).
- **Autorización de objetivos:** \`execution_policy.py\` exige que los directorios padre y ancestros del archivo de autorizaciones pertenezcan a root o al usuario efectivo; los permisos de escritura de grupo/otros siguen bloqueados salvo el caso sticky de root. \`nuclei_scanner.py\` revalida antes de lanzar, durante cada ciclo de supervisión y antes de aceptar resultados; \`task_runner.py\` revalida antes de lanzar y al finalizar, descartando resultados si el permiso caducó o fue revocado. Se añadieron regresiones de propiedad y revocación, y se actualizó la guía. Commits: [\`81d81e7\`](https://github.com/Xero-29/CYBER_AI/commit/81d81e71ee32f79c789ba46005b970a77f0f061e), [\`cef8f7a\`](https://github.com/Xero-29/CYBER_AI/commit/cef8f7ac63370b87d5f0678a1f6d3c768c5d03a0), [\`a44f2ae\`](https://github.com/Xero-29/CYBER_AI/commit/a44f2ae7dc8801819cc3d4d3057c7d1552343e85), [\`ac17137\`](https://github.com/Xero-29/CYBER_AI/commit/ac17137d580a3916d81b95581c642f27581f3fe8), [\`c76b6e1\`](https://github.com/Xero-29/CYBER_AI/commit/c76b6e103632a27018ec4894a577119cc5f28a33), [\`f9f0586\`](https://github.com/Xero-29/CYBER_AI/commit/f9f058656e4d4dc7bca035b91d8785f4373ac88e), [\`8ea23c1\`](https://github.com/Xero-29/CYBER_AI/commit/8ea23c1d1b5d8408a19b7d03175382b894770237), [\`a7a4964\`](https://github.com/Xero-29/CYBER_AI/commit/a7a496410429456304cec998fa5883649c59ac02), [\`3a0056e\`](https://github.com/Xero-29/CYBER_AI/commit/3a0056e3858f4573627eedb50935400a349ddbcc), [\`9cc586e\`](https://github.com/Xero-29/CYBER_AI/commit/9cc586e45dd3b3f2d585b6711e97187daaf57ce6), [\`dcfba05\`](https://github.com/Xero-29/CYBER_AI/commit/dcfba05d15501cd597b012676d36ffec743bfe80).
- **Ejecución de adaptadores:** las sondas de versión usan grupo de procesos POSIX, timeout de 5 s y salida máxima de 8 KiB; las herramientas trabajan desde un directorio temporal, no desde la raíz del repositorio. La evidencia valida la ruta antes de crearla, rechaza ancestros symlink y destinos externos no autorizados, y no cambia permisos de directorios existentes compartidos ni de la raíz del repositorio. Commits: [\`38b816d\`](https://github.com/Xero-29/CYBER_AI/commit/38b816d5d1e879447eb2dfd44797ba41af310d96), [\`b256b9a\`](https://github.com/Xero-29/CYBER_AI/commit/b256b9a4878bfe913072796d279516957588cb6e), [\`3440999\`](https://github.com/Xero-29/CYBER_AI/commit/34409998adcfeb6fa8d61826395720ee432f1a3e), [\`1350417\`](https://github.com/Xero-29/CYBER_AI/commit/1350417772a15b06a4d5ed2438e5cbc12ac1cc43), [\`c0d7f84\`](https://github.com/Xero-29/CYBER_AI/commit/c0d7f841a06e380b57ed6a46e5260a987a51f4f9), [\`44d81bb\`](https://github.com/Xero-29/CYBER_AI/commit/44d81bb6d7adc6b35cefdb36529b060daab59f68), [\`8018446\`](https://github.com/Xero-29/CYBER_AI/commit/801844631c1bcd88e8b3c02afd5a570133a37d0d), [\`21692dc\`](https://github.com/Xero-29/CYBER_AI/commit/21692dc2772e288dc53404c5d1e7b92b37e5ac1d), [\`196f501\`](https://github.com/Xero-29/CYBER_AI/commit/196f501e262ac40407791643e59dfbbc5763eabd), [\`a880157\`](https://github.com/Xero-29/CYBER_AI/commit/a880157a4d1caeeaf4a965c8f64dca6aa7e11710).
- **Aislamiento de procesos:** \`process_isolation.py\` valida tipos y contenido de argumentos, \`cwd\` y variables de entorno; limita la captura total a un máximo duro de 64 MiB. Se añadieron pruebas de entradas malformadas y de límites. Commits: [\`aed8f66\`](https://github.com/Xero-29/CYBER_AI/commit/aed8f661f1b03e54cbed3dde8376a56a89859187), [\`350d3ae\`](https://github.com/Xero-29/CYBER_AI/commit/350d3aeff2fdf613ba0649dd37411629894b40e9).

## CI y pruebas del HEAD exacto

- El último CI exitoso conocido sigue siendo el del SHA anterior \`4a19e2ffa04522de1aee03ad741d182f1478948d\`: Python Tests **641 aprobadas, 4 omitidas** (run [44766960784](https://github.com/Xero-29/CYBER_AI/actions/runs/44766960784)); Docker Sandbox **641 aprobadas, 4 omitidas y Ruff aislado** (run [44766960550](https://github.com/Xero-29/CYBER_AI/actions/runs/44766960550)).
- Esos runs **no validan** los commits nuevos de este corte. El HEAD actual al registrar este estado es \`dcfba05d15501cd597b012676d36ffec743bfe80\`.
- Python Tests está configurado para ejecutarse en cada push a cualquier rama; Docker Sandbox se ejecuta en push a \`codex/security-integrity-audit\`. Para el HEAD actual, la integración disponible no devuelve runs de push y los estados de commit consultables están vacíos. **No se declara CI verde** hasta obtener ambos checks terminados y exitosos para el SHA exacto.
- No hay checkout local del repositorio en este entorno; el intento de clonación no pudo completar el acceso de red. No se afirma que se haya ejecutado \`verify.sh\` localmente. La lógica de los controles nuevos se revisó de forma aislada, pero eso no sustituye la suite del proyecto.

## Límites de implementación que siguen abiertos

- Las correcciones nuevas de redacción, backup, autorización, adaptadores y proceso necesitan pasar la suite completa en CI. Las ACL de Windows todavía no se verifican.
- Las herramientas locales siguen ejecutándose en el host POSIX con HOME/TMP/cwd efímeros y grupo de procesos; esto **no** es sandbox de filesystem ni control de egress. Una herramienta comprometida puede acceder a otros archivos del usuario y a la red. No marcar como aislamiento completo.
- Windows: la ejecución de herramientas permanece cerrada hasta implementar y validar Job Objects.
- POSIX: el grupo de procesos no contiene descendientes que creen otra sesión/grupo. Para código hostil se requieren cgroups/namespaces o microVM; Docker comparte kernel.
- El aislamiento de red/egress de adaptadores host y Nuclei requiere políticas de firewall/gateway y pruebas reales. La autorización actual no autentica criptográficamente al aprobador ni verifica tickets externos.
- Backup local: se verifican hashes y se puede firmar con HMAC, pero no cifra ni equivale a WORM/offsite. Custodia de claves, cifrado, retención y recuperación DR requieren infraestructura externa.
- Ledger hash-chain local no es anclaje externo. KMS/HSM, RBAC/IdP/MFA, segregación de funciones y almacenamiento inmutable siguen pendientes.
- Proveedores LLM/embeddings necesitan pruebas contra servicios reales de política de datos, cuotas, latencia, coste, fallos y continuidad.
- Los 48 dominios de conocimiento no equivalen a validación científica. Las fuentes primarias, licencias, afirmaciones claim-to-source, laboratorios ejecutados y revisión experta siguen pendientes; los módulos no se consideran aprobados por estructura o volumen.

## Próxima secuencia de ingeniería

1. Obtener y verificar Python Tests y Docker Sandbox sobre el HEAD final exacto; revisar logs y corregir fallos antes de declarar verde.
2. Continuar auditoría estática de adaptadores, ejecución de herramientas, proveedores, almacenamiento, observabilidad y recuperación; añadir regresiones ante cada defecto reproducible.
3. Preparar la reconciliación en una rama separada, preservando explícitamente el commit \`3871047\` y los cambios de ambos lados. No integrar los 238/574 commits sin inventario de conflictos y validación.
4. Mantener bloqueadas las capacidades que dependen de Job Objects, cgroups/microVM, egress, KMS/HSM, RBAC, WORM/offsite, ACL Windows y proveedores reales hasta completar las pruebas externas.
5. Mantener la biblioteca en estado de borrador donde no haya referencias y evidencia verificables; no elevar madurez teórica ni operativa por documentación.

**Conclusión de este corte:** se corrigieron defectos reproducibles en redacción de secretos, rutas de backup, propiedad de la política de autorización, ejecución de sondas de herramientas, publicación de evidencia, límites de procesos y revocación de permisos de escaneo. La rama sigue divergida, el HEAD actual aún no tiene CI exacto verificable y la auditoría estática continúa. **No está lista para la validación final del usuario y no requiere intervención suya en este momento.**

---

## Registro histórico

Los bloques siguientes documentan estados y validaciones de iteraciones anteriores. Si alguna cifra, pendiente o afirmación contradice esta cabecera, prevalece el estado verificado de esta sección superior.

# Estado actual verificado — 2026-11-17

**HEAD verificado:** `b2477cff69e72b2576656b9e2b5ae4841547b667`  
**Rama:** `codex/security-integrity-audit`  
**Comparación con main:** 357 commits adelante, 0 detrás (comparación directa con el HEAD de main consultado).  
**CI de este HEAD:** Python tests — [success, 377 pruebas](https://github.com/Xero-29/CYBER_AI/actions/runs/43997370392); Docker sandbox — [success](https://github.com/Xero-29/CYBER_AI/actions/runs/43997363886).  
**PR #2:** abierto, en borrador; no fusionado. `main` no fue modificado.

## Cambio de seguridad de esta iteración

- `knowledge_audit.py` ahora rechaza rutas absolutas, traversal y symlinks en el manifiesto; no sigue directorios raíz symlink durante el inventario.
- Los manifiestos ausentes o inválidos producen diagnósticos en vez de interrumpir abruptamente la auditoría.
- La auditoría SQLite abre la base en modo solo lectura y devuelve un diagnóstico si el esquema no es válido.
- `tests/test_knowledge_audit.py` añade cobertura para rutas externas, symlinks de archivo/directorio, manifiestos inválidos y lectura SQLite.
- Validación de este cambio: 377 pruebas Python y Docker sandbox aprobados en el SHA exacto indicado arriba.

**Límite:** esto cierra una brecha del auditor local; no cierra las brechas institucionales de KMS/HSM, cifrado, WORM, RBAC, microVM, proveedores reales, evaluación experta de fuentes ni recuperación ante pérdida de host. Las secciones históricas siguientes documentan iteraciones anteriores; si contradicen este bloque, prevalece la evidencia del HEAD aquí indicado.

---

# Estado real y plan de cierre de CYBER_AI

**Actualizado:** 2026-11-17  
**Rama:** codex/security-integrity-audit
**CI:** Actions fijadas por SHA, checkout v5/setup-python v6/upload-artifact v5 (Node 24)  
**Base:** main (sin merge ni despliegue)

## Avance de esta iteración

## Recuperación transaccional del ledger — 2026-11-17

- `execution_ledger.py`: se incorpora el estado terminal `interrupted` y una reconciliación atómica de inicios sin evento terminal correlacionado por `metadata.start_event_id`.
- La reconciliación verifica la cadena hash completa dentro de la transacción antes de escribir. Si hay secuencias, enlaces o hashes inválidos, aborta sin añadir eventos.
- Los eventos recuperados declaran `outcome: unknown`; no se atribuye éxito ni fallo al trabajo que pudo quedar ejecutándose. Los IDs deterministas y la transacción evitan cierres duplicados o carreras entre reconciliadores.
- CLI: `python ledger_cli.py reconcile --confirm-no-active-runs` (opcional `--namespace NOMBRE` y `--older-than-seconds 300`). Exige confirmación de que los trabajadores están detenidos y omite inicios recientes por defecto; no se ejecuta automáticamente al iniciar el sistema.
- Pruebas añadidas: recuperación idempotente, no duplicación cuando ya existe terminal, migración de esquema antiguo y rechazo de reconciliación sobre cadena corrupta.
- **Límite:** solo se reconcilian inicios con `start_event_id` correlacionable y más antiguos que el umbral configurado. La CLI exige confirmar que no hay ejecuciones activas. Esto registra el estado desconocido en el ledger; no recupera procesos del sistema operativo, resultados perdidos ni datos de almacenamiento físicamente dañado.
- **CI del código:** Python tests — [success](https://github.com/Xero-29/CYBER_AI/actions/runs/43996430032) y Docker sandbox — [success](https://github.com/Xero-29/CYBER_AI/actions/runs/43996436845), ambos en `2fe9ede3d5d2c49bbc45551ee9d0325893bc6b25`. La actualización documental posterior vuelve a disparar CI y debe validarse por separado.


## Corrección de trazabilidad de ejecuciones (16-11-2026)

- `tool_executor.py`: el evento terminal se intenta escribir en `finally` cuando existe evento inicial; captura excepciones inesperadas y clasifica el resultado como fallido/denegado/timeout/completado. Con `--require-ledger`, un fallo al persistir el resultado devuelve código no cero.
- `task_runner.py`: las excepciones inesperadas posteriores al inicio generan un resultado fallido y se intenta cerrar el evento en el ledger.
- `agent_runner.py`: un guard externo a la implementación detecta un evento inicial sin terminal asociado y añade un evento fallido ante excepciones no controladas, evitando duplicar cierres ya registrados.
- Se añadieron pruebas unitarias para las rutas de excepción, denegación, fallo de ledger y prevención de cierres duplicados.
- **Estado de validación:** cambios publicados en la rama de auditoría; no se declara CI aprobado hasta disponer de resultados de GitHub Actions para el HEAD actual. Esta corrección no resuelve por sí sola el anclaje externo WORM/KMS ni la identidad criptográfica del aprobador.

El ledger incorpora eventos `started` y terminales, con migración transaccional de bases existentes que conserva eventos y hashes. `tool_executor.py`, `task_runner.py` y `agent_runner.py` enlazan inicio/resultado y cierran excepciones capturables; admiten fail-closed mediante `--require-ledger` o `CYBER_AI_LEDGER_REQUIRED=1`. `nuclei_scanner.scan_target` admite `require_ledger=True`; `team_orchestrator.py` exige registrar inicio y resultado. Tras dos ejecuciones supervisadas correctas de la misma tarea, `team_orchestrator.py` propone automáticamente una Skill candidata basada en las etapas del flujo y los IDs del ledger. Las propuestas ignoran eventos `started`; la candidata no es ejecutable hasta revisión/firma VERITAS externa. Un apagado abrupto, pérdida del almacenamiento o fallo del propio ledger todavía puede impedir el cierre; el hash-chain local no sustituye un anclaje WORM externo.

`knowledge_eval.py` mide Recall@K, Precision@K y MRR@K con un benchmark por defecto de 48 consultas sintéticas (una por especialidad) y un smoke test reducido de 12. La biblioteca incorpora recuperación híbrida FTS5 + vectores con Reciprocal Rank Fusion (RRF), filtro de namespace/tenant y reconstrucción verificable del índice textual. Si SQLite no tiene FTS5, se conserva la recuperación semántica. La calidad aún debe medirse con embeddings reales y conjuntos revisados por expertos; faltan umbrales por dominio y evaluaciones validadas por especialistas.

La integración de proveedores ahora exige declarar capacidades reales para plugins; valida chat/embeddings/model_listing, selecciona proveedores por capacidad y permite fallbacks configurados cuando un proveedor no tiene la capacidad solicitada. Se añadieron endpoints por defecto seguros para proveedores nativos. El fallback de configuración no cubre fallos de red, cuotas o errores durante una petición.

Se reforzó el bootstrap de la biblioteca offline: IDs deterministas por ruta y SHA-256, bloqueo entre procesos, rechazo de rutas absolutas/traversal/symlinks, estados `processing/completed/failed`, reanudación tras fallos y prevención de duplicados. La indexación identifica el espacio vectorial del proveedor ECO y reindexa el contenido cuando cambia el modelo/proveedor, evitando mezclar vectores incompatibles en las búsquedas. Se añadieron pruebas de reintento, rutas, fallos y espacios de embeddings.

El descargador ahora exige `CYBER_AI_KNOWLEDGE_EGRESS_PROXY` para cualquier descarga real; sin gateway configurado falla antes de resolver el destino o abrir conexiones. El gateway debe imponer allowlist de hosts, pinning DNS y bloqueo de redes privadas. Esto no sustituye la validación de seguridad del proxy externo.

Se amplió `tool_adapters.py` con comandos locales acotados para Checkov, detect-secrets, Hadolint, ShellCheck, actionlint, kube-linter, YARA (requiere reglas locales) y TShark (solo PCAP/PCAPNG). El inventario distingue herramientas catalogadas, adaptadores registrados y binarios realmente disponibles. La presencia de un adaptador no implica que el binario esté instalado; las herramientas activas de red siguen fuera de esta ejecución local.

Se incorpora execution_ledger.py: registro SQLite transaccional append-only de ejecuciones con namespace, huella de tarea, estado, herramienta/versión, modelo, entorno, duración, coste opcional, resultados de validadores y hash SHA-256 de evidencia. Incluye cadena hash verificable, redacción de campos con nombres sensibles y bloqueo ordinario de UPDATE/DELETE. Se añaden pruebas específicas.

Límite: es evidencia tamper-evident, no almacenamiento WORM ni prueba criptográfica de identidad. Existe `ledger_checkpoint.py` para anclajes HMAC; falta desplegar la clave y almacenar checkpoints en un sistema independiente (KMS/HSM/WORM), además de pruebas operativas de restauración. La captura de inicio/resultado y el cierre de excepciones capturables están implementados en los ejecutores principales descritos arriba; los fallos abruptos del proceso o del almacenamiento aún pueden dejar eventos `started` abiertos. El modo fail-closed es opt-in en tool_executor, task_runner, nuclei_scanner y agent_runner; team_orchestrator lo exige en su ruta normal. No existe una política global obligatoria para todo el sistema. La propuesta automática de Skills ya se activa tras dos flujos supervisados correctos y revisión independiente; la activación sigue bloqueada hasta firma VERITAS externa. La promoción automática, KMS/HSM, regresión y obsolescencia siguen pendientes.

## Validación más reciente

- Commit `c2b7d65ed4b4a2510bd3065d1b6f102a38b5f5e7`: GitHub Actions Python tests **success**, 336 pruebas; Docker sandbox **success**.
- Commit `53b04787ca0b84865e81ad70ea9256cdca30adc5`: Python tests **success** y Docker sandbox **success**.
- Commit `05986653249dcdb77df39082fffeadb5657e75df`: Python tests **success** y Docker sandbox **success**.
- La validación CI no equivale a pruebas con Ollama/proveedores remotos, objetivos reales autorizados, cargas adversariales ni aislamiento microVM.

## Capacidades existentes (no equivalen a cierre institucional)

- Inventario de 21 herramientas, selección explicable y 14 especificaciones de adaptador; 11 tienen ejecución local acotada; YARA y TShark requieren aislamiento aún no disponible y pip-audit permanece bloqueado por red. El inventario expone `execution_ready` y `requires_isolation` para no confundir adaptador con permiso de ejecución. El inventario separa registro, disponibilidad del binario y cobertura de adaptador.
- Sandbox Docker endurecido con timeout del cliente y limpieza forzada del contenedor ante timeout; comparte kernel y no es aislamiento para malware hostil.
- Atlas de 48 áreas y 138 referencias externas catalogadas; además, 48 paquetes metodológicos propios incluidos offline. Las referencias externas no están descargadas ni ingeridas.
- Biblioteca SQLite con fragmentos comprimidos, SHA-256, metadatos, separación shared/tenant y búsqueda semántica.
- Ingestión transaccional (publicación de todos los fragmentos en una única transacción), límite de 2 MiB por fragmento y descompresión acotada de TXT/Markdown, HTML, CSV, JSON/JSONL y código; extractores opcionales PDF/DOCX/XLSX/PPTX con límites de tamaño, expansión ZIP y extracción incremental acotada para evitar acumulación descontrolada de texto. OCR de PDF escaneado y ejecución aislada de extractores siguen pendientes. Catálogo, descubrimiento y downloader con manifiesto serializado por lock; dry-run sin DNS ni escrituras. La descarga ahora falla cerrada antes de resolver DNS si no hay proxy de salida explícito; la garantía contra DNS rebinding depende de que el gateway configurado implemente allowlist, pinning DNS y bloqueo de redes privadas.
- Reindexación con staging, backup y publicación transaccional.
- Proveedores Ollama, OpenAI-compatible, Anthropic chat y Gemini chat/embeddings, con extensiones instalables mediante entry points `cyber_ai.providers`; HTTP solo en loopback, HTTPS remoto y redirecciones bloqueadas para proteger credenciales.
- Skillbook con propuestas automáticas de candidatas tras dos ejecuciones supervisadas independientes, activación solo con firma HMAC VERITAS, versiones inmutables y exclusión de candidatas de la búsqueda ejecutable. La clave sigue siendo un secreto operativo externo, no una identidad de modelo.
- Memoria de lecciones con HMAC VERITAS vinculado a dos ejecuciones con revisiones objetivas de un agente revisor distinto y hashes del ledger, validación de firma al leer, aislamiento por namespace, lock y permisos 0600. El registro directo se bloquea; las lecciones v1 sin firma se ignoran. HMAC no autentica por sí solo la identidad del modelo.
- Dependencias base fijadas en `requirements.lock` para instalaciones repetibles (sin hashes de artefactos; la verificación de procedencia/hash queda pendiente).
- `preflight.py` para revisar dependencias, configuración, herramientas opcionales y ledger local sin iniciar servicios ni usar red.
- `sbom_generator.py` genera SBOM CycloneDX 1.5 determinista desde los requirements fijados, separa dependencias directas/transitivas y registra el hash del lock. No inventa hashes de artefactos ni relaciones transitivas no declaradas.
- `ledger_checkpoint.py` firma/verifica con HMAC la cabeza de la cadena del ledger; sirve para anclar checkpoints fuera del host. Requiere clave externa y almacenamiento separado; no es WORM.
- `data_backup.py` crea snapshots SQLite consistentes, copia archivos con confirmación de procesos detenidos, verifica SHA-256 y restaura conservando el directorio anterior. No cifra ni firma el backup.
- `docs/THREAT_MODEL.md` contiene el baseline STRIDE, límites de confianza, amenazas y pruebas de aceptación para revisión independiente.
- CLI `ledger_cli.py` para verificar integridad, listar namespaces y consultar historial.
- Ledger de ejecuciones: registra respuestas, ejecuciones locales, timeouts, denegaciones y revisiones objetivas independientes. Los eventos `started` y terminales se enlazan en `tool_executor.py`, `task_runner.py`, `nuclei_scanner.py`, `agent_runner.py` y `team_orchestrator.py`. Los dos primeros admiten `--require-ledger`; Nuclei admite `require_ledger=True`; agent_runner usa `CYBER_AI_LEDGER_REQUIRED=1`; team_orchestrator falla si no registra inicio o resultado. La base existente se migra al esquema nuevo conservando filas y hashes. `ledger_checkpoint.py` crea/verifica anclajes HMAC de la cabeza del ledger para guardarlos fuera del host; la clave debe permanecer en gestor externo y el almacenamiento WORM/identidad independiente siguen pendientes. El cierre ante apagados abruptos o fallos del ledger no está garantizado; el ciclo de aprobación y regresión de Skills aún requiere infraestructura externa.

## Avance de biblioteca offline

- Catálogo ampliado a 48 especialidades.
- 48 paquetes propios en español incluidos en `knowledge/packs/`; 48 ampliados con guías de dominio, metodología, controles, laboratorio y criterios de evaluación. No equivalen a corpus experto exhaustivo ni a documentación oficial de fabricantes.
- Las referencias externas siguen pendientes de licencia/procedencia y no se declaran descargadas ni ingeridas.

- `knowledge_bootstrap.py` valida e indexa paquetes offline con ECO. El dry-run no requiere IA. La ingestión real requiere un proveedor con embeddings configurado. El proceso es reanudable, idempotente y detecta cambios de espacio vectorial para reindexar. No se inicia automáticamente por conectar un chat.

## Pendientes de cierre

1. **Ejecución y aprendizaje:** probar en CI el cierre de excepciones en los ejecutores; cubrir apagados abruptos y fallos de almacenamiento con recuperación/reconciliación; almacenar artefactos en repositorio controlado; desplegar checkpoints firmados externamente (CLI HMAC implementada; falta clave/almacenamiento independiente); costes reales por proveedor; retención y privacidad.
2. **Skills verificadas:** provisionar firma desde KMS/HSM o servicio independiente; cerrar el circuito de aprobación independiente, pruebas de regresión automáticas por versión, rollback probado y detección de obsolescencia.
3. **Biblioteca documental:** validar extractores PDF/Office en fixtures adversariales y sandbox; OCR cuando aplique; deduplicación/versionado; evaluación de recuperación con embeddings reales y especialistas; ANN/performance a escala; citas por fragmento; revisión de licencias/procedencia.
4. **Herramientas:** completar adaptadores según utilidad y riesgo, fijar versiones e imágenes por digest, añadir hashes verificables de artefactos y procedencia completa; existe SBOM CycloneDX inicial basado en el lock, pero no sustituye hashes ni attestation. No habilitar herramientas de red sin política explícita; el downloader aún requiere mitigación externa del riesgo DNS rebinding.
5. **Sandbox:** Docker solo para código confiable/acotado; microVM/VM desechable requiere infraestructura externa y pruebas de aislamiento; gestión de secretos y permisos.
6. **IA:** contrato de capacidades común, embeddings equivalentes, detección de capacidades, selección/fallback de modelos, pruebas de compatibilidad y gestión segura de credenciales.
7. **Operación institucional:** existe baseline STRIDE en `docs/THREAT_MODEL.md`, pero requiere revisión independiente contra el despliegue; faltan RBAC, auditoría inmutable externa, cifrado de backups, almacenamiento externo/WORM y restauración operacional probada (existe backup local con hashes, no cifrado), retención, redacción, migraciones, concurrencia, observabilidad y pruebas de carga.

## Criterio de cierre

No declarar el sistema completo ni certificado hasta que cada brecha tenga código, pruebas automatizadas, evidencia reproducible y validación operacional. No descargar indiscriminadamente el atlas, no ejecutar herramientas de red por defecto y no promover Skills por respuestas plausibles.

## Revisión de integración adicional (16-11-2026)

- Comparación directa con `main`: rama de auditoría **298 commits ahead / 1 behind**; estado GitHub `diverged`.
- El único commit exclusivo de `main` es `7b5ed033f1f6461b5780a10ac4ada67a444b93e5` (`fix: repair sandbox policy tests`), que modifica `tests/test_sandbox_runner.py`.
- La versión de ese test en la rama de auditoría ya contiene las comprobaciones de ese commit y añade regresiones para el ledger obligatorio, allowlist de herramientas de sandbox, timeout del proceso Docker, imagen fijada por digest y validación de rutas de evidencia. Por tanto, no se debe reemplazar la versión de la rama por el archivo más antiguo de `main`.
- La divergencia se mantiene explícita; no se ha hecho merge ni force-push. Antes de integrar, revisar el grafo completo y confirmar que no existen otros efectos del commit exclusivo fuera del archivo comparado.
- Revisión del flujo de excepciones: la firma de `_run_agent_impl` coloca `task_id` en el quinto argumento posicional; el wrapper lo propaga en esa posición o como keyword, y la correlación se realiza por `metadata.task_id`, no por el prompt redactado.
- **CI de la rama durante esta revisión: no verificado** (las consultas de ejecuciones asociadas a PR y estados combinados devolvieron listas vacías para los commits consultados). Los resultados CI históricos indicados arriba no deben interpretarse como validación del HEAD actual.

## Verificación de cierre — 2026-11-16 (actualización)

- Se verificó que el commit `d325796f2732a5a6fb7bb34d39f8b7a2cb494e0c` existe en GitHub y añade pruebas para validar la duración reportada por adaptadores y el fallback monotónico.
- Se inspeccionó `tool_executor.py`: `_duration_ms` acepta únicamente números finitos no booleanos y no negativos; ante evidencia inválida usa el reloj monotónico local.
- **CI de ese commit: no verificado.** Las consultas de ejecuciones asociadas al commit y de estados combinados no devolvieron ejecuciones ni estados. Esto no demuestra éxito ni fallo; no se debe marcar como verde.
- La rama sigue divergida respecto de `main`: 301 commits por delante y 1 por detrás según la comparación consultada. No se hizo merge ni force-push.
- La ejecución de la suite completa, Docker, proveedores externos, restauración y pruebas de aislamiento deben confirmarse mediante ejecuciones reproducibles. Los resultados históricos no sustituyen la validación del HEAD actual.
- No se declara cierre institucional: permanecen las dependencias de infraestructura y validación externa enumeradas en este documento.


## Cierre incremental y evidencia CI — 2026-11-16

- HEAD de esta validación: `9e08af07c88b34aacf21ac43ca3dfc265022d53d` (`test: cover restore destination safety and missing parents`).
- GitHub Actions para ese SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43921744002). Instalación, validación de sintaxis y paso `Run complete local verification` completados correctamente.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43921743898). Construcción de imagen, verificación completa, Ruff dentro del sandbox y carga de evidencia completados correctamente.
- `data_backup.py`: el manifiesto ahora exige esquema y metadatos coherentes, entradas con tipo/tamaño/SHA-256 válidos, rutas POSIX canónicas, tipos de archivo permitidos y coincidencia exacta entre archivos declarados y existentes. Rechaza rutas duplicadas/conflictivas, symlinks, archivos extra y el uso de `manifest.json` como entrada.
- Restauración: rechaza destinos que se solapan con el backup y crea directorios padre ausentes antes de preparar el reemplazo. La restauración sigue requiriendo escritores detenidos y confirmación explícita para sustituir datos.
- Se añadieron pruebas para manifiestos manipulados, archivos no declarados, rutas no canónicas, symlinks, destinos solapados y restauración en directorios nuevos.
- **Límite persistente:** los backups siguen sin cifrado ni firma criptográfica externa. La protección de integridad SHA-256 detecta alteraciones respecto del manifiesto, pero no autentica el origen si un atacante puede reemplazar ambos. La clave/almacenamiento externo, WORM y pruebas de recuperación operacional siguen pendientes.
- Comparación actual con `main`: `codex/security-integrity-audit` está divergida, **306 commits adelante y 1 detrás**. El commit exclusivo de `main` sigue siendo `7b5ed033f1f6461b5780a10ac4ada67a444b93e5`; no se hizo merge ni force-push.
- La evidencia CI anterior sustituye la anotación histórica de “CI no verificado” solo para el SHA indicado. No demuestra compatibilidad con proveedores remotos, aislamiento microVM, recuperación ante pérdida física, cifrado/KMS ni certificación institucional.


## Validación de Skillbook y HEAD actualizado — 2026-11-16

- HEAD de código validado: `ece33eb64ee9de098fbf63d7147122107f65b3a0`.
- Se corrigió la promoción repetida de una Skill: la aprobación firmada conserva la huella del payload y una repetición idéntica devuelve la Skill/version ya activada, sin crear una segunda Skill activa. La prueba cubre la repetición y confirma que el historial sigue siendo `proposed → approved`.
- CI para ese SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922107708). El paso de verificación completa terminó correctamente.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922107770). Construcción, verificación completa, Ruff en el sandbox y carga de evidencia terminaron correctamente.
- Comparación con `main` después de estos commits: **310 commits adelante / 1 detrás**, estado `diverged`. Se mantiene la decisión de no hacer merge ni force-push sin resolver el commit exclusivo de `main`.
- Esta validación confirma las suites y el sandbox CI del código de esta revisión; no sustituye pruebas operacionales con proveedores remotos, despliegue KMS/HSM/WORM, cifrado de backups, microVM ni pruebas de recuperación ante fallos físicos.


## Integridad autenticada y restauración resistente a TOCTOU — 2026-11-16

- HEAD de código validado: `2350069ab15597cac0699a49ea084163a8265892`.
- `data_backup.py` admite firma HMAC-SHA256 opcional del manifiesto mediante `CYBER_AI_BACKUP_HMAC_KEY` (mínimo 32 bytes). Cuando existe la clave, los backups se firman automáticamente; `verify` y `restore` aceptan `--require-signature`. Una copia firmada no se valida si falta la clave o no coincide. El modo sin firma sigue disponible para compatibilidad.
- La restauración vuelve a comprobar la huella del manifiesto después de la verificación y calcula tamaño/SHA-256 de cada archivo copiado antes de publicar el directorio restaurado. Esto detecta cambios de origen entre verificación y copia (TOCTOU).
- README actualizado con el flujo de firma, verificación y restauración. HMAC no cifra, no equivale a identidad individual ni sustituye KMS/HSM, rotación de claves o almacenamiento WORM.
- Prueba de regresión que muta el archivo de origen entre verificación y copia; la restauración debe abortar y conservar intacto el directorio de datos existente.
- CI para este SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922727386): verificación completa, **352 pruebas**.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43922727384): build, verificación completa, Ruff dentro del sandbox y carga de evidencia.
- Comparación actual con `main`: **316 commits adelante / 1 detrás**, estado `diverged`. No se ha fusionado ni sobrescrito `main`.
- Pendiente externo: provisionar y custodiar la clave HMAC desde un gestor de secretos, definir rotación/recuperación, habilitar cifrado de backup y almacenar copias/checkpoints fuera del host. No declarar restauración institucional hasta ejecutar simulacros reales de pérdida y recuperación.


## Auditoría de proveedores y procedencia — 2026-11-16

- HEAD de código validado: `08d5f51e133908e3d6586af6cc29102ccc47e505`.
- `llm_providers.py`: se valida el timeout (finito, mayor que cero y máximo 600 s), la estructura de respuesta normalizada, la cantidad de embeddings solicitados, dimensiones/valores finitos y contadores de uso no negativos. Se añadieron pruebas de límites y respuestas malformadas.
- Nuevo `knowledge_provenance.py`: auditoría de IDs, URLs HTTPS, editor declarado, licencia/evidencia, compuerta de descarga y fechas/intervalos de revisión. `verify.sh` lo ejecuta y `docs/KNOWLEDGE_PROVENANCE.md` documenta los criterios.
- Resultado del catálogo actual: **138 referencias externas, 0 aprobadas/revisadas por este control, 276 hallazgos pendientes, 0 errores estructurales y 0 vencidas**. No se marcan como confiables ni descargables por defecto. Las referencias necesitan revisión real de licencia, procedencia y vigencia.
- CI de este SHA:
  - [Python tests — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43957123521): verificación completa, **365 pruebas**.
  - [Docker sandbox — success](https://github.com/Xero-29/CYBER_AI/actions/runs/43957123616): build, verificación completa, Ruff dentro del sandbox y carga de evidencia.
- La historia se reconcilió con el commit exclusivo de `main` mediante un commit de merge que conserva el árbol de la rama auditada. Comparación: **327 commits adelante / 0 detrás**. PR #2 queda mergeable/clean, pero sigue draft y no se fusionó en `main`.
- Esto no certifica proveedores reales, seguridad jurídica del corpus, KMS/HSM, cifrado/WORM, microVM, RBAC, recuperación ante pérdida de host ni carga/estrés operacional. Esas pruebas requieren servicios, infraestructura y revisión humana externos.



## Trabajo de cierre adicional — 2026-11-16

- HEAD de la rama: `b5974450f8341a30d5197707cf2997296b4d2223`.
- Se añadieron `.github/dependabot.yml` para proponer actualizaciones semanales de dependencias Python y GitHub Actions, `SECURITY.md` con canal/proceso de reporte responsable y `docs/RELEASE_GATES.md` con criterios verificables de build, seguridad, conocimiento/IA, resiliencia y autorización de release.
- La rama no tiene protección habilitada (`protected=false`); branch protection y required checks siguen siendo una configuración administrativa pendiente. No se activaron porque el acceso disponible no permite garantizar que los permisos de administración estén concedidos.
- PR #2 permanece abierto y en draft; no se fusionó.
- CI disparada por los cambios: para el commit `60148e426e9e1c61edcd543de9320d213f1bd97b`, Python tests estaba `in_progress` y Docker sandbox `queued` al momento de esta actualización. Los resultados verdes del SHA anterior `4dfca8889ab84bd0345dce80dd084f95faecec16` no validan los nuevos archivos ni el HEAD actual.
- Dependabot solo crea propuestas; no aprueba ni fusiona actualizaciones automáticamente.
- No se ha añadido una licencia: es una decisión legal del propietario del repositorio, no algo que deba inventarse.
- El lock `requirements.lock` sigue sin hashes de artefactos. Añadir hashes no verificados sería inseguro; debe generarse desde un entorno de resolución confiable y fijarse para todas las plataformas objetivo.
- Próximas brechas implementables: hash-locked reproducible con verificación de artefactos, pruebas de estrés/concurrencia automatizadas, política de release y cobertura adicional de fallo abrupto. Las brechas que dependen de servicios/decisiones externas siguen abiertas: KMS/HSM, cifrado y rotación, WORM externo, RBAC/IdP, microVM, licencias y restauración real.


## Endurecimiento adicional — 2026-11-17

- `preflight.py` ahora comprueba permisos privados de `data/` y subdirectorios, rechaza symlinks en el árbol de datos y verifica que archivos locales sensibles (claves, secretos, credenciales y tokens) no sean accesibles por grupo/otros. `setup.sh` aplica permisos 0700 a directorios de datos existentes sin seguir un symlink en la raíz; los workflows preparan los permisos del checkout antes del preflight.
- Skillbook: se añadió revocación/deprecación explícita de Skills activas mediante aprobación HMAC VERITAS vinculada a Skill, versión actual y motivo. La revocación crea versión append-only y excluye la Skill de la recuperación ejecutable.
- Backups: se añadieron pruebas para symlink de archivo, traversal, manipulación del manifiesto firmado y limpieza de staging ante fallo de publicación atómica.
- Se añadieron pruebas para permisos de directorios de datos, subdirectorios y claves locales.
- La primera ejecución CI detectó que los directorios de datos del checkout tenían permisos 0755; se corrigió el flujo de instalación/CI para aplicar 0700 antes del preflight. En el HEAD `7a09cb065309f6a13982268505116a45d7dd5596`, Python tests y Docker sandbox finalizaron correctamente: [Python CI](https://github.com/Xero-29/CYBER_AI/actions/runs/44101897656) y [Docker CI](https://github.com/Xero-29/CYBER_AI/actions/runs/44101883529).
- Persisten las brechas externas: KMS/HSM, RBAC/IdP/MFA, almacenamiento WORM/offsite, cifrado y recuperación real de backups, microVM, proveedores IA reales, revisión de licencias/corpus, carga/DR y revisión independiente.


## Cobertura adicional de resiliencia y operación de Skills — 2026-11-17

- Skill revocation también está disponible desde `skillbook_cli.py` mediante `deprecate-payload` y `deprecate`; la aprobación se vincula a la versión actual y al motivo, y una aprobación obsoleta no se puede reutilizar.
- Ledger: se añadieron pruebas de fallo SQLite después del intento de inserción y de IDs duplicados; ambas verifican rollback sin eventos parciales y preservación de la cadena SHA-256.
- Estas pruebas simulan fallos transaccionales; no equivalen a ensayos físicos de disco lleno, corrupción del sistema de archivos o pérdida de host.

## Endurecimiento adicional implementable por código (17-11-2026)

- **Ledger:** `verify()` ejecuta primero `PRAGMA quick_check` y después valida la cadena SHA-256. Devuelve diagnósticos estructurados ante errores SQLite o JSON de eventos malformado, en lugar de propagar una excepción inesperada. Se añadieron pruebas para payload JSON corrupto y ejecución del chequeo SQLite.
- **Ingestión Office:** el validador de paquetes DOCX/XLSX/PPTX rechaza entradas ZIP que sean symlinks, nombres duplicados, entradas cifradas y cargas VBA/macros, además de los controles existentes de traversal, tamaño y ratio de compresión. Se añadieron fixtures adversariales.
- **Skillbook:** la promoción firmada de una Skill que no tenga candidata previa ahora comprueba duplicados e inserta la Skill y su primera versión dentro de la misma transacción `BEGIN IMMEDIATE`. Evita la ventana de carrera que podía crear Skills duplicadas ante aprobaciones concurrentes.
- **Límite de validación:** los cambios están publicados en esta rama. No se consideran aprobados hasta que terminen los workflows del HEAD final. `quick_check` detecta corrupción estructural SQLite, pero no reemplaza restauración desde backup ni un checkpoint externo contra truncamiento deliberado.

- **Pruebas adicionales del ledger:** se cubre contención por bloqueo SQLite (writer ocupado) y diagnóstico ante un archivo de base de datos ilegible. Se comprueba que el intento bloqueado no deja eventos parciales y que la cadena previa permanece válida.
- **Skillbook concurrente:** prueba con dos promociones HMAC simultáneas; ambas deben devolver el mismo ID y dejar una sola Skill y una sola versión inicial.
- **Estado CI:** pendiente de finalización para el HEAD que incorpora estas pruebas.
- **Citas PDF:** la extracción conserva marcadores `[PDF page N]` dentro del texto para que los fragmentos recuperados mantengan la referencia de página; se añadió una prueba con lector PDF simulado. No se ha añadido OCR: sigue siendo una dependencia externa opcional.
- **Revisión de Skills:** añadido `list_skills_due_for_review(max_age_days)` y CLI `python skillbook_cli.py review-due --max-age-days 180`. Identifica Skills activas cuya última aprobación/actualización superó la antigüedad configurada o tiene timestamp inválido. Es una alerta de revisión; no caduca ni revoca automáticamente una Skill, porque la revocación sigue exigiendo aprobación HMAC VERITAS.

## Validación final de esta iteración — 17-11-2026

**HEAD de código validado:** `0e702e4cc41cac0112dd236863940b3630096616`.

- Python tests: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44103957939
- Docker sandbox: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44103959685
- Se ejecutó la verificación completa, generación de SBOM y procedencia; el workflow Docker construyó la imagen, ejecutó la verificación completa y Ruff dentro del sandbox.
- Los tests nuevos incluidos en este HEAD cubren integridad SQLite, payload corrupto, writer ocupado, archivo SQLite ilegible, archivos Office adversariales, marcadores de página PDF, promoción concurrente de Skills y detección de Skills que requieren revisión.
- **Alcance:** CI verde no equivale a validación operacional, auditoría externa ni certificación institucional. No se han probado KMS/HSM, WORM/offsite, microVM, OCR real, proveedores IA con credenciales ni recuperación ante pérdida de host.

## Endurecimiento implementable adicional — 17-11-2026

- **Procedencia de herramientas locales:** cada adaptador calcula SHA-256 del binario real resuelto, registra ruta/version/hash en la evidencia y vuelve a calcular el hash al finalizar. Si el ejecutable desaparece o cambia durante la ejecución, la evidencia queda marcada como `integrity_error` y no se considera exitosa. Esto mejora trazabilidad, pero no reemplaza firma de proveedor, verificación de origen ni aislamiento.
- **Skillbook:** nuevo `verify_skill_history(skill_id)` y CLI `python skillbook_cli.py verify-history --skill-id ID`. Comprueba secuencia continua de versiones, identidad de snapshots y coherencia de la versión vigente con el último snapshot; excluye contadores operacionales de uso.
- **Artefactos de dependencias:** `dependency_artifact_manifest.py` inspecciona wheels descargados, verifica que sus nombres/versiones coincidan con `requirements.lock` y calcula SHA-256. El workflow Python genera este manifiesto y lo integra en los campos `hashes` del SBOM CycloneDX para los wheels de la plataforma CI.
- **Límite de reproducibilidad:** los hashes registrados describen los artefactos obtenidos en esa ejecución/plataforma; no son todavía hashes fijados en `requirements.lock` ni aseguran equivalencia para todos los sistemas operativos/arquitecturas. No se inventaron hashes. La fijación multiplataforma requiere resolver y revisar artefactos para cada plataforma soportada.
- **Pruebas añadidas:** cambio de binario durante ejecución, historial de Skills discontinuo/manipulado, validación de manifiestos de wheels y hashes SBOM.

## Cierre de brechas implementables por código — 17-11-2026

- **Hashes de ejecutables:** los adaptadores calculan SHA-256 del binario resuelto antes y después de ejecutar. La evidencia incluye ruta, versión y hashes; si cambia o desaparece, el estado pasa a `integrity_error`. El ejecutor registra los validadores de salida e integridad como fallidos, aunque el proceso devuelva código 0.
- **Historial de Skills con hash chain:** cada snapshot versionado queda enlazado mediante SHA-256 al anterior. `verify_skill_history` comprueba continuidad de versiones, hashes de cadena, identidad de snapshots y coincidencia del estado actual. La migración convierte historiales antiguos al nuevo formato; la migración no puede demostrar que los datos previos a ella nunca hubieran sido manipulados.
- **CLI de verificación:** `python skillbook_cli.py verify-history --skill-id ID` devuelve código distinto de cero si el historial no supera los controles.
- **Dependencias:** el workflow Python descarga wheels correspondientes a las versiones fijadas, calcula SHA-256, verifica cobertura/versiones contra `requirements.lock` e integra hashes en el SBOM CycloneDX. Se publica el SBOM junto con el manifiesto de procedencia del build.
- **Límite de lock:** los hashes corresponden a artefactos de la plataforma de CI de esa ejecución. No equivalen a hashes obligatorios comprometidos en el lock para todos los sistemas/arquitecturas; no se inventaron hashes ni se habilitó una falsa garantía de reproducibilidad multiplataforma.
- **Pruebas:** CI ejecutó la suite completa, verificación de procedencia, generación SBOM con hashes y construcción/ejecución del sandbox Docker.

### Evidencia CI del HEAD de código

- HEAD: `defa615b7ff46bf36b3382d4396bc1082ce1ab29`.
- Python tests + wheel manifest + SBOM: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44106180565
- Docker sandbox + Ruff aislado: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44106180427
- Artefacto SBOM/procedencia publicado: `cyber-ai-sbom-defa615b7ff46bf36b3382d4396bc1082ce1ab29`.
- Comparación actual con `main`: 427 commits adelante, 0 detrás. PR #2 sigue abierto como draft; no se ha fusionado.

## Validación adicional de crash y protección de evidencias — 17-11-2026

- **Crash real de proceso simulado:** prueba que inicia una ejecución del ledger en un subproceso y termina abruptamente con `os._exit`; un nuevo proceso reconcilia el evento `started` como `interrupted`, conserva la cadena y confirma idempotencia. Es una simulación reproducible de terminación abrupta, no de fallo físico de disco/host.
- **Evidencias de herramientas:** directorio privado 0700 en POSIX, archivos 0600, creación exclusiva sin seguir symlinks, nombre de herramienta validado, flush/fsync y limpieza del archivo ante fallo de escritura. Se añadieron pruebas de permisos y rutas simbólicas/identificadores maliciosos.
- **CI del HEAD exacto:** `c552c104a44fa85b962d92601fb214a7f65295ff`.
  - Python tests, preflight, suite completa, manifiesto SHA-256 de wheels y SBOM CycloneDX: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44107141259
  - Docker build, suite completa y Ruff dentro del sandbox: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44107141220
- Comparación con `main`: 435 commits adelante, 0 detrás. PR #2 abierto como draft, no fusionado.

## Aclaraciones finales de seguridad de ejecución — 17-11-2026

- **Egress local:** los adaptadores host no aíslan la red del proceso. La evidencia lo declara explícitamente como `network_access: not_enforced` y `network_isolation_enforced: false`. Bloquear adaptadores que requieren red no impide que un binario local intente conexiones. El runner Docker usa `--network=none` para las herramientas instaladas en esa imagen (actualmente Ruff y Bandit); no generalizar ese aislamiento a los adaptadores ejecutados directamente en host.
- **Publicación de evidencia:** escritura en archivo temporal privado, flush/fsync, publicación por reemplazo atómico y fsync del directorio en POSIX. Archivos 0600 y directorios 0700 en POSIX; Windows requiere ACL privadas que el código no configura por sí solo.
- **HEAD de código y documentación validado:** `7fab89000660664a3fe16d61ca43f0fdda5efda8`.
  - Python suite + preflight + hashes de wheels + SBOM: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44107553414
  - Docker build + suite completa + Ruff en sandbox sin red: **success** — https://github.com/Xero-29/CYBER_AI/actions/runs/44107553436
- **Límite:** el runner Docker solo cubre herramientas incluidas en la imagen. Los demás adaptadores no heredan automáticamente aislamiento de red ni microVM.

