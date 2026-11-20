# Investigación técnica: Seguridad móvil Android e iOS

**ID:** mobile · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas en dispositivos físicos pendientes.

## Modelo
Una app móvil combina código cliente, sistema operativo, sandbox, permisos, almacenamiento, keystore/keychain, IPC, deep links, WebViews, push, biometría, backend/API, SDKs, analytics y distribución. La app cliente no es un entorno confiable para guardar secretos permanentes ni imponer autorización de negocio.

## Android
Revisar manifest, exported components, intents/deep links, permissions, Binder/IPC, ContentProviders, WebView, network security config, Keystore, backup, signing, Play Integrity y actualización. Validar storage privado, scoped storage, TLS, pinning con estrategia de rotación, permisos runtime y protección de datos en logs/screenshots. Analizar APK/AAB, DEX, native libs, resources y configuración de build.

## iOS
Revisar entitlements, sandbox, Keychain, Data Protection classes, App Transport Security, URL schemes/universal links, extensions, pasteboard, background tasks, signing/provisioning, jailbreak/root detection y privacy manifests. Evitar confiar exclusivamente en jailbreak detection como control de autorización.

## Backend y runtime
La autorización debe ejecutarse en servidor. Probar tokens, session binding, device changes, refresh, replay, rate limits y tenant isolation. Revisar SDKs de terceros, telemetría, consentimiento, tracking, crash reports y exposición de datos sensibles.

## Amenazas y pruebas
Reverse engineering, tampering, repackaging, insecure storage, weak crypto, exported components, deep link hijack, WebView injection, certificate validation flaws, API BOLA, root/jailbreak, hooking, runtime instrumentation y supply chain de SDK. Usar dispositivos/emuladores propios y cuentas sintéticas; no recolectar datos de usuarios reales.

## Laboratorios
App vulnerable deliberada en Android emulator/iOS simulator; test MASVS por storage, crypto, auth, network, platform, code, resilience y privacy. Instrumentar tráfico a backend mock, inspeccionar manifests/entitlements y comprobar que secretos canario no quedan en logs, backups o caches.

## Fuentes
- OWASP Mobile Application Security: https://owasp.org/projects/mobile-application-security/
- OWASP MASVS: https://mas.owasp.org/MASVS/
- OWASP MASTG: https://mas.owasp.org/MASTG/
- Android Security: https://source.android.com/docs/security
- Apple Platform Security: https://support.apple.com/guide/security/welcome/web

**Límite:** controles cambian entre versiones de Android/iOS y modelos de distribución; validar en dispositivos y releases objetivo.
