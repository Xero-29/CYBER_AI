# Secciones de profundización — Matemáticas aplicadas a ciberseguridad

## Modelo de amenazas
La amenaza matemática incluye supuestos erróneos, datos sesgados, estimaciones fuera de dominio, errores numéricos y modelos que confunden correlación con causalidad. En criptografía, explicitar adversario, seguridad formal, parámetros y supuestos; en riesgo, población y horizonte; en ML, distribución y función de pérdida. Toda inferencia debe declarar incertidumbre y condiciones de validez.

## Detección
Evaluar precision, recall, FPR/FNR, PR-AUC, calibración, drift, intervalos de confianza y prevalencia. Para grafos, detectar comunidades, centralidad y rutas de ataque sin asumir que centralidad implica riesgo. En anomalías, comparar baseline y distribución temporal. Evitar umbrales sin validación y métricas agregadas que oculten subgrupos.

## Respuesta a incidentes
Cuando una métrica o modelo falla, detener automatización de alto impacto, preservar datos/versiones, recalibrar con muestras representativas y comunicar incertidumbre. No tomar decisiones disciplinarias o de bloqueo irreversible basadas únicamente en score. Documentar cambios, sensibilidad y criterios de reactivación.

## Casos prácticos
Evaluar detector con conjunto sintético desbalanceado: construir matriz de confusión, precision/recall, PR-AUC e intervalo de confianza; variar prevalencia y umbral. Comparar dos clasificadores con el mismo split temporal y analizar drift. Publicar notebook, seed, versiones y limitaciones.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST AI RMF, literatura estadística, NIST cryptographic standards y documentación de métodos. Las métricas no sustituyen el modelo de amenaza.
