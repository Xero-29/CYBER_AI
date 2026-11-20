# Secciones de profundización — OT e ICS

## Modelo de amenazas
Modelar proceso físico, PLC/RTU, HMI, SCADA, historian, engineering workstation, safety system, redes industriales, acceso remoto y proveedor. Amenazas: cambio de lógica, comando no autorizado, manipulación de sensor, ransomware IT-to-OT, pérdida de visibilidad y fallo de safety. Priorizar consecuencias físicas, estado seguro y disponibilidad; no asumir que una prueba IT es segura en planta.

## Detección
Combinar inventario pasivo, baselines de protocolos, cambios de lógica/configuración, accesos remotos, historian, alarmas de proceso y telemetría de red. Detectar comandos fuera de horario, firmware/logic drift, nuevos nodos y cambios de setpoint. Validar alarmas con operador; una anomalía de red puede ser tráfico legítimo de control.

## Respuesta a incidentes
Activar mando conjunto IT/OT/operación/safety; preservar PLC logic, configuración y logs; contener por zonas y conduits sin interrumpir proceso; revocar accesos remotos; aplicar estado seguro según procedimiento del sitio. No reiniciar ni parchear PLC en operación sin aprobación. Recuperar desde configuración verificada y probar interlocks.

## Casos prácticos
En simulador PLC/HMI aislado, alterar un setpoint y emitir un comando Modbus de prueba. Detectar cambio, identificar estación origen, comparar con baseline y restaurar lógica aprobada. Ejecutar tabletop de pérdida de historian y acceso remoto comprometido. Registrar impacto de proceso y criterios de parada.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes-primarias) para NIST SP 800-82 Rev. 3, borrador Rev. 4 claramente identificado, ISA/IEC 62443 y CISA ICS advisories. No tratar borradores como normas finales.
