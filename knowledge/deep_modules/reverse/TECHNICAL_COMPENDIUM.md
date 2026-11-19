# Compendio técnico: Ingeniería inversa

ID: `reverse` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Ingeniería inversa; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema
### 1. arquitecturas, ABI y calling conventions

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. desensamblado y depuración

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. control flow y data flow

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. formatos binarios y linking

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. emulación y análisis aislado

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. protecciones y empaquetado

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. reproducibilidad y divulgación

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
| reverse-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| reverse-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| reverse-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| reverse-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

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


## Profundización técnica específica: Ingeniería inversa

### Flujo de análisis y preservación
Registrar origen autorizado, hash, arquitectura, formato, compilador probable, símbolos, dependencias, empaquetado y entorno. Preservar original y derivar copias de trabajo. La ingeniería inversa debe respetar licencias, contratos y legislación; priorizar interoperabilidad, análisis defensivo, respuesta y evaluación autorizada.

### Formatos y loaders
Analizar PE, ELF, Mach-O, bytecode JVM, .NET, DEX y firmware. Entender headers, secciones, relocations, imports, exports, dynamic loader, linking, ASLR, DEP/NX, PIE, stack canaries y metadata. Identificar packers, overlays y recursos. Desempaquetar altera representación; guardar hashes de cada etapa y documentar herramienta/versión.

### Desensamblado, decompilación y flujo
Reconstruir CFG, funciones, calling conventions, ABI, stack frames, registers, exceptions, indirect calls y control-flow obfuscation. El pseudocódigo es hipótesis, no fuente original. Validar tipos, estructuras y límites con trazas, referencias cruzadas y datos observados. Distinguir análisis estático, emulación e instrumentación dinámica.

### Análisis de datos y criptografía
Seguir taint desde entrada a sinks, reconstruir parsers, serialización, formatos y protocolos. Identificar uso de RNG, claves embebidas, nonce, KDF y primitivas, sin asumir debilidad por apariencia. No extraer ni divulgar secretos ajenos; documentar exposición de manera mínima y responsable.

### Vulnerabilidades y mitigaciones
Buscar integer overflow, memory corruption, use-after-free, race conditions, deserialization, path traversal y validación deficiente. Formular precondiciones y demostrar impacto en harness local o PoC inocua. Mitigar con límites, safe APIs, hardening, fuzzing, tests y parche. Coordinar disclosure y no publicar artefactos que faciliten abuso real.

### Laboratorios
- Analizar binarios de juguete compilados con símbolos y sin símbolos.
- Reconstruir parser de formato sintético y crear corpus fuzz.
- Comparar decompilación con fuente conocida para estimar límites.
- Trazar flujo de datos hacia una función sensible en código de laboratorio.
Medir cobertura de funciones, precisión de hipótesis, crashes reproducibles y falsos positivos.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.