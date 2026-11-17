# Protocolo de investigación técnica para la biblioteca CYBER_AI

**Versión:** 1.0.0  
**Estado:** estándar editorial y metodológico; su adopción no implica que cada dominio ya esté investigado.

## 1. Qué significa nivel de investigación

Un módulo alcanza madurez de investigación solo cuando contiene: revisión de literatura con trazabilidad; pregunta de investigación delimitada; estado del arte y taxonomía; modelo/hipótesis; metodología replicable; datos y entorno descritos; resultados medidos; análisis de incertidumbre y amenazas a la validez; comparación con baselines; artefactos reproducibles; revisión técnica independiente y limitaciones explícitas.

No se considera investigación una colección de enlaces, un resumen generado sin fuentes, una guía genérica ni un laboratorio sin métricas y evidencia.

## 2. Método obligatorio por dominio

1. **Delimitar:** alcance, activos, población/sistemas, contexto, supuestos, exclusiones y pregunta de investigación.
2. **Buscar literatura:** priorizar normas y publicaciones primarias, documentación oficial, artículos revisados por pares, repositorios académicos y avisos técnicos del fabricante/proyecto. Registrar términos, bases consultadas, fecha y criterios de inclusión/exclusión.
3. **Evaluar evidencia:** distinguir norma, especificación, paper, documentación, advisory, blog y opinión. Valorar autoridad, actualidad, método, reproducibilidad, sesgo y conflicto de interés.
4. **Sintetizar estado del arte:** taxonomía, enfoques competidores, resultados publicados, desacuerdos, vacíos y líneas futuras. No copiar textos protegidos; resumir y citar.
5. **Plantear hipótesis:** hipótesis falsables, variables independientes/dependientes, factores de confusión y criterios de refutación.
6. **Diseñar experimento:** baseline, grupo/control cuando aplique, muestras, entorno, versiones, instrumentación, métricas, repeticiones y análisis estadístico.
7. **Ejecutar con seguridad:** laboratorio aislado, datos sintéticos o autorizados, mínimo privilegio, límites de recursos, registro íntegro y criterio de parada. Nunca probar sistemas ajenos sin autorización expresa.
8. **Analizar:** resultados, incertidumbre, falsos positivos/negativos, reproducibilidad, sensibilidad, limitaciones y amenazas a validez interna/externa/constructo.
9. **Publicar artefactos:** código, configuración, dataset permitido, hashes, instrucciones, SBOM/licencias y resultados esperados; nunca incluir secretos ni datos personales.
10. **Revisar:** revisión por pares independiente, reproducción por segundo operador y registro de cambios.

## 3. Plantilla de pregunta de investigación

- Contexto y problema observable:
- Pregunta principal (PICO/PEO cuando aplique):
- Preguntas secundarias:
- Hipótesis nula y alternativa:
- Población/sistemas y criterios de muestreo:
- Variables y métricas:
- Baselines y comparadores:
- Método de análisis:
- Criterios de aceptación/refutación:
- Riesgos éticos, legales y de seguridad:
- Limitaciones y amenazas a la validez:

## 4. Métricas mínimas según el tipo de estudio

- Detección: precision, recall, F1, PR-AUC, tasa de falsos positivos por unidad de tiempo, latencia, cobertura de telemetría.
- Rendimiento: throughput, p50/p95/p99, CPU, memoria, IO, energía cuando proceda.
- Robustez: tasa de fallo, degradación bajo perturbaciones, recuperación, sensibilidad a configuración y distribución.
- Vulnerabilidades: reproducibilidad, precondiciones, alcance, impacto demostrado, tasa de falsos positivos, tiempo de remediación y retest.
- Forense: integridad/hash, cobertura de artefactos, error de atribución, cadena de custodia y repetibilidad.
- Criptografía: modelo de amenaza, propiedades formales, vectores de prueba, interoperabilidad y rendimiento; no inventar garantías a partir de benchmarks.
- GRC: cobertura de controles, evidencia, riesgo residual, coste y eficacia operacional.
- OT/IoT/telecom: seguridad funcional, disponibilidad, latencia, interoperabilidad, límites físicos y comportamiento seguro ante fallo.

Las métricas se eligen justificadamente; no se deben usar todas por defecto ni comparar resultados incompatibles.

## 5. Registro de fuentes y evidencia

Cada fuente se registra con ID, título, autores/editor, tipo, URL canónica/DOI, versión, fecha de publicación, fecha de consulta, licencia, SHA-256 del archivo cuando se archive, método de adquisición, secciones utilizadas, dominios respaldados, evaluación crítica y revisor. Una URL conocida no significa que el documento se haya descargado, leído o validado.

Cada afirmación importante debe enlazarse a una fuente concreta y, cuando sea posible, a página/sección/fragmento. Separar:
- **Evidencia primaria:** mediciones, logs, datasets, código, especificaciones.
- **Evidencia secundaria:** interpretación o síntesis publicada.
- **Inferencia:** conclusión derivada por el analista.
- **Hipótesis:** explicación aún no probada.

## 6. Reproducibilidad

Registrar sistema operativo, hardware, dependencias fijadas, versiones, comandos, configuración, semilla aleatoria, fecha, entorno, hashes, datos, procedimiento, salida y desviaciones. Automatizar la preparación y verificación. Un tercero debe poder repetir el experimento dentro de las limitaciones documentadas.

## 7. Madurez y puertas de calidad

- **M0 — Esbozo:** alcance y bibliografía inicial.
- **M1 — Fundamentos:** conceptos y arquitectura con fuentes primarias.
- **M2 — Método:** procedimientos y controles explicados.
- **M3 — Validación:** laboratorio reproducible, datos, métricas y resultados.
- **M4 — Investigación:** estado del arte, pregunta/hipótesis, comparadores, análisis crítico y amenazas a validez.
- **M5 — Revisado:** revisión independiente y reproducción externa documentada.

No subir madurez si faltan evidencias. Los estados de madurez son editoriales, no certificaciones profesionales.

## 8. Seguridad, legalidad y ética

Respetar leyes, contratos, políticas de divulgación coordinada, privacidad, licencias y límites de autorización. No publicar credenciales, datos personales, exploits operativos contra objetivos reales ni instrucciones que faciliten daño no autorizado. Para investigación ofensiva, usar sistemas deliberadamente vulnerables, CTF, emuladores o activos con permiso escrito; minimizar persistencia, impacto y exfiltración. En OT, automoción, medicina, satélites y sistemas físicos, usar simulación o bancos aislados y priorizar seguridad funcional.

## 9. Checklist de aceptación de un módulo M4/M5

- [ ] Pregunta de investigación clara y falsable.
- [ ] Revisión de literatura con estrategia de búsqueda reproducible.
- [ ] Fuentes primarias identificadas y evaluadas.
- [ ] Taxonomía/estado del arte y brecha de conocimiento.
- [ ] Hipótesis, variables, baselines y métricas justificadas.
- [ ] Diseño experimental y análisis predefinidos.
- [ ] Entorno, datos y versiones documentados.
- [ ] Resultados, incertidumbre y amenazas a validez.
- [ ] Artefactos y hashes para reproducción.
- [ ] Limitaciones, ética y seguridad documentadas.
- [ ] Revisión independiente y reproducción externa (M5).
