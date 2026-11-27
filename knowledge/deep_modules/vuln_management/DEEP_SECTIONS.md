# Secciones de profundización — Gestión de vulnerabilidades

## Modelo de amenazas
El riesgo depende de activo, versión, exposición, explotabilidad, privilegio, controles, criticidad y dependencia. Amenazas incluyen activos desconocidos, inventario obsoleto, CVE mal mapeado, scanner ciego, exploit disponible, KEV, falso positivo y parche que interrumpe servicio. Separar vulnerabilidad técnica de exposición y riesgo de negocio.

## Detección
Unificar escaneo autenticado/no autenticado, SCA, cloud posture, advisories, CVE/CPE, KEV, EPSS y exposición externa. Deduplicar por activo/componente/versión y conservar evidencia de detección. Detectar nuevos activos, cambios de exposición, vulnerabilidades explotadas y findings reabiertos. Medir cobertura de inventario, latencia de ingestión y precisión de identificación.

## Respuesta a incidentes
Priorizar explotación activa y activos expuestos; aplicar mitigación temporal, segmentación o regla compensatoria; coordinar parcheo con dueño de servicio y ventana; preservar evidencia si hay explotación; retest autenticado y confirmar versión corregida. Excepciones deben tener riesgo aceptado, controles compensatorios y vencimiento.

## Casos prácticos
Cruzar un inventario sintético con CVE, KEV y EPSS. Dos activos comparten CVE, pero uno está expuesto a Internet y otro aislado; justificar orden de remediación con contexto. Simular parche fallido, rollback y mitigación compensatoria. Evaluar si el sistema explica por qué prioriza cada activo.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para FIRST CVSS/EPSS, CISA KEV, NVD, CPE y SSVC. Fijar versión del scoring y fecha de consulta; no tratar CVSS como probabilidad de explotación.
