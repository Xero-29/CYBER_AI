# Investigación técnica: Seguridad de APIs

**ID:** api · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de contrato y autorización pendiente.

## Modelo
Una API es una frontera de negocio y datos. Modelar consumidores, gateway, autenticación, autorización, servicios, colas, bases de datos, proveedores, scopes, tokens, rate limits y telemetría. Inventariar REST, GraphQL, gRPC, webhooks, APIs internas, partner y machine-to-machine; incluir versiones, entornos y endpoints olvidados.

## Riesgos prioritarios OWASP API Top 10 2023
- API1 Broken Object Level Authorization: comprobar permiso sobre cada objeto solicitado, no confiar en ID opaco.
- API2 Broken Authentication: tokens, sesiones, MFA, OAuth/OIDC y validación de issuer/audience/expiry.
- API3 Broken Object Property Level Authorization: evitar mass assignment y exposición de propiedades sensibles.
- API4 Unrestricted Resource Consumption: cuotas, paginación, payload size, timeout, concurrency y coste.
- API5 Broken Function Level Authorization: permisos por función/operación, no solo endpoint.
- API6 Sensitive Business Flows: proteger procesos de negocio frente a automatización y abuso.
- API7 SSRF: validar destinos, DNS/IP tras resolución, redirecciones y egress fuera del proceso.
- API8 Security Misconfiguration: CORS, headers, TLS, errores, defaults y gateway.
- API9 Improper Inventory Management: versionado, shadow APIs, endpoints legacy y ownership.
- API10 Unsafe Consumption of APIs: validar respuesta de proveedores y tratarla como input no confiable.

## Autorización
Definir matriz sujeto-acción-recurso-tenant-contexto. Validar autorización en servidor en cada operación, incluyendo nested objects, batch, export, search, cache, async jobs y webhooks. Probar IDOR/BOLA con usuarios sintéticos de distintos tenants. La seguridad no puede depender de ocultar botones o filtrar solo en frontend.

## Diseño y controles
Usar schemas estrictos, allowlists de campos, límites de tamaño, canonicalización, idempotency keys, replay protection, timeouts, quotas y circuit breakers. OAuth scopes no sustituyen autorización de objeto. API gateway no sustituye controles en servicio. GraphQL requiere depth/complexity limits y autorización por resolver. gRPC exige authn/authz por método y control de metadata.

## Pruebas y laboratorios
Generar OpenAPI/GraphQL schemas versionados. Probar cada endpoint con matriz de roles/tenants, objeto ajeno, propiedad sensible, método no permitido, token expirado/audience incorrecta, payload excesivo, repetición, proveedor mock malicioso y SSRF hacia destinos bloqueados. Medir cobertura de endpoints, BOLA/BFLA, precisión de detección, rate limit, latencia y errores.

## Fuentes
- OWASP API Security Top 10 2023: https://owasp.org/www-project-api-security-project/
- OWASP API Security: https://api-security.owasp.org/
- OWASP API1 BOLA: https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/
- NIST SP 800-207 Zero Trust: https://doi.org/10.6028/NIST.SP.800-207

**Límite:** síntesis del proyecto OWASP y arquitectura; no equivale a auditoría de endpoints reales.
