# Agenda de investigación: Redes

**Dominio:** `network` · **Nivel objetivo:** L4 investigación · **Madurez actual:** agenda propuesta, no investigación concluida.

## Problema de investigación

Investigar protocolos, segmentación, detección, rendimiento y resistencia a fallos en el contexto de Redes. La agenda identifica líneas de trabajo a partir del currículo del dominio; no afirma resultados empíricos ni sustituye una revisión sistemática de literatura.

## Pregunta central

¿Qué enfoques técnicos ofrecen la mejor combinación demostrable de seguridad, resiliencia, rendimiento, coste y operabilidad para Redes, bajo amenazas, arquitecturas y restricciones explícitas?

## Líneas de investigación por tema

### T1. OSI/TCP-IP, routing y switching

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *OSI/TCP-IP, routing y switching* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T2. VLAN, VRF, microsegmentación y Zero Trust

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *VLAN, VRF, microsegmentación y Zero Trust* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T3. firewalls, ACL, NAT y egress

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *firewalls, ACL, NAT y egress* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T4. DNS, DHCP, NTP, VPN, TLS e IPsec

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *DNS, DHCP, NTP, VPN, TLS e IPsec* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T5. Wi-Fi empresarial y control de acceso

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *Wi-Fi empresarial y control de acceso* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T6. PCAP, NetFlow, Zeek y detección

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *PCAP, NetFlow, Zeek y detección* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

### T7. resiliencia y gestión fuera de banda

**Pregunta de investigación:** ¿Qué propiedades de seguridad, fiabilidad y observabilidad de *resiliencia y gestión fuera de banda* dependen de la arquitectura y configuración, y cómo se pueden medir de forma reproducible?

**Hipótesis de trabajo:** un diseño/configuración con controles explícitos y verificables mejora la métrica de seguridad definida frente a una línea base sin dichos controles, con un coste medible en rendimiento, complejidad o usabilidad. La hipótesis debe ser reformulada y falsable tras revisar literatura específica.

**Diseño propuesto:** definir sistema/población y versión; documentar baseline; variar una dimensión por experimento; mantener constantes factores de confusión; usar casos positivos, negativos y límite; repetir pruebas; registrar logs y artefactos con hashes; aplicar análisis estadístico apropiado.

**Métricas candidatas:** eficacia del control, cobertura, tasa de error/falsos positivos, latencia/coste, reproducibilidad y degradación ante cambios. Elegir solo métricas pertinentes y justificar la operacionalización.

**Resultado exigido:** mapa de literatura, taxonomía, protocolo, datos sintéticos/autorizados, resultados, intervalos de incertidumbre, amenazas a validez, limitaciones y artefactos para replicación.

## Método transversal

1. Formular pregunta delimitada, alcance, hipótesis falsable y criterios de refutación.
2. Ejecutar búsqueda bibliográfica reproducible: repositorios académicos, normas, advisories y documentación primaria; registrar términos, bases, fecha y criterios de selección.
3. Clasificar evidencia por tipo, autoridad, actualidad, método, sesgo y reproducibilidad.
4. Sintetizar estado del arte, taxonomía, desacuerdos, limitaciones y brecha de conocimiento.
5. Diseñar experimento con baseline, comparadores, variables, muestras, versiones, repeticiones y métricas justificadas.
6. Ejecutar solo en laboratorio aislado o activos autorizados; preservar cadena de custodia y minimización de datos.
7. Analizar resultados, intervalos de confianza cuando proceda, falsos positivos/negativos y amenazas a validez.
8. Publicar artefactos, configuración, dependencias, hashes, datos permitidos y procedimiento de reproducción.
9. Solicitar revisión técnica independiente y reproducción por otro operador antes de declarar M5.

## Entregables de investigación

- Revisión de literatura con estrategia y tabla de evidencia.
- Estado del arte y taxonomía comparativa.
- Preguntas, hipótesis, variables y protocolo pre-registrado cuando sea viable.
- Arquitectura del experimento, threat model y análisis de riesgos.
- Dataset sintético o autorizado, diccionario de datos y procedencia.
- Código, configuración, dependencias fijadas, SBOM y hashes.
- Resultados brutos saneados, análisis, gráficos/tablas y scripts.
- Discusión, limitaciones, amenazas a validez y trabajo futuro.
- Revisión independiente y registro de reproducción.

## Seguridad y ética

Autorización escrita para toda evaluación activa; alcance, exclusiones, límites de impacto y kill switch. No probar infraestructura de terceros, sistemas críticos ni dispositivos físicos en producción. En OT, automoción, satélites y hardware, usar simuladores o bancos de prueba. No publicar secretos, datos personales ni artefactos peligrosos sin saneamiento y revisión.

## Estado editorial

`research_agenda_defined` — preguntas y diseño inicial propuestos. No equivale a estado del arte terminado, paper reproducido ni resultado validado. Para avanzar a M4 se requiere literatura revisada, experimento ejecutado y análisis; M5 requiere revisión y reproducción externa.


## Protocolos de investigación específicos y falsables

### RQ-NET-01 — Efectividad real de la segmentación
**Pregunta:** ¿Cuánto reduce una política basada en identidad y contexto la reachability no autorizada frente a VLAN/ACL tradicionales en una topología virtual equivalente?
**H1:** la política granular reduce destinos no autorizados alcanzables sin superar el umbral de latencia/operación predefinido.
**Variables:** tipo de política (independiente); reachability prohibida, latencia p95, número de excepciones y tasa de fallos de cambio (dependientes).
**Controles:** topología, carga, servicios, rutas, versión de software y matriz de flujos.
**Diseño:** comparar baseline y tratamiento en laboratorio virtual; ejecutar conjunto fijo de pruebas permitidas/prohibidas y repetir con cambios de identidad.
**Validez:** la topología no representa redes heterogéneas; las métricas de reachability no miden por sí solas compromiso o impacto.

### RQ-NET-02 — Calidad de reglas de firewall
**Pregunta:** ¿La revisión automatizada de shadowing, redundancia, permisos excesivos y falta de propietario reduce errores de política frente a revisión manual?
**H1:** la combinación automatización + revisión humana encuentra más defectos confirmados que revisión manual sola, con tasa de falsos positivos aceptable.
**Diseño:** corpus sintético de reglas con defectos etiquetados; evaluación ciega, baseline manual y herramienta; medir precision, recall, F1 y tiempo.
**Controles:** mismos casos, criterios de etiquetado, versiones y experiencia de revisores.

### RQ-NET-03 — Cobertura y calidad de telemetría
**Pregunta:** ¿Qué combinación de PCAP, NetFlow/IPFIX, DNS y logs de firewall ofrece mejor detección por coste en escenarios etiquetados?
**H1:** la fusión de fuentes mejora recall respecto a una fuente aislada, pero puede elevar coste y falsos positivos.
**Diseño:** replay offline de tráfico sintético etiquetado; medir precision/recall, bytes almacenados, pérdida, latencia y carga de procesamiento.
**Controles:** reloj sincronizado, mismos escenarios, reglas congeladas y dataset versionado.

### RQ-NET-04 — Resiliencia de DNS y servicios de infraestructura
**Pregunta:** ¿Qué configuraciones reducen fallos de resolución y exposición a manipulación sin degradar disponibilidad?
**Diseño:** emular resolver primario/secundario, cambios de zona, expiración de caché, DNSSEC validación y fallos de upstream; medir disponibilidad, latencia y detección.
**Límite:** no extrapolar a resolvers públicos o redes de producción sin validación externa.

### RQ-NET-05 — VPN, mTLS y segmentación posterior a autenticación
**Pregunta:** ¿La identidad de dispositivo/servicio y la autorización contextual limitan mejor el acceso lateral que la pertenencia a una VPN?
**Diseño:** servicios sintéticos, certificados de prueba, identidades con roles distintos, expiración/revocación y rutas controladas; verificar acceso permitido/denegado y tiempo de revocación.
**Seguridad:** claves efímeras de laboratorio; no usar credenciales reales.

### RQ-NET-06 — Fallos de control y modos fail-open/fail-closed
**Pregunta:** ¿Qué comportamiento ante caída de firewall, sensor, controlador SDN o servidor NAC conserva el equilibrio más seguro entre disponibilidad y contención?
**Diseño:** inyección de fallos en emulador aislado; medir tráfico permitido indebidamente, indisponibilidad, tiempo de recuperación y pérdida de evidencia.
**Criterio de parada:** cualquier salida de la red virtual, impacto no previsto o pérdida de control del entorno.

Cada protocolo requiere preregistro, muestra/escenarios definidos, baseline, repetición, análisis de incertidumbre, resultados negativos, artefactos y revisión antes de elevar madurez.
