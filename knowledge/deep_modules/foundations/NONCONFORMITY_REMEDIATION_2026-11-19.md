# Remediación de no conformidades — Foundations

**Fecha:** 2026-11-19  
**Base:** dictamen `FOUNDATIONS_AUDIT_VERDICT_2026-11-19.md`  
**Rama:** `knowledge/develop-foundations`

Este documento registra correcciones y evidencia nueva. No borra el dictamen previo ni cambia automáticamente puertas a `passed`.

## Resumen de estado

| NC | Acción de esta iteración | Resultado |
|---|---|---|
| NC-01 Fuentes incompletas/vigencia | Añadido control de versiones y cambios oficiales para SP 800-57 Rev. 6 IPD, FIPS 203 errata, SP 800-53 5.2.0, ASVS 5.0.0 y ATT&CK v20.1 | Parcial: metadatos/changelog trazados; lectura integral sigue pendiente |
| NC-02 Simulación vs implementación | JWS HS256 real con verificación de firma y claims; cadena de auditoría HMAC con detección de alteración/reordenamiento; assurance exige evidencia estructurada | Parcial: prototipos locales fieles; sin IdP/KMS/SIEM externo |
| NC-03 Reproducción independiente | CI dedicado en runners limpios Python 3.11/3.12/3.13 y comparación exacta contra results.json | Parcial: reproducibilidad multi-runtime CI; segundo operador externo aún pendiente |
| NC-04 Evaluación de conocimiento | Añadida rúbrica de evaluación práctica y casos negativos como base para evaluación ciega | Diseño; no hay evaluador ni resultados de participantes |
| NC-05 Revisión externa | Definido paquete de revisión y checklist para tercero | Bloqueada hasta que una persona independiente revise y emita dictamen |
| NC-06 Skills no validadas | Se mantienen como candidatas; promoción exige pruebas negativas, límites, permisos, rollback, evidencia y revisión | No promovidas |

## NC-01 — Registro de fuentes y control de vigencia

### NIST SP 800-57 Part 1
- Rev. 5 sigue siendo la publicación final identificada en el registro consultado.
- Rev. 6 Initial Public Draft se publicó el 2025-12-05; el periodo de comentarios cerró el 2026-02-05.
- El IPD incluye propuestas relativas a Ascon, algoritmos post-cuánticos FIPS 203/204/205 y distinción de claves para establecimiento y almacenamiento.
- Decisión: no reemplazar Rev. 5 por un borrador. Mantener ambas entradas, etiquetar IPD y revalidar cuando NIST publique una revisión final.

### FIPS 203
NIST mantiene una nota de planificación del 2025-11-17 que indica un problema identificado para corrección en futura actualización/revisión y enlaza hoja de erratas potenciales. La biblioteca lo registra como aviso de errata pendiente de inspección del spreadsheet y seguimiento, no como estándar inmutable.

### SP 800-53 Release 5.2.0
La revisión de la nota de cambios identifica, entre otros, SA-24 Design for Cyber Resiliency, SA-15(13) Logging Syntax, SI-02(07) Root Cause Analysis y cambio en SI-07(12). El registro marca explícitamente que no se leyó el catálogo completo.

### OWASP ASVS 5.0.0
La página oficial confirma publicación estable el 2025-05-30 y descargas PDF/DOCX/CSV. El registro no convierte esto en lectura de todos los requisitos.

### MITRE ATT&CK v20.1
La versión oficial actual a fecha de revisión es v20.1 (2026-10-13). Se añadió referencia a las release notes de octubre 2026; las cifras/cambios de catálogo no se usan como probabilidades ni como prueba de aplicabilidad universal.

## NC-02 — Implementaciones de referencia ejecutables

### LAB-FND-04A: JWS HS256
Implementa con la biblioteca estándar: parser JSON estricto que rechaza miembros duplicados; algoritmo HS256 y typ JWT explícitos; verificación HMAC con comparación de tiempo constante; issuer/audience; exp/nbf; scope; jti/revocación; y casos negativos de firma alterada, alg none, claims incorrectos, expiración, not-before, scope, revocación y formato.

**Límite:** prototipo de verificación HS256. No implementa JWKS, rotación de claves, firmas asimétricas, discovery OIDC, nonce/state, TLS, servidor OAuth ni integración con IdP. La clave es fixture de laboratorio, no secreto de producción.

### LAB-FND-06A: cadena de auditoría HMAC
Cada evento se serializa canónicamente y se vincula al MAC anterior con secuencia monotónica. La verificación rechaza modificación de evento y reordenamiento.

**Límite:** integridad de la cadena mientras la clave permanezca protegida; no proporciona no repudio, timestamp confiable, protección tras compromiso de clave, SIEM ni garantías de entrega.

### LAB-FND-07A: evidencia estructurada
El cierre requiere control implementado, propietario, evidencia de tipo aceptado, alcance, hash SHA-256 sintácticamente válido, fecha vigente y ausencia de contradicción.

**Límite:** valida metadatos del fixture; no verifica por sí mismo el contenido del artefacto ni la identidad del emisor.

## NC-03 — Reproducción multi-runtime
Se añade job CI aislado para Python 3.11, 3.12 y 3.13. Cada ejecución usa runtime limpio, ejecuta tests y compara el resultado calculado con `labs/results.json`. Esto no se etiqueta como réplica independiente: los jobs proceden del mismo repositorio, autoría y definición de pruebas.

## NC-04 — Evaluación práctica propuesta
Cada tema tendrá tres ejercicios: (A) explicación/derivación de modelo, (B) diagnóstico con datos incompletos y supuestos, (C) ejecución de procedimiento y pruebas negativas. Criterios 0–2: conceptos, supuestos/incertidumbre, razonamiento técnico, controles/trade-offs, pruebas negativas/diagnóstico y evidencia/trazabilidad/límites. Aprobación propuesta: mínimo 10/12, sin cero en seguridad, supuestos o evidencia. Es una regla de evaluación propuesta, no norma externa ni resultado ya alcanzado. Falta evaluador y participantes reales.

## NC-05 — Paquete de revisión externa
El revisor debe declarar experiencia y conflictos; seleccionar al menos dos temas y muestra de capas; verificar citas/versiones/claims; ejecutar labs desde checkout limpio; cuestionar supuestos y validez; registrar defectos y severidad; emitir approve/request_changes/reject; y confirmar resolución/retest. No se puede autoadjudicar esta revisión. G8 sigue bloqueada hasta que una persona distinta del autor emita revisión.

## NC-06 — Gate de promoción de Skills
Ninguna Skill se promueve por documentación o un ejemplo feliz. Debe incluir precondiciones, permisos mínimos, I/O, pasos, pruebas negativas, límites, parada, rollback, logging, secretos, evidencias, versiones y owner. La promoción exige ejecución reproducible y revisión independiente. Las Skills siguen `candidate`.

## Próximos criterios de cierre
- NC-01: lectura técnica de fuentes prioritarias y claims por página/sección.
- NC-02: integrar IdP de laboratorio y stack de logs/KMS aislado, versiones fijadas, interoperabilidad y teardown seguro.
- NC-03: segundo operador en otro entorno con resultado registrado.
- NC-04: evaluación ciega real y análisis.
- NC-05: revisión externa efectiva y resolución.
- NC-06: no promover Skills hasta cumplir los gates.

**Estado general:** remediación parcial. G2, G4, G5, G6 y G7 permanecen en progreso; G8 bloqueada. No se cambia M2 ni se declara Foundations aprobado.
