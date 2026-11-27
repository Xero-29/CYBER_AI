# Compendio técnico: Ingeniería inversa

ID: `reverse` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Ingeniería inversa; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. Arquitecturas, ABI y calling conventions

La ingeniería inversa comienza con arquitectura y entorno: ISA, modo de ejecución, endianness, tamaño de palabra, alineación, ABI, formato de objeto, linker y loader. Distinguir x86-64 System V, Windows x64, AArch64 y convenciones específicas. En llamadas, identificar registros de argumentos/retorno, stack alignment, caller/callee-saved, shadow space, red zone, prólogo/epílogo y manejo de excepciones.

No inferir prototipos solo por decompilación. Comparar call sites, usos de registros, acceso a stack, referencias y comportamiento observado. PIE/ASLR, relocations, PLT/GOT, import tables y símbolos alteran direcciones; usar offsets relativos y registrar base de carga.

### 2. Desensamblado, depuración y validación de hipótesis

Desensamblador transforma bytes en instrucciones posibles; decompilador produce pseudocódigo aproximado. Ninguno recupera el código fuente original de forma garantizada. Validar boundaries de funciones, indirect branches, jump tables, tail calls, inlining, exceptions y código mezclado con datos. Comparar varios análisis y anotar incertidumbre.

Depuración dinámica en binarios de laboratorio: breakpoints, watchpoints, single-step, registros, stack, memoria y trazas. La instrumentación puede modificar timing y comportamiento. Guardar versión, símbolos, flags de compilación y entorno. Evitar depurar software de terceros sin autorización.

### 3. Control flow, data flow y reconstrucción semántica

Construir CFG con bloques básicos y aristas de control; construir call graph y data-flow graph para rastrear valores. SSA ayuda a razonar sobre definiciones y usos; aliasing y punteros dificultan conclusiones. Identificar validaciones, sanitización, transformaciones, estados, invariantes y efectos secundarios. Distinguir flujo alcanzable de código muerto o condicionado.

Para cada función documentar entradas, salidas, precondiciones, postcondiciones, estado global, errores y llamadas externas. Contrastar pseudocódigo con trazas de ejecución y tests de comportamiento. No renombrar símbolos como hechos: marcar etiquetas inferidas.

### 4. Parsing, formatos, serialización y protocolos

Reconstruir estructuras desde offsets, tamaños, endian, alignment, checksums, version tags, length fields y estados del parser. Usar corpus válido, inválido, truncado y límites. Validar integer overflow, signedness, desbordamiento de longitud, confusión de encoding, desincronización y diferencias parser/differential. Para protocolos, separar framing, negociación, autenticación, cifrado y payload; analizar PCAP sintético y documentación pública.

### 5. Ofuscación, empaquetado y anti-análisis

Distinguir compresión, cifrado, virtualización, control-flow flattening, opaque predicates, string encryption y anti-debugging. Entropía alta solo es señal auxiliar. La desofuscación debe conservar original, registrar cada transformación y comparar hashes. En malware o software potencialmente dañino, trabajar con muestras autorizadas y sandbox aislada; el objetivo del módulo es comprensión y defensa, no evadir controles ni producir implantes.

### 6. Vulnerabilidades, fuzzing y análisis diferencial

Identificar clases de fallos: integer overflow, out-of-bounds, use-after-free, double free, type confusion, race, deserialization, path traversal y validación incorrecta. Formular precondiciones y demostrar el defecto con harness inocuo, input mínimo y sanitizer. Fuzzing: corpus semilla, mutador, oracle, cobertura, crash deduplication, minimización y reproducción. No tratar crash como vulnerabilidad explotable sin análisis de causa e impacto.

Análisis diferencial compara versiones, builds o implementaciones: normalizar entorno, inputs, flags y dependencias; identificar cambios de comportamiento y regresiones. Para disclosure, coordinar con proveedor, respetar plazos y limitar detalles operativos hasta mitigación.

### 7. Firmware, dispositivos y componentes embebidos

Identificar contenedor, particiones, bootloader, kernel, filesystem, device tree, secure boot, firma, rollback protection y actualización OTA. Extraer firmware solo de dispositivos propios o autorizados; preservar imagen y hashes. Analizar configuración, secretos embebidos y protocolos sin conectarse a redes ajenas. La emulación no reproduce necesariamente periféricos, timing ni root of trust físico.

## Laboratorio reproducible

Usar programas propios, binarios de juguete compilados por el equipo, firmware de laboratorio y corpus sintético. No ejecutar payloads reales ni hacer ingeniería inversa de objetivos sin autorización.

| ID | Experimento frío | Diseño y criterio de aceptación |
|---|---|---|
| reverse-LAB-01 | ABI y calling convention | Compilar funciones pequeñas en 2 arquitecturas/ABIs; reconstruir argumentos y stack; contrastar con fuente |
| reverse-LAB-02 | CFG y decompilación | Programa con switch, inlining y excepciones; comparar CFG y pseudocódigo con ground truth |
| reverse-LAB-03 | Data flow | Seguir input sintético hasta sink; documentar sanitización, aliasing y rutas alternativas |
| reverse-LAB-04 | Parser y fuzzing | Parser de formato propio; corpus válido/malformado; sanitizers sin out-of-bounds ni hangs |
| reverse-LAB-05 | Análisis diferencial | Comparar dos versiones de programa propio; localizar cambio y generar test de regresión |
| reverse-LAB-06 | Ofuscación didáctica | Transformaciones inocuas de strings/control flow; medir pérdida de legibilidad y documentar límites |
| reverse-LAB-07 | Firmware de juguete | Analizar imagen creada para el laboratorio; identificar particiones, firmas y límites de emulación |

Conservar fuente ground truth, flags, binario, hashes, versión de herramientas, scripts, input corpus, crashes minimizados, logs y conclusión. Diseño definido; ejecución pendiente.

## Métricas y evaluación

Medir exactitud de reconstrucción de funciones, bloques CFG, referencias, campos de estructura, tasa de reproducción de crashes, cobertura de fuzzing, tiempo por hipótesis y falsos positivos. Reportar resultados por arquitectura, compilador, optimización y herramienta. Una puntuación de decompilación no equivale a recuperación semántica.

## Artefactos de aceptación

- Inventario de binario, arquitectura y hash.
- Modelo ABI y mapa de funciones.
- CFG/data-flow con ground truth.
- Hipótesis y observaciones dinámicas reproducibles.
- Harness, corpus y tests de regresión.
- Análisis de límites y riesgos de seguridad.
- Revisión independiente y disclosure responsable.

## Madurez

Contenido editorial específico incorporado; los experimentos no están ejecutados y no hay revisión independiente. M2 como máximo.

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