# Agenda de investigación: Seguridad de API

**Dominio:** `api` · **Nivel objetivo:** L4 investigación · **Madurez actual:** agenda propuesta, no investigación concluida.

## Problema de investigación

Investigar autorización, identidad de servicio, contratos, abuso de recursos y observabilidad en el contexto de Seguridad de API. La agenda identifica líneas de trabajo a partir del currículo del dominio; no afirma resultados empíricos ni sustituye una revisión sistemática de literatura.

## Pregunta central

¿Qué enfoques técnicos ofrecen la mejor combinación demostrable de seguridad, resiliencia, rendimiento, coste y operabilidad para Seguridad de API, bajo amenazas, arquitecturas y restricciones explícitas?

## Líneas de investigación por tema

### T1. REST, GraphQL, gRPC y contratos

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *REST, GraphQL, gRPC y contratos* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T2. OAuth 2.0, OIDC, JWT y tokens

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *OAuth 2.0, OIDC, JWT y tokens* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T3. BOLA, BFLA y autorización por objeto

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *BOLA, BFLA y autorización por objeto* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T4. rate limiting, cuotas y anti-automatización

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *rate limiting, cuotas y anti-automatización* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T5. validación de esquemas y mass assignment

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *validación de esquemas y mass assignment* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T6. mTLS, CORS, gateway y service mesh

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *mTLS, CORS, gateway y service mesh* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T7. inventario, versionado y retirada segura

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *inventario, versionado y retirada segura* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

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
