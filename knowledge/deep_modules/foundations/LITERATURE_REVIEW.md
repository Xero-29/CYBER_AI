# Revisión de literatura exploratoria — Fundamentos de ciberseguridad

**Corte:** 2026-11-17  
**Madurez:** M1 (páginas oficiales y abstracts inspeccionados para tres referencias adicionales); **no M2 consolidado/M3/M4/M5**.  
**Alcance:** revisión exploratoria inicial y protocolo de investigación.  
**Procedencia:** la referencia nueva se localizó en el sitio del emisor, pero su texto completo no se declara leído. No es revisión sistemática ni validación empírica.

## Pregunta

¿Cómo conectar activos, amenazas, debilidades, controles, evidencia y riesgo residual?

## Síntesis

NIST CSF estructura resultados; RMF conecta categorización, selección, implementación, evaluación y monitoreo; NICE organiza competencias. Ningún marco reemplaza análisis contextual ni demuestra eficacia. Distinguir amenaza, vulnerabilidad, exposición, impacto, probabilidad, control, evidencia e incertidumbre.

**Lectura crítica:** los marcos ordenan riesgos y requisitos, pero no prueban que un control esté desplegado o reduzca incidentes. Separar evidencia normativa, documentación de implementación, estudios empíricos y resultados del laboratorio. No atribuir a las fuentes contenido no examinado.

## Taxonomía técnica

Activos; trust boundaries; threat actors; attack surface; likelihood/impact; assurance; residual risk.

## Hipótesis falsable

- **H1:** una evaluación estructurada y basada en escenarios del dominio detectará más fallos reproducibles que una revisión superficial basada solo en checklist.
- **H0:** la diferencia no es significativa bajo muestra y protocolo definidos.
- Son hipótesis propuestas, no resultados.

## Diseño experimental propuesto (no ejecutado)

Caso sintético multi-sistema; modelar riesgos con matrices y grafo relacional; medir trazabilidad y duplicados.

Fijar versiones, commit, configuración, dataset, semillas y criterios antes de ejecutar; repetir; registrar desviaciones; conservar evidencia saneada. Usar solo activos propios o autorizados, con criterios de parada y rollback.

## Métricas

Cobertura activos; enlaces verificables; inconsistencias; riesgos sin dueño; evidencia vencida.

## Amenazas a la validez y límites

- **Externa:** un laboratorio no representa automáticamente otros proveedores, arquitecturas o sectores.
- **Interna:** controlar versiones, instrumentación, selección de muestras y variables de confusión.
- **Constructo:** distinguir alertas, cobertura y puntuaciones de resultados reales de seguridad.
- **Reproducibilidad:** conservar scripts, hashes, datos sintéticos, versiones y pasos.
- **Ética:** autorización, minimización, alcance, parada y divulgación coordinada.

## Brechas y trabajo siguiente

1. Leer íntegramente las referencias primarias y registrar edición, fecha, hash, páginas revisadas y licencia.
2. Incorporar artículos revisados por pares con criterios de inclusión/exclusión reproducibles.
3. Contrastar la síntesis con especialistas y documentar desacuerdos.
4. Ejecutar el protocolo en laboratorio autorizado y publicar resultados negativos y análisis de incertidumbre.
5. No elevar a M4 sin experimento ejecutado y analizado; no elevar a M5 sin revisión independiente y reproducción externa.

## Límite de madurez empírica

**Límite explícito: no M3/M4/M5.** Esta revisión está en M1 exploratorio: se inspeccionaron páginas oficiales y abstracts, pero no se ha completado lectura integral de todas las fuentes, revisión sistemática con criterios reproducibles, experimento ejecutado, análisis de resultados, revisión independiente ni reproducción externa. El diseño experimental descrito es una propuesta, no un resultado. No elevar la madurez hasta que existan esas evidencias.

## Referencias y procedencia

| ID | Referencia | Estado editorial en este repositorio |
|---|---|---|
| `NIST-CSWP-29-CSF-2.0` | NIST Cybersecurity Framework 2.0 | Página oficial y abstract inspeccionados; texto completo pendiente |
| `NIST-SP-800-30r1` | NIST Guide for Conducting Risk Assessments | Página oficial y abstract inspeccionados; texto completo pendiente |
| `NIST-SP-800-53r5` | NIST Security and Privacy Controls | Página oficial y abstract inspeccionados; texto completo pendiente |
| `CIS-CONTROLS-v8.1` | CIS Critical Security Controls 8.1 | Página oficial inspeccionada; descarga, términos y lectura integral pendientes |
| `RESEARCH-FOUNDATIONS` | NIST Risk Management Framework (SP 800-37 Rev. 2) | Referencia localizada; texto íntegro pendiente |

## Identificadores del registro de fuentes

- `NIST-CSWP-29-CSF-2.0`
- `NIST-SP-800-30r1`
- `NIST-SP-800-53r5`
- `CIS-CONTROLS-v8.1`
- `RESEARCH-FOUNDATIONS`


## Alcance real de la revisión editorial

El 2026-11-19 se inspeccionaron las páginas oficiales de NIST CSF 2.0, NIST SP 800-30 Rev. 1, NIST SP 800-53 Rev. 5 y CIS Controls v8.1. Esta inspección confirma identidad bibliográfica, alcance declarado y estado editorial de las publicaciones; **no equivale a lectura integral de los documentos ni a extracción de requisitos por página**. Los estados del registro reflejan exactamente esa limitación. No se usaron estas páginas como evidencia de eficacia de controles en una organización.
