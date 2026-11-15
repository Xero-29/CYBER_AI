# DevSecOps y seguridad de cadena de suministro — Guía de dominio

**ID:** `devsecops` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Integra seguridad verificable en diseño, código, dependencias, build, artefactos, despliegue y operación. El pipeline es un activo privilegiado: una modificación puede publicar código, firmar releases o acceder a secretos. La meta es evidencia reproducible, no acumular escáneres.

## Superficie y amenazas
Revisar repositorios, ramas, CI runners, workflows, paquetes, registries, imágenes, artefactos, firmas, secretos, tokens OIDC, deploy keys y entornos. Riesgos: dependency confusion, typosquatting, acciones CI comprometidas, runner persistente, secretos expuestos, build no reproducible, artefactos sin procedencia y permisos excesivos.

## Competencias específicas
- Diseñar pipeline con identidad mínima y separación de entornos.
- Integrar SAST, SCA, secret scanning, IaC scanning y container scanning.
- Generar SBOM CycloneDX/SPDX y validar dependencias.
- Firmar artefactos y generar attestations/provenance.
- Usar dependencias fijadas, hashes y repositorios aprobados.
- Proteger runners efímeros, OIDC y tokens de corta duración.
- Aplicar policy-as-code y quality gates con excepciones.
- Medir cobertura y falsos positivos.

## Controles prioritarios
- Permisos mínimos por job y workflow; evitar write-all.
- Fijar acciones CI por commit SHA y dependencias por versión/hash.
- Usar runners efímeros y aislar jobs no confiables.
- No ejecutar código de PR no confiable con secretos de release.
- Proteger secretos con OIDC/secret manager y rotación.
- Generar SBOM, firmar artefactos y validar provenance.
- Bloquear publicación si falla verificación de firma o política crítica.
- Mantener logs de build, commit, runner y artefacto.
- Aplicar branch protection y revisión independiente.

## Metodología
1. Modelar pipeline como sistema de producción con activos y privilegios.
2. Inventariar workflows, permisos, dependencias y secretos.
3. Analizar código, IaC, imágenes y dependencias.
4. Revisar origen y pinning de acciones y paquetes.
5. Generar SBOM y attestations de build.
6. Definir gates según severidad y contexto.
7. Probar en fork/laboratorio sin secretos productivos.
8. Verificar artefacto publicado contra commit y provenance.
9. Revisar excepciones, caducidad y drift.

## Laboratorio seguro
Repositorio de prueba con workflow de lint, test, SCA, secret scan y SBOM. Generar artefacto firmado y comprobar que un cambio no aprobado falla el gate. No usar secretos de producción ni desplegar a entornos reales.

## Evaluación
Cada release está ligado a commit, dependencias, runner y artefacto; SBOM disponible; firma verificable; permisos mínimos; excepciones justificadas.

## Referencias y herramientas
SLSA, NIST SSDF, OpenSSF Scorecard, Sigstore, in-toto, SPDX, CycloneDX, Semgrep, Gitleaks, Syft, Grype, Trivy y Checkov.

## Instrucciones para agentes IA
No ejecutes workflows ni publiques releases. Revisa permisos y procedencia antes de proponer automatización. Trata scripts de CI y acciones de terceros como código ejecutable.