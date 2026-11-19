# Agenda de investigación: seguridad de APIs

**Dominio:** `api` · **Objetivo:** K5 investigación · **Estado:** hipótesis y protocolos propuestos; estudios no ejecutados.  
**Límite empírico:** no M3/M4/M5.

## Problema y estrategia de revisión

Las APIs se protegen con gateways, contratos, tokens y límites, pero su presencia no demuestra autorización contextual ni resistencia a abuso. La investigación debe medir resultados en entornos reproducibles y distinguir cumplimiento de especificación, implementación y eficacia.

Fuentes iniciales: OWASP API Security Top 10 2023, OWASP ASVS 5.0.0, IETF RFC 9700, OpenAPI Specification 3.2.1 y documentación gRPC Authentication. Se inspeccionaron páginas oficiales y partes de documentos; no se declara revisión sistemática ni lectura integral. Para estado del arte ampliar con IEEE Xplore, ACM Digital Library, USENIX, IETF RFCs y artículos revisados por pares. Guardar consultas, fecha, criterios de inclusión/exclusión y versiones.

## Línea 1 — Autorización multi-tenant y BOLA/BOPLA/BFLA

**Pregunta:** ¿Qué estrategia de generación de pruebas detecta más fallos de autorización con coste de ejecución y mantenimiento razonable?

- H1: matriz sujeto–acción–objeto–tenant y pruebas basadas en relaciones detectan más defectos sembrados que pruebas endpoint-centric.
- H0: no hay mejora relevante en recall o el coste adicional excede el umbral predefinido.
- Diseño: API local con dos o más tenants, roles, recursos propios/ajenos, operaciones de lectura/escritura/exportación y fallos sembrados.
- Variables: método de prueba; recall, precision, cobertura combinatoria, defectos escapados, tiempo de ejecución/triage.
- Controles: mismos endpoints, fixtures, versiones, orden aleatorizado y ground truth revisado por dos evaluadores.
- Amenaza: fallos sembrados pueden favorecer el enfoque relacional; publicar corpus y limitaciones.

## Línea 2 — Seguridad de flujos OAuth y tokens

**Pregunta:** ¿Qué errores de implementación OAuth se detectan con pruebas basadas en RFC 9700 frente a validaciones de conformidad superficiales?

- H1: un conjunto de pruebas de protocolo con PKCE, state, nonce, redirect exacta, issuer y audience detecta más errores críticos que pruebas de login funcional.
- H0: no existe diferencia material bajo el protocolo.
- Diseño: authorization server y clientes sintéticos; inyectar errores de configuración y token controlados.
- Variables: clase de fallo; tasa de detección, falsos positivos, tiempo y compatibilidad.
- Controles: mismo issuer, clock, claves, clientes y versiones.
- Amenaza: entorno de referencia no representa proveedores comerciales ni federaciones complejas.

## Línea 3 — Rate limiting y equidad

**Pregunta:** ¿Qué algoritmo y clave de partición ofrece mejor equilibrio entre protección, latencia y equidad multi-tenant?

- H1: token bucket por tenant+identidad+coste ofrece control de ráfagas y menor bloqueo de usuarios legítimos que límites globales o por IP.
- H0: no mejora equidad o añade inconsistencia distribuida inaceptable.
- Diseño: simulador local con fixed window, sliding window y token bucket; carga sintética reproducible.
- Métricas: requests admitidas/rechazadas, falsos bloqueos, latencia p95/p99, throughput, equidad y recuperación tras burst.
- Controles: carga idéntica, reloj fijo, número de workers y política de coste.
- Amenaza: el simulador no representa todos los patrones de red ni fallos de almacenamiento distribuido.

## Línea 4 — Contrato vs implementación

**Pregunta:** ¿Qué clases de defectos se correlacionan con divergencias entre OpenAPI y el comportamiento observado?

- H1: validación continua de contrato más pruebas negativas reduce regresiones de esquema y exposición de propiedades.
- H0: no reduce defectos escapados frente a tests funcionales.
- Diseño: versiones congeladas de contrato/servicio y cambios deliberadamente compatibles/incompatibles.
- Métricas: divergencias detectadas, cobertura de operaciones, cambios rotos, falsos positivos y tiempo.
- Controles: misma versión de servicio, fixtures y reglas de compatibilidad.
- Amenaza: la validez del contrato depende de su calidad y actualización.

## Línea 5 — Webhooks, idempotencia y replay

**Pregunta:** ¿Qué combinación de firma, timestamp, deduplicación e idempotency keys previene replay sin descartar reintentos legítimos?

- H1: firma sobre cuerpo exacto + timestamp + event ID persistente reduce replay exitoso sin aumentar duplicados legítimos.
- H0: la combinación no mejora seguridad o provoca pérdida de eventos.
- Diseño: productor/receptor local con reintentos, duplicados, retrasos y firmas inválidas.
- Métricas: replay aceptado, evento legítimo perdido, efectos duplicados, latencia y recuperación.
- Controles: secuencia de eventos, ventana temporal y política de reintentos fijas.
- Amenaza: sistemas distribuidos reales presentan particiones y desorden más complejos.

## Línea 6 — Identidad de servicio y mTLS

**Pregunta:** ¿Qué diseño de identidad y autorización servicio-a-servicio minimiza bypass y complejidad operativa?

- H1: mTLS con identidad workload explícita más autorización por método/recurso reduce llamadas no autorizadas frente a TLS de servidor más confianza de red.
- H0: no mejora detección o el coste de emisión/rotación afecta disponibilidad por encima del umbral.
- Diseño: microservicios locales con certificados de prueba, expiración, rotación y políticas deliberadamente incompletas.
- Métricas: llamadas no autorizadas admitidas, fallos de rotación, latencia, tiempo de recuperación y bypass.
- Controles: CA de laboratorio, reloj, política, versiones y topología fijas.
- Amenaza: simulación no prueba todos los escenarios de service mesh/PKI empresarial.

## Protocolo común

Antes de ejecutar:
1. fijar hipótesis, outcomes primarios y plan de análisis;
2. registrar muestra, unidad de análisis, baseline y criterios de exclusión;
3. congelar commit, contratos, claves sintéticas, versiones, configuración y semillas;
4. separar desarrollo y evaluación para evitar fuga;
5. definir ground truth y resolver desacuerdos de etiquetado;
6. registrar resultados brutos, logs saneados, hashes y desviaciones;
7. reportar tamaños de efecto e incertidumbre, no solo promedios;
8. publicar resultados negativos y limitaciones;
9. solicitar revisión independiente y reproducción.

## Umbrales de madurez

- M1: páginas y abstracts identificados, agenda exploratoria.
- M2: lectura crítica y protocolo completo.
- M3: ejecución y análisis de datos trazables.
- M4: revisión independiente y reproducción equivalente.
- M5: réplica externa y contribución revisada.

**Estado actual M1; no M3/M4/M5.** Ninguna de las seis líneas se ha ejecutado.
