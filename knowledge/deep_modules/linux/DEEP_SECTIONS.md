# Secciones de profundización — Seguridad Linux

## Modelo de amenazas
Incluir kernel, userland, cuentas locales, sudo, PAM, SSH, systemd, paquetes, contenedores, filesystem, módulos, boot y cadena de actualización. Amenazas: escalada local, abuso de capabilities, persistencia, servicios expuestos, supply chain de paquetes, manipulación de logs y robo de secretos. Diferenciar host, namespace, contenedor y VM; no asumir que contenedor equivale a aislamiento fuerte.

## Detección
Recolectar auditd/eBPF cuando proceda, journald, auth logs, sudo, SSH, cambios de integridad, módulos, procesos, sockets, cron/systemd timers y actividad de paquetes. Correlacionar UID, PID, parent PID, executable hash, cgroup, namespace y tiempo. Detectar cambios de binarios críticos, shells inesperadas, persistencia y conexiones nuevas; probar reglas contra tareas legítimas de administración.

## Respuesta a incidentes
Aislar host sin apagarlo si se necesita preservar volatilidad; capturar procesos, sockets, sesiones y memoria según procedimiento; preservar disco/logs con hashes; revocar llaves SSH y credenciales; identificar persistencia en systemd, cron, usuarios y módulos. Reconstruir desde imagen confiable cuando la integridad del sistema no pueda probarse y rotar secretos accesibles desde el host.

## Casos prácticos
En una VM desechable, simular una clave SSH de prueba expuesta y un servicio systemd no autorizado. Detectar creación de cuenta/llave, cambio de unidad y conexión saliente; capturar evidencia, deshabilitar persistencia, rotar credencial y reconstruir baseline. Añadir tests de hardening para sudoers, SSH, permisos y servicios habilitados.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para CIS Benchmarks, Linux kernel documentation, systemd, audit framework y NIST. Registrar distribución, versión de kernel y configuración; los controles varían entre familias.
