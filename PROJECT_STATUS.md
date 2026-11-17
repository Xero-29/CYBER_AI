# Estado canónico vigente — 2026-11-17

> Esta sección es la fuente de verdad vigente. Los bloques históricos que aparecen debajo documentan etapas anteriores y no deben interpretarse como el estado actual.

**Rama:** `main`  
**Último cambio de código y pruebas:** `39f197ea6aa96b30535d6a356084ae148756b898`  
**Respaldo:** `backup/main-before-cyber-ai-2026-11-17` (no modificado).  
**CI del HEAD:** sin checks publicados/recuperables en la última consulta; queda pendiente de validación exacta.

## Limpieza estructural realizada

Se eliminaron seis archivos sin consumidores de producción ni una función mantenida y probada:
- `audit_target.py` y `test_api.py`: demo local aislada que simulaba un gateway de producción; no formaba parte del producto y dependía de Flask, ausente de las dependencias instaladas.
- `agent_benchmark.py`: benchmark ad hoc contra `example.com` y una ruta local fija, sin integración ni pruebas.
- `agent_core.py` y `tests/test_agent_core.py`: motor/prototipo independiente sustituido por el pipeline real de adaptadores, autorización y allowlist.
- `verifier.py`: verificador NVD inicial sin consumidores ni pruebas; la ruta mantenida de informes usa `nvd_client.py`.

Se conservan `batch_analyzer.py`, `nvd_client.py`, `report_manager.py`, `ledger_cli.py` y `skillbook_cli.py`: tienen consumidores o funciones CLI diferenciadas. `tests/final_smoke_test.txt` se conserva como muestra de informe, no como resultado de ejecución.

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
