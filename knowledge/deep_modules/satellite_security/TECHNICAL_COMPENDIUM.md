# Compendio técnico: Satélites y sistemas espaciales

ID: `satellite_security` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Satélites y sistemas espaciales; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Ruta de desarrollo técnico; no declara cobertura exhaustiva ni fuentes leídas íntegramente. Operar solo con autorización explícita, datos sintéticos y laboratorios aislados. En infraestructuras físicas o críticas, usar simulación/bancos de pruebas y no intervenir producción.

## Desarrollo por subtema
### 1. segmentos espacial y terrestre

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. TT&C y telemetría

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. RF y espectro

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. firmware y estaciones terrestres

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. resiliencia y anti-jamming

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. identidad y criptografía

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. simulación y coordinación

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

## Laboratorio
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Prueba | Evidencia |
|---|---|---|
| satellite_security-LAB-01 | Baseline | Versiones, configuración, hashes y salida |
| satellite_security-LAB-02 | Evento/fallo sintético | Entrada, precondiciones, logs y resultado |
| satellite_security-LAB-03 | Detección/diagnóstico | Señal, cobertura, precisión y límites |
| satellite_security-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después y retest |

Diseño propuesto; no ejecutado.

## Métricas
Definir métricas acordes al caso: cobertura, eficacia del control/detección, falsos positivos/negativos, latencia, disponibilidad, impacto, recuperación y repetibilidad. Publicar unidad de análisis, muestra, baseline, versiones, repeticiones e incertidumbre.

## Método de investigación
- Búsqueda reproducible: bases, consultas, fechas, idiomas e inclusión/exclusión.
- Fuentes: estándares, especificaciones, documentación primaria, advisories y artículos revisados por pares.
- Texto completo solo se marca revisado tras inspección real.
- Extraer método, población, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y separar evidencia, inferencia e hipótesis.
- Registrar versión, licencia, URL canónica, fecha y hash cuando sea legal archivar.

## Preguntas candidatas
1. ¿Qué controles mejoran la eficacia frente a un baseline y en qué condiciones?
2. ¿Qué factores explican divergencias entre el estado del arte y las pruebas reproducidas?
3. ¿Qué señales permiten detectar antes sin elevar falsos positivos o impacto operacional?

Cada estudio debe definir H0/H1, variables, muestra, comparadores, refutación, análisis, ética y limitaciones.

## Artefactos exigibles
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos, datos, identidades, versiones y dependencias.
- [ ] Modelo de amenazas.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimientos reproducibles con rollback y parada.
- [ ] Laboratorio y casos con resultados medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencia, edición, fecha y hashes.
- [ ] Incertidumbre, sesgos y amenazas a validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No prueba profundidad ni madurez M3/M4/M5. Avanzar exige lectura crítica, artefactos específicos, experimentos ejecutados y evidencia auditable.


## Profundización técnica específica: Seguridad satelital

### Segmentos y activos
Modelar segmento espacial, ground segment, user segment, TT&C, payload, gateways, estaciones, enlaces inter-satélite, proveedores, software de misión y supply chain. Identificar disponibilidad, safety, confidencialidad, integridad y restricciones de ventana orbital. La arquitectura depende de órbita, misión, operador y capacidades del enlace.

### Enlaces y protocolos
Evaluar RF, telemetría, telecommand, ranging, GNSS, enlaces ópticos y protocolos de misión. Amenazas incluyen jamming, spoofing, replay, command injection, key compromise y denial of service. Protección requiere autenticación de comandos, anti-replay, gestión de claves, control de acceso a estaciones y monitoreo de espectro.

### Segmento terrestre y cadena de mando
Ground systems suelen conectar redes corporativas, misión y proveedores. Segmentar, autenticar operadores, proteger estaciones, registrar comandos y aplicar doble aprobación para acciones críticas. Diseñar safe mode y recuperación bajo latencia, conectividad limitada y ventanas de contacto.

### Firmware y supply chain
Controlar firmware, FPGA bitstreams, boot chain, bibliotecas, toolchains, proveedores y actualizaciones. Firmar artefactos y validar antes de cargar; tener rollback seguro y control de configuración. Evaluar riesgo de componentes COTS y obsolescencia.

### Laboratorios
Simular telemetría/comandos y canal con retraso, pérdida y replay; validar autenticación y safe mode con simulador, nunca satélite operativo. Medir detección, disponibilidad, latencia y recuperación.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.