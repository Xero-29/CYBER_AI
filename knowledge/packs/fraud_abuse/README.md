# Fraude, abuso y confianza de plataforma — Guía de dominio

**ID:** `fraud_abuse` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Detecta y reduce abuso de cuentas, pagos, promociones, marketplaces, APIs y plataformas digitales. Los controles deben equilibrar seguridad, privacidad, experiencia y falsos positivos. Las decisiones automatizadas requieren explicación, revisión y mecanismos de apelación.

## Tipologías
Account takeover, credential stuffing, bots, abuso de promociones, fraude de pago, chargeback, mule accounts, scraping, spam, fake reviews, abuso de referidos, enumeración y manipulación de métricas. Distinguir abuso confirmado, señal débil y comportamiento legítimo de alto volumen.

## Competencias
- Diseñar señales de riesgo por cuenta, dispositivo, sesión y transacción.
- Correlacionar eventos con minimización de datos.
- Construir reglas y modelos calibrados con clases desbalanceadas.
- Medir precision/recall, tasa de bloqueo, apelaciones y daño colateral.
- Diseñar step-up authentication y límites adaptativos.
- Gestionar investigación, evidencia, privacidad y escalamiento.
- Detectar evasión y adaptación de adversarios.

## Controles
- MFA y protección de recuperación de cuenta.
- Rate limits y cuotas por identidad, dispositivo y acción.
- Detección de anomalías con umbrales y revisión humana.
- Verificación escalonada según riesgo, no bloqueo indiscriminado.
- Protección de pagos con controles del proveedor y señales contextuales.
- Telemetría minimizada, pseudonimizada y con retención definida.
- Registro de decisiones y apelaciones.
- Separación entre señales, decisión automatizada y revisión humana.

## Metodología
1. Definir abuso, daño, población y métricas.
2. Crear taxonomía y etiquetado con procedencia.
3. Construir baseline y medir tasa base.
4. Diseñar reglas/modelos y calibrar umbrales.
5. Simular ataques con cuentas sintéticas.
6. Medir falsos positivos por segmento y posibles sesgos.
7. Desplegar en shadow mode y revisar impacto.
8. Introducir step-up/bloqueos graduales con rollback.
9. Revisar drift y apelaciones.

## Laboratorio
Dataset sintético de sesiones y transacciones. Comparar reglas y un modelo simple con clases desbalanceadas; medir precision, recall, FPR y coste de falsos positivos.

## Evaluación
Decisiones explicables, falsos positivos medidos, apelaciones operativas y privacidad proporcional.

## Referencias
NIST AI RMF, OWASP Automated Threats, FATF guidance cuando aplique, PCI DSS y literatura de fraud analytics.

## Instrucciones para agentes IA
No etiquetes personas como fraudulentas por una sola señal. Expón incertidumbre y evita inferir atributos sensibles. Las acciones sobre cuentas o pagos requieren autoridad humana.