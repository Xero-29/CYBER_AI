# Investigación técnica: Seguridad cloud

**ID:** cloud · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación multi-cloud pendiente.

## Modelo compartido
Cloud security requiere modelo de responsabilidad compartida por servicio y contrato: IaaS, PaaS, SaaS, serverless, managed identities, control plane, data plane, regiones, cuentas/subscriptions/projects, network, storage, keys, logs y proveedores. No asumir que el proveedor protege configuración, identidad, datos o aplicaciones del cliente.

## Identidad y control plane
Inventariar humanos, service principals, roles, workload identities, federation, API keys y break-glass. Aplicar MFA, least privilege, JIT, conditional access, separation of duties y revisión de grants. Proteger root/owner accounts y evitar credenciales estáticas en CI/CD. Alertar sobre cambios de IAM, políticas, keys, network, logging y desactivación de guardrails.

## Red y datos
Diseñar VPC/VNet, subnets, routes, security groups, firewall, private endpoints, egress, DNS, WAF y peering. Revisar storage public exposure, encryption, key ownership, backup, retention, data residency y access logs. La segmentación cloud requiere analizar rutas transitivas, endpoints privados, service mesh y permisos de control plane.

## Servicios y workloads
Evaluar VM images, containers, Kubernetes, serverless, managed databases, object storage, message queues, metadata services, secrets managers y CI/CD. Aplicar image provenance, patching, runtime protection, workload identity, secret rotation, policy-as-code y secure configuration. Cloud posture scanner no detecta todas las fallas de lógica ni de identidad.

## Detección y respuesta
Centralizar audit logs de control plane, identity, network flow, storage, workload y key management. Habilitar retención protegida y alertas de anomalía. Preparar playbooks de key compromise, public bucket, exposed API, IAM privilege escalation, crypto mining, data exfiltration y region outage. Preservar evidencias sin violar privacidad o residencia.

## Evaluación
Usar account baseline, CSPM, IaC scanning, container/image scanning, threat modeling, attack path analysis y pruebas de recuperación. Medir IAM privilege excess, public assets, unencrypted data, logging gaps, drift, exposed management plane, backup restore success y incident response time.

## Laboratorios
Crear cuentas/subscriptions de prueba con presupuesto y quotas; IaC versionada; tenant separado; storage sintético; roles y policies de prueba; red privada; logging y detección. Simular public exposure, excessive permissions, secret leakage y restore. Egress restringido y destrucción controlada al finalizar.

## Fuentes
- NIST SP 800-144 Cloud Computing Security and Privacy: https://doi.org/10.6028/NIST.SP.800-144
- NIST SP 800-207 Zero Trust: https://doi.org/10.6028/NIST.SP.800-207
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- CSA Cloud Controls Matrix: https://cloudsecurityalliance.org/research/cloud-controls-matrix

**Límite:** la nube no es una sola plataforma; cada servicio/proveedor requiere matriz de responsabilidad y pruebas propias.
