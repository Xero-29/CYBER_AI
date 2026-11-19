# Investigación técnica: Seguridad inalámbrica, Wi-Fi, Bluetooth y NFC

**ID:** wireless_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Pruebas RF autorizadas pendientes.

## Modelo
Analizar espectro, radios, firmware, pairing, identity, key management, AP/controller, client, roaming, gateway, backend y entorno físico. Identificar banda, protocolo, versión, capacidades, regulatory domain, potencia, canal y dispositivos. Interferencia y pruebas RF pueden afectar terceros; usar jaula/cámara RF o laboratorio autorizado.

## Wi-Fi
Dominar 802.11, WPA2/WPA3, 802.1X/EAP, RADIUS, SAE, PMF/802.11w, roaming, enterprise certificates, guest networks y controller management. Revisar PSK reuse, weak passphrase, evil twin, rogue AP, downgrade, deauth, misconfigured guest VLAN y management exposure. WPA3 no elimina phishing de portal, endpoint compromise o misconfiguration.

## Bluetooth/BLE
Revisar pairing modes, bonding, LE Secure Connections, GATT, service/characteristic permissions, privacy addresses, key storage, firmware updates, debug interfaces y device identity. Riesgos: weak pairing, insecure GATT, spoofing, tracking, relay, downgrade y exposed debug. Probar con dispositivos propios y datos sintéticos.

## NFC/RFID
Entender proximity, tag types, NDEF, secure elements, access cards, anti-collision, key diversification, relay, cloning and reader configuration. No copiar tarjetas ni probar control de acceso real sin permiso explícito; usar tarjetas de laboratorio.

## Controles
Inventario de AP/client/IoT, 802.1X/EAP-TLS donde aplique, certificados y revocación, WPA3/SAE, PMF, segmentación, guest isolation, NAC, WIDS/WIPS con cuidado, firmware firmado y control de administración. Revisar compatibilidad y legacy clients.

## Laboratorios
AP de laboratorio, clients de prueba, BLE dev boards, NFC tags propios, shielded RF environment, packet captures y tests de pairing. Medir coverage, rogue AP detection, auth failures, client isolation, false alarms, RF interference y recovery.

## Fuentes
- IEEE 802.11 Working Group: https://www.ieee802.org/11/
- Bluetooth Core Specification: https://www.bluetooth.com/specifications/specs/
- NFC Forum specifications: https://nfc-forum.org/build/specifications/
- NIST SP 800-94 IDPS (referencia histórica): https://doi.org/10.6028/NIST.SP.800-94

**Límite:** especificaciones completas pueden requerir acceso/licencia; verificar edición y regulación de espectro por país.
