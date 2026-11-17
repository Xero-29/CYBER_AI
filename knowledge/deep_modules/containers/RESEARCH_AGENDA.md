# Agenda de investigación: Contenedores y Kubernetes

**Dominio:** `containers` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta, no investigación concluida.

## Problema y pregunta central

Investigar runtime isolation, image provenance, orchestration and workload policy para Contenedores y Kubernetes. ¿Qué enfoques técnicos ofrecen mejoras medibles de seguridad, resiliencia y operabilidad bajo amenazas, arquitecturas y restricciones explícitas?

## Líneas de investigación

### T1: namespaces, cgroups, seccomp y capabilities

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de namespaces, cgroups, seccomp y capabilities a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T2: imágenes, registries, firmas y SBOM

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de imágenes, registries, firmas y SBOM a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T3: Docker daemon y runtime

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de Docker daemon y runtime a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T4: Kubernetes RBAC y admission

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de Kubernetes RBAC y admission a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T5: network policies, secrets y etcd

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de network policies, secrets y etcd a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T6: supply chain y control plane

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de supply chain y control plane a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
- **Hipótesis provisional:** controles explícitos y verificables mejoran una métrica de seguridad predefinida frente a una línea base, con costes medibles en rendimiento, complejidad o usabilidad. Reformular tras revisar literatura.
- **Método:** definir versiones y alcance; establecer baseline; variar una variable por ensayo; controlar factores de confusión; incluir casos positivos, negativos y límite; repetir; guardar datos, logs y hashes.
- **Métricas candidatas:** eficacia, cobertura, falsos positivos/negativos, latencia/coste, robustez y reproducibilidad. Justificar selección y medición.
- **Evidencia:** revisión de literatura, protocolo, datos sintéticos/autorizados, resultados, incertidumbre, limitaciones y artefactos replicables.

### T7: detección y respuesta runtime

- **Pregunta:** ¿Cómo afectan las decisiones de diseño, implementación y configuración de detección y respuesta runtime a la seguridad y fiabilidad, y cómo medirlo de forma reproducible?
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
