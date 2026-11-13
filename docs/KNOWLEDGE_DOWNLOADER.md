# Descargador de conocimiento

## Simulación y descarga

```bash
python knowledge_downloader.py --dry-run
python knowledge_downloader.py --area <area_id>
python knowledge_downloader.py --area <area_id> --retry-failed
```

El modo `--dry-run` valida formato de URL, configuración, tamaño y destino sin resolver DNS, crear carpetas, descargar datos ni modificar el manifiesto. La descarga real requiere `verified_for_download=true` en el catálogo.

## Controles

- HTTPS, puerto 443, sin IP literal, sin credenciales embebidas.
- Resolución DNS validada contra direcciones globales antes de cada petición.
- Proxies heredados deshabilitados y redirecciones limitadas al mismo host.
- Límites por archivo y globales, tipo de contenido, SHA-256 opcional y escritura temporal con reemplazo atómico.
- Lock exclusivo del manifiesto para evitar que dos procesos sobrescriban estados concurrentes.
- El manifiesto se actualiza después de cada recurso descargado o fallido.

## Riesgo residual

La comprobación DNS y la conexión HTTP son operaciones separadas; un atacante que controle DNS podría intentar un rebinding entre ambas (TOCTOU). No se debe declarar protección SSRF perfecta. Para uso institucional, ejecutar el downloader detrás de un proxy de salida con allowlist o usar transporte con pinning de IP que preserve SNI y validación TLS. Hasta entonces, solo habilitar fuentes revisadas y usar el downloader en un entorno de red controlado.
