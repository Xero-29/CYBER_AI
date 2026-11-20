# Investigación técnica: Red Team de IA y agentes

**ID:** ai_red_team · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Red-team de modelos reales pendiente.

## Alcance
Evaluar sistema completo de IA: modelo, prompts, RAG, memoria, agentes, herramientas, conectores, identidad, datos, evaluadores, observabilidad y proveedor. El objetivo es probar límites de seguridad definidos, no maximizar jailbreaks sin control.

## Threat model
Activos: datos, secretos, pesos, prompts privilegiados, herramientas, permisos, coste, decisiones y reputación. Adversarios: usuario, documento indirecto, proveedor comprometido, insider, tenant cruzado y atacante de supply chain. Definir capacidades, acceso, restricciones y objetivos.

## Clases de prueba
Direct/indirect prompt injection, RAG poisoning, data/model poisoning, tool misuse, excessive agency, cross-tenant leakage, secret extraction, insecure output handling, denial of wallet, model extraction, unsafe fallback, memory poisoning, agent loops y evaluator gaming. Variar idioma, encoding, context, multimodal input y ordering.

## Controles
Policy engine externo al modelo, autorización determinista, least privilege, tool isolation, approval gates, typed schemas, provenance, ACL en retrieval, secret canaries, rate limits, budgets, circuit breakers, kill switch, human review y logs con redaction. El modelo no debe decidir sus propios permisos.

## Evaluación
Attack success rate por clase, unauthorized action rate, leakage rate, policy bypass, citation precision, retrieval recall, false refusal, tool correctness, p95 latency, cost per task y recovery. Repetir por modelo/version/config; informar incertidumbre y false positives.

## Laboratorios
RAG corpus sintético con inyección indirecta, tools mock read/write, multi-tenant ACL, canary secrets, tool-output poisoning y agent loop simulator. No introducir secretos reales ni usar datos de terceros.

## Fuentes
- OWASP Top 10 for LLM Applications: https://owasp.org/projects/top-10-for-large-language-model-applications
- OWASP AI Testing Guide: https://owasp.org/www-project-ai-testing-guide/
- MITRE ATLAS: https://atlas.mitre.org/
- NIST AI 100-2 E2025: https://doi.org/10.6028/NIST.AI.100-2e2025
- NIST AI RMF: https://doi.org/10.6028/NIST.AI.100-1

**Límite:** benchmarks y red-team no demuestran seguridad universal; resultados dependen de modelo, versión, prompt y entorno.
