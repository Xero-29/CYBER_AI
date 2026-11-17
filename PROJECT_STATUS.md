# Estado canónico vigente — 2026-11-17

> Esta sección describe el HEAD verificado; los bloques históricos inferiores son contexto, no estado actual.

**Rama:** `main`  
**HEAD auditado:** `71bab12b35690ada40e3f6bbc6e4e7bcfd0d88cb` (antes de esta ronda de correcciones).  
**Árbol:** 220 archivos; 46 módulos Python de producción y 490 pruebas reportadas por la última CI.  
**CI en HEAD auditado:** Python tests y Docker sandbox completados con éxito (run IDs `44120967805` y `44120967821`).  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17`, sin modificar.

## Auditoría estructural y funcional

- La limpieza anterior retiró seis prototipos/demos sin consumidores de producción: `audit_target.py`, `test_api.py`, `agent_benchmark.py`, `agent_core.py`, `tests/test_agent_core.py` y `verifier.py`.
- Se conservaron herramientas CLI y subsistemas independientes con finalidad concreta, aunque no sean imports directos del orquestador.
- La revisión detectó un fallo real de portabilidad: `knowledge_downloader.py` importaba `fcntl` incondicionalmente, por lo que el comando no podía arrancar en Windows. La corrección en curso reutiliza el bloqueo POSIX/Windows ya probado de `knowledge_bootstrap.py`.
- Se detectó además que el downloader confiaba en el estado `downloaded` del manifiesto y omitía el recurso sin verificar el archivo. La corrección en curso fuerza la comprobación SHA-256 y permite recuperar archivos ausentes o alterados.
- No se eliminan los `pass` encontrados de forma automática: los observados pertenecen a limpieza de temporales o manejo de fallos secundarios, no a implementaciones vacías.
- Los resultados de CI se deben asociar al SHA exacto. Los dos workflows del HEAD anterior están verdes; los cambios de esta ronda requieren nueva CI antes de considerarse verificados.

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
