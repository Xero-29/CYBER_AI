# Auditoría de procedencia y vigencia del conocimiento

Ejecuta desde la raíz del repositorio:

```bash
python knowledge_provenance.py
python knowledge_provenance.py --json
python knowledge_provenance.py --require-reviewed
```

El informe revisa IDs duplicados, URLs HTTPS, editor/dominio declarado, estado de licencia, evidencia de licencia, compuerta de descarga, fecha de última revisión e intervalo de vigencia.

- `ready`: las fuentes están aprobadas, documentadas y dentro de su ventana de revisión.
- `needs_review`: hay licencias pendientes/restringidas, metadatos incompletos o revisiones vencidas.
- `invalid`: hay errores estructurales o una compuerta de descarga insegura.

El modo normal informa brechas sin bloquear el resto de la verificación; `--require-reviewed` devuelve código distinto de cero si existe alguna fuente pendiente o vencida. El script no certifica la exactitud técnica del contenido, no valida jurídicamente licencias, no descarga documentos y no sustituye la revisión humana ni el control de derechos. Las fechas y evidencias deben proceder de una revisión real; no deben rellenarse automáticamente para hacer pasar la auditoría.
