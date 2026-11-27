# Evaluación en frío FND-01.01 — versión 2

**Estado:** instrumento corregido; listo para administración externa; no administrado.  
**Duración:** 150 minutos. **Puntaje:** 100 puntos. **Acceso del candidato:** solo este documento y los anexos de datos que entregue el administrador.  
**Prohibido al candidato:** consultar el dossier, las soluciones modelo, la guía del evaluador o la matriz durante la prueba.

## Propósito y condiciones

Evaluar transferencia individual en cinco dimensiones: enseñar, explicar, analizar, diseñar e integrar. No evalúa memoria literal. El candidato debe declarar supuestos, separar hechos de inferencias, identificar incertidumbre y abstenerse de dar consignas físicas no autorizadas.

El administrador debe seleccionar una variante A, B o C al azar, sin informar previamente cuál se utilizará. La variante se entrega solo al inicio. No utilizar la misma variante en una repetición inmediata. La evaluación debe ser supervisada y conservar respuestas originales, tiempo y versión.

## Distribución y puntuación

| Bloque | Capacidad | Peso |
|---|---|---:|
| A | Enseñar | 15 |
| B | Explicar | 15 |
| C | Analizar | 30 |
| D | Diseñar | 30 |
| E | Integrar y refutar | 10 |
| **Total** | | **100** |

Cada bloque se califica de 0 a 4 mediante la rúbrica común. Conversión: puntos del bloque = (nivel / 4) × peso. El resultado total es la suma de los cinco bloques. No redondear cada bloque; redondear el total a una cifra decimal.

**Umbral de aprobación de trabajo:** total ≥ 80/100, cada bloque ≥ 3/4, ninguna falla crítica y acuerdo entre dos evaluadores. Un total alto no compensa un bloque inferior a 3/4. La aprobación es de esta unidad y de este instrumento, no acredita por sí sola T4.

## Rúbrica común 0–4

- **0 — ausente/incorrecto:** no responde o presenta errores fundamentales.
- **1 — nominal:** enumera términos o controles sin causalidad, contexto ni criterio verificable.
- **2 — parcial:** resuelve lo evidente, pero omite dependencias, incertidumbre, trade-offs o evidencia relevante.
- **3 — competente:** razonamiento técnicamente correcto, contextualizado y verificable; identifica límites, alternativas y riesgo residual.
- **4 — experto demostrable en la tarea:** integra modelos, contraejemplos, dependencias y límites; justifica decisiones frente a alternativas, identifica qué evidencia refutaría su conclusión y transfiere a condiciones nuevas. No se otorga por extensión o jerga.

## A. Enseñar — 15 puntos

Diseña una microlección de 12 minutos para un equipo mixto de software, operaciones y privacidad que confunde:
- privacidad con confidencialidad;
- safety con ciberseguridad;
- resiliencia con backup;
- disponibilidad con confiabilidad.

Incluye:
1. prerrequisitos y tres objetivos observables;
2. secuencia didáctica desde un caso concreto hasta abstracciones;
3. un ejemplo y un contraejemplo para cada confusión;
4. una pregunta de transferencia no memorizable y criterios de evaluación;
5. una actividad que muestre cómo una propiedad puede mejorar mientras otra empeora.

## B. Explicar — 15 puntos

Explica el siguiente sistema conceptual: sensores redundantes alimentan un controlador local; el controlador recibe cambios de consigna desde una pasarela remota; la pasarela depende de un proveedor de identidad, DNS y un plano de administración compartido por dos regiones; los registros contienen identidad de operadores.

Entrega:
1. diagrama lógico textual de componentes, flujos y dependencias;
2. explicación causal de cómo una falla de identidad afecta (o no) el control local;
3. análisis de por qué redundancia física y redundancia regional no prueban independencia;
4. distinción entre seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia;
5. evidencia necesaria para sostener cada afirmación principal.

## C. Analizar — 30 puntos

El administrador entregará una sola variante:

### Variante A — proceso de agua

Una planta de tratamiento pierde conectividad con identidad central. El controlador local continúa, pero dos sensores divergen. Una actualización de proveedor se aplicó 40 minutos antes. Las regiones de respaldo comparten identidad y administración. Los logs identifican operadores y no tienen retención definida.

### Variante B — cadena de frío farmacéutica

Un centro logístico pierde el servicio de autorización en la nube. Los controladores locales siguen activos, pero la telemetría de dos cámaras difiere. El firmware se actualizó el mismo día. El proveedor remoto administra ambos sitios con una cuenta de servicio común. Los logs incluyen identificadores de empleados y eventos de temperatura.

### Variante C — infraestructura de edificios

Un centro de control pierde su broker de identidad. HVAC y control de acceso siguen operativos localmente. Un sensor de ocupación y un sensor ambiental entregan datos contradictorios. Un integrador externo administra dos edificios desde el mismo plano de gestión. Los registros conservan identificadores y patrones de presencia.

Analiza:
- misión, funciones esenciales, activos, sujetos y fronteras;
- hechos, hipótesis, datos faltantes y confianza;
- peligros, fallos accidentales, amenazas y causas comunes sin confundirlos;
- propiedades afectadas, conflictos y posibles efectos en personas;
- dependencias técnicas, organizacionales y de proveedor;
- alternativas de contención/modo degradado y condiciones de uso;
- criterios de parada, escalamiento y retorno a servicio;
- riesgo residual, autoridad y evidencia que modificaría la decisión.

Compara al menos tres alternativas. No prescribas consignas físicas, temperaturas objetivo, dosis, parámetros de proceso ni bypass de seguridad. Especifica quién debe determinarlos y bajo qué evidencia.

## D. Diseñar — 30 puntos

A partir de la variante, diseña una arquitectura conceptual y verificable.

Entregables:
1. requisitos con identificador, sujeto, condición, comportamiento y criterio de aceptación;
2. diagrama de zonas, flujos y límites de confianza;
3. modelo de estados normal, degradado, mantenimiento, recuperación y retorno;
4. acceso de emergencia nominal, temporal, limitado, aprobado, auditable y revocable;
5. protección de integridad, secuencia y frescura de órdenes;
6. tratamiento de dependencias compartidas y fallos correlacionados;
7. privacidad por diseño para telemetría y registros;
8. continuidad y recuperación de identidad, configuración, claves, proveedor y datos;
9. plan de verificación estática y plan futuro de laboratorio aislado, con casos positivos, negativos, fallos y rollback;
10. argumento de assurance: claims, argumentos, evidencia, supuestos, derrotadores y riesgo residual.

No se acepta una lista de productos o controles sin justificar el comportamiento que se pretende garantizar.

## E. Integrar y refutar — 10 puntos

Identifica una decisión de diseño propia que pueda ser refutada. Indica:
- la hipótesis que la sostiene;
- un contraejemplo;
- la evidencia mínima que la refutaría;
- el cambio de arquitectura o decisión que seguiría;
- qué conclusión no puedes sostener todavía.

## Fallas críticas automáticas

Cualquiera de las siguientes impide aprobar, independientemente del puntaje:
1. tratar privacidad como sinónimo de cifrado o confidencialidad;
2. equiparar safety con ciberseguridad;
3. afirmar que backup equivale a resiliencia;
4. suponer independencia sin modelar dependencias comunes;
5. recomendar desactivar controles o interlocks sin análisis de peligros, autoridad y límites;
6. inventar parámetros operacionales o consignas físicas;
7. confundir un plan de prueba con evidencia de prueba ejecutada;
8. afirmar que un sistema es seguro/confiable por ausencia de incidentes;
9. ignorar daño a personas por tratamiento de datos;
10. ocultar incertidumbre o presentar supuestos como hechos.

## Registro de administración

El administrador registra: ID seudónimo del candidato, fecha/hora, variante, versión, duración, incidencias, respuestas originales, puntajes por bloque, fallas críticas, evaluadores, conflictos de interés y acuerdo/desacuerdo. No incluir nombre, documento, correo ni datos sensibles del candidato en la biblioteca pública.

La calificación debe ser doble e independiente. Cada evaluador puntúa antes de discutir. Si difieren en más de un nivel en cualquier bloque o más de 10 puntos en total, un tercer evaluador adjudica. Conservar ambas hojas originales y la resolución.

## Estado

Instrumento preparado. No administrado. No hay candidato evaluado, puntuación, resultado de aprendizaje ni aprobación que registrar todavía.
