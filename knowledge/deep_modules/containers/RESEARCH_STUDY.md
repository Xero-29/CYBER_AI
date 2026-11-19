# Investigación técnica: Contenedores, Kubernetes y supply chain de imágenes

**ID:** containers · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas de cluster pendientes.

## Modelo
Contenedores comparten kernel host; imagen, runtime, daemon, registry, orchestrator, control plane, CNI/CSI, admission, secrets, nodes y workloads forman la superficie. Kubernetes añade API server, etcd, scheduler, controller manager, kubelet, kube-proxy, RBAC, service accounts, admission controllers y network policies.

## Seguridad de imágenes y build
Usar imágenes mínimas, digest pin, SBOM, provenance, firma, escaneo y rebuild. No ejecutar como root, eliminar capabilities, filesystem read-only, no-new-privileges, seccomp y LSM cuando sea compatible. Evitar secretos en layers, args y env persistentes. Revisar Dockerfile, build context, base image, paquetes, entrypoint y permisos.

## Kubernetes
- RBAC least privilege; evitar cluster-admin general y tokens de service account montados innecesariamente.
- NetworkPolicy con CNI que realmente aplique política; default deny y excepciones explícitas.
- Pod Security Standards, admission policy, quotas, limits, seccomp, capabilities y host namespaces.
- Proteger etcd encryption at rest, backups, API endpoint, audit logs y control plane.
- Limitar hostPath, privileged pods, hostNetwork, hostPID, hostIPC y device mounts.
- Rotar certificados y credenciales; proteger kubeconfig y acceso de operadores.
- Segregar namespaces por trust boundary, sin tratar namespace como frontera fuerte por sí solo.

## Riesgos
Container escape, runtime/daemon compromise, supply chain, image poisoning, exposed API, RBAC escalation, secrets exposure, lateral movement, malicious admission webhook, insecure node, kubelet exposure, DNS abuse, network policy gaps y resource exhaustion.

## Evaluación y laboratorio
Cluster local desechable (kind/k3d/minikube) con red aislada. Probar RBAC, service account token, network policy, pod security, admission, secrets, image signature, read-only FS, limits, audit logs y backup/restore etcd. No ejecutar escape exploit fuera de laboratorio controlado.

Métricas: imágenes firmadas, workloads non-root, privileged pods, RBAC excess, network policy coverage, secret exposure, image vulnerabilities por SLA, drift, API audit coverage y restore success.

## Fuentes
- NIST SP 800-190 Application Container Security Guide: https://doi.org/10.6028/NIST.SP.800-190
- NSA/CISA Kubernetes Hardening Guidance: https://www.cisa.gov/resources-tools/resources/kubernetes-hardening-guidance
- Kubernetes Security Checklist: https://kubernetes.io/docs/concepts/security/security-checklist/
- CIS Kubernetes Benchmark: https://www.cisecurity.org/cis-benchmarks

**Límite:** controles dependen de versión Kubernetes, runtime, CNI y distribución; verificar soporte y enforcement efectivo.
