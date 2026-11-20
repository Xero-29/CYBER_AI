# Foundations — Mapa de cobertura por las doce capas obligatorias

**Corte:** 2026-11-20  
**Alcance:** FND-01.01, FND-01.02 y FND-01.03, primeros tres subtemas del currículo.  
**Regla:** la presencia de un documento no equivale a que una capa esté aprobada. Los estados se mantienen en progreso y T0/O0 hasta cumplir la evidencia exigida.

## 1. Mapeo de capas

| Capa | Requisito del estándar | FND-01.01 | FND-01.02 | Brecha que impide promoción |
|---|---|---|---|---|
| L1 Fundamentos teóricos | vocabulario, definiciones, principios, supuestos y límites | Topic FND-01.01 + crosswalk §§1–3 | Topic FND-01.02 + synthesis §§1–3 | contraste integral de fuentes y revisión independiente |
| L2 Matemáticos/formales | modelos, probabilidades, lógica, métricas y supuestos | crosswalk §4: riesgo, confiabilidad, disponibilidad y resiliencia | synthesis: CIA, autenticidad, integridad, métricas y evidencia | formalización más rigurosa por sistema/sector; ejemplos resueltos y sensibilidad |
| L3 Arquitectura/funcionamiento | componentes, flujos, interfaces, estados, dependencias y confianza | topic §2; crosswalk §§5–6 | synthesis §§4–6 | diagramas completos y arquitectura de referencia por sector |
| L4 Estándares/metodologías | versiones, alcance, selección, diferencias y límites | crosswalk §7; source registry | synthesis §8; source registry | lectura integral de normas y mapeo cláusula-requisito-control |
| L5 Implementación técnica | algoritmos, configuraciones, diagramas y resultados esperados | patrones fail-safe/fail-secure, acceso de emergencia, telemetría y recuperación; prototipos sintéticos LAB-FND-08A a LAB-FND-13A ejecutados en CI | mecanismos de firma, PKI, logs, control de acceso, integridad y freshness; LAB-FND-09A, LAB-FND-12A y LAB-FND-13A como modelos sintéticos | pseudocódigo/arquitecturas de referencia, configuraciones seguras y análisis estático; sin ejecución real |
| L6 Análisis avanzado | casos límite, fallos, trade-offs y causa raíz | crosswalk §5 y casos A–D | synthesis §§4, 5 y 7 | análisis cuantitativo y casos sectoriales adicionales |
| L7 Perspectiva de seguridad | amenazas, abuso, prevención, detección, respuesta y recuperación | threat/hazard/privacy/failure model en topic y crosswalk | controles CIA, autenticidad, accountability, privacidad y casos de abuso | threat model formal y trazabilidad amenaza-control-evidencia por arquitectura |
| L8 Investigación científica | estado del arte, pregunta, brecha, hipótesis, protocolo y validez | RESEARCH_AGENDA + LITERATURE_REVIEW + crosswalk | RESEARCH_AGENDA + LITERATURE_REVIEW + synthesis | lectura integral, protocolo de investigación detallado y revisión independiente |
| L9 Laboratorios/datasets | entorno autorizado, procedencia, esquema, baseline, hashes y resultados | laboratorios sintéticos LAB-FND-08A a LAB-FND-12A ejecutados en CI; no hay prueba física, equipo real ni validación operacional | escenarios sintéticos LAB-FND-09A y LAB-FND-12A ejecutados en CI; laboratorio con datos/ground truth sectoriales pendiente | dataset/corpus con ground truth, baseline, hashes, scripts y resultados esperados específicos por subtema |
| L10 Evaluación/benchmarks | métricas, umbrales, incertidumbre y criterios de aprobación | instrumento FND-01-01 V2 preparado, no administrado | instrumento FND-01-02 V1 preparado, no administrado | administración en frío, respuestas originales, segundo evaluador y adjudicación |
| L11 Conocimiento operativo | Skills versionadas, precondiciones, permisos, validaciones y rollback | Skill candidata de análisis integrado indexada; no activa ni registrada en skillbook | Skill candidata de evaluación CIA indexada; no activa ni registrada en skillbook | especificación de Skill y pruebas de aceptación; no promover sin evidencia |
| L12 Trazabilidad/mantenimiento | fuentes, autoría, versión, licencia, hashes, revisión y obsolescencia | source registry de 218 IDs, crosswalk, auditoría V2, logs y hash de documentos | source registry de 218 IDs, synthesis, instrumento de evaluación y auditoría V2 | lectura integral, licencia validada, revisión independiente y actualización periódica |

## 2. Estado por subtema

### FND-01.01 — Seguridad, safety, privacidad, confiabilidad y resiliencia

**Avance documental:** crosswalk disciplinar incorporado; distingue propiedades, modelos de riesgo, interacciones, métodos, métricas, estándares y aplicabilidad colombiana condicionada. Se registran metadatos y estados de revisión de NIST, NASA, IEC e ISO.

**Pendiente crítico:** lectura integral de NIST SP 800-160 Vol. 1 Rev. 1 y Vol. 2 Rev. 1 y fuentes esenciales; análisis de confiabilidad y safety con modelos contrastados; revisión jurídica/sectorial colombiana; evaluación supervisada; revisión independiente.

### FND-01.02 — Propiedades de seguridad y CIA extendida

**Avance documental:** síntesis primaria, matriz CIA y propiedades relacionadas, contraejemplos, mecanismos, límites de autenticidad/non-repudiation y evaluación en frío preparada.

**Pendiente crítico:** full-text review de fuentes primarias; escenarios y laboratorio específico; administración del instrumento; segundo evaluador; mapeo de controles a arquitectura y evidencia.

## 3. Reglas de estado

- L1–L12 siguen in_progress en ambos subtemas.
- Ninguna capacidad se marca passed.
- La madurez teórica y operativa sigue T0/O0.
- Un instrumento preparado no es una evaluación administrada.
- Un laboratorio sintético diseñado no es un laboratorio ejecutado.
- Un metadato o abstract oficial no equivale a lectura integral.
- T4 requiere revisión disciplinar independiente; T5 requiere contribución o síntesis de investigación rigurosa.

## 4. Próximo trabajo

1. Terminar remediación documental de FND-01.01 y FND-01.02 sin cerrar artificialmente las no conformidades externas.
2. Desarrollar FND-01.03 y siguientes en el orden del currículo, aplicando desde el inicio las doce capas.
3. No abrir AI Red Team hasta que Foundations tenga sus 102 subtemas desarrollados en frío o una excepción explícita y justificada.


### FND-01.03 — Activo y misión

- L1–L12: contenido de borrador presente en `topics/FND-01-03_ASSET_SUBJECT_OBJECT_RESOURCE_DATA_PROCESS_SERVICE_MISSION_STAKEHOLDER.md`.
- L9: LAB-FND-13A detecta ownership ausente, registros obsoletos, datos sin clasificar, criticidad alta sin logging y soporte desconocido; ejecutado en CI como simulación sintética.
- L10: instrumento en frío V1 preparado, no administrado.
- L11: Skill candidata de inventario orientado a misión indexada, no activa.
- L12: fuentes, estados de revisión, evidencia y hashes registrados.
- Todas las capas permanecen in_progress; 0 aprobadas; T0/O0.
