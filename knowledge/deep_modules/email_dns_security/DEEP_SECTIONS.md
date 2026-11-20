# Secciones de profundización — Seguridad de correo y DNS

## Modelo de amenazas
Modelar registrador, DNS autoritativo/recursivo, MX, MTA, gateway, buzón, IdP, SPF, DKIM, DMARC, MTA-STS, TLS-RPT y terceros. Amenazas: spoofing, BEC, phishing, dominio lookalike, takeover DNS, subdominio abandonado, forwarding abusivo y robo de sesión. Incluir proveedores de marketing y SaaS.

## Detección
Analizar autenticación SPF/DKIM/DMARC, cambios DNS, registros MX, creación de reglas de buzón, forwarding externo, OAuth grants y patrones de envío. Detectar dominios similares, anomalías de volumen, fallos de alineación, cambios de selector DKIM y accesos anómalos. Conservar headers y trazabilidad de mensaje.

## Respuesta a incidentes
Bloquear dominio/remitente con contexto, preservar headers y logs, revocar sesiones y tokens, retirar reglas maliciosas, rotar credenciales y revisar mensajes entregados. Corregir DNS/DMARC de forma gradual y validar impacto en emisores legítimos. Coordinar takedown de dominios y notificación a destinatarios.

## Casos prácticos
Enviar mensajes de prueba desde dominio de laboratorio con SPF/DKIM válidos e inválidos; medir decisión DMARC. Simular regla de forwarding maliciosa en buzón sintético, detectarla, revocar sesión y revisar alcance. Verificar DNSSEC y rollback de registros sin afectar producción.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para RFC 7208, 6376, 7489, 8461, 8460, CISA y documentación de proveedores. Registrar estado y fecha de cada RFC.
