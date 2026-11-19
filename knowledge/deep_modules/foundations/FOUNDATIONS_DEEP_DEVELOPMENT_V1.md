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
| FND-14 | Cinco protocolos de laboratorio definidos | Ejecución, datos, scripts y resultados |
| FND-15 | Evaluación y rúbrica diseñadas | Pruebas aplicadas, resultados y evaluación externa |

## 16. Estado de las 12 capas y puertas

L1 fundamentos: desarrollo ampliado; revisión de cobertura pendiente.
L2 formal/matemática: modelos introductorios documentados; validación formal y calibración pendientes.
L3 arquitectura: ciclo de vida y grafos documentados; casos ejecutados pendientes.
L4 estándares: alcance comparativo inicial; revisión de versiones y mapeos pendientes.
L5 implementación: procedimientos y casos definidos; artefactos ejecutables parciales.
L6 análisis avanzado: límites, fallos y trade-offs desarrollados; pruebas de estrés pendientes.
L7 seguridad: amenazas adversariales y no adversariales integradas; revisión especializada pendiente.
L8 investigación: agenda y diseño de método; revisión sistemática no ejecutada.
L9 laboratorios: cinco protocolos diseñados; cero ejecuciones acreditadas en este documento.
L10 evaluación: métricas y rúbricas especificadas; benchmarks no ejecutados.
L11 operación/Skills: cinco Skills candidatas; no promovidas.
L12 trazabilidad: referencias y estados documentados; lectura integral, hashes y revisión periódica incompletos.

Puertas G1–G8: no se declaran aprobadas por este cambio. G1/G3 tienen evidencia documental ampliada que requiere auditoría de cobertura; G2 permanece parcial; G4 parcial; G5/G6/G7 pendientes de ejecución; G8 pendiente de revisión independiente. Madurez conservadora del módulo: M2 editorial ampliado, investigación exploratoria; no K4/K5 ni M4/M5.

## 17. Fuentes primarias y estado de lectura

- NIST CSWP 29, Cybersecurity Framework 2.0 (2024), https://doi.org/10.6028/NIST.CSWP.29 — página oficial y contenido consultado; lectura integral no certificada.
- NIST SP 800-30 Rev. 1 (2012), https://doi.org/10.6028/NIST.SP.800-30r1 — secciones de modelo de riesgo inspeccionadas; no lectura lineal certificada.
- NIST SP 800-37 Rev. 2 (2018), https://doi.org/10.6028/NIST.SP.800-37r2 — descripción oficial y extractos de RMF consultados; texto completo pendiente de lectura registrada.
- NIST SP 800-160 Vol. 1 Rev. 1 (2022), https://doi.org/10.6028/NIST.SP.800-160v1r1 — descripción oficial y contenido previamente inspeccionado; lectura integral pendiente.
- NIST SP 800-61 Rev. 3 (2025), https://doi.org/10.6028/NIST.SP.800-61r3 — descripción oficial consultada; lectura por secciones y trazabilidad pendiente.
- ISO 31000:2018, https://www.iso.org/standard/65694.html — ficha oficial; texto normativo completo no incluido ni declarado leído.
- MITRE ATT&CK Enterprise Introduction, https://attack.mitre.org/resources/enterprise-introduction/ — introducción oficial consultada; versión y fecha de captura deben registrarse en el registro de fuentes.

La consulta de una ficha oficial no equivale a lectura completa. No se atribuyen a estas fuentes resultados experimentales.

## 18. Criterio de salida de Foundations

No avanzar al módulo 2 hasta completar: revisión tema×capa con evidencia; lectura y extracción de fuentes prioritarias; solución documental de brechas críticas; casos integradores resueltos; laboratorios ejecutados y resultados reproducibles cuando proceda; auditoría de consistencia y duplicación; actualización del índice y tracker. Revisión independiente externa puede seguir pendiente, pero debe quedar explícitamente bloqueante para K4/K5 y no confundirse con cierre editorial.

Este documento amplía la base técnica y define el trabajo restante. No certifica por sí mismo la finalización del estándar.
