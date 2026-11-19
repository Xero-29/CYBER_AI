# Agenda de investigación: Fundamentos

**Dominio:** `foundations` · **Nivel objetivo:** L4 investigación · **Madurez actual:** agenda propuesta, no investigación concluida.

## Problema de investigación

Investigar comparación de modelos, evaluación de controles y gestión de incertidumbre en el contexto de Fundamentos. La agenda identifica líneas de trabajo a partir del currículo del dominio; no afirma resultados empíricos ni sustituye una revisión sistemática de literatura.

## Pregunta central

¿Qué enfoques técnicos ofrecen la mejor combinación demostrable de seguridad, resiliencia, rendimiento, coste y operabilidad para Fundamentos, bajo amenazas, arquitecturas y restricciones explícitas?

## Líneas de investigación por tema

Las preguntas siguientes son agendas propuestas. No son resultados ni conclusiones; deben afinarse después de revisar literatura primaria y delimitar una población o sistema experimental.

### T1. Modelos de seguridad y confianza

**Pregunta:** ¿Qué errores de arquitectura aparecen con mayor frecuencia al definir límites de confianza en aplicaciones con varios servicios, identidades y proveedores?

**Hipótesis falsable:** un análisis basado en flujos de datos y fronteras de confianza identifica más rutas de acceso no previstas que una revisión de componentes aislados, bajo el mismo tiempo de análisis.

**Diseño:** construir modelos sintéticos equivalentes; asignar evaluadores; comparar rutas descubiertas, falsos positivos, tiempo y acuerdo entre evaluadores. Predefinir criterios de ruta válida.

### T2. Inventario y clasificación de activos

**Pregunta:** ¿Qué combinación de fuentes pasivas mejora cobertura, atribución y frescura de inventario en entornos híbridos sin introducir escaneo intrusivo?

**Hipótesis falsable:** la reconciliación de CMDB, cloud inventory, identidad, EDR y DNS reduce activos no atribuidos frente a una única fuente, bajo un alcance y periodo definidos.

**Diseño:** dataset sintético con activos duplicados, efímeros, huérfanos y mal etiquetados; comparar fuentes individuales y combinadas; medir precisión, recall, duplicados y latencia.

### T3. Superficie de ataque y modelado de amenazas

**Pregunta:** ¿Qué combinación de DFD, STRIDE y árboles de ataque produce escenarios más completos y accionables para una arquitectura multi-tier?

**Hipótesis falsable:** combinar DFD y análisis de abuso reduce omisiones de rutas entre componentes frente a STRIDE aplicado sin modelo de flujo.

**Diseño:** casos sintéticos con ground truth elaborado por expertos; evaluación ciega; medir cobertura, falsos positivos, severidad de omisiones y acuerdo interevaluador.

### T4. Identidad, privilegios y autenticación

**Pregunta:** ¿Qué patrones de identidad no humana producen mayor exposición por exceso de privilegios, duración de credenciales y ausencia de propietario?

**Hipótesis falsable:** credenciales efímeras y scopes mínimos reducen la ventana de exposición en escenarios controlados frente a secretos estáticos de larga duración, sin degradar la función prevista fuera de umbral.

**Diseño:** laboratorio con identidades de servicio simuladas; medir duración de credenciales, permisos efectivos, revocación, disponibilidad y fallos de autorización.

### T5. Seguridad de redes y sistemas

**Pregunta:** ¿Qué fallos de segmentación lógica persisten cuando se consideran rutas administrativas, identidades y dependencias además de reglas de firewall?

**Hipótesis falsable:** un modelo de flujos e identidades descubre caminos no contemplados por una revisión exclusiva de reglas de red.

**Diseño:** topología simulada con rutas directas/indirectas, cuentas administrativas y servicios compartidos; comparar revisión de reglas con análisis combinado; medir rutas válidas omitidas.

### T6. Gestión de vulnerabilidades

**Pregunta:** ¿Cómo cambia la priorización cuando CVSS, EPSS, exposición, criticidad del activo y controles compensatorios se analizan conjuntamente?

**Hipótesis falsable:** un modelo contextual produce un orden de remediación más alineado con pérdidas simuladas que el orden por CVSS aislado.

**Diseño:** dataset sintético con etiquetas de impacto y escenarios; comparar ranking CVSS, ranking contextual y revisión experta; medir precision@k, estabilidad y sensibilidad a supuestos. No presentar dataset sintético como evidencia de eficacia real.

### T7. Telemetría, respuesta y recuperación

**Pregunta:** ¿Qué campos de telemetría son mínimos para reconstruir una secuencia de acciones y atribuirla de forma reproducible?

**Hipótesis falsable:** eventos con identidad, recurso, acción, timestamp sincronizado, resultado y origen permiten mayor reconstrucción correcta que logs sin uno o más de esos campos.

**Diseño:** generar trazas sintéticas con pérdida, retraso y alteración de eventos; medir completitud de reconstrucción, atribución correcta, falsos enlaces y tiempo de análisis.

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
