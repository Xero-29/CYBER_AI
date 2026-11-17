# Revisión de literatura inicial — Seguridad OT, ICS y SCADA

**Corte:** 2026-11-17  
**Madurez:** M1 documental; no M3/M4.  
**Alcance:** sistemas industriales y ciberfísicos, arquitectura, segmentación, operación segura, detección y respuesta.

## Pregunta

¿Cómo mejorar la seguridad de OT sin degradar seguridad funcional, disponibilidad, determinismo, confiabilidad ni continuidad del proceso físico?

## Síntesis de fuentes primarias

NIST SP 800-82 Rev. 3 (septiembre de 2023) define OT como sistemas programables que interactúan con el entorno físico o controlan dispositivos/procesos. Incluye ICS, automatización de edificios, transporte, control de acceso físico y monitoreo ambiental. La guía insiste en atender requisitos singulares de rendimiento, confiabilidad y seguridad.

A fecha de corte existe un **borrador público inicial de SP 800-82 Rev. 4**, publicado el 21-09-2026 con comentarios abiertos hasta 30-11-2026. Añade/reorganiza sectores OT, alinea el documento con CSF 2.0 y amplía orientación de inventario, monitoreo/detección, protección de funciones de gestión y principios Zero Trust. Es un borrador, no reemplaza la versión final vigente; mantener Rev. 3 como referencia final hasta que NIST publique Rev. 4 definitiva.

## Consecuencias arquitectónicas

- La seguridad funcional y la disponibilidad pueden tener precedencia sobre cambios de seguridad en tiempo real.
- No asumir que escaneo activo, reinicio, parcheo o bloqueo de red son inocuos.
- Separar redes por zonas/conduits y funciones; controlar accesos remotos y estaciones de ingeniería.
- Mantener inventario pasivo/validado de PLC, RTU, HMI, historiadores, gateways, firmware y dependencias.
- Detección basada en protocolos/telemetría industrial con baseline de proceso y coordinación con ingeniería.
- Respuesta debe coordinar operador OT, seguridad, seguridad funcional, proveedor y responsable del proceso.
- Ensayar cambios en simulador/digital twin o banco aislado antes de producción.

## Hipótesis investigables

- H1: monitoreo pasivo más inventario validado detecta cambios de activos/configuración con menor riesgo de interrupción que escaneo activo indiscriminado.
- H0: no hay diferencia medible en cobertura/impacto bajo el laboratorio.
- H2: un procedimiento de respuesta OT con autorización del operador y criterios de seguridad funcional reduce acciones inseguras frente a un playbook IT genérico.

## Protocolo propuesto (no ejecutado)

- **Banco:** simulador PLC/HMI o testbed industrial aislado; proceso físico simulado y datos sintéticos.
- **Escenarios:** activo no inventariado, cambio de lógica, acceso remoto inesperado, tráfico anómalo y pérdida de telemetría.
- **Comparadores:** inventario manual, sondeo activo limitado y monitorización pasiva.
- **Métricas:** cobertura y exactitud de inventario, detección de cambios, falsos positivos/hora, latencia, CPU/red, pérdida de paquetes, tiempo de detección y efecto sobre el proceso simulado.
- **Seguridad:** no enviar paquetes de prueba a PLC/SCADA de producción; no ejecutar pruebas disruptivas ni malware; criterios de parada definidos por ingeniería.
- **Análisis:** sensibilidad por protocolo/topología, condiciones de carga, validez externa limitada por el testbed.

## Referencias y control de versión

- NIST SP 800-82 Rev. 3, final, 2023-09. https://csrc.nist.gov/pubs/sp/800/82/r3/final
- NIST SP 800-82 Rev. 4, initial public draft, 2026-09-21; comments due 2026-11-30. https://csrc.nist.gov/pubs/sp/800/82/r4/ipd
- NIST SP 800-207, Zero Trust Architecture. https://csrc.nist.gov/pubs/sp/800/207/final

## Brechas

Leer el texto íntegro de Rev. 3 y el borrador Rev. 4, comparar cambios por sección, añadir IEC 62443 con licencia/procedencia verificada y fuentes sectoriales, ejecutar un testbed y someter el protocolo a revisión de un especialista OT/seguridad funcional.
\n\n## Identificadores del registro de fuentes\n\n- `NIST-SP-800-82r3`\n- `NIST-SP-800-82r4-IPD`\n- `NIST-SP-800-207`\n