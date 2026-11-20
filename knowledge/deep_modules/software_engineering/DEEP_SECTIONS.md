# Secciones de profundización — Ingeniería de software segura

## Modelo de amenazas
Incluir requisitos, diseño, repositorio, identidad de desarrollador, dependencias, CI, build, release, despliegue y runtime. Amenazas: requisitos ambiguos, defectos de diseño, inyección, dependencia comprometida, workflow manipulado, secretos filtrados, artefacto sustituido y falta de mantenimiento. Trazar cada componente desde el commit hasta la versión desplegada.

## Detección
Integrar SAST, DAST, SCA, secret scanning, revisión de IaC, SBOM, provenance, tests, logs de CI y runtime. Correlacionar finding con commit, archivo, dependencia, owner, release y servicio. Detectar regresiones, bypass de controles, builds no reproducibles y vulnerabilidades reintroducidas. Medir cobertura, falsos positivos y tiempo de corrección.

## Respuesta a incidentes
Detener release comprometido, preservar repositorio, workflow y artefactos, revocar tokens, aislar runners y determinar builds afectados. Corregir código/dependencias, regenerar artefactos desde entorno limpio, firmar y verificar provenance. Añadir test de regresión y revisar ramas, paquetes publicados y despliegues derivados.

## Casos prácticos
Introducir un defecto de autorización en una API de laboratorio y una dependencia vulnerable fijada. Detectar en PR con test negativo y SCA; bloquear merge; corregir y generar SBOM. Simular un artefacto construido desde commit distinto y comprobar que provenance impide su despliegue.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SSDF, OWASP SAMM, CWE, SLSA y OpenSSF. Fijar versiones y relacionar controles con el ciclo de vida real.
