# Secciones de profundización — Forense cloud

## Modelo de amenazas
La evidencia cloud se distribuye entre control plane, identidad, APIs, logs del proveedor, snapshots, objetos, red virtual, workloads y SaaS. Amenazas: expiración de logs, borrado de snapshots, retención insuficiente, cambios de región, relojes desalineados, acceso del proveedor y adquisición incompleta. Documentar límites de visibilidad y responsabilidad compartida.

## Detección
Preparar logging de organización, trails inmutables, alertas de borrado/retención, snapshots y exportación a cuenta separada. Detectar desactivación de auditoría, cambios de policy, borrado de objetos/versiones y accesos al repositorio de evidencia. Verificar cobertura por cuenta, región y servicio.

## Respuesta a incidentes
Preservar primero logs y snapshots con IDs, región, timestamps y request IDs; calcular hashes y exportar a repositorio protegido. Revocar sesiones, congelar cambios no esenciales y coordinar con proveedor. Documentar método de adquisición, límites API, cadena de custodia y cualquier dato que no pudo obtenerse.

## Casos prácticos
En cuenta cloud de laboratorio, generar cambios IAM, creación de instancia y borrado de objeto versionado. Adquirir logs de control plane y snapshot, construir timeline y reproducir hallazgos por un segundo analista. Simular expiración de logs y verificar alerta preventiva.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-201, NIST SP 800-86, guías de evidencia del proveedor y documentación de auditoría. Registrar servicio y región.
