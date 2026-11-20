# Secciones de profundización — Seguridad inalámbrica

## Modelo de amenazas
Modelar AP, clientes, autenticación, roaming, radio, controlador, BLE, NFC/RFID y backend. Amenazas: evil twin, downgrade, credenciales débiles, desautenticación, rogue AP, pairing inseguro, relay, clonación de tag y fuga por metadatos. Incluir interferencia y disponibilidad, además de confidencialidad.

## Detección
Monitorizar inventario de AP/BSSID, cambios de canal, autenticación, roaming, certificados, eventos de asociación, BLE advertisements y uso de NFC/RFID. Detectar AP no autorizado, métodos de autenticación débiles, patrones de deauth, dispositivos nuevos y anomalías de pairing. Correlacionar ubicación y tiempo con cautela.

## Respuesta a incidentes
Identificar y aislar AP o dispositivo rogue, preservar capturas y logs, rotar credenciales/certificados, revisar clientes afectados y actualizar perfiles. En ataques de disponibilidad, coordinar canal alternativo y evitar cambios que amplifiquen interferencia. Para BLE/RFID, revocar credenciales o identificadores y reemplazar tags vulnerables.

## Casos prácticos
En laboratorio RF controlado, configurar WPA2-Enterprise/WPA3 y un AP de prueba no autorizado; observar detección y autenticación fallida sin interferir redes ajenas. En BLE, probar pairing y autorización con dos dispositivos sintéticos; documentar relay y controles de proximidad.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para Wi-Fi Alliance, IEEE 802.11, Bluetooth SIG, NIST wireless guidance y documentación NFC. Fijar versiones y perfiles de seguridad.
