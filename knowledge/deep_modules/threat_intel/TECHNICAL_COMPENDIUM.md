# Compendio técnico: Inteligencia de amenazas

ID: `threat_intel` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Inteligencia de amenazas; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. Ciclo de inteligencia, PIR y requisitos

La inteligencia convierte preguntas de decisión en productos oportunos y evaluables. Definir Priority Intelligence Requirements (PIR), necesidades de información, consumidor, decisión que soporta, horizonte, nivel de confianza y cadencia. El ciclo incluye dirección, planificación, recolección, procesamiento, análisis, difusión y retroalimentación; no es estrictamente lineal.

Cada requisito debe ser específico y accionable: qué se necesita saber, para quién, para cuándo y qué decisión cambiaría. Evitar producir reportes que solo enumeran indicadores sin responder al problema. Mantener matriz requisito→fuente→colección→análisis→producto→decisión.

### 2. OSINT, fiabilidad, sesgos y validación

Registrar procedencia, autoría, fecha de publicación/observación, método, jurisdicción, acceso, idioma, limitaciones y riesgo de manipulación. Evaluar fiabilidad de fuente separada de credibilidad de la información: una fuente generalmente confiable puede equivocarse; una fuente desconocida puede aportar un dato corroborable. Usar escalas con definiciones internas explícitas, no números sin metodología.

Corroborar mediante fuentes independientes, buscar evidencia contradictoria y conservar capturas/metadatos conforme a ley y política. Evitar doxxing, recolección innecesaria de datos personales y atribuciones basadas en identidad aparente. OSINT no equivale a verdad ni autoriza intrusión.

### 3. STIX, TAXII, MISP y modelado de inteligencia

STIX 2.1 modela objetos y relaciones como Indicator, Malware, Intrusion Set, Campaign, Threat Actor, Tool, Vulnerability, Observed Data, Sighting y Report. TAXII 2.1 transporta colecciones y objetos; MISP facilita intercambio y correlación de eventos/atributos. Los objetos deben llevar source, created/modified, confidence, markings, external references y granularidad temporal.

Un indicador STIX no es una firma universal: especificar pattern_type, valid_from, valid_until, labels y contexto. Gestionar revocación, versionado, duplicados, confianza y marking. En TAXII revisar autenticación, paginación, filtros, retención, control de acceso y sincronización incremental. En MISP evitar exportar eventos sin revisar distribución y clasificación.

### 4. TTP, ATT&CK y análisis de comportamiento

ATT&CK organiza tácticas, técnicas y sub-técnicas observadas; no es taxonomía completa ni prueba de que una organización fue comprometida. Mapear comportamiento observado a técnica con evidencia y confianza; indicar alternativas y técnicas no observables. Diferenciar procedimiento específico de técnica general.

Construir hipótesis sobre objetivo, acceso inicial, ejecución, persistencia, descubrimiento, movimiento lateral, colección, exfiltración e impacto. Relacionar cada hipótesis con telemetría que podría confirmarla o refutarla. Evitar mapear por nombre de herramienta solamente.

### 5. Atribución, campañas y análisis de actores

La atribución es una inferencia probabilística, no una etiqueta determinista. Separar infraestructura, herramientas, TTP, idioma, horario, victimología, targeting y declaraciones públicas. Evaluar falsos flags, infraestructura compartida, reuso de código, operaciones de engaño y dependencia de fuentes secundarias. Expresar nivel de confianza y evidencia contradictoria.

Usar hipótesis competidoras y matriz de evidencia; declarar qué hallazgo haría cambiar la conclusión. No atribuir a una persona ni grupo solo por geolocalización, idioma, malware compartido o proveedor de hosting.

### 6. Indicadores, detección y utilidad operacional

IOC: hash, dominio, URL, IP, certificado, email, mutex u otro observable. TTP y patrones conductuales suelen ser más duraderos, pero requieren contexto y telemetría. Cada indicador debe tener fuente, primera/última observación, expiración, confianza, false positive known, sightings y acción recomendada. Evitar bloquear IPs compartidas o dominios legítimos sin análisis de impacto.

Medir utilidad por detecciones confirmadas y decisiones mejoradas, no por cantidad de indicadores. Integrar inteligencia con SIEM/EDR mediante reglas con pruebas, TTL y propietario. La ausencia de coincidencias no significa ausencia de amenaza.

### 7. Productos, difusión y retroalimentación

Productos: alerta táctica, informe técnico, evaluación estratégica, perfil de actor, campaña, brief ejecutivo y paquete de detección. Adaptar detalle, confianza, incertidumbre y recomendación al consumidor. Marcar información sensible, restricciones de distribución, expiración y nivel de confianza. Recoger feedback sobre utilidad y decisiones reales.

## Laboratorio reproducible

Usar CTI feeds de prueba, datasets públicos con licencia y eventos sintéticos; no recolectar datos personales ni interactuar con infraestructura adversaria.

| ID | Experimento frío | Diseño y criterio de aceptación |
|---|---|---|
| ti-LAB-01 | PIR a producto | Convertir 3 preguntas decisionales en requisitos medibles y productos; revisión de consumidor |
| ti-LAB-02 | Evaluación de fuentes | Dataset con fuentes confiables, dudosas y contradictorias; justificar credibilidad y sesgos |
| ti-LAB-03 | STIX/TAXII | Crear bundle sintético, validar esquema, referencias, marking, versionado y revocación |
| ti-LAB-04 | MISP e intercambio | Importar/exportar evento de prueba; comprobar distribución, deduplicación y trazabilidad |
| ti-LAB-05 | Mapeo ATT&CK | Etiquetar observaciones con evidencia y alternativas; segundo analista revisa falsos mapeos |
| ti-LAB-06 | Atribución con hipótesis rivales | Dataset sintético; actualizar confianza ante evidencia contradictoria y explicar incertidumbre |
| ti-LAB-07 | Utilidad de detección | Evaluar IOC con fixtures benignos/maliciosos etiquetados; medir precisión, caducidad y coste colateral |

## Métricas y evaluación

Medir tiempo de respuesta a PIR, porcentaje de productos accionables, precisión de indicadores, tasa de caducidad, cobertura de fuentes, corroboración independiente, calibración de confianza, falsos positivos y decisiones modificadas. Evaluar utilidad con consumidores reales solo bajo autorización y gobernanza. No usar cantidad de IOCs como proxy de calidad.

## Artefactos de aceptación

- Registro de PIR y consumidor.
- Matriz fuente/procedencia/confianza.
- Evidencia corroborante y contradictoria.
- Objetos STIX/MISP validados.
- Mapeo ATT&CK con citas a observaciones.
- Hipótesis de atribución y confianza calibrada.
- Producto con expiración, markings y feedback.

## Madurez

Contenido editorial específico incorporado; feeds, normas y literatura no están revisados integralmente. Los laboratorios están diseñados, no ejecutados. M2 como máximo.

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
| threat_intel-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| threat_intel-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| threat_intel-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| threat_intel-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

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


## Profundización técnica específica: Inteligencia de amenazas

### Requisitos e hipótesis
Partir de PIR/EEI vinculados a decisiones concretas: proteger activos, priorizar vulnerabilidades, detectar actividad o preparar respuesta. Definir consumidor, horizonte, región/sector, nivel de confianza, coste de error y fecha de caducidad. Evitar recopilar indicadores sin pregunta operacional. Separar inteligencia estratégica, operacional, táctica y técnica.

### Ciclo de inteligencia
Planificar, dirigir, recopilar, procesar, analizar, difundir y retroalimentar. Registrar origen, método, fecha de observación, fecha de publicación, geografía, víctima/sector cuando sea lícito, confianza, corroboración y sesgo. Diferenciar fuente primaria, reporte secundario, inferencia analítica y rumor. Mantener hipótesis alternativas y nivel de confianza explícito.

### Modelos y taxonomías
ATT&CK describe tácticas/técnicas observadas; no es una lista de indicadores ni una escala de riesgo. CAPEC modela patrones de ataque y CWE debilidades; STIX estructura objetos y relaciones; TAXII facilita intercambio. Mapear entidades, software, infraestructura, campañas y técnicas con identificadores estables y versionado. Evitar equivalencias uno-a-uno cuando la relación es contextual.

### Indicadores y enriquecimiento
IP, dominio, URL, hash, certificado y artefactos deben incluir contexto temporal, infraestructura compartida, prevalencia, expiración y confianza. Un indicador puede ser legítimo, reutilizado o caducado. Enriquecimiento requiere fuentes independientes, resolución pasiva/activa autorizada, reputación, WHOIS/RDAP, certificados, DNS y contexto de hosting. No convertir coincidencia de IOC en atribución.

### Análisis de actores y campañas
Evaluar TTP, targeting, idioma, infraestructura, malware, timing y motivación con pesos y explicaciones. Separar atribución técnica, organizacional y geopolítica. Registrar hipótesis competidoras, evidencia contradictoria y umbral de confianza. Evitar sesgo de confirmación, circular reporting y atribuciones copiadas entre proveedores.

### Calidad y medición
Medir oportunidad, relevancia, precisión, cobertura, acción habilitada, coste de falsos positivos y caducidad de IOC. Evaluar inteligencia por decisiones mejoradas, no volumen de feeds. Controlar duplicados, normalización, drift, procedencia y licencias. Feedback de SOC/red team/IR actualiza PIR y confianza, pero no reescribe evidencia original.

### Laboratorios
- Procesar STIX bundle sintético y validar relaciones/esquema.
- Correlacionar ATT&CK con telemetría sintética y medir cobertura.
- Evaluar caducidad y falsos positivos de IOC sobre corpus controlado.
- Redactar informe con hipótesis, evidencia contradictoria y confidence statement.
No recolectar ni difundir datos personales o infraestructura sensible fuera de base legal.

## Estado de validación de la ampliación
Contenido técnico editorial añadido; fuentes completas, revisión independiente y laboratorios ejecutados permanecen pendientes. No elevar por redacción a M3/M4/M5.