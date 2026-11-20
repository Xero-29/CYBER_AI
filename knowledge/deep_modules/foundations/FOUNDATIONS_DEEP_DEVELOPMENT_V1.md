# Foundations — desarrollo disciplinar ampliado
Fecha de corte: 2026-11-19
Versión: 1.0.0
Estado: desarrollo documental incorporado; validación experimental y revisión externa pendientes.
Norma de trabajo: knowledge/EXPERT_RESEARCH_STANDARD.md

## Alcance y posición epistemológica

Foundations enseña los modelos transversales para razonar sobre seguridad de sistemas socio-técnicos. No reemplaza Identity, Network, AppSec, Vulnerability Management, Incident Response, Privacy, Safety ni Business Continuity: proporciona los fundamentos y deriva el tratamiento especializado a esos módulos.

Una afirmación se etiqueta como hecho respaldado, resultado observado, inferencia, hipótesis o recomendación. Una norma describe requisitos o resultados previstos; no demuestra que un control esté implantado ni que sea eficaz. Un laboratorio sintético permite comprobar propiedades del modelo, no estimar automáticamente la frecuencia del mundo real.

## 1. Ontología de seguridad y propiedades del sistema

### 1.1 Sistema de interés

Modelar un sistema como una frontera de análisis que contiene componentes, personas, procesos, datos, interfaces, proveedores y dependencias. La frontera no coincide necesariamente con la red corporativa: incluye servicios externos y procesos humanos cuando afectan la misión.

Distinguir:
- **Security:** resistencia frente a acciones o condiciones que comprometen propiedades protegidas.
- **Safety:** ausencia de riesgo inaceptable de daño físico o ambiental.
- **Privacy:** control y legitimidad del tratamiento de información relativa a personas; no se reduce a confidencialidad.
- **Reliability:** capacidad de prestar la función prevista durante un intervalo y condiciones especificadas.
- **Resilience:** capacidad de anticipar, resistir, recuperarse y adaptarse ante perturbaciones.
- **Trustworthiness:** grado justificable de confianza basado en evidencia sobre comportamiento, dependencias, operación y ciclo de vida.

Estas propiedades pueden entrar en conflicto. Una medida de autenticación más estricta puede reducir abuso y, a la vez, aumentar bloqueo operativo. El diseño debe registrar objetivo, población afectada, contexto y trade-off; no declarar que una propiedad maximiza todas las demás.

### 1.2 Propiedades de protección

La tríada CIA es una taxonomía inicial, no un modelo completo. Añadir autenticidad, responsabilidad, trazabilidad, privacidad, disponibilidad, seguridad funcional y resiliencia según misión. Para cada propiedad definir: sujeto, objeto, acción, contexto, condición de fallo, impacto y evidencia observable.

Ejemplo: “disponibilidad del servicio” debe precisar servicio, población, ventana temporal, SLO, dependencias y degradación aceptable. Sin denominador ni ventana, una cifra de disponibilidad no es interpretable.

## 2. Modelos formales, probabilidad e incertidumbre

### 2.1 Grafo de sistema y confianza

Representar el sistema mediante un grafo dirigido G=(V,E). Cada vértice v∈V puede ser activo, identidad, proceso, servicio, almacén o tercero; cada arista e∈E representa flujo de datos, invocación, administración, dependencia o delegación. Etiquetar aristas con protocolo, identidad, dirección, datos, autorización y controles.

Una frontera de confianza es una partición o interfaz donde cambian autoridad, dominio administrativo, nivel de exposición o garantías. El análisis debe incluir caminos indirectos, identidades de servicio, plano de administración, CI/CD, backups y proveedores. Un diagrama sin flujos ni privilegios no basta para modelar confianza.

### 2.2 Estados y transición

Para un recurso protegido, definir estados (por ejemplo: no autenticado, autenticado, autorizado, revocado) y transiciones con precondiciones, actor, evento y efecto. Las invariantes expresan propiedades que deben mantenerse, como “ninguna operación de escritura ocurre sin autorización válida”. Las pruebas negativas intentan violar invariantes con credenciales expiradas, contexto cambiado, revocación concurrente o identidad equivocada.

### 2.3 Modelo causal de riesgo

Usar la cadena:
contexto → activo/objetivo → fuente de amenaza o causa → evento → condición/debilidad → consecuencia → impacto → decisión → control → riesgo residual.

No todos los eventos son maliciosos: error humano, fallo de software, corte eléctrico, error de proveedor, desastre y dependencia compartida también pueden originar pérdidas. No confundir amenaza (potencial de causar daño), evento (ocurrencia), vulnerabilidad (debilidad explotable), exposición (posibilidad de interacción), impacto (consecuencia) y riesgo (efecto de incertidumbre sobre objetivos).

### 2.4 Probabilidad condicionada

Para un escenario S, declarar contexto C y horizonte T. La probabilidad relevante es P(S|C,T), no una etiqueta universal. Cuando hay eventos encadenados, usar regla de la cadena:
P(A∩B|C)=P(A|C)P(B|A,C).
No asumir independencia. Si se usa una aproximación de independencia, justificarla y analizar sensibilidad.

Pérdida esperada discreta:
E[L|C,T]=Σ_i P(S_i|C,T)·L_i.
La fórmula requiere escenarios bien definidos, horizonte consistente y evitar doble conteo. La pérdida esperada no describe por sí sola colas extremas, incertidumbre de parámetros ni distribución completa. Añadir percentiles, escenarios severos plausibles y análisis de sensibilidad cuando la decisión lo requiera.

Si faltan datos, no inventar probabilidades. Usar rangos, escenarios ordinales o juicio experto documentado; registrar quién estima, evidencia, desacuerdo, sesgo potencial y fecha de revisión. Las matrices cualitativas sirven para comunicación y priorización, no son medidas cardinales ni permiten multiplicaciones con interpretación física sin calibración.

### 2.5 Sensibilidad y valor de información

Identificar variables dominantes (frecuencia, exposición, eficacia de control, coste de interrupción). Variar supuestos dentro de rangos plausibles y observar si cambia la decisión. Si pequeñas variaciones alteran el ranking, declarar inestabilidad. Una nueva medición es valiosa cuando puede cambiar una decisión o reducir incertidumbre relevante; no recopilar métricas sin propósito.

## 3. Ingeniería de sistemas seguros y ciclo de vida

### 3.1 Desde misión hasta evidencia

Secuencia de ingeniería:
1. Contexto operacional, misión, stakeholders y restricciones.
2. Pérdidas temidas y consecuencias inaceptables.
3. Necesidades de protección y objetivos medibles.
4. Requisitos de seguridad/privacidad/safety asignados a componentes.
5. Arquitectura y límites de confianza.
6. Análisis de alternativas y trade-offs.
7. Implementación e integración.
8. Verificación de requisitos y validación de necesidades.
9. Despliegue, operación, mantenimiento y monitoreo.
10. Cambio, migración, retiro y disposición segura.

Requisito bien formado: identificador, sujeto, condición, comportamiento requerido, umbral verificable, justificación, propietario, método de verificación y dependencias. “El sistema será seguro” no es requisito verificable.

### 3.2 Verificación frente a validación

- **Verificación:** ¿el producto cumple la especificación?
- **Validación:** ¿el producto satisface la necesidad real en el contexto de uso?
Una prueba unitaria puede verificar una función, pero no valida por sí sola que la arquitectura proteja la misión. Usar inspección, análisis, demostración y prueba; indicar alcance y limitaciones de cada método.

### 3.3 Trade studies

Comparar alternativas con criterios explícitos: riesgo, rendimiento, coste total, complejidad operacional, dependencia, privacidad, recuperación y mantenibilidad. Registrar pesos y sensibilidad; no ocultar decisiones normativas tras una puntuación agregada. La opción “más segura” puede no ser viable si introduce un modo de fallo operacional mayor.

## 4. Activos, pérdidas y consecuencias

Un activo no es solo hardware o dato: puede ser capacidad de misión, reputación, seguridad de personas, propiedad intelectual, confianza pública, continuidad, servicio esencial o cumplimiento. Asociar propietario, custodio, usuarios, dependencias, ubicación, clasificación, criticidad, ciclo de vida y fuente de verdad.

Construir un grafo de dependencia para propagar consecuencias: servicio → proceso → cliente/paciente/ciudadano → impacto. Separar pérdida primaria y secundaria, impacto directo e indirecto, y horizonte temporal. La criticidad no se deriva únicamente del valor contable.

Para cada escenario, documentar:
- qué valor o capacidad se pierde;
- quién sufre la consecuencia;
- duración y reversibilidad;
- alcance y población afectada;
- obligaciones legales/contractuales;
- dependencias y efectos en cascada;
- supuestos y evidencia.

## 5. Amenazas, fallos y análisis de escenarios

Combinar métodos según propósito:
- DFD y trust boundaries para flujos y autoridad.
- STRIDE como lista de clases de amenaza, no como garantía de cobertura.
- árboles de ataque para descomponer objetivos adversarios.
- FMEA/FMECA para modos de fallo y efectos.
- fault trees para combinaciones causales de fallos.
- bow-tie para amenazas, evento central, consecuencias y barreras.
- análisis de causa raíz para explicar condiciones sistémicas, evitando culpar automáticamente al último operador.

No sumar taxonomías como si fueran probabilidades. ATT&CK describe tácticas y técnicas observadas; no es una predicción de probabilidad ni un catálogo exhaustivo. Distinguir adversario intencional, error, accidente, defecto, dependencia y perturbación ambiental.

## 6. Controles, assurance y argumento de seguridad

### 6.1 Control como hipótesis comprobable

Cada control debe especificar objetivo, alcance, propietario, mecanismo, frecuencia, entradas, salida esperada, evidencia, excepciones y dependencia. Separar:
- diseño adecuado;
- implementación existente;
- operación sostenida;
- eficacia observada;
- cobertura de población/activos;
- riesgo residual.

Un control configurado no es automáticamente eficaz. Muestrear operación real, probar escenarios negativos, observar bypass y medir cobertura. Los controles compensatorios deben tener dueño, justificación, fecha de expiración y criterio de retirada.

### 6.2 Assurance case

Estructurar una afirmación (claim), argumento (argument) y evidencia (evidence), con contexto y supuestos explícitos. Ejemplo:
- Claim: “El acceso administrativo a producción está limitado a identidades aprobadas”.
- Argumento: inventario de rutas, política de autorización, segregación y monitoreo cubren todos los caminos relevantes.
- Evidencia: configuración versionada, pruebas de acceso permitido/denegado, logs, revisión de excepciones y muestreo.
- Derrotadores: cuenta de emergencia, proveedor, pipeline, acceso físico, credencial persistente o bypass no modelado.

Una colección de controles no constituye por sí sola un argumento de assurance. El argumento debe tratar derrotadores y límites.

## 7. Gobierno, organización y cadena de suministro

Definir derechos de decisión: quién establece apetito/tolerancia, quién es dueño del riesgo, quién implementa controles, quién evalúa, quién acepta excepciones y quién comunica. Separar ejecución de evaluación cuando el riesgo lo amerite. Vincular riesgo técnico con objetivos y lenguaje comprensible para dirección.

Para terceros: inventario de servicios y subprocesadores, datos compartidos, ubicación, privilegios, dependencia, continuidad, notificación de incidentes, derecho de auditoría, salida y borrado, portabilidad, concentración y riesgo de actualización. Una certificación del proveedor es evidencia limitada al alcance, periodo y controles examinados; no elimina la responsabilidad del cliente.

La gestión debe incluir adquisición, desarrollo, cambios, vulnerabilidades, componentes de software, firmware, servicios administrados, personal y fin de contrato. Evaluar dependencia y concentración, no solo cuestionarios.

## 8. Privacidad, safety y resiliencia

### 8.1 Privacidad

Modelar ciclo de vida de datos: recolección, uso, inferencia, compartición, almacenamiento, retención, acceso, transferencia y eliminación. Evaluar finalidad, necesidad, proporcionalidad, minimización, transparencia, derechos, reidentificación, correlación y efectos sobre personas. Confidencialidad no garantiza privacidad: un tratamiento puede ser confidencial y aun así ser excesivo o ilegítimo.

### 8.2 Safety

Cuando el sistema pueda afectar personas o entorno físico, identificar peligros, severidad, exposición, controlabilidad y barreras. Coordinar con ingeniería de safety y responsables operacionales. No aplicar pruebas ofensivas en sistemas productivos críticos; usar simulación, gemelo digital o banco de pruebas autorizado.

### 8.3 Resiliencia

Definir funciones críticas, dependencias mínimas, modos degradados, RTO/RPO basados en análisis de impacto, respaldos, recuperación de identidad/llaves/configuración y criterios de retorno seguro. Probar restauración y dependencia de proveedores. Un backup exitoso no demuestra restaurabilidad; una recuperación técnica no demuestra recuperación del proceso de negocio.

## 9. Estándares y marcos: alcance y no equivalencia

- NIST CSF 2.0: taxonomía de resultados, perfiles organizacionales y tiers; no receta única ni certificación automática.
- NIST SP 800-30 Rev. 1: guía para evaluación de riesgo, con preparación, conducción y mantenimiento.
- NIST SP 800-37 Rev. 2: RMF de ciclo de vida (Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor); asigna responsabilidades y conecta sistema y organización.
- NIST SP 800-160 Vol. 1 Rev. 1: ingeniería de sistemas seguros y confiables durante el ciclo de vida.
- NIST SP 800-53 Rev. 5: catálogo de controles de seguridad y privacidad; seleccionar/adaptar según contexto, no copiar indiscriminadamente.
- ISO 31000: principios y directrices de gestión de riesgo; no es estándar certificable.
- MITRE ATT&CK: conocimiento de tácticas y técnicas adversarias observadas.
- CIS Controls: conjunto priorizado de salvaguardas; revisar versión, alcance y contexto.

No hacer mapeos uno-a-uno sin estudiar semántica, alcance, granularidad, evidencia y audiencia. Un control equivalente en nombre puede tener requisitos distintos.

## 10. Métricas y evaluación rigurosa

Para clasificador de hallazgos:
precision=TP/(TP+FP); recall=TP/(TP+FN); F1=2·precision·recall/(precision+recall).
Informar denominadores, definición de positivo, prevalencia, muestreo, umbral, intervalo de confianza y coste de error. Con clases raras, accuracy puede ser engañosa; usar PR-AUC y matriz de confusión además de métricas operativas.

Para inventario: cobertura frente a ground truth, tasa de activos no atribuidos, duplicados, frescura, latencia y error de reconciliación.
Para modelado: cobertura de rutas y escenarios, severidad de omisiones, falsos positivos, acuerdo interevaluador y tiempo.
Para controles: cobertura, tasa de bypass, operación, eficacia por escenario y coste de mantenimiento.
Para resiliencia: éxito de restauración, RTO/RPO observado, pérdida de datos, dependencias fallidas y tiempo hasta operación segura.

No comparar organizaciones con denominadores, definiciones o poblaciones diferentes. Las métricas son indicadores, no sustitutos de resultados de misión.

## 11. Casos integradores de aplicación

### Caso A — SaaS multi-tenant
Modelar identidad de usuario, identidad de workload, API, almacenamiento, plano de control, telemetría y proveedor cloud. Analizar aislamiento entre tenants, secretos, backups, soporte privilegiado, CI/CD, borrado y recuperación. Evidencia mínima: DFD, matriz de autorización, pruebas negativas cross-tenant, inventario de dependencias y plan de respuesta.

### Caso B — pequeña organización
Inventario de activos y cuentas, dependencia de MSP, correo, copias, pagos y conectividad. Priorizar por consecuencias y recursos reales. Evitar imponer una arquitectura empresarial inviable; diseñar controles mínimos verificables, responsables y plan de recuperación.

### Caso C — entorno híbrido
Analizar identidad federada, redes, endpoints, nube, DNS, proveedores y administración remota. Buscar rutas indirectas y dependencias compartidas. Evidencia: grafo de rutas, logs sincronizados, pruebas de revocación, segmentación y restauración.

### Caso D — OT simulado
Representar proceso, PLC simulado, HMI, ingeniería, historiador y acceso remoto. Priorizar safety y continuidad; no ejecutar escaneos ni explotación en planta real. Evaluar segmentación, control de cambios, backups de lógica, acceso de proveedor y recuperación segura.

## 12. Laboratorios fríos y calientes

### LAB-FND-01 — grafo de activos y dependencias
Datos: dataset sintético versionado con activos, propietarios, relaciones, etiquetas incorrectas, duplicados y dependencias ocultas.
Ground truth: grafo original separado de los datos perturbados.
Tareas: reconciliar fuentes, detectar activos huérfanos, construir grafo y justificar incertidumbre.
Métricas: precision/recall de entidades y aristas, duplicados, activos sin propietario, tiempo y sensibilidad a datos ausentes.
Negativos: identificadores repetidos, fuente desactualizada, dependencia circular, activo efímero.
Estado: protocolo diseñado; ejecución pendiente.

### LAB-FND-02 — análisis de riesgo con incertidumbre
Datos: escenarios sintéticos con rangos de probabilidad/impacto y supuestos explícitos.
Tareas: comparar matriz ordinal, escenarios y pérdida esperada cuando los datos lo permitan; realizar sensibilidad.
Métricas: estabilidad del ranking, variación de decisión, calibración solo si existe ground truth adecuado.
Negativos: eventos dependientes, doble conteo, horizonte incoherente, falsa precisión.
Estado: protocolo diseñado; ejecución pendiente.

### LAB-FND-03 — modelado de amenazas
Datos: arquitecturas SaaS e híbridas sintéticas con DFD y rutas ocultas conocidas.
Tareas: aplicar STRIDE, árboles de ataque y revisión de dependencias; comparar evaluadores.
Métricas: cobertura de rutas, falsos positivos, severidad de omisiones y acuerdo.
Estado: protocolo diseñado; ejecución pendiente.

### LAB-FND-04 — assurance de controles
Datos: políticas, configuraciones y logs simulados, incluyendo controles ausentes y bypass.
Tareas: construir claim-argument-evidence y buscar derrotadores.
Métricas: claims sustentados, evidencia vigente, derrotadores encontrados y reproducibilidad.
Estado: protocolo diseñado; ejecución pendiente.

### LAB-FND-05 — telemetría y reconstrucción
Datos: eventos sintéticos con retrasos, pérdida, reloj desalineado y duplicados.
Tareas: reconstruir secuencia causal, distinguir correlación de atribución.
Métricas: eventos correctamente enlazados, falsos enlaces, error temporal y completitud.
Estado: protocolo diseñado; ejecución pendiente.

Condiciones de ejecución: fijar commit, entorno, dependencias, semilla, esquema y hash; separar datos de entrenamiento/prueba cuando aplique; guardar resultados brutos; repetir; documentar desviaciones. No declarar resultados hasta ejecutar.

## 13. Evaluación profesional y rúbrica

Evaluar transferencia, no repetición de definiciones:
1. Explicar por qué CVSS alto no equivale automáticamente a riesgo empresarial alto.
2. Identificar rutas de confianza omitidas en un DFD.
3. Construir una cadena causal con amenaza no adversarial.
4. Derivar un requisito medible desde una pérdida temida.
5. Distinguir verificación, validación y assurance.
6. Criticar una matriz 5×5 con supuestos implícitos.
7. Proponer controles y explicar riesgo residual y derrotadores.
8. Diseñar recuperación considerando identidad, llaves y proveedor.
9. Interpretar precision/recall con prevalencia baja.
10. Presentar una decisión ejecutiva con incertidumbre y trade-offs.

Rúbrica 0–4: 0 incorrecto/ausente; 1 vocabulario sin mecanismo; 2 razonamiento correcto con omisiones; 3 análisis técnico completo con supuestos y límites; 4 transferencia a caso nuevo, evidencia y crítica de alternativas. Para K3+ se requiere evaluación práctica ejecutada, no solo preguntas propuestas.

## 14. Skills operativas derivables

- FND-SK-01 Asset & Dependency Modeling: entradas, alcance, fuentes, reconciliación, grafo, validación de propietarios, salida y limitaciones.
- FND-SK-02 Scenario Risk Assessment: contexto, horizonte, escenarios, probabilidad condicionada, impacto, sensibilidad, decisión y aceptación autorizada.
- FND-SK-03 Trust Boundary Review: DFD, identidades, flujos, privilegios, rutas indirectas, pruebas negativas y evidencia.
- FND-SK-04 Control Assurance: claim, argumento, evidencia, derrotadores, muestreo, operación y riesgo residual.
- FND-SK-05 Recovery Readiness Review: dependencias, identidad, secretos, backup, restauración, RTO/RPO y retorno seguro.

Estas son especificaciones candidatas, no Skills validadas ni automatizaciones aprobadas. Cada una requiere pruebas, permisos, rollback y revisión antes de promoción.

## 15. Matriz de cierre de las brechas FND-01 a FND-15

| ID | Tratamiento documental incorporado | Evidencia aún necesaria |
|---|---|---|
| FND-01 | Currículo específico y unidades diferenciadas | Revisión de cobertura por subtema |
| FND-02 | Modelos de grafos, estados, probabilidad e incertidumbre | Derivaciones y pruebas formales adicionales |
| FND-03 | Ciclo de vida de ingeniería segura | Caso de requisitos y trazabilidad ejecutado |
| FND-04 | Activos, pérdidas y consecuencias | Validación con especialistas de dominio |
| FND-05 | Probabilidad condicionada, dependencia y sensibilidad | Datos y calibración empírica donde existan |
| FND-06 | Assurance case y derrotadores | Caso completo revisado independientemente |
| FND-07 | Fallos humanos, ambientales y sistémicos | Casos comparativos y evidencia operacional |
| FND-08 | Gobierno, terceros y cadena de suministro | Matriz contractual/jurisdiccional por contexto |
| FND-09 | Privacidad, safety y resiliencia | Revisión legal, safety y continuidad especializada |
| FND-10 | Alcance y límites de marcos principales | Verificación de ediciones y mapeos detallados |
| FND-11 | Métricas, denominadores, sesgo e incertidumbre | Benchmark ejecutado y análisis estadístico |
| FND-12 | Cuatro casos integradores definidos | Soluciones completas evaluadas |
| FND-13 | Método de revisión reproducible descrito | Búsqueda ejecutada, cribado y extracción documentados |
| FND-14 | Cinco protocolos generales y siete protocolos temáticos definidos; los siete temáticos ejecutados como simulaciones sintéticas | Integración real aislada, datasets representativos y réplica independiente |
| FND-15 | Rúbricas definidas; ocho pruebas unitarias del harness ejecutadas | Evaluación de transferencia, revisión ciega y evaluación externa |

## 16. Estado de las 12 capas y puertas

L1 fundamentos: desarrollo ampliado; revisión de cobertura pendiente.
L2 formal/matemática: modelos introductorios documentados; validación formal y calibración pendientes.
L3 arquitectura: ciclo de vida y grafos documentados; casos ejecutados pendientes.
L4 estándares: alcance comparativo inicial; revisión de versiones y mapeos pendientes.
L5 implementación: procedimientos y casos definidos; artefactos ejecutables parciales.
L6 análisis avanzado: límites, fallos y trade-offs desarrollados; pruebas de estrés pendientes.
L7 seguridad: amenazas adversariales y no adversariales integradas; revisión especializada pendiente.
L8 investigación: agenda y diseño de método; revisión sistemática no ejecutada.
L9 laboratorios: cinco protocolos generales diseñados; siete protocolos temáticos ejecutados localmente con datos sintéticos y resultados versionados. No son pruebas de eficacia en producción ni réplica independiente.
L10 evaluación: métricas y rúbricas especificadas; ocho pruebas unitarias y métricas sintéticas ejecutadas; benchmarks externos/representativos pendientes.
L11 operación/Skills: cinco Skills candidatas; no promovidas.
L12 trazabilidad: referencias y estados documentados; lectura integral, hashes y revisión periódica incompletos.

Puertas G1–G8: ninguna se declara `passed`. G1–G4 continúan en progreso por cobertura, lectura de fuentes, profundidad y aplicación. G5–G7 pasan a `in_progress` por siete simulaciones sintéticas, ocho pruebas unitarias, métricas y repetición determinista; falta réplica independiente e integración real aislada. G8 permanece `blocked` por revisión independiente. Madurez conservadora: M2 editorial ampliado, investigación exploratoria; no K3/K4/K5 ni M3/M4/M5.

## 17. Fuentes primarias y estado de lectura

Revisión de secciones y trazabilidad afirmación→fuente→capa: [SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md](SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md).

- NIST CSWP 29, Cybersecurity Framework 2.0 (2024), https://doi.org/10.6028/NIST.CSWP.29 — secciones pertinentes del PDF oficial inspeccionadas; véase el dossier de revisión de fuentes.
- NIST SP 800-30 Rev. 1 (2012), https://doi.org/10.6028/NIST.SP.800-30r1 — capítulos y apéndices pertinentes inspeccionados; véase el dossier de revisión.
- NIST SP 800-37 Rev. 2 (2018), https://doi.org/10.6028/NIST.SP.800-37r2 — pasos RMF y tareas Prepare/Monitor pertinentes inspeccionados; véase el dossier de revisión.
- NIST SP 800-160 Vol. 1 Rev. 1 (2022), https://doi.org/10.6028/NIST.SP.800-160v1r1 — marco SSE, assurance case, requisitos, principios de diseño y procesos pertinentes inspeccionados; véase el dossier.
- NIST SP 800-61 Rev. 3 (2025), https://doi.org/10.6028/NIST.SP.800-61r3 — sección 2 y modelo CSF 2.0 de respuesta inspeccionados; véase el dossier.
- ISO 31000:2018, https://www.iso.org/standard/65694.html — ficha oficial; texto normativo completo no incluido ni declarado leído.
- MITRE ATT&CK Version History/Updates, https://attack.mitre.org/resources/versions/ — v20.1 vigente al corte 2026-11-19; changelog inspeccionado, objetos de catálogo no revisados exhaustivamente.

La consulta de una ficha oficial no equivale a lectura completa. Las secciones pertinentes y sus hallazgos están trazados en `SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md`. No se atribuyen a las fuentes resultados experimentales.

## 18. Criterio de salida de Foundations

No avanzar al módulo 2 hasta completar: revisión tema×capa con evidencia; lectura y extracción de fuentes prioritarias; solución documental de brechas críticas; casos integradores resueltos; laboratorios ejecutados y resultados reproducibles cuando proceda; auditoría de consistencia y duplicación; actualización del índice y tracker. Revisión independiente externa puede seguir pendiente, pero debe quedar explícitamente bloqueante para K4/K5 y no confundirse con cierre editorial.

Este documento amplía la base técnica y define el trabajo restante. No certifica por sí mismo la finalización del estándar.


---

# Auditoría disciplinar por tema — versión 1.1 (2026-11-19)

Esta sección convierte los siete temas del currículo inicial en unidades explícitas y trazables. Corrige una deficiencia de la versión anterior: el desarrollo transversal cubría conceptos relevantes, pero no demostraba qué contenido correspondía a cada tema ni cómo se satisfacían las doce capas. Cada capa que sigue contiene contenido disciplinar y una evidencia/artefacto exigible. **Estado de esta iteración: desarrollo documental ampliado; las capas quedan en `in_progress`, no `passed`, hasta que se adjunten fuentes de texto completo, artefactos y pruebas.**

## Convenciones comunes para los siete temas

- **Hecho normativo/documental:** describe lo que establece una publicación identificada; no demuestra eficacia local.
- **Inferencia:** conclusión que depende de supuestos explícitos.
- **Hipótesis:** proposición que debe ser probada.
- **Resultado:** solo se usa cuando existe ejecución, datos y registro reproducible.
- En todos los laboratorios: usar únicamente sistemas propios, simuladores o entornos con autorización expresa; definir alcance, límites, criterio de parada, limpieza y rollback.
- El riesgo no se calcula multiplicando escalas ordinales como si fueran probabilidades. Si no hay datos para estimar probabilidades, usar escenarios, rangos, bandas y análisis de sensibilidad.

## Tema 1 — Modelos de seguridad y confianza

**ID:** `foundations-01`  
**Objetivo:** representar propiedades de seguridad, sujetos, objetos, políticas, mecanismos, límites de confianza y fallos de mediación en un sistema sociotécnico.

### L1. Fundamentos teóricos
Distinguir seguridad (protección frente a acciones intencionales o no), safety (evitar daño accidental o peligroso), privacidad (tratamiento legítimo y limitado de datos personales), confiabilidad (cumplimiento consistente de funciones) y resiliencia (adaptación/recuperación). Definir sujeto, objeto, acción, autoridad, política, mecanismo de referencia, activo, frontera de confianza y dominio de fallo. Ninguna propiedad aislada garantiza las demás.

### L2. Fundamentos matemáticos y formales
Modelar el sistema como grafo dirigido y tipado (G=(V,E)), donde nodos representan identidades, procesos, datos, servicios y proveedores; aristas representan invocación, flujo, dependencia o delegación. Modelar autorización como predicado (P(s,o,a,c) ∈ {permit, deny}), con sujeto (s), objeto (o), acción (a) y contexto (c). Las invariantes se expresan como propiedades sobre estados: por ejemplo, todo acceso a un objeto restringido debe estar mediado por una decisión válida. Usar lógica temporal cuando importe el orden; no fingir que una matriz de riesgo es una prueba formal.

### L3. Arquitectura y funcionamiento interno
Descomponer punto de decisión, punto de aplicación, proveedor de identidad, motor de políticas, almacén de atributos, recurso y telemetría. Seguir una petición de extremo a extremo: identidad autenticada → contexto/atributos → evaluación → enforcement → registro → revocación. Identificar planos de control y datos, trust boundaries, canales laterales y dependencias compartidas. Un gateway no protege rutas que lo eluden.

### L4. Estándares y metodologías
Contrastar NIST SP 800-207 (arquitectura Zero Trust) con modelos DAC, MAC, RBAC y ABAC: Zero Trust es una arquitectura/principios de decisión sobre recursos, no un modelo de permisos intercambiable ni un producto. Usar NIST SP 800-160 Vol. 1 Rev. 1 para integrar seguridad en el ciclo de ingeniería. Registrar edición y alcance; no declarar equivalencia entre marcos.

### L5. Implementación técnica
Construir una matriz sujeto–recurso–acción–contexto; convertirla en pruebas de autorización positivas y negativas. Instrumentar decisiones con identificador de petición, sujeto, recurso, acción, política/versión, resultado y motivo, minimizando datos personales. Implementar denegación por defecto para operaciones sensibles y rutas de revocación. Verificar bypass de API, acceso directo al backend, cachés y credenciales de servicio.

### L6. Análisis avanzado
Analizar confusión de identidad, atributos obsoletos, propagación excesiva de privilegios, TOCTOU, fail-open/fail-closed, caché de decisiones, reloj desincronizado, dependencia del IdP y fallos de política. Evaluar disponibilidad del plano de autorización, consistencia de revocación y degradación segura. La autenticación correcta no prueba que la autorización sea correcta.

### L7. Perspectiva de seguridad
Amenazas: suplantación, elevación de privilegios, confused deputy, abuso de delegación, bypass de enforcement, robo de sesión y abuso interno. Controles: MFA resistente a phishing cuando aplique, mínimo privilegio, separación de funciones, tokens acotados, validación en el recurso, auditoría protegida y revocación. Documentar riesgo residual y vías de fallo común.

### L8. Investigación científica
Pregunta: ¿qué combinación de evaluación centralizada y enforcement local reduce más las decisiones inconsistentes bajo cambios de atributos y revocación? Hipótesis falsable: un diseño con versión de política y expiración explícita reduce decisiones obsoletas frente a caché sin invalidación. Variables: latencia, tasa de decisión obsoleta, disponibilidad, falsos permisos/denegaciones. Controlar carga, reloj y topología; publicar resultados negativos y amenazas a validez.

### L9. Laboratorios y datasets
LAB-FND-01A: simulador de autorización con 3 roles, 4 recursos, 5 acciones, atributos y reglas conflictivas; generar casos permitidos, denegados, atributos nulos/obsoletos y revocación. Ground truth manual versionado. No conectar a identidad real. Registrar configuración, semilla, entradas, decisiones y logs.

### L10. Evaluación y benchmarks
Métricas: tasa de decisiones correctas respecto al ground truth, falsos permisos, falsas denegaciones, cobertura de rutas, latencia p50/p95/p99, tiempo de propagación de revocación y disponibilidad. Reportar matriz de confusión y resultados por clase; accuracy global no basta si los permisos indebidos son raros.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.AUTHZ-MODEL`: entradas (inventario, sujetos, recursos, acciones, contexto), precondiciones (alcance autorizado y propietario), pasos (modelar, derivar políticas, generar pruebas, revisar bypass), salidas (matriz, DFD, pruebas y hallazgos), parada (identidad/alcance incierto), rollback (restaurar política versionada). No promover hasta probarla en casos distintos.

### L12. Trazabilidad y mantenimiento
Mantener diagrama y matriz versionados, ID de política, responsable, fecha de revisión, dependencias, cambios y evidencia de prueba. Cada decisión relevante debe apuntar a requisito, política y test. Revisar cuando cambien identidades, proveedores, APIs, topología o clasificación de datos.

### Profundización técnica derivada de fuentes primarias
En ingeniería de sistemas seguros, no reducir el diseño a una cadena de controles. El marco SSE de NIST SP 800-160 Vol. 1 Rev. 1 organiza el razonamiento en contextos de problema, solución y trustworthiness que interactúan de forma iterativa/recursiva durante el ciclo de vida. El assurance case debe ser un artefacto argumentado y auditable: claims, subclaims, argumentos, evidencia y supuestos explícitos; la evidencia debe ser pertinente, creíble y suficientemente rigurosa para la consecuencia que se quiere asegurar. Un requisito de seguridad debe definir capacidad/funcionamiento y evidencia verificable; una política prescribe comportamiento en el contexto operacional; un mecanismo implementa ese comportamiento. Confundirlos produce requisitos no verificables o controles sin objetivo trazable.

Formalizar la decisión de acceso como P(s,o,a,c,t) y registrar política/versionado, identidad, contexto y tiempo. Una propiedad útil es: para toda transición que modifica un objeto protegido, existe una decisión válida que cubre sujeto, objeto, acción y contexto en ese instante. La caché de autorización debe estar vinculada a versión/epoch de política, identidad y atributos; la revocación debe invalidar o acotar explícitamente el TTL. El modo fail-closed reduce bypass pero puede afectar disponibilidad; definir excepciones de emergencia con alcance, expiración, auditoría y dueño, nunca un bypass permanente.

## Tema 2 — Inventario y clasificación de activos

**ID:** `foundations-02`  
**Objetivo:** descubrir, reconciliar, clasificar y mantener activos y dependencias con procedencia y confianza explícitas.

### L1. Fundamentos teóricos
Distinguir activo, componente, servicio, dato, dependencia, propietario, custodio y operador. Un activo tiene valor por su relación con una misión; no todo host equivale a un activo y un activo lógico puede residir en varios componentes. Clasificar datos por sensibilidad, impacto y obligación, no solo por ubicación.

### L2. Fundamentos matemáticos y formales
Representar inventario como grafo de dependencias con atributos temporales. Para reconciliación, usar claves fuertes (UUID, cloud resource ID, serial) y reglas probabilísticas solo como sugerencia, nunca como fusión automática sin evidencia. Métricas: cobertura (C=|A_{observados} ∩ A_{referencia}|/|A_{referencia}|), duplicados, huérfanos, frescura y tasa de atribución. Declarar el ground truth y sus limitaciones.

### L3. Arquitectura y funcionamiento interno
Fuentes: EDR, MDM, CMDB, cloud APIs, DNS/DHCP, IAM, repositorios, SBOM, IaC, contratos y entrevistas. Pipeline: extracción → normalización → resolución de identidad → reconciliación → enriquecimiento → clasificación → asignación de dueño → ciclo de revisión. Conservar la fuente original, timestamp y método de descubrimiento.

### L4. Estándares y metodologías
Usar NIST CSF 2.0 como taxonomía de resultados y NIST SP 800-53 Release 5.2.0 como catálogo de controles; no tratarlos como un esquema universal de inventario. Para ciclo de vida, retiro y reutilización de medios, contrastar NIST SP 800-88 Rev. 2 (2025), que reemplaza Rev. 1 y orienta un programa de sanitización con assurance, no solo la ejecución de un comando. Definir taxonomía local, criterios de clasificación y retención. Separar requisitos legales locales de guías estadounidenses y validar aplicabilidad en jurisdicción colombiana antes de declarar obligación.

### L5. Implementación técnica
Esquema mínimo: `asset_id`, `asset_type`, `source_id`, `source_record_id`, `owner`, `operator`, `environment`, `data_classes`, `criticality`, `dependencies`, `first_seen`, `last_seen`, `confidence`, `status`. Importar en staging, normalizar nombres y unidades, deduplicar por identificadores fuertes, generar cola de conflictos y exportar inventario con historial. No borrar registros huérfanos: marcarlos y resolverlos.

### L6. Análisis avanzado
Casos difíciles: activos efímeros, autoscaling, serverless, BYOD, shadow IT, cuentas de proveedor, entornos desconectados, dispositivos sin agente, clones de VM, recursos borrados y drift. Medir falsos merges y falsos splits. Un inventario aparentemente completo puede ocultar sesgo de observación si todas las fuentes comparten la misma omisión.

### L7. Perspectiva de seguridad
Riesgos: activo sin dueño, recurso expuesto olvidado, identidad huérfana, clasificación incorrecta, datos en backup/exportación no inventariados y dependencia crítica desconocida. Controles: reconciliación multi-fuente, owner obligatorio para activos críticos, expiración/revisión, detección de drift y clasificación heredada con validación humana.

### L8. Investigación científica
Pregunta: ¿la fusión de fuentes heterogéneas mejora la cobertura real sin aumentar falsos merges? Hipótesis: claves fuertes más reconciliación supervisada mejoran F1 frente a hostname como clave única. Diseñar dataset sintético con duplicados, cambios de nombre, clones y recursos efímeros; comparar algoritmos y analizar sesgo de fuentes.

### L9. Laboratorios y datasets
LAB-FND-02A: generar 500 registros sintéticos desde CMDB, cloud, EDR y DNS, con 10% de duplicados y 5% de activos sin dueño (parámetros configurables, no datos reales). Publicar esquema, generador, semilla y ground truth. Medir reconciliación y conservar conflictos.

### L10. Evaluación y benchmarks
Precision/recall/F1 de emparejamiento, cobertura frente al ground truth, tasa de falsos merges, duplicados residuales, activos sin propietario, antigüedad mediana, latencia de actualización y coste operativo. Separar métrica de calidad del inventario de métrica de seguridad real.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.ASSET-RECONCILIATION`: delimitar fuentes, validar permisos, extraer snapshots, normalizar, reconciliar, producir excepciones y asignar responsables. No ejecutar descubrimiento activo ni escaneo de red sin autorización y alcance documentados.

### L12. Trazabilidad y mantenimiento
Registrar conectores y versiones, consultas, timestamps, licencias, hashes de snapshots, reglas de matching, decisiones humanas y cambios de esquema. Definir SLA de frescura por criticidad y revisar cobertura cuando se incorpore una nueva nube, proveedor o unidad de negocio.

### Profundización técnica derivada de fuentes primarias
La reconciliación es un problema de resolución de entidades con observaciones parciales, no una simple deduplicación de nombres. Mantener por registro: fuente, identificador nativo, instante de observación, confianza, entorno, estado y evidencia de correspondencia. Las claves fuertes (UUID de instancia, ID de recurso cloud, serial validado) permiten enlaces deterministas solo dentro de su ámbito de unicidad y ciclo de vida. Hostname, IP y etiquetas son atributos mutables; deben producir candidatos, no fusiones automáticas. Si dos fuentes comparten el mismo error de descubrimiento, su acuerdo no elimina el sesgo.

Medir cobertura respecto de un ground truth explícito: C=|A_observados ∩ A_referencia|/|A_referencia|. Medir por separado precision/recall de emparejamiento, activos sin dueño, antigüedad de last_seen y proporción de registros ambiguos. La antigüedad debe evaluarse con SLA distinto por criticidad y volatilidad. SP 800-88 Rev. 2 añade una dimensión de cierre del ciclo: la disposición del medio exige programa, método adecuado a sensibilidad/reutilización, confianza en el proveedor y evidencia de sanitización; la validación decide aprobar/rechazar la eficacia y puede requerir repetir/escalar. Cryptographic erase depende de la calidad y procedencia del cifrado y de condiciones previas de gestión de claves; no inferir borrado seguro de la mera desaparición del inventario.

## Tema 3 — Superficie de ataque y modelado de amenazas

**ID:** `foundations-03`  
**Objetivo:** identificar rutas de abuso y fallos desde el contexto de misión, arquitectura, datos, identidades y dependencias.

### L1. Fundamentos teóricos
Distinguir amenaza, actor, capacidad, intención, oportunidad, evento, vulnerabilidad, exposición, ataque, impacto y riesgo. La superficie incluye interfaces técnicas, humanas, físicas, organizativas y de proveedor. STRIDE clasifica amenazas; no es un método completo de priorización ni sustituye análisis de safety.

### L2. Fundamentos matemáticos y formales
Construir DFD con procesos, almacenes, entidades externas y flujos; marcar trust boundaries. Modelar attack graph como estados y transiciones condicionadas por precondiciones, permisos y vulnerabilidades. Árboles de ataque expresan combinaciones AND/OR. Probabilidades de rutas no se multiplican sin independencia justificada; usar análisis de sensibilidad cuando los datos sean escasos.

### L3. Arquitectura y funcionamiento interno
Proceso: contexto y activos → diagrama de contexto/DFD → límites → escenarios → rutas → controles → riesgo residual → requisitos y pruebas. Incluir plano de administración, CI/CD, identidad de workload, backups, soporte, observabilidad, proveedores y recuperación; no limitarse al tráfico externo.

### L4. Estándares y metodologías
Combinar STRIDE, attack trees, misuse/abuse cases y MITRE ATT&CK como taxonomías complementarias. ATT&CK v20.1 (13-10-2026) describe comportamiento adversario documentado; no certifica que una técnica sea aplicable a un sistema ni proporciona probabilidad. NIST SP 800-30 Rev. 1 diferencia eventos adversariales y no adversariales y separa iniciación/ocurrencia de probabilidad de impacto; NIST SP 800-160 integra seguridad en ingeniería.

### L5. Implementación técnica
Plantilla de escenario: activo, actor, objetivo, precondiciones, vector, ruta, debilidad, control existente, evidencia, consecuencia, detección, mitigación, riesgo residual y prueba. Mantener DFD en formato versionable (p. ej. Mermaid/PlantUML) y asociar cada amenaza a test verificable.

### L6. Análisis avanzado
Buscar rutas alternativas, fallos comunes, abuso de privilegio, errores de configuración, amenazas internas, fallos de proveedor, cadenas de dependencias, degradación y recuperación. Evitar doble conteo de escenarios correlacionados. Priorizar rutas completas y factibles, no sumar listas de CVE sin contexto.

### L7. Perspectiva de seguridad
Considerar confidencialidad, integridad, disponibilidad, autenticidad, privacidad y safety. Para cada escenario especificar prevención, detección, respuesta y recuperación. Validar controles con pruebas negativas seguras; no demostrar una amenaza atacando sistemas de terceros.

### L8. Investigación científica
Pregunta: ¿DFD más análisis de abuso encuentra rutas críticas omitidas por STRIDE aplicado sin modelar flujos? Hipótesis: el enfoque combinado reduce omisiones de rutas del ground truth en sistemas de referencia. Evaluación ciega por revisores, medir cobertura, severidad de omisiones y acuerdo interevaluador.

### L9. Laboratorios y datasets
LAB-FND-03A: arquitectura sintética multi-tier con API, IdP, cola, base de datos, CI/CD y proveedor externo. Crear ground truth de 30 escenarios (benignos y adversariales), etiquetados por dos revisores. Probar solo diagramas y simulador, sin explotación de sistemas reales.

### L10. Evaluación y benchmarks
Cobertura de amenazas críticas, falsos positivos, severidad de omisiones, porcentaje de escenarios con evidencia y test asociado, tiempo de modelado y acuerdo interevaluador (Cohen's kappa cuando proceda). Publicar desacuerdos y reglas de adjudicación.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.THREAT-MODEL`: recopilar arquitectura y alcance; construir DFD; marcar límites; enumerar amenazas; derivar controles/tests; revisar con propietario. Salida obligatoria: modelo, registro de escenarios y riesgos no resueltos. Parar si faltan límites o autorización.

### L12. Trazabilidad y mantenimiento
Versionar arquitectura, supuestos, catálogo de amenazas, revisión, cambios, fecha y evidencia. Reabrir el modelo ante cambios de flujo, proveedor, privilegios, exposición, datos o misión; asociar cada hallazgo a un commit o release.

### Profundización técnica derivada de fuentes primarias
El modelo de riesgo debe distinguir fuente de amenaza, evento, vulnerabilidad/condición predisponente, probabilidad de iniciación u ocurrencia, probabilidad de impacto e impacto. Para eventos adversariales se consideran capacidad, intención y targeting; para eventos no adversariales se consideran frecuencia/historial y condiciones operativas. La probabilidad global depende del modelo de la organización: NIST SP 800-30 Rev. 1 no impone una fórmula universal para combinar escalas semicuantitativas. Por ello, no convertir escalas ordinales en porcentajes ni multiplicar valores 1–5 como si fueran probabilidades calibradas.

Un attack graph debe especificar estado inicial, precondiciones, transición, privilegio requerido, activo objetivo y condición de éxito. En rutas AND, todos los prerrequisitos deben satisfacerse; en rutas OR basta una alternativa. ATT&CK v20.1 debe registrarse con fecha y dominio (Enterprise/Mobile/ICS); mapear una técnica a un escenario significa compatibilidad analítica, no evidencia de que ocurrió ni estimación de likelihood. Las rutas deben terminar en consecuencias de misión y pruebas de control, no en listas descontextualizadas de técnicas.

## Tema 4 — Identidad y control de acceso

**ID:** `foundations-04`  
**Objetivo:** razonar sobre ciclo de vida de identidades humanas/no humanas, autenticación, autorización, delegación y privilegios.

### L1. Fundamentos teóricos
Distinguir identificación, autenticación, autenticidad, autorización, accounting, federación, sesión, credencial, factor, privilegio y delegación. Las identidades de máquina y workloads requieren propietario, propósito, ciclo de vida y rotación; no son cuentas humanas simplificadas.

### L2. Fundamentos matemáticos y formales
Representar autorización como relación sujeto–recurso–acción–contexto; analizar jerarquías RBAC, atributos ABAC y restricciones de separación de funciones. Usar entropía solo para propiedades probabilísticas de secretos; no confundir longitud con entropía efectiva. Modelar caducidad/revocación como estado temporal y analizar ventanas de exposición.

### L3. Arquitectura y funcionamiento interno
Componentes: IdP, directorio, MFA, federation broker, token issuer, policy decision/enforcement points, PAM, vault, workload identity y auditoría. Trazar OIDC/OAuth 2.0/SAML según uso y roles; distinguir autenticación de usuario de autorización API. Revisar issuer, audience, scope, expiry, nonce/state y validación de firma cuando corresponda.

### L4. Estándares y metodologías
NIST SP 800-207 para principios ZT; NIST SP 800-53 Release 5.2.0 para controles; NIST SP 800-63-4 (incluidas SP 800-63B-4 y 800-63C-4) para identity proofing, autenticación, gestión de autenticadores, federación y assertions; FIDO/WebAuthn y OAuth/OIDC como especificaciones de protocolos/identidad, no equivalentes entre sí. RFC 9700 (BCP 240, 2025) establece prácticas actuales para OAuth 2.0: redirect URI con coincidencia exacta, PKCE para clientes públicos (S256), evitar implicit grant, restringir audience/scope y considerar tokens sender-constrained o rotación de refresh tokens. Verificar versiones, perfiles y erratas antes de implementación.

### L5. Implementación técnica
Diseñar alta/cambio/baja (JML), MFA, recuperación, acceso privilegiado temporal, scopes mínimos, tokens de vida corta, rotación de secretos, revisión de acceso y cuentas break-glass. Incluir pruebas de expiración, revocación, audience incorrecta, issuer no confiable, scope excesivo y acceso cross-tenant.

### L6. Análisis avanzado
Riesgos de sincronización, replay, token confusion, consent phishing, session fixation, refresh-token theft, cuentas huérfanas, service principals olvidados, secretos en CI y dependencia del IdP. Evaluar disponibilidad de autenticación y modo de recuperación sin crear bypass permanente.

### L7. Perspectiva de seguridad
Amenazas: suplantación, elevación, persistencia, abuso de delegación, insider y robo de credenciales. Mitigar con phishing-resistant MFA cuando el riesgo lo exija, PAM, JIT/JEA, device posture, revisión de grants, detección de anomalías y revocación verificable.

### L8. Investigación científica
Pregunta: ¿credenciales efímeras y permisos mínimos reducen exposición sin degradar disponibilidad en workloads? Medir duración, permisos efectivos, fallos legítimos, tiempo de recuperación y tasa de acceso indebido en simulación. Separar eficacia técnica de experiencia de usuario.

### L9. Laboratorios y datasets
LAB-FND-04A: IdP simulado, dos aplicaciones, tres roles, dos workloads y tokens de prueba; inyectar expiración, audience errónea, revocación tardía y scopes excesivos. Usar secretos ficticios. Registrar eventos sin material sensible.

### L10. Evaluación y benchmarks
Cobertura MFA, cuentas sin dueño, privilegios excesivos, tiempo de revocación, duración de credenciales, tasa de decisiones erróneas, latencia y fallos de acceso legítimo. Segmentar humanos, servicios y workloads.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.IDENTITY-LIFECYCLE`: inventariar identidades, mapear dueño/propósito, revisar permisos, validar autenticación, probar revocación y emitir excepciones. No rotar ni revocar identidades productivas sin aprobación del dueño y plan de rollback.

### L12. Trazabilidad y mantenimiento
Guardar esquema de claims, issuer/audience, versiones de librerías, configuración no secreta, responsable, fecha, evidencias de pruebas y excepciones aprobadas. Nunca almacenar tokens, claves privadas o contraseñas en el repositorio.

### Profundización técnica derivada de fuentes primarias
Para OAuth 2.0, RFC 9700 exige coincidencia exacta de redirect URI (con excepción limitada para el puerto localhost de apps nativas) y PKCE para clientes públicos; S256 evita exponer el verifier. El implicit grant no debe ser el flujo predeterminado porque expone tokens en la respuesta/URL y complica sender constraint. En el resource server validar firma y algoritmo permitido, issuer, audience, expiración, scopes/claims, y estado de revocación cuando el diseño lo requiera; comprobar solo que un JWT está bien formado no autentica nada.

Los tokens sender-constrained (mTLS o DPoP) reducen replay de tokens robados, pero no protegen cuando se compromete el cliente y se extraen tanto token como clave. La rotación de refresh tokens debe invalidar el anterior y detectar su reutilización, manteniendo la relación entre tokens para identificar compromiso. La simulación LAB-FND-04A prueba solo claims sintéticos: la implementación real requiere bibliotecas mantenidas, validación criptográfica, pruebas negativas de protocolo e interoperabilidad.

## Tema 5 — Criptografía y protección de datos

**ID:** `foundations-05`  
**Objetivo:** seleccionar y operar mecanismos criptográficos adecuados al propósito, modelo de amenaza y ciclo de vida de datos/llaves.

### L1. Fundamentos teóricos
Distinguir cifrado, hash, MAC, firma, KDF, KEM, aleatoriedad, secreto, autenticidad, integridad y no repudio. La criptografía protege propiedades concretas bajo supuestos; no corrige endpoints comprometidos, mala autorización, metadatos expuestos ni disponibilidad.

### L2. Fundamentos matemáticos y formales
Explicar seguridad como indistinguibilidad/ventaja del adversario en modelos pertinentes; entropía de Shannon/min-entropía para fuentes aleatorias; colisiones/preimagen para hash; composición AEAD y límites de nonce. Evitar derivar seguridad práctica solo de tamaño de clave. Documentar supuestos de adversario y modelo.

### L3. Arquitectura y funcionamiento interno
Ciclo de claves: generación → distribución → almacenamiento → uso → rotación → revocación → backup/recuperación → destrucción. Separar data keys y key-encryption keys; identificar KMS/HSM, trust boundaries, envelope encryption, certificados, PKI y gestión de secretos. Mapear datos en reposo, tránsito y uso.

### L4. Estándares y metodologías
Separar mecanismos: AES (FIPS 197) es cifrado simétrico; HMAC es autenticación/integridad; ML-KEM (FIPS 203) es un mecanismo de encapsulación de claves, no cifrado de archivos; ML-DSA (FIPS 204) y SLH-DSA (FIPS 205) son firmas digitales. SP 800-57 Part 1 Rev. 5 guía gestión de claves y FIPS 140 aplica a validación de módulos criptográficos. FIPS 203 mantiene aviso de errata potencial del 2025-11-17; FIPS 204 mantiene aviso del 2026-07-31 sobre varios issues menores. Comprobar las hojas oficiales de erratas y futuras revisiones antes de fijar parámetros. No extrapolar estos avisos a FIPS 205 sin evidencia del emisor. No inventar cumplimiento ni asumir que usar un algoritmo aprobado hace segura toda la arquitectura.

### L5. Implementación técnica
Preferir bibliotecas mantenidas y APIs de alto nivel; no diseñar primitivas propias. Usar AEAD con nonce único bajo el esquema del algoritmo; validar certificados/cadenas y hostname; almacenar claves en KMS/HSM cuando corresponda; separar secretos por entorno; probar rotación, revocación, backup y restauración. Evitar claves hardcodeadas.

### L6. Análisis avanzado
Analizar nonce reuse, downgrade, padding oracle, side channels, RNG defectuoso, validación parcial de certificados, confusión de algoritmos, mala separación de claves, pérdida de KMS, expiración y errores de migración. Incluir impacto de comprometer endpoint, operador, proveedor y backup.

### L7. Perspectiva de seguridad
Amenazas: robo de claves, sustitución de certificados, manipulación de ciphertext, exfiltración de secretos, replay y destrucción de material criptográfico. Controles: mínimo privilegio, rotación, dual control, auditoría, separación de duties, protección de backups y plan de recuperación. El cifrado no sustituye clasificación ni control de acceso.

### L8. Investigación científica
Pregunta: ¿qué política de rotación/recuperación minimiza exposición sin aumentar pérdida de disponibilidad? Hipótesis comparativa en simulación; variables: tiempo de rotación, fallo de recuperación, exposición acumulada, latencia y error de operación. No probar algoritmos débiles en producción.

### L9. Laboratorios y datasets
LAB-FND-05A: entorno aislado con biblioteca criptográfica estándar, certificados de prueba y KMS simulado; probar round-trip, modificación de ciphertext, nonce duplicado detectado por harness, expiración, rotación y recuperación. Datos ficticios; guardar versiones y hashes, nunca secretos.

### L10. Evaluación y benchmarks
Pruebas de interoperabilidad, vectores de prueba oficiales, tasa de verificación correcta, rechazo de mensajes alterados, latencia/throughput, uso de CPU, tiempo de rotación y recuperación. Benchmarks deben fijar hardware, versión, parámetros y tamaño de muestra.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.CRYPTO-REVIEW`: clasificar datos, definir propiedades, revisar algoritmos/parametría, mapa de llaves, ciclo de vida, dependencias y pruebas. Parar ante algoritmo propietario, parámetros desconocidos o llaves expuestas; escalar al especialista criptográfico.

### L12. Trazabilidad y mantenimiento
Registrar algoritmo, modo, parámetros, biblioteca/versión, política, key ID no secreto, dueño, fecha de rotación y evidencia. Prohibido incluir claves, tokens o material secreto. Mantener plan de agilidad criptográfica y revisión de obsolescencia.

### Profundización técnica derivada de fuentes primarias
No agrupar cifrado, firma y establecimiento de claves bajo una sola etiqueta. AES (FIPS 197) es un cifrador de bloque simétrico; el modo de operación determina propiedades y requisitos adicionales. HMAC-SHA-256 proporciona autenticación de mensaje e integridad con una clave compartida, pero no confidencialidad ni firma pública. ML-KEM (FIPS 203) establece un secreto compartido mediante encapsulación; ML-DSA (FIPS 204) y SLH-DSA (FIPS 205) generan/verifican firmas. No usar una firma como KEM ni presentar un KEM como cifrado directo de datos.

El IPD SP 800-57pt1r6 describe cuatro fases del ciclo de vida: pre-operational, operational, post-operational y destroyed. Las fases agrupan estados de clave; no son sinónimos de ellos. Las transiciones de estado deben quedar registradas en logs y metadata. El borrador describe estados como pre-activation, active, suspended, compromised y destroyed; un sistema puede adaptar estados aplicables, pero debe justificarlo y registrar transiciones.

El mismo IPD indica que el inventario de claves de largo plazo debe mantener referencias o punteros al material, no copiar claves secretas/privadas salvo que el inventario también cumpla funciones de backup/archivo. Debe incluir owner/sponsor, tipo, algoritmo, longitud, uso y expiración, además de estado/compromiso para facilitar revocación y sustitución. Distinguir re-keying (nueva clave independiente) de key update (derivada de la anterior); la cadena de key update puede propagar el compromiso de una clave anterior. Estas observaciones proceden de un IPD y no sustituyen la publicación final vigente.

El laboratorio actual usa deliberadamente HMAC del estándar de biblioteca para probar alteración y cambio de clave; no implementa AES, KMS, HSM, PKI ni valida conformidad FIPS. La producción requiere gestión de ciclo de vida de claves, aleatoriedad, separación de usos, control de acceso, backup/recuperación, rotación, revocación y destrucción. Para AEAD, el nonce debe cumplir las condiciones específicas del algoritmo y no reutilizarse con la misma clave cuando el modo lo prohíba. Un benchmark criptográfico debe registrar CPU, biblioteca, versión, parámetros, tamaños, número de repeticiones e intervalos; no extrapolar resultados de una sola máquina.

## Tema 6 — Detección, respuesta y recuperación

**ID:** `foundations-06`  
**Objetivo:** convertir telemetría en detección accionable y coordinar respuesta, contención, erradicación, recuperación y aprendizaje.

### L1. Fundamentos teóricos
Distinguir evento, alerta, incidente, evidencia, indicador, señal, hipótesis de investigación, contención, erradicación y recuperación. Un log no es evidencia suficiente por sí mismo: necesita integridad, contexto, tiempo, origen y cadena de custodia cuando corresponda.

### L2. Fundamentos matemáticos y formales
Usar correlación temporal, ventanas, grafos de eventos y modelos de secuencia. Medir precisión, recall, FPR, FNR, prevalencia, MTTD/MTTA/MTTR y cobertura; definir denominadores y unidad de análisis. La tasa base afecta el valor predictivo: una alerta con buen recall puede producir muchos falsos positivos en eventos raros.

### L3. Arquitectura y funcionamiento interno
Fuentes: endpoint, identidad, red, DNS, cloud control plane, aplicaciones, correo, CI/CD y sistemas físicos relevantes. Pipeline: recolección → normalización → enriquecimiento → correlación → detección → triage → caso → decisión → contención → recuperación → lecciones. Sincronizar tiempo y preservar fuente original.

### L4. Estándares y metodologías
NIST SP 800-61 Rev. 3 (2025) integra respuesta a incidentes en CSF 2.0 y sustituye Rev. 2. El modelo conecta Govern, Identify y Protect (preparación), Detect, Respond y Recover (respuesta) con mejora continua en Identify/Improvement. Usar NIST SP 800-53 Release 5.2.0 para controles aplicables. Adaptar requisitos legales, privacidad y notificación a la jurisdicción y sector; no copiar plazos estadounidenses como si fueran colombianos.

### L5. Implementación técnica
Definir playbooks con disparador, alcance, severidad, autoridad, pasos, evidencia, comunicación, criterios de contención, rollback y validación de recuperación. Para cada alerta, conservar evento bruto, parser/version, reloj, regla, contexto y analista. Diseñar pruebas de detección con datos sintéticos y simuladores.

### L6. Análisis avanzado
Tratar evasión, telemetría faltante, retraso, duplicados, reloj sesgado, log poisoning, pérdida de colector, saturación, alert fatigue y dependencias de respuesta. La contención puede destruir evidencia o interrumpir misión; evaluar impacto antes de aislar. Incluir recuperación de identidad, llaves, backups y proveedores.

### L7. Perspectiva de seguridad
Amenazas: borrado/manipulación de logs, living-off-the-land, abuso de cuentas legítimas, movimiento lateral y ransomware. Respuesta: preservar, delimitar, contener proporcionalmente, erradicar, restaurar desde fuentes confiables y monitorizar reinfección. No atribuir actor sin evidencia suficiente.

### L8. Investigación científica
Pregunta: ¿qué campos mínimos de evento permiten reconstrucción robusta bajo pérdida/retraso? Hipótesis: identidad, recurso, acción, timestamp sincronizado, resultado y origen mejoran reconstrucción frente a eventos sin esos campos. Controlar pérdida y desorden; medir atribución correcta, secuencias reconstruidas y tiempo.

### L9. Laboratorios y datasets
LAB-FND-06A: generar trazas sintéticas normales y de incidente con pérdida, retraso, duplicados y alteración. Ground truth de secuencias; evaluar parsers y reglas en entorno desconectado. Los playbooks se prueban en tabletop o simulador, no ejecutando contención sobre sistemas productivos.

### L10. Evaluación y benchmarks
Precision/recall, FPR/FNR, MTTD/MTTA/MTTR, completitud de eventos, cobertura de fuentes, tasa de reconstrucción correcta, tiempo de contención simulado, porcentaje de recuperación validada y recurrencia. Reportar intervalos y distribución por escenario.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.IR-TRIAGE-RECOVER`: validar alerta, alcance y autoridad; preservar datos; construir línea temporal; decidir contención; coordinar recuperación; verificar; documentar. Requiere permisos explícitos, matriz de escalamiento y kill switch. No ejecutar acciones destructivas automáticamente.

### L12. Trazabilidad y mantenimiento
Conservar case ID, timeline, hashes, fuente, zona horaria, versiones de reglas/parsers, decisiones, aprobaciones, cadena de custodia y postmortem. Actualizar playbooks tras cambios de infraestructura, amenazas o lecciones aprendidas; retener datos según política y ley aplicable.

### Profundización técnica derivada de fuentes primarias
NIST SP 800-61 Rev. 3 reemplaza el enfoque aislado de Rev. 2 por integración con CSF 2.0: Govern, Identify y Protect sostienen preparación y reducción de impacto; Detect, Respond y Recover articulan la respuesta; la mejora continua retroalimenta las funciones. La respuesta depende de roles internos y externos, incluida dirección, responsables técnicos, legal, comunicaciones y proveedores. El modelo no obliga a todas las organizaciones a usar idéntico organigrama o playbook; el contexto y la misión determinan la adaptación.

Un evento útil para reconstrucción requiere al menos identificador, fuente, sujeto/identidad, acción, objeto/recurso, resultado, timestamp con zona/precisión y contexto de correlación. Preservar el evento bruto y metadatos de parser; deduplicar por ID estable sin destruir procedencia. Un timeline ordenado no prueba causalidad: reloj sesgado, retraso, pérdida, duplicación y eventos fuera de banda deben representarse como incertidumbre. LAB-FND-06A comprueba ordenamiento y completitud sobre ground truth sintético, no detección ni atribución real.

## Tema 7 — Gobierno, riesgo y aseguramiento

**ID:** `foundations-07`  
**Objetivo:** asignar responsabilidad, decidir riesgo contextual, seleccionar controles y construir argumentos verificables de confianza.

### L1. Fundamentos teóricos
Distinguir gobierno, gestión, riesgo inherente/residual, apetito/tolerancia, obligación, política, control, evidencia, assurance, auditoría y autorización. El riesgo pertenece a una decisión y contexto; una puntuación no reemplaza al responsable que acepta el riesgo.

### L2. Fundamentos matemáticos y formales
Modelar escenario (R=(A,T,V,C,I,U)): activo, amenaza, vulnerabilidad, controles, impacto e incertidumbre. Usar árboles de escenarios, análisis bayesiano solo con priors/datos defendibles y Monte Carlo solo si las distribuciones están justificadas. Separar incertidumbre aleatoria de desconocimiento; realizar sensibilidad y análisis de rangos.

### L3. Arquitectura y funcionamiento interno
Estructura: órgano de gobierno → ejecutivo/risk owner → CISO/función de riesgo → propietarios de sistema/datos → control owners → operadores → auditoría independiente. Flujo: contexto → evaluación → tratamiento → implementación → assessment → autorización → monitoreo → reevaluación. Diferenciar primera, segunda y tercera línea según modelo organizativo.

### L4. Estándares y metodologías
NIST CSF 2.0 organiza resultados sin prescribir una única implementación; NIST SP 800-30 Rev. 1 guía evaluaciones de riesgo y exige hacer explícitos modelo, supuestos y reglas de combinación; SP 800-37 Rev. 2 define RMF en siete pasos (Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor); SP 800-53 Release 5.2.0 cataloga controles. La autorización es una decisión del responsable competente sustentada en evidencia, no una aprobación automática por completar una checklist. ISO 27001/27005, CIS Controls y regulación local tienen propósitos distintos. Mapear requisitos sin asumir equivalencia ni certificación automática.

### L5. Implementación técnica
Mantener registro de riesgos con escenario, causa, consecuencia, owner, controles, evidencia, residual, tratamiento, fecha, vencimiento y aceptación. Crear matriz requisito–control–prueba–evidencia. Construir assurance case con claim, subclaims, argumentos, supuestos y evidencia. Los controles deben tener criterio de operación y test.

### L6. Análisis avanzado
Analizar concentración de proveedores, riesgo sistémico, conflicto de interés, control compensatorio, riesgo de cambio, deuda técnica, incentivos perversos, métricas manipulables y riesgo residual correlacionado. Evitar falsa precisión en matrices 5×5 y riesgo agregado que oculte colas de impacto catastrófico.

### L7. Perspectiva de seguridad
Gobierno debe cubrir abuso interno, terceros, privacidad, safety, continuidad, supply chain y divulgación. Asegurar segregación entre quien opera y quien verifica, gestión de excepciones, protección de evidencia, canal de escalamiento y aceptación formal del riesgo por autoridad competente.

### L8. Investigación científica
Pregunta: ¿la trazabilidad requisito–control–prueba–evidencia mejora la detección de controles no operativos frente a revisión documental? Hipótesis: las pruebas basadas en escenarios detectan más fallos reproducibles que el checklist aislado. Diseño con casos sintéticos y revisores ciegos; controlar experiencia y sesgo de selección.

### L9. Laboratorios y datasets
LAB-FND-07A: caso organizacional sintético con 20 riesgos, owners, controles, evidencias válidas/obsoletas y excepciones. Construir matriz y assurance case; introducir evidencias contradictorias y controles no implementados. No usar información confidencial real.

### L10. Evaluación y benchmarks
Cobertura de riesgos críticos, porcentaje con dueño, evidencia vigente, controles probados, excepciones vencidas, tiempo de tratamiento, falsos cierres y acuerdo entre evaluadores. Evaluar calidad del argumento y suficiencia de evidencia, no cantidad de controles listados.

### L11. Conocimiento operativo
Skill candidata `FOUNDATIONS.RISK-ASSURANCE`: fijar contexto, facilitar identificación de escenarios, revisar controles/evidencia, analizar residual, proponer tratamiento y escalar aceptación. La IA puede asistir y documentar; no aceptar riesgo ni certificar cumplimiento en nombre del responsable.

### L12. Trazabilidad y mantenimiento
Versionar políticas, matriz de obligaciones, registro de riesgos, controles, evidencias, responsables, decisiones y excepciones. Mantener fecha de vigencia y jurisdicción. Revisar ante cambios legales, incidentes, proveedores, misión, arquitectura o apetito de riesgo.

### Profundización técnica derivada de fuentes primarias
El RMF de NIST SP 800-37 Rev. 2 consta de Prepare, Categorize, Select, Implement, Assess, Authorize y Monitor. Prepare-System identifica misión, stakeholders, ciclo de vida de información, evaluación de riesgo y requisitos priorizados; Monitor adapta la frecuencia a criticidad y volatilidad de controles. La selección de controles y su implementación no equivalen a evaluación; evaluación tampoco equivale a autorización. La autoridad de riesgo recibe evidencia, limitaciones y riesgo residual y decide dentro de su competencia. Monitor observa cambios del sistema y entorno, y alimenta reevaluaciones. Los controles heredados necesitan proveedor, alcance y evidencia de que siguen aplicando.

NIST SP 800-30 Rev. 1 requiere explicitar propósito, alcance, supuestos, restricciones, modelo de riesgo y regla de combinación. La incertidumbre inherente (conocimiento incompleto de amenazas, vulnerabilidades no descubiertas y dependencias desconocidas) se propaga a la evaluación; comunicar una puntuación sin incertidumbre crea falsa precisión. Separar la incertidumbre aleatoria (variabilidad) de la incertidumbre epistémica (falta de conocimiento); reportar rangos y sensibilidad cuando no existan frecuencias defendibles. El CSF 2.0 describe resultados deseables y Profiles/Tiers para contextualizar; no prescribe una receta técnica ni otorga certificación automática. Un crosswalk entre marcos es una relación orientativa, no equivalencia uno-a-uno ni prueba de cumplimiento.

## Matriz de brechas y correcciones de esta iteración

| Hallazgo de auditoría | Corrección aplicada | Estado verificable |
|---|---|---|
| El documento transversal no asignaba explícitamente sus bloques a los siete temas del currículo | Se añadieron siete dossiers con ID estable y alcance propio | Documental incorporado |
| La capa formal estaba tratada de forma desigual | Cada tema incluye modelos, fórmulas o justificación formal y límites | Documental incorporado; revisión matemática independiente pendiente |
| Los protocolos de laboratorio no estaban alineados uno a uno con los temas | Se añadieron LAB-FND-01A a LAB-FND-07A con datos sintéticos, ground truth y métricas | Diseñados; no ejecutados |
| La agenda de investigación usaba siete líneas que no coincidían con el currículo | Debe alinearse a los siete IDs de esta auditoría | Corrección de agenda pendiente en este commit |
| Fuentes citadas no tenían lectura integral acreditada | Se limita la afirmación a metadatos/abstract/página oficial inspeccionados | Lectura completa pendiente |
| Skills no tenían pruebas de promoción | Se mantienen como candidatas con precondiciones, parada y rollback | No validadas |
| No había trazabilidad por tema×capa | Se enlaza cada ID con este documento y estado `in_progress` en matriz JSON/Markdown | Pendiente de actualización de matrices |

## Dictamen de auditoría documental

- Siete temas identificados y desarrollados por separado: **sí, en esta versión documental**.
- Doce capas descritas para cada tema: **sí, como contenido de trabajo y criterios verificables**.
- K3/K4/K5: **no acreditados**.
- M3/M4/M5: **no acreditados**.
- Laboratorios ejecutados: **cero acreditados en esta iteración**.
- Revisión independiente: **pendiente**.
- G1–G8: **ninguna se declara aprobada**. Las puertas dependientes de ejecución o revisión externa permanecen bloqueadas hasta disponer de evidencia.


## Protocolos operativos y evaluación por tema — complemento obligatorio

Los protocolos siguientes son diseños reproducibles para ejecución posterior. No se declara que se hayan ejecutado. En todos los casos, guardar artefactos en una carpeta de ejecución separada, registrar commit, versiones, fecha UTC, semilla y hashes; usar datos sintéticos; no conectar sistemas productivos.

### LAB-FND-01A — Modelos de seguridad y confianza

- **Precondiciones:** Python fijado por lockfile; simulador local; política de prueba versionada; sin credenciales reales.
- **Datos:** matriz de 3 sujetos × 4 recursos × 5 acciones, atributos de contexto y un ground truth revisado manualmente.
- **Pasos:** (1) validar esquema y tipos; (2) cargar políticas RBAC y ABAC de referencia; (3) generar casos permitidos/denegados; (4) mutar atributos, expirar sesiones y revocar permisos; (5) ejecutar motor de decisión; (6) comparar con ground truth; (7) introducir fallo de IdP/PDP y observar modo degradado.
- **Salida esperada:** CSV de decisiones, matriz de confusión, latencias y lista de rutas no mediadas.
- **Verificación:** repetir con la misma semilla y obtener el mismo conjunto de casos y decisiones; revisar manualmente todos los falsos permisos.
- **Limpieza/rollback:** borrar contenedor y datos sintéticos; restaurar versión de política inicial. No hay cambios externos.

**Ejemplo:** un usuario con rol de lectura puede consultar un expediente no restringido y no puede exportarlo. **Contraejemplo:** asumir que pertenecer a la VLAN corporativa autoriza una acción sobre cualquier recurso.

**Evaluación:** explicar por qué autenticación no equivale a autorización; derivar una regla ABAC; identificar un bypass en un flujo API→backend. Rúbrica: modelo correcto, supuestos explícitos, prueba negativa, explicación de riesgo residual.

### LAB-FND-02A — Inventario y clasificación de activos

- **Precondiciones:** dataset generator local; esquema de inventario versionado; fuentes sintéticas CMDB/cloud/EDR/DNS.
- **Datos:** 500 registros sintéticos; incluir duplicados, cambios de hostname, recursos efímeros, activos sin dueño y registros obsoletos. El generador crea el ground truth por separado.
- **Pasos:** (1) validar esquema; (2) normalizar identificadores y timestamps; (3) reconciliar por claves fuertes; (4) poner coincidencias ambiguas en cola humana; (5) asignar clasificación y propietario; (6) comparar con ground truth; (7) repetir con una fuente deliberadamente incompleta.
- **Salida esperada:** inventario reconciliado, conflictos, activos huérfanos, métricas precision/recall/F1 y reporte de frescura.
- **Verificación:** no fusionar automáticamente registros ambiguos; preservar referencia a cada fuente; recalcular métricas desde datos brutos.
- **Limpieza/rollback:** eliminar snapshots sintéticos y conservar solo el manifiesto/hash de ejecución.

**Ejemplo:** dos recursos cloud con IDs distintos no se fusionan aunque compartan hostname. **Contraejemplo:** usar hostname como clave primaria global y descartar la procedencia de registros.

**Evaluación:** resolver tres conflictos de identidad de activo y justificar la confianza de cada decisión. Rúbrica: precisión, procedencia, tratamiento de incertidumbre y conservación de huérfanos.

### LAB-FND-03A — Superficie de ataque y modelado de amenazas

- **Precondiciones:** arquitectura sintética multi-tier, herramienta de diagramación local y alcance escrito del escenario.
- **Datos:** API, IdP, cola, base de datos, CI/CD, proveedor externo y 30 escenarios etiquetados; etiquetas revisadas por dos evaluadores.
- **Pasos:** (1) delimitar misión y activos; (2) dibujar contexto y DFD; (3) marcar trust boundaries; (4) enumerar amenazas STRIDE y abuse cases; (5) construir rutas AND/OR; (6) asociar controles y pruebas; (7) comparar con ground truth; (8) resolver desacuerdos y registrar adjudicación.
- **Salida esperada:** DFD versionado, threat register, attack graph y tabla de omisiones/falsos positivos.
- **Verificación:** toda amenaza crítica debe tener activo, precondición, consecuencia y evidencia/test; repetir evaluación ciega.
- **Limpieza/rollback:** retirar diagramas temporales y restaurar versión inicial del modelo.

**Ejemplo:** una identidad de pipeline con permisos de escritura sobre producción introduce una ruta de compromiso de supply chain. **Contraejemplo:** marcar “SQL injection” como riesgo sin endpoint, dato, precondición, impacto ni prueba.

**Evaluación:** producir un escenario completo y distinguir amenaza de vulnerabilidad y riesgo. Rúbrica: cobertura, factibilidad, causalidad, control y trazabilidad.

### LAB-FND-04A — Identidad y control de acceso

- **Precondiciones:** IdP de laboratorio aislado, dos aplicaciones demo, dos identidades de workload y secretos ficticios.
- **Datos:** tres roles, dos tenants, tokens de prueba y casos de expiración/revocación/audience/scope.
- **Pasos:** (1) configurar emisores y audiencias de prueba; (2) emitir tokens ficticios; (3) ejecutar flujos legítimos; (4) ejecutar pruebas negativas con issuer/audience/scope incorrectos; (5) revocar y medir propagación; (6) revisar cuentas sin owner; (7) verificar que no exista bypass directo al recurso.
- **Salida esperada:** matriz de autorización, registros de rechazo, tiempo de revocación y fallos legítimos.
- **Verificación:** todo caso negativo se rechaza; toda identidad tiene owner/propósito; no se almacenan tokens en artefactos.
- **Limpieza/rollback:** destruir tenant de laboratorio, invalidar tokens ficticios y eliminar secretos de prueba.

**Ejemplo:** un token válido para API-A se rechaza en API-B si el audience no coincide. **Contraejemplo:** aceptar cualquier JWT con firma válida sin validar issuer, audience, expiración y claims requeridos.

**Evaluación:** analizar una delegación excesiva y proponer revocación segura. Rúbrica: protocolo correcto, mínimo privilegio, pruebas negativas y recuperación.

### LAB-FND-05A — Criptografía y protección de datos

- **Precondiciones:** biblioteca criptográfica mantenida, entorno aislado, KMS simulado y vectores de prueba publicados por el proveedor del algoritmo.
- **Datos:** mensajes ficticios, certificados de prueba, claves efímeras generadas durante la ejecución; nunca guardar material secreto.
- **Pasos:** (1) fijar biblioteca/versión y parámetros; (2) ejecutar vectores conocidos; (3) cifrar/descifrar con AEAD; (4) alterar ciphertext y verificar rechazo; (5) probar rotación y recuperación con llaves de laboratorio; (6) medir latencia y errores; (7) inspeccionar logs para confirmar ausencia de secretos.
- **Salida esperada:** reporte de vectores, interoperabilidad, latencia, fallos y rotación; manifiesto sin claves.
- **Verificación:** mensajes alterados se rechazan; parámetros/nonce cumplen el contrato del algoritmo; restauración funciona con claves ficticias.
- **Limpieza/rollback:** destruir llaves temporales, limpiar KMS simulado y conservar únicamente resultados saneados.

**Ejemplo:** AEAD protege confidencialidad e integridad del mensaje bajo sus supuestos y uso correcto del nonce. **Contraejemplo:** afirmar que cifrar una base de datos impide que una aplicación comprometida lea los datos descifrados.

**Evaluación:** seleccionar mecanismo para confidencialidad, integridad o firma y explicar límites. Rúbrica: selección adecuada, gestión de claves, supuestos, vectores y ausencia de secretos.

### LAB-FND-06A — Detección, respuesta y recuperación

- **Precondiciones:** SIEM/simulador local, reloj de laboratorio controlado y reglas versionadas.
- **Datos:** trazas sintéticas normales e incidentes con ground truth; variantes con pérdida, duplicación, retraso y timestamps alterados.
- **Pasos:** (1) generar trazas; (2) registrar hashes; (3) ingerir y normalizar; (4) ejecutar reglas; (5) correlacionar eventos; (6) comparar detecciones y timeline con ground truth; (7) ejecutar tabletop de contención y recuperación; (8) verificar restauración y monitoreo posterior.
- **Salida esperada:** alertas, timeline, matriz de confusión, métricas operativas y acta del tabletop.
- **Verificación:** distinguir detección de atribución; preservar eventos brutos; calcular denominadores y FPR/FNR; documentar falsos positivos/negativos.
- **Limpieza/rollback:** reiniciar simulador y borrar datos de ejecución; no realizar aislamiento real ni alterar sistemas externos.

**Ejemplo:** eventos con identidad, recurso, acción y timestamp permiten enlazar una secuencia con mejor contexto. **Contraejemplo:** atribuir un incidente a un actor solo por una dirección IP o un IOC aislado.

**Evaluación:** reconstruir una secuencia con eventos faltantes y decidir qué conclusiones no están justificadas. Rúbrica: integridad temporal, incertidumbre, preservación y decisión proporcional.

### LAB-FND-07A — Gobierno, riesgo y aseguramiento

- **Precondiciones:** caso organizacional ficticio, taxonomía de riesgos y plantilla de assurance case.
- **Datos:** 20 escenarios, owners, controles, evidencia válida/obsoleta/contradictoria y excepciones con vencimiento.
- **Pasos:** (1) fijar contexto y apetito de riesgo ficticio; (2) asignar owners; (3) construir registro de riesgos; (4) mapear requisito→control→prueba→evidencia; (5) marcar evidencia insuficiente/caducada; (6) construir claim/argument/evidence; (7) someter a revisión ciega; (8) adjudicar desacuerdos.
- **Salida esperada:** risk register, matriz de trazabilidad, assurance case y reporte de falsos cierres.
- **Verificación:** ningún riesgo crítico sin dueño; ninguna afirmación de control eficaz sin evidencia pertinente; excepciones con responsable y fecha.
- **Limpieza/rollback:** archivar solo datos sintéticos y borrar copias de trabajo.

**Ejemplo:** un control de backup se considera probado solo si hay restauración documentada y verificada. **Contraejemplo:** declarar continuidad porque existe una política escrita o un contrato de backup.

**Evaluación:** revisar un claim y detectar evidencia que no lo sustenta. Rúbrica: trazabilidad, calidad de argumento, gestión de incertidumbre y autoridad de aceptación.

## Rúbrica transversal de salida por tema

Puntuar cada criterio 0–2: 0 ausente/incorrecto; 1 parcial o no reproducible; 2 completo y respaldado. Criterios: (a) definiciones y alcance; (b) modelo y supuestos; (c) arquitectura/flujo; (d) estándares y versión; (e) procedimiento reproducible; (f) fallos y límites; (g) controles y riesgo residual; (h) hipótesis y validez; (i) dataset/ground truth; (j) métricas y baselines; (k) Skill con permisos/parada/rollback; (l) trazabilidad. Un puntaje documental no aprueba G5/G7/G8: esas puertas requieren ejecución, reproducción y revisión real. Un cero en seguridad, procedencia o trazabilidad bloquea la promoción del tema.


## Laboratorios sintéticos adicionales — 2026-11-20

### LAB-FND-08A — Conflicto safety/security

- **Escenario:** controlador de acceso con fallo de energía durante una emergencia. El control electrónico mantiene ingress bloqueado (fail-secure), mientras un mecanismo mecánico independiente permite egress.
- **Pregunta:** ¿se pueden satisfacer simultáneamente la protección frente a entrada no autorizada y la evacuación segura?
- **Modelo:** estados de emergencia, bloqueo electrónico, salida mecánica independiente y condiciones de autorización.
- **Aserción:** safety_egress_preserved y security_ingress_denied deben ser verdaderos. Un único estado fail-secure no es suficiente si impide salida.
- **Límite:** modelo lógico sintético; no sustituye HAZOP/STPA, diseño de puertas ni certificación física.

### LAB-FND-09A — Privacidad no es confidencialidad

- **Escenario:** telemetría cifrada y con acceso restringido se reutiliza para una finalidad incompatible.
- **Pregunta:** ¿puede fallar privacidad mientras confidencialidad permanece protegida?
- **Modelo:** cifrado, control de acceso, finalidad, minimización, retención y compatibilidad de uso.
- **Aserción:** confidentiality_protected y privacy_risk_detected pueden ser verdaderos al mismo tiempo; la mitigación exige finalidad compatible, minimización y retención limitada.
- **Límite:** no determina base legal ni derechos; requiere análisis jurídico contextual.

### LAB-FND-10A — Recuperación de confianza

- **Escenario:** el servicio se restaura desde backup, pero credenciales del atacante siguen válidas.
- **Pregunta:** ¿se recuperó disponibilidad, confianza o ambas?
- **Modelo:** restauración, compromiso de credenciales, rotación, reconstrucción de identidad y procedencia del backup.
- **Aserción:** service_available_after_restore puede ser verdadero mientras trust_restored_before_controls es falso.
- **Límite:** no prueba recuperación real; exige restore test, rotación de secretos y verificación de estado en ambiente aislado.

### LAB-FND-11A — Redundancia y causa común

- **Escenario:** dos nodos independientes comparten el mismo proveedor de identidad.
- **Pregunta:** ¿la redundancia nominal mantiene la misión cuando falla la dependencia común?
- **Modelo:** nodos, dependencia compartida, fallo común y ruta independiente de recuperación.
- **Aserción:** common_cause_detected debe ser verdadero; una ruta de recuperación independiente puede sostener servicio degradado.
- **Límite:** la independencia real requiere análisis de proveedores, energía, red, identidad, DNS, administración y ubicación.

### LAB-FND-12A — Integridad, autenticidad y verdad

- **Escenario:** una lectura de sensor está firmada y su hash coincide, pero el sensor tiene calibración vencida.
- **Pregunta:** ¿qué demuestra la firma y qué no demuestra?
- **Modelo:** firma, hash, calibración, contraste con sensor independiente y validez semántica.
- **Aserción:** integrity_and_authenticity puede ser verdadero mientras semantic_validity_before_review es falso.
- **Límite:** la validez física exige calibración, metrología y evidencia del proceso de medición.

Los cinco laboratorios se ejecutan como modelos deterministas en CI. Los resultados sintéticos no acreditan O1 de un sistema real, ni sustituyen ensayos físicos, evaluación de safety o revisión independiente.
