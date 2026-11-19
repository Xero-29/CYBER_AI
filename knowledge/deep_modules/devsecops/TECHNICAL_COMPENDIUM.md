# Compendio técnico: DevSecOps y supply chain

ID: `devsecops` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de DevSecOps y supply chain; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El compendio estructura el desarrollo; no declara revisión sistemática ni lectura completa de fuentes. Operar solo sobre activos propios/autorizados, en laboratorio aislado y con datos sintéticos. En hardware y sistemas físicos, usar simulación/banco controlado, minimizar energía/riesgo y priorizar seguridad funcional.

## Desarrollo por subtema
### 1. SDLC y threat modeling

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. CI/CD, runners y secretos

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. SAST, SCA, DAST y gates

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. SBOM, provenance y SLSA

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. IaC y policy-as-code

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. artefactos y releases

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. supply chain response

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
| devsecops-LAB-01 | Baseline | Versiones, configuración, hash y salida |
| devsecops-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs y resultado |
| devsecops-LAB-03 | Detección/diagnóstico | Señal, regla, cobertura y límites |
| devsecops-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después, rollback |

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


## Profundización técnica específica: DevSecOps

### Pipeline y trust boundaries
Modelar repositorio, developer workstation, SCM, CI runners, artifact registry, signing service, deployment controller y runtime. Cada transición es una frontera de confianza. Proteger tokens, runners efímeros, branch protection, approvals, webhooks, caches, secrets y permisos de workflow. Evitar que código de PR no confiable acceda a secretos o credenciales de producción.

### SAST, SCA, DAST y secretos
Definir política por lenguaje y riesgo; ajustar reglas, baseline, suppressions con vencimiento y triage. SCA correlaciona dependencias directas/transitivas, licencias, reachability y exploitability. Secret scanning requiere revocación/rotación, no solo borrar del commit. DAST en entornos aislados con datos sintéticos y scope explícito.

### IaC y policy-as-code
Analizar Terraform, Kubernetes manifests, Helm, cloud templates y scripts. Validar exposición pública, IAM excesivo, cifrado, logging, redes, secretos y drift. Policy-as-code debe versionarse, probarse con casos permitidos/denegados y tener excepciones auditables. Separar plan y apply; proteger state y backend.

### Supply chain y procedencia
SBOM, provenance, build isolation, pinned dependencies, signature verification, reproducible builds y attestations. Proteger dependencias, actions/plugins, base images y package registries. SLSA levels y frameworks son modelos de garantías, no sustituyen evaluación de amenaza. Firmar artefacto y verificar firma en deployment, vinculando digest a build.

### Release y operación
Separar entornos, credenciales y aprobaciones; usar progressive delivery, canary, rollback y feature flags seguros. Monitorear runtime, configuración y drift; conectar hallazgos con tickets y retest. El objetivo no es maximizar cantidad de scanners, sino reducir riesgo con baja fricción y evidencia.

### Métricas y laboratorios
Medir tiempo de feedback, vulnerabilidades escapadas, tasa de falsos positivos, cobertura de repos, porcentaje de builds firmadas, provenance verificable y tiempo de remediación. Laboratorios: pipeline con secreto sintético, IaC insegura, dependencia vulnerable y verificación de firma. Documentar runners, versiones, reglas y outputs.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.