# Secciones de profundización — Informática forense

## Modelo de amenazas
La evidencia puede ser destruida, alterada, incompleta o contaminada durante adquisición, transporte, análisis y reporte. Identificar fuentes volátiles, discos, móviles, cloud, logs, SaaS, backups y terceros. Amenazas incluyen anti-forensics, clock drift, cifrado, rotación de logs, snapshots inconsistentes y pérdida de metadatos. Separar hechos observados, inferencias y atribución.

## Detección
Establecer readiness: logging habilitado, retención, sincronización horaria, snapshots, audit trails, permisos de adquisición y alertas de borrado/alteración. Detectar gaps de telemetría, cambios de configuración de logging, borrado de snapshots y acceso inusual a repositorios de evidencia. La detección forense depende de cobertura previa, no solo de herramientas posteriores.

## Respuesta a incidentes
Priorizar fuentes volátiles y requisitos legales; documentar autorización, operador, hora, método, herramienta y estado. Adquirir copias verificables, calcular hashes, preservar originales y analizar duplicados de trabajo. Mantener cadena de custodia y control de acceso. En cloud, coordinar con proveedor y preservar logs antes de que expire retención.

## Casos prácticos
En una VM de laboratorio, generar eventos de login, descarga y borrado; adquirir disco y logs, calcular hashes, reconstruir timeline y comparar con reloj de sistema. Repetir con snapshot cloud y objeto versionado. Un segundo analista debe reproducir hallazgos desde evidencia preservada y obtener el mismo timeline.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-86, ISO/IEC 27037, RFC 3227 y guías de proveedor cloud. La validez legal depende de jurisdicción, autorización y procedimiento documentado.
