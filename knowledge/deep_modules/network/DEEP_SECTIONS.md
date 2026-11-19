# Secciones de profundización — Seguridad de redes

## Modelo de amenazas
Inventariar zonas, rutas, activos, planos de gestión, enlaces, DNS, VPN, Wi-Fi, servicios expuestos y dependencias del carrier. Amenazas: spoofing, envenenamiento, interceptación, movimiento lateral, abuso de túneles, segmentación incorrecta, DDoS y compromiso de equipos de red. Analizar rutas de administración y confianza entre redes, no solo puertos visibles.

## Detección
Correlacionar NetFlow/IPFIX, DNS, firewall, IDS/NDR, VPN, autenticación, DHCP, proxy y telemetría de switches/routers. Detectar beaconing, escaneo, cambios de ruta, DNS anómalo, conexiones este-oeste y egress inusual. Conservar timestamps sincronizados, topología y contexto de activo. Medir visibilidad por segmento y distinguir falta de telemetría de ausencia de amenaza.

## Respuesta a incidentes
Aislar segmentos o rutas comprometidas mediante cambios reversibles aprobados; preservar configuraciones y tablas de rutas; revocar claves VPN y credenciales de administración; bloquear indicadores con caducidad; revisar saltos laterales y equipos de borde. Recuperar configuraciones firmadas/conocidas, validar redundancia y comprobar que el bloqueo no interrumpe funciones críticas.

## Casos prácticos
Un equipo de laboratorio muestra consultas DNS periódicas hacia un dominio de prueba y conexiones salientes inesperadas. Capturar PCAP, resolver proceso/host/usuario, comparar con baseline, bloquear el dominio en entorno aislado y comprobar propagación de la regla. Repetir con DNS-over-HTTPS y un túnel VPN para evaluar puntos ciegos y límites de detección.

## Referencias
Fuentes y versiones en [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes-primarias): NIST SP 800-41, NIST SP 800-77, NIST SP 800-94, RFC relevantes y MITRE ATT&CK. Validar compatibilidad con la topología y el fabricante desplegado.
