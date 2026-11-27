# Desarrollo técnico de las 192 brechas avanzadas

**Edición:** 2026-11-19 · **Cobertura:** 48 dominios × 4 brechas = 192 módulos.

**Estado:** borradores técnicos estructurados. Este documento no declara lectura integral de cada referencia, experimentos ejecutados, revisión experta ni validación independiente. Las pruebas descritas son planes de laboratorio seguro, no resultados.



# foundations

**Contexto del dominio:** Trata riesgo como decisión bajo incertidumbre: distingue frecuencia, impacto, exposición, eficacia de controles y confianza en evidencia.
## 1. cuantificación de riesgo y análisis de incertidumbre

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Trata riesgo como decisión bajo incertidumbre: distingue frecuencia, impacto, exposición, eficacia de controles y confianza en evidencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. arquitectura de confianza y resiliencia sistémica

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Trata riesgo como decisión bajo incertidumbre: distingue frecuencia, impacto, exposición, eficacia de controles y confianza en evidencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. economía de seguridad y priorización basada en impacto

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Trata riesgo como decisión bajo incertidumbre: distingue frecuencia, impacto, exposición, eficacia de controles y confianza en evidencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. gestión de exposición externa y attack surface management

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Trata riesgo como decisión bajo incertidumbre: distingue frecuencia, impacto, exposición, eficacia de controles y confianza en evidencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# appsec

**Contexto del dominio:** Sigue el flujo de negocio y límites de confianza entre navegador, frontend, backend, terceros y almacenamiento; el servidor aplica la autorización.
## 1. seguridad de lógica de negocio y flujos transaccionales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Sigue el flujo de negocio y límites de confianza entre navegador, frontend, backend, terceros y almacenamiento; el servidor aplica la autorización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-top-ten/
- https://owasp.org/www-project-application-security-verification-standard/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. seguridad de navegador, extensiones y aislamiento de origen

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Sigue el flujo de negocio y límites de confianza entre navegador, frontend, backend, terceros y almacenamiento; el servidor aplica la autorización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-top-ten/
- https://owasp.org/www-project-application-security-verification-standard/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. seguridad de componentes frontend y cadena de dependencias

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Sigue el flujo de negocio y límites de confianza entre navegador, frontend, backend, terceros y almacenamiento; el servidor aplica la autorización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-top-ten/
- https://owasp.org/www-project-application-security-verification-standard/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. pruebas de autorización y propiedades de seguridad por flujo

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Sigue el flujo de negocio y límites de confianza entre navegador, frontend, backend, terceros y almacenamiento; el servidor aplica la autorización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-top-ten/
- https://owasp.org/www-project-application-security-verification-standard/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# api

**Contexto del dominio:** La unidad de control es cada operación sobre recurso y tenant; contratos, autorización, límites y telemetría se prueban por versión.
## 1. GraphQL federation, introspection y autorización por resolver

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La unidad de control es cada operación sobre recurso y tenant; contratos, autorización, límites y telemetría se prueban por versión.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-api-security/
- https://doi.org/10.6028/NIST.SP.800-207A

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. gRPC, protobuf y seguridad de canales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La unidad de control es cada operación sobre recurso y tenant; contratos, autorización, límites y telemetría se prueban por versión.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-api-security/
- https://doi.org/10.6028/NIST.SP.800-207A

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. API inventory, shadow APIs y contratos versionados

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La unidad de control es cada operación sobre recurso y tenant; contratos, autorización, límites y telemetría se prueban por versión.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-api-security/
- https://doi.org/10.6028/NIST.SP.800-207A

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. abuso de negocio, replay y límites distribuidos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La unidad de control es cada operación sobre recurso y tenant; contratos, autorización, límites y telemetría se prueban por versión.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://owasp.org/www-project-api-security/
- https://doi.org/10.6028/NIST.SP.800-207A

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# network

**Contexto del dominio:** Incluye plano de control y datos, resolución DNS, rutas, segmentación, gestión fuera de banda y rutas alternativas.
## 1. BGP, RPKI y validación de origen de rutas

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye plano de control y datos, resolución DNS, rutas, segmentación, gestión fuera de banda y rutas alternativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. IPv6, RA guard y superficies dual-stack

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye plano de control y datos, resolución DNS, rutas, segmentación, gestión fuera de banda y rutas alternativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. DNS moderno, DoH/DoT y seguridad de resolvers

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye plano de control y datos, resolución DNS, rutas, segmentación, gestión fuera de banda y rutas alternativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. SASE, SD-WAN, ZTNA y seguridad de borde

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye plano de control y datos, resolución DNS, rutas, segmentación, gestión fuera de banda y rutas alternativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# linux

**Contexto del dominio:** Distingue kernel, namespaces, capabilities, cgroups, LSM, servicios y userland; los logs de usuario no prueban integridad del host.
## 1. eBPF y observabilidad/seguridad del kernel

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue kernel, namespaces, capabilities, cgroups, LSM, servicios y userland; los logs de usuario no prueban integridad del host.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. Linux namespaces, cgroups y escape de contenedores

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue kernel, namespaces, capabilities, cgroups, LSM, servicios y userland; los logs de usuario no prueban integridad del host.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. PAM, sudo, systemd y hardening por distribución

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue kernel, namespaces, capabilities, cgroups, LSM, servicios y userland; los logs de usuario no prueban integridad del host.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. firmware, boot chain y respuesta a compromisos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue kernel, namespaces, capabilities, cgroups, LSM, servicios y userland; los logs de usuario no prueban integridad del host.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# windows_ad

**Contexto del dominio:** Modela bosque, dominios, trusts, controladores, PKI, identidades híbridas y planos cloud.
## 1. AD CS, certificados y abuso de PKI empresarial

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela bosque, dominios, trusts, controladores, PKI, identidades híbridas y planos cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. Entra ID/híbrido, OAuth y workload identities

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela bosque, dominios, trusts, controladores, PKI, identidades híbridas y planos cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. Kerberos delegation, trusts y tiering avanzado

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela bosque, dominios, trusts, controladores, PKI, identidades híbridas y planos cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. detección de identidad y recuperación forest-level

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela bosque, dominios, trusts, controladores, PKI, identidades híbridas y planos cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# cloud

**Contexto del dominio:** Evalúa control plane, data plane, identidades, metadatos, servicios gestionados, regiones y relaciones entre cuentas.
## 1. SaaS security posture y control plane de identidades

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa control plane, data plane, identidades, metadatos, servicios gestionados, regiones y relaciones entre cuentas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-207A
- https://csrc.nist.gov/pubs/ir/8587/final

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. serverless, event-driven y permisos por función

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa control plane, data plane, identidades, metadatos, servicios gestionados, regiones y relaciones entre cuentas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-207A
- https://csrc.nist.gov/pubs/ir/8587/final

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. CNAPP, CSPM, CIEM y correlación de exposición

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa control plane, data plane, identidades, metadatos, servicios gestionados, regiones y relaciones entre cuentas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-207A
- https://csrc.nist.gov/pubs/ir/8587/final

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. cloud-native zero trust y workload identity

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa control plane, data plane, identidades, metadatos, servicios gestionados, regiones y relaciones entre cuentas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-207A
- https://csrc.nist.gov/pubs/ir/8587/final

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# containers

**Contexto del dominio:** La frontera incluye host, runtime, orquestador, registry, admission, workload identity, red y almacenamiento.
## 1. Kubernetes supply chain y verificación de imágenes

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La frontera incluye host, runtime, orquestador, registry, admission, workload identity, red y almacenamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-190
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. runtime security, eBPF y detección de comportamiento

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La frontera incluye host, runtime, orquestador, registry, admission, workload identity, red y almacenamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-190
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. service mesh, SPIFFE/SPIRE y políticas de servicio

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La frontera incluye host, runtime, orquestador, registry, admission, workload identity, red y almacenamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-190
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. admission control, secrets y recuperación de control plane

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La frontera incluye host, runtime, orquestador, registry, admission, workload identity, red y almacenamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-190
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# mobile

**Contexto del dominio:** Incluye dispositivo, SO, app, SDK, distribución, backend, identidad y radio; el cliente no es autoridad confiable.
## 1. mobile app supply chain y firma de releases

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye dispositivo, SO, app, SDK, distribución, backend, identidad y radio; el cliente no es autoridad confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. runtime application self-protection y anti-tampering

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye dispositivo, SO, app, SDK, distribución, backend, identidad y radio; el cliente no es autoridad confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. baseband, eSIM y superficie de radio

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye dispositivo, SO, app, SDK, distribución, backend, identidad y radio; el cliente no es autoridad confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. privacidad, SDKs de terceros y telemetría móvil

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye dispositivo, SO, app, SDK, distribución, backend, identidad y radio; el cliente no es autoridad confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# crypto

**Contexto del dominio:** La seguridad depende de algoritmo, parámetros, protocolo, implementación, claves, aleatoriedad y ciclo de vida; no diseñar primitivas propias.
## 1. cripto-agilidad e inventario criptográfico empresarial

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La seguridad depende de algoritmo, parámetros, protocolo, implementación, claves, aleatoriedad y ciclo de vida; no diseñar primitivas propias.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.FIPS.203
- https://doi.org/10.6028/NIST.FIPS.204

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. side-channel y fault attacks en implementaciones

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La seguridad depende de algoritmo, parámetros, protocolo, implementación, claves, aleatoriedad y ciclo de vida; no diseñar primitivas propias.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.FIPS.203
- https://doi.org/10.6028/NIST.FIPS.204

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. protocolos híbridos y negociación segura

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La seguridad depende de algoritmo, parámetros, protocolo, implementación, claves, aleatoriedad y ciclo de vida; no diseñar primitivas propias.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.FIPS.203
- https://doi.org/10.6028/NIST.FIPS.204

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. validación de bibliotecas, vectores y erratas

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La seguridad depende de algoritmo, parámetros, protocolo, implementación, claves, aleatoriedad y ciclo de vida; no diseñar primitivas propias.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.FIPS.203
- https://doi.org/10.6028/NIST.FIPS.204

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# identity

**Contexto del dominio:** Distingue autenticación, federación, autorización, sesión, token, identidad humana, workload y cuenta de servicio.
## 1. passkeys/WebAuthn y autenticación resistente a phishing

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue autenticación, federación, autorización, sesión, token, identidad humana, workload y cuenta de servicio.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/pubs/ir/8587/final
- https://doi.org/10.6028/NIST.SP.800-63-4

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. identidades no humanas y ciclo de vida de credenciales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue autenticación, federación, autorización, sesión, token, identidad humana, workload y cuenta de servicio.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/pubs/ir/8587/final
- https://doi.org/10.6028/NIST.SP.800-63-4

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. CIEM y permisos efectivos multi-cloud

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue autenticación, federación, autorización, sesión, token, identidad humana, workload y cuenta de servicio.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/pubs/ir/8587/final
- https://doi.org/10.6028/NIST.SP.800-63-4

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. detección de ataques a identidad y recuperación segura

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Distingue autenticación, federación, autorización, sesión, token, identidad humana, workload y cuenta de servicio.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/pubs/ir/8587/final
- https://doi.org/10.6028/NIST.SP.800-63-4

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# malware

**Contexto del dominio:** Analiza ejecución, persistencia, evasión, comunicación y objetivo; muestras desconocidas solo en laboratorio aislado.
## 1. malware fileless y abuso de herramientas legítimas

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza ejecución, persistencia, evasión, comunicación y objetivo; muestras desconocidas solo en laboratorio aislado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. firmware/UEFI y bootkits

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza ejecución, persistencia, evasión, comunicación y objetivo; muestras desconocidas solo en laboratorio aislado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. análisis de memoria y artefactos multiplataforma

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza ejecución, persistencia, evasión, comunicación y objetivo; muestras desconocidas solo en laboratorio aislado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. ransomware, exfiltración y recuperación coordinada

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza ejecución, persistencia, evasión, comunicación y objetivo; muestras desconocidas solo en laboratorio aislado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# forensics

**Contexto del dominio:** Preserva integridad, cadena de custodia, contexto temporal, procedencia y reproducibilidad; separa observación de inferencia.
## 1. forense de memoria multiplataforma

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Preserva integridad, cadena de custodia, contexto temporal, procedencia y reproducibilidad; separa observación de inferencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/digital-evidence
- https://doi.org/10.6028/NIST.SP.800-86

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. forense SaaS/cloud con APIs y retención distribuida

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Preserva integridad, cadena de custodia, contexto temporal, procedencia y reproducibilidad; separa observación de inferencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/digital-evidence
- https://doi.org/10.6028/NIST.SP.800-86

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. adquisición móvil moderna y cifrado

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Preserva integridad, cadena de custodia, contexto temporal, procedencia y reproducibilidad; separa observación de inferencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/digital-evidence
- https://doi.org/10.6028/NIST.SP.800-86

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. reproducibilidad, validación de herramientas y error forense

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Preserva integridad, cadena de custodia, contexto temporal, procedencia y reproducibilidad; separa observación de inferencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/digital-evidence
- https://doi.org/10.6028/NIST.SP.800-86

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# incident_response

**Contexto del dominio:** Coordina contención, evidencia, continuidad, comunicación y recuperación; cada acción requiere autoridad y criterio de salida.
## 1. respuesta a ransomware y extorsión múltiple

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Coordina contención, evidencia, continuidad, comunicación y recuperación; cada acción requiere autoridad y criterio de salida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://www.cisa.gov/stopransomware

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. respuesta cloud, SaaS e identidad comprometida

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Coordina contención, evidencia, continuidad, comunicación y recuperación; cada acción requiere autoridad y criterio de salida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://www.cisa.gov/stopransomware

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. notificación regulatoria y coordinación sectorial

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Coordina contención, evidencia, continuidad, comunicación y recuperación; cada acción requiere autoridad y criterio de salida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://www.cisa.gov/stopransomware

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. recuperación segura, validación de backups y crisis

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Coordina contención, evidencia, continuidad, comunicación y recuperación; cada acción requiere autoridad y criterio de salida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://www.cisa.gov/stopransomware

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# threat_intel

**Contexto del dominio:** Cada inteligencia necesita fuente, tiempo, confianza, contexto, licencia y caducidad; un IOC no prueba compromiso ni atribución.
## 1. ATT&CK versionado, STIX y procedencia de objetos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Cada inteligencia necesita fuente, tiempo, confianza, contexto, licencia y caducidad; un IOC no prueba compromiso ni atribución.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://oasis-open.github.io/cti-documentation/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. calidad de inteligencia y evaluación de hipótesis

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Cada inteligencia necesita fuente, tiempo, confianza, contexto, licencia y caducidad; un IOC no prueba compromiso ni atribución.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://oasis-open.github.io/cti-documentation/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. detección estratégica basada en cadenas de comportamiento

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Cada inteligencia necesita fuente, tiempo, confianza, contexto, licencia y caducidad; un IOC no prueba compromiso ni atribución.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://oasis-open.github.io/cti-documentation/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. automatización de CTI con control de poisoning

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Cada inteligencia necesita fuente, tiempo, confianza, contexto, licencia y caducidad; un IOC no prueba compromiso ni atribución.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://oasis-open.github.io/cti-documentation/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# reverse

**Contexto del dominio:** Usa binarios identificados por hash, entorno aislado, arquitectura y versiones; diferencia comportamiento observado de intención inferida.
## 1. WebAssembly, bytecode y runtimes modernos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa binarios identificados por hash, entorno aislado, arquitectura y versiones; diferencia comportamiento observado de intención inferida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. firmware, bootloaders y análisis de dispositivos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa binarios identificados por hash, entorno aislado, arquitectura y versiones; diferencia comportamiento observado de intención inferida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. análisis de vulnerabilidades de memoria y compiladores

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa binarios identificados por hash, entorno aislado, arquitectura y versiones; diferencia comportamiento observado de intención inferida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. reproducibilidad de builds y artefactos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa binarios identificados por hash, entorno aislado, arquitectura y versiones; diferencia comportamiento observado de intención inferida.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# iot_hardware

**Contexto del dominio:** La cadena incluye silicio, boot ROM, firmware, componentes, identidad, provisioning, radio, gateway y servicio cloud.
## 1. device identity y provisioning de confianza

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La cadena incluye silicio, boot ROM, firmware, componentes, identidad, provisioning, radio, gateway y servicio cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. SBOM/firmware BOM y vulnerabilidades de componentes

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La cadena incluye silicio, boot ROM, firmware, componentes, identidad, provisioning, radio, gateway y servicio cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. actualizaciones OTA, rollback y recuperación

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La cadena incluye silicio, boot ROM, firmware, componentes, identidad, provisioning, radio, gateway y servicio cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. seguridad de radios, gateways y protocolos industriales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La cadena incluye silicio, boot ROM, firmware, componentes, identidad, provisioning, radio, gateway y servicio cloud.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# devsecops

**Contexto del dominio:** Asegura código, dependencias, builders, runners, secretos, artefactos, provenance y despliegue; la pipeline también es superficie de ataque.
## 1. provenance verificable, SLSA y attestations

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Asegura código, dependencias, builders, runners, secretos, artefactos, provenance y despliegue; la pipeline también es superficie de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/Projects/ssdf
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. OIDC, runners efímeros y permisos por job

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Asegura código, dependencias, builders, runners, secretos, artefactos, provenance y despliegue; la pipeline también es superficie de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/Projects/ssdf
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. seguridad de modelos/datasets en pipelines ML

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Asegura código, dependencias, builders, runners, secretos, artefactos, provenance y despliegue; la pipeline también es superficie de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/Projects/ssdf
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. verificación de artefactos y políticas de despliegue

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Asegura código, dependencias, builders, runners, secretos, artefactos, provenance y despliegue; la pipeline también es superficie de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://csrc.nist.gov/Projects/ssdf
- https://slsa.dev/spec/v1.0/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# ai_security

**Contexto del dominio:** Modela modelo, datos, prompt, retrieval, memoria, herramientas, orquestador, proveedor y usuario; el contenido recuperado no es confiable.
## 1. model supply chain y model BOM

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela modelo, datos, prompt, retrieval, memoria, herramientas, orquestador, proveedor y usuario; el contenido recuperado no es confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. seguridad de agentes, tools y delegación de autoridad

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela modelo, datos, prompt, retrieval, memoria, herramientas, orquestador, proveedor y usuario; el contenido recuperado no es confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. aislamiento multi-tenant de RAG, memoria y vectores

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela modelo, datos, prompt, retrieval, memoria, herramientas, orquestador, proveedor y usuario; el contenido recuperado no es confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. evaluación continua de modelos y datasets contaminados

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela modelo, datos, prompt, retrieval, memoria, herramientas, orquestador, proveedor y usuario; el contenido recuperado no es confiable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# governance

**Contexto del dominio:** Traduce obligaciones y apetito de riesgo a responsables, controles, evidencias, excepciones y decisiones auditables.
## 1. regulación colombiana y sectorial aplicable

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Traduce obligaciones y apetito de riesgo a responsables, controles, evidencias, excepciones y decisiones auditables.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. riesgo de terceros, concentración y cadena de suministro

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Traduce obligaciones y apetito de riesgo a responsables, controles, evidencias, excepciones y decisiones auditables.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. métricas cuantitativas, apetito y riesgo residual

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Traduce obligaciones y apetito de riesgo a responsables, controles, evidencias, excepciones y decisiones auditables.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. gobierno de IA, privacidad y uso responsable

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Traduce obligaciones y apetito de riesgo a responsables, controles, evidencias, excepciones y decisiones auditables.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# vuln_management

**Contexto del dominio:** Prioriza exposición explotable según activo, KEV, EPSS, CVSS, reachability, controles y rutas de ataque.
## 1. exposure management y attack surface externo

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza exposición explotable según activo, KEV, EPSS, CVSS, reachability, controles y rutas de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://www.first.org/epss/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. correlación KEV, EPSS, CVSS y contexto de activo

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza exposición explotable según activo, KEV, EPSS, CVSS, reachability, controles y rutas de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://www.first.org/epss/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. priorización por ruta de ataque y explotabilidad

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza exposición explotable según activo, KEV, EPSS, CVSS, reachability, controles y rutas de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://www.first.org/epss/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. gestión de excepciones, deuda y remediación verificable

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza exposición explotable según activo, KEV, EPSS, CVSS, reachability, controles y rutas de ataque.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://www.first.org/epss/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# bug_bounty

**Contexto del dominio:** Define autorización, alcance, safe harbor, límites de prueba, manejo de datos y divulgación coordinada.
## 1. VDP, safe harbor y coordinación legal

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define autorización, alcance, safe harbor, límites de prueba, manejo de datos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. triage reproducible y deduplicación de hallazgos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define autorización, alcance, safe harbor, límites de prueba, manejo de datos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. pruebas seguras de impacto sin exfiltración

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define autorización, alcance, safe harbor, límites de prueba, manejo de datos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. métricas de programa y divulgación coordinada

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define autorización, alcance, safe harbor, límites de prueba, manejo de datos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# secure_arch

**Contexto del dominio:** Define trust boundaries, identidades, flujos, blast radius, dependencias y modos de fallo; valida propiedades con pruebas.
## 1. arquitectura cloud-native Zero Trust

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define trust boundaries, identidades, flujos, blast radius, dependencias y modos de fallo; valida propiedades con pruebas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. resiliencia, degradación segura y blast-radius control

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define trust boundaries, identidades, flujos, blast radius, dependencias y modos de fallo; valida propiedades con pruebas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. arquitectura multi-tenant y separación de datos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define trust boundaries, identidades, flujos, blast radius, dependencias y modos de fallo; valida propiedades con pruebas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. seguridad de APIs internas, service mesh y supply chain

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define trust boundaries, identidades, flujos, blast radius, dependencias y modos de fallo; valida propiedades con pruebas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# data_security

**Contexto del dominio:** Protege datos y derivados mediante clasificación, minimización, acceso, lineage, retención, cifrado y borrado verificable.
## 1. DSPM, clasificación automatizada y data lineage

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege datos y derivados mediante clasificación, minimización, acceso, lineage, retención, cifrado y borrado verificable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. confidential computing y protección de datos en uso

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege datos y derivados mediante clasificación, minimización, acceso, lineage, retención, cifrado y borrado verificable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. privacidad-preserving analytics y aprendizaje

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege datos y derivados mediante clasificación, minimización, acceso, lineage, retención, cifrado y borrado verificable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. borrado verificable, retención y gobernanza de backups

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege datos y derivados mediante clasificación, minimización, acceso, lineage, retención, cifrado y borrado verificable.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# software_engineering

**Contexto del dominio:** Integra seguridad en requisitos, diseño, código, revisión, pruebas, build, release y mantenimiento.
## 1. memory safety y lenguajes seguros

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Integra seguridad en requisitos, diseño, código, revisión, pruebas, build, release y mantenimiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. concurrencia, race conditions y seguridad de runtime

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Integra seguridad en requisitos, diseño, código, revisión, pruebas, build, release y mantenimiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. reproducible builds y provenance de dependencias

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Integra seguridad en requisitos, diseño, código, revisión, pruebas, build, release y mantenimiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. fuzzing, property-based testing y verificación

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Integra seguridad en requisitos, diseño, código, revisión, pruebas, build, release y mantenimiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# machine_learning

**Contexto del dominio:** Evalúa datos, etiquetas, features, entrenamiento, pesos, inferencia y feedback; separa robustez, privacidad y seguridad.
## 1. adversarial ML, poisoning y backdoors

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa datos, etiquetas, features, entrenamiento, pesos, inferencia y feedback; separa robustez, privacidad y seguridad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. privacy leakage, membership inference y extracción

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa datos, etiquetas, features, entrenamiento, pesos, inferencia y feedback; separa robustez, privacidad y seguridad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. model evaluation, calibration y uncertainty

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa datos, etiquetas, features, entrenamiento, pesos, inferencia y feedback; separa robustez, privacidad y seguridad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. MLOps, model registry y procedencia de datasets

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa datos, etiquetas, features, entrenamiento, pesos, inferencia y feedback; separa robustez, privacidad y seguridad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# hardware_security

**Contexto del dominio:** Incluye amenazas físicas, supply chain, arranque, firmware, microarquitectura, side-channel, debug y actualización.
## 1. silicon assurance y cadena de fabricación

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye amenazas físicas, supply chain, arranque, firmware, microarquitectura, side-channel, debug y actualización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. fault injection y side-channel avanzado

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye amenazas físicas, supply chain, arranque, firmware, microarquitectura, side-channel, debug y actualización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. attestation, TEE y confidential computing

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye amenazas físicas, supply chain, arranque, firmware, microarquitectura, side-channel, debug y actualización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. firmware lifecycle y recuperación de root of trust

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye amenazas físicas, supply chain, arranque, firmware, microarquitectura, side-channel, debug y actualización.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# mathematics

**Contexto del dominio:** Declara supuestos, distribuciones, unidades, incertidumbre y límites; no confundas correlación con causalidad.
## 1. estadística bayesiana y calibración de confianza

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Declara supuestos, distribuciones, unidades, incertidumbre y límites; no confundas correlación con causalidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. optimización robusta y detección de anomalías

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Declara supuestos, distribuciones, unidades, incertidumbre y límites; no confundas correlación con causalidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. teoría de información aplicada a privacidad

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Declara supuestos, distribuciones, unidades, incertidumbre y límites; no confundas correlación con causalidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. métodos formales y pruebas criptográficas

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Declara supuestos, distribuciones, unidades, incertidumbre y límites; no confundas correlación con causalidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# soc_siem

**Contexto del dominio:** Una detección requiere hipótesis, datos, lógica versionada, evaluación, owner y respuesta; mide cobertura real de telemetría.
## 1. ATT&CK Detection Strategies y Analytics versionados

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Una detección requiere hipótesis, datos, lógica versionada, evaluación, owner y respuesta; mide cobertura real de telemetría.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. detección de secuencias y causalidad temporal

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Una detección requiere hipótesis, datos, lógica versionada, evaluación, owner y respuesta; mide cobertura real de telemetría.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. calidad, cobertura y drift de telemetría

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Una detección requiere hipótesis, datos, lógica versionada, evaluación, owner y respuesta; mide cobertura real de telemetría.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. evaluación estadística de reglas y playbooks

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Una detección requiere hipótesis, datos, lógica versionada, evaluación, owner y respuesta; mide cobertura real de telemetría.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://attack.mitre.org/
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# edr_xdr

**Contexto del dominio:** Correlaciona endpoint, identidad, red y cloud considerando integridad del sensor y latencia.
## 1. telemetría kernel y eBPF multiplataforma

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Correlaciona endpoint, identidad, red y cloud considerando integridad del sensor y latencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. detección de identidad, SaaS y cloud workloads

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Correlaciona endpoint, identidad, red y cloud considerando integridad del sensor y latencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. resistencia a tampering y gaps de sensor

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Correlaciona endpoint, identidad, red y cloud considerando integridad del sensor y latencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. aislamiento reversible y recuperación del endpoint

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Correlaciona endpoint, identidad, red y cloud considerando integridad del sensor y latencia.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# threat_hunting

**Contexto del dominio:** Formula hipótesis falsables, base rate, fuentes, ventana y criterios de refutación; documenta búsquedas negativas.
## 1. hipótesis falsables y análisis de base rates

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Formula hipótesis falsables, base rate, fuentes, ventana y criterios de refutación; documenta búsquedas negativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. detección por comportamiento y cadenas de eventos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Formula hipótesis falsables, base rate, fuentes, ventana y criterios de refutación; documenta búsquedas negativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. ATT&CK analytics y data components actuales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Formula hipótesis falsables, base rate, fuentes, ventana y criterios de refutación; documenta búsquedas negativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. reproducibilidad y medición de valor del hunt

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Formula hipótesis falsables, base rate, fuentes, ventana y criterios de refutación; documenta búsquedas negativas.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# red_team

**Contexto del dominio:** Exige autorización, scope, ventana, deconfliction, límites, reglas de parada y canal de escalamiento.
## 1. adversary emulation con ATT&CK versionado

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Exige autorización, scope, ventana, deconfliction, límites, reglas de parada y canal de escalamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. cloud, SaaS e identidad como superficies prioritarias

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Exige autorización, scope, ventana, deconfliction, límites, reglas de parada y canal de escalamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. purple teaming y validación de detecciones

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Exige autorización, scope, ventana, deconfliction, límites, reglas de parada y canal de escalamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. seguridad operacional, deconfliction y límites

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Exige autorización, scope, ventana, deconfliction, límites, reglas de parada y canal de escalamiento.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# wireless_security

**Contexto del dominio:** Modela medio compartido, identidad, cifrado, roaming, gestión, interferencia y dispositivos invitados/IoT.
## 1. WPA3 Enterprise, 802.1X y roaming seguro

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela medio compartido, identidad, cifrado, roaming, gestión, interferencia y dispositivos invitados/IoT.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. Bluetooth LE privacy y seguridad GATT

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela medio compartido, identidad, cifrado, roaming, gestión, interferencia y dispositivos invitados/IoT.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. SDR, espectro y pruebas de radio autorizadas

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela medio compartido, identidad, cifrado, roaming, gestión, interferencia y dispositivos invitados/IoT.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. Wi-Fi 6E/7 y segmentación de IoT

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Modela medio compartido, identidad, cifrado, roaming, gestión, interferencia y dispositivos invitados/IoT.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# ot_ics

**Contexto del dominio:** Prioriza safety y disponibilidad; comienza con inventario y observación pasiva, valida en simulador y coordina con operador.
## 1. IEC 62443 ciclo de vida y zonas/conduits

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza safety y disponibilidad; comienza con inventario y observación pasiva, valida en simulador y coordina con operador.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/resources-tools/resources/ics-recommended-practices
- https://www.nist.gov/publications/guide-industrial-control-systems-ics-security

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. safety-security co-engineering y análisis de consecuencias

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza safety y disponibilidad; comienza con inventario y observación pasiva, valida en simulador y coordina con operador.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/resources-tools/resources/ics-recommended-practices
- https://www.nist.gov/publications/guide-industrial-control-systems-ics-security

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. remote access, vendor access y control de cambios

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza safety y disponibilidad; comienza con inventario y observación pasiva, valida en simulador y coordina con operador.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/resources-tools/resources/ics-recommended-practices
- https://www.nist.gov/publications/guide-industrial-control-systems-ics-security

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. detección pasiva y recuperación de lógica/firmware

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza safety y disponibilidad; comienza con inventario y observación pasiva, valida en simulador y coordina con operador.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/resources-tools/resources/ics-recommended-practices
- https://www.nist.gov/publications/guide-industrial-control-systems-ics-security

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# telecom_5g

**Contexto del dominio:** Incluye RAN, core, SBA, roaming, slicing, edge, SIM/eSIM, señalización y proveedores.
## 1. Open RAN y seguridad de interfaces

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye RAN, core, SBA, roaming, slicing, edge, SIM/eSIM, señalización y proveedores.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. 5G SBA, APIs y service-based identity

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye RAN, core, SBA, roaming, slicing, edge, SIM/eSIM, señalización y proveedores.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. slicing, roaming y aislamiento entre tenants

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye RAN, core, SBA, roaming, slicing, edge, SIM/eSIM, señalización y proveedores.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. eSIM, supply chain y edge/MEC

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye RAN, core, SBA, roaming, slicing, edge, SIM/eSIM, señalización y proveedores.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# automotive_security

**Contexto del dominio:** Conecta ECU, bus, gateway, telemática, backend, OTA y taller; considera safety y ciclo de vida prolongado.
## 1. UNECE R155/R156 y CSMS/SUMS

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Conecta ECU, bus, gateway, telemática, backend, OTA y taller; considera safety y ciclo de vida prolongado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. CAN-FD, Automotive Ethernet y gateways zonales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Conecta ECU, bus, gateway, telemática, backend, OTA y taller; considera safety y ciclo de vida prolongado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. V2X, telemática y backend cloud

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Conecta ECU, bus, gateway, telemática, backend, OTA y taller; considera safety y ciclo de vida prolongado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. OTA, HIL/SIL y análisis de seguridad funcional

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Conecta ECU, bus, gateway, telemática, backend, OTA y taller; considera safety y ciclo de vida prolongado.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# satellite_security

**Contexto del dominio:** Incluye segmento espacial, estaciones terrestres, TT&C, enlaces, GNSS, claves y cadena de mando.
## 1. ground segment, TT&C y cadena de mando

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye segmento espacial, estaciones terrestres, TT&C, enlaces, GNSS, claves y cadena de mando.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. GNSS spoofing/jamming y resiliencia de navegación

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye segmento espacial, estaciones terrestres, TT&C, enlaces, GNSS, claves y cadena de mando.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. RF links, key management y anti-replay

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye segmento espacial, estaciones terrestres, TT&C, enlaces, GNSS, claves y cadena de mando.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. supply chain y operaciones de constelaciones

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Incluye segmento espacial, estaciones terrestres, TT&C, enlaces, GNSS, claves y cadena de mando.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# physical_security

**Contexto del dominio:** Analiza controladores, credenciales, redes de edificios, cámaras, puertas, energía y convergencia con identidad.
## 1. convergencia de identidad física y lógica

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza controladores, credenciales, redes de edificios, cámaras, puertas, energía y convergencia con identidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. controladores de acceso, firmware y redes de edificios

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza controladores, credenciales, redes de edificios, cámaras, puertas, energía y convergencia con identidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. CCTV/IoT, privacidad y retención de evidencia

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza controladores, credenciales, redes de edificios, cámaras, puertas, energía y convergencia con identidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. amenazas internas y respuesta ciberfísica

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Analiza controladores, credenciales, redes de edificios, cámaras, puertas, energía y convergencia con identidad.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# email_dns_security

**Contexto del dominio:** Evalúa dominio, DNS, MTA, autenticación, alineación, transporte y flujo de recepción.
## 1. DMARC alignment, reporting y operación de políticas

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa dominio, DNS, MTA, autenticación, alineación, transporte y flujo de recepción.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. MTA-STS, DANE, TLS-RPT y downgrade

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa dominio, DNS, MTA, autenticación, alineación, transporte y flujo de recepción.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. BIMI, ARC y ecosistema de autenticación de correo

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa dominio, DNS, MTA, autenticación, alineación, transporte y flujo de recepción.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. DNS registrar security, DNSSEC y account takeover

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa dominio, DNS, MTA, autenticación, alineación, transporte y flujo de recepción.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# fraud_abuse

**Contexto del dominio:** Combina señales de cuenta, dispositivo, transacción, grafo y comportamiento; controla falsos positivos, sesgos y apelaciones.
## 1. identidad sintética y señales de dispositivo

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Combina señales de cuenta, dispositivo, transacción, grafo y comportamiento; controla falsos positivos, sesgos y apelaciones.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. detección de bots y fricción adaptativa

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Combina señales de cuenta, dispositivo, transacción, grafo y comportamiento; controla falsos positivos, sesgos y apelaciones.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. grafos de fraude y análisis temporal

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Combina señales de cuenta, dispositivo, transacción, grafo y comportamiento; controla falsos positivos, sesgos y apelaciones.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. apelación, fairness y medición de falsos positivos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Combina señales de cuenta, dispositivo, transacción, grafo y comportamiento; controla falsos positivos, sesgos y apelaciones.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# privacy_engineering

**Contexto del dominio:** Define propósito, base legal, minimización, sujetos, flujos, terceros, retención, derechos y reidentificación.
## 1. DPIA/PIA y evaluación de riesgo de reidentificación

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define propósito, base legal, minimización, sujetos, flujos, terceros, retención, derechos y reidentificación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define variables, población, horizonte y unidad de análisis; declara supuestos, incertidumbre, sensibilidad y sesgos. Compara contra línea base y no interpretes una escala ordinal como probabilidad calibrada. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/privacy-framework
- https://www.edpb.europa.eu/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. PETs: differential privacy, MPC y federated learning

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define propósito, base legal, minimización, sujetos, flujos, terceros, retención, derechos y reidentificación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/privacy-framework
- https://www.edpb.europa.eu/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. gobierno de SDKs, telemetría y terceros

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define propósito, base legal, minimización, sujetos, flujos, terceros, retención, derechos y reidentificación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/privacy-framework
- https://www.edpb.europa.eu/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. retención, derechos y borrado verificable

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Define propósito, base legal, minimización, sujetos, flujos, terceros, retención, derechos y reidentificación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/privacy-framework
- https://www.edpb.europa.eu/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# cloud_forensics

**Contexto del dominio:** Obtén logs y snapshots por API con permisos y retención documentados; planifica evidencia efímera y residencia regional.
## 1. evidencia de control plane y auditoría cloud

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Obtén logs y snapshots por API con permisos y retención documentados; planifica evidencia efímera y residencia regional.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. serverless, containers y evidencia efímera

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Obtén logs y snapshots por API con permisos y retención documentados; planifica evidencia efímera y residencia regional.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. snapshots, object lock y cadena de custodia

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Obtén logs y snapshots por API con permisos y retención documentados; planifica evidencia efímera y residencia regional.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Documenta protocolo, actores, estados, trust boundaries, validación, autorización y límites. Prueba degradación, mensajes malformados, replay, estados fuera de orden y fallos de dependencia en entorno autorizado. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. correlación multi-cloud, SaaS e identidad

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Obtén logs y snapshots por API con permisos y retención documentados; planifica evidencia efímera y residencia regional.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# ai_red_team

**Contexto del dominio:** Prueba prompts, retrieval, memoria, herramientas, identidad y multimodalidad con datos sintéticos y límites seguros.
## 1. ataques multimodales y prompt injection indirecta

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prueba prompts, retrieval, memoria, herramientas, identidad y multimodalidad con datos sintéticos y límites seguros.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. tool abuse, excessive agency y autorización

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prueba prompts, retrieval, memoria, herramientas, identidad y multimodalidad con datos sintéticos y límites seguros.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. RAG poisoning, memory poisoning y cross-tenant

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prueba prompts, retrieval, memoria, herramientas, identidad y multimodalidad con datos sintéticos y límites seguros.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. evaluación de agentes, costes y recuperación

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prueba prompts, retrieval, memoria, herramientas, identidad y multimodalidad con datos sintéticos y límites seguros.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# pki_hsm

**Contexto del dominio:** Protege ciclo de vida de claves, roles, ceremonia, quorum, backup, rotación, revocación y recuperación.
## 1. ACME, CT logs y automatización de certificados

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege ciclo de vida de claves, roles, ceremonia, quorum, backup, rotación, revocación y recuperación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. ceremonias de claves, quorum y recuperación HSM

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege ciclo de vida de claves, roles, ceremonia, quorum, backup, rotación, revocación y recuperación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. CA compromise, revocation y trust store governance

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege ciclo de vida de claves, roles, ceremonia, quorum, backup, rotación, revocación y recuperación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. PQC certificates y crypto-agility

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Protege ciclo de vida de claves, roles, ceremonia, quorum, backup, rotación, revocación y recuperación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Separa sujeto, credencial, autenticador, issuer, audience, autorización y sesión. Verifica binding, expiración, rotación, revocación, replay y recuperación; evita secretos persistentes y privilegios compartidos. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# post_quantum_crypto

**Contexto del dominio:** Prioriza inventario, sensibilidad temporal, HNDL, agilidad, compatibilidad y migración por riesgo.
## 1. NIST IR 8547 y hoja de ruta de transición

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza inventario, sensibilidad temporal, HNDL, agilidad, compatibilidad y migración por riesgo.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.IR.8547
- https://doi.org/10.6028/NIST.FIPS.203

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. inventario criptográfico y clasificación HNDL

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza inventario, sensibilidad temporal, HNDL, agilidad, compatibilidad y migración por riesgo.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.IR.8547
- https://doi.org/10.6028/NIST.FIPS.203

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. interoperabilidad híbrida, rendimiento y fallback

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza inventario, sensibilidad temporal, HNDL, agilidad, compatibilidad y migración por riesgo.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.IR.8547
- https://doi.org/10.6028/NIST.FIPS.203

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. gobierno de algoritmos heredados y fechas de retiro

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Prioriza inventario, sensibilidad temporal, HNDL, agilidad, compatibilidad y migración por riesgo.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://doi.org/10.6028/NIST.IR.8547
- https://doi.org/10.6028/NIST.FIPS.203

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# business_continuity

**Contexto del dominio:** La recuperación cuenta solo tras restaurar en entorno limpio y validar identidades, datos, dependencias y aceptación.
## 1. ransomware recovery y clean-room restoration

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La recuperación cuenta solo tras restaurar en entorno limpio y validar identidades, datos, dependencias y aceptación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Define hipótesis, fuentes, campos, normalización, ventana temporal y calidad de eventos. Prueba positivos, negativos y benignos parecidos; mide precisión, recall estimado, falsos positivos, latencia y cobertura. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/stopransomware
- https://doi.org/10.6028/NIST.SP.800-34r1

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. validación de backups inmutables y credenciales

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La recuperación cuenta solo tras restaurar en entorno limpio y validar identidades, datos, dependencias y aceptación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/stopransomware
- https://doi.org/10.6028/NIST.SP.800-34r1

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. dependencia de proveedores y continuidad SaaS

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La recuperación cuenta solo tras restaurar en entorno limpio y validar identidades, datos, dependencias y aceptación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/stopransomware
- https://doi.org/10.6028/NIST.SP.800-34r1

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. crisis exercises y recuperación de procesos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. La recuperación cuenta solo tras restaurar en entorno limpio y validar identidades, datos, dependencias y aceptación.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.cisa.gov/stopransomware
- https://doi.org/10.6028/NIST.SP.800-34r1

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# database_security

**Contexto del dominio:** Evalúa motor, roles, extensiones, consultas, copias, replicación, caches y vectores; prueba aislamiento también en analytics.
## 1. vector databases y controles de acceso por fila/tenant

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa motor, roles, extensiones, consultas, copias, replicación, caches y vectores; prueba aislamiento también en analytics.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. cloud-managed databases y control plane

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa motor, roles, extensiones, consultas, copias, replicación, caches y vectores; prueba aislamiento también en analytics.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. auditoría, query abuse y detección de exfiltración

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa motor, roles, extensiones, consultas, copias, replicación, caches y vectores; prueba aislamiento también en analytics.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. backup encryption, restore testing y secretos

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Evalúa motor, roles, extensiones, consultas, copias, replicación, caches y vectores; prueba aislamiento también en analytics.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.



# vulnerability_research

**Contexto del dominio:** Usa hipótesis, entorno reproducible, sanitizers/fuzzing, reducción de casos y divulgación coordinada.
## 1. fuzzing coverage-guided y corpus minimization

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa hipótesis, entorno reproducible, sanitizers/fuzzing, reducción de casos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 2. memory corruption, sanitizers y exploitability

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa hipótesis, entorno reproducible, sanitizers/fuzzing, reducción de casos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Clasifica datos y derivados, define propósito, tenant, owner, retención y permisos. Evalúa filtración, envenenamiento, inferencia y reidentificación; incluye segregación, auditoría y borrado verificable. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 3. coordinated disclosure y gestión de CVE

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa hipótesis, entorno reproducible, sanitizers/fuzzing, reducción de casos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Especifica entradas, estados, invariantes, dependencias y resultados esperados. Construye casos nominales, negativos, límite y fallo; registra condiciones de carrera, bypass y degradación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

## 4. supply-chain vulnerabilities y análisis de dependencias

### Propósito y alcance
El módulo define qué propiedad técnica debe protegerse, qué activos y procesos cubre, qué queda fuera y qué evidencia permitiría demostrar el resultado. Usa hipótesis, entorno reproducible, sanitizers/fuzzing, reducción de casos y divulgación coordinada.

### Arquitectura y modelo de amenazas
Descompón actores, activos, interfaces, estados, flujos, dependencias y autoridades. Marca trust boundaries y puntos de autenticación, autorización, transformación, almacenamiento y exportación. Considera abuso de privilegios, manipulación de estado, entrada no confiable, replay, exposición lateral, dependencia comprometida, mala configuración y pérdida de telemetría. Para cada escenario registra precondiciones, capacidad del adversario, impacto, señales y supuestos; no infieras atribución sin evidencia.

### Desarrollo técnico y controles
Inventaría componentes, identidades de workload, permisos efectivos, artefactos, dependencias y rutas administrativas. Verifica provenance, restringe egress, fija versiones y ensaya actualización, rollback y recuperación. Aplica mínimo privilegio, separación de funciones, validación en el componente de confianza, límites de recursos, segmentación, gestión de secretos, logging resistente a manipulación y recuperación probada. Cada control requiere owner, alcance, modo de fallo, evidencia y excepción con vencimiento. Un gateway, escáner o agente no sustituye la decisión de autorización en el componente dueño del recurso.

### Procedimiento reproducible
1. Inventariar activos, versiones y dependencias.
2. Establecer línea base y supuestos.
3. Formular una hipótesis falsable y casos de abuso.
4. Ejecutar pruebas en staging, simulador o entorno aislado con datos sintéticos.
5. Capturar configuración, logs, hashes y resultados.
6. Corregir causa raíz y repetir pruebas de regresión.
7. Registrar owner, fecha, limitaciones y criterio de salida.

### Laboratorio y evaluación
Crear un entorno aislado con componentes mock que represente el flujo esencial. Incluir caso nominal, abuso, límite, dependencia no disponible y prueba negativa que demuestre bloqueo. No usar datos personales ni sistemas de terceros. Definir precondiciones, snapshots, limpieza y reglas de parada. Medir cobertura, tasa de casos detectados, falsos positivos/negativos, latencia, impacto operativo y reproducibilidad, usando solo métricas pertinentes y fijando umbrales antes del ensayo.

### Evidencia y limitaciones
Conservar diseño, configuración, scripts, datos sintéticos, hashes, logs, resultados y decisión. El estado de este módulo es desarrollo documental inicial: no acredita laboratorio ejecutado, exactitud exhaustiva ni revisión independiente. Para declararlo validado se requiere trazabilidad de afirmaciones a secciones concretas de fuentes primarias, resultados reproducibles, pruebas negativas y revisión por otra persona.

### Fuentes de partida
- https://www.nist.gov/cyberframework
- https://www.cisa.gov/resources-tools

**Estado de las fuentes:** referencias de contexto para lectura y contraste; no se afirma que respalden línea por línea este módulo.

