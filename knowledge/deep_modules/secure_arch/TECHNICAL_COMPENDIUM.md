# Compendio técnico: Arquitectura segura

ID: `secure_arch` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Arquitectura segura; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El compendio estructura el desarrollo; no declara revisión sistemática ni lectura completa de fuentes. Operar solo sobre activos propios/autorizados, en laboratorio aislado y con datos sintéticos. En hardware y sistemas físicos, usar simulación/banco controlado, minimizar energía/riesgo y priorizar seguridad funcional.

## Desarrollo por subtema
### 1. requisitos y atributos de calidad

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. contexto y límites de confianza

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. STRIDE, attack trees y abuse cases

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. Zero Trust y defensa en profundidad

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. identidad, datos y secretos

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. resiliencia y observabilidad

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. revisión y ADR

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

## Laboratorio
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Seguridad: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Prueba | Evidencia |
|---|---|---|
| secure_arch-LAB-01 | Baseline | Versiones, configuración, hash y salida |
| secure_arch-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs y resultado |
| secure_arch-LAB-03 | Detección/diagnóstico | Señal, regla, cobertura y límites |
| secure_arch-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después, rollback |

Estos son diseños, no experimentos ejecutados.

## Métricas y método
Seleccionar según la pregunta: cobertura de activos/escenarios, tasa de éxito del control, falsos positivos/negativos, latencia, disponibilidad, impacto colateral, recuperación y repetibilidad. Declarar muestra, baseline, unidad de análisis, versiones, repeticiones y análisis estadístico; no extrapolar fuera del laboratorio.

## Revisión bibliográfica reproducible
- Registrar consultas, repositorios/bases, fecha, idioma y criterios de selección.
- Priorizar estándares, especificaciones, documentación primaria, advisories y papers revisados por pares.
- Leer texto completo antes de marcar `full_text_reviewed`.
- Extraer método, muestra, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar enfoques y resultados; distinguir evidencia primaria, secundaria, inferencia e hipótesis.
- Registrar edición, URL canónica, licencia, fecha y SHA-256 cuando sea legal archivar el documento.

## Preguntas candidatas
1. ¿Qué control ofrece la mayor reducción de riesgo medible respecto al baseline?
2. ¿Qué condiciones de entorno o versión explican divergencias de resultados?
3. ¿Qué señales y criterios mejoran detección/diagnóstico sin afectar indebidamente la operación?

Todo estudio debe definir H0/H1, variables, muestra, comparadores, criterio de refutación, análisis, riesgos éticos y límites.

## Artefactos de aceptación
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos, datos, identidades, versiones y dependencias.
- [ ] Modelo de amenazas.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimiento reproducible, precondiciones, rollback y parada.
- [ ] Laboratorio aislado y casos con resultados medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes con licencia, edición, fecha y hashes.
- [ ] Incertidumbre, falsos positivos/negativos y amenazas a validez.
- [ ] Revisión independiente/reproducción externa para M5.

## Madurez
M0/M1 estructural. Este documento no prueba profundidad cubierta ni madurez M3/M4/M5. Siguiente puerta: lectura crítica de fuentes completas, artefactos específicos, ejecución de laboratorio y evidencia verificable.


## Profundización técnica específica: Arquitectura segura

### Principios y límites de confianza
Definir dominios, actores, activos, flujos, límites, dependencias, invariantes y objetivos de seguridad. Aplicar least privilege, complete mediation, fail-safe defaults, separation of duties, defense in depth y secure by design. Documentar supuestos, riesgos residuales, decisiones y alternativas descartadas. Zero Trust exige decisiones explícitas por recurso/contexto, no solo segmentación.

### Modelado de amenazas
Usar STRIDE, attack trees, misuse cases, LINDDUN u otros métodos según objetivo. Identificar spoofing, tampering, repudiation, information disclosure, denial of service y elevation of privilege. Asociar amenazas a activos, precondiciones, controles, pruebas y evidencia. Revisar el modelo cuando cambien arquitectura, proveedor, datos o trust boundary.

### Arquitectura distribuida y cloud-native
Evaluar identidad de servicio, mTLS, service mesh, API gateway, event bus, queues, retries, circuit breakers, secrets, control plane y observabilidad. Fallos de red y consistencia generan ventanas de autorización; revisar cache invalidation, replay, idempotencia y mensajes duplicados. Seguridad debe mantenerse durante degradación y recuperación.

### Resiliencia y fallos
Modelar dependencias críticas, single points of failure, fail-open/fail-closed, graceful degradation, backups, restore, disaster recovery y aislamiento de incidentes. Definir RTO/RPO por servicio y probarlos. No diseñar seguridad que haga imposible recuperación ni disponibilidad que abra rutas inseguras.

### Revisión y aceptación
Architecture review debe incluir diagramas actualizados, threat model, requisitos, matriz de controles, análisis de privacidad, supply chain, operación, telemetría, coste y plan de pruebas. Registrar excepciones con dueño, vencimiento y compensating controls. La aceptación requiere evidencia técnica y operativa.

### Laboratorios
- Comparar dos diseños de autorización/segmentación con threat models.
- Simular caída de identidad, DNS o proveedor y medir comportamiento seguro.
- Evaluar arquitectura multi-tenant y rutas de datos.
- Revisar un cambio de arquitectura y actualizar trazabilidad.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.