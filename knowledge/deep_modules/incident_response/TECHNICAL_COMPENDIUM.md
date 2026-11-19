# Compendio técnico: Respuesta a incidentes

ID: `incident_response` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Respuesta a incidentes; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema
### 1. preparación, roles y severidad

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. detección, triage y validación

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. contención y preservación

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. erradicación y recuperación

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. comunicaciones y notificación

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. tabletop y simulacros

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. lecciones aprendidas

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

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