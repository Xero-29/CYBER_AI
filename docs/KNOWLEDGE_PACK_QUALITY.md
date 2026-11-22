# Criterio de calidad para los 48 paquetes offline

## Estado actual

Los paquetes versionados contienen guías editoriales iniciales. No deben describirse como dossiers expertos ni como conocimiento científicamente validado. El manifiesto marca las 48 áreas como authored_foundation_unverified, con cero fuentes externas verificadas, sin evidencia de laboratorios ejecutados y sin aprobación independiente.

## Niveles de madurez

- foundation_draft: faltan secciones técnicas requeridas o el paquete no está disponible/seguro.
- awaiting_external_evidence: la estructura editorial está completa, pero faltan fuentes verificadas, laboratorio reproducible o revisión independiente.
- expert_ready: se cumplen todas las condiciones siguientes. Este estado no puede inferirse del número de palabras.

## Requisitos acumulativos para expert_ready

1. **Contenido técnico:** propósito/límites, fundamentos, arquitectura, modelo de amenazas, competencias, mecanismos técnicos, controles, metodología, ejemplos desarrollados, laboratorio, reproducibilidad, evaluación, fuentes verificables e instrucciones de seguridad para agentes.
2. **Fuentes:** al menos cinco fuentes HTTPS con título, editor, versión/fecha, licencia aprobada, fecha de verificación y evidencia de verificación. El registro debe ser trazable y no basta con enumerar nombres de estándares.
3. **Laboratorio:** al menos una ejecución aprobada con comando, alcance autorizado, entorno, fecha y SHA-256 de un artefacto reproducible.
4. **Revisión:** decisión aprobada por revisor independiente, identificador del revisor, fecha, commit revisado y evidencia de la revisión.
5. **No confundir estados:** contenido incluido, indexado, recuperable, comprendido y dominado son estados diferentes. La indexación no certifica comprensión ni capacidad operativa.

## Auditoría

~~~bash
python knowledge_pack_quality.py
python knowledge_pack_quality.py --json
python knowledge_pack_quality.py --area foundations --json
python knowledge_pack_quality.py --require-expert-ready
~~~

El comando normal es diagnóstico. --require-expert-ready devuelve código 1 mientras quede alguna especialidad sin validar; el código 2 indica un manifiesto inválido. El auditor no descarga fuentes, no verifica jurídicamente licencias, no ejecuta laboratorios ni sustituye la revisión humana.

## Regla de aceptación

Ningún módulo se aprueba por volumen, número de encabezados o mera presencia de una bibliografía. Debe enseñar fundamentos, explicar mecanismos, analizar escenarios, diseñar soluciones, incluir ejemplos reproducibles y superar validación independiente. La madurez teórica y la operativa se registran por separado.
