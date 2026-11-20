# FND-01.01 — Anexo de profundización técnica y análisis de caso V1

**Propósito:** ampliar la unidad sobre seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia con modelos formales aplicados, análisis causal y un diseño de referencia. Este anexo no sustituye las fuentes normativas ni certifica dominio.
**Estado:** material de desarrollo interno; requiere revisión técnica independiente. **Madurez:** T0/O0. Los cálculos son ejemplos analíticos, no mediciones de un sistema real.

## 1. Delimitar propiedades antes de seleccionar controles

Una propiedad debe expresarse sobre un sujeto y una función, dentro de un contexto y un horizonte temporal. Una frase como «el sistema es seguro» no es un requisito verificable. La forma mínima es:

`P = (sujeto, activo/función, propiedad, condición, horizonte, criterio, evidencia)`

Ejemplo: «El servicio de dosificación mantiene la concentración dentro del intervalo operativo autorizado durante pérdida de conectividad con el plano de supervisión, por un máximo de 20 minutos; se verifica mediante análisis de estados, pruebas de transición y registros firmados».

La formulación no implica que el sistema real sea seguro. Obliga a identificar: quién o qué debe permanecer protegido; cuál es la función; bajo qué perturbación; por cuánto tiempo; qué desviación es tolerable; y qué evidencia permite aceptar el resultado.

### 1.1 Propiedades relacionadas, no intercambiables

| Propiedad | Pregunta de aceptación | Evidencia típica | Error frecuente |
|---|---|---|---|
| Seguridad de la información | ¿Se preservan los activos frente a acciones no autorizadas? | Política, pruebas de autorización, análisis de amenazas | Reducirla a confidencialidad |
| Safety | ¿Se evitan estados que puedan producir daño inaceptable? | Hazard analysis, requisitos de seguridad funcional, validación sectorial | Tratar todo incidente como ataque |
| Privacidad | ¿El tratamiento de datos evita problemas injustificados para personas? | Inventario de datos, propósito, minimización, evaluación de impacto | Equipararla a cifrado o secreto |
| Confiabilidad | ¿La función cumple lo especificado durante el intervalo? | Modelo de fallos, tasa de fallos, pruebas de fiabilidad | Suponer que «sin fallos observados» prueba fiabilidad |
| Disponibilidad | ¿La función está utilizable cuando se requiere? | SLI/SLO, ventana, población, degradación | Confundir uptime de proceso con servicio utilizable |
| Resiliencia | ¿El sistema limita impacto, mantiene funciones esenciales y se recupera/adapta? | Escenarios de perturbación, tiempos, integridad de recuperación | Reducirla a redundancia o backup |

Una misma decisión puede mejorar una propiedad y degradar otra. La decisión debe documentar el objetivo primario, los límites no negociables y la compensación aceptada por el responsable legítimo.

## 2. Modelos cuantitativos: alcance y supuestos

### 2.1 Confiabilidad y disponibilidad

Para un componente reparable con tiempos de operación y reparación estacionarios, independientes y representativos, una aproximación clásica es:

`A = MTBF / (MTBF + MTTR)`

Si MTBF = 1.000 h y MTTR = 4 h, entonces A ≈ 0,9960 (99,60%). Esto no es automáticamente la disponibilidad extremo a extremo: supone una unidad de análisis bien definida, distribución y régimen compatibles con el promedio, y no incorpora mantenimiento programado, degradación parcial, dependencias ni causas comunes.

Para una cadena de componentes en serie que deben funcionar todos, bajo independencia:

`A_system = Π A_i`

Con tres dependencias de disponibilidad 0,99, 0,995 y 0,999, la disponibilidad combinada es aproximadamente 0,9841 (98,41%), no 99,5%. El ejemplo muestra por qué la disponibilidad de cada proveedor no debe confundirse con la del servicio completo. La independencia es un supuesto fuerte: una región, identidad, DNS, KMS o plano de control compartido puede causar fallos correlacionados.

Para componentes redundantes en paralelo, bajo independencia y una lógica de conmutación perfecta:

`A_parallel = 1 - Π(1 - A_i)`

Dos componentes de 0,99 darían 0,9999 en ese modelo ideal. En la realidad deben modelarse fallo de conmutación, mantenimiento común, configuración compartida, firmware, alimentación, credenciales, red, errores humanos y fallos de modo común. No presentar el número ideal como predicción.

**Regla:** todo resultado cuantitativo debe incluir unidad de análisis, población, ventana, distribución asumida, independencia/correlación, datos de entrada, exclusiones e incertidumbre. Sin esos elementos, es una ilustración, no un SLA/SLO ni una estimación defendible.

### 2.2 Árbol de fallos y probabilidad

Un árbol de fallos parte de un evento superior no deseado y lo descompone en causas mediante puertas lógicas. Para eventos independientes A y B:

- AND: `P(A ∩ B) = P(A)P(B)`.
- OR: `P(A ∪ B) = P(A) + P(B) - P(A)P(B)`.

La independencia no se debe asumir por conveniencia. Si A y B comparten causa, el cálculo multiplicativo subestima el riesgo. El análisis cualitativo sigue siendo útil aunque no existan probabilidades confiables: identifica rutas causales, barreras y puntos únicos de fallo.

### 2.3 Safety: peligro, riesgo y barreras

No existe una única escala universal que permita convertir cualquier peligro en una probabilidad comparable. Un análisis debe distinguir:
- **Peligro (hazard):** condición con potencial de causar daño.
- **Situación peligrosa:** exposición de personas, ambiente o activos a ese peligro.
- **Evento iniciador:** transición o perturbación que contribuye a la situación.
- **Daño:** consecuencia materializada.
- **Riesgo:** combinación contextual de probabilidad/frecuencia y severidad, definida por el método sectorial aplicable.

La secuencia de análisis es: definir misión y contexto; identificar peligros; derivar escenarios; estimar severidad/exposición/probabilidad según método aceptado; establecer requisitos y barreras; verificar independencia y cobertura de barreras; validar el sistema integrado; documentar riesgo residual y autoridad de aceptación. No reemplazar un análisis sectorial de safety por una matriz genérica de ciber-riesgo.

### 2.4 Privacidad como riesgo para personas

El objeto de análisis no es solo la base de datos ni el atacante. Deben examinarse las acciones de tratamiento y sus consecuencias para individuos: vigilancia, discriminación, pérdida de autonomía, exposición, inferencias, exclusión, daño económico o físico y efectos colectivos. La probabilidad de una brecha de seguridad no equivale a la probabilidad de un problema de privacidad.

Un análisis de privacidad documenta al menos: población afectada; categorías y sensibilidad de datos; finalidad declarada y usos secundarios; origen y legitimidad de recolección; flujo y destinatarios; retención y eliminación; inferencias y enlaces; controles de acceso; transparencia y capacidad de ejercer derechos; impacto por escenario; mitigaciones; riesgo residual y responsable. Cifrado y control de acceso son salvaguardas, no demostración suficiente de privacidad.

## 3. Caso de diseño: control de dosificación de agua con supervisión remota

### 3.1 Contexto y límites

Sistema hipotético de dosificación en una planta pequeña. Un controlador local lee sensores y acciona una bomba; un operador remoto supervisa tendencias y modifica consignas mediante una pasarela. El proceso físico puede causar daño si la concentración sale del rango autorizado. No se especifican químicos, valores de proceso ni instrucciones de operación reales: estos deben proceder del ingeniero de proceso y la autoridad competente.

Activos y funciones:
- continuidad del control local seguro;
- integridad de sensor, consigna y firmware;
- autoridad de cambio de parámetros;
- disponibilidad de supervisión;
- registros mínimos necesarios para diagnóstico;
- datos de operadores y cuentas de mantenimiento.

Límites de confianza: sensor/controlador; controlador/actuador; red OT/DMZ; pasarela/servicio remoto; identidad/administración; repositorio de firmware; almacenamiento de telemetría. Cada frontera necesita identidad, autorización, validación de datos y tratamiento explícito de pérdida de comunicación.

### 3.2 Escenarios causales

| ID | Escenario | Propiedad principal | Consecuencia potencial | Barreras que deben evaluarse |
|---|---|---|---|---|
| H-01 | Sensor deriva o queda congelado | Safety, integridad, confiabilidad | Control basado en medición falsa | Diagnóstico de plausibilidad, sensor redundante independiente, límites físicos, estado seguro definido |
| H-02 | Pérdida de supervisión remota | Disponibilidad, resiliencia | Operador pierde visibilidad | Control local autónomo dentro de límites, alarma local, procedimiento de operación degradada |
| H-03 | Consigna remota no autorizada | Seguridad, safety | Cambio peligroso de proceso | Identidad fuerte, autorización por función, doble aprobación para cambios críticos, límites locales no anulables |
| H-04 | Actualización comprometida | Integridad, safety, seguridad | Comportamiento alterado | Firma y verificación de artefacto, arranque seguro, inventario, rollback autenticado, validación |
| H-05 | Telemetría contiene identidad de operador | Privacidad | Exposición y uso secundario | Minimización, seudonimización, acceso limitado, retención justificada, auditoría |
| H-06 | Restauración recupera configuración antigua | Integridad, resiliencia | Control con parámetros obsoletos | Versionado, validación de configuración, aprobación, reconciliación de estado antes de reanudar |

La tabla no constituye una HAZOP ni un análisis de riesgo terminado. Es un conjunto inicial de escenarios para iniciar el trabajo disciplinar. La lista debe ampliarse con operadores, ingeniería de proceso, seguridad funcional, ciberseguridad, mantenimiento y privacidad.

### 3.3 Arquitectura de referencia

1. El controlador mantiene el lazo de control local y los límites físicos de seguridad definidos por ingeniería de proceso.
2. La pasarela remota no puede desactivar ni sobreescribir los límites locales.
3. Las órdenes remotas son autenticadas, autorizadas por acción y validadas por rango, estado y vigencia.
4. Pérdida de conectividad no implica que el controlador acepte indefinidamente la última orden remota: la transición de modo debe especificarse y verificarse.
5. Cambios críticos requieren segregación de funciones y aprobación adicional.
6. Firmware y configuración tienen procedencia, versión, integridad y procedimiento de reversión.
7. Telemetría se minimiza; se separan datos de proceso de identificadores de personas cuando sea viable.
8. La recuperación comienza en modo aislado/degradado; la reanudación requiere reconciliar integridad de sensor, configuración, identidad y estado físico.

### 3.4 Requisitos verificables de ejemplo

- **REQ-SAF-01:** el controlador no ejecutará una consigna fuera de límites aprobados por el proceso, incluso si la orden procede de una cuenta privilegiada. Verificación: análisis de diseño y pruebas de frontera con valores sintéticos en banco aislado.
- **REQ-SEC-01:** cada cambio remoto deberá asociarse a una identidad individual, acción autorizada, versión anterior/nueva, instante y resultado. Verificación: pruebas de autorización y revisión de registros.
- **REQ-AV-01:** ante pérdida de la conexión remota, el control local conservará la función esencial definida por el análisis de peligros durante el horizonte aprobado. Verificación: análisis de estados y ensayo controlado posterior.
- **REQ-PRV-01:** los registros de telemetría no incluirán identificadores personales salvo que exista finalidad documentada y necesidad demostrada. Verificación: inspección de esquema y pruebas de datos sintéticos.
- **REQ-REC-01:** tras restauración, el sistema permanecerá en estado de reanudación controlada hasta validar firmware, configuración, parámetros y coherencia de sensores. Verificación: análisis de transición y ensayo de recuperación.

Cada requisito necesita propietario, trazabilidad a peligro/amenaza/impacto, condición inicial, criterio cuantitativo cuando sea posible, método de verificación, evidencia y autoridad de aceptación. Los valores concretos de rango, tiempo y tolerancia no se inventan: se obtienen de análisis de proceso y requisitos sectoriales.

### 3.5 Decisión de modo degradado

No existe una regla universal «fail-open» o «fail-closed». Para cada función, comparar:
- mantener control local autónomo;
- pasar a un estado seguro definido por el análisis de peligros;
- detener una función no esencial;
- exigir intervención humana local;
- limitar temporalmente la operación.

La selección depende del peligro físico, dinámica del proceso, posibilidad de supervisión local, tolerancia de continuidad y capacidad de recuperación. Un estado que protege el sistema informático puede causar un peligro físico; un estado que mantiene producción puede amplificar el daño. La autoridad de proceso y safety define el estado seguro, no una regla genérica de ciberseguridad.

## 4. Análisis de fallos y causas comunes

Para cada componente, documentar función, modo de fallo, causa, efecto local, efecto de sistema, detectabilidad, barrera, evidencia y acción. FMEA es útil para organizar fallos de componentes; no demuestra exhaustividad y no sustituye árboles de fallos, análisis de peligros, análisis de seguridad ni escenarios adversariales.

**Causas comunes que invalidan redundancia aparente:**
- dos sensores con mismo principio físico y misma vulnerabilidad ambiental;
- dos controladores con mismo firmware vulnerable;
- dos regiones que comparten plano de identidad o control;
- backup y producción con la misma credencial privilegiada;
- dos enlaces que comparten ducto, proveedor o energía;
- restauración que replica corrupción o configuración maliciosa.

Para evaluar independencia, identificar recursos compartidos y modelar eventos comunes explícitamente. La diversidad puede reducir ciertos fallos correlacionados, pero aumenta complejidad de integración y mantenimiento; debe justificarse, no asumirse superior.

## 5. Procedimiento estático de diseño y verificación

1. Definir contexto, misión, stakeholders, población, límites físicos y autoridad.
2. Crear inventario de activos, funciones, flujos, datos, interfaces y dependencias.
3. Separar amenazas intencionales, errores, fallos aleatorios, peligros de proceso y eventos externos.
4. Construir modelos causales apropiados: DFD y límites de confianza; árbol de fallos; FMEA; análisis de peligros; escenarios de privacidad.
5. Derivar requisitos con condición, criterio, propietario y evidencia.
6. Comparar alternativas mediante matriz de decisión, restricciones no negociables y sensibilidad.
7. Diseñar modos normales, degradados, mantenimiento, emergencia, recuperación y retorno a servicio.
8. Revisar que los controles no creen peligros nuevos ni transfieran el riesgo a personas o procesos.
9. Definir verificación estática, pruebas de banco, pruebas de integración y validación operacional futura por separado.
10. Registrar incertidumbres, exclusiones, riesgos residuales y autoridad que los acepta.

**Criterio de parada:** no emitir recomendación de configuración real si faltan análisis de peligros, valores de proceso, autoridad sectorial, límites de autorización o contexto operativo suficiente.

## 6. Evaluación fría ampliada: variantes nuevas

### Variante A — Telemetría fiable, identidad comprometida

Un sistema registra 100% de las órdenes, pero una cuenta de mantenimiento compartida puede modificar consignas. El registro prueba que una credencial actuó, no qué persona actuó ni si tenía autoridad. Una respuesta correcta debe separar trazabilidad, autenticación, atribución, autorización, integridad de registro y safety; proponer identidad individual, autorización por acción, protección de claves, segregación y límites locales independientes.

### Variante B — Dos regiones y un único proveedor de identidad

La organización afirma 99,99% por región. Ambas regiones dependen del mismo IdP y del mismo KMS. La independencia del cálculo no está demostrada. Se debe modelar el plano compartido como causa común, medir disponibilidad del servicio completo, diseñar acceso de emergencia controlado y evaluar el riesgo de que una contingencia de identidad degrade seguridad o continuidad.

### Variante C — Cifrado y retención indefinida

Una plataforma cifra todos los datos, conserva telemetría indefinidamente y permite inferir rutinas de personas. El cifrado protege ciertos escenarios de acceso no autorizado, pero no justifica finalidad, minimización, retención, inferencias ni uso secundario. La respuesta debe diseñar ciclo de vida de datos, controles de propósito, acceso, retención/eliminación, transparencia y evaluación de impacto.

### Variante D — Restauración rápida, estado no confiable

El servicio se restaura en 12 minutos, pero usa un backup previo a la revocación de credenciales y no verifica integridad de configuración. El RTO se cumple; la recuperación segura no. Deben definirse RTO y RPO junto con criterios de confianza, integridad, revocación, reconciliación y autorización de retorno a servicio.

**Rúbrica por variante (0–4):**
- 0: no identifica la propiedad o propone acción peligrosa.
- 1: enumera controles sin causalidad.
- 2: resuelve caso común, omite dependencias o trade-offs.
- 3: modela causalidad, límites, alternativas, evidencia y riesgo residual.
- 4: además justifica supuestos, incertidumbre, sensibilidad y límites de generalización con fuentes trazables.

Una evaluación autogenerada no es una evaluación independiente. El banco debe ser administrado a ciegas por un evaluador distinto del autor para aportar evidencia de competencia.

## 7. Diseño de investigación: disponibilidad aparente frente a recuperación confiable

**Pregunta:** ¿qué factores explican la diferencia entre recuperar el servicio y recuperar un estado confiable después de una interrupción que compromete identidad o configuración?

**Hipótesis de trabajo:** los planes que miden únicamente tiempo de restauración pueden declarar éxito mientras persisten condiciones de integridad, identidad o configuración que impiden reanudar de forma segura.

**Diseño propuesto:** experimento factorial en entorno simulado, con escenarios sintéticos de fallo de IdP, KMS, configuración y corrupción de backup. Variables independientes: estrategia de recuperación y controles de verificación. Variables dependientes: tiempo hasta servicio disponible, tiempo hasta estado confiable, cambios no autorizados aceptados, pérdida de datos y porcentaje de evidencias completas. Controlar tamaño del sistema, carga, dependencias y perfil de fallo. Separar escenarios de desarrollo y evaluación.

**Amenazas a validez:** simulación no representativa, selección de escenarios, dependencia entre fallos, sesgo de implementación, tamaño muestral insuficiente y métricas que premien velocidad a costa de safety. No se formula conclusión empírica hasta ejecutar, analizar incertidumbre y publicar datos/protocolo.

## 8. Fuentes y estado de revisión aplicado

- NIST SP 800-160 Vol. 1 Rev. 1, *Engineering Trustworthy Secure Systems*, publicación final 2022-11-16. La ficha oficial y el resumen se consultaron para confirmar versión vigente, alcance de ingeniería de sistemas seguros y carácter de propiedad emergente; no se declara lectura integral del PDF: https://doi.org/10.6028/NIST.SP.800-160v1r1
- NIST SP 800-160 Vol. 2 Rev. 1, *Developing Cyber-Resilient Systems: A Systems Security Engineering Approach*, final 2021-12-09. La página oficial confirma estado y relación con ingeniería de resiliencia; lectura integral pendiente: https://csrc.nist.gov/projects/systems-security-engineering-project/publications
- NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0*, 2024-02-26. Se consultó la ficha oficial y el resumen para delimitar que CSF expresa resultados de alto nivel y no prescribe por sí solo cómo lograrlos; lectura integral pendiente: https://doi.org/10.6028/NIST.CSWP.29
- NIST CSWP 40 IPD, *NIST Privacy Framework 1.1*, 2025-04-14. Borrador público inicial; revisión selectiva registrada en el documento principal y source registry. No tratar como versión final: https://doi.org/10.6028/NIST.CSWP.40.ipd

**Límite de evidencia:** esta profundización es síntesis técnica interna con ejemplos hipotéticos y fuentes oficiales identificadas. No se ha completado lectura integral de las publicaciones, no se han revisado normas sectoriales aplicables al caso, no hay validación legal colombiana, no se ha ejecutado el experimento y no existe revisión disciplinar independiente. Por tanto, no cierra NC-FND-01.01-01, -02, -03 ni -04 y no eleva T0/O0.

## 9. Checklist de revisión para el siguiente ciclo

- [ ] Contrastar fórmulas y supuestos con bibliografía primaria de confiabilidad y análisis de sistemas.
- [ ] Incorporar métodos de safety sectoriales según dominio concreto y edición vigente.
- [ ] Revisar integralmente NIST SP 800-160 Vol. 1 Rev. 1 y Vol. 2 Rev. 1.
- [ ] Revisar requisitos legales colombianos pertinentes con fuentes oficiales y asesoría competente; no extrapolar una norma transversal a todos los sectores.
- [ ] Administrar variantes A–D a un evaluador ciego y conservar respuestas anonimizadas, rúbrica y dictamen.
- [ ] Someter arquitectura y modelos causales a revisión independiente de especialistas de proceso, safety, seguridad y privacidad.
- [ ] Actualizar matriz solo con evidencia de cierre verificable.
