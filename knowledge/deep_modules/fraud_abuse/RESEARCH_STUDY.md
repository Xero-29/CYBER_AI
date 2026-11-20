# Investigación técnica: Fraude digital, abuso de negocio y automatización maliciosa

**ID:** fraud_abuse · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de señales reales pendiente.

## Modelo
El fraude explota flujos legítimos: registro, login, recuperación, pagos, promociones, inventario, scraping, referidos, marketplace, soporte y onboarding. Diferenciar abuso de negocio, fraude financiero, abuso de identidad, automatización, insider y vulnerabilidad técnica.

## Taxonomía
Credential stuffing, account takeover, fake account creation, carding, payment fraud, promo abuse, scalping, scraping, denial of inventory, referral abuse, synthetic identity, mule accounts, refund abuse, CAPTCHA defeat, cost inflation, spam y account aggregation. OWASP Automated Threats describe patrones OAT; no todos son vulnerabilidades tradicionales.

## Detección
Combinar señales de sesión, dispositivo, IP/ASN, identidad, velocidad, comportamiento, relación entre cuentas, pago, historial y contexto. Usar grafos, velocity rules, anomaly detection y modelos supervisados con etiquetas confiables. Controlar base rates, drift, adversarial adaptation y fairness. Una IP compartida o VPN no prueba fraude.

## Controles
Rate limits, step-up auth, device binding, risk-based friction, idempotency, payment verification, velocity caps, abuse reporting, manual review y appeal process. Evitar bloqueos opacos; registrar razón y permitir revisión. Minimizar PII y retención.

## Métricas
Fraud loss, false positive/negative, precision/recall, chargeback, conversion impact, review cost, account takeover rate, abuse rate, time to detection y appeal overturn rate.

## Laboratorios
Eventos sintéticos de ecommerce/marketplace con cuentas normales, bots, velocity patterns, synthetic identities y false positives. Evaluar reglas/modelos, adversarial adaptation y fairness. No probar con pagos reales ni datos de clientes.

## Fuentes
- OWASP Automated Threats to Web Applications: https://owasp.org/www-project-automated-threats-to-web-applications/
- MITRE CAPEC: https://capec.mitre.org/data/
- OWASP API Security Top 10: https://api-security.owasp.org/
- NIST AI RMF: https://doi.org/10.6028/NIST.AI.100-1

**Límite:** regulación financiera y privacidad varían por país; revisar fraude sectorial y obligaciones legales.
