# Revisión de literatura inicial — Contenedores y Kubernetes

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta
¿Qué controles limitan el impacto de compromisos en imágenes, runtime, orquestación, secrets y supply chain de contenedores?

## Síntesis
NIST SP 800-190 (2017) trata contenedores como virtualización a nivel de sistema operativo combinada con empaquetado de aplicaciones y describe riesgos y recomendaciones para planificar, implementar y mantener contenedores. Es una referencia base pero antigua: debe complementarse con especificaciones actuales de OCI/Kubernetes, prácticas de hardening y SLSA. El aislamiento de namespaces/cgroups no equivale a una VM ni elimina el riesgo del kernel compartido.

## Superficies de riesgo
Imagen/base y dependencias; registry y tags mutables; build pipeline; runtime y capabilities; kernel/host; secretos y service accounts; API server/RBAC; admission; network policies; volúmenes; logging; upgrades y control plane.

## Hipótesis / experimento (no ejecutado)
H1: baseline endurecida con imágenes por digest, usuario no-root, capabilities mínimas, filesystem read-only, seccomp/AppArmor, límites de recursos y políticas de red reduce escapes/impacto de escenarios sintéticos frente a configuración por defecto. H0: sin diferencia.
Banco: clúster local desechable, imágenes benignas de laboratorio, pruebas no destructivas. Medir controles efectivos, privilegios expuestos, egress, resistencia a configuración incorrecta, latencia, consumo y facilidad de recuperación. Nunca ejecutar pruebas de escape contra clúster ajeno.

## Brechas
Revisar Kubernetes Security Checklist y guías vigentes de Kubernetes; evaluar containerd/CRI, admission controllers, secrets, supply chain y runtime detection. Actualizar SP 800-190 con referencias contemporáneas; no afirmar cumplimiento por usar Docker.

## Fuentes
- NIST SP 800-190: https://doi.org/10.6028/NIST.SP.800-190
- NIST IR 8176 (referencia complementaria): https://csrc.nist.gov/pubs/ir/8176/final
- SLSA v1.1: https://slsa.dev/spec/v1.1/

## Identificadores del registro de fuentes
- `NIST-SP-800-190`
- `NIST-IR-8176`
- `SLSA-v1.1`


## Identificadores del registro de fuentes

- `NIST-SP-800-190`
- `NIST-IR-8176`
- `SLSA-v1.1`
