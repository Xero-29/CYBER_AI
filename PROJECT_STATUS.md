# Estado de integración de seguridad y dependencias — 2026-11-17

**Rama:** `codex/integration-hash-locks-2026-11-17-v2`  
**Main preservado hasta:** `c9c794c984b3fff5ff2032d0831f7f161205afc0` (incluido como segundo padre de este merge de integración).  
**Base inicial de esta rama:** `12c5942a73bf21f2eb0cc2bb5b79a5826801defd`.  
**Rama fuente de dependencias:** `codex/security-integrity-audit`, HEAD `482df7480ac547003a90e621c95c15789067c4dc`; 13 commits únicos desde el merge-base `cae816d6037b56f017c2fbdbb3e98ef00df58c1d`.  
**PR #2:** ya fusionado en main. **PR #1:** sigue como draft antiguo, no se duplica ni se integra a ciegas. No se ha modificado ni fusionado `main`.

## Cambios añadidos y preservados

- Dependencias base y sandbox con SHA-256 y `pip --require-hashes`; instalación base restringida a CPython 3.12.x/Linux x86_64/glibc >= 2.26.
- Lock independiente de Ruff/Bandit, verificación de wheels, generador reproducible de locks y SBOM CycloneDX separado para ambos entornos.
- Evaluación de conocimiento endurecida y pruebas de regresión.
- Se preservan los cambios posteriores de main: CLI y orquestación, pipeline de herramientas locales con allowlist/evidencia/ledger, y el nuevo contrato de validación de resultados remotos/Nuclei con cierre seguro ante evidencia inválida.
- Workflows con smoke test Windows, hash enforcement y ejecución Docker en esta rama.

## Evidencia

- Rama fuente `482df7480ac547003a90e621c95c15789067c4dc`: Python Tests success, 471 pruebas ([44116054953](https://github.com/Xero-29/CYBER_AI/actions/runs/44116054953)); Docker Sandbox success ([44116054989](https://github.com/Xero-29/CYBER_AI/actions/runs/44116054989)).
- Main `c9c794c984b3fff5ff2032d0831f7f161205afc0`: Python Tests success ([44118679332](https://github.com/Xero-29/CYBER_AI/actions/runs/44118679332)); Docker Sandbox success ([44118679148](https://github.com/Xero-29/CYBER_AI/actions/runs/44118679148)).
- La rama de integración debe volver a validarse sobre su HEAD exacto después de incorporar estas dos líneas de trabajo. No se declara verde hasta que sus propios checks concluyan.

## Brechas pendientes

- `requirements-documents.txt` sigue usando rangos de versión sin hashes; falta lock y SBOM de ese entorno opcional.
- Los locks actuales cubren CPython 3.12.x/Linux x86_64/glibc >= 2.26; otras plataformas requieren hashes propios.
- Los hashes fijan wheels pero no sustituyen provenance/attestations upstream.
- Docker comparte kernel; falta microVM/aislamiento fuerte.
- HMAC local no sustituye KMS/HSM, firma asimétrica ni custodia independiente.
- Faltan RBAC/IdP/MFA, WORM/offsite, backups cifrados y simulacros DR/RPO/RTO.
- Faltan pruebas operacionales en equipo limpio, carga/estrés, proveedores reales, observabilidad y revisión experta de la biblioteca.

**Estado:** rama de integración en preparación. No está certificada ni lista para producción. El criterio de avance es CI verde sobre el HEAD exacto de esta rama y revisión del PR; después quedarán las validaciones operacionales externas.

---

# Estado canónico vigente — 2026-11-17

> Esta sección es la fuente de verdad vigente. Los bloques históricos que aparecen debajo documentan etapas anteriores y no deben interpretarse como el estado actual.

**Rama:** `main`  
**Último cambio de código y pruebas:** `39f197ea6aa96b30535d6a356084ae148756b898`  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17` (no modificado).  
**CI del HEAD:** sin checks publicados/recuperables en la última consulta; queda pendiente de validación exacta.

## Integración realizada

- `cyber_ai.py --ask` conecta la entrada principal con DIRECTOR, agentes y recuperación de conocimiento.
- `cyber_ai.py --team` conecta el flujo multiagente supervisado con planificador e inventario de herramientas.
- La ejecución local opcional usa `--execute-tools --confirm-tool-execution --tool-target`; exige confirmación explícita, allowlist HMAC obligatoria y objetivo relativo confinado al repositorio.
- El pipeline local genera evidencia, valida integridad y registra eventos del ledger; los resultados llegan a los agentes como datos no confiables.
- Nuclei usa el contrato `cyber-ai.remote-scan.v1`, valida estructura y origen de cada hallazgo contra el destino autorizado, rechaza JSONL malformado y enlaza la evidencia con el evento terminal del ledger.
- La autorización de Nuclei continúa siendo específica por destino/acción y separada del planificador local. No se heredan permisos entre rutas.
- El planificador degrada con advertencia explícita cuando falta el índice de capacidades.

## Evidencia de CI

- Docker sandbox: éxito en `12c5942a73bf21f2eb0cc2bb5b79a5826801defd`; 488 pruebas, construcción Docker y Ruff aprobados en ese SHA.
- Python workflow y smoke test Windows de ese SHA no tenían resultado final confirmado en la última revisión.
- Los cambios posteriores, incluido el contrato de Nuclei, **no están validados por CI todavía**. No se afirma suite verde en el HEAD actual.

## Límites pendientes

- El validador remoto comprueba estructura y correspondencia del origen, no veracidad, explotabilidad ni exhaustividad de los hallazgos.
- Nuclei sigue separado del flujo multiagente; la ejecución remota requiere autorización local vigente y configuración real.
- Los adaptadores locales en host no tienen aislamiento de red forzado (`network_access=not_enforced`).
- Siguen pendientes enrolamiento confiable de binarios, custodia/rotación externa de claves, ACL Windows completas, lock multiplataforma con hashes oficiales, corpus experto, OCR y aislamiento real de parsers.
- KMS/HSM, RBAC/IdP/MFA, WORM/offsite, backups/DR, MicroVM, proveedores IA reales, observabilidad, pruebas de carga y revisión independiente requieren infraestructura/decisiones externas.

**Conclusión:** la conectividad del flujo local y la ruta de evidencia de Nuclei mejoraron, pero el proyecto no está terminado ni certificado para producción. La siguiente condición es CI verde en el HEAD final y pruebas E2E autorizadas con Nuclei real.
