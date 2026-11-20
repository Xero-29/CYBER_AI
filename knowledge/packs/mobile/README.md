# Seguridad móvil Android e iOS — Guía de dominio

**ID:** `mobile` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Evalúa aplicaciones Android/iOS, SDKs, almacenamiento local, autenticación, comunicaciones, permisos, integridad y distribución. El dispositivo móvil mezcla datos personales, sensores, identidad y acceso corporativo; privacidad y seguridad funcional importan tanto como la resistencia a ataques. Las pruebas deben usar dispositivos/emuladores propios y cuentas sintéticas.

## Superficie y amenazas
Revisar APK/AAB/IPA, manifiestos, entitlements, deep links, WebViews, IPC, intents, URL schemes, keychain/keystore, SQLite, backups, logs, certificados, pinning, SDKs, push, biometría y APIs. Riesgos: secretos embebidos, almacenamiento sin cifrar, exportación de componentes, intent hijacking, deep-link takeover, WebView insegura, TLS débil, jailbreak/root detection mal diseñada, backup de datos y SDKs con exceso de permisos.

## Competencias específicas
- Revisar permisos Android y entitlements iOS con principio de mínimo privilegio.
- Proteger tokens y claves en Android Keystore/iOS Keychain.
- Evaluar autenticación, biometría, sesiones y revocación.
- Validar TLS, trust store, pinning y manejo de certificados.
- Analizar IPC, intents, deep links, WebViews y universal links.
- Revisar almacenamiento, logs, backups y datos temporales.
- Evaluar SDKs, dependencias, privacidad y cadena de distribución.
- Diseñar controles de integridad y protección anti-tampering proporcionales.

## Controles prioritarios
- No guardar secretos estáticos ni claves privadas dentro del paquete.
- Cifrar datos sensibles y limitar backups/exportación.
- Deshabilitar debugging y componentes exportados innecesarios en releases.
- Validar parámetros y permisos en cada deep link/intent.
- Configurar ATS/Network Security Config y TLS moderno.
- Evitar WebView con JavaScript/bridge salvo necesidad y validación estricta.
- Rotar tokens, revocar sesiones y proteger refresh tokens.
- Minimizar permisos, telemetría y datos personales.
- Firmar artefactos y proteger cuentas de publicación.

## Metodología
1. Definir plataforma, versión, dispositivos, cuentas y datos de prueba.
2. Obtener artefacto firmado y SBOM de SDKs/dependencias.
3. Revisar manifest/entitlements, permisos y componentes exportados.
4. Analizar almacenamiento, logs, backups y secretos.
5. Inspeccionar tráfico en proxy de laboratorio y validar TLS.
6. Probar deep links, IPC y autenticación con usuarios sintéticos.
7. Verificar privacidad, consentimiento y retención.
8. Registrar hallazgos con evidencia mínima y mitigación.
9. Repetir en dispositivo limpio y build release.

## Laboratorio seguro
Emulador Android y simulador iOS, backend local y usuarios ficticios. Probar almacenamiento de tokens, deep links, WebView, certificados y revocación. No acceder a dispositivos de terceros ni recolectar datos personales reales.

## Evaluación
Permisos justificados, secretos ausentes, almacenamiento protegido, transporte seguro, componentes no exportados sin necesidad, SDKs inventariados y pruebas de regresión por hallazgo.

## Referencias y herramientas
OWASP MASVS, OWASP MASTG, Apple Platform Security, Android Security Best Practices, MobSF, JADX y Frida solo en dispositivos de laboratorio autorizados.

## Instrucciones para agentes IA
No solicites credenciales reales ni datos personales. No sugieras bypass de controles en apps ajenas. Prioriza revisión estática y pruebas locales con build de laboratorio.

---

## Marco obligatorio de desarrollo experto e investigación

Este paquete se desarrolla conforme al [Estándar experto e investigación](../../EXPERT_RESEARCH_STANDARD.md). El estándar aplica a esta especialidad, no solo al currículo global.

**Estado del perfil:** estructura y mapa de evidencias definidos; el contenido técnico ampliado, la revisión integral de fuentes, los laboratorios ejecutados y la validación independiente se registran por separado. No se declara K4/K5 por la existencia de este marco.

Cada tema de esta especialidad debe desarrollarse como unidad independiente y cubrir: teoría, formalización pertinente, arquitectura, estándares versionados, implementación, análisis avanzado, seguridad adaptada al dominio, investigación, laboratorio/dataset, evaluación, Skills verificadas y trazabilidad. La matriz detallada de capas, evidencias, enfoque matemático y restricciones de laboratorio está en `knowledge/curricula/domain_curriculum.json`, dentro del perfil `mobile`.

**Madurez:** K1–K5 se asigna por tema y evidencia. Las ocho puertas G1–G8 deben mostrar estado explícito; lo no ejecutado o no revisado permanece pendiente. Las referencias descubiertas no cuentan como lectura completa y los laboratorios diseñados no cuentan como ejecutados.
