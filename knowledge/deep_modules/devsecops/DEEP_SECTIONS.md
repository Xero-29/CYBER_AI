# Secciones de profundización — DevSecOps y cadena de suministro

## Modelo de amenazas
Modelar repositorio, identidad de desarrollador, revisión, CI runners, actions/plugins, dependencias, build, artefactos, registry, firma, despliegue y runtime. Amenazas: dependency confusion, typosquatting, maintainer compromise, secret leakage, runner persistence, workflow injection, build tampering y artefactos sin procedencia. Trazar commit a binario desplegado.

## Detección
Verificar SBOM, hashes, firma, provenance, dependencias nuevas, cambios de workflow, permisos de tokens, uso de runners y publicación de artefactos. Detectar builds no reproducibles, dependencias no fijadas, secretos en logs y divergencia entre commit aprobado y artefacto. Correlacionar actor, commit, workflow, runner, digest y despliegue.

## Respuesta a incidentes
Detener publicación, revocar tokens y credenciales de CI, aislar runners, preservar logs e imágenes, identificar artefactos derivados de la ventana comprometida y bloquear digests. Reconstruir en runners limpios, regenerar SBOM/provenance, firmar nuevamente y desplegar artefactos verificados. Evaluar dependencias transitivas y downstream consumers.

## Casos prácticos
Comprometer deliberadamente un runner efímero de laboratorio mediante un workflow de prueba que imprime un secreto sintético. Verificar detección, aislamiento, rotación y ausencia de persistencia en jobs siguientes. Segundo caso: dependencia con versión mutable; demostrar bloqueo por lockfile, hash y política de revisión.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SSDF, SLSA, Sigstore, SPDX, CycloneDX y OpenSSF Scorecard. Fijar versiones de especificaciones y herramientas.
