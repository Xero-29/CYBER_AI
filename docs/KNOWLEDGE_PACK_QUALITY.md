# Criterio de calidad para los 48 paquetes offline

## Estado actual

Los paquetes versionados contienen guías editoriales iniciales. No deben describirse como dossiers expertos ni como conocimiento científicamente validado. El manifiesto marca las 48 áreas como authored_foundation_unverified, con cero fuentes externas verificadas, sin evidencia de laboratorios ejecutados y sin aprobación independiente.

## Niveles de madurez

- foundation_draft: faltan secciones técnicas requeridas o el paquete no está disponible/seguro.
- awaiting_external_evidence: la estructura editorial está completa, pero faltan fuentes verificadas, laboratorio reproducible o revisión independiente.
- expert_ready: se cumplen todas las condiciones siguientes. Este estado no puede inferirse del número de palabras.

## Requisitos acumulativos para expert_ready

1. **Contenido técnico:** propósito/límites, fundamentos, arquitectura, modelo de amenazas, competencias, mecanismos técnicos, controles, metodología, ejemplos desarrollados, laboratorio, reproducibilidad, evaluación, fuentes verificables e instrucciones de seguridad para agentes.
2. **Fuentes:** al menos cinco fuentes HTTPS con título, editor, versión/fecha, licencia aprobada, fecha de verificación y evidencia de verificación. Cada fuente debe apuntar a un artefacto de evidencia versionado mediante verification_evidence_path y verification_evidence_sha256. El auditor comprueba los bytes reales y rechaza hashes ausentes o incorrectos, URLs con credenciales, parámetros, fragmentos, IP no globales, IPv4 abreviado/numérico, hosts locales y nombres DNS malformados o de una sola etiqueta. La comprobación es sintáctica: no resuelve DNS ni sustituye el gateway de salida.
3. **Laboratorio:** al menos una ejecución aprobada con comando, alcance autorizado, entorno, fecha y SHA-256 de un artefacto reproducible. artifact_path debe resolver a un archivo regular dentro del repositorio y artifact_sha256 debe coincidir con su contenido real. Un hash escrito en JSON sin artefacto no cuenta.
4. **Revisión:** decisión aprobada por un revisor independiente, identificador, fecha, commit revisado y evidencia material. El registro incluye reviewed_pack_sha256, reviewed_sources_sha256 y reviewed_lab_evidence_sha256, todos ligados a los bytes exactos auditados. Cada elemento de evidence contiene path y sha256 y el auditor comprueba el archivo real.
5. **Firma independiente:** la revisión debe llevar una firma Ed25519 en Base64 sobre el JSON canónico UTF-8 de schema_version, area_id, decision, evidence, independent_review, reviewed_at, reviewed_commit, los tres hashes revisados y reviewer_id. El auditor verifica con OpenSSL (pkeyutl -verify -pubin -rawin) y una clave pública confiable provisionada fuera del repositorio. Requiere:
   - CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_PEM: clave pública PEM Ed25519.
   - CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_SHA256: SHA-256 exacto de los bytes PEM.
   - CYBER_AI_KNOWLEDGE_REVIEWER_ID: identidad esperada para esa clave.

   Si falta OpenSSL, la clave, su fingerprint o la identidad confiable, la revisión no se aprueba. La clave privada nunca debe entrar al repositorio ni al proceso que genera el paquete. El fingerprint y la asociación reviewer/key deben configurarse mediante un canal administrativo independiente.
6. **No confundir estados:** contenido incluido, indexado, recuperable, comprendido y dominado son estados diferentes. La indexación no certifica comprensión ni capacidad operativa.

El registro de revisión se invalida si cambia el paquete, el registro de fuentes, el registro de laboratorio o cualquiera de los artefactos firmados. Una revisión debe repetirse sobre los nuevos hashes.

El auditor carga el manifiesto y los registros JSON de fuentes, laboratorio y revisión con un parser estricto: rechaza claves duplicadas en cualquier nivel, NaN/Infinity y exponentes que desbordan o subdesbordan el rango `float`. Un documento JSON ambiguo o numéricamente no representable no aporta fuentes, laboratorios ni revisiones verificadas.

## Diagnóstico de bloqueos por especialidad

El informe JSON de `knowledge_pack_quality.py` incluye `readiness_blockers` para cada área. Los códigos son deliberadamente conservadores:

- `pack_missing_or_unsafe`: el paquete no existe, no es un archivo regular seguro o su ruta no supera la validación.
- `missing_required_sections`: faltan una o más de las secciones técnicas requeridas; el detalle está en `missing_sections`.
- `verified_sources_below_minimum`: hay menos de cinco fuentes que superan todas las comprobaciones de licencia, procedencia, fecha y hash de evidencia.
- `lab_evidence_missing_or_unverified`: no existe una ejecución aprobada vinculada a un artefacto real cuyo SHA-256 coincida.
- `independent_review_missing_or_untrusted`: no hay una revisión independiente válida ligada a los hashes exactos del paquete, fuentes y laboratorio y verificada con la clave pública Ed25519 configurada fuera del repositorio.
- El campo `external_evidence_pending` y el contador `external_evidence_pending_count` son independientes de `quality_status`: una especialidad puede seguir siendo `foundation_draft` por secciones incompletas y, simultáneamente, tener fuentes, laboratorio y revisión pendientes. Los contadores `source_evidence_pending_count`, `lab_evidence_pending_count` e `independent_review_pending_count` muestran cada categoría por separado. No interpretar `awaiting_external_evidence_count` como el total de áreas con evidencia pendiente: ese contador representa únicamente áreas cuya estructura editorial ya está completa.

Un área sin bloqueos solo significa que satisface las comprobaciones automatizadas definidas por este auditor. No demuestra por sí sola que un experto haya validado la corrección semántica, ni sustituye la revisión disciplinar independiente.

Comandos recomendados:

~~~bash
python3 knowledge_pack_quality.py
python3 knowledge_pack_quality.py --json
python3 knowledge_pack_quality.py --area foundations --json
python3 knowledge_pack_quality.py --require-expert-ready
~~~

El resultado de `knowledge_bootstrap.py` (documentos indexados/sin cambios/fallidos) mide el trabajo de ingesta; no cambia ni satisface los requisitos de calidad, fuentes, laboratorio o revisión independiente.

## Auditoría

~~~bash
python knowledge_pack_quality.py
python knowledge_pack_quality.py --json
python knowledge_pack_quality.py --area foundations --json
python knowledge_pack_quality.py --require-expert-ready
~~~

El comando normal es diagnóstico y devuelve código 0 cuando el manifiesto es estructuralmente válido, aunque existan borradores. --require-expert-ready devuelve código 1 mientras quede alguna especialidad sin validar; el código 2 indica un manifiesto inválido. verify.sh ejecuta el diagnóstico para detectar corrupción y rutas inseguras, pero no fuerza que las 48 áreas estén aprobadas.

El auditor no descarga fuentes, no determina por sí solo la legalidad de una licencia, no ejecuta laboratorios ni sustituye la revisión humana. La firma demuestra que la clave configurada aprobó un payload concreto; la organización debe custodiar esa clave, validar la identidad del revisor y comprobar que la segregación de funciones sea real. No constituye certificación científica ni autorización operativa.

## Regla de aceptación

Ningún módulo se aprueba por volumen, número de encabezados o mera presencia de una bibliografía. Debe enseñar fundamentos, explicar mecanismos, analizar escenarios, diseñar soluciones, incluir ejemplos reproducibles y superar validación independiente. La madurez teórica y la operativa se registran por separado.
