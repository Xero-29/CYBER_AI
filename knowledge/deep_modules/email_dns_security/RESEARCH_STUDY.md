# Investigación técnica: Seguridad de correo, DNS y dominios

**ID:** email_dns_security · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de dominios y flujo real pendiente.

## Correo
Modelar DNS, MX, MTA, MUA, relay, gateway, SaaS, identidad, mailing lists, forwarding, archiving y third-party senders. Revisar SMTP, submission, TLS, authentication, message headers, MIME, attachments, URL rewriting, sandboxing y mail routing.

## Autenticación de dominio
SPF autoriza hosts para identidades MAIL FROM/HELO; controlar lookup limits, include chains, forwarding y alignment. DKIM firma partes del mensaje y requiere rotación de claves, selector y canonicalization. DMARC alinea SPF/DKIM con RFC5322.From y define policy/reporting.

**Cambio de estándar importante:** RFC 7489 (DMARC original) aparece obsoleto y sustituido por RFC 9989, 9990 y 9991; no usar RFC 7489 como única referencia vigente. SPF RFC 7208 y DKIM RFC 6376 también tienen actualizaciones; revisar RFC asociadas antes de generar políticas.

## DNS
Revisar authoritative/recursive split, DNSSEC, registrar/registrant, registrar lock, zone transfers, CAA, TTL, NS delegation, dynamic DNS, subdomain takeover, dangling records, DoH/DoT, resolver logging y cache. DNSSEC autentica datos DNS, no cifra consultas ni protege aplicaciones por sí solo.

## Amenazas
Domain spoofing, BEC, phishing, lookalike domains, compromised mailbox, OAuth app consent, malicious forwarding, SPF softfail/misconfiguration, DKIM key leakage, DMARC none forever, DNS hijack, subdomain takeover, tunneling y malicious attachments.

## Controles y evaluación
MFA resistente al phishing, DMARC gradual a enforcement, SPF/DKIM alignment, TLS, MTA-STS/TLS-RPT, DNSSEC donde aplique, registrar lock, least privilege en mail admin, OAuth app governance, mailbox audit, anti-phishing, sandbox y backup. Probar correo legítimo de proveedores, forwarding, mailing lists y terceros para evitar bloquear flujos legítimos.

## Laboratorios
Dominio de prueba, DNS zone sintética, SPF/DKIM/DMARC, SMTP sink, phishing simulation sin usuarios reales, malicious attachment benigno y subdomain inventory. Medir authentication pass/alignment, delivery, false positive y tiempo de revocación.

## Fuentes
- RFC 7208 SPF: https://www.rfc-editor.org/rfc/rfc7208.html
- RFC 6376 DKIM: https://www.rfc-editor.org/rfc/rfc6376.html
- RFC 9989 DMARC: https://www.rfc-editor.org/rfc/rfc9989.html
- RFC 9990 Aggregate Reporting: https://www.rfc-editor.org/rfc/rfc9990.html
- RFC 9991 Failure Reporting: https://www.rfc-editor.org/rfc/rfc9991.html
- NIST SP 800-81 (DNS deployment guidance): https://csrc.nist.gov/

**Límite:** revisar actualizaciones y erratas RFC, proveedor de correo y arquitectura antes de modificar registros DNS.
