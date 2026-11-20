# Dictamen de auditoría interna — Foundations

**Fecha de corte:** 2026-11-19  
**Rama:** `knowledge/develop-foundations`  
**Commit auditado:** `f1d9f3bf8e6fa76e5f11c954d552da3e49c90a32`  
**Estándar:** `knowledge/EXPERT_RESEARCH_STANDARD.md`  
**Estado del dictamen:** **CERRADO — NO APROBADO PARA PROMOCIÓN**  
**Madurez:** `M2_editorial_draft_only`

## 1. Decisión ejecutiva

La auditoría interna de Foundations queda cerrada en esta iteración con resultado **no conforme para aceptación experta**. El contenido documental, los laboratorios sintéticos y la integración CI muestran avance verificable, pero no satisfacen las condiciones de evidencia necesarias para declarar el módulo superado.

No se cambia ningún estado a `passed` por inferencia. No se declara K3/K4/K5, M3/M4/M5, validación científica, eficacia operacional ni revisión independiente.

Este dictamen cierra el ciclo de inspección y deja un plan de salida verificable; **no equivale a cerrar satisfactoriamente la aceptación del módulo**.

## 2. Alcance y cobertura inspeccionada

Se verificaron los siete temas de Foundations:

1. Modelos de seguridad y confianza.
2. Inventario y clasificación de activos.
3. Superficie de ataque y modelado de amenazas.
4. Identidad y control de acceso.
5. Criptografía y protección de datos.
6. Detección, respuesta y recuperación.
7. Gobierno, riesgo y aseguramiento.

La matriz contiene 7 temas × 12 capas = **84 celdas**. En el commit auditado, las 84 están en `in_progress`; ninguna está aprobada. Los dossiers específicos existen en `FOUNDATIONS_DEEP_DEVELOPMENT_V1.md`, con límites, modelos, procedimientos, hipótesis, métricas y trazabilidad. La presencia de esos apartados acredita desarrollo editorial, no la suficiencia técnica de cada capa.

## 3. Evidencia técnica comprobada

### 3.1 Laboratorios locales sintéticos

El repositorio incluye siete laboratorios deterministas y un archivo de resultados:

- LAB-FND-01A: revocación e invalidación de autorización cacheada.
- LAB-FND-02A: reconciliación de activos; compara hostname con identificador estable.
- LAB-FND-03A: representación de rutas de amenaza en un grafo sintético.
- LAB-FND-04A: validación simulada de claims de identidad.
- LAB-FND-05A: integridad/autenticidad HMAC-SHA-256.
- LAB-FND-06A: ordenación y deduplicación de eventos.
- LAB-FND-07A: rechazo de cierres de controles con evidencia insuficiente.

El resultado registrado indica 7/7 grupos de comprobaciones correctos; la suite incluye 8 pruebas unitarias. El experimento de activos usa 250 activos y 500 registros sintéticos: el baseline por hostname produce 40 falsos merges y F1=0.9259; el identificador estable produce F1=1.0 dentro de ese generador. Esto **no** prueba que el método generalice a inventarios reales.

Límites relevantes:
- El lab de identidad no verifica firmas JWT ni implementa OAuth/OIDC.
- El lab criptográfico no implementa cifrado, AES, KMS ni validación FIPS.
- Las rutas del grafo no demuestran explotabilidad.
- El dataset de activos es sintético y controlado.
- No hay benchmark con población real, muestra externa ni estimación de incertidumbre poblacional.

### 3.2 CI del commit auditado

Los tres check-runs asociados al SHA auditado terminaron en éxito:

| Check | Run | Resultado |
|---|---:|---|
| sandbox-smoke | 44608392869 | success |
| unit-tests | 44608392741 | success |
| unit-tests | 44608378530 | success |

En `sandbox-smoke` finalizaron correctamente construcción de imágenes, verificación local, Ruff dentro del sandbox y carga de evidencia. En `unit-tests` finalizaron validación de sintaxis, verificación local, captura de hashes de wheels, SBOM CycloneDX y carga de SBOM/provenance.

Esto verifica el pipeline de software ejecutado en ese SHA. **No certifica la exactitud científica de la biblioteca ni sustituye revisión de contenido.**

### 3.3 Revisión independiente del PR

Al corte de esta auditoría, el PR #14 no registra reviews ni comentarios de revisión. Por tanto, no existe evidencia de revisión disciplinar independiente en GitHub.

## 4. Resultado de las ocho puertas

| Puerta | Estado | Evidencia actual | Condición de salida |
|---|---|---|---|
| G1 Cobertura | in_progress | 7 temas × 12 capas identificados; matriz explícita | Evaluación de suficiencia y dependencias por un revisor de dominio |
| G2 Fuentes | in_progress | Secciones pertinentes de fuentes primarias inspeccionadas y trazadas | Completar lectura dirigida/integral según criticidad, versiones, erratas, licencias y hashes de artefactos |
| G3 Profundidad | in_progress | Dossiers específicos por tema | Contrastar mecanismos, casos límite y exactitud con fuentes completas y revisión técnica |
| G4 Aplicación | in_progress | Procedimientos y siete simulaciones | Implementaciones reales en laboratorio aislado, con configuración y rollback |
| G5 Experimentación | in_progress | Siete labs sintéticos ejecutados localmente | Experimentos con controles reales o prototipos fieles, datos, baselines y amenazas a validez |
| G6 Evaluación | in_progress | Métricas y ocho tests de software | Evaluación conceptual/práctica del conocimiento y benchmarks válidos con incertidumbre |
| G7 Reproducibilidad | in_progress | Runner determinista, seed y CI | Reproducción desde entorno limpio por otro operador; hashes y resultados independientes |
| G8 Revisión independiente | blocked | No hay review externa registrada | Revisor competente sin autoría del trabajo, observaciones, resolución y aprobación explícita |

No hay puertas aprobadas. G8 permanece bloqueada por ausencia de revisor independiente, no por una tarea que pueda resolverse autoevaluándose.

## 5. Actualización de vigencia de fuentes

La revisión de fuentes debe incorporar dos advertencias de vigencia:

- NIST SP 800-57 Part 1 Rev. 5 es la publicación final identificada, pero NIST anunció un borrador inicial de Rev. 6 el 5 de diciembre de 2025, con periodo de comentarios hasta el 5 de febrero de 2026. La biblioteca debe comparar el borrador y cualquier publicación posterior antes de fijar políticas actuales de gestión de claves.
- NIST FIPS 203 mantiene una nota oficial del 17 de noviembre de 2025 sobre un problema identificado que se corregirá en una futura actualización/revisión. La errata potencial debe formar parte del control de vigencia; no se debe tratar el estándar como inmutable.

La ficha oficial de OWASP ASVS identifica 5.0.0 como versión estable publicada el 30 de mayo de 2025. Esto confirma versión y estado estable, no lectura completa del catálogo de requisitos.

## 6. No conformidades que bloquean la aceptación

**NC-01 — Evidencia de fuentes incompleta.** La revisión se limita a secciones pertinentes y metadatos en varias fuentes. No existe lectura completa acreditada para todos los documentos críticos.

**NC-02 — Brecha entre simulación y aplicación.** Los siete laboratorios son sintéticos. No prueban integración ni comportamiento con implementaciones reales.

**NC-03 — Sin reproducción independiente.** La repetición local en CI no es una réplica realizada por otro operador independiente.

**NC-04 — Sin evaluación externa del conocimiento.** No hay examen ciego, revisión de un especialista externo ni validación de que un profesional pueda aplicar correctamente los procedimientos.

**NC-05 — G8 bloqueada.** El PR no tiene reviews independientes registradas.

**NC-06 — Skills no validadas.** Las Skills candidatas no deben promoverse a procedimientos operativos aprobados.

## 7. Plan de cierre para superar la auditoría

La aceptación solo podrá reconsiderarse cuando exista evidencia adjunta para cada punto:

1. **Fuentes:** completar revisión dirigida de los documentos normativos críticos y registrar páginas/secciones, versión, erratas, fecha, licencia y SHA-256 de cada artefacto archivado. Prioridad: NIST SP 800-57 Rev. 5 frente al borrador Rev. 6, FIPS 203 y erratas, SP 800-53 Release 5.2.0, OWASP ASVS 5.0.0 y MITRE ATT&CK versión fijada.
2. **Implementación:** ejecutar pruebas con componentes reales o prototipos fieles en laboratorio aislado, con versiones, configuración, datos sintéticos/permitidos, controles de seguridad, resultados brutos, limpieza y rollback.
3. **Evaluación:** definir ground truth, baselines y métricas por tema; medir falsos positivos/negativos, incertidumbre y amenazas a validez donde aplique.
4. **Reproducción:** entregar entorno reproducible y pedir a un segundo operador que ejecute sin depender de instrucciones verbales del autor; conservar diferencias y resultados.
5. **Evaluación de competencia:** preparar rúbricas y ejercicios por tema que evalúen comprensión, diagnóstico y ejecución, no memorización.
6. **Revisión externa:** obtener revisión por especialista independiente; registrar identidad profesional/afiliación si autoriza, alcance, conflictos de interés, observaciones, respuestas y disposición final.
7. **Promoción:** actualizar las 84 celdas y G1–G8 solo con evidencias enlazadas y verificadas. La promoción se realiza por tema/capa; no por promedio ni por el éxito del pipeline.

## 8. Criterio de reentrada y no-regresión

La próxima auditoría debe partir de este dictamen y de los artefactos existentes. No borrar hallazgos negativos ni reemplazar resultados históricos: agregar una nueva iteración fechada. Un hallazgo solo se cierra con evidencia verificable, responsable, fecha y criterio de aceptación satisfecho.

Foundations no se considera terminado y no se inicia la aceptación del siguiente módulo hasta resolver las no conformidades que afectan a sus siete temas. El PR #14 permanece draft/open; `main` no se modifica y no se realiza merge.

## 9. Fuentes oficiales de control de vigencia

- NIST SP 800-57 Part 1 Rev. 5: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- NIST Key Management Guidelines (incluye aviso del borrador Rev. 6): https://csrc.nist.gov/Projects/key-management/key-management-guidelines
- NIST FIPS 203 y nota de erratas potenciales: https://csrc.nist.gov/pubs/fips/203/final
- OWASP ASVS 5.0.0: https://asvs.owasp.org/
