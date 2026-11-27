# Seguridad Linux y Unix — Guía de dominio

**ID:** `linux` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Endurece sistemas Linux/Unix, servicios, hosts de contenedores y estaciones de administración. Considera kernel, paquetes, usuarios, privilegios, servicios, red, almacenamiento, arranque y telemetría. No ejecutes cambios sobre hosts productivos sin ventana, respaldo, revisión y plan de reversión.

## Superficie y amenazas
Revisar cuentas locales, SSH, sudo, PAM, capabilities, namespaces, systemd, cron, sockets, módulos de kernel, paquetes, repositorios, filesystem, logs, firewall y procesos. Riesgos: root remoto, sudoers excesivo, claves SSH sin rotación, servicios innecesarios, binarios SUID/SGID, capabilities peligrosas, permisos débiles, secretos en archivos, persistencia en systemd/cron y kernel sin parches.

## Competencias específicas
- Analizar autenticación local, PAM, SSH y políticas sudo.
- Aplicar least privilege con usuarios de servicio y Linux capabilities.
- Revisar systemd, cron, sockets y unidades privilegiadas.
- Evaluar kernel, módulos, sysctl, namespaces, seccomp y LSM.
- Auditar permisos, ACL, SUID/SGID, montajes y cifrado de disco.
- Centralizar auditd, journald, syslog y telemetría de procesos.
- Gestionar paquetes, repositorios firmados y actualizaciones reproducibles.
- Preparar hardening y baseline para imágenes inmutables.

## Controles prioritarios
- Deshabilitar login SSH root y autenticación por contraseña cuando la operación lo permita; usar claves protegidas y MFA en bastión.
- Revisar sudoers con validación sintáctica y comandos mínimos.
- Quitar servicios, puertos y paquetes no requeridos.
- Aplicar actualizaciones de seguridad y verificar origen/firma de paquetes.
- Configurar umask, permisos y propietarios; proteger archivos de credenciales.
- Limitar capabilities y evitar contenedores privilegiados.
- Activar auditd y logs persistentes con tiempo sincronizado.
- Aplicar SELinux/AppArmor en modo enforcing tras validar políticas.
- Proteger arranque, Secure Boot cuando aplique y recuperación de claves.

## Metodología
1. Identificar distribución, versión, kernel, rol y criticidad.
2. Capturar baseline de paquetes, servicios, usuarios, puertos y permisos.
3. Comparar configuración con CIS Benchmark correspondiente.
4. Revisar accesos privilegiados, sudo, SSH, cron y systemd.
5. Analizar logs de autenticación, kernel y auditoría.
6. Proponer cambios en modo diff; probar en clon o VM.
7. Medir impacto en disponibilidad y compatibilidad.
8. Aplicar con rollback y verificar el estado posterior.
9. Automatizar controles de regresión con Ansible, OpenSCAP o scripts idempotentes.

## Laboratorio seguro
VM desechable con distribución soportada, usuario normal, cuenta de servicio y servicio HTTP de prueba. Generar baseline, corregir permisos, endurecer SSH, auditar sudo y comparar logs. No usar malware real ni ejecutar payloads con privilegios.

## Criterios de evaluación
Se conoce versión y propietario; privilegios mínimos; servicios necesarios; parches y repositorios confiables; logs útiles; hardening probado; rollback disponible.

## Marcos y herramientas
CIS Linux Benchmarks, DISA STIG cuando aplique, NIST SP 800-123, OpenSCAP, Lynis, auditd, osquery, Ruff/ShellCheck para automatización.

## Instrucciones para agentes IA
No sugieras comandos destructivos ni cambios directos de firewall/SSH sin mostrar impacto y rollback. Diferencia comandos de inspección de comandos de modificación. No expongas hashes de contraseñas ni secretos en salidas.

---

## Marco obligatorio de desarrollo experto e investigación

Este paquete se desarrolla conforme al [Estándar experto e investigación](../../EXPERT_RESEARCH_STANDARD.md). El estándar aplica a esta especialidad, no solo al currículo global.

**Estado del perfil:** estructura y mapa de evidencias definidos; el contenido técnico ampliado, la revisión integral de fuentes, los laboratorios ejecutados y la validación independiente se registran por separado. No se declara K4/K5 por la existencia de este marco.

Cada tema de esta especialidad debe desarrollarse como unidad independiente y cubrir: teoría, formalización pertinente, arquitectura, estándares versionados, implementación, análisis avanzado, seguridad adaptada al dominio, investigación, laboratorio/dataset, evaluación, Skills verificadas y trazabilidad. La matriz detallada de capas, evidencias, enfoque matemático y restricciones de laboratorio está en `knowledge/curricula/domain_curriculum.json`, dentro del perfil `linux`.

**Madurez:** K1–K5 se asigna por tema y evidencia. Las ocho puertas G1–G8 deben mostrar estado explícito; lo no ejecutado o no revisado permanece pendiente. Las referencias descubiertas no cuentan como lectura completa y los laboratorios diseñados no cuentan como ejecutados.
