# Adquisición de conocimiento externo

## Catálogo curado

`data/knowledge_sources/acquisition_sources.json` registra fuentes oficiales, repositorios de datos y publicaciones académicas con especialidades, formatos, cadencia, URL de origen y notas de licencia. Es un catálogo de descubrimiento, no una colección descargada ni una afirmación de lectura o validación.

```bash
python knowledge_source_acquisition.py --audit --json
python knowledge_source_acquisition.py --build-downloader-catalog --json
python knowledge_downloader.py --dry-run
```

El generador produce `data/knowledge_sources/download_catalog.json`, consumido por `knowledge_downloader.py`. Todos los recursos salen con `verified_for_download=false` y `download=false`. Un responsable debe revisar el artefacto y su versión exactos, licencia, URL directa, hash esperado, tamaño, destino y condiciones de redistribución antes de habilitar una descarga.

## Flujo operativo

1. Descubrir candidatos en el catálogo curado y en el registro editorial.
2. Revisar documento original, licencia y condiciones de acceso.
3. Habilitar individualmente solo artefactos autorizados.
4. Descargar detrás del gateway de salida exigido por el downloader.
5. Verificar tipo, tamaño, hash y procedencia; conservar el original.
6. Ejecutar `knowledge_discovery.py` para registrar el archivo local.
7. Ejecutar `knowledge_ingest.py` solo después de inspección de seguridad.
8. Clasificar, revisar texto completo, registrar versión y evaluación.
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

El catálogo contiene fuentes y endpoints candidatos, pero no significa que se hayan descargado, leído ni incorporado sus contenidos. La descarga real permanece bloqueada por diseño hasta la revisión humana de cada recurso y configuración del gateway. Las licencias listadas son pistas de revisión, no asesoría legal ni autorización general de redistribución.
