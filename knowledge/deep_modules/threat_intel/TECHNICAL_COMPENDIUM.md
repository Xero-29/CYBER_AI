# Compendio técnico: Inteligencia de amenazas

ID: `threat_intel` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Inteligencia de amenazas; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema
### 1. ciclo de inteligencia y PIR

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. OSINT, fiabilidad y sesgos

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. STIX/TAXII y MISP

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. ATT&CK, TTP y campañas

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. IOC, contexto y caducidad

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. enriquecimiento y correlación

- **Fundamentos y modelo:** explicar arquitectura, componentes, estados, interfaces, identidades, datos y límites de confianza.
- **Amenazas/fallos:** identificar abuso, errores de diseño e implementación, configuración insegura, dependencias y fallos operativos; indicar precondiciones.
- **Controles:** relacionar prevención, detección, respuesta y recuperación con cada amenaza; explicitar riesgo residual y efectos secundarios.
- **Pruebas:** definir casos positivos, negativos, límites y regresión con entradas sintéticas, resultado esperado, logs y criterio de parada.
- **Investigación:** comparar enfoques, registrar desacuerdos y formular una pregunta falsable sin anticipar resultados.
- **Evidencia:** entregar explicación técnica original, modelo/diagrama, tabla amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. productos estratégicos y tácticos

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