# CYBER_AI — Contexto del proyecto

## Objetivo
Crear una herramienta ligera de ciberseguridad para identificar,
clasificar y documentar vulnerabilidades, con el fin de participar
en programas Bug Bounty y, posteriormente, ofrecer servicios
profesionales de auditoría autorizada.

## Restricciones
- Equipo actual: Intel Core i5-4200M, 16 GB RAM y SSD.
- Sistema: Ubuntu, Python 3.12.3.
- Presupuesto reducido.
- Priorizar herramientas existentes y automatización.
- Evitar entrenar modelos grandes o construir infraestructura innecesaria.

## Arquitectura prevista
1. Detección: herramientas de seguridad existentes.
2. Verificación: módulo activado cada vez que se genera un informe.
3. Inteligencia de vulnerabilidades: consulta fuentes públicas como
   NVD/CVE para encontrar coincidencias conocidas.
4. Clasificación: distinguir hallazgos conocidos, posibles novedades,
   duplicados y casos pendientes de validación.
5. Estado de solución: registrar si existe parche, no existe o
   todavía no se ha podido determinar.
6. Informes: guardar evidencias, referencias y recomendaciones.
7. Automatización: conectar el verificador al flujo de informes.

## Reglas fundamentales
- No descartar una vulnerabilidad únicamente porque no tenga parche.
- Una búsqueda sin coincidencias no demuestra que sea nueva.
- Una coincidencia por palabras no demuestra que sea el mismo fallo.
- No afirmar que existe o no existe un parche sin evidencia suficiente.
- Marcar como pendientes los casos que no puedan verificarse.
- Ejecutar pruebas únicamente en sistemas propios o autorizados.
- Mantener los módulos independientes y ligeros.

## Estado actual
- Estructura creada: reports/ y data/.
- Verificador inicial: verifier.py, consulta la API pública de NVD.
- El verificador inicial todavía no está conectado automáticamente
  al generador de informes.
- No se ha confirmado todavía una consulta real exitosa a NVD.

## Próximas tareas
1. Comprobar y mejorar verifier.py.
2. Añadir registro de resultados y deduplicación.
3. Consultar fuentes públicas para verificar referencias y parches.
4. Integrar la verificación al generar cada informe.
5. Añadir pruebas y documentación mínima de uso.

## Instrucciones para Codex
Lee este archivo antes de modificar el proyecto.
Inspecciona los archivos existentes y evita sobrescribir trabajo útil.
Implementa la solución funcional más sencilla, sin dependencias
innecesarias. Ejecuta pruebas y actualiza este contexto al terminar.

## Progreso
- Paso 4/12: estructura básica y pruebas automáticas iniciales.
- Pruebas: comprobación de carpetas, verificador y archivo de contexto.
- Seguridad: analizar únicamente sistemas propios o con autorización.

- Paso 5/12: añadido report_analyzer.py para extraer referencias CVE y generar análisis JSON.
- Los hallazgos sin CVE quedan pendientes; no se declaran vulnerabilidades nuevas automáticamente.
- El estado del parche queda como no verificado hasta disponer de evidencia.
- Pruebas añadidas para referencias CVE, clasificación y estado del parche.

- Paso 6/12: creado cyber_ai.py como punto de entrada de la herramienta.
- Incluye comprobación básica y análisis de informes mediante --report.
- Pruebas: entrada principal y manejo de informe inexistente.

- Paso 7/12: probado el flujo de análisis con un informe de ejemplo.
- Validado el JSON generado, la extracción de CVE y el estado de parche no verificado.

- Paso 8/12: añadido nvd_client.py para comprobar identificadores CVE exactos en NVD.
- El análisis de informes incorpora la respuesta de NVD cuando existe conexión.
- Si la consulta falla, el estado queda pendiente; el parche sigue sin verificar.
- Pruebas de NVD realizadas con respuestas simuladas, sin depender de Internet.

- Paso 9/12: añadido índice local de informes y detección de duplicados exactos por huella SHA-256.
- Los duplicados se marcan como posibles duplicados; no se comparan todavía vulnerabilidades semánticamente.

- Paso 10/12: añadido batch_analyzer.py para procesar lotes de informes TXT y Markdown.
- Cada informe genera su JSON de análisis; errores de lectura se registran por archivo.\n
- Paso 11/12: integrado el comando --batch en cyber_ai.py.
- La herramienta puede analizar un informe individual o una carpeta completa.
- Añadidas pruebas de procesamiento por lotes y manejo de carpetas inexistentes.


## Uso de la herramienta
- Analizar un informe: `python3 cyber_ai.py --report reports/informe.txt`
- Analizar una carpeta: `python3 cyber_ai.py --batch reports`
- Comprobar instalación: `python3 cyber_ai.py --self-test`
- Ejecutar pruebas: `python3 -m unittest discover -s tests -v`

## Limitaciones
- Las coincidencias CVE requieren validación manual.
- El estado del parche permanece sin verificar automáticamente.
- Una búsqueda sin resultados no demuestra que exista una vulnerabilidad nueva.
- La detección de duplicados compara el texto normalizado, no la causa técnica.
- Ejecutar pruebas de seguridad únicamente con autorización.

- Paso 12/12: integración final, compilación, pruebas automáticas y prueba funcional.
- Estado: revisar los resultados de las pruebas antes de considerar la herramienta validada.
