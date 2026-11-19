# Investigación técnica: Identidad, autenticación y control de acceso

**ID:** identity · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación IdP/tenant pendiente.

## Modelo
Modelar ciclo de vida de identidades humanas, workload, dispositivo, servicio, máquina y tercero. Separar identity proofing, enrollment, autenticación, federation, autorización, sesión, provisioning, recertificación y deprovisioning. Una identidad autenticada no implica autorización a cada recurso.

## Estándares y niveles
NIST SP 800-63-4 (final, julio 2025) sustituye Rev. 3 y cubre identity proofing, autenticadores, gestión y federación; incluye SP 800-63A-4, 63B-4 y 63C-4. Seleccionar IAL/AAL/FAL según riesgo, población y contexto, sin trasladar automáticamente requisitos federales a cualquier entorno. MFA resistente al phishing y autenticadores vinculados al dominio reducen ataques de proxy/credential replay, pero no eliminan compromiso de endpoint o recuperación débil.

## Protocolos y arquitectura
Dominar OIDC, OAuth 2.0, SAML 2.0, WebAuthn/FIDO2, Kerberos, LDAP, SCIM, RADIUS y certificados X.509. Revisar issuer, audience, nonce/state, redirect URI exacta, PKCE, scopes, claims, signature algorithms, key rotation, token lifetime, refresh token rotation, revocation, session binding y clock skew. OAuth es framework de autorización; OIDC añade autenticación. No tratar access token como prueba universal de identidad ni aceptar JWT sin validar algoritmo, issuer, audience y claves.

## Autorización
RBAC asigna permisos por rol; ABAC evalúa atributos/contexto; ReBAC modela relaciones. Definir subject-action-resource-context, deny precedence, separación de funciones, SoD, JIT/JEA, delegation y break-glass. En multi-tenant validar ACL en cada API, query, cache, export, async job y backup.

## Ciclo de vida
Joiner/mover/leaver, acceso temporal, revisión periódica, cuentas huérfanas, service accounts, workload identity, secretos, recuperación, deshabilitación, revocación y auditoría. Medir tiempo de baja, privilegios excesivos, MFA coverage, phishing-resistant coverage, stale accounts, access review completion y token revocation propagation.

## Laboratorios
IdP de prueba con OIDC/SAML, app client, API resource server y dos tenants sintéticos. Probar redirect URI abierta, audience incorrecta, token expirado, key rotation, refresh replay, scopes excesivos, account recovery y revocación. No usar usuarios ni tokens reales.

## Fuentes
- NIST SP 800-63-4: https://doi.org/10.6028/NIST.SP.800-63-4
- NIST SP 800-63B-4: https://doi.org/10.6028/NIST.SP.800-63b-4
- NIST Implementation Hub: https://pages.nist.gov/800-63-4-Implementation-Resources/
- NIST SP 800-207: https://doi.org/10.6028/NIST.SP.800-207

**Límite:** guía documental; revisar perfiles de industria, legislación y configuración concreta del IdP.
