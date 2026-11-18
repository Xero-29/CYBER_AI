# Agenda de investigación: Seguridad cloud

**Dominio:** `cloud` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta, no investigación concluida.

## Problema y pregunta central

Investigar IAM, control planes, tenant isolation and cloud-native attack surface para Seguridad cloud. ¿Qué enfoques técnicos ofrecen mejoras medibles de seguridad, resiliencia y operabilidad bajo amenazas, arquitecturas y restricciones explícitas?

## Líneas de investigación

### T1: responsabilidad compartida y landing zones

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de responsabilidad compartida y landing zones a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T2: IAM, federación y guardrails

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de IAM, federación y guardrails a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T3: VPC/VNet, endpoints y egress

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de VPC/VNet, endpoints y egress a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T4: KMS, secretos y ciclo de claves

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de KMS, secretos y ciclo de claves a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T5: storage, snapshots y exposición pública

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de storage, snapshots y exposición pública a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T6: audit logs y postura cloud

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de audit logs y postura cloud a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T7: IaC, drift y respuesta

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de IaC, drift y respuesta a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

## Método de investigación

1. Delimitar pregunta, hipótesis falsable, alcance y criterios de refutación.
2. Buscar literatura en repositorios académicos, estándares, advisories y documentación primaria; registrar consultas, fecha y criterios de inclusión/exclusión.
3. Clasificar evidencia por autoridad, actualidad, método, sesgo, reproducibilidad y conflicto de interés.
4. Construir estado del arte, taxonomía, desacuerdos y brecha de conocimiento.
5. Diseñar experimento con baseline, comparadores, variables, muestras, versiones, repeticiones y métricas.
6. Ejecutar en laboratorio aislado o activos autorizados; minimizar datos y conservar integridad.
7. Analizar resultados, incertidumbre, falsos positivos/negativos y amenazas a validez.
8. Publicar código/configuración/dependencias fijadas/SBOM/hashes/datos permitidos y guía de reproducción.
9. Solicitar revisión independiente y reproducción externa antes de M5.

## Entregables

Revisión de literatura; tabla de evidencia; estado del arte; modelo de amenazas; protocolo; dataset y diccionario; código y entorno fijado; resultados y scripts; discusión; limitaciones; amenazas a validez; trabajo futuro; revisión y reproducción.

## Seguridad y ética

Autorización escrita para pruebas activas, alcance, exclusiones, límites y criterio de parada. No probar sistemas de terceros ni infraestructura crítica en producción. En sistemas físicos usar simuladores o bancos aislados. Sanear secretos y datos personales.

## Madurez

`research_agenda_defined`: agenda propuesta; no acredita literatura revisada, experimento ejecutado ni resultado validado. M4 exige estudio y análisis empírico; M5 exige revisión y reproducción externa.
