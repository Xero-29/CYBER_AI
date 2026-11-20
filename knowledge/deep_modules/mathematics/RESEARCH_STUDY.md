# Investigación técnica: Matemáticas, estadística y métodos cuantitativos para ciberseguridad

**ID:** mathematics · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación matemática especializada pendiente.

## Fundamentos necesarios
Álgebra lineal: vectores, matrices, espacios, autovalores, SVD, proyecciones y embeddings. Cálculo: derivadas, gradientes, optimización, integrales y ecuaciones diferenciales cuando aplique. Matemática discreta: lógica, conjuntos, relaciones, grafos, combinatoria, teoría de números y estructuras algebraicas. Probabilidad: variables aleatorias, distribuciones, Bayes, independencia, entropía y procesos estocásticos.

## Estadística aplicada
Diseño de muestreo, estimación, intervalos de confianza, tests de hipótesis, potencia, tamaño de muestra, regresión, correlación, causalidad, series temporales, supervivencia, detección de anomalías y análisis multivariado. Distinguir significancia estadística de importancia operacional. Corregir comparaciones múltiples y sesgo de selección.

## Criptografía
Teoría de números, grupos, anillos, campos finitos, curvas elípticas, retículas, teoría de información, complejidad y reducción de seguridad. Diferenciar intuición matemática de demostración formal. No diseñar algoritmos criptográficos basados solo en intuición o benchmarks.

## Grafos y redes
Modelar ataque paths, dependencias, identidad, trust relationships, propagation y network flows. Medir centralidad, conectividad, cut sets, reachability y riesgo de propagación. Un grafo incompleto produce conclusiones incompletas; documentar datos ausentes.

## Detección y ML
Precision/recall, ROC/PR, calibration, base rate, Bayes, anomaly scoring, drift, adversarial robustness y uncertainty. En SOC, falsos positivos por hora y coste de investigación suelen ser más útiles que una métrica agregada aislada.

## Métodos numéricos y reproducibilidad
Estabilidad, error de redondeo, condicionamiento, convergencia, optimización convexa/no convexa y simulación Monte Carlo. Registrar unidades, precisión, seeds, librerías y tolerancias.

## Laboratorios
Bayesian triage con datos sintéticos; detección de anomalías en series de logs; grafos de rutas de privilegios; simulación de propagación; evaluación estadística de IDS; ejemplos de RSA/ECC/PQC solo en entornos didácticos. Incluir soluciones y contraejemplos.

## Fuentes
- NIST AI 100-2 E2025 (AML taxonomy): https://doi.org/10.6028/NIST.AI.100-2e2025
- NIST FIPS 203/204/205: https://csrc.nist.gov/projects/post-quantum-cryptography
- NIST/SEMATECH Engineering Statistics Handbook: https://www.itl.nist.gov/div898/handbook/

**Límite:** currículo matemático aplicado, no un tratado completo; validar pruebas, supuestos y derivaciones con especialistas.
