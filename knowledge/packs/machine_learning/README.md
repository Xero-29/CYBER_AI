# Seguridad de aprendizaje automático — Guía de dominio

**ID:** `machine_learning` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege pipelines de datos, entrenamiento, evaluación, inferencia y despliegue ML tradicional. Cubre poisoning, leakage, extracción, inversión, membership inference, abuso de APIs y dependencia de modelos/artefactos. Los experimentos adversariales se realizan con datasets sintéticos y modelos propios.

## Competencias
- Inventariar datasets, modelos, pesos, tokenizers, features y pipelines.
- Controlar provenance, splits, etiquetas y calidad de datos.
- Evaluar privacidad, robustez, drift y comportamiento fuera de distribución.
- Proteger feature stores, endpoints, notebooks y experiment tracking.
- Gestionar acceso a modelos, cuotas y extracción masiva.
- Firmar artefactos y fijar dependencias de entrenamiento.
- Medir leakage, poisoning, fairness y estabilidad.

## Controles
- Dataset versionado, hash y linaje de origen.
- Separación de entrenamiento/validación/test para evitar leakage.
- Validación de etiquetas y detección de anomalías en datos.
- Artefactos firmados y registry con permisos.
- Endpoints autenticados, rate limits y límites de tamaño/coste.
- Minimización de datos y controles contra membership inference.
- Reproducibilidad con versiones de código, datos y entorno.
- Monitorización de drift, calidad y abuso.

## Metodología
1. Modelar amenazas por etapa del ciclo ML.
2. Validar fuentes, licencias, consentimiento y procedencia.
3. Analizar datasets por duplicados, sesgo y contaminación.
4. Entrenar con entorno aislado y dependencias fijadas.
5. Evaluar robustness y privacidad con datos sintéticos.
6. Revisar artefactos y permisos antes de publicar.
7. Probar endpoint frente a abuso, enumeración y extracción.
8. Monitorizar drift y comportamiento anómalo.
9. Mantener rollback de modelo y dataset.

## Laboratorio
Dataset sintético tabular y clasificador local. Simular label poisoning, data leakage y consultas excesivas; evaluar métricas antes/después y crear controles. No utilizar PII ni modelos de terceros sin permiso.

## Evaluación
Procedencia trazable, splits limpios, métricas reproducibles, endpoint limitado, artefactos firmados y proceso de rollback.

## Referencias
NIST AI RMF, MITRE ATLAS, OWASP ML Security Top 10, ISO/IEC 23894, Google Secure AI Framework y papers de adversarial ML.

## Instrucciones para agentes IA
No entrenes ni subas datasets con datos sensibles. Separa robustez, privacidad y fairness. No afirmes que un modelo es seguro por una sola métrica.