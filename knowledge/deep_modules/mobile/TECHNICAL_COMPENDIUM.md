# Compendio técnico: Seguridad móvil

ID: `mobile` · Versión 0.1.0 · Estado: cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Seguridad móvil; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

El documento organiza el desarrollo por subtema; no afirma investigación exhaustiva ni lectura integral de referencias. Usar activos propios/autorizados, entornos aislados y datos sintéticos. Para sistemas físicos, usar simuladores o bancos controlados y priorizar seguridad funcional.

## Desarrollo técnico por subtema

### 1. Android: sandbox, permisos y Android Keystore

**Modelo de ejecución.** Cada aplicación se ejecuta bajo un UID propio en el kernel Linux. El aislamiento combina UID/GID, permisos DAC, SELinux en modo enforcing, namespaces y restricciones del framework. No describir el sandbox como una única barrera: una vulnerabilidad del kernel, un servicio privilegiado o una interfaz IPC mal protegida puede cruzar límites de aplicación. ART ejecuta bytecode DEX; JNI y bibliotecas nativas introducen memoria y superficies adicionales.

**Permisos y componentes.** Analizar el manifiesto efectivo del APK (no solo el fuente): activities, services, receivers y content providers; atributos `exported`, permisos de componente, intent filters, URI grants y permisos runtime. Desde Android 12, los componentes con intent filters deben declarar explícitamente `android:exported`. Los permisos normales, peligrosos, signature y special app access tienen semánticas distintas. Un permiso declarado no demuestra que el sistema lo conceda ni que la app lo use correctamente.

**Keystore.** Android Keystore mantiene material de clave fuera del proceso de la aplicación; cuando el dispositivo lo soporta, operaciones pueden ejecutarse en TEE o StrongBox. La clave privada puede ser no exportable, pero el proceso autorizado aún puede pedir operaciones criptográficas mientras conserva acceso. Documentar alias, propósito, modos, padding, digest, autenticación requerida, validez temporal, invalidación por cambios biométricos y comportamiento ante ausencia de hardware seguro. No asumir StrongBox/TEE por versión de Android: comprobar capacidades en runtime.

**Fallos típicos.** Secretos hardcodeados; tokens en SharedPreferences sin protección; exportación innecesaria de componentes; URI grants excesivos; validación débil de intents; WebView con JavaScript bridge expuesto; confiar en root detection como control de autorización; claves que no se rotan o que quedan inutilizables tras cambio de bloqueo/biometría.

**Verificación fría.** Construir una app de laboratorio con dos UIDs y componentes exportados/no exportados. Probar llamadas permitidas y denegadas, permisos revocados, intent explícito/implícito, URI grants y acceso a contenido. Registrar versión de OS, targetSdk, manifiesto fusionado, UID, AVC denials, resultado esperado/observado y logs saneados.

### 2. iOS: sandbox, entitlements y Keychain

**Cadena de confianza.** Separar Secure Boot, firma de código, provisioning profile, entitlements, sandbox, Data Protection y Secure Enclave. La firma verifica integridad/origen del código según la cadena de confianza; no demuestra que la lógica de negocio sea segura. Los entitlements son capacidades firmadas y autorizadas por el sistema, no simples preferencias configurables por la app.

**Sandbox y extensiones.** Mapear contenedor de app, grupos compartidos, App Groups, Keychain access groups, extensiones, URL schemes, Universal Links y servicios del sistema. Revisar qué proceso posee cada dato y qué entitlement habilita el acceso. La extensión tiene límites de ciclo de vida y recursos; no asumir que comparte todo el estado del proceso principal.

**Keychain y Data Protection.** Elegir clases de accesibilidad conforme a disponibilidad y amenaza: por ejemplo, datos disponibles solo cuando el dispositivo está desbloqueado frente a los que pueden sobrevivir a reinicios o migraciones. Evaluar sincronización iCloud, migración, backup, access group, Secure Enclave y requisitos de presencia del usuario. Separar secreto exportable de clave privada no exportable. Probar estados bloqueado/desbloqueado, reinicio, restauración y cambio de passcode.

**Riesgos.** URL schemes que aceptan callbacks no autenticados; Universal Links mal asociados; grupos Keychain demasiado amplios; datos sensibles en logs, pasteboard, snapshots de UI o archivos temporales; entitlements excesivos; confundir biometría local con autenticación del servidor.

**Verificación fría.** Inspeccionar firma, entitlements y provisioning profile de una app de laboratorio. Ejecutar pruebas con dos apps firmadas para distintos grupos, callback válido/alterado, estado bloqueado y restauración de backup. Preservar comandos, versión de Xcode/iOS, hashes y salida.

### 3. Almacenamiento local, backups y ciclo de vida de datos

Crear un inventario por tipo de dato: credenciales, tokens, PII, datos de negocio, cachés, claves, telemetría y contenido descargado. Para cada elemento registrar clasificación, ubicación, cifrado, propietario, retención, exportabilidad, backup, sincronización y borrado esperado.

**Android.** Revisar almacenamiento interno/externo, scoped storage, SQLite/Room, archivos temporales, logs, preferencias, Auto Backup y reglas de extracción. Cifrar con claves gestionadas por Keystore y usar bibliotecas mantenidas; el cifrado de archivo no protege si la clave se almacena junto al ciphertext. Excluir secretos del backup cuando la política lo requiera y verificar el comportamiento real del target OS.

**iOS.** Revisar Data Protection por archivo, protección de bases de datos, Keychain, caches, backups y sincronización. Asegurar que la clase de protección corresponde al estado de uso; evitar almacenar secretos en Documents si no deben sincronizarse. El borrado lógico de una fila no equivale necesariamente a borrado físico inmediato en flash, WAL o snapshots.

**Amenazas y pruebas.** Extracción de backup, dispositivo desbloqueado, logs/crash reports, screenshots, clipboard, teclado de terceros, filesystem residual, sincronización accidental y restauración a otro dispositivo. Usar datos sintéticos marcados y buscar cada canario en ubicaciones previstas y no previstas. Medir exposición por superficie, persistencia tras logout/revocación y falsos positivos del escáner.

### 4. TLS, confianza del dispositivo y autenticación

**TLS.** Validar cadena, hostname, expiración, usos de certificado, protocolos y suites admitidos por la plataforma. Nunca aceptar todos los certificados ni sustituir hostname verification por pinning. Certificate pinning es una defensa adicional contra ciertos escenarios de CA comprometida; introduce riesgo de indisponibilidad y requiere estrategia de rotación, pins de respaldo y proceso de emergencia.

**OAuth 2.0/OIDC.** Para clientes móviles públicos usar Authorization Code con PKCE; no incrustar un client secret como si fuera confidencial. Validar state, nonce cuando aplique, issuer, audience, expiración, redirect URI exacta y firma de tokens según especificación. Preferir navegador del sistema para SSO y evitar WebView embebida como agente de autenticación. Los access tokens deben tener alcance y duración mínimos; refresh tokens requieren rotación/revocación y detección de reutilización según el proveedor.

**Confianza del dispositivo.** Attestation e indicadores de integridad aportan señales de riesgo, no prueba absoluta de que el dispositivo esté limpio. Definir política de degradación: step-up, limitar operaciones sensibles o pedir reautenticación; no bloquear automáticamente a todos los dispositivos modificados sin analizar falsos positivos y accesibilidad.

**Pruebas.** Certificado caducado, hostname incorrecto, CA no confiable, proxy de laboratorio, redirect URI manipulada, state ausente/reutilizado, token de audiencia incorrecta, refresh revocado y reloj desfasado. La app debe fallar de forma segura sin filtrar tokens en logs.

### 5. Deep links, IPC, intents y WebView

Tratar cada frontera de IPC como entrada no confiable, incluso si la llamada procede de otra app instalada. Definir esquema, tipos, tamaño, autenticidad, autorización y validación de cada parámetro.

**Android.** Revisar intents explícitos e implícitos, exported components, PendingIntent mutability, broadcast receivers, Binder, content providers, path permissions y URI permission flags. Preferir intents explícitos para flujos internos; validar caller/permiso donde sea posible. Un intent filter no es mecanismo de autenticación. En PendingIntent, usar inmutabilidad por defecto cuando el caso lo permita y comprobar identidad/alcance del token.

**iOS.** Comparar URL schemes personalizados con Universal Links asociados a dominio y archivo de asociación. Validar parámetros, estado de sesión y autorización en backend; un deep link no debe ser una capacidad bearer sin caducidad. Revisar callbacks OAuth, universal link fallback y colisiones de esquemas.

**WebView.** Desactivar JavaScript si no es necesario; restringir navegación, orígenes y carga de contenido mixto; no exponer bridges a contenido remoto no confiable; validar esquemas y descargas; evitar interfaces nativas invocables desde cualquier frame. No confiar en una allowlist superficial si redirecciones y subrecursos quedan fuera.

**Casos de prueba.** Parámetros duplicados, Unicode/normalización, URL encodificada doble, esquema desconocido, host parecido, redirect externo, replay, payload sobredimensionado, componente exportado y contenido remoto que intenta invocar bridge. Registrar decisión de autorización y origen real.

### 6. MASVS/MSTG, análisis estático/dinámico y evaluación

Usar OWASP MASVS como estándar de requisitos y MASTG como guía de pruebas; fijar versión/commit de ambos y mapear cada caso a un identificador concreto. No declarar conformidad por ejecutar un escáner ni usar una checklist sin evidencia.

**Análisis estático.** Inspeccionar manifiestos/entitlements, permisos, configuración de red, dependencias, SDKs, strings, endpoints, criptografía, logs y almacenamiento. Los hallazgos deben confirmarse con contexto y versión; los secretos de prueba no deben confundirse con credenciales activas.

**Análisis dinámico.** Instrumentar solo apps propias/autorizadas en emulador o dispositivo de laboratorio. Observar filesystem, IPC, tráfico, logs, memoria accesible y comportamiento ante cambios de estado. Distinguir comportamiento del emulador del hardware real, especialmente Keystore/TEE, Secure Enclave, biometría y attestation.

**Rúbrica.** Cada hallazgo incluye requisito MASVS/MASTG, activo, precondición, impacto, evidencia reproducible, severidad contextual, falso positivo posible, mitigación, retest y riesgo residual. Medir precision/recall sobre un corpus etiquetado; publicar denominadores y criterios de confirmación. No inferir cobertura total a partir de la cantidad de pruebas automatizadas.

### 7. MDM/MAM, respuesta y ciclo de vida empresarial

Separar gestión del dispositivo (MDM), gestión de aplicaciones (MAM), gestión de identidades, protección de datos y telemetría. Modelar BYOD, COPE y dispositivos corporativos como perfiles de privacidad y control distintos. Registrar qué datos puede ver el administrador y qué acciones son posibles: borrar perfil laboral, retirar app, revocar certificados, bloquear sesión o wipe total.

**Controles.** Enrollment autenticado; compliance posture con versión/patch; configuración gestionada; distribución y actualización firmada; certificados por dispositivo; VPN/per-app networking cuando aplique; separación de datos laborales; remote lock/wipe; inventario y revocación al offboarding. No asumir que MDM impide extracción por cámara, capturas externas o dispositivos comprometidos.

**Respuesta.** Ante pérdida/robo: revocar sesiones y certificados, bloquear acceso backend, evaluar sensibilidad de datos locales, aplicar wipe proporcional, preservar logs disponibles y notificar según política. Ante app comprometida: detener distribución, revocar credenciales/firmas si corresponde, publicar versión corregida, forzar reautenticación y medir dispositivos aún vulnerables.

**Métricas.** Tiempo hasta revocación, cobertura de dispositivos administrados, cumplimiento de versión, porcentaje de apps con configuración gestionada, éxito de wipe, falsos bloqueos y tiempo de recuperación. Definir denominadores y separar BYOD de flota corporativa.

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
| mobile-LAB-01 | Baseline seguro | Versiones, configuración, hashes, salida |
| mobile-LAB-02 | Fallo/abuso sintético | Precondiciones, entrada, logs, resultado |
| mobile-LAB-03 | Detección y diagnóstico | Señal, regla, precisión, límites |
| mobile-LAB-04 | Mitigación y regresión | Diff, antes/después, rollback |

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


## Profundización técnica específica: Seguridad móvil

### Arquitectura y superficies
Distinguir Android (Linux kernel, HAL, Binder, ART, framework, APK/AAB) e iOS (Secure Enclave, Keychain, code signing, sandbox, entitlements, app extensions). Modelar app, OS, baseband, boot chain, hardware trust, MDM, store, backend, SDK y canales de actualización. La seguridad de la app depende también de configuración del dispositivo y del backend.

### Almacenamiento y secretos
Revisar Keychain/Keystore, hardware-backed keys, StrongBox/Secure Enclave cuando disponible, backups, shared preferences, SQLite, archivos temporales, logs, clipboard, screenshots y caches. Definir clasificación de datos, cifrado, protección por estado del dispositivo, retención y borrado. No guardar tokens o claves en preferencias planas ni confiar solo en ofuscación.

### Comunicación y autenticación
Validar TLS, hostname, trust store, certificate pinning con estrategia de rotación, OAuth/OIDC, PKCE, deep links, universal links y redirect handling. Revisar exportación de componentes Android, intents, content providers, URL schemes, app links, WebViews, universal links y IPC. Pinning puede causar indisponibilidad si no se diseña renovación; no reemplaza validación TLS.

### Plataforma, permisos y supply chain
Evaluar permisos mínimos, runtime permissions, background execution, accessibility services, notification content, biometrics, device integrity y jailbreak/root signals. Revisar manifest, entitlements, signing identities, provisioning profiles, dependency SDKs, build reproducible y distribución. SBOM debe incluir SDKs y bibliotecas nativas. Proteger pipeline de firma y claves de publicación.

### Reverse engineering y privacidad
El análisis estático/dinámico debe usar aplicaciones propias o muestras autorizadas, emuladores y dispositivos de laboratorio. Revisar strings, endpoints, certificados, logs, filesystem, IPC, memoria y tráfico. Anti-tampering y obfuscation elevan coste, no sustituyen controles backend. Minimizar telemetría, consentimiento, identificadores persistentes y datos sensibles conforme a jurisdicción.

### Laboratorios y métricas
- App de prueba con almacenamiento seguro/inseguro y verificación de artefactos.
- Deep link e intent routing con casos válidos, inválidos y maliciosos sintéticos.
- Revisión de permisos, componentes exportados y configuración de red.
- Evaluación de SDK/SBOM y firma de artefactos.
Medir hallazgos confirmados, falsos positivos, cobertura de API/flows, exposición de datos y compatibilidad por versión/OS.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.