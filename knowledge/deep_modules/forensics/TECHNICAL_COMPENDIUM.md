# Compendio técnico: Forense digital

ID: `forensics` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Forense digital; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. Cadena de custodia, integridad y admisibilidad

La evidencia digital debe conservar identidad, integridad, procedencia, contexto y trazabilidad desde la adquisición hasta la presentación. Registrar quién obtiene, cuándo, dónde, con qué autoridad, herramienta y versión, método, condiciones, hash inicial/final, transferencias, almacenamiento y accesos. Un hash prueba igualdad de bytes entre momentos, no autenticidad de origen ni corrección del procedimiento.

Distinguir evidencia original, imagen forense, copia de trabajo, exportación lógica y artefacto derivado. Documentar transformaciones, zona horaria, reloj del sistema, errores y decisiones del examinador. Las reglas legales varían por jurisdicción; el laboratorio técnico no determina por sí solo admisibilidad.

### 2. Adquisición forense, write blockers y verificación

Antes de adquirir, identificar medio, interfaz, capacidad, estado, cifrado, riesgos de encendido y autoridad. Preferir adquisición bit a bit cuando el caso lo requiere; adquisición lógica cuando alcance y limitaciones estén justificados. Usar write blocker validado, registrar modelo/firmware y comprobar que el origen no cambia. En medios defectuosos, usar herramientas que gestionen errores y registrar sectores no leídos; nunca ocultar huecos.

Calcular hash de origen cuando sea posible y de imagen resultante; verificar copia, tamaño, logs y errores. La adquisición en vivo puede modificar RAM, procesos, conexiones y timestamps: documentar orden de volatilidad y toda interacción. Cifrado, TRIM, SSD, RAID y almacenamiento cloud imponen límites distintos.

### 3. Filesystems, artefactos y timeline

Interpretar particiones, volúmenes, filesystem, metadata, journal y asignación de bloques. NTFS: MFT, USN Journal, $LogFile, ADS y timestamps; FAT/exFAT: directorios, allocation tables y limitaciones de metadata; ext4: superblocks, inodes, journal y extents; APFS: containers, snapshots, clones y encryption. La interpretación debe ser dependiente de versión y estado del filesystem.

Construir timeline normalizando UTC y conservando valor original, zona, fuente y precisión. Correlacionar filesystem, logs, browser, endpoint, autenticación y red. MAC times pueden alterarse, copiarse o reflejar procesos legítimos. Registrar hipótesis alternativas y contradicciones; no ordenar eventos de distinta precisión como si fueran exactos.

### 4. Memoria, procesos y artefactos volátiles

Adquirir memoria con método compatible y documentar herramienta, versión, arquitectura, perfil y alteraciones. Analizar procesos, threads, módulos, handles, sockets, regiones, command lines, environment, credenciales residuales y objetos kernel cuando proceda. Un perfil incorrecto puede producir resultados plausibles pero erróneos. Volcado de memoria puede contener secretos y datos personales: acceso mínimo, cifrado y retención limitada.

La evidencia volátil desaparece con apagado o cambios; priorizar captura según objetivo y riesgo. En incidentes activos coordinar con respuesta para no destruir actividad crítica. Separar artefactos del sistema de artefactos de herramientas de adquisición.

### 5. Forense de red, correo y navegador

PCAP preserva paquetes capturados, pero la captura puede perder tráfico, omitir segmentos o sufrir asimetría. Documentar punto de captura, filtros, snaplen, reloj, drops y topología. Correlacionar DNS, TLS metadata, proxy, firewall, DHCP y autenticación. No atribuir contenido cifrado que no fue observado.

Correo: conservar mensaje original con headers completos, Received chain, Message-ID, DKIM, SPF, DMARC y adjuntos con hashes; validar la cadena y reconocer que headers pueden falsificarse fuera de dominios confiables. Browser: historia, cache, cookies, downloads, local storage y sincronización; explicar artefactos de perfiles múltiples y borrado.

### 6. Forense cloud, móvil y entornos distribuidos

La evidencia cloud depende de proveedor, región, servicio, API, retención y permisos. Exportar audit logs, snapshots, objetos, identity events y configuración con IDs, timestamps, request IDs y cadena de custodia. La consola puede mostrar vistas transformadas; conservar exportación original y documentación de API. En contenedores, capturar metadata de orquestador, image digest, layers, runtime events, volumes y logs; una imagen no representa estado efímero.

En móvil, documentar modelo, OS/build, estado de bloqueo, cifrado, aislamiento, método lógico/file-system/físico y limitaciones. No eludir controles ni adquirir dispositivos ajenos sin autorización. Backups sincronizados no equivalen a contenido íntegro del dispositivo.

### 7. Análisis, informe y testimonio técnico

Separar pregunta pericial, alcance, método, observación, inferencia, conclusión y limitación. Cada conclusión debe apuntar a artefactos identificados y método reproducible. Usar lenguaje calibrado: observado, consistente con, probable bajo supuestos, no determinado. Explicar herramientas, validación, errores conocidos y posibilidad de falsos positivos.

## Laboratorio reproducible

Usar imágenes de entrenamiento con licencia, discos virtuales creados por el equipo y datasets públicos autorizados. Nunca practicar sobre el disco de trabajo ni datos personales reales.

| ID | Experimento frío | Diseño y criterio de aceptación |
|---|---|---|
| forensics-LAB-01 | Cadena de custodia | Crear evidencia sintética; completar transferencias y hashes; cualquier discrepancia queda detectada y explicada |
| forensics-LAB-02 | Imagen y write blocker | Medio virtual read-only; demostrar que origen no cambia y que la imagen verifica |
| forensics-LAB-03 | Timeline filesystem | Generar eventos conocidos; reconstruirlos con zonas horarias y precisión declaradas |
| forensics-LAB-04 | PCAP y DNS | Capturar tráfico de laboratorio; identificar pérdidas, filtros y límites de inferencia |
| forensics-LAB-05 | Memoria de entrenamiento | Analizar dump autorizado con perfil correcto/incorrecto; documentar sensibilidad a perfil |
| forensics-LAB-06 | Evidencia cloud sintética | Exportar eventos de cuenta demo; verificar IDs, paginación, integridad y retención |
| forensics-LAB-07 | Informe reproducible | Entregar conclusiones vinculadas a artefactos, alternativas y límites; revisión ciega por segundo analista |

Registrar hashes, herramientas, versiones, comandos, configuración, operador, reloj, logs, errores y cadena de custodia. Diseño definido; ejecución pendiente.

## Métricas y evaluación

Medir integridad de adquisición, sectores no leídos, reproducibilidad entre analistas, porcentaje de afirmaciones trazables, errores de timeline, precisión de clasificación y tiempo. Evaluar falsos positivos/negativos con ground truth. No usar tasa de hash coincidente como única métrica de calidad pericial.

## Artefactos de aceptación

- Autoridad y alcance documentados.
- Cadena de custodia completa.
- Adquisición verificada y limitaciones declaradas.
- Herramientas validadas con dataset controlado.
- Timeline con zona horaria, precisión y fuente.
- Informe que distingue hechos e inferencias.
- Revisión independiente y retención segura.

## Madurez

Contenido editorial específico incorporado; no se ha adquirido ni analizado evidencia real. Lectura integral de fuentes, laboratorios, revisión independiente y validación jurídica siguen pendientes. M2 como máximo.

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