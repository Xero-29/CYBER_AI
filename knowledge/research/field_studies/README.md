# Índice de investigaciones técnicas profundas

**Corte inicial:** 2026-11-18  
**Rama de trabajo:** codex/deep-research-library-2026-11-18  
**Estado:** primera entrega de estudios de campo; no equivale a 48 dominios investigados ni a validación experta.

## Estudios incorporados

| Dominio | Estudio | Alcance de esta entrega |
|---|---|---|
| Redes | [RESEARCH_STUDY](../deep_modules/network/RESEARCH_STUDY.md) | Arquitectura, switching, routing, TCP/UDP, DNS, TLS, VPN, Wi-Fi, amenazas y laboratorios |
| Criptografía | [RESEARCH_STUDY](../deep_modules/crypto/RESEARCH_STUDY.md) | Primitivas, AEAD, PKI, lifecycle de claves, PQC, pruebas y erratas |
| Seguridad de IA | [RESEARCH_STUDY](../deep_modules/ai_security/RESEARCH_STUDY.md) | Prompt injection, RAG, agentes, tool security, poisoning, privacidad y evaluación |
| OT/ICS/SCADA | [RESEARCH_STUDY](../deep_modules/ot_ics/RESEARCH_STUDY.md) | Zonas, protocolos, safety, controles, operación y actualización SP 800-82 Rev. 4 |
| Respuesta a incidentes | [RESEARCH_STUDY](../deep_modules/incident_response/RESEARCH_STUDY.md) | Preparación, detección, contención, forense, recuperación, playbooks y métricas |
| Gestión de vulnerabilidades | [RESEARCH_STUDY](../deep_modules/vuln_management/RESEARCH_STUDY.md) | CVE/CWE/CVSS/EPSS/KEV, matching, priorización y evaluación |
| DevSecOps | [RESEARCH_STUDY](../deep_modules/devsecops/RESEARCH_STUDY.md) | CI/CD, supply chain, SBOM, provenance, firma y pipelines |
| Arquitectura segura | [RESEARCH_STUDY](../deep_modules/secure_arch/RESEARCH_STUDY.md) | Threat modeling, Zero Trust, requisitos y validación |

## Procedencia

- [Registro de fuentes primarias](./SOURCE_REGISTER_2026-11-18.json)
- [Protocolo de investigación](../RESEARCH_PROTOCOL.md)
- [Auditoría global de cobertura](../GLOBAL_COVERAGE_AUDIT.md)
- [Matriz global de requisitos](../global_coverage_matrix.json)

## Reglas editoriales

1. La presencia de un estudio no significa que el dominio esté terminado.
2. El estado de una fuente debe indicar si se inspeccionó su página, abstract o texto completo.
3. Un borrador normativo nunca se etiqueta como final.
4. Cada experimento debe guardar versiones, datos permitidos, configuración, comandos, hashes, resultados y limitaciones.
5. La validación M4/M5 exige literatura trazable, metodología, resultados medidos, amenazas a validez y revisión independiente.
6. No se copiarán estándares protegidos ni contenido de terceros más allá de lo permitido; se producirán síntesis originales y referencias precisas.

## Próxima secuencia de investigación

La siguiente tanda debe cubrir fundamentos, AppSec/API, Windows/AD, Linux, cloud, contenedores/Kubernetes, malware, forense, inteligencia de amenazas, SOC/SIEM, EDR/XDR y threat hunting. Después se abordarán las especialidades sectoriales: móvil, IoT, hardware, telecom/5G, automoción, satélites, OT y seguridad física, junto con las áreas de privacidad, fraude, continuidad, PKI, criptografía poscuántica y matemáticas aplicadas.
