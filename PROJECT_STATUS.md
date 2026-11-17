# Estado canónico vigente — 2026-11-17

> Esta sección describe el HEAD verificado; los bloques históricos inferiores son contexto, no estado actual.

**Rama:** `main`  
**HEAD auditado:** `c51bfe087bcd533a1ff1bc42268cade2b7c9a21b` (correcciones funcionales de esta ronda).  
**Árbol:** 220 archivos; 46 módulos Python de producción y 490 pruebas reportadas por la última CI.  
**CI:** Docker sandbox aprobado en el HEAD auditado (run `44122739051`); el workflow Python está pendiente de asignación de runner (run `44122739059`).  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17`, sin modificar.

## Auditoría estructural y funcional

- La limpieza anterior retiró seis prototipos/demos sin consumidores de producción: `audit_target.py`, `test_api.py`, `agent_benchmark.py`, `agent_core.py`, `tests/test_agent_core.py` y `verifier.py`.
- Se conservaron herramientas CLI y subsistemas independientes con finalidad concreta, aunque no sean imports directos del orquestador.
- La revisión detectó un fallo real de portabilidad: `knowledge_downloader.py` importaba `fcntl` incondicionalmente, por lo que el comando no podía arrancar en Windows. La corrección reutiliza el bloqueo POSIX/Windows de `knowledge_bootstrap.py` y se añadió su ejecución a la comprobación Windows.
- Se detectó además que el downloader confiaba en el estado `downloaded` del manifiesto y omitía el recurso sin verificar el archivo. La corrección fuerza la comprobación SHA-256 y permite recuperar archivos ausentes o alterados; se añadió una prueba de regresión.
- No se eliminan los `pass` encontrados de forma automática: los observados pertenecen a limpieza de temporales o manejo de fallos secundarios, no a implementaciones vacías.
- Los resultados de CI se deben asociar al SHA exacto. El sandbox Docker del HEAD actual está verde, incluyendo `verify.sh` y Ruff. El workflow Python independiente sigue pendiente, por lo que no se declara verificación completa.

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
