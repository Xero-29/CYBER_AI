# Compendio técnico: seguridad de APIs

**ID:** `api` · **Versión:** 2.1.0 · **Idioma:** español  
**Madurez editorial:** desarrollo técnico ampliado; no certificación experta ni investigación empírica concluida.  
**Ámbito:** APIs REST/HTTP, GraphQL, gRPC, OAuth/OIDC, tokens, gateways, service mesh, webhooks y contratos.

## 0. Propósito y resultados

Una API es una frontera de confianza y una interfaz de negocio. Protegerla requiere asegurar identidad, autorización, semántica, datos, disponibilidad, inventario, compatibilidad y dependencias. Un gateway, un JWT válido o un documento OpenAPI no prueban que cada operación sea segura.

El profesional o agente debe poder: modelar consumidores y proveedores; verificar autenticación y autorización por objeto/función/tenant; diseñar contratos; detectar exposición excesiva; controlar abuso y agotamiento; asegurar OAuth y tokens; revisar mTLS y confianza entre servicios; probar compatibilidad y regresiones; y documentar evidencia reproducible.

Todas las pruebas activas se limitan a APIs propias, laboratorios o activos con autorización escrita. Usar datos sintéticos, límites de tasa y criterios de parada.

## 1. Modelo de amenaza y arquitectura

Representar la cadena consumidor → DNS/TLS → gateway/WAF → autenticación → servicio → autorización → datos/colas → dependencias externas. Para cada salto registrar:
- identidad autenticada y método de prueba;
- identidad de workload y audiencia;
- autoridad y política aplicada;
- datos de entrada/salida y clasificación;
- tenant, propietario y relación de recurso;
- límites de tamaño, tiempo, concurrencia y coste;
- telemetría, correlación y manejo de errores;
- versión del contrato y responsable.

Los límites importantes no coinciden necesariamente con la red. Dos servicios dentro de una VPC pueden tener propietarios, permisos y niveles de confianza distintos. El gateway puede autenticar una llamada, pero el microservicio debe autorizar la acción sobre el recurso con contexto suficiente.

Amenazas API comunes:
- BOLA: acceso indebido a objetos;
- BOPLA: exposición o modificación de propiedades;
- BFLA: invocación de funciones fuera del permiso;
- autenticación rota y tokens mal validados;
- consumo ilimitado y operaciones de coste asimétrico;
- abuso de flujos de negocio;
- SSRF y confianza excesiva en integraciones;
- inventario incompleto, shadow APIs y versiones obsoletas;
- configuración insegura y consumo inseguro de APIs de terceros.

## 2. Contratos y semántica de protocolo

### 2.1 REST y HTTP

El contrato debe definir métodos, rutas, parámetros, esquemas, códigos de estado, autenticación, errores, límites y compatibilidad. Los métodos seguros/idempotentes tienen semántica HTTP: GET no debe cambiar estado; PUT/DELETE son idempotentes por definición semántica; POST no es automáticamente idempotente. No confiar en el nombre del método si la implementación viola esa semántica.

Controles:
- allowlist de métodos y tipos de contenido;
- límites de cuerpo, cabeceras, paginación y profundidad;
- parseo estricto y rechazo de campos desconocidos en operaciones sensibles;
- respuestas con allowlist de propiedades;
- errores normalizados sin stack trace, query interna o secreto;
- caché privada/no-store para respuestas sensibles según contexto;
- TLS con validación de certificado y hostname;
- timeouts y límites de conexión entre servicios.

### 2.2 OpenAPI

OpenAPI formaliza operaciones y esquemas, habilita generación de clientes y validación contractual. La especificación y sus esquemas deben fijarse por versión; el validador de esquema no garantiza detectar toda infracción del texto normativo ni contradicciones con la implementación. Mantener:
- contrato fuente bajo control de versiones;
- validación de diff y compatibilidad;
- securitySchemes y scopes explícitos;
- esquemas de request/response sin propiedades excesivas;
- ejemplos sintéticos y tests de contrato;
- revisión de divergencia entre contrato y servicio real.

No usar el documento como evidencia de autorización real: una descripción de scope no demuestra que cada endpoint aplique la política.

### 2.3 GraphQL

La superficie depende de schema, resolvers, directivas, batching y relaciones. Proteger:
- autorización en cada resolver/campo sensible, no solo en el endpoint;
- límites de profundidad, complejidad, alias, batching y tamaño;
- paginación acotada y límites de recursos;
- timeouts y cancelación;
- control de introspección según exposición y necesidad operativa;
- prevención de N+1 y abuso de resolvers;
- filtrado de campos y relaciones por usuario/tenant.

Deshabilitar introspección no corrige autorización. Persisted queries pueden reducir superficie y controlar consultas, pero no reemplazan límites de coste ni autorización.

### 2.4 gRPC

gRPC usa HTTP/2 y contratos Protocol Buffers; requiere identidad de canal/llamada, autorización por método y recurso, límites de mensaje, deadlines, cancelación y control de streaming. TLS autentica el servidor y cifra el canal; mTLS puede autenticar también al cliente/workload, pero no concede permiso de negocio. Reflection debe evaluarse según exposición y entorno. Los interceptors facilitan controles comunes, pero la política contextual sigue necesitando recurso y sujeto.

## 3. Identidad, OAuth 2.0, OIDC y tokens

Separar OAuth (delegación de autorización) de OpenID Connect (capa de identidad/autenticación). Aplicar RFC 9700 como BCP de seguridad actual para OAuth 2.0.

Para Authorization Code:
- registrar y comparar redirect URIs con coincidencia exacta;
- usar PKCE con S256, incluyendo clientes confidenciales cuando proceda;
- vincular state/nonce a transacción y agente de usuario;
- evitar open redirectors;
- proteger contra mix-up cuando hay múltiples authorization servers;
- no usar implicit grant ni password grant como diseño nuevo;
- evitar tokens en URLs, historial y logs.

Validación de JWT:
- fijar algoritmos permitidos fuera del token;
- verificar firma y claves según issuer confiable;
- comprobar issuer, audience, expiración, not-before, sujeto y scopes;
- validar tipo de token y propósito para evitar confusión ID token/access token;
- rotar claves y manejar JWKS de forma segura;
- rechazar tokens expirados, malformados o de emisor/audiencia incorrectos.

JWT firmado no significa cifrado. Un access token es una credencial portadora salvo que se use mecanismo sender-constrained. Para reducir replay considerar mTLS-bound tokens o DPoP cuando el ecosistema lo soporte. Los refresh tokens de clientes públicos requieren protección apropiada, como rotación o sender-constraining.

Los scopes son permisos gruesos. El recurso debe comprobar autorización fina por objeto, función, propiedad y tenant. Un token con scope `orders:read` no implica acceso a todos los pedidos.

## 4. Autorización y aislamiento multi-tenant

Formalizar:

`Decision = Policy(principal, action, resource, tenant, environment)`

Comprobar cada operación sensible en el backend. No derivar autorización del ID enviado por cliente, del frontend, de un rol almacenado sin frescura ni de la pertenencia a una red.

Pruebas mínimas:
- usuario A lee y modifica recurso propio;
- usuario A intenta leer/modificar recurso de B;
- usuario de tenant A intenta acceder a tenant B;
- rol lector intenta mutación;
- usuario suspendido o sesión revocada intenta operar;
- recurso inexistente y recurso ajeno producen respuestas que no revelan existencia cuando ello sea requisito;
- operación masiva/exportación aplica la misma política que la lectura individual.

Para datos multi-tenant, aplicar separación en capa de servicio y, cuando proceda, en DB (RLS/row-level security) como defensa adicional. Evitar confiar únicamente en un filtro de UI o un parámetro `tenant_id` suministrado por cliente.

## 5. Rate limiting, cuotas y abuso de recursos

Un algoritmo token bucket puede modelarse con capacidad B, tasa de reposición r tokens/s y saldo T:

`T(t) = min(B, T(t0) + r × (t - t0))`

Una operación de coste c se admite si T ≥ c y entonces T := T - c. El modelo permite ráfagas acotadas; la implementación distribuida debe tratar concurrencia, reloj, consistencia y particiones.

Aplicar límites por identidad autenticada, tenant, endpoint, operación y coste; IP solo como señal complementaria. Considerar:
- límites concurrentes y colas;
- tamaño máximo y paginación;
- presupuestos para consultas GraphQL;
- timeouts y circuit breakers;
- cuotas diferenciadas por plan/función;
- idempotency keys para operaciones financieras o reintentables;
- límites de creación de cuentas, envío, exportación y reset;
- detección de automatización con revisión de falsos positivos y accesibilidad.

No usar una única cuota global: puede permitir que un tenant consuma recursos de otros. No bloquear a un usuario legítimo únicamente por NAT compartida.

## 6. Webhooks, callbacks y eventos

Validar firma sobre bytes exactos del cuerpo, timestamp dentro de ventana, identidad del emisor y rotación de secreto. Evitar replay con identificador de evento/idempotencia y almacenamiento de deduplicación. No confiar en IP como única autenticación. Procesar de forma asíncrona con límites, reintentos exponenciales y dead-letter queue; no ejecutar acciones de negocio dos veces por reintento. Firmar y autenticar callbacks salientes y restringir destinos para prevenir SSRF.

## 7. Gateway, mTLS y service mesh

El gateway puede terminar TLS, aplicar límites y enrutar, pero no debe convertirse en único punto de autorización. Propagar identidad verificable y contexto de manera autenticada; no aceptar cabeceras de identidad desde clientes externos. Evitar confundir identidad de servicio con usuario final: conservar ambos sujetos y su cadena de delegación.

mTLS autentica extremos del canal según certificados y política PKI. Deben definirse SAN/identidad, trust bundle, rotación, revocación, expiración, emisión y autorización. Un certificado válido no autoriza todas las operaciones. En service mesh, revisar configuración de políticas, bypass paths, puertos excluidos, tráfico fuera del proxy y telemetría de fallos.

## 8. Errores, logging y observabilidad

Registrar actor/servicio, acción, recurso pseudonimizado, tenant, resultado, razón de denegación, request ID, versión y latencia. No registrar bearer tokens, cookies, secretos, payloads sensibles ni PII innecesaria. Los logs deben protegerse contra inyección, acceso indebido y retención excesiva.

Las respuestas externas deben ser estables y mínimas; el detalle diagnóstico va a logs internos con control de acceso. Correlacionar trazas entre servicios sin propagar credenciales como atributos. Alertar sobre fallos de autorización repetidos, cambios de permisos, uso anómalo, picos de coste y APIs sin propietario.

## 9. Evaluación de controles y métricas

Para defectos etiquetados:
- TP: defecto real detectado;
- FP: alerta incorrecta;
- FN: defecto no detectado;
- TN: caso negativo correctamente clasificado.

`Precision = TP / (TP + FP)`  
`Recall = TP / (TP + FN)`  
`F1 = 2 × Precision × Recall / (Precision + Recall)`

Complementar con cobertura de operaciones, roles, objetos, tenants, estados, versiones, métodos y rutas de error; defectos escapados; latencia p95/p99; coste por operación; tasa de denegación incorrecta; disponibilidad y tiempo de triage. Precision/recall solo tienen sentido si existe ground truth razonable. Un benchmark de fallos sembrados no representa todos los defectos reales.

## 10. Laboratorios fríos (diseñados, no ejecutados)

Entorno: API local en contenedor, red de salida bloqueada, dos tenants ficticios, cuentas de prueba, datos sintéticos, límites de recursos y snapshot.

### LAB-API-01 — Matriz de autorización
Crear usuarios lector/escritor en dos tenants y recursos propios/cruzados. Ejecutar matriz de lectura, escritura, exportación y borrado. Resultado esperado: acceso solo en combinaciones autorizadas; denegaciones auditadas sin filtrar datos ajenos.

### LAB-API-02 — Validación de OAuth
Usar servidor de autorización local de prueba y clientes sintéticos. Comprobar redirect URI, state, nonce, PKCE S256, issuer, audience, expiración, rotación y revocación. Resultado esperado: rechazar tokens/flows inválidos; no emitir ni registrar secretos reales.

### LAB-API-03 — Presupuesto de consultas y rate limit
Comparar token bucket, fixed window y sliding window con carga sintética controlada. Medir ráfagas admitidas, falsos bloqueos, equidad por tenant, latencia y consistencia. No generar tráfico hacia servicios públicos.

### LAB-API-04 — Contratos y compatibilidad
Fijar contrato OpenAPI y servicio; introducir cambios compatibles e incompatibles. Ejecutar contract tests y comprobar diferencias de esquema, autenticación, códigos de error y propiedades expuestas.

### LAB-API-05 — Webhooks y replay
Simular emisor/receptor locales, firma, timestamps y duplicados. Verificar rechazo de firma incorrecta, expiración y replay; comprobar idempotencia del efecto de negocio.

Criterios de parada: cualquier salida de red fuera del laboratorio, dato no sintético, acceso cruzado no controlado, carga que afecte host/servicios compartidos o exposición de secreto. Detener, guardar evidencia saneada y restaurar snapshot.

## 11. Evaluación

| Competencia | Peso | Evidencia |
|---|---:|---|
| Arquitectura y contrato | 15% | inventario, OpenAPI/schema, límites de confianza |
| OAuth/OIDC y tokens | 20% | pruebas PKCE, claims, issuer/audience, rotación |
| Autorización | 25% | matriz y regresiones multi-tenant |
| Disponibilidad/abuso | 15% | cuotas, límites y análisis de coste |
| Comunicación entre servicios | 10% | mTLS, identidad y política |
| Observabilidad/reproducibilidad | 15% | logs saneados, versiones, protocolo y resultados |

Umbral interno propuesto: 80/100 y cero fallos críticos de autorización, validación de token o aislamiento. Este umbral es una propuesta de evaluación, no certificación externa.

## 12. Agenda de investigación y brechas

Preguntas abiertas:
1. ¿Qué diseño de matriz de autorización maximiza cobertura multi-tenant sin explotar combinatoriamente los tests?
2. ¿Cómo combinar límites de coste GraphQL y equidad entre tenants?
3. ¿Qué señales detectan replay y abuso de webhooks sin rechazar reintentos legítimos?
4. ¿Qué políticas de token sender-constrained son viables en diferentes topologías de API?
5. ¿Qué divergencias entre OpenAPI y comportamiento real predicen defectos de autorización o exposición?
6. ¿Qué arquitectura de mTLS y autorización de servicio minimiza bypass y complejidad operativa?

Los estudios requieren baseline, muestra, variables, controles, análisis de incertidumbre, datos sintéticos/licenciados, hashes y réplica independiente.

## 13. Fuentes y madurez

| ID | Fuente | Estado |
|---|---|---|
| `OWASP-API-TOP10-2023` | OWASP API Security Top 10 2023 | Página oficial y categorías revisadas; lectura integral pendiente |
| `OWASP-API1-BOLA-2023` | API1 BOLA | Página oficial revisada |
| `IETF-RFC9700` | OAuth 2.0 Security BCP | RFC oficial y recomendaciones de seguridad inspeccionadas; lectura integral pendiente |
| `OPENAPI-OAS-3.2.1` | OpenAPI Specification 3.2.1 | Índice oficial de versiones inspeccionado; texto completo pendiente |
| `GRPC-AUTH-GUIDE` | gRPC Authentication | Guía oficial inspeccionada; revisión por lenguaje/versión pendiente |

**Límite empírico: no M3/M4/M5.** Este compendio contiene desarrollo técnico, pero no declara laboratorios ejecutados, benchmarks propios, revisión independiente ni reproducción externa. No asignar K4/K5 hasta que la evidencia correspondiente esté disponible.
