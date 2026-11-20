# Seguridad de contenedores y Kubernetes — Guía de dominio

**ID:** `containers` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Protege imágenes, runtimes, registries, nodos, orquestadores y workloads. Un contenedor no es una VM: comparte kernel y depende de namespaces, cgroups, capabilities, seccomp y políticas LSM. El control de clúster debe proteger API server, etcd, identidades, admission, red, secretos y supply chain. No ejecutar cargas hostiles en Docker compartido; usar microVM/VM aislada.

## Superficie y amenazas
Analizar Docker/Containerd/CRI-O, imágenes base, Dockerfile, registry, kubelet, API server, etcd, RBAC, admission controllers, CNI, CSI, service accounts, secrets, ingress y nodes. Riesgos: contenedor privilegiado, root, hostPath, socket Docker montado, capabilities excesivas, escape por kernel, imágenes con secretos, tag mutable, registry público, RBAC wildcard, service account token expuesto y network policy ausente.

## Competencias específicas
- Construir imágenes mínimas, reproducibles y sin herramientas innecesarias.
- Aplicar usuario no root, read-only rootfs, seccomp y capabilities mínimas.
- Gestionar SBOM, firmas, procedencia y escaneo de vulnerabilidades.
- Configurar RBAC por namespace y recurso, evitando ClusterRole amplio.
- Proteger secretos con KMS/CSI y rotación, no ConfigMaps.
- Aplicar Pod Security Standards, admission policy y NetworkPolicy.
- Endurecer nodos, kubelet, etcd, API server y registry.
- Monitorizar runtime y detectar procesos, montajes y conexiones anómalas.

## Controles prioritarios
- Prohibir privileged, hostPID/hostNetwork/hostIPC y hostPath salvo excepción revisada.
- Bloquear escalada de privilegios y eliminar capabilities no requeridas.
- Exigir imágenes firmadas, digest fijado y registry aprobado.
- Separar namespaces y limitar service accounts.
- Activar Pod Security Admission, seccomp RuntimeDefault y políticas de admisión.
- Aplicar network policies deny-by-default.
- Cifrar secretos en reposo, limitar acceso a etcd y auditar lectura de secretos.
- Parchar nodos y runtime; usar nodos inmutables y reemplazo controlado.
- Definir quotas, limits y probes para limitar DoS accidental.

## Metodología
1. Inventariar clúster, versión, namespaces, nodos, registries y workloads.
2. Revisar manifiestos, Helm charts, Kustomize e IaC antes de desplegar.
3. Analizar imágenes con SBOM y escáner; comprobar firma y procedencia.
4. Revisar RBAC, service accounts, secrets, admission y políticas de red.
5. Evaluar runtime y configuración del host con checks de solo lectura.
6. Probar políticas en clúster desechable con workloads sintéticos.
7. Medir impacto de restricciones y excepciones.
8. Publicar remediaciones declarativas y plan de rollback.
9. Verificar drift y repetir el análisis en cada release.

## Laboratorio seguro
Clúster local kind/k3d con dos namespaces y workloads ficticios. Desplegar una imagen no root, RBAC mínimo, network policy y Pod Security. Introducir manifiestos inseguros y detectarlos con kube-linter/kube-bench/Checkov. No usar host mounts ni cargas de escape.

## Evaluación
Ningún workload privilegiado sin excepción, imágenes fijadas y firmadas, RBAC mínimo, secretos protegidos, network policies probadas y nodos parcheados.

## Referencias y herramientas
CIS Kubernetes Benchmark, NSA/CISA Kubernetes Hardening Guidance, Kubernetes Pod Security Standards, OCI Image Spec, Syft, Grype, Trivy, kube-linter y Kubescape.

## Instrucciones para agentes IA
No afirmes que Docker aísla malware. No sugieras montar socket Docker o host filesystem para resolver tareas. Usa manifiestos sintéticos y bloquea cualquier prueba de escape fuera de VM desechable.

---

## Marco obligatorio de desarrollo experto e investigación

Este paquete se desarrolla conforme al [Estándar experto e investigación](../../EXPERT_RESEARCH_STANDARD.md). El estándar aplica a esta especialidad, no solo al currículo global.

**Estado del perfil:** estructura y mapa de evidencias definidos; el contenido técnico ampliado, la revisión integral de fuentes, los laboratorios ejecutados y la validación independiente se registran por separado. No se declara K4/K5 por la existencia de este marco.

Cada tema de esta especialidad debe desarrollarse como unidad independiente y cubrir: teoría, formalización pertinente, arquitectura, estándares versionados, implementación, análisis avanzado, seguridad adaptada al dominio, investigación, laboratorio/dataset, evaluación, Skills verificadas y trazabilidad. La matriz detallada de capas, evidencias, enfoque matemático y restricciones de laboratorio está en `knowledge/curricula/domain_curriculum.json`, dentro del perfil `containers`.

**Madurez:** K1–K5 se asigna por tema y evidencia. Las ocho puertas G1–G8 deben mostrar estado explícito; lo no ejecutado o no revisado permanece pendiente. Las referencias descubiertas no cuentan como lectura completa y los laboratorios diseñados no cuentan como ejecutados.
