# Matemáticas para ciberseguridad — Guía de dominio

**ID:** `mathematics` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Proporciona fundamentos matemáticos para criptografía, detección, análisis de riesgo, grafos, anomalías y aprendizaje automático. Los resultados matemáticos deben vincularse a supuestos y contexto; una fórmula no valida por sí sola un sistema real.

## Competencias
- Probabilidad, estadística, inferencia y teoría de información.
- Álgebra lineal, vectores, matrices, espacios y reducción dimensional.
- Teoría de números, grupos, anillos, campos y aritmética modular.
- Grafos, caminos, centralidad y análisis de dependencias.
- Optimización, complejidad, algoritmos y teoría de juegos.
- Series temporales, detección de anomalías y calibración.
- Cuantificación de incertidumbre y análisis bayesiano.

## Aplicaciones
- Criptografía: entropía, grupos, curvas, factorización y seguridad de parámetros.
- Detección: tasas base, precisión/recall, ROC/PR y coste de falsos positivos.
- Threat modeling: grafos de ataque, rutas y propagación de privilegios.
- Riesgo: escenarios, sensibilidad, intervalos y distribución de pérdidas.
- ML: regularización, overfitting, drift y calibración probabilística.
- Forense: correlación temporal y análisis de evidencia con incertidumbre.

## Metodología
1. Definir pregunta y variables observables.
2. Declarar supuestos y dominio de validez.
3. Seleccionar modelo matemático apropiado.
4. Comprobar unidades, límites y casos extremos.
5. Validar con datos sintéticos y análisis de sensibilidad.
6. Comparar con baseline y medir error.
7. Explicar incertidumbre y reproducibilidad.
8. Evitar extrapolaciones fuera del dominio.

## Laboratorio
Construir un detector de anomalías sobre series sintéticas. Comparar umbral fijo, z-score y modelo robusto; medir precisión/recall con distintas tasas base. Resolver un ejercicio de aritmética modular y explicar por qué no constituye un algoritmo criptográfico seguro.

## Evaluación
Supuestos explícitos, cálculo reproducible, unidades correctas, límites documentados y métricas interpretadas en contexto.

## Referencias
NIST Statistical Methods, Handbook of Applied Cryptography, Introduction to Algorithms, Applied Cryptography y material universitario de probabilidad/álgebra.

## Instrucciones para agentes IA
Muestra derivaciones cuando importen. No inventes parámetros ni probabilidades. Distingue demostración matemática, estimación estadística y evidencia empírica.

## Arquitectura
La evaluación cuantitativa de seguridad debe definir sistema, variables observables, supuestos, distribución de amenazas, datos, modelo y decisión. En criptografía, distinguir problemas matemáticos, parámetros, reducciones, supuestos y modelo de adversario; en riesgo, separar probabilidad, impacto e incertidumbre; en detección, definir población base, tasa de prevalencia, sensibilidad, especificidad y coste de errores. Documentar unidades, dominios, condiciones de borde y límites de validez antes de aplicar una fórmula o interpretar una métrica.

## Controles
Verificar derivaciones y unidades de forma independiente; usar aritmética de precisión adecuada; fijar semillas y versiones en experimentos; separar datos de entrenamiento/prueba; evitar fuga de información; informar intervalos de confianza y tamaños de muestra; analizar sensibilidad y supuestos; someter primitivas criptográficas a bibliografía y estándares reconocidos, sin diseñar algoritmos propios para producción. Una métrica aislada no sustituye el modelo de amenaza ni la revisión experta.
