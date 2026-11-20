# Investigación técnica: Seguridad Linux y Unix

**ID:** linux · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación por distribución pendiente.

## Modelo del sistema
Analizar boot chain, firmware, kernel, namespaces, cgroups, systemd/init, usuarios, PAM, sudo, filesystem, paquetes, servicios, sockets, capabilities, SELinux/AppArmor, audit, logs y actualización. Diferenciar distribuciones, versiones de kernel, LTS, hardening del proveedor y perfiles de uso.

## Identidad y privilegios
Revisar UID/GID, grupos, sudoers, PAM, SSH, cuentas de servicio, capabilities, setuid/setgid, ACL, namespaces y permisos de archivos. Eliminar cuentas innecesarias, prohibir login root remoto, usar MFA/bastion cuando proceda, claves SSH protegidas y rotación de credenciales. No asumir que deshabilitar contraseña en SSH cubre todos los métodos de autenticación.

## Kernel y aislamiento
Comprender syscall boundary, modules, seccomp, namespaces, cgroups, capabilities, LSM, ptrace y procfs/sysfs. Endurecer módulos, sysctl y servicios según rol. Contenedores comparten kernel y no sustituyen VM/microVM ante adversarios de kernel. SELinux/AppArmor deben probarse en enforcing con política específica; deshabilitar controles por conveniencia elimina defensa.

## Servicios y supply chain
Inventariar paquetes, repositorios, firmas, dependencias, servicios systemd, cron/timers, sockets, firewall, DNS y actualizaciones. Usar repositorios firmados y canales soportados; verificar provenance, CVE y backports de la distribución. Un número de versión upstream no siempre refleja el parche aplicado por el proveedor.

## Logging y respuesta
Configurar journald/syslog/auditd según amenaza y retención. Proteger logs, timestamps, permisos y envío remoto. Correlacionar auth, sudo, SSH, process execution, kernel events, package manager, network y service changes. Minimizar datos sensibles en logs.

## Evaluación
Inventario, baseline por rol, permisos anómalos, servicios expuestos, kernel config, patch status, integridad de paquetes, reglas firewall y auditoría. Probar restauración y rollback. No aplicar hardening ciego en servidores de producción sin change control.

## Laboratorios
VM snapshot con Debian/Ubuntu/RHEL-family; probar sudo least privilege, SSH, SELinux/AppArmor, systemd hardening, auditd, kernel module policy y firewall. Simular escalada solo con CVEs deliberadamente vulnerables y aisladas. Registrar distro, kernel, paquetes, config y resultados.

## Fuentes
- Linux kernel documentation: https://docs.kernel.org/
- systemd documentation: https://www.freedesktop.org/software/systemd/man/
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks

**Límite:** no existe un baseline universal; los controles deben ser versionados por distro y rol.
