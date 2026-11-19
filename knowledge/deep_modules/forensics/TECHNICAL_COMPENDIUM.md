# Compendio técnico: Forense digital

ID: `forensics` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Forense digital; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema
### 1. cadena de custodia y evidencia

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. adquisición forense y write blockers

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. filesystem, artefactos y timeline

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. memoria volátil y procesos

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. logs, navegador y endpoints

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. PCAP, móviles y cloud

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. reproducibilidad y reporte

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
| forensics-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| forensics-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| forensics-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| forensics-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

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


## Profundización técnica específica: Informática forense

### Principios, alcance y cadena de custodia
Definir autoridad legal, objetivo, alcance, jurisdicción, custodio, fuente, método, herramienta/versión, hora, zona horaria y hash. Preservar original, trabajar sobre copias verificadas y registrar cada transferencia/acceso. Minimizar datos personales y privilegiados no pertinentes. La adquisición debe ser proporcional y documentada; una imagen no es íntegra por el mero hecho de generarse.

### Adquisición y volatilidad
Priorizar según volatilidad: estado de memoria, procesos, conexiones, sesiones, claves volátiles y configuración activa; después discos, snapshots, logs remotos, cloud y backups. La secuencia depende del caso y riesgo de alterar evidencia. Registrar herramientas, comandos, errores, tiempos y cambios inevitables. En cloud, preservar snapshots, API audit logs, metadata, identidad y límites de retención del proveedor.

### Sistemas de archivos y artefactos
Analizar particiones, volúmenes, MFT/USN Journal, timestamps, permisos, enlaces, borrados, journaling y artefactos de ejecución. Distinguir MAC times y su posibilidad de manipulación. Correlacionar Prefetch, Amcache, Shimcache, Registry, Event Logs, LNK, Jump Lists, browser artifacts, shell history y logs Linux. No atribuir autoría solo por una cuenta o timestamp.

### Memoria, malware y red
Memoria permite examinar procesos, módulos, handles, sockets, regiones y artefactos de ejecución; depende de perfil, kernel y método de adquisición. Red reconstruye sesiones desde PCAP, NetFlow, DNS, proxy y firewall, considerando reloj y pérdida. Malware requiere análisis estático/dinámico en sandbox aislado; nunca ejecutar muestras en host de trabajo. Documentar evasión, límites del sandbox y artefactos generados por el análisis.

### Cloud, móviles y contenedores
En móviles preservar estado, cifrado, lock state, backups, permisos y cadena de custodia del dispositivo. En cloud registrar tenant, región, API, principal, recurso, snapshot ID, audit events y retención. Contenedores requieren imagen digest, layers, manifiestos, runtime state, volúmenes y nodos. Los datos exportados deben conservar metadatos y procedencia.

### Análisis, validación y reporte
Separar hechos observados, inferencias y opiniones. Validar herramientas con datasets conocidos, controles negativos, hashes y replicación. Reportar método, cobertura, artefactos, limitaciones, zonas horarias, incertidumbre y explicaciones alternativas. Conclusiones deben ser reproducibles por otro examinador con acceso legal equivalente.

### Laboratorios
- Imagen forense de disco sintético con artefactos sembrados y ground truth.
- Adquisición de memoria de VM de laboratorio y reconstrucción de procesos/conexiones.
- Timeline multifuente con desviación horaria conocida.
- Caso de incidente cloud sintético con snapshots y audit logs.
Evaluar exactitud de recuperación, falsos positivos, tiempo, reproducibilidad y alteración introducida.

## Estado de validación de la ampliación
Contenido técnico editorial añadido; fuentes completas, revisión independiente y laboratorios ejecutados permanecen pendientes. No elevar por redacción a M3/M4/M5.