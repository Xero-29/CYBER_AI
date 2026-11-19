# Compendio técnico: IoT y hardware

ID: `iot_hardware` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de IoT y hardware; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El compendio estructura el desarrollo; no declara revisión sistemática ni lectura completa de fuentes. Operar solo sobre activos propios/autorizados, en laboratorio aislado y con datos sintéticos. En hardware y sistemas físicos, usar simulación/banco controlado, minimizar energía/riesgo y priorizar seguridad funcional.

## Desarrollo por subtema
### 1. MCU/SoC y buses

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. UART, SPI, I2C, JTAG y SWD

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. firmware, bootloader y secure boot

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. OTA y rollback protection

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. radio, sensores y gateways

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. debug ports y secretos

- **Modelo:** describir arquitectura, componentes, estados, interfaces, identidades, datos, dependencias y límites de confianza.
- **Amenazas:** estudiar abuso, fallos de diseño/implementación, configuraciones, cadena de suministro y riesgos operativos relevantes; anotar precondiciones.
- **Controles:** asignar medidas preventivas, detectivas, de respuesta y recuperación; explicar cobertura y riesgo residual.
- **Validación:** casos positivos, negativos, de borde y regresión; entradas sintéticas, resultado esperado, telemetría, evidencia y regla de parada.
- **Análisis crítico:** comparar alternativas, explicitar supuestos, desacuerdos, sesgos y límites de generalización.
- **Entregable:** análisis técnico original, modelo/diagrama, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. ciclo de vida y laboratorio

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
| iot_hardware-LAB-01 | Baseline | Versiones, configuración, hash y salida |
| iot_hardware-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs y resultado |
| iot_hardware-LAB-03 | Detección/diagnóstico | Señal, regla, cobertura y límites |
| iot_hardware-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después, rollback |

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


## Profundización técnica específica: IoT y seguridad de hardware

### Arquitectura de dispositivo
Inventariar MCU/SoC, boot ROM, bootloader, firmware, periféricos, buses, sensores, actuadores, radio, debug ports, almacenamiento y servicios cloud. Definir trust boundaries entre hardware, firmware, aplicación, gateway y backend. Analizar amenazas de acceso físico, cadena de suministro, actualización maliciosa, clonación, extracción de secretos y manipulación de sensores.

### Root of trust y secure boot
Evaluar immutable root of trust, secure/measured boot, verificación de firmas, anti-rollback, protección de claves, debug lifecycle y recuperación. Secure boot demuestra cadena de autorización, no ausencia de vulnerabilidades. El modo de producción debe bloquear interfaces de debug según amenaza y permitir recuperación autenticada. Proteger claves únicas por dispositivo y evitar secretos globales compartidos.

### Firmware y actualización OTA
Diseñar manifest firmado, verificación de integridad/autenticidad, versionado, rollback policy, A/B partitions, recuperación ante fallo y rotación de claves. Validar compatibilidad, atomicidad, supply chain, SBOM, reproducibilidad y soporte de versiones. OTA debe tolerar pérdida de energía/conectividad y no degradar seguridad por rollback no autorizado.

### Interfaces y buses
Revisar UART, JTAG, SWD, SPI, I2C, CAN, USB, Ethernet, BLE, Wi-Fi, Zigbee/Thread y protocolos industriales. Evaluar autenticación, cifrado, replay, spoofing, fuzzing de parsers y control de acceso físico. Las pruebas de fault injection, side-channel o glitching requieren equipo y dispositivos propios, límites eléctricos y seguridad funcional.

### Identidad y privacidad
Usar identidad individual, certificados por dispositivo, provisioning seguro, rotación/revocación y attestation cuando aplique. Analizar onboarding, ownership transfer, factory reset, pérdida/robo, telemetry y exposición de datos. Un reset debe borrar secretos según modelo y no permitir re-enrolamiento fraudulento.

### Laboratorios
- Firmware de demostración con secure boot/anti-rollback simulado.
- Análisis estático de imagen firmware y extracción de SBOM.
- Fuzzing offline de parser de protocolo sintético.
- Validación de provisioning/certificados de dispositivos ficticios.
No aplicar pruebas eléctricas destructivas en equipos operativos o infraestructura crítica.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.