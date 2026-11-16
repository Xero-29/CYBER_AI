# Seguridad inalámbrica, Bluetooth y NFC — Guía de dominio

**ID:** `wireless_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito
Evalúa WLAN, Bluetooth Classic/LE, NFC, RFID y protocolos de proximidad. Las pruebas radioeléctricas afectan dispositivos y espectro; solo deben ejecutarse en laboratorio blindado o entorno controlado con autorización. No capturar comunicaciones privadas de terceros.

## Superficie y amenazas
Inventariar AP, controladores, clientes, SSID, WPA Enterprise/Personal, 802.1X, RADIUS, EAP, BLE GATT, pairing, bonding, NFC tags, lectores y gateways. Riesgos: PSK débil/compartida, rogue AP, evil twin, downgrade, configuración EAP incorrecta, pairing inseguro, BLE services expuestos, replay y NFC tags no autenticados.

## Competencias
- Diseñar WPA3-Enterprise/802.1X y RADIUS con certificados.
- Revisar roaming, PMF/802.11w y segmentación de invitados.
- Analizar pairing BLE, bonding, privacy addresses y GATT permissions.
- Evaluar NFC NDEF, autenticación y controles anti-replay.
- Detectar AP rogue mediante sensores autorizados.
- Revisar firmware, actualizaciones y claves de dispositivos.
- Correlacionar eventos WLAN con identidad y NAC.

## Controles
- WPA3-Enterprise cuando sea compatible; retirar WEP/WPA/TKIP.
- EAP-TLS y validación estricta de certificados.
- Rotación y unicidad de credenciales; no PSK compartidas para empresa.
- PMF y segmentación de invitados/IoT.
- Deshabilitar servicios BLE innecesarios y exigir autorización por característica.
- No usar UID NFC como autenticación secreta.
- Limitar lectores, tags y acceso físico.
- Inventariar firmware y retirar dispositivos sin soporte.

## Metodología
1. Definir bandas, canales, SSID, dispositivos y límites físicos.
2. Inventariar configuración desde controladores y endpoints.
3. Revisar certificados, RADIUS, segmentación y políticas.
4. Analizar pairing y GATT en dispositivos de laboratorio.
5. Probar roaming y pérdida de conectividad con clientes sintéticos.
6. Verificar detección de rogue AP sin interferir.
7. Revisar NFC con tags propios y datos de prueba.
8. Documentar alcance, resultados y riesgos de disponibilidad.

## Laboratorio
AP aislado sin conexión a redes externas, dos clientes de prueba, periférico BLE y tags NFC propios. Validar EAP-TLS, pairing, permisos GATT y detección. No ejecutar deauth, jamming o captura de tráfico ajeno.

## Evaluación
Cifrado moderno, autenticación validada, segmentación, servicios mínimos, firmware soportado y pruebas sin impacto a terceros.

## Referencias
IEEE 802.11, WPA3/ Wi-Fi Alliance, Bluetooth Core Specification, NFC Forum, NIST SP 800-153 y OWASP IoT.

## Instrucciones IA
No recomiendes jamming, deauthentication ni interceptación. Usa configuraciones exportadas, simuladores y equipos propios; prioriza controles defensivos.