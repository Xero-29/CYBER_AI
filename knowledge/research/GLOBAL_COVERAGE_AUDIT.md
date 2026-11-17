# Auditoría global de cobertura de conocimiento CYBER_AI

**Corte:** 2026-11-17  
**Estado:** línea base de mapeo; no es certificación de exhaustividad.

## Objetivo

Contrastar las 48 áreas del manifiesto con marcos, estándares, taxonomías, guías y especificaciones reconocidas. La matriz separa el mapeo temático de la profundidad real del contenido.

## Resultado de la línea base

- 48 áreas del manifiesto incorporadas al cruce.
- 61 familias de referencia identificadas.
- Las relaciones área–referencia indican relevancia temática, no cobertura profunda.
- Los 48 módulos conservan `content_depth_status: not_assessed_by_this_crosswalk`.
- Las referencias se catalogan como no leídas íntegramente.
- Se registran 8 brechas transversales prioritarias.

## Marcos de contraste

| Familia | Qué contrasta | Límite |
|---|---|---|
| NIST CSF 2.0 / NICE 2.2 | Resultados de riesgo y competencias | No prueban profundidad técnica |
| NIST SP 800 | Controles y guías especializadas | Cada publicación tiene alcance específico |
| MITRE ATT&CK / ATLAS / D3FEND | Comportamiento adversario, IA y defensas | No enumeran todas las amenazas |
| OWASP | Aplicaciones, API, móvil y LLM | Cobertura por proyecto |
| CIS Controls / Benchmarks | Salvaguardas y configuración | Requiere plataforma y versión |
| ISO/IEC, IEC, ETSI, 3GPP, CCSDS | Gestión y sectores especializados | Requiere edición y aplicabilidad |
| CVE, CWE, CVSS, CAPEC, KEV, EPSS | Vulnerabilidades, debilidades, severidad y explotación | No sustituyen análisis de riesgo |
| RFC / OASIS | Protocolos e intercambio de inteligencia | Se deben revisar especificaciones concretas |

## Brechas transversales

1. Regulación por país y sector: privacidad, finanzas, salud, infraestructura crítica, telecomunicaciones y notificación de incidentes.
2. Investigación académica: búsquedas sistemáticas, criterios de selección, evaluación de calidad y lectura integral.
3. Herramientas: catálogo vivo de herramientas OSS/comerciales, licencias, versiones, mantenimiento, adaptadores y pruebas.
4. Protocolos y versiones: inventario por protocolo, plataforma, edición, obsolescencia y conformidad.
5. Evidencia experimental: experimentos, baselines, métricas, estadística y reproducción independiente.
6. Sistemas críticos: OT, automoción, medicina, satélites, aeroespacial y seguridad física.
7. Cobertura regional y en español: normas nacionales, regulación local y fuentes oficiales.
8. Vigilancia de cambios: nuevas normas, CVE, advisories, papers y releases.

## Interpretación

- `mapped_scope_only`: hay referencias asociadas, no se ha medido profundidad.
- `partial_scope_only`: las referencias cubren una parte o son adyacentes.
- `not_assessed_by_this_crosswalk`: el contenido del pack no se ha evaluado semánticamente.
- Una referencia catalogada no equivale a documento leído.
- Un tema en un currículo no equivale a procedimiento implementado.
- Una herramienta en un inventario no equivale a herramienta operativa.
- No se calcula porcentaje de cobertura total porque no existe un universo completo y ponderado.

## Secuencia de cierre

1. Validar IDs entre manifiesto y matriz.
2. Descomponer cada dominio en subdominios y requisitos.
3. Verificar edición, vigencia, licencia, URL, integridad y texto completo.
4. Añadir fuentes académicas y revisiones sistemáticas.
5. Auditar contenido real por tema, no solo existencia de archivos.
6. Asociar competencias con procedimientos, laboratorios, herramientas, evidencias y pruebas.
7. Realizar revisión técnica, legal y de seguridad independiente.

## Archivos

- Matriz: `global_coverage_matrix.json`
- Auditor: `knowledge_global_coverage_audit.py`
- Pruebas: `tests/test_knowledge_global_coverage_audit.py`

## Fuentes institucionales iniciales

- NIST NICE 2.2.0: https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220
- NIST CSF 2.0: https://www.nist.gov/cyberframework
- MITRE ATT&CK Enterprise: https://attack.mitre.org/matrices/enterprise/
- MITRE ATT&CK Mobile: https://attack.mitre.org/matrices/mobile/
- MITRE ATT&CK ICS: https://attack.mitre.org/matrices/ics/
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1
- ISO/IEC 27001:2022: https://www.iso.org/standard/27001
- OWASP API Security: https://owasp.org/API-Security/
- OWASP GenAI: https://genai.owasp.org/

Los enlaces son puntos de partida institucionales; fijar la edición exacta y comprobar el texto antes de atribuir requisitos concretos.


## Matriz de requisitos verificables por especialidad — 2026-11-17

La versión 1.1.0 de `global_coverage_matrix.json` añade, para cada una de las 48 especialidades:

- Requisitos explícitos por cada tema técnico del currículo (sin convertirlos en contenido ya cubierto).
- Artefactos exigibles: arquitectura, inventario, modelo de amenazas, controles, procedimientos, laboratorio, caso práctico, evaluación y procedencia.
- Siete puertas de validación: fuentes, contenido técnico, procedimientos, herramientas, laboratorios, investigación y revisión independiente.
- Estados controlados: `not_assessed`, `in_progress`, `partially_validated`, `validated`, `not_applicable`.
- Para validar un elemento se exigen referencias de evidencia, revisor identificado y fecha.

### Línea base de requisitos

Todos los temas, artefactos y puertas empiezan en `not_assessed`. Esto es intencional: la matriz define qué debe probarse, no finge que ya está cubierto. No se calcula porcentaje global ni se declara ninguna especialidad validada.

El auditor ahora contrasta la matriz con el manifiesto y el currículo, verifica correspondencia exacta de temas/artefactos, valida estados y rechaza elementos marcados como validados sin evidencia, revisor y fecha.

### Criterio para declarar una especialidad completa

Una especialidad solo podrá declararse validada cuando cada requisito aplicable tenga contenido técnico suficiente, fuentes primarias vigentes y revisadas, procedimientos reproducibles, herramientas probadas cuando corresponda, laboratorio y casos prácticos con resultados, además de revisión independiente. Las áreas críticas (OT, automoción, medicina, satélites y sistemas físicos) requieren instalaciones autorizadas y análisis de seguridad funcional.

### Limitación

Esta ampliación crea una matriz auditable, no una biblioteca ya completada. La lista de subtemas procede del currículo vigente y sigue siendo un universo de trabajo acotado, no una enumeración demostrablemente exhaustiva de todo lo que existe en ciberseguridad.
