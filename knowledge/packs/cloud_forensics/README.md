# Forense cloud — Guía de dominio

**ID:** `cloud_forensics` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Preserva y analiza evidencia de control planes, workloads, almacenamiento, identidad y servicios gestionados. La evidencia cloud es efímera, distribuida y dependiente de proveedor, región y configuración de logging. La adquisición debe respetar jurisdicción, contratos y privacidad.

## Fuentes
CloudTrail/CloudTrail Lake, Azure Activity/Entra logs, GCP Audit Logs, flow logs, DNS, snapshots, object versioning, EDR, Kubernetes audit, IAM, KMS, serverless, CI/CD, SaaS y tickets de cambios. Registrar región, cuenta, proyecto, tenant, actor, API, request ID, timestamp, retención y estado de integridad.

## Competencias
- Preservar logs de control plane y datos con exportación nativa.
- Correlacionar identidades humanas, service principals y workloads.
- Analizar cambios IAM, tokens, claves, redes, storage y snapshots.
- Construir timeline distribuido y normalizar UTC.
- Adquirir snapshots y discos sin alterar originales.
- Evaluar logs ausentes, retrasos, límites y gaps por servicio.
- Gestionar evidencias de proveedores y solicitudes legales.

## Controles de preservación
- Activar logging organizacional y exportación central fuera de cuenta.
- Retención bloqueada/inmutable y acceso segregado.
- Snapshots con tags, hashes y registro de operador.
- Preservar configuración y metadatos junto al contenido.
- No apagar ni terminar workloads antes de evaluar volatilidad.
- Evitar copiar datos personales innecesarios.
- Registrar API calls y request IDs de adquisición.
- Cifrar evidencias y limitar acceso por caso.

## Metodología
1. Definir autorización, jurisdicción, cuentas y alcance.
2. Preservar primero logs de control plane, identidad y red.
3. Exportar logs nativos y verificar integridad/continuidad.
4. Capturar snapshots con cambios mínimos y aprobación.
5. Correlacionar actores, recursos, regiones y tiempos.
6. Construir timeline y distinguir eventos confirmados de inferencias.
7. Solicitar evidencias del proveedor si el plano de control no expone detalle.
8. Revisar hallazgos con analista independiente.
9. Conservar cadena de custodia y plan de retención.

## Laboratorio
Cuenta cloud sandbox con audit logs y recursos ficticios. Simular creación de rol, cambio de bucket policy y acceso a secreto; exportar eventos y reconstruir timeline. No usar datos reales ni modificar producción.

## Evaluación
Evidencia preservada en cuenta separada, timeline trazable, huecos documentados y adquisición reproducible.

## Referencias
NIST SP 800-86, NIST SP 800-201, CSA Cloud Forensics, AWS/Azure/GCP audit logging guides y ISO/IEC 27037.

## Instrucciones IA
No borres, detengas ni restaures recursos. Preserva primero y coordina con dueño de cuenta y legal. No afirmes atribución a partir de IP o user-agent aislado.