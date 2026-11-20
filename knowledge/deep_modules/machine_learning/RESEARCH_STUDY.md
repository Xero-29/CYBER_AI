# Investigación técnica: Aprendizaje automático e ingeniería de IA

**ID:** machine_learning · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Experimentos y evaluación estadística pendientes.

## Ciclo de vida
Modelar adquisición de datos, labeling, limpieza, feature engineering, entrenamiento, validación, selección, despliegue, inferencia, monitoreo, actualización y retirada. Registrar dataset lineage, versiones, licencias, consentimiento/base legal, representatividad, sesgos, splits y leakage. El rendimiento offline no garantiza generalización a producción.

## Fundamentos
Dominar álgebra lineal, cálculo, probabilidad, estadística, optimización, teoría de información, aprendizaje supervisado/no supervisado/self-supervised, reinforcement learning, deep learning, transformers, embeddings, modelos generativos y evaluación. Comprender overfitting, underfitting, bias-variance, regularización, calibration, drift, distribution shift y causalidad.

## Evaluación
Separar train/validation/test por entidad/tiempo para evitar leakage. Elegir métricas por tarea: precision/recall/F1, ROC/PR-AUC, calibration, log loss, RMSE/MAE, ranking, robustness y utility. Informar intervalos de confianza, tamaño de muestra, baseline, seeds, hyperparameters y ablation studies. No comparar resultados con datasets o splits incompatibles.

## Seguridad adversarial
NIST AI 100-2 E2025 (marzo 2025) actualiza la taxonomía de adversarial ML e incluye predictive y generative AI, evasion, poisoning, privacy y misuse; usar esta edición y marcar E2023 como histórica. Evaluar data poisoning, backdoors, evasion, model extraction, membership inference, inversion, prompt injection, supply chain y misuse. Mitigaciones tienen límites; medir robustez bajo threat model explícito.

## MLOps y supply chain
Versionar código, datos, pesos, tokenizer, features, pipelines y dependencias; registrar hashes, origen, licencia, builder y entorno. Asegurar artefactos, secrets, model registry, endpoints, monitoring y rollback. Proteger datasets/embeddings contra contaminación y acceso cross-tenant.

## Laboratorios
Dataset sintético con drift, imbalance, poisoning y adversarial examples; entrenar baseline y robust model; comparar métricas y calibration; evaluar leakage y membership inference con datos sintéticos. Registrar hardware, seed, framework, commit, weights hash y scripts.

## Fuentes
- NIST AI 100-2 E2025: https://doi.org/10.6028/NIST.AI.100-2e2025
- NIST AI RMF: https://doi.org/10.6028/NIST.AI.100-1
- NIST GenAI Profile: https://doi.org/10.6028/NIST.AI.600-1
- OWASP LLM Top 10: https://owasp.org/projects/top-10-for-large-language-model-applications

**Límite:** resultados de laboratorio no generalizan sin validación externa y monitoreo de distribución.
