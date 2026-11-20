# Secciones de profundización — Seguridad móvil

## Modelo de amenazas
Modelar dispositivo, boot chain, OS, sandbox, permisos, almacenamiento, biometría, aplicación, SDK, backend, MDM y tiendas. Amenazas: app reempaquetada, abuso de permisos, rooting/jailbreak, hooking, extracción de tokens, deep links inseguros, backup expuesto, TLS mal validado y SDK comprometido. Distinguir controles del dispositivo de controles de servidor.

## Detección
Correlacionar autenticación, attestation cuando exista, cambios de dispositivo, integridad de app, permisos sensibles, fallos de pinning, sesiones y API. Buscar anomalías de dispositivo, automatización, abuso de deep links, cambios de firma/versiones y patrones de exfiltración. Evitar depender exclusivamente de señales de rooting que pueden falsificarse o producir falsos positivos.

## Respuesta a incidentes
Revocar tokens y sesiones del dispositivo afectado, bloquear versiones o certificados comprometidos, preservar logs de backend y artefactos de app, evaluar exposición local y remota, rotar secretos y publicar actualización firmada. Si hay datos locales, valorar borrado remoto según política y preservar evidencia antes cuando proceda. Comprobar versiones antiguas aún activas y compatibilidad.

## Casos prácticos
En emulador y dispositivo de prueba, instalar una app firmada de laboratorio que almacena un token de test en preferencias y acepta un deep link sin validar origen. Demostrar el riesgo sin cuentas reales, corregir almacenamiento y validación, añadir tests estáticos/dinámicos y verificar revocación de sesión desde backend.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para OWASP MASVS/MSTG, Android Security, Apple Platform Security y NIST. Registrar versiones de OS, SDK, dispositivo y modelo de amenaza.
