# Investigación disciplinar y análisis de brechas — AI Red Team

**ID:** `ai_red_team`  
**Corte de investigación:** 2026-11-19  
**Rama objetivo:** `knowledge/develop-foundations`  
**Estado:** investigación documental inicial con fuentes primarias localizadas; lectura integral y validación experimental pendientes.  
**Regla:** este documento no declara el módulo validado ni sustituye la revisión de texto completo.

## 1. Pregunta y alcance disciplinar

¿Cómo se evalúa de forma reproducible la seguridad de sistemas basados en IA —modelos, aplicaciones LLM, RAG, agentes, herramientas y cadenas de suministro— frente a adversarios realistas, y cómo se demuestra que los controles reducen el impacto sin confundir una negativa textual con una acción efectivamente bloqueada?

El objeto de evaluación es el sistema sociotécnico completo. Deben distinguirse: (a) seguridad del modelo; (b) seguridad de la aplicación que lo integra; (c) seguridad de datos y recuperación; (d) autorización y ejecución de herramientas; (e) infraestructura, identidad y supply chain; (f) procesos humanos y gobierno.

## 2. Fuentes externas localizadas y valor probatorio

| Fuente | Tipo / alcance | Qué aporta a la investigación | Límite |
|---|---|---|---|
| NIST AI 600-1, Generative AI Profile (2024), https://doi.org/10.6028/NIST.AI.600-1 | Perfil de gestión de riesgos | Taxonomía de riesgos y acciones de gestión a lo largo del ciclo de vida; contexto de gobernanza y evaluación | Marco de gestión; no es por sí solo un procedimiento de red-team ni evidencia de eficacia de un control |
| MITRE ATLAS, https://atlas.mitre.org/ | Base viva de tácticas y técnicas | Taxonomía adversaria para sistemas predictivos, generativos y agénticos; técnicas, mitigaciones y casos | Cobertura evolutiva; no debe tratarse como benchmark exhaustivo ni como prueba de explotabilidad en cualquier sistema |
| OWASP GenAI LLM Top 10 2026, https://genai.owasp.org/ y https://github.com/GenAI-Security-Project/GenAI-LLM-Top10 | Guía comunitaria de riesgos de aplicaciones LLM | Riesgos y controles actuales; la edición 2026 sustituye como referencia vigente a la edición 2025 | Documento de concienciación/priorización, no estándar de certificación ni medición universal |
| Geng et al. (2026), revisión de 128 estudios sobre prompt injection, DOI 10.32604/cmc.2025.074081, https://www.sciopen.com/article/10.32604/cmc.2025.074081 | Revisión sistemática según resumen editorial | Taxonomías de inyección directa, indirecta y multimodal; objetivos, defensas y brechas de evaluación | La cifra y conclusiones deben verificarse en el texto completo, método de búsqueda, criterios, calidad de estudios y sesgo de publicación |
| Lee et al. (2025), JAMA Network Open, DOI 10.1001/jamanetworkopen.2025.49963, https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2842987 | Estudio empírico en un contexto médico concreto | Evidencia de que la inyección puede evaluarse con resultados observables y métricas de éxito/falsos positivos | Dominio médico y modelos evaluados limitan la generalización; leer métodos, corpus, modelos y limitaciones antes de reutilizar cifras |
| Duarte et al. (2026), IEEE Access, DOI 10.1109/ACCESS.2026.3656849, https://ieeexplore.ieee.org/abstract/document/11359704/ | Revisión sistemática | Evolución a ataques multi-turn, indirectos, estructurados, multimodales y asistidos por herramientas; benchmarks y mitigaciones | El resumen no basta para validar cada afirmación; texto completo requerido |

**Estado de lectura:** las fuentes anteriores fueron localizadas y sus metadatos/resúmenes consultados en esta fase. No se marca ninguna como `full_text_reviewed`. Se debe registrar licencia, versión, fecha, páginas/secciones efectivamente leídas y hash solo cuando el documento se archive legalmente.

## 3. Contraste con la biblioteca actual

Se inspeccionaron:
- `knowledge/deep_modules/ai_red_team/TECHNICAL_COMPENDIUM.md`
- `knowledge/deep_modules/ai_red_team/LITERATURE_REVIEW.md`
- `knowledge/EXPERT_RESEARCH_STANDARD.md`
- `knowledge/research/DOMAIN_LAYER_AUDIT_48.md`

### Hallazgos verificables

1. El compendio enumera siete temas, pero los seis apartados de modelo/amenazas/controles/verificación/análisis/entregable se repiten casi literalmente. No existe desarrollo independiente suficiente de los mecanismos propios de cada tema.
2. La sección añadida de profundización aporta una visión transversal de activos, vectores, controles y métricas, pero no desarrolla en detalle los siete temas ni sus fundamentos, arquitecturas, protocolos, casos límite y comparaciones.
3. La revisión de literatura se declara exploratoria M1; registra MITRE ATLAS como localizada, con texto íntegro pendiente. No contiene estrategia de búsqueda ejecutada, tabla de estudios primarios, evaluación de calidad ni síntesis comparativa suficiente.
4. El laboratorio contiene cuatro escenarios genéricos (baseline, fallo sintético, detección, mitigación). No define todavía datasets versionados, ground truth, matriz de escenarios, harness de evaluación, protocolo estadístico ni resultados observados.
5. La descripción del riesgo necesita actualizarse frente a OWASP GenAI LLM Top 10 2026 y la evolución de ATLAS; no debe seguir tratándose la edición 2025 como la actual.
6. La biblioteca no distingue suficientemente evaluación de modelos, evaluación de aplicaciones y evaluación de agentes con herramientas. Son unidades experimentales distintas y requieren amenazas, límites de confianza y métricas diferentes.

### Brechas que deben añadirse

| Área temática | Conocimiento faltante o insuficiente | Entregables de investigación necesarios |
|---|---|---|
| 1. Plan de pruebas y threat model | Activos, adversarios, capacidades, objetivos, límites de confianza, trust boundaries entre modelo/app/tools/RAG, escenarios y priorización por impacto | Método de scoping; plantilla de threat model; árbol de ataque; matriz de cobertura y reglas de parada |
| 2. Prompt injection | Diferencia entre directa/indirecta, persistente, multi-turn, multimodal y cross-context; flujo de instrucciones/datos; causas raíz y límites de mitigación | Taxonomía con casos reproducibles; corpus sintético; pruebas por canal/modalidad; análisis de controles en profundidad |
| 3. Abuso de herramientas y agencia | Confused deputy, autorización delegada, identidad de agente, capability security, permisos excesivos, aprobación humana, idempotencia y acciones irreversibles | Modelo de autoridad; pruebas de autorización servidor-side; escenarios de tool misuse y rollback |
| 4. RAG poisoning y cross-tenant | Ciclo de ingestión, provenance, chunking, embeddings, retrieval, ACL pre/post retrieval, aislamiento, cache y borrado | Dataset multi-tenant sintético; pruebas de aislamiento y poisoning; trazabilidad por fragmento |
| 5. Exfiltración y extracción | Secretos en contexto, extracción de datos/modelo, membership inference, model inversion, canales de salida, egress y límites de rate/coste | Modelo de datos/secretos; canaries; pruebas de leakage; medición de extracción y controles |
| 6. Evaluación adversarial | Diseño de benchmark, muestreo, cobertura, severidad, tasas base, variabilidad, contaminación, reproducibilidad y evaluación humana | Harness versionado; rúbrica; conjunto de casos; métricas y análisis de incertidumbre |
| 7. Retest y reporte | Evidencia suficiente, severidad contextual, causalidad, impacto, reproducibilidad, retest y comunicación responsable | Esquema de informe; cadena de evidencia; criterios de cierre; regression suite |

## 4. Desarrollo técnico requerido por las doce capas

Para cada uno de los siete temas se debe producir contenido diferenciado en las capas del estándar:

1. **Teoría:** definiciones, taxonomías, supuestos y alcance.
2. **Formal/matemática:** modelos de amenaza, probabilidad de éxito, teoría de decisión y estadística de evaluación cuando apliquen; justificar lo no aplicable.
3. **Arquitectura:** diagramas de componentes, flujos de datos/instrucciones, identidades, permisos y límites de confianza.
4. **Estándares:** comparar NIST AI RMF/AI 600-1, MITRE ATLAS y OWASP GenAI 2026 sin asumir equivalencia.
5. **Implementación:** harness, instrumentación, reglas, validadores y ejemplos en entorno controlado.
6. **Análisis avanzado:** casos límite, multi-turn, multimodal, cross-tenant, fallos de control, falsos positivos y trade-offs.
7. **Seguridad:** prevención, detección, respuesta, recuperación y riesgo residual.
8. **Investigación:** estado del arte, preguntas, hipótesis falsables, protocolo y amenazas a validez.
9. **Laboratorios/datasets:** corpus sintético, herramientas mock, ground truth, aislamiento, versiones y hashes.
10. **Evaluación:** métricas, baseline, muestras, intervalos de confianza, falsos positivos/negativos y criterios de aprobación.
11. **Skills:** procedimientos con alcance, permisos, entradas/salidas, validación, parada y rollback.
12. **Trazabilidad:** fuente por afirmación, versiones, licencia, fecha, revisión y mantenimiento.

## 5. Protocolo experimental propuesto

**Pregunta experimental:** ¿qué combinación de controles de arquitectura reduce las acciones no autorizadas y la exposición de datos frente a inyección directa/indirecta, sin degradar de forma inaceptable la utilidad legítima?

- **Entorno:** aplicación local con modelo o simulador, RAG sintético multi-tenant, herramientas mock y secretos canary no reales.
- **Variables independientes:** separación de privilegios, validación de argumentos, ACL en retrieval, filtrado de egress, aprobación humana y controles de procedencia.
- **Variables dependientes:** tasa de acción no autorizada, tasa de fuga de canary, éxito de ataque por categoría, tasa de falsos positivos, utilidad en tareas benignas, latencia y coste.
- **Controles:** baseline sin control, control individual y combinaciones predefinidas.
- **Diseño:** casos emparejados, repeticiones por versión/configuración, orden aleatorizado cuando proceda y criterios definidos antes de ejecutar.
- **Análisis:** denominadores explícitos, intervalos de confianza, tamaños de efecto y análisis por categoría; no resumir solo con una puntuación global.
- **Seguridad:** activos propios, datos sintéticos, sin servicios de terceros, sin credenciales reales, límites de coste y regla de parada.
- **Estado:** protocolo propuesto; no ejecutado. No existen resultados empíricos en este documento.

## 6. Criterios de aceptación para cerrar las brechas

- Cada uno de los siete temas tiene explicación técnica original, no plantilla compartida.
- Cada afirmación relevante se vincula a fuente o se marca como inferencia/hipótesis.
- Las fuentes primarias se leen y registran con alcance real de lectura.
- OWASP 2026 y ATLAS se versionan con fecha de consulta y cambios relevantes.
- Los casos de prueba distinguen modelos, aplicaciones, RAG y agentes.
- El laboratorio contiene corpus, ground truth, scripts, configuración, hashes y resultados.
- Se publican resultados negativos y limitaciones.
- Ningún experimento diseñado se registra como ejecutado.
- G1–G8 y K1–K5 se actualizan solo con evidencia.

## 7. Conclusión de esta primera investigación

El módulo `ai_red_team` no necesita que se le agreguen más encabezados. Necesita desarrollo disciplinar real en sus siete temas, revisión de literatura reproducible y un sistema experimental medible. La brecha más crítica es la ausencia de evaluación end-to-end de sistemas con RAG y herramientas, especialmente autorización, aislamiento multi-tenant y consecuencias de acciones del agente.

**Madurez conservadora:** M2 editorial con brechas críticas; la revisión de literatura permanece M1 exploratoria. No se propone elevar K ni aprobar puertas G en esta fase.
