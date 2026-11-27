# Compendio técnico: Seguridad física ciberfísica

ID: `physical_security` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Seguridad física ciberfísica; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Ruta de desarrollo técnico; no declara cobertura exhaustiva ni fuentes leídas íntegramente. Operar solo con autorización explícita, datos sintéticos y laboratorios aislados. En infraestructuras físicas o críticas, usar simulación/bancos de pruebas y no intervenir producción.

## Desarrollo por subtema
### 1. zonificación y perímetros

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. acceso y visitantes

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. CCTV y sensores

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. USB y medios extraíbles

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. salas, racks y cableado

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. convergencia físico-digital

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. respuesta coordinada

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
| physical_security-LAB-01 | Baseline | Versiones, configuración, hashes y salida |
| physical_security-LAB-02 | Evento/fallo sintético | Entrada, precondiciones, logs y resultado |
| physical_security-LAB-03 | Detección/diagnóstico | Señal, cobertura, precisión y límites |
| physical_security-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después y retest |

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


## Profundización técnica específica: Seguridad física

### Modelo de amenaza físico-digital
Identificar perímetro, edificios, salas, racks, cableado, energía, refrigeración, medios extraíbles, dispositivos, visitantes, proveedores y personal. Modelar adversarios, capacidades, acceso, tiempo, detección y consecuencias. Seguridad física afecta confidencialidad, integridad, disponibilidad y seguridad humana.

### Control de acceso y zonas
Diseñar zonas por criticidad, autenticación multifactor física cuando aplique, anti-tailgating, visitor management, escort, registros y revocación. Revisar llaves maestras, tarjetas perdidas, credenciales compartidas, puertas de emergencia y bypass. Los controles deben preservar evacuación y seguridad de personas.

### Protección de infraestructura
Racks cerrados, puertos deshabilitados, cableado protegido, UPS, generador, HVAC, sensores ambientales, detección de incendio, agua y sabotaje. Evaluar single points of failure, acceso a consola, KVM, BMC y medios backup. Mantener inventario y control de cambios.

### CCTV, biometría y privacidad
Definir finalidad, retención, acceso, auditoría, consentimiento/base legal y minimización. Biometría no es secreto revocable; proteger plantillas y mecanismos de fallback. CCTV debe cubrir riesgos sin vigilancia excesiva. Evaluar falsos positivos y sesgos en controles automatizados.

### Respuesta y pruebas
Procedimientos para intrusión, pérdida de energía, incendio, robo, manipulación y acceso no autorizado. Ejercicios deben coordinar seguridad física, TI, continuidad y autoridades. Medir tiempo de detección, respuesta, cobertura y fallos de control.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.