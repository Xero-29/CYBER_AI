# Agenda de investigación: IoT y hardware

**Dominio:** `iot_hardware` · **Objetivo:** L4 investigación · **Estado:** agenda, no resultados validados.

## Pregunta central

¿Qué propiedades de seguridad, resiliencia y verificabilidad de IoT y hardware pueden medirse objetivamente y qué brechas permanecen en la literatura y práctica actual?

## Agenda por tema

### 1. MCU/SoC y buses

**Pregunta:** ¿Qué enfoques publicados existen para MCU/SoC y buses, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

### 2. UART, SPI, I2C, JTAG y SWD

**Pregunta:** ¿Qué enfoques publicados existen para UART, SPI, I2C, JTAG y SWD, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

### 3. firmware, bootloader y secure boot

**Pregunta:** ¿Qué enfoques publicados existen para firmware, bootloader y secure boot, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

### 4. OTA y rollback protection

**Pregunta:** ¿Qué enfoques publicados existen para OTA y rollback protection, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

### 5. radio, sensores y gateways

**Pregunta:** ¿Qué enfoques publicados existen para radio, sensores y gateways, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

### 6. debug ports y secretos

**Pregunta:** ¿Qué enfoques publicados existen para debug ports y secretos, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

### 7. ciclo de vida y laboratorio

**Pregunta:** ¿Qué enfoques publicados existen para ciclo de vida y laboratorio, bajo qué supuestos funcionan y qué fallos/limitaciones no han sido evaluados suficientemente?

**Hipótesis provisional:** una evaluación controlada con threat model explícito descubre diferencias medibles entre alternativas que no se reflejan en evaluaciones basadas solo en checklist.

**Método:** mapear literatura; definir taxonomía; fijar baseline y criterios; seleccionar escenarios representativos y de borde; variar factores controlados; medir resultados; repetir; analizar falsos positivos, sesgo y validez.

**Métricas:** cobertura de amenazas/controles, eficacia, fiabilidad, tiempo/coste, error de clasificación y reproducibilidad, según el tema.

**Entregable:** protocolo, dataset o casos sintéticos, tabla de evidencia, resultados, análisis crítico y paquete reproducible.

## Estado del arte

Realizar búsqueda reproducible en normas, literatura revisada por pares, especificaciones y documentación primaria. Registrar bases, consultas, fecha, filtros, criterios de inclusión/exclusión y evaluación de calidad. Comparar métodos, supuestos, datasets, métricas y limitaciones; identificar sesgos y preguntas sin resolver.

## Diseño experimental

Definir pregunta, hipótesis falsable, variables, población/unidad de análisis, comparadores, muestra, baseline, métricas, método estadístico, tratamiento de incertidumbre y criterios de refutación. Fijar hardware, versiones, configuración, dependencias y semillas. Registrar todos los cambios y desviaciones.

## Entregables

Revisión de literatura; taxonomía; threat model; protocolo; datos sintéticos/autorizados; código y configuración; SBOM y hashes; resultados brutos saneados; análisis; amenazas a validez; limitaciones; trabajo futuro; revisión y reproducción independiente.

## Salvaguardas

Pruebas activas solo con autorización y alcance; sistemas críticos y dispositivos físicos solo en simulación/banco aislado; proteger datos sensibles y secretos; cadena de custodia para evidencia; divulgación coordinada de vulnerabilidades.

**Criterio:** M4 exige investigación ejecutada y análisis; M5 exige revisión y reproducción independiente. **Madurez actual:** `research_agenda_defined`.
