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


## Actualización de taxonomías y evaluación — 2026-11-24

La edición 2026 de OWASP Top 10 for LLM Applications publica una taxonomía distinta a la edición 2025. En la página oficial consultada aparecen, entre otros, Prompt Injection (LLM01:2026), Sensitive Information Disclosure (LLM02:2026), Excessive Agency (LLM03:2026), Supply Chain (LLM04:2026), Data and Model Poisoning (LLM05:2026), Unbounded Consumption (LLM06:2026), Misinformation (LLM07:2026), Hidden Context Exposure (LLM08:2026), Vector and Embedding Weaknesses (LLM09:2026) e Improper Output Handling (LLM10:2026). No reutilizar los números de 2025 como si fueran equivalentes.

OWASP publica además el Top 10 for Agentic Applications 2026 (ASI01–ASI10), con riesgos como goal hijack, tool misuse, identity/privilege abuse, supply chain, memory/context poisoning, inter-agent communication y cascading failures. Debe tratarse como una clasificación diferente, no como renumeración automática del Top 10 de LLM: https://genai.owasp.org/top-10-for-agentic-applications-2026/. MITRE ATLAS sigue siendo una base viva de tácticas y técnicas adversarias; cada evaluación debe fijar fecha o snapshot.

NIST AI 200-3 (ARIA Evaluation Planning Manual, 2026) organiza la evaluación holística alrededor de pruebas de modelo, red teaming y user testing. Esto ayuda a evitar que una prueba aislada de prompt injection se presente como evaluación completa del sistema. NIST AI 600-1 continúa siendo perfil de gestión de riesgo de GenAI, no catálogo de payloads ni garantía de mitigación.

**Implicación para el protocolo:** estratificar resultados por sistema, modelo, versión, tenant, tipo de entrada, herramienta, control y efecto observable. Una negativa textual no equivale a bloqueo si se produjo un efecto externo.

**Estado de evidencia:** se consultaron páginas oficiales de OWASP y NIST para actualizar alcance y taxonomía; esto no acredita lectura integral de todos los documentos ni valida experimentalmente las mitigaciones. Las referencias se mantienen como candidatas hasta que se registre lectura completa, localizador y revisión de cada afirmación.

### Referencias añadidas
- OWASP Top 10 for LLM Applications 2026: https://genai.owasp.org/top-10-for-llm-applications-2026/
- OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10): https://genai.owasp.org/top-10-for-agentic-applications-2026/
- OWASP LLM01:2026 Prompt Injection: https://genai.owasp.org/llm2026/llm012026-prompt-injection/
- OWASP GenAI Red Teaming Guide: https://genai.owasp.org/resource/genai-red-teaming-guide/
- NIST AI 200-3, ARIA Evaluation Planning Manual: https://doi.org/10.6028/NIST.AI.200-3
- NIST AI 600-1, Generative AI Profile: https://doi.org/10.6028/NIST.AI.600-1
