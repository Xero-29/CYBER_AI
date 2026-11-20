# Foundations — instrumento de evaluación de competencia v1

**Estado:** diseñado; todavía no administrado. **Tiempo sugerido:** 120–180 minutos.  
**Regla:** declarar supuestos, datos faltantes, límites, evidencia y riesgo residual. Separar hechos, inferencias e hipótesis.

## Rúbrica por tema (0–2 en cada dimensión; máximo 12)
1. Exactitud conceptual.
2. Modelo, alcance y supuestos.
3. Razonamiento y trade-offs.
4. Aplicación reproducible y segura.
5. Pruebas negativas y manejo de fallos.
6. Evidencia, trazabilidad, incertidumbre y límites.

0 = ausente/incorrecto/inseguro; 1 = parcial; 2 = correcto, justificado y trazable. Umbral propuesto: ≥10/12 sin ceros en exactitud, aplicación o evidencia. Es una regla interna no calibrada, no una norma externa.

## Tema 1 — Modelos de seguridad y confianza
- **A / comprensión:** distinguir security, safety, privacy, reliability, resilience y trustworthiness; explicar por qué Zero Trust no es un producto ni equivale a RBAC/ABAC; diferenciar requisito, política, mecanismo y enforcement.
- **B / diagnóstico:** API cachea decisiones de autorización 30 minutos; usuario pierde privilegios y una ruta interna omite el gateway. Modelar activos, identidades, fronteras, flujos, bypass y datos faltantes.
- **C / aplicación:** diseñar matriz de pruebas de autorización contextual: allow/deny, revocación, atributos mutables, expiración, rutas alternativas, caché, fail-open/closed, logs y rollback.

## Tema 2 — Inventario y clasificación
- **A:** diferenciar activo, recurso, identidad, servicio, dependencia, owner, custodian y fuente de verdad; explicar por qué hostname/IP no son IDs estables.
- **B:** cloud, EDR y CMDB reportan 600 registros con instancias efímeras, clones, renombrados y fuentes correlacionadas. Diseñar reconciliación y tratar incertidumbre/doble conteo.
- **C:** esquema de inventario con ID estable, aliases, procedencia, timestamps, owner, criticidad, clasificación, relaciones, confianza y ciclo de vida; reglas de matching, revisión manual, sanitización y métricas false-merge/false-split.

## Tema 3 — Superficie de ataque y amenazas
- **A:** comparar DFD, STRIDE, attack trees, FMEA y ATT&CK; explicar por qué ATT&CK no es probabilidad ni catálogo exhaustivo.
- **B:** aplicación pública con API, IdP, cola, worker, runner CI, gestor de secretos y DB; atacante obtiene cuenta de desarrollador. Modelar rutas adversariales y fallos no maliciosos.
- **C:** entregar DFD, fronteras, tabla de amenazas, attack graph, precondiciones, controles, evidencia y pruebas negativas; distinguir ruta modelada de explotabilidad demostrada.

## Tema 4 — Identidad y acceso
- **A:** explicar firma vs claims, issuer, audience, exp, nbf, scope, jti, PKCE, redirect URI exacta, refresh rotation y sender-constrained tokens.
- **B:** servicio acepta tokens sin restringir audience; otro confía en header de rol enviado por cliente. Analizar confused deputy, replay y elevación.
- **C:** diseñar verificador y tests para firma alterada, alg no permitido, issuer/audience, exp/nbf, scope, revocación, JSON duplicado y rotación de claves; no incrustar secretos.

## Tema 5 — Criptografía y protección de datos
- **A:** diferenciar hash, HMAC, AEAD, firma digital, KEM y KDF; explicar por qué HMAC no cifra y ML-KEM no es cifrado bulk.
- **B:** aplicación cifra contraseñas con clave compartida, usa SHA-256 simple para autenticidad y rota clave sin versionar ciphertext. Identificar fallos y riesgos de migración.
- **C:** plan de claves: generación, almacenamiento, acceso, uso, rotación, revocación, backup, recuperación, destrucción y compromiso; incluir pruebas de manipulación y rotación.

## Tema 6 — Detección, respuesta y recuperación
- **A:** integrar respuesta con Govern, Identify, Protect, Detect, Respond, Recover e Improvement del CSF 2.0.
- **B:** cuenta privilegiada usada desde ubicación atípica, lectura de secretos y cambio de producción; logs con desfase, duplicados y retención desigual. Construir hipótesis y timeline con incertidumbre.
- **C:** playbook con severidad, roles, preservación, contención segura, comunicación, recuperación validada, criterios de retorno, retest y métricas.

## Tema 7 — Gobierno, riesgo y assurance
- **A:** diferenciar control diseñado, implementado, operado y eficaz; explicar claim-argument-evidence y los siete pasos RMF.
- **B:** control declarado eficaz con política de hace 18 meses y sin evidencia operacional; test reciente contradice la política. Decidir si puede cerrarse y quién acepta riesgo.
- **C:** construir assurance case con claim, contexto, argumento, evidencia, supuestos, derrotadores, owner, vigencia y riesgo residual.

## Protocolo de administración
- Evaluador distinto del autor; declarar cualificación y conflictos.
- Para evaluación ciega, entregar solo esta hoja y mantener la clave separada.
- Registrar versión, fecha, duración, entorno, ayudas permitidas y puntuación por dimensión con evidencia concreta.
- Usar un segundo caso equivalente para comprobar consistencia; no reutilizar literalmente casos ya vistos.
- El instrumento diseñado no demuestra por sí solo que el contenido sea correcto ni que alguien sea experto.
