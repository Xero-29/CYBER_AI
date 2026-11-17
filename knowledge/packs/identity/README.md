# Gestión de identidad y acceso — Guía de dominio

**ID:** `identity` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Protege identidades humanas, de servicio, workloads, dispositivos y terceros a lo largo de su ciclo de vida. IAM es plano de control: errores en autenticación, autorización, federación, aprovisionamiento o recuperación pueden comprometer todo el entorno.

## Modelo y amenazas
Inventariar IdP, directorios, MFA, SSO, OAuth/OIDC, SAML, SCIM, PAM, cuentas de servicio, secretos, roles, grupos, dispositivos y accesos de terceros. Amenazas: robo de sesión, phishing, MFA fatigue, token replay, consent phishing, privilegios persistentes, cuentas huérfanas, secretos estáticos, abuso de federación y recuperación de cuenta débil.

## Competencias específicas
- Diseñar autenticación adaptativa y MFA resistente a phishing.
- Diferenciar autenticación, autorización, federación y aprovisionamiento.
- Configurar OAuth/OIDC con PKCE, redirect URI estricta y scopes mínimos.
- Aplicar RBAC/ABAC y revisión periódica de privilegios.
- Gestionar ciclo Joiner-Mover-Leaver y acceso temporal.
- Proteger identidades de servicio y workload con credenciales efímeras.
- Diseñar PAM, break-glass y doble control.
- Monitorizar eventos de login, cambios de rol, tokens y sesiones.

## Controles prioritarios
- Preferir passkeys/FIDO2 y MFA resistente a phishing para cuentas privilegiadas.
- Deshabilitar autenticación heredada y revisar excepciones.
- Aplicar acceso condicional por riesgo, dispositivo y contexto.
- Exigir consentimiento mínimo y revisar aplicaciones OAuth.
- Usar tokens de corta duración, rotación y revocación.
- Eliminar cuentas huérfanas y cuentas compartidas.
- Separar cuentas de administración y uso diario.
- Gestionar secretos de servicio en vault y rotar automáticamente.
- Revisar permisos y membresías con recertificación periódica.
- Mantener cuentas break-glass controladas, alertadas y probadas.

## Metodología
1. Inventariar identidades, roles, grupos, aplicaciones y proveedores.
2. Mapear flujos de autenticación, autorización y aprovisionamiento.
3. Revisar MFA, políticas de sesión, recuperación y federación.
4. Detectar privilegios excesivos y cuentas sin propietario.
5. Revisar OAuth apps, secretos, certificados y tokens.
6. Validar Joiner-Mover-Leaver y revocación de acceso.
7. Simular escenarios de compromiso con identidades ficticias.
8. Medir cobertura MFA, cuentas privilegiadas y tiempo de revocación.
9. Documentar excepciones con vencimiento y dueño.

## Laboratorio seguro
IdP de prueba con dos aplicaciones, roles de lector/admin, cuenta de servicio y usuarios sintéticos. Probar PKCE, redirect URI incorrecta, expiración de sesión, revocación, MFA y baja de usuario. No usar cuentas corporativas reales.

## Evaluación
100% de identidades críticas con propietario; privilegios revisados; MFA adecuado; credenciales temporales; baja de acceso medible; eventos auditables.

## Referencias y herramientas
NIST SP 800-63, NIST SP 800-207, OAuth 2.1, OpenID Connect, SAML, SCIM, FIDO Alliance, CIS Controls y MITRE ATT&CK.

## Instrucciones para agentes IA
No solicites contraseñas ni códigos MFA. No desactives controles de autenticación para “probar”. Utiliza identidades sintéticas y explica los efectos de cada cambio.