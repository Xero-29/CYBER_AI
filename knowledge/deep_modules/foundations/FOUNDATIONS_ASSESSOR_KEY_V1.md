# Foundations — clave de corrección v1 (evaluadores)

**No entregar antes de finalizar la prueba.** Respuestas equivalentes bien argumentadas pueden recibir puntuación completa.

## Tema 1
- A: distinguir las seis propiedades; Zero Trust es enfoque de decisión contextual; RBAC/ABAC son modelos de autorización; requisito ≠ política ≠ mecanismo ≠ enforcement.
- B: caché stale, revocación tardía, gateway bypass, inconsistencias y rutas internas.
- C: tests allow/deny, revocación, cambio de atributos, expiración, caché, timeout PDP/PEP, fail-open/closed y evidencia de logs.

## Tema 2
- A: ID canónico separado de alias mutable; owner/custodian y lineage distintos.
- B: fuentes correlacionadas no son evidencia independiente; ID estable, snapshots temporales, activos efímeros y sin agente.
- C: provenance, confianza, vigencia, precision/recall/F1, false merge/split, revisión humana y sanitización validada.

## Tema 3
- A: DFD=flujos/confianza; STRIDE=clases; attack tree=descomposición; FMEA=fallos; ATT&CK=tradecraft observado versionado, no probabilidad.
- B: credencial developer puede afectar CI/CD, secrets, workers y deploy; incluir causas no adversariales.
- C: rutas, precondiciones, controles, cobertura, derrotadores; no afirmar explotabilidad por una ruta dibujada.

## Tema 4
- A: verificar firma antes de confiar en claims; issuer/audience exactos; exp/nbf; scope mínimo; PKCE S256; redirect URI exact matching; refresh reuse detection; sender constraint reduce replay pero no elimina compromiso del cliente.
- B: audience confusion, rol controlado por cliente, replay, confused deputy y revocación ausente.
- C: negativos de firma, alg none/alg confusion, issuer/audience, exp/nbf, scope, jti, JSON duplicado, kid desconocido y rollover JWKS.

## Tema 5
- A: hash no autentica; HMAC autentica con secreto compartido pero no cifra ni ofrece no repudio; AEAD protege confidencialidad/integridad; firma asimétrica; KEM establece secreto; KDF deriva claves.
- B: contraseñas requieren password hashing lento y salado, no cifrado reversible; SHA-256 simple no autentica; versionar claves y ciphertext.
- C: ciclo de vida, separación de funciones, backup/recovery, compromiso, envelope encryption, validación de algoritmo y test vectors.

## Tema 6
- A: IR integrada a gestión de riesgo y CSF 2.0; no es solo actividad del SOC.
- B: preservar originales, hashes, zonas horarias, calidad de fuente, desfase y duplicados; distinguir observación/inferencia; no destruir evidencia al contener.
- C: roles, severidad, contención con trade-offs, cadena de custodia, comunicación, validación de recuperación y mejora.

## Tema 7
- A: diseño/implementación/operación/eficacia son estados distintos; claim-argument-evidence; Prepare/Categorize/Select/Implement/Assess/Authorize/Monitor.
- B: política no demuestra operación; test contradictorio es derrotador; no cerrar control; elevar al owner/autoridad de riesgo.
- C: claim acotado, evidencia vigente/auténtica/con alcance, supuestos y derrotadores explícitos; aceptación formal de riesgo residual.

## Calificación
0 ausente/incorrecto/inseguro; 1 parcial; 2 correcto, aplicado y justificado. No dar 2 por repetir palabras clave. Cero en exactitud, aplicación o evidencia bloquea el tema. El umbral ≥10/12 es provisional: calibrarlo con dos evaluadores y respuestas piloto antes de adoptarlo como criterio definitivo.

## Registro del evaluador
Cualificación; conflictos; fecha; versión; tema/caso; puntuación por dimensión; evidencia concreta; desacuerdos; decisión pass/revise/fail; limitaciones.
