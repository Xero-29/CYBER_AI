# Secciones de profundización — Seguridad de APIs

## Modelo de amenazas
Modelar REST, GraphQL, gRPC y webhooks con identidades humanas y de servicio, gateways, scopes, objetos, propiedades y operaciones. Priorizar BOLA, BFLA, autorización por propiedad, autenticación rota, consumo ilimitado, SSRF, inventario/versiones obsoletas y confianza indebida en APIs de terceros. Revisar límites de tenant, callbacks, resolvers anidados, operaciones batch y endpoints administrativos.

## Detección
Registrar identidad autenticada, cliente, scope, tenant, ruta/operación, objeto, decisión de autorización, consumo, latencia y resultado. Alertar por enumeración de IDs, cambios de propiedad no esperados, exceso de paginación, abuso de tokens, anomalías de cuota y destinos SSRF. Proteger logs contra tokens y cuerpos sensibles. Medir por endpoint cobertura de autorización y tasa de alertas confirmadas.

## Respuesta a incidentes
Revocar credenciales y tokens comprometidos, reducir scopes, invalidar sesiones y bloquear temporalmente operaciones abusadas. Identificar recursos consultados o modificados, preservar trazas del gateway y backend, rotar secretos de integraciones, corregir autorización en servidor y revisar cachés/colas. Añadir tests contractuales y de regresión multi-tenant antes de reabrir el endpoint.

## Casos prácticos
Una API devuelve facturas por ruta con identificador y valida sesión, pero no pertenencia del objeto. Crear dos tenants sintéticos, probar lectura y modificación cruzada, confirmar exposición sin acceder a datos reales, implementar autorización contextual y ejecutar matriz de pruebas por rol, objeto, método y tenant. Repetir el mismo análisis en GraphQL, endpoints batch y exportaciones.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para OWASP API Security Top 10 2023, ASVS, OAuth 2.0 Security BCP y documentación de protocolos. No extrapolar un control de REST a GraphQL o gRPC sin validar su semántica.
