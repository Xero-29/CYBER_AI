# Seguridad cloud — Guía de dominio

**ID:** `cloud` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Evalúa plataformas AWS, Azure, GCP y entornos multicloud. La seguridad cloud es responsabilidad compartida: el proveedor protege componentes del servicio, pero el cliente conserva responsabilidades sobre identidad, datos, configuración, aplicaciones, red, claves y operación. Las pruebas activas requieren cuenta de laboratorio o autorización específica.

## Arquitectura y amenazas
Inventariar organizaciones, cuentas/subscriptions/projects, regiones, redes, IAM, almacenamiento, KMS, secretos, logs, workloads, serverless, Kubernetes, endpoints de metadata y pipelines. Riesgos frecuentes: almacenamiento público, roles excesivos, claves largas, metadata SSRF, exposición de snapshots, logs incompletos, redes planas, recursos abandonados, secretos en imágenes y abuso de identidades de workload.

## Competencias específicas
- Diseñar jerarquía de cuentas y separación de entornos.
- Aplicar IAM de mínimo privilegio, roles temporales y federación.
- Proteger almacenamiento, bases de datos, snapshots y copias.
- Configurar KMS, rotación, separación de funciones y control de claves.
- Revisar security groups, NSG, VPC/VNet, endpoints privados y egress.
- Activar logs de control, identidad, red y datos con retención.
- Auditar Kubernetes, serverless, contenedores y supply chain.
- Evaluar postura con CIS Foundations Benchmarks y servicios nativos.

## Controles prioritarios
- Prohibir credenciales raíz de uso diario y exigir MFA resistente a phishing.
- Preferir roles federados y credenciales temporales frente a claves estáticas.
- Aplicar SCP/Policy/Organization guardrails y separación por cuenta.
- Bloquear acceso público no justificado a buckets, snapshots y bases.
- Cifrar datos en reposo y tránsito; controlar grants y rotación KMS.
- Restringir metadata endpoints y usar protección SSRF de plataforma.
- Activar audit logs y alertas para cambios IAM, red, storage y KMS.
- Aplicar egress controlado, private endpoints y segmentación.
- Mantener imágenes, IaC y dependencias escaneadas antes de desplegar.

## Metodología
1. Confirmar proveedor, cuenta, región, alcance y permisos de lectura.
2. Inventariar activos y propietarios con APIs de solo lectura.
3. Evaluar IAM, claves, almacenamiento público, red, cifrado y logging.
4. Revisar IaC y drift respecto a baseline.
5. Priorizar exposiciones públicas y rutas de privilegio.
6. Validar con evidencia de configuración y logs; no modificar recursos.
7. Recomendar remediaciones como cambios IaC revisables.
8. Probar en cuenta sandbox y ejecutar plan de rollback.
9. Verificar que logs, alertas y backups cubren el recurso.

## Laboratorio seguro
Cuenta cloud aislada con presupuesto, sin datos reales y con guardrails. Desplegar una red privada, rol de workload, bucket cifrado y logging. Introducir una mala configuración ficticia, detectarla con Prowler/ScoutSuite/Checkov y corregirla por IaC. Borrar el entorno al terminar.

## Criterios de evaluación
Inventario completo, IAM mínimo, exposición pública justificada, logging activo, claves protegidas, egress controlado y cambios reproducibles por IaC.

## Marcos y herramientas
CIS AWS/Azure/GCP Foundations, NIST CSF, CSA CCM, AWS Well-Architected Security Pillar, Prowler, ScoutSuite, Checkov, Trivy y policy-as-code.

## Instrucciones para agentes IA
No solicites ni uses credenciales root. Empieza con lectura y evidencia. No cambies IAM, firewall, storage ni claves sin autorización explícita y plan de reversión. Nunca copies secretos o datos de cliente a proveedores remotos.