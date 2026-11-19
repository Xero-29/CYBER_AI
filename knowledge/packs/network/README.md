# Seguridad de redes — Guía de dominio

**ID:** `network` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Diseña y verifica redes empresariales, centros de datos, campus, WAN y segmentos cloud. La seguridad depende de identidad, segmentación, rutas, resolución de nombres, cifrado, administración y visibilidad. El escaneo activo, captura de tráfico y pruebas de disponibilidad requieren alcance autorizado y ventanas acordadas.

## Arquitectura y riesgos
Inventariar zonas de usuario, servidor, administración, producción, invitados, terceros, DMZ y OT. Mapear switching L2, routing L3, VPN, DNS, DHCP, NTP, proxies, firewalls, balanceadores, Wi-Fi, SD-WAN y enlaces externos. Riesgos prioritarios: redes planas, ACL permisivas, servicios de gestión expuestos, DNS inseguro, protocolos obsoletos, credenciales compartidas, rutas asimétricas y falta de telemetría.

## Competencias específicas
- Interpretar VLAN, VRF, routing, ACL, NAT, VPN y controles de salida.
- Diseñar segmentación basada en criticidad y Zero Trust.
- Evaluar TLS, IPsec, SSH, SNMPv3, DNSSEC y autenticación de red.
- Analizar PCAP y logs para detectar escaneo, beaconing, exfiltración y anomalías.
- Revisar reglas firewall por propietario, justificación, caducidad y flujo.
- Diseñar redundancia, gestión fuera de banda y recuperación de configuración.
- Distinguir detección de prevención y medir cobertura de sensores.

## Controles prioritarios
- Denegar por defecto entre zonas y permitir flujos mínimos documentados.
- Separar plano de administración, plano de datos y redes de usuarios.
- Exigir MFA y bastión para administración; limitar SSH/RDP/SNMP a redes de gestión.
- Usar DNS resolvers controlados, filtrado de salida y registros con retención.
- Retirar Telnet, FTP y protocolos criptográficos débiles; usar versiones TLS soportadas.
- Autenticar dispositivos y puertos donde corresponda; proteger Wi-Fi con WPA3-Enterprise/802.1X.
- Registrar cambios de reglas y revisar reglas huérfanas.
- Sincronizar relojes y conservar logs de firewall, DNS, VPN, DHCP y proxy.

## Metodología
1. Obtener diagramas, inventario, rutas y responsables.
2. Construir matriz origen-destino-protocolo-puerto-justificación.
3. Revisar reglas, servicios de gestión y exposición externa.
4. Comprobar segmentación mediante pruebas de conectividad no destructivas.
5. Analizar PCAP sintéticos o capturas autorizadas con filtros documentados.
6. Validar resolución DNS, certificados, VPN y rutas.
7. Revisar telemetría, tiempos, zonas horarias y alertas.
8. Probar failover y recuperación en laboratorio.
9. Entregar cambios de firewall como diff revisable con rollback.

## Laboratorio seguro
Topología local con router virtual, firewall, dos VLAN y servicios ficticios. Verificar que usuario no alcanza administración ni OT, analizar un PCAP sintético y ensayar pérdida de enlace. No ejecutar Nmap, Masscan ni pruebas de flooding fuera de un laboratorio propio.

## Evaluación
Flujos autorizados tienen dueño y justificación; administración está segmentada; logs permiten reconstruir actividad; pruebas de conectividad negativa confirman aislamiento; configuración puede restaurarse.

## Referencias y herramientas
NIST SP 800-41, CIS Benchmarks, MITRE ATT&CK, RFC 8446, Wireshark/TShark, Zeek, Suricata, Nmap y firewall vendor guides.

## Instrucciones para agentes IA
Empieza con revisión pasiva. No inventes topología ni afirmes que un puerto está abierto sin evidencia. Toda prueba activa debe comprobar autorización, rango y tasa; no realices DoS ni interceptación de terceros.

---

## Marco obligatorio de desarrollo experto e investigación

Este paquete se desarrolla conforme al [Estándar experto e investigación](../../EXPERT_RESEARCH_STANDARD.md). El estándar aplica a esta especialidad, no solo al currículo global.

**Estado del perfil:** estructura y mapa de evidencias definidos; el contenido técnico ampliado, la revisión integral de fuentes, los laboratorios ejecutados y la validación independiente se registran por separado. No se declara K4/K5 por la existencia de este marco.

Cada tema de esta especialidad debe desarrollarse como unidad independiente y cubrir: teoría, formalización pertinente, arquitectura, estándares versionados, implementación, análisis avanzado, seguridad adaptada al dominio, investigación, laboratorio/dataset, evaluación, Skills verificadas y trazabilidad. La matriz detallada de capas, evidencias, enfoque matemático y restricciones de laboratorio está en `knowledge/curricula/domain_curriculum.json`, dentro del perfil `network`.

**Madurez:** K1–K5 se asigna por tema y evidencia. Las ocho puertas G1–G8 deben mostrar estado explícito; lo no ejecutado o no revisado permanece pendiente. Las referencias descubiertas no cuentan como lectura completa y los laboratorios diseñados no cuentan como ejecutados.
