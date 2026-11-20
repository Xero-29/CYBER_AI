# Compendio técnico: PKI, certificados y HSM

ID: `pki_hsm` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de PKI, certificados y HSM; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Este documento transforma el currículo en una ruta de trabajo técnico y experimental; no certifica cobertura exhaustiva ni lectura integral de fuentes. Usar solo activos propios/autorizados, datos sintéticos y laboratorios aislados. Para entornos críticos/físicos, simular y preservar seguridad funcional y continuidad.

## Desarrollo por subtema
### 1. X.509 y cadena de confianza

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

### 2. CA y políticas CP/CPS

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

### 3. OCSP, CRL y CT

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

### 4. HSM y ceremonia de claves

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

### 5. mTLS y code signing

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

### 6. rotación y expiración

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

### 7. compromiso de CA

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas y fallos:** identificar abuso, debilidades, errores de configuración, fallos operativos y precondiciones; separar hipótesis de observaciones.
- **Controles:** asociar prevención, detección, respuesta y recuperación con amenazas; indicar cobertura, riesgo residual y efectos secundarios.
- **Verificación:** diseñar pruebas positivas, negativas, límites y regresión con entradas sintéticas, resultados esperados, evidencia y criterio de parada.
- **Análisis crítico:** comparar enfoques, revisar desacuerdos, sesgos, incertidumbre y límites de generalización.
- **Entregable:** explicación técnica original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento y limitaciones.

## Laboratorio
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Seguridad: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Caso | Evidencia |
|---|---|---|
| pki_hsm-LAB-01 | Baseline | Configuración, versiones, hashes y salida |
| pki_hsm-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs y resultado |
| pki_hsm-LAB-03 | Detección/diagnóstico | Señal, cobertura, precisión y límites |
| pki_hsm-LAB-04 | Mitigación y retest | Diff, antes/después, rollback |

Diseño definido; ejecución pendiente.

## Métricas
Seleccionar según la pregunta: cobertura, eficacia, falsos positivos/negativos, latencia, disponibilidad, impacto colateral, tiempo de recuperación y repetibilidad. Registrar muestra, baseline, unidad de análisis, versiones, repeticiones e incertidumbre.

## Investigación bibliográfica
- Registrar bases, cadenas de búsqueda, fecha, idioma y criterios de inclusión/exclusión.
- Priorizar estándares, especificaciones, documentación primaria y literatura revisada por pares.
- Marcar texto completo revisado solo tras inspección real.
- Extraer método, muestra, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y distinguir evidencia primaria, secundaria, inferencia e hipótesis.
- Registrar edición, licencia, URL canónica, fecha y SHA-256 cuando el archivo pueda archivarse legalmente.

## Preguntas de investigación
1. ¿Qué medidas producen mejora cuantificable frente a un baseline?
2. ¿Qué variables explican divergencias entre fuentes y resultados reproducidos?
3. ¿Qué controles equilibran seguridad, privacidad, resiliencia, coste y operación?

Definir H0/H1, variables, población, comparadores, criterio de refutación, análisis, ética y limitaciones.

## Artefactos obligatorios
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos, datos, identidades, versiones y dependencias.
- [ ] Modelo de amenazas y abuso.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimiento reproducible con precondiciones, rollback y parada.
- [ ] Laboratorio y casos con resultados medidos.
- [ ] Caso práctico con hallazgo, impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencias, ediciones, fechas y hashes.
- [ ] Incertidumbre, sesgos y amenazas a validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No acredita profundidad ni M3/M4/M5. Para avanzar: leer fuentes completas, producir artefactos específicos, ejecutar laboratorios y registrar evidencia auditable.


## Profundización técnica específica: PKI y HSM

### Arquitectura PKI
Modelar raíz offline, CAs intermedias, RA, repositorios, OCSP/CRL, CT, políticas, perfiles, relying parties y automatización ACME. Definir CP/CPS, identidad, validación, emisión, renovación, revocación, expiración y trust anchors. Separar emisión de autorización de uso.

### Certificados y validación
Revisar SAN, EKU, key usage, basic constraints, path building, name constraints, policy OIDs, algoritmos, validity periods, revocation checking y hostname. Un certificado válido no implica identidad autorizada. Controlar certificados wildcard, misissuance, subCA, certificados huérfanos y private key reuse.

### HSM y custodia
Evaluar FIPS level/validation scope, tamper resistance, partitions, roles, quorum, audit logs, backup, HA, firmware, remote admin y key export policy. Certificación aplica a módulo/configuración/operación definidos, no a todo el sistema. Definir ceremonias de claves, dual control, split knowledge y recuperación.

### Automatización y ciclo de vida
Inventariar certificados, owners, SAN, issuer, key type, expiry, usage, environment y rotation. Automatizar emisión/renovación sin exponer private keys. Alertar expiración, CA compromise, anomalías de emisión y uso. Diseñar revocación efectiva en clientes y servicios.

### Laboratorios
Construir CA de laboratorio, emitir/revocar certificados, probar path validation, expiración, hostname mismatch y rotación de HSM simulado. Medir tiempo de propagación, cobertura y fallos de cliente. No usar claves privadas reales.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.