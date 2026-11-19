# Investigación técnica: DevSecOps y cadena de suministro de software

**ID:** devsecops · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 · **Auditoría de pipeline real:** pendiente.

## Modelo de cadena
El artefacto desplegado depende de código, revisión, herramientas, runner, workflow, dependencias, paquetes, compiladores, imágenes base, registries, secretos, firmantes, repositorios y procesos de release. El riesgo existe en el código y en el proceso que produce y distribuye el artefacto.

Modelar origen → build → test → package → sign → publish → deploy → runtime. Cada etapa debe producir evidencia vinculada al commit, builder, workflow, dependencias, artefacto y entorno.

## Prácticas fundamentales
- Repositorios protegidos, revisión independiente, branch rules, CODEOWNERS y control de cambios.
- CI con permisos mínimos por job, tokens de corta duración, secretos separados y runners efímeros cuando sea viable.
- Dependencias fijadas, hashes, lockfiles, mirrors confiables y política de actualización.
- Builds reproducibles cuando sea posible; registrar toolchain, flags, fuentes y entorno.
- Tests unitarios/integración, SAST, SCA, secret scanning, IaC scanning, container scanning y DAST autorizado con gates basados en riesgo.
- SBOM por artefacto e imagen; relacionar componentes con PURL, versión, licencia, hash y dependencia transitiva.
- Firma de artefactos y attestations vinculadas a identidad del builder y workflow.
- Provenance verificable; separar quién aprueba release de quién produce build.
- Releases inmutables, rollback y retención de evidencia.
- Monitoreo post-release y proceso de respuesta.

## Riesgos y controles
| Riesgo | Controles |
|---|---|
| Dependencia comprometida | Lock/hash, revisión, allowlist, mirror, SCA, provenance |
| Workflow injection | Permisos mínimos, pin de actions por SHA, validación de inputs |
| Secret exfiltration | OIDC short-lived, masking, no secrets en PR no confiables, egress restringido |
| Build tampering | Runner efímero, aislamiento, builder identity, attestations y firma |
| Artifact substitution | Hash, firma, verificación en deploy y registry protegido |
| Typosquatting/confusion | PURL exacto, revisión de paquete, namespace y política de origen |
| Base image vulnerable | Digest pin, rebuild periódico, SBOM, scanner y SLA |
| Release no reproducible | Lockfiles, toolchain fijado, build metadata y comparación de hashes |

## SBOM y provenance
Un SBOM describe componentes; no demuestra que el artefacto sea seguro, inventario completo o build confiable. Debe asociarse a digest, formato/versión y dependencias directas/transitivas. Provenance describe cómo se produjo: builder, parámetros, fuentes, materiales y workflow. La firma debe verificarse contra identidad y política confiables; una firma válida de builder comprometido no garantiza integridad.

## Métricas
Porcentaje de releases con SBOM/provenance verificables; dependencias fijadas/hash-verificadas; tiempo de remediación; build reproducibility rate; pipelines con permisos mínimos y runners efímeros; falsos positivos de SAST/SCA; tiempo de revocación de credenciales y recuperación ante compromiso.

## Laboratorios
Pipeline de ejemplo con dependencia fijada, lockfile, SBOM, firma y verificación; sustitución de artefacto y rechazo en deploy; workflow PR no confiable que intenta leer secretos; comparación de builds reproducibles; dependencia vulnerable sintética en SBOM; rotación de credenciales CI y verificación de ausencia de tokens persistentes.

## Fuentes
- NIST SP 800-218 SSDF: https://doi.org/10.6028/NIST.SP.800-218
- NIST SSDF Project y SP 800-218A: https://csrc.nist.gov/Projects/ssdf
- SLSA: https://slsa.dev/spec/
- in-toto: https://in-toto.io/
- CycloneDX: https://cyclonedx.org/specification/overview/
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1

**Estado de evidencia:** página oficial NIST SSDF inspeccionada; otros proyectos son referencias de trabajo pendientes de revisión de versión/licencia. No se ha auditado un pipeline productivo.
