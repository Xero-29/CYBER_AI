# FND-01.01 — Soluciones desarrolladas para las cuatro capacidades V1

**Unidad:** seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia.  
**Estado:** soluciones modelo internas para entrenamiento y evaluación; no son respuestas de un candidato ni una validación independiente. **Madurez:** T0/O0.

## 1. Capacidad de enseñar — secuencia didáctica completa

### 1.1 Resultados observables

Al finalizar, el aprendiz debe poder:
1. distinguir seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia sin tratarlas como sinónimos;
2. formular una propiedad con sujeto, función, contexto, condición, horizonte y criterio;
3. identificar una causa común que invalida una afirmación de redundancia;
4. convertir un escenario en requisitos verificables y explicar qué evidencia falta;
5. justificar por qué una restauración rápida no demuestra un estado confiable.

### 1.2 Progresión de enseñanza

**Etapa 1 — empezar por el resultado, no por el control.** Presentar una planta que sigue funcionando, pero aplica una consigna manipulada. Preguntar: ¿está disponible? Sí, puede responder. ¿Es segura? No se sabe; puede ser peligrosa. ¿Es íntegra? La consigna puede no serlo. ¿Es confiable? No si incumple la función especificada. ¿Es resiliente? Solo si mantiene funciones esenciales y recupera un estado confiable. La primera lección es que una única métrica no representa todas las propiedades.

**Etapa 2 — definir el objeto.** Identificar sistema de interés, función, activos, personas, misión, fronteras y horizonte. Evitar «la plataforma es segura». Sustituirlo por afirmaciones acotadas, como «las órdenes de cambio de consigna se aceptan únicamente si la identidad, autorización, vigencia, integridad y límites locales se verifican».

**Etapa 3 — separar propiedades.** Usar la tabla de la unidad y pedir ejemplos que satisfagan una propiedad mientras fallan en otra. Ejemplo: servicio con 99,99% de uptime pero que registra identificadores personales innecesarios; disponible no significa privado. Backup restaurado en cinco minutos con credenciales revocadas sin validar; disponible no significa confiable.

**Etapa 4 — introducir causalidad y dependencias.** Dibujar sensor → controlador → actuador → proceso, y el plano remoto de identidad/administración. Marcar límites de confianza y dependencias comunes. Mostrar que dos regiones con el mismo IdP no son dos dominios de fallo independientes.

**Etapa 5 — derivar requisitos.** Para cada propiedad, convertir el objetivo en condición verificable. No comenzar por «instalar MFA» o «duplicar servidores». Comenzar por el comportamiento que se exige y las consecuencias que deben evitarse.

**Etapa 6 — enseñar evidencia.** Diferenciar análisis, inspección, demostración, prueba y validación. Un requisito escrito y una prueba diseñada no acreditan que el sistema real lo cumpla.

### 1.3 Concepciones erróneas y corrección

| Error | Por qué falla | Pregunta correctiva |
|---|---|---|
| «Cifrado = privacidad» | No resuelve finalidad, minimización, retención, inferencias ni uso secundario | ¿Qué problema para una persona evita el cifrado y cuáles deja intactos? |
| «Redundancia = resiliencia» | Puede haber causas comunes, fallo de conmutación o estado replicado comprometido | ¿Qué recursos, credenciales, firmware y plano de control comparten los nodos? |
| «Fail-closed siempre es seguro» | El cierre puede provocar pérdida de una función física esencial | ¿Qué peligro produce cada estado ante cada pérdida de dependencia? |
| «Uptime alto = confiabilidad» | Puede medir proceso activo, no función correcta | ¿Qué función, población, ventana y degradación mide el SLI? |
| «Restaurado = recuperado» | Un backup puede contener estado corrupto, secreto antiguo o configuración inválida | ¿Qué prueba autoriza volver a confiar en el sistema? |

### 1.4 Ejercicio graduado y solución

**Nivel básico:** un servicio está disponible pero expone datos de operadores. Clasificar propiedades.  
**Solución:** disponibilidad puede estar satisfecha en la ventana medida; privacidad está afectada si la exposición crea un problema para personas; confidencialidad puede estar afectada si el acceso fue no autorizado. No se concluye que safety o confiabilidad hayan fallado sin analizar sus funciones y consecuencias.

**Nivel intermedio:** dos regiones tienen réplicas, pero comparten IdP.  
**Solución:** la disponibilidad compuesta no puede calcularse como independiente sin modelar el IdP común; este constituye un posible punto de fallo común. Debe calcularse disponibilidad de la función completa y analizar el modo de acceso degradado, sin sacrificar autorización ni crear credenciales maestras permanentes.

**Nivel avanzado:** después de una intrusión se restaura un backup en 10 minutos, pero no se verifica configuración ni revocación.  
**Solución:** el RTO técnico puede haberse cumplido, pero no hay evidencia de estado confiable. Definir un estado de cuarentena/reanudación controlada; validar integridad, identidad, claves, configuración, datos y sensores antes de autorizar servicio normal.

## 2. Capacidad de explicar — reconstrucción de mecanismo

### 2.1 Modelo funcional

Un sistema hipotético de control de proceso contiene:
- sensor: convierte una magnitud física en una señal;
- controlador: estima estado, compara con una referencia y decide;
- actuador: ejecuta la orden física;
- proceso: responde con dinámica y perturbaciones;
- operador: supervisa y puede solicitar cambios;
- pasarela: comunica el plano remoto;
- identidad/autorización: determina quién puede realizar qué acción;
- registros: conservan eventos necesarios para control, auditoría y diagnóstico.

El comportamiento depende de la composición. La calidad de cada elemento no garantiza la propiedad emergente del conjunto: sensor correcto no evita una orden manipulada; controlador robusto no evita un actuador atascado; autenticación fuerte no evita que una orden autorizada sea peligrosa para el proceso.

### 2.2 Flujo de una orden remota

1. El operador inicia una sesión con identidad individual.
2. El sistema verifica autenticación y contexto de sesión.
3. La solicitud se asocia a una acción concreta, no a un permiso global genérico.
4. El motor de autorización comprueba rol, atributos, contexto, separación de funciones y vigencia.
5. La pasarela valida integridad, secuencia, frescura y formato de la orden.
6. El controlador local comprueba estado, límites físicos y reglas de seguridad independientes del plano remoto.
7. Si las condiciones se cumplen, ejecuta o rechaza la orden y registra resultado.
8. El registro se protege contra alteración y se minimizan datos personales.
9. Ante pérdida de identidad o comunicación, la máquina de estados aplica el modo degradado especificado; no se permite que una última orden remota quede válida indefinidamente sin criterio.

### 2.3 Por qué las propiedades no se heredan de un componente

Sea una función de sistema (F = g(x_1, x_2, ldots, x_n, c)), donde (x_i) son componentes y (c) representa contexto, entorno e interacciones. Una afirmación sobre cada (x_i) no demuestra automáticamente una afirmación sobre (F): la composición introduce interfaces, estados, temporización, dependencia, errores y comportamientos emergentes.

Ejemplo: sensor A y sensor B son individualmente exactos, pero comparten alimentación y entorno. Una perturbación común puede degradarlos a la vez. El supuesto de independencia necesario para combinar sus probabilidades no está justificado. La solución es identificar causa común, definir diversidad/independencia verificable y conservar límites/diagnósticos que no dependan de ambos sensores de la misma forma.

### 2.4 Contraejemplo: el cierre no es universalmente seguro

En un servicio de archivos, negar acceso ante fallo del autorizador puede proteger confidencialidad. En un control físico, detener inmediatamente una función puede generar un peligro. No se deduce que se deba permitir acceso; se deriva que el estado de fallo debe diseñarse por función, peligro, contexto y autoridad. Las opciones pueden incluir control local limitado, intervención humana, transición gradual o parada segura, siempre definidas por análisis competente.

## 3. Capacidad de analizar — escenario nuevo resuelto

### 3.1 Escenario

Un centro de tratamiento de agua pierde conectividad con su servicio central de identidad durante una contingencia regional. El controlador local sigue operando. Un sensor muestra una desviación respecto del segundo sensor. Un técnico propone desactivar autenticación remota para recuperar acceso y la dirección propone conmutar a la segunda región. Ambas regiones comparten el mismo proveedor de identidad y el mismo plano de administración. Los registros identifican a operadores y se conservan sin plazo definido.

### 3.2 Delimitación

No se conoce el proceso químico, el sector exacto, la criticidad, los rangos ni el diseño de seguridad funcional. No se puede recomendar una consigna ni decidir qué sensor es correcto. Se requiere detener toda modificación remota que no tenga autoridad y evidencia suficiente; mantener el modo local definido por ingeniería de proceso, si existe y ha sido validado.

### 3.3 Análisis causal

- **Disponibilidad:** pérdida de IdP puede impedir administración remota aunque el controlador siga activo. La región secundaria no es independiente por compartir IdP.
- **Seguridad:** desactivar autenticación elimina una barrera de identidad y puede habilitar órdenes no atribuibles. Un acceso de emergencia requiere identidad individual, alcance mínimo, tiempo limitado, aprobación y registro.
- **Integridad:** divergencia de sensores exige diagnóstico de plausibilidad, calibración, historial y causa; no elegir uno por conveniencia.
- **Safety:** si la discrepancia impide determinar el estado físico con confianza, la función de control debe seguir el procedimiento de seguridad de proceso aprobado. No inventar el estado seguro.
- **Privacidad:** bitácoras identificables y retención indefinida requieren finalidad, necesidad, acceso, retención y eliminación justificados.
- **Resiliencia:** se debe mantener función esencial y recuperar administración confiable, no solo cambiar de región.

### 3.4 Alternativas y trade-offs

| Alternativa | Beneficio | Riesgo/condición |
|---|---|---|
| Desactivar autenticación remota | Recupera conectividad administrativa rápidamente | Riesgo crítico de acceso no autorizado; rechazar como solución genérica |
| Conmutar región | Puede recuperar servicios dependientes | No elimina fallo común de IdP; requiere prueba de independencia real |
| Operación local degradada | Reduce dependencia del plano remoto | Solo aceptable si el modo y sus límites fueron analizados y validados por proceso |
| Acceso de emergencia temporal | Permite una acción controlada | Requiere identidad individual, autorización acotada, aprobación, expiración, registro y revisión posterior |
| Detener o limitar función | Puede reducir exposición a un peligro | Puede crear un peligro físico/servicio; decisión de autoridad de proceso |

### 3.5 Decisión provisional defendible

No desactivar autenticación de forma global. No afirmar que la segunda región resuelve la contingencia. Preservar el control local únicamente dentro de su modo degradado previamente aprobado; escalar la discrepancia de sensores según procedimiento de proceso; suspender cambios remotos no esenciales; activar un mecanismo de emergencia documentado si existe y cumple requisitos. Esta decisión es provisional y no sustituye autoridad de operación.

### 3.6 Evidencia que cambiaría la decisión

- análisis de peligros y definición del modo local degradado;
- arquitectura de identidad y dependencia del plano de administración;
- independencia real de la región secundaria;
- diagnóstico/calibración de sensores;
- matriz de permisos y procedimientos de emergencia;
- finalidad y retención de registros;
- resultados de pruebas de banco e integración en entorno autorizado.

## 4. Capacidad de diseñar — solución de referencia y argumento de assurance

### 4.1 Requisitos de diseño

| ID | Requisito | Verificación estática | Prueba futura |
|---|---|---|---|
| D-01 | Límites locales de proceso no anulables por la pasarela remota | Revisión de arquitectura, política y modelo de estados | Pruebas de límites y órdenes inválidas en banco |
| D-02 | Cada orden remota se vincula a identidad individual, acción, vigencia y autorización | Análisis de flujo y matriz de permisos | Pruebas positivas/negativas y revocación |
| D-03 | La pérdida del IdP no provoca aceptación indefinida de órdenes antiguas | Revisión de máquina de estados y secuencia | Ensayo de expiración, revocación y pérdida de servicio |
| D-04 | La discrepancia de sensores activa diagnóstico y procedimiento definido por proceso | Revisión de requisitos y árbol de fallos | Ensayo controlado con señales sintéticas |
| D-05 | Telemetría minimiza datos personales y define retención por finalidad | Inspección de esquema y flujo de datos | Pruebas de datos sintéticos y eliminación |
| D-06 | Recuperación verifica integridad de firmware/configuración/identidad antes de retorno a servicio | Revisión de secuencia y criterios | Restauración aislada, verificación y autorización de retorno |

### 4.2 Arquitectura

- Separar red OT, DMZ y servicios empresariales; limitar flujos explícitos.
- Mantener lógica crítica de límites y estados localmente, con autoridad independiente del plano remoto.
- Usar autenticación individual y autorización por acción, con expiración, revocación y separación de funciones.
- Hacer que la pasarela no tenga autoridad para anular interlocks o límites físicos.
- Firmar/verificar firmware y configuración; conservar versión aprobada y procedimiento de recuperación.
- Diseñar logs con integridad, minimización y retención; separar identificadores de personas cuando no sean necesarios.
- Crear modos normal, degradado, mantenimiento, recuperación y retorno a servicio como estados explícitos y verificables.

### 4.3 Plan de verificación y aceptación

**En frío/estático:** revisar requisitos, trazabilidad, DFD, modelo de amenazas/peligros, máquina de estados, reglas de autorización, ecuaciones de disponibilidad y supuestos, esquema de telemetría, rollback y argumento de assurance.

**En banco controlado:** introducir señales sintéticas, pérdida de conectividad, expiración/revocación, configuración alterada y fallos de conmutación; recoger logs, versiones y resultados. No probar sobre planta productiva.

**En integración:** verificar IdP/KMS/registro/OT en entorno aislado; probar fallos de contrato, recuperación, segregación y degradación.

**En operación representativa:** requiere aprobación de responsables, ventana, plan de parada, observabilidad, rollback y límites de seguridad. No se deduce de la verificación estática.

### 4.4 Argumento de assurance

- **Claim C0:** el diseño propuesto limita cambios remotos no autorizados y preserva el control local dentro de los límites aprobados.
- **Subclaim C1:** la autoridad de la pasarela no puede anular límites locales.
- **Evidencia E1:** arquitectura, matriz de permisos, modelo de estados y análisis de interfaces.
- **Subclaim C2:** los cambios remotos tienen identidad, autorización, frescura y trazabilidad.
- **Evidencia E2:** diseño de flujo, política de autorización y esquema de logs; la prueba real queda pendiente.
- **Subclaim C3:** pérdida de dependencias y recuperación no producen una transición no controlada.
- **Evidencia E3:** análisis de estados, FMEA/árbol de fallos, protocolo de ensayo y criterios de retorno.
- **Supuestos:** límites de proceso proporcionados por ingeniería competente; entorno y componentes corresponden a la arquitectura; el modo degradado está autorizado.
- **Derrotadores:** sensor comúnmente defectuoso, firmware comprometido, bypass físico, clave de firma comprometida, error sistemático de configuración o dependencia omitida.
- **Conclusión permitida hoy:** existe una solución conceptual verificable. No hay evidencia de que el sistema implementado satisfaga los claims.

## 5. Matriz de autoauditoría de estas soluciones

| Capacidad | Evidencia nueva | Qué demuestra | Qué no demuestra |
|---|---|---|---|
| Enseñar | Progresión, resultados, errores y ejercicios resueltos | Secuencia didáctica y explicación modelo | Aprendizaje de un evaluado |
| Explicar | Flujo de orden, composición y contraejemplo | Reconstrucción causal del sistema hipotético | Corrección de una implementación real |
| Analizar | Escenario no trivial con alternativas y condiciones | Razonamiento sobre propiedades, dependencias y riesgo | Revisión independiente ni validez sectorial |
| Diseñar | Requisitos, arquitectura, pruebas y assurance case | Diseño conceptual y trazabilidad | Integración, operación o eficacia observada |

**Regla de aceptación:** estas soluciones elevan la calidad del material de entrenamiento, pero no cambian la matriz a `passed`. La prueba en frío debe administrarse a un candidato sin acceso a las soluciones; el evaluador debe puntuar y registrar errores. La revisión independiente sigue siendo requisito para T4. No se asigna nivel de competencia a ninguna persona ni modelo con este documento.
