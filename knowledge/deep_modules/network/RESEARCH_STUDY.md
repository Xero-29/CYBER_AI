# Investigación técnica: Redes y seguridad de comunicaciones

**ID:** network · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 en elaboración · **Revisión experta:** pendiente.

## Modelo del dominio
Una red debe analizarse como un sistema distribuido de planos y límites de confianza, no como una lista de puertos. Separar plano de datos, plano de control, plano de gestión, identidad, resolución de nombres, sincronización temporal, servicios de infraestructura y telemetría. Documentar topología física/lógica, direccionamiento, rutas, zonas, VRF/VLAN, puntos de inspección, dependencias externas, enlaces redundantes y propietarios.

El modelo de amenaza debe considerar adversarios externos e internos, errores de configuración, fallos de proveedor, abuso de credenciales, dispositivos no administrados, compromisos de cadena de suministro y fallos de protocolos. La ubicación en una LAN no equivale a confianza: NIST SP 800-207 orienta el acceso a recursos según sujeto, dispositivo y contexto, con autenticación y autorización explícitas.

## Protocolos y mecanismos
### Switching y Ethernet
Dominar trama Ethernet, MTU, VLAN 802.1Q, tablas MAC, STP/RSTP, LACP, ARP/ND y broadcast/multicast. Evaluar segmentación por función y criticidad; una VLAN no constituye por sí sola una frontera fuerte si existen rutas, trunks o administración compartida. Revisar puertos access/trunk, VLAN nativa, BPDU Guard/Root Guard, DHCP snooping, Dynamic ARP Inspection y controles NAC según el equipo.

### IP y routing
Estudiar IPv4/IPv6, ICMP, subnetting, routing estático/dinámico, BGP, OSPF, VRF, ACL y políticas de ruta. Analizar filtrado de prefijos, RPKI origin validation, protección de sesiones de routing, route leaks, exposición de gestión y resiliencia ante cambios. Distinguir filtrado de paquetes, inspección stateful, proxy de aplicación y controles de identidad.

### TCP y UDP
TCP: establecimiento/cierre, números de secuencia, ACK, retransmisión, ventanas, control de congestión, RST y estados. RFC 9293 consolida la especificación moderna de TCP y debe leerse junto con RFC vigentes de congestión y temporizadores. UDP no garantiza entrega ni orden; analizar amplificación, spoofing, rate limiting, fragmentación y autenticación de aplicación. Probar pérdidas, reordenamiento, latencia, MTU, resets y límites de recursos solo en endpoints propios.

### DNS, DHCP y tiempo
DNS: resolución recursiva/autoritativa, delegación, caché, TTL, DNSSEC, split-horizon, DoH/DoT, logging y protección de zonas. DHCP: scopes, reservas, relay, opciones, rogue DHCP y controles L2. NTP/PTP: jerarquía, fuentes confiables, deriva y efecto del tiempo incorrecto en certificados, logs y correlación forense. DNSSEC no elimina compromiso del endpoint o del resolver.

### TLS, VPN e identidad del canal
TLS separa handshake y record protocol; evaluar autenticación, negociación, suites AEAD, derivación de claves, certificados, nombres, revocación, reanudación y 0-RTT. **Actualización crítica:** RFC 9846, publicado en julio de 2026, sustituye RFC 8446 como especificación TLS 1.3. 0-RTT puede permitir replay; restringirlo a operaciones idempotentes o aplicar mitigaciones de repetición a nivel de aplicación. VPN/IPsec/WireGuard deben evaluarse por identidad, gestión de claves, rutas, split tunneling, postura del endpoint, revocación y observabilidad.

### Wi-Fi
Estudiar 802.11, WPA2/WPA3, 802.1X/EAP, RADIUS, roaming, redes invitadas, gestión de claves y ataques de desautenticación/evil twin. Diseñar separación de invitados, IoT y usuarios, protección de management frames cuando sea compatible y telemetría de controladores. No probar interferencia o deauth fuera de laboratorio autorizado.

## Amenazas y controles
| Superficie | Amenazas | Controles y evidencia |
|---|---|---|
| Switching | VLAN hopping, rogue DHCP, ARP spoofing, loops | Hardening L2, DHCP snooping, DAI, revisión de trunks |
| Routing | Route leak, hijack, gestión expuesta | Filtrado, RPKI, ACL de control plane, autenticación y logging |
| DNS | Cache poisoning, tunneling, shadow domains | DNSSEC donde proceda, resolvers controlados, detección y logging |
| Transporte | Agotamiento de estado, spoofing, resets | Rate limits, protección de estado, capacidad y telemetría |
| TLS/VPN | Certificados inválidos, downgrade, claves expuestas | Configuración actual, PKI, rotación y validación de nombre |
| Wireless | Rogue AP, credenciales débiles, segmentación rota | WPA3/802.1X, detección RF, aislamiento e identidad |
| Gestión | SNMP/SSH/API expuestos, credenciales compartidas | Red de gestión separada, MFA, bastion, secretos y auditoría |

Cada control debe vincularse a amenaza, precondición, activo, responsable, prueba y riesgo residual. Evitar listas de hardening sin contexto de plataforma y versión.

## Método de evaluación autorizada
1. Descubrir activos desde CMDB, controladores, tablas de routing y fuentes pasivas antes de escanear.
2. Aprobar alcance: CIDR/hosts, exclusiones, intensidad, horario, contactos y límites de impacto.
3. Construir baseline pasivo de flujos y servicios; preservar timestamps y sincronización.
4. Ejecutar pruebas graduales en laboratorio y luego pruebas activas aprobadas, con rate limit y stop conditions.
5. Validar hallazgos manualmente; distinguir exposición, vulnerabilidad, explotabilidad e impacto.
6. Correlacionar configuración, logs, rutas, DNS, certificados y telemetría.
7. Repetir tras remediación y registrar antes/después.

**Métricas:** cobertura de inventario, porcentaje de flujos con propietario, reglas sin uso, servicios expuestos no aprobados, MTTR de exposición, latencia p50/p95/p99, pérdida, disponibilidad, falsos positivos y éxito de segmentación negativa.

## Laboratorios reproducibles
- Topología virtual de tres zonas, router/firewall, DNS recursivo, servidor TLS y cliente.
- Simulación de route leak y validación de política sin anunciar rutas a Internet.
- DNS lab con zona controlada, DNSSEC y consultas sintéticas.
- PCAP sintéticos para validar parser, detección y correlación.
- TLS lab con certificados de prueba, suites y versiones configuradas; nunca degradar endpoints productivos.
- Dataset benigno/anómalo para medir detección de beaconing, tunneling y escaneo.

Fijar versiones, topología, configuración, semillas, PCAP, comandos, salidas esperadas, hashes y limpieza del entorno.

## Criterios de aceptación
Diagrama L2/L3 y límites de confianza revisados; catálogo de protocolos con RFC/edición actual y obsolescencia; amenaza-control-telemetría-prueba trazable; laboratorios repetibles para routing, DNS, TLS y segmentación; casos negativos y falsos positivos documentados; revisión independiente.

## Fuentes primarias
- NIST SP 800-207 Zero Trust: https://doi.org/10.6028/NIST.SP.800-207
- IETF RFC 9293 TCP: https://www.rfc-editor.org/rfc/rfc9293.html
- IETF RFC 9846 TLS 1.3 (2026; reemplaza RFC 8446): https://www.rfc-editor.org/rfc/rfc9846.html
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1
- MITRE ATT&CK Enterprise: https://attack.mitre.org/matrices/enterprise/

**Estado de evidencia:** se inspeccionaron páginas oficiales, metadatos y resúmenes. No se afirma lectura integral de cada estándar, validación de conformidad ni revisión experta.
