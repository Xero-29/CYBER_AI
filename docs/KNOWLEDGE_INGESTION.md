# Ingestión documental

## Formatos

La ingesta base admite texto UTF-8, Markdown, HTML, CSV, JSON/JSONL y código fuente. Los extractores opcionales permiten PDF con texto, DOCX, XLSX y PPTX.

Instala los extras documentales con:

```bash
pip install -r requirements-documents.txt
```

El extractor aplica límites de 100 MiB por archivo, 256 MiB de expansión para paquetes Office, 10.000 entradas ZIP, ratio de compresión máximo de 500, 200.000 filas para CSV/XLSX, 5.000 páginas/diapositivas y 10 millones de caracteres extraídos.

La generación de embeddings se completa por lotes antes de publicar los fragmentos. Si un lote falla, el documento no deja una importación parcial visible en la biblioteca; el guardado final de los fragmentos es una sola transacción SQLite.

## Límites y seguridad

- PDF cifrados se rechazan.
- PDF escaneados sin capa de texto requieren OCR externo; no se declara OCR implementado.
- Se rechazan enlaces simbólicos como entrada.
- Se eliminan scripts/estilos del texto extraído desde HTML.
- Los paquetes Office se inspeccionan antes de usar las bibliotecas de extracción.
- Los parsers siguen ejecutándose dentro del proceso local. Hasta disponer de sandbox dedicada para extracción, importa solo documentos confiables.
- El texto extraído se envía al proveedor de embeddings configurado; no envíes documentos confidenciales a proveedores remotos sin autorización y política de datos.
- La ingesta no verifica licencias ni concede derechos de redistribución. Registra procedencia y licencia antes de compartir el contenido.

## Validación pendiente

Las pruebas automatizadas cubren HTML, CSV, JSON, límites de tamaño, fragmentación y almacenamiento simulado. PDF y Office requieren fixtures de prueba adicionales y validación operacional con archivos reales.
