# Agenda de investigación: seguridad de aplicaciones y servicios

**Dominio:** `appsec` · **Objetivo:** investigación reproducible (K5) · **Estado actual:** agenda e hipótesis propuestas; no investigación concluida.  
**Límite empírico:** no M3/M4/M5 hasta ejecutar experimentos, analizar resultados y obtener revisión/reproducción independiente.

## Problema y alcance

La seguridad de aplicaciones se evalúa con estándares, pruebas automatizadas y revisión manual, pero la presencia de controles o la cantidad de hallazgos no demuestran por sí mismas una reducción del riesgo. Esta agenda busca medir cobertura, precisión, eficacia de controles, coste operativo y reproducibilidad en aplicaciones de laboratorio, sin extrapolar resultados a producción sin evidencia.

## Estado del arte y estrategia de búsqueda

Fuentes primarias iniciales: OWASP ASVS 5.0.0, OWASP WSTG 4.2 (WSTG 5.0 figura en desarrollo), OWASP API Security Top 10 2023, OWASP Cheat Sheet Series, CWE Top 25 2025 y NIST SP 800-218 SSDF 1.1. Se identificaron páginas oficiales y abstracts; no se declara lectura integral de todos los documentos ni revisión sistemática.

Para ampliar literatura: buscar en IEEE Xplore, ACM Digital Library, USENIX, arXiv (preprints separados de peer review) y repositorios institucionales con consultas reproducibles sobre software security testing, authorization testing, taint analysis, vulnerability detection, dependency reachability y software supply-chain attestations. Registrar fecha, consulta exacta, filtros, criterios de inclusión/exclusión, duplicados y razón de descarte.

## Línea 1 — Pruebas de autorización multi-tenant

**Pregunta:** ¿Una matriz sujeto–acción–objeto–tenant mejora la detección de fallos BOLA/BOPLA/BFLA frente a pruebas basadas únicamente en endpoints?

- H1: la matriz explícita aumenta recall de defectos sembrados sin incremento desproporcionado de falsos positivos.
- H0: la diferencia de recall no supera el umbral práctico predefinido.
- Diseño: aplicación sintética con dos o más tenants, roles y recursos; defectos sembrados de lectura/escritura/exportación; comparadores endpoint-centric y matriz relacional.
- Variables: método de prueba; recall, precision, cobertura de combinaciones, tiempo de triage y defectos escapados.
- Controles: mismo código, rutas, datos, roles, orden aleatorizado y versiones congeladas.
- Validez: defectos sembrados no representan todo el espectro de errores reales; documentar sesgo del benchmark.

## Línea 2 — Eficacia combinada de SAST, DAST, SCA y revisión manual

**Pregunta:** ¿Qué combinación de técnicas ofrece mejor relación entre defectos confirmados, falsos positivos, cobertura y coste?

- H1: combinación de técnicas complementarias detecta clases distintas de fallos y mejora recall frente a cada técnica aislada.
- H0: la combinación no mejora recall o el coste de revisión supera el beneficio acordado.
- Diseño: repositorio sintético versionado con defectos conocidos y revisión ciega por dos evaluadores; SAST/DAST/SCA ejecutados con reglas fijadas.
- Variables: técnica/combinación; TP/FP/FN, precision, recall, F1, tiempo y cobertura por CWE.
- Controles: baseline, versiones de herramientas, configuración, corpus, criterios de etiquetado y umbral de severidad.
- Validez: etiquetas imperfectas, sesgo por reglas conocidas y dependencia de lenguajes/frameworks.

## Línea 3 — Análisis de flujo de datos y sanitizadores

**Pregunta:** ¿Cuánto cambia la precisión de análisis de taint cuando el modelo incorpora fuentes, sinks, propagadores y sanitizadores específicos del framework?

- H1: modelos de flujo adaptados al framework reducen falsos positivos frente a reglas genéricas manteniendo recall.
- H0: el modelado adicional no produce mejora medible o aumenta falsos negativos.
- Diseño: corpus de ejemplos con rutas de datos etiquetadas y versiones de frameworks.
- Métricas: precision/recall por clase, rutas alcanzadas, tiempo de análisis y errores por sanitizador mal modelado.
- Controles: mismos ejemplos, compilador, dependencias, reglas y versiones.
- Validez: el corpus puede no cubrir patrones emergentes ni configuraciones de producción.

## Línea 4 — Mitigaciones de SSRF y DNS cambiante

**Pregunta:** ¿Qué combinación de validación de destino, resolución DNS, control de egress y política de redirección resiste mejor escenarios sintéticos de rebinding y redirección?

- H1: defensa en capas con validación de IP resuelta y egress restringido bloquea más casos que validación textual de URL aislada.
- H0: la defensa en capas no mejora el bloqueo o genera fallos operativos inaceptables.
- Diseño: simulador local de DNS/HTTP, destinos reservados y servicios falsos; no usar infraestructura pública ni direcciones de terceros.
- Métricas: intentos bloqueados/permitidos, falsos bloqueos, redirecciones, tiempo y registros.
- Controles: reloj, TTL, secuencia de resolución, configuración de proxy y reglas de firewall fijas.
- Validez: el simulador no reproduce todos los resolvers, proxies ni redes cloud.

## Línea 5 — Priorización contextual de dependencias

**Pregunta:** ¿La priorización que combina severidad (CVSS), señales de explotación (KEV/EPSS), reachability y contexto de despliegue mejora la asignación de esfuerzo frente a severidad sola?

- H1: el modelo contextual mejora la proporción de remediaciones que reducen exposición real, sin omitir vulnerabilidades críticas.
- H0: la priorización contextual no mejora decisiones bajo criterios predefinidos.
- Diseño: snapshots fechados de advisories y SBOM sintéticos o públicos con licencia, aplicaciones de laboratorio y reachability documentada.
- Métricas: precisión de priorización, tiempo a remediación, vulnerabilidades explotables alcanzables y falsos negativos de alto impacto.
- Controles: fijar fecha, versión de advisories, grafo de dependencias y reglas de puntuación.
- Validez: KEV/EPSS reflejan señales del ecosistema, no probabilidad individual exacta ni riesgo total del activo.

## Línea 6 — Integridad de artefactos y procedencia

**Pregunta:** ¿Qué evidencia permite verificar que el artefacto desplegado corresponde al código revisado y al proceso de build aprobado?

- H1: SBOM más procedencia firmada y verificación de digest detecta sustituciones que no detecta un SBOM aislado.
- H0: la combinación no detecta más alteraciones o el coste supera el beneficio definido.
- Diseño: pipeline de laboratorio con builds controlados, artefactos mutados y verificación de firmas/digests.
- Métricas: alteraciones detectadas, falsos rechazos, reproducibilidad de build, coste y completitud de metadatos.
- Controles: runner aislado, claves de prueba, commits fijos y política de confianza predefinida.
- Validez: no equivale a demostrar que el código original sea seguro ni que el proceso de build no esté comprometido.

## Protocolo común y análisis

Antes de cada experimento:
1. registrar protocolo, hipótesis, outcomes primarios/secundarios y análisis;
2. definir unidad de análisis, muestra, criterios de inclusión/exclusión y baseline;
3. fijar commit, dependencias, contenedor, sistema operativo, versiones y semillas;
4. separar conjunto de desarrollo y evaluación; evitar fuga de datos;
5. definir ground truth y doble revisión para casos ambiguos;
6. registrar datos brutos, logs saneados, hashes, desviaciones y fallos;
7. reportar tamaño de muestra, intervalos de incertidumbre, tamaños de efecto y limitaciones;
8. conservar resultados negativos y no seleccionar solo métricas favorables;
9. pedir revisión independiente y réplica antes de afirmar generalización.

No escoger una prueba estadística por rutina: verificar supuestos, distribución, independencia y tamaño de muestra. Para métricas binarias, considerar intervalos apropiados; para comparaciones pareadas, preservar emparejamiento. Evitar inferir causalidad desde correlaciones observacionales.

## Entregables de investigación

- revisión sistemática o scoping review con estrategia reproducible;
- mapa de requisitos ASVS versionados y escenarios WSTG versionados;
- corpus/dataset con licencia, esquema, hashes y etiquetas;
- scripts y configuración de experimentos;
- resultados brutos y procesados;
- análisis estadístico y amenazas a validez;
- informe de resultados negativos y positivos;
- réplica independiente y registro de discrepancias.

## Umbrales de madurez

- **M1:** páginas/abstracts y agenda exploratoria.
- **M2:** lectura crítica documentada y protocolo definido.
- **M3:** experimento ejecutado con datos y análisis trazables.
- **M4:** revisión técnica independiente y resultados reproducibles en entorno equivalente.
- **M5:** reproducción externa/independiente, límites explicitados y contribución revisada.

**Estado actual: M1. No M3/M4/M5.** No se ha ejecutado ninguno de los seis estudios.
