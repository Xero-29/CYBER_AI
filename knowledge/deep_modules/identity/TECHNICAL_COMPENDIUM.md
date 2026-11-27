# Compendio técnico: Identidad y acceso

ID: `identity` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Identidad y acceso; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. IAM, IGA, PAM y ciclo de vida

IAM administra identidades, autenticación y autorización; IGA gobierna solicitudes, aprobaciones, recertificación, segregación de funciones y evidencia; PAM controla cuentas y sesiones privilegiadas. No son sinónimos ni una sola plataforma garantiza los tres dominios. Separar plano de identidad, plano de políticas, plano de credenciales y plano de auditoría.

Modelar cada identidad con identificador inmutable, tipo (humana, workload, dispositivo, servicio, externa), propietario, fuente autoritativa, estado, atributos, credenciales vinculadas y fechas de alta/cambio/baja. El proceso joiner-mover-leaver debe ser idempotente, auditable y reconciliable. La baja debe revocar sesiones, tokens, claves, certificados, grupos y delegaciones; deshabilitar solo la cuenta primaria deja credenciales residuales.

IGA debe comparar permisos asignados con permisos efectivos, detectar cuentas huérfanas, identidades duplicadas, derechos incompatibles y excepciones sin vencimiento. PAM debe preferir elevación temporal, aprobación contextual, grabación proporcional y credenciales efímeras. Break-glass necesita custodia separada, alertas inmediatas, uso justificado y rotación posterior.

**Caso verificable:** una persona cambia de finanzas a desarrollo. La prueba no termina cuando cambia su grupo: debe demostrar revocación de permisos financieros, concesión mínima de los nuevos, expiración de sesiones anteriores, propagación a SaaS y ausencia de privilegios transitivos.

### 2. MFA resistente a phishing y autenticadores

Distinguir factor de conocimiento, posesión e inherencia de la resistencia real al phishing. OTP y push pueden ser capturados o inducidos mediante proxy adversario; la aprobación push sin vinculación de origen es vulnerable a fatiga y aprobación equivocada. WebAuthn/FIDO2 usa desafío firmado y vinculación al relying party; passkeys pueden sincronizarse o ser ligadas a dispositivo según el modelo del proveedor.

En WebAuthn validar challenge único, origin exacto, RP ID, tipo de ceremonia, flags UP/UV, firma, contador cuando aplique y asociación de la clave pública al usuario. No aceptar un resultado exitoso si el desafío no pertenece a la sesión actual. La recuperación de cuenta es parte del sistema MFA: un flujo débil puede anular el autenticador fuerte.

**Pruebas negativas:** origin de otro dominio, challenge repetido, challenge expirado, respuesta para otro usuario, downgrade a OTP, pérdida de dispositivo, recuperación con datos insuficientes y sesión iniciada desde un proxy no confiable. Registrar por separado tasa de éxito legítimo, rechazo correcto y falsos rechazos.

### 3. OAuth 2.0, OpenID Connect, SAML y Kerberos

OAuth 2.0 delega autorización; OpenID Connect añade una capa de identidad sobre OAuth. Un access token autoriza a un recurso; un ID token comunica autenticación al cliente. No intercambiar sus audiencias ni validar un JWT solo por decodificarlo. Validar firma con algoritmo permitido, issuer, audience, expiración, not-before, nonce cuando corresponda, tipo de token y contexto de flujo.

Authorization Code con PKCE reduce la interceptación del código; state vincula respuesta y solicitud; redirect URI debe compararse exactamente contra registros autorizados. Evitar implicit grant y flujos heredados salvo necesidad justificada. Para refresh tokens aplicar rotación, detección de reutilización, revocación y almacenamiento seguro. En OIDC revisar discovery y JWKS, rotación de claves y comportamiento ante claves desconocidas.

SAML usa assertions firmadas y XML; revisar issuer, recipient, destination, audience, condiciones temporales, InResponseTo, ID único, firma sobre el nodo correcto y prevención de XML signature wrapping. Kerberos usa tickets y claves de sesión; entender AS-REQ/AS-REP, TGS-REQ/TGS-REP, service tickets, SPN, reloj, KDC y delegación. Los tickets y hashes no deben exponerse en ejercicios reales.

**Matriz de pruebas:** firma válida/inválida, issuer incorrecto, audience adicional no autorizada, token expirado, replay, redirect URI similar pero distinta, assertion duplicada, skew temporal y revocación durante sesión.

### 4. RBAC, ABAC, ReBAC y autorización efectiva

RBAC asigna permisos a roles; ABAC evalúa atributos de sujeto, recurso, acción y entorno; ReBAC evalúa relaciones. RBAC facilita administración pero puede producir explosión de roles; ABAC expresa contexto pero exige atributos confiables y políticas comprensibles; ReBAC es útil en colaboración y jerarquías, pero puede crear rutas de acceso transitivas difíciles de auditar.

Formalizar una decisión como P(subject, action, resource, context) → permit/deny. Aplicar deny-by-default, precedencia explícita de denegación, validación de atributos, separación entre policy decision point y enforcement point, y registro de razón de decisión. Evaluar permisos efectivos incluyendo grupos anidados, herencia, delegaciones, tokens, permisos de plataforma y relaciones indirectas.

**Prueba de autorización:** construir tabla de sujetos, acciones, recursos y contexto con resultados esperados; incluir usuario anónimo, usuario deshabilitado, rol heredado, atributo ausente, recurso de otro tenant y cambio de propiedad durante una sesión. Probar BOLA/IDOR en aplicaciones propias con identificadores sintéticos.

### 5. Workload identity, secretos y confianza entre servicios

Una workload no debe heredar automáticamente la identidad de la persona que la despliega. Preferir identidades federadas de corta duración, certificados de servicio o tokens emitidos bajo condiciones verificables frente a claves estáticas persistentes. SPIFFE/SPIRE ofrece un modelo de identidad de workload basado en identificadores SPIFFE y SVID; su uso requiere proteger el proceso de attestation y el trust domain.

Separar emisión, distribución, uso, rotación y revocación de secretos. Evitar secretos en repositorios, imágenes, logs, trazas, tickets, variables de entorno persistentes y artefactos de CI. La detección de secretos debe cubrir historial Git y artefactos, pero el hallazgo requiere revocar y rotar: borrar el texto del último commit no invalida una credencial filtrada.

Para mTLS validar cadena, SAN esperado, EKU, vigencia, trust bundle, revocación disponible y correspondencia entre identidad autenticada y política de autorización. Rotar certificados sin interrumpir servicios requiere solapamiento controlado, observabilidad y prueba de rollback.

### 6. Recertificación, SoD y gobierno de acceso

La recertificación debe mostrar al revisor el permiso efectivo, su uso, criticidad, propietario del recurso, justificación y conflicto potencial; una lista plana de grupos fomenta aprobaciones automáticas. SoD identifica combinaciones incompatibles, como crear proveedor y aprobar pagos. Modelar conflicto preventivo y detective, excepciones temporales, compensaciones y dueño de aceptación de riesgo.

Medir porcentaje de identidades con propietario, tiempo de baja, cuentas huérfanas, privilegios permanentes, accesos sin uso, excepciones vencidas, cobertura de MFA resistente a phishing, reutilización de secretos y tiempo de revocación. Las métricas deben declarar denominador, ventana temporal y exclusiones.

### 7. Abuso y recuperación de cuentas

Modelar credential stuffing, password spraying, SIM swap, MFA fatigue, session theft, help-desk social engineering, abuso de OAuth consent y secuestro de recuperación. No inferir compromiso por una sola señal: correlacionar dispositivo, IP/ASN, geografía imposible con cautela, reputación, velocidad, patrón de autenticación y cambios de factores.

La recuperación debe verificar identidad con factores independientes, invalidar sesiones y refresh tokens, revisar métodos de recuperación, alertar por canal previamente registrado y ofrecer demora/retención para cambios de alto riesgo. No enviar secretos por correo ni permitir que soporte omita controles sin registro.

## Laboratorio reproducible

Entorno: IdP local o tenant de pruebas, aplicaciones de demostración, directorio sintético y reloj controlado. No conectar cuentas de producción ni importar credenciales reales.

| ID | Experimento frío | Diseño y criterio de aceptación |
|---|---|---|
| identity-LAB-01 | Ciclo joiner-mover-leaver | Crear 3 identidades sintéticas; cambiar rol y dar de baja; verificar propagación, sesiones, tokens y permisos residuales |
| identity-LAB-02 | Validación OIDC/OAuth | Emitir tokens de prueba; probar issuer, audience, nonce, PKCE, expiración y replay; todos los negativos deben rechazarse |
| identity-LAB-03 | Matriz de autorización | Ejecutar matriz RBAC/ABAC con atributos faltantes, herencia y cross-tenant; comparar decisión real con ground truth |
| identity-LAB-04 | MFA y recuperación | Simular WebAuthn con relying party de laboratorio y recuperación; demostrar rechazo de challenge/origin incorrectos |
| identity-LAB-05 | Workload identity | Emitir SVID/certificado efímero; rotar y revocar; comprobar que identidad anterior deja de autorizar |
| identity-LAB-06 | SoD y recertificación | Inyectar conflictos sintéticos y permisos sin uso; medir detección, explicación y cierre de excepciones |

Para cada ejecución conservar configuración, versiones, dataset sintético, hash, reloj, logs, resultado esperado/observado, desviaciones y rollback. Diseño definido; no declarar ejecución hasta conservar evidencia.

## Métricas, límites y criterios

Métricas mínimas: cobertura de MFA resistente a phishing; tasa de revocación dentro del SLA; cuentas huérfanas por 1.000 identidades; privilegios permanentes; precisión/recall de detección; falsos rechazos de autenticación; tiempo de propagación; y porcentaje de decisiones de autorización con explicación. Reportar intervalos y segmentar por tipo de identidad.

Riesgos de validez: IdP simulado no reproduce latencia ni integraciones SaaS; datasets sintéticos no modelan conducta humana; los logs pueden omitir decisiones en sistemas federados. No extrapolar un resultado local a toda una organización.

## Artefactos de aceptación por tema

- Diagrama de componentes, flujos y límites de confianza.
- Modelo de identidad, amenazas y política de autorización.
- Casos positivos, negativos, límites y regresión con ground truth.
- Matriz amenaza → control → prueba → evidencia → riesgo residual.
- Configuración y scripts reproducibles sin secretos reales.
- Fuentes versionadas, páginas revisadas y afirmaciones trazables.
- Informe de incertidumbre, limitaciones y revisión independiente.

## Madurez

Remediación editorial específica propuesta. No equivale a lectura integral de normas, laboratorio ejecutado, revisión externa ni validación científica. Mantener M2 como máximo hasta que cada puerta de evidencia esté satisfecha.

## Laboratorio reproducible
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Caso | Evidencia exigida |
|---|---|---|
| identity-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| identity-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| identity-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| identity-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

Diseño definido; ejecución pendiente.

## Métricas
Elegir métricas específicas: cobertura, tasa de detección, falsos positivos/negativos, latencia, disponibilidad, impacto colateral, tiempo de remediación y repetibilidad. Toda cifra exige unidad de análisis, muestra, baseline, versiones, repeticiones y método de análisis.

## Investigación bibliográfica
- Registrar bases, cadenas de búsqueda, fecha, idiomas y criterios de inclusión/exclusión.
- Priorizar normas, especificaciones, documentación primaria y literatura revisada por pares.
- Leer texto completo antes de usar `full_text_reviewed`.
- Extraer método, población, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y enfoques; separar evidencia, inferencia e hipótesis.
- Registrar edición, URL canónica, licencia, fecha y hash cuando el archivo pueda archivarse legalmente.

## Preguntas de investigación candidatas
1. ¿Qué controles reducen el riesgo de los escenarios priorizados frente a un baseline?
2. ¿Qué condiciones de versión/entorno explican diferencias entre resultados publicados y reproducidos?
3. ¿Qué combinación de señales y criterios mejora la detección sin impacto operacional inaceptable?

Cada estudio debe definir H0/H1, variables, muestra, comparadores, refutación, análisis, ética, seguridad y límites.

## Artefactos de aceptación
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos/datos/identidades/versiones.
- [ ] Modelo de amenazas y escenarios.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimientos con precondiciones, rollback y parada.
- [ ] Laboratorio y casos medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencias, edición, fecha y hashes.
- [ ] Incertidumbre, falsos positivos/negativos y validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No demuestra cobertura profunda ni M3/M4/M5. Próxima puerta: revisar fuentes completas, producir artefactos específicos, ejecutar pruebas y registrar evidencia.


## Profundización técnica específica: Gestión de identidad y acceso

### Modelo de identidad y ciclo de vida
Modelar identidades humanas, workload, servicio, dispositivo, máquina, federadas y externas. El ciclo joiner-mover-leaver debe automatizar alta, cambio, suspensión y baja con propietario, fuente autoritativa, sincronización, expiración y reconciliación. Identidades huérfanas, duplicadas y compartidas degradan trazabilidad. Distinguir sujeto, principal, credencial, autenticador, sesión y autorización.

### Autenticación y federación
Evaluar MFA resistente a phishing, passkeys/WebAuthn, FIDO2, certificados, OTP y recuperación de cuenta. OAuth 2.0 es framework de autorización; OIDC agrega identidad; SAML se usa en federación empresarial. Revisar issuer, audience, redirect URI, nonce, state, PKCE, token lifetime, refresh rotation, revocation y validación de firma/algoritmo. No aceptar tokens por decodificación sin validar firma, issuer, audience, expiración y contexto.

### Autorización y privilegios
RBAC simplifica roles; ABAC usa atributos; ReBAC modela relaciones. Aplicar deny-by-default, separación de funciones, mínimo privilegio, scopes y políticas centralizadas con decisión auditable. Revisar herencia, roles anidados, permisos efectivos, service accounts, delegación y privilegios transitivos. PAM/JIT/JEA reduce permanencia de privilegios; break-glass requiere control, alertas, caducidad y revisión.

### Sesiones, credenciales y secretos
Proteger cookies, session binding, expiración, rotación, revocación, logout y dispositivos confiables. Almacenar contraseñas con KDF adecuados y parámetros actualizados; evitar secretos en código, logs, variables expuestas y tickets. Gestión de claves/certificados requiere emisión, rotación, inventario y revocación. Detectar credential stuffing y abuso con límites adaptativos sin bloquear injustamente usuarios.

### Directorios y gobierno
AD, LDAP, Entra/IdP y directorios cloud deben mapear trusts, sincronización, fuentes autoritativas, grupos privilegiados, políticas de acceso condicional y cuentas de emergencia. Revisar SCIM provisioning, atributos, grupos dinámicos, claims y riesgo de sobreasignación. La identidad de workload requiere federación y rotación, no secretos estáticos incrustados.

### Métricas y laboratorios
Medir cobertura MFA, phishing-resistant MFA, cuentas huérfanas, privilegios permanentes, tiempo de baja, tokens de larga vida, autenticaciones anómalas y falsos positivos. Laboratorios: ciclo de vida sintético, autorización con matriz de sujetos/recursos/acciones, validación de OIDC/OAuth con tokens de prueba y recuperación segura de cuenta. No probar credenciales reales ni capturar secretos.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.