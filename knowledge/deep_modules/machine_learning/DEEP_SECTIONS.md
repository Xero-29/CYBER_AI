# Secciones de profundización — Machine learning seguro

## Modelo de amenazas
Trazar fuentes y derechos de datos, labeling, preprocessing, features, entrenamiento, pesos, registry, serving, API, feedback y proveedores. Amenazas: poisoning, backdoor, data leakage, membership inference, model inversion, extracción, adversarial examples, drift, dependencia comprometida y abuso de GPU. Separar entrenamiento, evaluación e inferencia.

## Detección
Monitorear integridad/linaje de datasets, cambios de distribución, métricas por subgrupo, anomalías de inferencia, uso de recursos, acceso a pesos y cambios de pipeline. Detectar drift, poisoning, consultas de extracción y degradación selectiva. Registrar versión de modelo/datos y configuración sin almacenar información sensible innecesaria.

## Respuesta a incidentes
Retirar versión sospechosa, congelar promoción de modelos, preservar pesos, dataset, pipeline y logs, revocar credenciales y aislar artefactos. Reentrenar desde datos confiables, comparar con baseline y evaluar impacto sobre predicciones. Mantener rollback reproducible y revisar modelos derivados y copias exportadas.

## Casos prácticos
Crear dataset sintético con una pequeña proporción de etiquetas alteradas y evaluar cambio en métricas; comparar detector de poisoning y baseline. Segundo caso: consultas repetidas intentan extraer un clasificador; aplicar rate limits y detección, medir utilidad y falsos positivos. No usar datos reales sin autorización.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST AI RMF, MITRE ATLAS, papers de robustez y documentación de frameworks. Registrar dataset, seed, modelo, hardware y versión.
