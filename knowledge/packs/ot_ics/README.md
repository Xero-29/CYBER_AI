# Seguridad OT, ICS y SCADA — Guía de dominio

**ID:** `ot_ics` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege procesos industriales donde disponibilidad, seguridad física y calidad del producto pueden ser prioritarias. Una acción de ciberseguridad puede provocar daño físico o pérdida de control. No realizar escaneos activos, fuzzing, cambios de PLC ni pruebas de explotación en producción industrial.

## Arquitectura y protocolos
Inventariar PLC, RTU, DCS, HMI, historiadores, ingeniería, safety instrumented systems, gateways, estaciones y enlaces remotos. Modelar Purdue/ISA-95 sin asumir que todos los sitios siguen ese patrón. Reconocer Modbus/TCP, DNP3, OPC UA, Profinet, EtherNet/IP, IEC 61850 y protocolos propietarios. Identificar límites IT/OT, zonas, conduits y dependencias de tiempo real.

## Competencias
- Clasificar activos por impacto de seguridad, proceso y disponibilidad.
- Aplicar IEC 62443 zones/conduits y requisitos por nivel de seguridad.
- Analizar acceso remoto de proveedores y estaciones de ingeniería.
- Revisar firmware, lógica PLC, backups y cambios de configuración.
- Diseñar segmentación industrial, DMZ y monitoreo pasivo.
- Preparar respuesta coordinada con operadores de proceso y safety.
- Evaluar vulnerabilidades con contexto de versión, exposición y compensaciones.

## Controles prioritarios
- Inventario pasivo y propietario técnico/operacional por activo.
- Segmentación estricta IT/OT y acceso remoto mediante jump hosts controlados.
- MFA para acceso remoto; cuentas individuales y ventanas autorizadas.
- Allowlisting de aplicaciones en estaciones de ingeniería.
- Backups offline de lógica, recetas y configuraciones, con restauración ensayada.
- Monitorización pasiva con sensores compatibles con el proceso.
- Gestión de cambios MOC y aprobación del responsable de operación.
- Control de medios extraíbles y mantenimiento de proveedores.
- Coordinación con seguridad funcional; no alterar SIS por controles IT.

## Metodología
1. Obtener autorización del propietario de planta y responsable de seguridad funcional.
2. Revisar diagramas, inventario y dependencias con operadores.
3. Analizar configuración y tráfico pasivamente.
4. Priorizar rutas de acceso remoto, ingeniería y puentes IT/OT.
5. Diseñar mitigaciones con impacto operativo y plan de reversión.
6. Probar cambios en banco de laboratorio o gemelo digital.
7. Ejecutar solo con ventana, MOC, operador presente y parada segura definida.
8. Verificar proceso, alarmas y disponibilidad después del cambio.

## Laboratorio
Simulador PLC/SCADA o banco didáctico desconectado. Capturar tráfico sintético Modbus/OPC UA, construir inventario y validar reglas de detección pasiva. No conectar a redes de planta.

## Evaluación
Activos y flujos críticos identificados, segmentación revisada, acceso remoto controlado, backups probados y cada cambio aprobado por operaciones/safety.

## Referencias
IEC 62443, NIST SP 800-82 Rev. 3, CISA Cross-Sector Cybersecurity Performance Goals, MITRE ATT&CK for ICS y CISA ICS advisories.

## Instrucciones IA
Prioriza seguridad humana y continuidad. No envíes paquetes activos ni comandos a PLC/RTU. Recomienda primero captura pasiva y simulación; exige aprobación operacional para cambios.