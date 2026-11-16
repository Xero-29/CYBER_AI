# Ciberseguridad automotriz y CAN — Guía de dominio

**ID:** `automotive_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Evalúa ECU, redes internas, conectividad, telemática, infotainment, actualizaciones y backend. Los sistemas vehiculares pueden afectar seguridad física; no transmitir tramas, modificar ECU ni conectar herramientas de prueba a vehículos en circulación.

## Arquitectura y superficies
Inventariar ECU, CAN/CAN FD, LIN, FlexRay, Automotive Ethernet, gateway, OBD-II, TCU, infotainment, ADAS, sensores, secure element, OTA y backend. Analizar dominios de seguridad, separación safety/security, buses, diagnóstico UDS, boot chain, firmware y credenciales de fábrica.

## Competencias
- Comprender CAN IDs, arbitraje, frames, gateway y segmentación.
- Revisar autenticación de diagnóstico y controles UDS.
- Evaluar secure boot, firmware signing y anti-rollback.
- Proteger telemática, APIs móviles y backend.
- Analizar mensajes y señales con datasets sintéticos.
- Diseñar threat analysis and risk assessment (TARA).
- Coordinar ciberseguridad y seguridad funcional.
- Gestionar vulnerabilidades y actualizaciones durante vida útil.

## Controles
- Separar infotainment/telemática de dominios safety-critical.
- Autenticar diagnósticos y limitar funciones por estado del vehículo.
- Firmar actualizaciones y verificar integridad antes de instalar.
- Gestionar claves únicas y protección hardware.
- Registrar versiones y procedencia de firmware.
- Controlar interfaces OBD y acceso de talleres.
- Aplicar gateway filtering y detección de anomalías.
- Definir proceso de divulgación y respuesta de fabricante.

## Metodología
1. Definir vehículo, ECU, banco y autorización.
2. Crear arquitectura y activos con impacto safety.
3. Realizar TARA y mapear caminos de ataque.
4. Revisar firmware, protocolos y actualización de forma pasiva.
5. Probar en banco desconectado o simulador.
6. Validar controles con datos sintéticos y fault injection controlada.
7. Documentar impacto funcional y riesgo residual.
8. Aprobar cambios con ingeniería y safety.
9. Verificar regresión en banco y release firmado.

## Laboratorio
Simulador CAN o banco ECU de desarrollo aislado con tramas ficticias. Analizar captura PCAP/CAN y validar reglas de gateway. No enviar comandos de diagnóstico a vehículos reales.

## Evaluación
Interfaces y dominios inventariados, TARA documentada, firmware verificable, diagnósticos restringidos y cambios probados en banco.

## Referencias
ISO/SAE 21434, UNECE R155/R156, ISO 26262, AUTOSAR, SAE J3061 y MITRE ATT&CK for ICS como referencia parcial.

## Instrucciones IA
Prioriza seguridad física. No sugieras inyección de tramas ni manipulación de ECU en vehículos reales. Limita ejemplos a simuladores y bancos autorizados.