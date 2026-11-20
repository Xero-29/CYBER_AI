# Investigación técnica: Seguridad web y aplicaciones

**ID:** appsec · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas en aplicación real pendientes.

## Modelo de aplicación
Modelar navegador/cliente, frontend, API, backend, identidad, sesión, datos, colas, servicios externos, almacenamiento, CI/CD y operadores. Mapear entradas, salidas, trust boundaries, estados, permisos y flujos sensibles. Amenazas cambian por arquitectura monolítica, microservicios, SPA, server-side rendering, mobile backend y serverless.

## Clases de fallos
- Autenticación débil, recuperación insegura, sesión predecible o mal invalidada.
- Autorización rota a nivel de objeto, propiedad o función.
- Inyección SQL/NoSQL/LDAP/OS/template, XSS, CSRF, SSRF y deserialización insegura.
- Traversal, file upload, path confusion, parser differential y request smuggling.
- Configuración insegura, headers/CORS/TLS, secretos expuestos y errores verbosos.
- Business logic abuse, race conditions, idempotencia rota y abuso de flujos.
- Supply chain, dependencias, build, CI/CD y componentes de terceros.

## Requisitos y verificación
OWASP ASVS 5.0.0 es la versión estable publicada el 30-05-2025; úsese como catálogo de requisitos verificables, fijando versión y nivel. OWASP WSTG 4.2 es la versión estable señalada por el proyecto, mientras 5.0 sigue en desarrollo; no mezclar IDs de versiones. OWASP Top 10 sirve para concienciación/priorización, no sustituye un estándar de verificación.

Para cada requisito, definir activo, amenaza, condición previa, prueba positiva/negativa, resultado esperado, evidencia, owner y riesgo residual. Revisar controles de sesión, control de acceso, validación, codificación de salida, seguridad de archivos, criptografía, logging y configuración.

## Método de pruebas
1. Obtener autorización y alcance escrito, cuentas de prueba y exclusiones.
2. Revisar arquitectura, código, configuración y dependencias.
3. Crear mapa de endpoints, roles, datos y operaciones sensibles.
4. Ejecutar pruebas pasivas y luego activas controladas.
5. Validar manualmente hallazgos y reproducibilidad.
6. Documentar impacto, evidencia mínima, mitigación y retest.
7. Evitar extracción real de datos o persistencia fuera del entorno aprobado.

## Laboratorios
OWASP Juice Shop/WebGoat o aplicaciones propias vulnerables; casos de control de acceso multiusuario, inyección en datos sintéticos, XSS con payloads inocuos, CSRF, SSRF contra endpoints mock, uploads limitados y lógica de negocio. Aislar egress para evitar SSRF hacia metadata cloud o redes reales.

## Métricas
Cobertura ASVS por requisito, endpoints probados, roles y combinaciones, defectos confirmados, falsos positivos, defectos reabiertos, tiempo de remediación y regresión por release.

## Fuentes
- OWASP ASVS 5.0.0: https://asvs.owasp.org/
- OWASP WSTG: https://wstg.owasp.org/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- NIST SSDF: https://doi.org/10.6028/NIST.SP.800-218

**Límite:** referencias oficiales consultadas; los controles deben adaptarse a tecnología/versión y validarse en laboratorio.
