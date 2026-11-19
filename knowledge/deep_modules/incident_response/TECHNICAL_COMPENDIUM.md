# Compendio técnico: Respuesta a incidentes

ID: `incident_response` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Respuesta a incidentes; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. Preparación, gobierno, roles y severidad

La respuesta a incidentes es una capacidad organizacional continua, no una secuencia improvisada de herramientas. Definir autoridad para declarar incidente, comandante, responsable técnico, comunicaciones, legal/privacidad, negocio, proveedor y observador de evidencias. Mantener matriz RACI, contactos alternos, autoridad de aislamiento y criterios de escalamiento. Separar severidad técnica, impacto de negocio y urgencia.

Preparación incluye inventario de activos, dependencias, backups, telemetría, playbooks, acceso de emergencia, acuerdos con proveedores, retención y ejercicios. Los playbooks deben indicar precondiciones, decisión, evidencia, rollback, responsable y condición de salida. Preparar acceso fuera de banda y copias offline de procedimientos.

### 2. Detección, triage y validación

Triage determina si una alerta es evento benigno, sospecha o incidente confirmado. Validar calidad de fuente, identidad/activo, ventana temporal, baseline, corroboración independiente y posible duplicado. Enriquecer con criticidad del activo, exposición, identidad, vulnerabilidad, telemetría y alcance. No cerrar por ausencia de alertas si la fuente está caída o el endpoint dejó de reportar.

Registrar hipótesis, evidencia a favor/en contra, confianza, impacto potencial y siguiente acción reversible. Preservar alertas originales y query usada; la normalización puede perder campos. Establecer reloj común y correlación sin asumir sincronización perfecta.

### 3. Contención y preservación

Contención busca limitar daño sin destruir evidencia ni interrumpir procesos críticos innecesariamente. Opciones: aislamiento EDR, segmentación, bloqueo de cuenta, revocación de tokens, bloqueo de IOC, suspensión de workload o control de egress. Elegir según alcance, persistencia, impacto y riesgo de propagación. Documentar quién autorizó, qué cambió, cuándo y cómo revertir.

Preservar logs, memoria, snapshots, PCAP, identidad, nube y artefactos de endpoint según volatilidad y alcance. Antes de apagar, evaluar memoria y cifrado; antes de bloquear una cuenta, considerar dependencias de servicio. No realizar acciones destructivas automáticas sin aprobación y plan de rollback.

### 4. Erradicación, recuperación y validación

Erradicación elimina causa y persistencia, no solo indicador visible. Determinar vector inicial, vulnerabilidad, credencial, configuración o tercero comprometido; corregirlo antes de restaurar. Reconstruir desde imágenes confiables cuando la integridad no pueda demostrarse. Rotar credenciales y claves con orden de dependencia, revisar tokens y certificados, parchear y validar backups.

Recuperar por etapas con controles reforzados, observación de señales de recurrencia, pruebas de negocio y criterios de rollback. Restaurar un backup no prueba que esté limpio ni que el vector haya desaparecido. Mantener monitoreo elevado durante ventana definida.

### 5. Ransomware, BEC, cloud y supply chain

Ransomware: identificar cifrado activo, exfiltración, alcance de identidad, backups y movimiento lateral; coordinar continuidad, legal y privacidad. No conectar backups al dominio comprometido. BEC: preservar correo y headers, revocar sesiones, investigar reglas de forwarding, OAuth grants y pagos; validar cambios bancarios por canal independiente. Cloud: preservar audit logs, IAM, snapshots, keys, control plane y API activity; evitar destruir recursos antes de capturar metadata. Supply chain: identificar artefacto, versión, build provenance, dependencias, firma y consumidores.

### 6. Comunicación, regulación y coordinación externa

Definir mensajes confirmados, desconocidos y próximos hitos. Evitar atribución prematura y especulación pública. Notificaciones regulatorias dependen de jurisdicción, sector, datos y contratos; escalar a legal/privacidad temprano y registrar plazos. Coordinar CERT, aseguradora, proveedor cloud, law enforcement y clientes conforme a autoridad y política. Mantener un único registro de decisiones.

### 7. Postmortem, métricas y mejora

Postmortem sin culpabilización pero con responsables de acciones. Reconstruir timeline, causa raíz, factores contribuyentes, controles que fallaron, detecciones ausentes, decisiones, impacto, tiempo y evidencia perdida. Acciones deben tener propietario, fecha, criterio verificable y test de cierre.

## Laboratorio reproducible

Ejercicios de mesa y simuladores inocuos en entorno aislado; no ejecutar ransomware ni provocar indisponibilidad real.

| ID | Experimento frío | Diseño y criterio de aceptación |
|---|---|---|
| ir-LAB-01 | Tabletop de incidente | Escenario sintético; roles, severidad, decisiones y escalamiento quedan registrados con tiempos |
| ir-LAB-02 | Triage con alertas | Dataset etiquetado; clasificar y justificar TP/FP/duplicados; medir precisión y tiempo |
| ir-LAB-03 | Contención reversible | Simular aislamiento y revocación en tenant demo; validar aprobación, rollback y evidencia |
| ir-LAB-04 | Preservación | Recoger logs/snapshot/PCAP sintéticos; cadena de custodia y hashes completos |
| ir-LAB-05 | Recuperación ransomware simulada | Restaurar snapshots de archivos fixture; validar backup limpio, RTO/RPO y detección de recurrencia |
| ir-LAB-06 | Incidente cloud | Eventos sintéticos de IAM/API; delimitar alcance y preservar IDs/request IDs |
| ir-LAB-07 | Postmortem | Informe con timeline, causa raíz, acciones medibles y revisión ciega |

## Métricas y evaluación

Medir MTTD, tiempo a triage, tiempo a contención, tiempo a recuperación, alcance afectado, pérdida de evidencia, porcentaje de acciones con rollback probado, cumplimiento de RTO/RPO y recurrencia. Definir inicio/fin de cada reloj y segmentar por severidad. No comparar equipos con definiciones distintas.

## Artefactos de aceptación

- Plan de respuesta y autoridad.
- Matriz de severidad y escalamiento.
- Playbooks con precondiciones, decisiones y rollback.
- Dataset de ejercicio con ground truth.
- Timeline y registro de decisiones.
- Evidencia preservada y controles de acceso.
- Informe postmortem y acciones verificables.

## Madurez

Contenido editorial específico incorporado; ejercicios diseñados, no ejecutados. No declarar preparación operacional ni validación científica sin simulacros medidos, revisión independiente y evidencia. M2 como máximo.

## Laboratorio reproducible
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Caso | Evidencia exigida |
|---|---|---|
| incident_response-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| incident_response-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| incident_response-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| incident_response-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

Diseño definido; ejecución pendiente.

## Métricas
Elegir métricas específicas: cobertura, tasa de detección, falsos positivos/negativos, latencia, disponibilidad, impacto colateral, tiempo de remediación y repetibilidad. Toda cifra exige unidad de análisis, muestra, baseline, versiones, repeticiones y método de análisis.

## Investigación bibliográfica
- Registrar bases, cadenas de búsqueda, fecha, idiomas y criterios de inclusión/exclusión.
- Priorizar normas, especificaciones, documentación primaria y literatura revisada por pares.
- Leer texto completo antes de usar `full_text_reviewed`.
- Extraer método, población, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y enfoques; separar evidencia, inferencia e hipótesis.
- Registrar edición, URL canónica, licencia, fecha y hash cuando el archivo pueda archivarse legalmente.

## Preguntas de investigación candidatas
1. ¿Qué controles reducen el riesgo de los escenarios priorizados frente a un baseline?
2. ¿Qué condiciones de versión/entorno explican diferencias entre resultados publicados y reproducidos?
3. ¿Qué combinación de señales y criterios mejora la detección sin impacto operacional inaceptable?

Cada estudio debe definir H0/H1, variables, muestra, comparadores, refutación, análisis, ética, seguridad y límites.

## Artefactos de aceptación
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos/datos/identidades/versiones.
- [ ] Modelo de amenazas y escenarios.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimientos con precondiciones, rollback y parada.
- [ ] Laboratorio y casos medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencias, edición, fecha y hashes.
- [ ] Incertidumbre, falsos positivos/negativos y validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No demuestra cobertura profunda ni M3/M4/M5. Próxima puerta: revisar fuentes completas, producir artefactos específicos, ejecutar pruebas y registrar evidencia.


## Profundización técnica específica: Respuesta a incidentes

### Preparación y gobierno operativo
Definir autoridad de activación, severidad, criterios de escalamiento, RACI, suplencias, canales primarios/alternos, contactos externos, asesoría legal y comunicación ejecutiva. Preparación incluye inventario, logging, sincronización temporal, backups probados, playbooks, acceso break-glass, acuerdos con proveedores y ejercicios. Separar incidente confirmado, evento, vulnerabilidad y crisis operacional. Mantener criterios de decisión por impacto en confidencialidad, integridad, disponibilidad, seguridad física, obligaciones regulatorias y continuidad.

### Detección, triage y clasificación
Normalizar alertas con entidad, tiempo, fuente, confianza, técnica, activo, identidad, exposición y contexto de negocio. Triage debe validar señal, descartar errores de telemetría, establecer alcance inicial y preservar evidencia. Asignar identificador único, cronología UTC, custodio y nivel de sensibilidad. Evitar cerrar como falso positivo sin evidencia. Correlacionar endpoint, identidad, red, cloud, aplicaciones, DNS, correo y terceros.

### Análisis y contención
Construir hipótesis competidoras y línea temporal; distinguir indicador, observación, inferencia y conclusión. Contención debe limitar propagación sin destruir evidencia ni interrumpir servicios críticos más allá de lo autorizado. Opciones incluyen revocar sesiones/tokens, aislar endpoint, bloquear indicadores, suspender cuentas, segmentar red o detener pipeline. Cada acción registra aprobador, alcance, hora, efecto esperado, riesgo colateral y rollback.

### Erradicación y recuperación
Eliminar persistencia y causa raíz, corregir configuración, rotar credenciales comprometidas y reconstruir desde fuentes confiables. Validar integridad de imágenes, backups y artefactos antes de restaurar. Recuperación gradual por criticidad, monitorización reforzada y criterios de salida. No confundir restauración de servicio con erradicación del adversario. Mantener evidencia y cadena de custodia durante el ciclo.

### Comunicación, regulación y terceros
Preparar mensajes para dirección, usuarios, clientes, reguladores, aseguradoras, proveedores y autoridades según jurisdicción/contratos. No divulgar hipótesis como hechos. Documentar reloj de notificación, asesoría jurídica y base de decisión. Coordinar con proveedores cloud/MSP para logs y preservación de datos, entendiendo límites de acceso y retención.

### Métricas y mejora
Medir MTTD, MTTA, tiempo a contención, tiempo de recuperación, recurrencia, cobertura de logs, porcentaje de playbooks ejercitados, integridad de evidencia, impacto y coste. Definir inicio/fin consistentemente; reportar medianas y percentiles, no promedios aislados. Postmortem sin culpa debe convertir causas sistémicas en acciones con dueño, plazo y prueba de eficacia.

### Ejercicios
- Tabletop de ransomware con decisiones de continuidad y comunicación.
- Simulación de compromiso de identidad cloud y revocación de sesiones.
- Replay de eventos sintéticos para validar triage y correlación.
- Recuperación de servicios desde backups aislados con verificación de integridad.
Registrar injects, decisiones, retrasos, fallos de comunicación, métricas y mejoras. Los ejercicios diseñados no equivalen a incidentes reales ni a eficacia demostrada.

## Estado de validación de la ampliación
Contenido técnico editorial añadido; fuentes completas, revisión independiente y laboratorios ejecutados permanecen pendientes. No elevar por redacción a M3/M4/M5.