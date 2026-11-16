# Seguridad de correo y DNS — Guía de dominio

**ID:** `email_dns_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege correo, dominios, resolución de nombres y autenticación de mensajes. El correo es vector de fraude, phishing, malware y fuga; DNS soporta identidad, routing y confianza. Cambios de DNS o correo pueden interrumpir servicios, por lo que deben revisarse y planificarse.

## Competencias
- Configurar SPF, DKIM y DMARC con alineación y reportes.
- Revisar MTA, relay, TLS, MTA-STS y TLS-RPT.
- Proteger MX, DNS autoritativo, registrar y DNSSEC.
- Analizar BEC, spoofing, phishing y abuso de dominios.
- Revisar forwarding, reglas inbox, OAuth apps y cuentas delegadas.
- Gestionar dominios similares, expiración y transfer locks.
- Correlacionar cabeceras, autenticación y logs.

## Controles
- DMARC en política gradual hacia reject tras analizar reportes.
- SPF con un único registro, límites DNS y remitentes necesarios.
- DKIM con claves rotadas y selectores controlados.
- DNSSEC cuando el proveedor y la operación lo soporten.
- MTA-STS/TLS-RPT para validar transporte.
- MFA resistente a phishing y protección de OAuth consent.
- Bloqueo de auto-forward externo no aprobado.
- Alertas de cambios DNS/MX, reglas inbox y delegación.
- Protección de registrar, lock y contactos de recuperación.

## Metodología
1. Inventariar dominios, subdominios, DNS, MX y proveedores.
2. Consultar registros de forma pasiva y guardar evidencia.
3. Evaluar SPF, DKIM, DMARC, DNSSEC y TLS.
4. Revisar cabeceras de muestras autorizadas y logs de correo.
5. Detectar reglas de forwarding y delegaciones sospechosas.
6. Diseñar rollout de DMARC con monitorización.
7. Probar cambios en dominio de laboratorio antes de producción.
8. Verificar recepción, entrega y reportes tras cambios.

## Laboratorio
Dominio de prueba y MTA local. Generar mensajes sintéticos y validar SPF/DKIM/DMARC; probar DNSSEC en zona de laboratorio. No enviar campañas masivas ni suplantar dominios de terceros.

## Evaluación
Dominios inventariados, autenticación alineada, forwarding controlado y cambios monitorizados.

## Referencias
RFC 7208, RFC 6376, RFC 7489, RFC 8461, RFC 8460, RFC 4033-4035 y NIST email security guidance.

## Instrucciones para agentes IA
No modifiques DNS ni envíes correos sin aprobación. No uses dominios de terceros para pruebas de spoofing; limita el ejercicio a zonas propias.