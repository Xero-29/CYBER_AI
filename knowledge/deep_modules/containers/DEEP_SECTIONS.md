# Secciones de profundización — Contenedores y Kubernetes

## Modelo de amenazas
Analizar código fuente, dependencias, Dockerfile, builder, registry, imagen, runtime, kernel, orchestrator, admission, RBAC, secrets, network policies y control plane. Amenazas: imagen comprometida, dependencia maliciosa, escape, privileged pod, service account excesiva, secret expuesto, admission bypass, supply chain y abuso de nodo. Identificar límites entre namespaces y host.

## Detección
Escanear imágenes por digest, provenance y SBOM; registrar eventos de API server, admission, RBAC, exec/attach, cambios de pods, runtime syscalls, red y acceso a secretos. Detectar contenedores privilegiados, drift, imágenes no aprobadas, shells inesperadas, service accounts nuevas y egress anómalo. Correlacionar workload UID, namespace, node, image digest y actor.

## Respuesta a incidentes
Aislar namespace/nodo según impacto, preservar manifest, eventos, logs y snapshot de volúmenes, revocar service accounts y secrets, bloquear imagen/digest y detener rollout. Rotar credenciales, reconstruir desde base verificada y revisar registry, pipeline y nodos. Evitar eliminar pods antes de recolectar evidencia; documentar pérdida de volatilidad y límites del runtime.

## Casos prácticos
Desplegar en clúster de laboratorio una imagen con paquete vulnerable y un pod con permisos excesivos. Detectar digest no aprobado, exec interactivo y acceso a API; aplicar admission policy, RBAC mínimo y NetworkPolicy. Repetir con secret montado como variable y comprobar que no aparece en logs ni artefactos.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para Kubernetes security documentation, NIST SP 800-190, SLSA, OCI y CIS Kubernetes Benchmark. Fijar versiones de Kubernetes, runtime y distribución.
