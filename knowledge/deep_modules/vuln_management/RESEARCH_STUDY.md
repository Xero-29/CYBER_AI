# Investigación técnica: Gestión de vulnerabilidades y priorización basada en riesgo

**ID:** vuln_management · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 · **Validación con datos reales:** pendiente.

## El problema de priorización
La gestión de vulnerabilidades no es ordenar CVE por CVSS y parchear de mayor a menor. Debe combinar inventario, exposición, explotabilidad, evidencia de explotación, impacto técnico, criticidad del activo, controles compensatorios, disponibilidad de parche, ventana operacional y riesgo de negocio.

Distinguir: CVE identifica vulnerabilidades divulgadas; CWE modela clases de debilidad; CVSS expresa severidad técnica bajo supuestos definidos; EPSS estima probabilidad de explotación observada en 30 días; CISA KEV registra vulnerabilidades con evidencia de explotación conocida; riesgo local combina esas señales con contexto propio.

## Flujo de gestión
1. Descubrir activos/software con propietario, versión, exposición, criticidad y dependencia.
2. Ingerir CVE/advisories con timestamp, fuente, versión y hash.
3. Normalizar CPE/PURL/producto/versión; conservar ambigüedad y no asumir match por substring.
4. Correlacionar CVE con inventario, SBOM, configuración y exposición real.
5. Enriquecer con CVSS, EPSS, KEV, exploit maturity, advisory y contexto.
6. Validar aplicabilidad, precondiciones, configuración y mitigaciones.
7. Priorizar con política transparente y override justificado.
8. Remediar o aceptar temporalmente riesgo con owner, fecha y compensaciones.
9. Verificar parche/configuración y repetir prueba.
10. Medir backlog, aging, exposición y reincidencia.

## Interpretación de señales
### CVSS v4.0
CVSS 4.0 separa métricas Base, Threat, Environmental y Supplemental. Base describe severidad intrínseca; Threat y Environmental permiten ajustar con madurez de explotación y contexto; Supplemental agrega información que no cambia el score final. Guardar vector además de número para que el score sea interpretable.

### EPSS
EPSS estima probabilidad de explotación observada en los próximos 30 días, no probabilidad de impacto en una organización concreta. El score cambia diariamente: guardar snapshot, fecha, versión del modelo y método de consulta. No tratar score bajo como ausencia de riesgo.

### KEV
KEV es un catálogo oficial de vulnerabilidades con evidencia de explotación conocida. Tiene valor como señal de urgencia, pero no es inventario completo de explotaciones ni lista exhaustiva de vulnerabilidades peligrosas. Capturar snapshots fechados y revisar fechas/acciones recomendadas.

### Contexto
Ajustar por exposición externa, privilegios, ruta de ataque, datos, criticidad, compensaciones, segmentación, exploit disponible, alcance y ventana de remediación. En OT, medicina, automoción y safety-critical, parchear puede requerir pruebas de fabricante y ventanas; documentar medidas compensatorias y riesgo residual.

## Motor explicable
Evitar fórmula opaca que sume CVSS + EPSS + KEV sin calibración. Política transparente:
- KEV confirmado y activo expuesto: prioridad inmediata, tras validar aplicabilidad.
- Exploit observado y ruta alcanzable: elevar.
- Servicio internet-facing, identidad privilegiada o activo crítico: elevar.
- Vulnerabilidad no aplicable o mitigación probada: reducir con evidencia y caducidad.
- Parche de alto riesgo operacional: mitigación temporal, owner, fecha y plan de cambio.
- Datos incompletos: marcar prioridad provisional y disparar enriquecimiento.

Toda decisión registra señales, versiones, datos, explicación, responsable y override.

## Calidad de datos y falsos positivos
Errores frecuentes: CPE ambiguo, backport de distro, firmware no identificado, producto renombrado, advisory corregido, CVE duplicado, CVSS de proveedor distinto, versión prerelease y SBOM incompleto. Mantener estado unknown en vez de asumir vulnerable/no vulnerable.

Medir precision/recall de matching, falsos positivos, vulnerabilidades sin owner, porcentaje con versión validada, tiempo desde publicación hasta detección, tiempo hasta mitigación y KEV aplicables remediados dentro de SLA.

## Laboratorio reproducible
Dataset sintético de activos y CVE con versiones afectadas/no afectadas; casos de backport y versión ambigua; snapshots CVSS/EPSS/KEV con fecha y hashes; matching exacto vs normalización; simulación de activo crítico, exposición, compensación y excepción; ingestión de advisory corregido y feed offline. No explotar producción para comprobar aplicabilidad: preferir advisory, versión, SBOM, scanner autorizado y laboratorio.

## Fuentes
- FIRST CVSS v4.0: https://www.first.org/cvss/specification-document
- FIRST EPSS: https://www.first.org/epss/
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- NIST NVD: https://nvd.nist.gov/
- MITRE CWE: https://cwe.mitre.org/
- MITRE CVE: https://www.cve.org/

**Estado de evidencia:** especificación CVSS y páginas oficiales EPSS/KEV registradas; no se han descargado snapshots ni validado motor con inventario real.
