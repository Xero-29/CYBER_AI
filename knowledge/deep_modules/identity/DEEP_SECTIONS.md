# Secciones de profundización — Identidad y acceso

## Modelo de amenazas
Incluir IdP, directorios, federación, MFA, passkeys, sesiones, tokens, cuentas de servicio, workload identity, recovery flows, sincronización y privilegios. Amenazas: phishing, fatigue MFA, token theft, consentimiento malicioso, abuso de refresh token, federación mal configurada, cuentas huérfanas, escalada de privilegios y compromiso de IdP. Trazar identidad, autenticador, sesión y recurso.

## Detección
Correlacionar autenticaciones, MFA, emisión/refresh/revocación de tokens, cambios de grupos, roles, consentimientos, políticas, dispositivos y sesiones privilegiadas. Detectar impossible travel con cautela, spray, fatiga MFA, nuevos factores, OAuth grants anómalos, privilegios persistentes y cuentas inactivas reactivadas. Medir cobertura por IdP y aplicaciones federadas.

## Respuesta a incidentes
Deshabilitar o restringir identidad comprometida, revocar sesiones y refresh tokens, rotar credenciales y secretos de aplicaciones, revisar consentimientos, claves de federación y cuentas de servicio. Identificar recursos accedidos durante la ventana y propagar revocación a aplicaciones downstream. Restaurar accesos por proceso verificado y documentar impacto de sesiones no revocables inmediatamente.

## Casos prácticos
Simular consentimiento OAuth excesivo de una aplicación de prueba y robo de refresh token. Detectar grant, identificar scopes y recursos consultados, revocar consentimiento y sesiones, rotar secreto de aplicación y restringir permisos. Repetir con cuenta de servicio sin propietario y comprobar proceso de baja y alerta.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-63, OAuth 2.0 Security BCP, OpenID Connect, FIDO y CIS Controls. Fijar perfiles y versiones de protocolos.
