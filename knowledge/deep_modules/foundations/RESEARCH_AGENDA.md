# Agenda de investigación: Fundamentos

**Dominio:** `foundations` · **Nivel objetivo:** L4 investigación · **Madurez actual:** agenda propuesta, no investigación concluida.

## Problema de investigación

Investigar comparación de modelos, evaluación de controles y gestión de incertidumbre en el contexto de Fundamentos. La agenda identifica líneas de trabajo a partir del currículo del dominio; no afirma resultados empíricos ni sustituye una revisión sistemática de literatura.

## Pregunta central

¿Qué enfoques técnicos ofrecen la mejor combinación demostrable de seguridad, resiliencia, rendimiento, coste y operabilidad para Fundamentos, bajo amenazas, arquitecturas y restricciones explícitas?

## Líneas de investigación por tema

Las líneas quedan alineadas exactamente con los siete IDs curriculares y con los protocolos LAB-FND-01A a LAB-FND-07A del desarrollo disciplinar. Las hipótesis son propuestas, no resultados.

### T1 — `foundations-01`: Modelos de seguridad y confianza
**Pregunta:** ¿la evaluación centralizada más enforcement local reduce decisiones de autorización obsoletas bajo cambios de atributos y revocación?
**H1:** versionado de políticas y expiración explícita reduce decisiones obsoletas frente a cachés sin invalidación.
**Diseño:** simulador con IdP, PDP/PEP, atributos mutables, revocación y fallos de red; medir decisiones erróneas, latencia y disponibilidad.

### T2 — `foundations-02`: Inventario y clasificación de activos
**Pregunta:** ¿la reconciliación multi-fuente mejora cobertura sin elevar falsos merges?
**H1:** identificadores fuertes más reconciliación supervisada mejoran F1 frente a hostname como clave única.
**Diseño:** dataset sintético con duplicados, clones, activos efímeros, huérfanos y cambios de nombre; comparar reglas y baseline de clave única.

### T3 — `foundations-03`: Superficie de ataque y modelado de amenazas
**Pregunta:** ¿DFD más análisis de abuso detecta rutas críticas omitidas por STRIDE sin modelo de flujo?
**H1:** el enfoque combinado reduce omisiones de rutas del ground truth.
**Diseño:** arquitecturas sintéticas multi-tier; revisión ciega por dos evaluadores; medir cobertura, falsos positivos, severidad de omisiones y acuerdo interevaluador.

### T4 — `foundations-04`: Identidad y control de acceso
**Pregunta:** ¿credenciales efímeras y permisos mínimos reducen exposición de workloads sin degradar disponibilidad?
**H1:** reducir duración y alcance de credenciales disminuye ventana de exposición con degradación operacional dentro de umbral predefinido.
**Diseño:** IdP y workloads simulados; medir permisos efectivos, revocación, fallos legítimos, latencia y recuperación.

### T5 — `foundations-05`: Criptografía y protección de datos
**Pregunta:** ¿qué política de rotación y recuperación minimiza exposición de claves sin aumentar pérdida de disponibilidad?
**H1:** rotación automatizada con recuperación ensayada reduce exposición acumulada frente a rotación manual sin ensayo.
**Diseño:** KMS simulado, claves ficticias, fallos de operador/proveedor; medir tiempo de rotación, fallos de recuperación, disponibilidad y errores.

### T6 — `foundations-06`: Detección, respuesta y recuperación
**Pregunta:** ¿qué campos de telemetría permiten reconstrucción robusta bajo pérdida, retraso y duplicación de eventos?
**H1:** identidad, recurso, acción, timestamp sincronizado, resultado y origen mejoran reconstrucción frente a registros incompletos.
**Diseño:** trazas sintéticas con ground truth; variar pérdida y desorden; medir secuencias correctas, atribución, FPR/FNR y tiempo de análisis.

### T7 — `foundations-07`: Gobierno, riesgo y aseguramiento
**Pregunta:** ¿la trazabilidad requisito–control–prueba–evidencia detecta controles no operativos mejor que un checklist documental?
**H1:** pruebas basadas en escenarios detectan más fallos reproducibles que revisión de checklist aislada.
**Diseño:** caso organizacional sintético con evidencias caducadas/contradictorias; evaluación ciega; medir falsos cierres, cobertura y acuerdo entre revisores.

## Método transversal

1. Formular pregunta delimitada, alcance, hipótesis falsable y criterios de refutación.
2. Ejecutar búsqueda bibliográfica reproducible: repositorios académicos, normas, advisories y documentación primaria; registrar términos, bases, fecha y criterios de selección.
3. Clasificar evidencia por tipo, autoridad, actualidad, método, sesgo y reproducibilidad.
4. Sintetizar estado del arte, taxonomía, desacuerdos, limitaciones y brecha de conocimiento.
5. Diseñar experimento con baseline, comparadores, variables, muestras, versiones, repeticiones y métricas justificadas.
6. Ejecutar solo en laboratorio aislado o activos autorizados; preservar cadena de custodia y minimización de datos.
7. Analizar resultados, intervalos de confianza cuando proceda, falsos positivos/negativos y amenazas a validez.
8. Publicar artefactos, configuración, dependencias, hashes, datos permitidos y procedimiento de reproducción.
9. Solicitar revisión técnica independiente y reproducción por otro operador antes de declarar M5.

## Entregables de investigación

- Revisión de literatura con estrategia y tabla de evidencia.
- Estado del arte y taxonomía comparativa.
- Preguntas, hipótesis, variables y protocolo pre-registrado cuando sea viable.
- Arquitectura del experimento, threat model y análisis de riesgos.
- Dataset sintético o autorizado, diccionario de datos y procedencia.
- Código, configuración, dependencias fijadas, SBOM y hashes.
- Resultados brutos saneados, análisis, gráficos/tablas y scripts.
- Discusión, limitaciones, amenazas a validez y trabajo futuro.
- Revisión independiente y registro de reproducción.

## Seguridad y ética

Autorización escrita para toda evaluación activa; alcance, exclusiones, límites de impacto y kill switch. No probar infraestructura de terceros, sistemas críticos ni dispositivos físicos en producción. En OT, automoción, satélites y hardware, usar simuladores o bancos de prueba. No publicar secretos, datos personales ni artefactos peligrosos sin saneamiento y revisión.

## Estado editorial

`research_agenda_defined` — preguntas y diseño inicial propuestos. No equivale a estado del arte terminado, paper reproducido ni resultado validado. Para avanzar a M4 se requiere literatura revisada, experimento ejecutado y análisis; M5 requiere revisión y reproducción externa.
