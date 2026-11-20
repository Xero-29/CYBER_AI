# Seguridad de API — Guía de dominio

**ID:** `api` · **Versión:** 2.1.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Define controles para APIs REST, GraphQL, gRPC y eventos. El riesgo dominante suele estar en autorización por objeto/función, identidad máquina-a-máquina, exposición excesiva de datos, abuso de recursos y confianza incorrecta entre servicios. Las pruebas activas solo se ejecutan sobre APIs propias o autorizadas.

## Modelo de amenazas
Identificar consumidor, gateway, servicio, identidad, recurso, tenant, datos, cola y proveedor. Analizar BOLA/IDOR, BFLA, mass assignment, autenticación rota, consumo ilimitado, SSRF, inventario incompleto, versiones abandonadas, configuración insegura y abuso de lógica de negocio. Para GraphQL revisar introspección expuesta, profundidad/coste de consultas y autorización por resolver. Para gRPC revisar mTLS, identidad de servicio, reflection y límites de mensajes.

## Competencias específicas
- Diseñar autenticación con OAuth 2.1/OIDC, mTLS o credenciales de workload según caso.
- Validar tokens: issuer, audience, firma, expiración, algoritmo permitido, scopes y rotación.
- Aplicar autorización por objeto, función, tenant y contexto de negocio.
- Definir esquemas estrictos, límites de tamaño, paginación y tipos.
- Prevenir replay, enumeración, abuso de endpoints y agotamiento de recursos.
- Versionar, inventariar y retirar APIs con control de compatibilidad.
- Proteger secretos, webhooks, callbacks y comunicación servicio-a-servicio.

## Controles esenciales
- Nunca confiar en IDs enviados por el cliente: comprobar propiedad y permiso en el servidor.
- Evitar confiar únicamente en scopes generales; comprobar autorización en cada operación y objeto.
- Validar firmas y claims del token; no aceptar algoritmos elegidos por el cliente ni tokens sin audience.
- Separar autenticación de autorización y no confundir CORS con control de acceso.
- Usar idempotency keys para operaciones reintentables y controles anti-replay en webhooks.
- Aplicar rate limiting y cuotas por identidad, tenant, IP y coste de operación.
- Redactar PII y secretos en logs; registrar actor, recurso, acción y resultado.
- Evitar respuestas excesivas; aplicar allowlists de campos y filtrado por rol.

## Metodología
1. Exportar OpenAPI/GraphQL schema y validar que refleje la implementación.
2. Crear inventario de endpoints, métodos, roles, scopes y recursos.
3. Construir matriz de autorización con casos permitidos y denegados.
4. Revisar tokens, mTLS, gestión de claves, rotación y expiración.
5. Probar casos negativos con dos tenants sintéticos y usuarios de roles distintos.
6. Verificar límites de tasa, paginación, tamaños y consultas costosas.
7. Inspeccionar logs para asegurar trazabilidad y redacción.
8. Documentar compatibilidad, versiones obsoletas y plan de retirada.
9. Añadir pruebas de regresión de autorización y abuso.

## Laboratorio seguro
API local con dos organizaciones ficticias, dos usuarios por organización, roles lector/escritor y recursos separados. Ejecutar pruebas de acceso cruzado, escalada de función, token expirado, replay de webhook y consultas excesivas. Las pruebas deben confirmar denegación y no recuperar datos ajenos.

## Evaluación
Cada endpoint tiene autenticación, autorización, esquema, límites, logging y propietario definidos. La matriz de permisos tiene pruebas positivas y negativas. Los cambios de API incluyen versionado y regresión.

## Referencias
OWASP API Security Top 10, OAuth 2.1, OpenID Connect, RFC 9700, OpenAPI, GraphQL Security, gRPC Security y CWE.

## Instrucciones para agentes IA
No generes tokens reales ni envíes solicitudes a servicios productivos. Usa fixtures locales. No marques una API como segura por tener gateway o JWT: verifica autorización por objeto, tenant y operación.

---

## Arquitectura
Modelar el recorrido cliente → DNS/TLS/CDN o gateway → autenticación/autorización → servicio API → colas y servicios internos → almacenes de datos y terceros. Separar plano de control (registro, versionado, políticas y secretos) del plano de datos. Identificar límites entre tenants, servicios y zonas de confianza; registrar scopes, claims, identidad de workload, contratos, esquemas, límites de tamaño y operaciones con efectos laterales. Los callbacks/webhooks, resolvers GraphQL, endpoints administrativos y rutas internas son superficies distintas y requieren controles propios.

## Marco obligatorio de desarrollo experto e investigación

Este paquete se desarrolla conforme al [Estándar experto e investigación](../../EXPERT_RESEARCH_STANDARD.md). El estándar aplica a esta especialidad, no solo al currículo global.

**Estado del perfil:** estructura y mapa de evidencias definidos; el contenido técnico ampliado, la revisión integral de fuentes, los laboratorios ejecutados y la validación independiente se registran por separado. No se declara K4/K5 por la existencia de este marco.

Cada tema de esta especialidad debe desarrollarse como unidad independiente y cubrir: teoría, formalización pertinente, arquitectura, estándares versionados, implementación, análisis avanzado, seguridad adaptada al dominio, investigación, laboratorio/dataset, evaluación, Skills verificadas y trazabilidad. La matriz detallada de capas, evidencias, enfoque matemático y restricciones de laboratorio está en `knowledge/curricula/domain_curriculum.json`, dentro del perfil `api`.

**Madurez:** K1–K5 se asigna por tema y evidencia. Las ocho puertas G1–G8 deben mostrar estado explícito; lo no ejecutado o no revisado permanece pendiente. Las referencias descubiertas no cuentan como lectura completa y los laboratorios diseñados no cuentan como ejecutados.


## Mapa técnico ampliado (v2.1.0)

El compendio cubre arquitectura y límites de confianza, REST/HTTP, OpenAPI, GraphQL, gRPC, OAuth 2.0/OIDC, RFC 9700, JWT, autorización multi-tenant, rate limiting, abuso de negocio, webhooks, mTLS, gateway/service mesh, telemetría y métricas.

La agenda define seis líneas de investigación con hipótesis falsables y diseños experimentales. Cinco laboratorios fríos están diseñados; no se han ejecutado.

## Estado de madurez

- Contenido técnico específico ampliado: `knowledge/deep_modules/api/TECHNICAL_COMPENDIUM.md`.
- Fuentes oficiales y límites de revisión: `LITERATURE_REVIEW.md` y `knowledge/research/source_registry.json`.
- Lectura integral de RFC 9700, OpenAPI y documentación gRPC: pendiente.
- Revisión sistemática académica: pendiente.
- Laboratorios, benchmarks y resultados propios: pendientes.
- Revisión independiente y reproducción: pendientes.
- Skills verificadas: no promovidas en este cambio.

**Límite empírico: no M3/M4/M5.** El contenido ampliado no equivale a validación experta ni investigación concluida. K1–K5 se asigna por tema y evidencia conforme a `knowledge/EXPERT_RESEARCH_STANDARD.md`.
