# Gestión de vulnerabilidades — Guía de dominio

**ID:** `vuln_management` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Gestiona exposición técnica desde descubrimiento hasta remediación y verificación. Un hallazgo no es automáticamente un riesgo crítico: considerar activo, exposición, explotabilidad, impacto, controles compensatorios y contexto de negocio. Escaneos activos requieren alcance autorizado y límites.

## Ciclo de vida
Inventario de activos, descubrimiento, identificación, validación, priorización, asignación, remediación, retest, excepción y cierre. Correlacionar CVE, CWE, CVSS, EPSS, CISA KEV, SBOM, versión instalada y exposición real. Evitar duplicados por producto, ruta, paquete o causa raíz.

## Competencias específicas
- Normalizar hallazgos de SAST, DAST, SCA, IaC, cloud y pentest.
- Validar falsos positivos y reproducir sin impacto.
- Priorizar por KEV, EPSS, CVSS, exposición y criticidad del activo.
- Definir SLA por riesgo y excepciones aprobadas.
- Relacionar vulnerabilidad con SBOM y dependencias transitivas.
- Gestionar vulnerabilidades de terceros y end-of-life.
- Medir tiempo de remediación, recurrencia y backlog.
- Verificar cierre mediante retest y evidencia.

## Controles prioritarios
- Inventario continuo con dueño y criticidad.
- Escaneo autenticado cuando esté autorizado y sea seguro.
- Priorización contextual y fecha límite según riesgo.
- Parches probados en staging y plan de rollback.
- Mitigación temporal cuando el parche no sea viable.
- Excepciones con aprobador, compensación y expiración.
- Retest independiente y cierre con evidencia.
- Alertas para activos expuestos con CVE explotada activamente.

## Metodología
1. Importar hallazgos y normalizar identificadores.
2. Deduplicar por causa raíz y activo.
3. Verificar versión, configuración y exposición.
4. Enriquecer con CVSS, EPSS, KEV y criticidad.
5. Priorizar y asignar propietario.
6. Definir remediación o mitigación temporal.
7. Probar cambio y rollback.
8. Retest con mismo criterio de detección.
9. Cerrar o renovar excepción con justificación.

## Laboratorio seguro
Repositorio de prueba con dependencias vulnerables conocidas y fixtures locales. Ejecutar SCA/SAST, priorizar usando datos de vulnerabilidad sintéticos y corregir versión. No escanear rangos externos ni explotar CVEs en producción.

## Evaluación
Hallazgos tienen propietario, prioridad contextual, SLA, evidencia, retest y cierre. Métricas distinguen tiempo de detección, remediación y exposición real.

## Referencias y herramientas
FIRST CVSS, EPSS, CISA KEV, NVD, CWE, OSV, OWASP, DefectDojo, Trivy, Grype, pip-audit y Semgrep.

## Instrucciones para agentes IA
No uses CVSS como única prioridad. No ejecutes PoC contra producción. Distingue hallazgo confirmado, potencial y falso positivo; documenta la evidencia que falta.

## Arquitectura
El flujo de gestión de vulnerabilidades une inventario/CMDB y descubrimiento → fuentes de vulnerabilidad y exposición → normalización y deduplicación → enriquecimiento (CVE, CPE, CVSS, EPSS, KEV, exposición y criticidad) → priorización → ticket/propietario/SLA → remediación o excepción → verificación y cierre. Mantener sincronía entre activos, software, nube, endpoints y dependencias; registrar cobertura y activos desconocidos. Separar escaneo autenticado/no autenticado y pruebas activas de la toma de decisiones de riesgo.
