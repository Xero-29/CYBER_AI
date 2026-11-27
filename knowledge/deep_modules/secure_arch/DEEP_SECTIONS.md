# Secciones de profundización — Arquitectura segura

## Modelo de amenazas
Descomponer sistema en contextos de confianza, planos de control/datos, identidades, servicios, datos, secretos, red y dependencias. Aplicar STRIDE, attack trees y misuse cases; examinar trust boundaries, rutas de administración, single points of failure y cascadas. Incluir amenazas de proveedor, operador, build y recovery plane.

## Detección
Traducir decisiones arquitectónicas a señales verificables: cambios de IAM, rutas, firewall, configuración, secretos, trust stores, endpoints y dependencias. Detectar drift respecto de baseline, rutas no autorizadas, cambios de política y componentes fuera de inventario. Cada requisito debe tener prueba, propietario y evidencia observable.

## Respuesta a incidentes
Usar diagramas y threat model para identificar blast radius, dependencias y rutas de contención. Deshabilitar componentes comprometidos, revocar identidades, preservar artefactos y reconstruir desde configuración declarativa aprobada. Actualizar modelo y controles después del incidente; validar que la corrección no abre otro trust boundary.

## Casos prácticos
Diseñar una arquitectura de API multi-tenant con RAG y herramientas. Identificar flujos de prompt, retrieval, identidad y secretos; modelar prompt injection y acceso cruzado; definir autorización por tenant, egress, logging y fallback. Ejecutar pruebas negativas y comparar el diseño con una arquitectura sin segmentación.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-160, NIST SP 800-207, OWASP ASVS y Microsoft SDL. Los patrones requieren adaptación y evidencia en el despliegue.
