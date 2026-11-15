# Seguridad Windows y Active Directory — Guía de dominio

**ID:** `windows_ad` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Protege endpoints Windows, servidores, identidades de dominio y servicios de directorio. El dominio AD debe tratarse como plano de control de la organización: comprometer identidades privilegiadas puede afectar estaciones, servidores, políticas y copias de seguridad. La enumeración y simulación de técnicas adversarias se limita a dominios de laboratorio o autorizados.

## Arquitectura y amenazas
Inventariar bosques, dominios, controladores, trusts, OUs, GPO, DNS, LDAP, Kerberos, AD CS, Entra ID/identidad híbrida, cuentas de servicio y estaciones privilegiadas. Amenazas: Kerberoasting, AS-REP roasting, abuso de delegación, ACLs peligrosas, DCSync, pass-the-ticket, password spraying, abuso de certificados, GPO débil, cuentas huérfanas y movimiento lateral.

## Competencias específicas
- Comprender Kerberos, NTLM, LDAP, DNS y replicación de directorio.
- Revisar privilegios de Domain Admin, Enterprise Admin y grupos delegados.
- Analizar ACLs, delegación, SPN, trusts y rutas de escalada.
- Endurecer controladores de dominio, AD CS y políticas de autenticación.
- Aplicar Windows LAPS, tiering administrativo y estaciones PAW.
- Revisar GPO, scripts de inicio, tareas programadas y servicios.
- Correlacionar eventos Windows y telemetría EDR.

## Controles prioritarios
- Reducir miembros de grupos privilegiados y usar cuentas separadas de administración.
- Evitar inicio de sesión de cuentas Tier 0 en estaciones de usuario.
- Desplegar Windows LAPS y rotar secretos de cuentas locales/servicio.
- Eliminar protocolos heredados cuando sea viable y exigir SMB signing donde corresponda.
- Revisar delegación Kerberos y deshabilitar configuraciones inseguras.
- Proteger AD CS: plantillas, permisos de inscripción, EKU y claves privadas.
- Auditar cambios de grupos, GPO, trusts, cuentas, SPN y políticas de autenticación.
- Mantener controladores parcheados, respaldos de System State y recuperación ensayada.
- Usar MFA y acceso condicional para identidad híbrida.

## Metodología
1. Obtener inventario de bosque, dominios, DCs, OUs y cuentas privilegiadas.
2. Revisar baseline y eventos de seguridad relevantes.
3. Analizar relaciones de privilegio y rutas de ataque con datos autorizados.
4. Revisar ACLs, GPO, delegación, SPN, AD CS y cuentas de servicio.
5. Verificar MFA, LAPS, tiering, PAW y políticas de acceso.
6. Correlacionar hallazgos con MITRE ATT&CK.
7. Priorizar rutas que alcanzan Tier 0 y cerrar primero las de mayor impacto.
8. Probar cambios en laboratorio, respaldar y validar replicación.
9. Repetir análisis para comprobar que las rutas se cerraron.

## Laboratorio seguro
Bosque AD desechable con un DC y dos clientes, usuarios ficticios y cuentas de prueba. Usar Purple Knight/BloodHound Community solo para análisis del laboratorio y documentar rutas de privilegio. No ejecutar técnicas de extracción de credenciales ni pruebas de contraseña contra dominios reales.

## Evaluación
Privilegios Tier 0 mínimos, delegaciones justificadas, cuentas de servicio controladas, GPO verificadas, telemetría activa y recuperación de AD ensayada.

## Referencias
Microsoft Security Baselines, Microsoft AD DS/AD CS guidance, MITRE ATT&CK Enterprise, CIS Microsoft Windows Server Benchmark y NIST SP 800-53.

## Instrucciones para agentes IA
No generes comandos de dumping de credenciales ni persistencia. Prioriza consultas de solo lectura y configuración defensiva. Señala si una prueba puede bloquear cuentas o afectar replicación.