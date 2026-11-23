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
