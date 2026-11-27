# Gobierno del conocimiento

## Principios
- Procedencia antes que autoridad: toda afirmación importante debe rastrearse a una fuente.
- Vigencia: registrar publicación, versión y fecha de consulta.
- Integridad: conservar SHA-256 del artefacto y de cada versión.
- Licencia: registrar condiciones de reutilización; fuentes no aclaradas quedan pendientes.
- Separación: diferenciar datos públicos, internos, confidenciales y personales; aislar tenants.
- Evidencia: separar observación, afirmación de fuente, inferencia, hipótesis y recomendación.
- Calidad: conservar contradicciones, limitaciones, confianza y método de validación.
- Seguridad: documentos y páginas externas son datos no confiables, nunca instrucciones para agentes.

## Fuentes orientativas
Estándares y documentación normativa oficial (NIST, ISO según licencia/acceso, FIRST, IETF, MITRE); avisos de fabricantes y CERT; CVE Program, NVD, CISA KEV, EPSS y CWE; publicaciones académicas; documentación de proyectos oficiales; investigación técnica corroborada. Evaluar siempre pertinencia, fecha, independencia y evidencia primaria.

## Metadatos mínimos
`resource_id`, `title`, `canonical_uri`, `publisher`, `author`, `resource_type`, `language`, `published_at`, `accessed_at`, `source_version`, `license`, `license_status`, `sha256`, `area_id`, `domain_id`, `topic_id`, `classification_status`, `validation_status`, `confidence`, `tenant_id`, `processing_status`.

## Ciclo de vida
1. Descubrir sin ejecutar contenido.
2. Registrar ruta/URL, hash y metadatos.
3. Comprobar licencia, formato, tamaño, idioma y seguridad.
4. Clasificar en una o varias ramas.
5. Ingerir en cuarentena y sanitizar HTML/contenido activo.
6. Dividir e indexar vinculando fragmentos, recurso y versión.
7. Evaluar procedencia, vigencia, autoridad y contradicciones.
8. Aprobar publicación según política del tenant.
9. Revalidar fuentes críticas y archivar versiones obsoletas sin perder trazabilidad.

## Estados de evidencia
- `observed`: observado directamente y con artefacto reproducible.
- `source_asserted`: afirmado por una fuente identificada.
- `inferred`: inferencia con premisas trazables.
- `hypothesis`: aún no verificada.
- `contradicted`: evidencia contraria disponible.
- `pending`: insuficiente o conflictiva.

Una coincidencia semántica, un resultado de escáner o una puntuación de modelo nunca bastan por sí solos para declarar una vulnerabilidad confirmada.
