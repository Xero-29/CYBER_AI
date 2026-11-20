# Investigación técnica: Windows, Active Directory e identidad empresarial

**ID:** windows_ad · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Ejecución Windows pendiente.

## Modelo
Modelar endpoints, servidores, dominios/forest, trusts, DC, DNS, Kerberos, LDAP, Group Policy, Entra ID/híbrido, PKI, endpoints de administración, backup y service accounts. Inventariar nivel funcional, versiones, sites, subnets, trusts, privilegios, delegaciones y dependencias de aplicaciones.

## Identidad y privilegios
Revisar cuentas privilegiadas, grupos protegidos, delegación, service accounts, gMSA, SPN, Kerberos tickets, NTLM legado, LDAP signing/channel binding, LAPS, MFA y Conditional Access en escenarios híbridos. Separar cuentas de usuario/admin, usar estaciones de administración dedicadas, JIT/JEA y tiering según modelo operativo. Controlar cuentas de servicio y secretos de automatización.

## Active Directory
Evaluar ACLs de objetos, delegación de control, GPO, SYSVOL, replicación, trusts, DNS, AD CS, plantillas de certificados, enrollment rights, shadow credentials, DCSync/DCSync rights y rutas de escalada. Analizar riesgos de AD CS con enfoque de configuración, permisos y abuso; no ejecutar técnicas de persistencia en dominios productivos.

## Windows endpoint/server
Aplicar security baselines por versión y rol; controlar Defender/EDR, firewall, PowerShell logging, WDAC/AppLocker, Credential Guard, Secure Boot, BitLocker, SMB signing, RDP, WinRM y actualización. No copiar una baseline de Server 2025 a versiones anteriores sin validar soporte y efectos.

## Detección
Correlacionar eventos de autenticación, Kerberos, cambios de grupos, creación de servicios/tareas, PowerShell, procesos, GPO, AD CS, replicación, endpoint y cloud identity. Mapear a ATT&CK con versión fijada; ATT&CK Data Sources fue deprecado en v18, por lo que los diseños nuevos deben basarse en Detection Strategies/Analytics actuales.

## Laboratorios
Forest/dominio aislado con DC, member server, workstation y usuarios sintéticos. Simular delegación incorrecta, GPO débil, Kerberos misconfiguration, permisos AD CS y cuentas de servicio; probar detecciones y restauración. Snapshots y red privada sin trust con redes reales.

## Fuentes
- Microsoft Windows Server 2025 Security Baselines: https://learn.microsoft.com/windows-server/security/osconfig/osconfig-how-to-configure-security-baselines
- Microsoft Learn Active Directory Domain Services: https://learn.microsoft.com/windows-server/identity/ad-ds/
- MITRE ATT&CK Enterprise: https://attack.mitre.org/matrices/enterprise/
- NIST NICE: https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center

**Límite:** el estudio es documental; la ejecución y las pruebas de AD/Windows quedan pendientes en entorno de laboratorio Windows.
