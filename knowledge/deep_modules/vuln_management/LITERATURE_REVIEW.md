# Revisión de literatura inicial — Gestión de vulnerabilidades

**Corte:** 2026-11-17  
**Madurez:** M1 documental; no M3/M4.  
**Alcance:** identificación, priorización, remediación, excepciones, verificación y riesgo residual.

## Pregunta

¿Cómo priorizar vulnerabilidades combinando evidencia de explotación, probabilidad, impacto y contexto real del activo, evitando tratar una puntuación aislada como riesgo organizacional completo?

## Síntesis de evidencia

- **EPSS (FIRST):** estima la probabilidad de observar explotación de una CVE en los siguientes 30 días; el score está entre 0 y 1 y se actualiza diariamente. EPSS no es un score de riesgo completo: no incorpora impacto local, exposición, controles compensatorios ni criticidad del activo.
- **CISA KEV:** catálogo de vulnerabilidades con evidencia de explotación conocida. Una CVE presente en KEV representa evidencia operativa que debe prevalecer sobre una probabilidad EPSS baja cuando la decisión es si existe explotación conocida.
- **CVSS:** expresa severidad técnica según una metodología/version; no reemplaza la evaluación contextual de exposición, impacto, probabilidad ni mitigaciones. En este dossier no se ha incorporado aún la especificación CVSS v4 completa; no usar fórmulas o campos no verificados.

## Modelo de decisión propuesto

1. **Confirmar exposición:** producto/versión, configuración, servicio alcanzable, activo afectado y propietario.
2. **Buscar evidencia de explotación:** KEV y fuentes de inteligencia confiables; registrar fecha de consulta.
3. **Estimar probabilidad:** EPSS con fecha/version de consulta, no como certeza ni como riesgo total.
4. **Evaluar impacto:** criticidad del activo, privilegios obtenibles, confidencialidad/integridad/disponibilidad, alcance lateral y obligaciones.
5. **Evaluar mitigaciones:** controles compensatorios demostrados, no supuestos.
6. **Decidir tratamiento:** parche, mitigación temporal, aislamiento, aceptación con expiración o excepción aprobada.
7. **Verificar:** retest técnico, inventario actualizado y evidencia de cierre.

No sumar mecánicamente CVSS + EPSS + KEV. Son señales de naturaleza diferente. KEV es evidencia de explotación conocida; EPSS es probabilidad modelada de explotación futura en 30 días; CVSS es severidad técnica. La decisión debe preservar cada señal y explicar cómo se combina con contexto.

## Hipótesis y experimento propuesto (no ejecutado)

- **H1:** una priorización que incorpora KEV, EPSS, exposición y criticidad produce menor tiempo hasta remediación de vulnerabilidades explotadas en un dataset retrospectivo que una priorización basada solo en CVSS.
- **H0:** no existe diferencia bajo el protocolo.
- **Dataset:** CVEs históricas con snapshots fechados de EPSS, KEV, severidad y un inventario sintético de activos; no usar datos privados.
- **Comparadores:** CVSS-only; KEV-first; modelo contextual transparente.
- **Métricas:** recall de vulnerabilidades explotadas dentro del top-k, precision@k, tiempo simulado de remediación, falsos positivos de exposición y calibración temporal de EPSS.
- **Controles:** evitar leakage temporal; cada decisión solo puede usar datos disponibles en su fecha de corte; separar entrenamiento/evaluación temporal.
- **Análisis:** curvas precision-recall, calibración, sensibilidad de umbrales y coste de oportunidad. Documentar desbalance de clases.

## Reglas operativas

- Una CVE no se considera aplicable hasta confirmar producto, versión, configuración y precondiciones.
- La ausencia de KEV no prueba ausencia de explotación.
- EPSS bajo no invalida evidencia directa de explotación.
- Un parche aplicado no cierra el hallazgo sin verificación posterior.
- Toda excepción tiene propietario, justificación, controles, expiración y revisión.
- La priorización no debe ocultar activos desconocidos: calidad del inventario es una variable crítica.

## Brechas

Incorporar revisión completa de CVSS v4 y snapshots históricos de KEV/EPSS; ejecutar evaluación retrospectiva sin fuga temporal y documentar la calidad del inventario de activos.

## Referencias

- FIRST, EPSS FAQ. https://www.first.org/epss/faq
- FIRST, EPSS How It Works. https://www.first.org/epss/how-it-works
- CISA, Known Exploited Vulnerabilities Catalog. https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- NIST, Vulnerability Management / NVD (referencia complementaria por desarrollar). https://nvd.nist.gov/


## Identificadores del registro de fuentes

- `FIRST-EPSS-FAQ`
- `FIRST-EPSS-METHOD`
- `CISA-KEV`
