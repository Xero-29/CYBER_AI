# Agenda de investigación: identity

**Dominio:** `identity` · **Estado:** protocolo específico propuesto; no ejecutado.  
**Objetivo de diseño:** L4; la madurez efectiva permanece M2 editorial hasta disponer de fuentes leídas y resultados.  
**Hipótesis central:** ¿Qué combinación de ciclo de vida, autenticación resistente a phishing, federación y autorización reduce accesos indebidos sin crear fallos inaceptables de disponibilidad o usabilidad?

## Pregunta central

¿Qué combinación de ciclo de vida, autenticación resistente a phishing, federación y autorización reduce accesos indebidos sin crear fallos inaceptables de disponibilidad o usabilidad?

## Alcance, exclusiones y ética

Los estudios se limitan a datos sintéticos, datasets con licencia y activos propios o expresamente autorizados. No se ejecutarán acciones contra terceros, no se usarán credenciales ni datos personales reales y no se desplegarán muestras/payloads operativos fuera de entornos controlados. Cada experimento debe declarar responsable, autorización, límites de recursos, regla de parada y procedimiento de rollback.

## Protocolos específicos

### R1 — IAM/IGA/PAM y lifecycle

Unidad: identidad sintética y evento joiner/mover/leaver. Variables: tipo de identidad, latencia de sincronización, dependencias SaaS y sesión activa. Baseline: baja manual documentada. Intervención: workflow automatizado idempotente. Casos: cambio de rol, baja, cuenta huérfana, grupo anidado y proveedor desconectado. Métricas: tiempo de revocación, permisos residuales, errores y trazabilidad.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R2 — MFA y recuperación

Unidad: ceremonia de autenticación y recuperación en IdP demo. Variables: origin, challenge, dispositivo, método de recuperación y expiración. Controles: passkey/WebAuthn, OTP de laboratorio y recovery débil simulado. Métricas: aceptación indebida, falsos rechazos, abandono y tiempo de revocación.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R3 — OAuth/OIDC/SAML/Kerberos

Unidad: transacción de federación. Variar issuer, audience, nonce/state, PKCE, redirect URI, firma, reloj, replay y rotación JWKS. Comparador: configuración de referencia fijada. Métricas: negativos rechazados, interoperabilidad y fallos de validación.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R4 — RBAC/ABAC/ReBAC

Unidad: decisión sujeto-acción-recurso-contexto. Dataset sintético con roles, atributos faltantes, herencia, tenant y relaciones. Comparar política esperada con decisión observada. Métricas: autorización incorrecta, explicabilidad y coste de evaluación.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R5 — Workload identity/secretos

Unidad: identidad de servicio y ciclo de credencial efímera. Variar attestation, expiración, rotación, revocación y trust bundle. Métricas: tiempo de revocación, credenciales residuales y disponibilidad tras rotación.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

### R6 — SoD/recertificación/abuso

Unidad: usuario sintético, combinación de permisos y sesión. Inyectar conflictos, privilegios sin uso, anomalías y recuperación. Medir detección, falsos positivos, cierre de excepciones y tiempo de respuesta.

**Hipótesis falsable:** la intervención definida mejora la métrica primaria respecto de la baseline sin superar el umbral de daño/coste predefinido. **H0:** no existe diferencia bajo el protocolo y la muestra definidos.  
**Análisis:** informar tamaño muestral, distribución, intervalos de confianza y casos excluidos; no generalizar fuera del corpus.

## Protocolo común de ejecución

1. Congelar pregunta, hipótesis, unidad de análisis, métrica primaria y criterio de exclusión antes de ejecutar.
2. Registrar versiones de OS, herramientas, librerías, datasets, configuración y hardware.
3. Fijar corpus y su procedencia, licencia, etiquetas, hash y particiones; evitar fuga entre train/test o entre versiones.
4. Construir baseline reproducible y controles positivos/negativos.
5. Aislar entorno, registrar reloj y verificar salvaguardas antes de introducir casos.
6. Ejecutar piloto para comprobar instrumentación; no mezclar resultados del piloto con la muestra confirmatoria sin declararlo.
7. Ejecutar repeticiones predefinidas y conservar salidas brutas, logs saneados y errores.
8. Analizar incertidumbre, sesgo de selección, variables de confusión y resultados negativos.
9. Reproducir desde entorno limpio y registrar diferencias.

## Métricas y análisis

Cada protocolo define su métrica primaria. Cuando se evalúe clasificación, reportar matriz de confusión, precision, recall, F1 cuando sea pertinente y prevalencia; no usar accuracy aislada con clases desbalanceadas. Para tiempos, informar mediana, p50/p95, tamaño muestral y condiciones. Para reproducibilidad, declarar qué constituye una repetición válida. Los resultados deben incluir falsos positivos, falsos negativos, intervalos y casos no concluyentes.

## Amenazas a la validez

- **Interna:** versiones, reloj, instrumentación, operador, orden de pruebas y variables no controladas.
- **Externa:** muestras sintéticas o un proveedor no representan todos los entornos.
- **Constructo:** cobertura, alerta o puntuación no equivalen automáticamente a seguridad.
- **Selección:** corpus sesgado, duplicados y contaminación entre particiones.
- **Reproducibilidad:** cambios de herramienta, firmware, dependencias o datos.
- **Ética/legal:** autorización, privacidad, licencias, divulgación y retención.

## Entregables

- Protocolo preregistrado y baseline.
- Dataset/corpus con procedencia, licencia, hash y ground truth.
- Scripts, configuración y versiones fijadas.
- Resultados brutos, métricas y análisis estadístico.
- Registro de falsos positivos/negativos y casos no concluyentes.
- Limitaciones, amenazas a validez y plan de reproducción.
- Revisión independiente.

## Puertas de madurez

- **M2:** contenido específico y protocolo reproducible diseñado.
- **M3:** fuentes primarias leídas con extracción de requisitos y síntesis crítica.
- **M4:** experimentos ejecutados, resultados conservados y reproducción interna.
- **M5:** revisión independiente y reproducción por un segundo operador.

**Estado actual:** agenda M2 propuesta. No se declaran experimentos ejecutados ni validación científica.
