# Agenda de investigación: Threat hunting

**Dominio:** `threat_hunting` · **Objetivo:** L4 investigación · **Estado:** plan, no resultados validados.

## Pregunta central

¿Cómo evaluar rigurosamente la eficacia, cobertura, precisión y resiliencia de Threat hunting en escenarios representativos, manteniendo control de falsos positivos, coste y riesgo operacional?

## Estudios por tema

### 1. hipótesis basadas en TTP

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de hipótesis basadas en TTP y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

### 2. calidad de telemetría

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de calidad de telemetría y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

### 3. KQL, Sigma y pivots

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de KQL, Sigma y pivots y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

### 4. líneas base y anomalías

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de líneas base y anomalías y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

### 5. validación de hipótesis

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de validación de hipótesis y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

### 6. detecciones persistentes

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de detecciones persistentes y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

### 7. cobertura y reproducibilidad

- **Pregunta:** ¿Qué condiciones de entorno, instrumentación y amenaza afectan la eficacia de cobertura y reproducibilidad y qué brechas no se detectan con las pruebas habituales?
- **Hipótesis:** un método con hipótesis de detección/defensa explícitas y validación con casos positivos y negativos mejora la cobertura o reduce falsos positivos frente a la baseline.
- **Diseño:** definir eventos/escenarios etiquetados; establecer ground truth; separar desarrollo y evaluación; incluir escenarios de borde; repetir; evitar fuga entre conjuntos; registrar versiones y fuentes.
- **Métricas:** precision, recall, F1/PR-AUC cuando aplique, falsos positivos por unidad de tiempo, tiempo de detección/respuesta, cobertura y coste.
- **Evidencia:** dataset sintético o autorizado, diccionario, reglas/modelos versionados, scripts, resultados y análisis de errores.

## Revisión bibliográfica

Buscar artículos revisados por pares, estándares, especificaciones y documentación oficial. Registrar consultas, bases, fecha, criterios de inclusión/exclusión y evaluación de calidad. Analizar sesgos de datasets, validez externa, drift, limitaciones y conflictos de interés.

## Experimento

Predefinir hipótesis, variables, conjunto de prueba, baseline, comparadores, ground truth, métricas y análisis estadístico. Fijar hardware/software/versiones/semillas. Mantener evaluación ciega cuando sea posible. Analizar errores por subgrupo y escenarios no vistos. Registrar incertidumbre y amenazas a validez.

## Entregables

Estado del arte; taxonomía; threat model; dataset y licencia/procedencia; protocolo; código y dependencias; configuración/SBOM/hashes; resultados; scripts de análisis; limitaciones; revisión independiente y reproducción.

## Seguridad y ética

Datos minimizados y autorizados; no recopilar telemetría personal sin base legal; proteger indicadores sensibles; usar escenarios aislados; definir kill switch y no desplegar experimentos de respuesta automática sin aprobación.

**Madurez:** `research_agenda_defined`. M4 necesita experimento y análisis; M5 necesita revisión y reproducción externa.
