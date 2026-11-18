# Agenda de investigación: PKI, certificados y HSM

**Dominio:** `pki_hsm` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta.

## Pregunta central

¿Cómo equilibrar seguridad, privacidad, equidad, resiliencia y utilidad en PKI, certificados y HSM, y qué evidencia permite comparar los enfoques sin ignorar el contexto social y legal?

## Estudios por tema

### 1. X.509 y cadena de confianza

**Pregunta:** ¿Qué propiedades de X.509 y cadena de confianza son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

### 2. CA y políticas CP/CPS

**Pregunta:** ¿Qué propiedades de CA y políticas CP/CPS son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

### 3. OCSP, CRL y CT

**Pregunta:** ¿Qué propiedades de OCSP, CRL y CT son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

### 4. HSM y ceremonia de claves

**Pregunta:** ¿Qué propiedades de HSM y ceremonia de claves son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

### 5. mTLS y code signing

**Pregunta:** ¿Qué propiedades de mTLS y code signing son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

### 6. rotación y expiración

**Pregunta:** ¿Qué propiedades de rotación y expiración son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

### 7. compromiso de CA

**Pregunta:** ¿Qué propiedades de compromiso de CA son observables y medibles, qué supuestos introducen sesgo y cómo varían entre poblaciones o escenarios?

**Hipótesis provisional:** una evaluación contextual, con métricas explícitas y análisis de error por segmento, mejora la calidad de decisión frente a un enfoque agregado.

**Método:** revisión de literatura y normativa; definir población, unidad de análisis y contexto; crear dataset minimizado/sintético; definir baseline y comparadores; medir errores, efectos no deseados y coste; realizar análisis de sensibilidad.

**Métricas:** precisión, recall, tasas de error por subgrupo, utilidad, coste/fricción, exposición de datos, explicabilidad y robustez, según aplique.

**Entregable:** protocolo, registro de datos y consentimiento/base legal, análisis de sesgos, resultados, limitaciones y scripts reproducibles.

## Estado del arte y ética

Buscar fuentes académicas, normas, legislación aplicable y documentación oficial. Registrar jurisdicción, fecha, versión, alcance y limitaciones. Evaluar calidad metodológica, sesgo de selección, representatividad, conflicto de interés y aplicabilidad. No sustituir asesoría jurídica por un resumen técnico.

## Diseño experimental

Predefinir hipótesis, población, muestreo, variables, métricas, comparadores, análisis estadístico y criterios de exclusión. Minimizar datos, anonimizar cuando sea posible y documentar base legal, retención y controles. Analizar incertidumbre y validez externa.

## Artefactos

Revisión de literatura; matriz de fuentes; protocolo; evaluación de impacto; dataset sintético/minimizado; código y entorno; métricas; resultados; análisis de sesgo; limitaciones; reproducción independiente.

## Madurez

M4 requiere estudio empírico y análisis crítico; M5 revisión y reproducción independiente. Estado actual: `research_agenda_defined`.
