# Estado canónico vigente — 2026-11-17

> Esta sección describe el HEAD auditado; los bloques históricos inferiores son contexto.

**Rama:** `main`  
**HEAD auditado:** `d9337c5e46e6760ae16f14e99afba1986644ffa7`.  
**CI:** Python `unit-tests` aprobado en este SHA (run `44125848717`, 493 pruebas). Docker sandbox de este SHA pendiente de conclusión al actualizar este estado. Las pruebas Windows siguen aplazadas.  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17`, sin modificar.

## Cambio reciente: perfiles y herramientas personalizadas

- Se incorporó `config/tool_execution_profiles.json` con perfiles `standard`, `extended` y `restricted`; el perfil se selecciona con `--tool-profile` en `cyber_ai.py --team`, o con `CYBER_AI_TOOL_PROFILE`.
- Los perfiles configuran el máximo de herramientas, timeout, permiso de objetivos externos y activación de herramientas personalizadas. No pueden omitir confirmación ni allowlist HMAC.
- Se incorporó un registro declarativo de herramientas personalizadas. Se definen ejecutable, argumentos argv, palabras clave y timeout en el JSON; el planificador puede proponerlas y el runner las ejecuta sin shell.
- Cada herramienta personalizada exige hash SHA-256 firmado en la allowlist HMAC; su evidencia se valida y registra en el ledger como las herramientas nativas.
- Los objetivos externos requieren simultáneamente el perfil `extended` (o uno equivalente que los permita) y el flag `--allow-external-targets`.
- La ejecución arbitraria de shell continúa deshabilitada. El runner personalizado no impone aislamiento de red; la evidencia declara `network_access=not_enforced`.
- Documentación: `docs/TOOL_EXECUTION_PROFILES.md`. Pruebas nuevas: `tests/test_tool_execution_profiles.py`.




## Auditoría estructural y funcional

- La limpieza anterior retiró seis prototipos/demos sin consumidores de producción: `audit_target.py`, `test_api.py`, `agent_benchmark.py`, `agent_core.py`, `tests/test_agent_core.py` y `verifier.py`.
- Se conservaron herramientas CLI y subsistemas independientes con finalidad concreta, aunque no sean imports directos del orquestador.
- La revisión detectó un fallo real de portabilidad: `knowledge_downloader.py` importaba `fcntl` incondicionalmente, por lo que el comando no podía arrancar en Windows. La corrección reutiliza el bloqueo POSIX/Windows de `knowledge_bootstrap.py` y la comprobación Windows se conserva como tarea aplazada y se ejecutará en una ronda posterior.
- Se detectó además que el downloader confiaba en el estado `downloaded` del manifiesto y omitía el recurso sin verificar el archivo. La corrección fuerza la comprobación SHA-256 y permite recuperar archivos ausentes o alterados; se añadió una prueba de regresión.
- No se eliminan los `pass` encontrados de forma automática: los observados pertenecen a limpieza de temporales o manejo de fallos secundarios, no a implementaciones vacías.
- Los resultados de CI se deben asociar al SHA exacto. El workflow Python del HEAD actual está verde. El sandbox Docker se verifica por separado; no se declara verificación completa hasta confirmar también ese run.

## Funciones mantenidas

- Entradas: `cyber_ai.py --ask`, `--team`, `--report`, `--batch`, `--scan`, `--self-test`.
- Orquestación/proveedores: agentes, DIRECTOR, planificador, equipo multiagente y adaptadores.
- Autorización y trazabilidad: allowlist HMAC, política de ejecución, validadores, evidencia y ledger.
- Conocimiento: catálogo, bootstrap offline, ingestión, índice, búsqueda híbrida, embeddings, procedencia y evaluación.
- Memoria y Skills: memoria de aprendizaje, gestor de memoria de modelos, Skillbook y regresión.
- Informes y vulnerabilidades: análisis, NVD, lotes, registro de duplicados y Nuclei.

## Límites que siguen abiertos

- La validación de evidencia comprueba integridad/estructura y alcance declarado; no demuestra por sí sola veracidad, explotabilidad ni exhaustividad.
- El aislamiento de red de los procesos locales no está forzado (`network_access=not_enforced`).
- Nuclei conserva un flujo de autorización separado del planificador local.
- El catálogo de herramientas no garantiza instalación, adaptación ni disponibilidad operativa.
- Custodia/rotación externa de claves, ACL Windows completas, aislamiento de parsers, KMS/HSM, RBAC/IdP/MFA, WORM/offsite, DR, MicroVM, proveedores IA reales, observabilidad, pruebas de carga y revisión independiente requieren infraestructura y validación externas.

**Conclusión:** el repositorio tiene cobertura modular y CI automatizada, pero no debe declararse listo ni certificado para producción hasta cerrar los límites anteriores y superar pruebas E2E autorizadas.
