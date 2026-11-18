# Adquisición de conocimiento externo

## Catálogo curado y cobertura temática

`data/knowledge_sources/acquisition_sources.json` incorpora las referencias candidatas del catálogo temático y las relaciona con los IDs reales de `knowledge/curricula/domain_curriculum.json`. El catálogo temático contiene 107 URLs únicas distribuidas entre 48 áreas. Las entradas importadas conservan `license_status=pending`, `verified_for_download=false` y `download=false`: una URL registrada no implica que el contenido se haya descargado, leído, licenciado o validado.

```bash
python knowledge_source_acquisition.py --audit --json
python knowledge_source_acquisition.py --build-downloader-catalog --json
python knowledge_downloader.py --dry-run
```

El auditor contrasta cada ID con el currículo, rechaza áreas desconocidas e informa áreas sin referencias asociadas. Cobertura 48/48 significa únicamente que cada área tiene al menos una referencia candidata mapeada; no demuestra profundidad, calidad ni actualidad.

## Flujo operativo

1. Descubrir candidatos en los catálogos curados.
2. Revisar documento original, licencia y condiciones de acceso.
3. Habilitar individualmente solo artefactos autorizados.
4. Descargar detrás del gateway de salida exigido por el downloader.
5. Verificar tipo, tamaño, hash y procedencia; conservar el original.
6. Ejecutar `knowledge_discovery.py` para registrar el archivo local.
7. Ejecutar `knowledge_ingest.py` solo después de inspección de seguridad.
8. Clasificar, revisar el texto completo, registrar versión y evaluación.
9. Reindexar y comprobar recuperación con `knowledge_eval.py`.

## Salvaguardas

- No elude paywalls, autenticación, robots ni términos de uso.
- No descarga masivamente repositorios o datasets con condiciones inciertas.
- No ejecuta archivos obtenidos; documentos y datasets se consideran no confiables.
- Las licencias se verifican por artefacto, no se heredan del sitio anfitrión.
- Los preprints se distinguen de publicaciones revisadas por pares.
- La ingestión no convierte automáticamente un recurso en evidencia validada.
- El downloader exige `CYBER_AI_KNOWLEDGE_EGRESS_PROXY`; la validación DNS local no elimina el riesgo TOCTOU.

## Límites

El catálogo contiene referencias candidatas, no documentos descargados. Las licencias de cada documento y versión siguen pendientes de verificación. La descarga real permanece deshabilitada por defecto. El mapeo no declara validación científica ni cobertura profunda.
