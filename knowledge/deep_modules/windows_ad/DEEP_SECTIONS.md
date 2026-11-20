# Secciones de profundización — Windows y Active Directory

## Modelo de amenazas
Modelar AD forest/domain, DC, DNS, Kerberos, LDAP, GPO, trusts, PKI, endpoints, cuentas de servicio, Entra/híbrido y rutas administrativas. Amenazas incluyen robo/reutilización de credenciales, Kerberoasting, abuso de delegación, ACLs peligrosas, DCSync, movimiento lateral, GPO maliciosa y compromiso de DC. Analizar privilegios efectivos y relaciones de confianza.

## Detección
Centralizar eventos de autenticación, Kerberos, cambios de grupos/GPO/ACL, creación de servicios/tareas, PowerShell, Defender/EDR, DNS y cambios en DC. Correlacionar usuario, host origen, logon ID, ticket, proceso y objeto AD. Detectar patrones anómalos de tickets, replicación, delegación y privilegios; validar cobertura de auditoría y retención en todos los controladores.

## Respuesta a incidentes
Ante sospecha de compromiso de dominio, preservar eventos de DC y endpoints, identificar alcance de credenciales/tickets, contener equipos y cuentas de forma coordinada, rotar secretos según plan de recuperación de AD y revisar trusts, GPO, ACLs y mecanismos de persistencia. La rotación indiscriminada de cuentas de servicio puede causar indisponibilidad; seguir runbook probado y recuperar desde estado confiable.

## Casos prácticos
En un dominio de laboratorio, una cuenta de servicio de prueba tiene SPN y contraseña débil. Demostrar exposición con herramientas de auditoría autorizadas, correlacionar eventos, corregir contraseña/gMSA y privilegios, y comprobar que no se rompen servicios. Segundo caso: GPO altera firewall; detectar cambio, identificar autor y restaurar versión aprobada.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para Microsoft Security Baselines, Windows event auditing, MITRE ATT&CK y CISA. Fijar versiones de Windows Server, AD schema y políticas aplicables.
