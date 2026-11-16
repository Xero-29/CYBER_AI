# Seguridad satelital y espacial — Guía de dominio

**ID:** `satellite_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege segmentos space, ground y link: satélite, payload, bus, TT&C, estaciones terrestres, gateways, terminales y sistemas de misión. La disponibilidad, integridad de comandos y seguridad física son esenciales. No transmitir, interferir ni intentar acceder a enlaces o activos espaciales reales.

## Arquitectura y amenazas
Inventariar flight software, OBC, payload, sensores, actuadores, radios, criptografía, antenas, ground station, misión, telemetría y proveedores. Riesgos: comandos no autenticados, replay, claves compartidas, firmware vulnerable, cadena de suministro, estaciones terrestres expuestas, GNSS spoofing/jamming, pérdida de sincronía y degradación orbital.

## Competencias
- Modelar trust boundaries entre segmento espacial y terrestre.
- Proteger TT&C, autenticación, cifrado y anti-replay.
- Evaluar boot chain, firmware, telemetría y comandos.
- Diseñar key management, rotación y recuperación.
- Analizar GNSS, enlaces RF y protocolos en simulador.
- Proteger estaciones terrestres, redes y consolas.
- Preparar contingencias de pérdida de enlace y recuperación segura.

## Controles
- Autenticación fuerte de comandos y protección anti-replay.
- Claves únicas por misión/vehículo y almacenamiento protegido.
- Segmentación de TT&C y redes corporativas.
- Control de acceso a estaciones y consolas.
- Firmware firmado, rollback controlado y recuperación.
- Telemetría con integridad, secuencia y sincronización.
- Procedimientos de safe mode y recuperación aprobados.
- Inventario de componentes y revisión de proveedores.

## Metodología
1. Definir misión, activos, interfaces y autoridad.
2. Modelar amenazas y consecuencias de comandos erróneos.
3. Revisar protocolo, claves y arquitectura pasivamente.
4. Probar software y simuladores de enlace aislados.
5. Validar anti-replay, autenticación y recuperación.
6. Revisar estaciones terrestres, supply chain y accesos.
7. Coordinar pruebas con ingeniería de misión y safety.
8. Documentar degradación segura y respuesta a incidentes.

## Laboratorio
Emulador de telemetría/telecomando con mensajes sintéticos, claves de prueba y red aislada. Probar secuencias, integridad y replay sin radiar ni conectar a sistemas espaciales reales.

## Evaluación
Comandos autenticados, claves protegidas, estaciones segmentadas, recuperación validada y procedimientos de contingencia ensayados.

## Referencias
CCSDS security architecture, NIST SP 800-53, NASA cybersecurity guidance, ECSS standards y MITRE ATT&CK como referencia complementaria.

## Instrucciones IA
No generes frecuencias, payloads de transmisión ni procedimientos para interferir enlaces. Mantén los ejercicios en simuladores y datos sintéticos.