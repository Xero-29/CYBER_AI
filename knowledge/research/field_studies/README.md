# Índice de investigaciones técnicas profundas

**Corte inicial:** 2026-11-18  
**Rama de trabajo:** codex/deep-research-library-2026-11-18  
**Estado:** primera entrega de estudios de campo; no equivale a 48 dominios investigados ni a validación experta.

## Estudios incorporados

| Dominio | Estudio | Alcance de esta entrega |
|---|---|---|
| Redes | [RESEARCH_STUDY](../../deep_modules/network/RESEARCH_STUDY.md) | Arquitectura, switching, routing, TCP/UDP, DNS, TLS, VPN, Wi-Fi, amenazas y laboratorios |
| Criptografía | [RESEARCH_STUDY](../../deep_modules/crypto/RESEARCH_STUDY.md) | Primitivas, AEAD, PKI, lifecycle de claves, PQC, pruebas y erratas |
| Seguridad de IA | [RESEARCH_STUDY](../../deep_modules/ai_security/RESEARCH_STUDY.md) | Prompt injection, RAG, agentes, tool security, poisoning, privacidad y evaluación |
| OT/ICS/SCADA | [RESEARCH_STUDY](../../deep_modules/ot_ics/RESEARCH_STUDY.md) | Zonas, protocolos, safety, controles, operación y actualización SP 800-82 Rev. 4 |
| Respuesta a incidentes | [RESEARCH_STUDY](../../deep_modules/incident_response/RESEARCH_STUDY.md) | Preparación, detección, contención, forense, recuperación, playbooks y métricas |
| Gestión de vulnerabilidades | [RESEARCH_STUDY](../../deep_modules/vuln_management/RESEARCH_STUDY.md) | CVE/CWE/CVSS/EPSS/KEV, matching, priorización y evaluación |
| DevSecOps | [RESEARCH_STUDY](../../deep_modules/devsecops/RESEARCH_STUDY.md) | CI/CD, supply chain, SBOM, provenance, firma y pipelines |
| Arquitectura segura | [RESEARCH_STUDY](../../deep_modules/secure_arch/RESEARCH_STUDY.md) | Threat modeling, Zero Trust, requisitos y validación |

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


## Segunda entrega de estudios profundos (2026-11-18)

Se incorporaron ocho dominios adicionales:
- [Fundamentos](../../deep_modules/foundations/RESEARCH_STUDY.md)
- [Seguridad web y aplicaciones](../../deep_modules/appsec/RESEARCH_STUDY.md)
- [Seguridad de API](../../deep_modules/api/RESEARCH_STUDY.md)
- [Linux y Unix](../../deep_modules/linux/RESEARCH_STUDY.md)
- [Windows y Active Directory](../../deep_modules/windows_ad/RESEARCH_STUDY.md)
- [Seguridad cloud](../../deep_modules/cloud/RESEARCH_STUDY.md)
- [Contenedores y Kubernetes](../../deep_modules/containers/RESEARCH_STUDY.md)
- [Seguridad móvil](../../deep_modules/mobile/RESEARCH_STUDY.md)

Las referencias de esta tanda distinguen ASVS 5.0.0 estable de WSTG 4.2 estable/WSTG 5.0 en desarrollo, y fijan fuentes oficiales por plataforma. La existencia del estudio no demuestra que se hayan probado todos los controles en sistemas reales.


## Tercera entrega de estudios profundos (2026-11-18)

Se incorporaron ocho dominios adicionales:
- [Identidad y acceso](../../deep_modules/identity/RESEARCH_STUDY.md)
- [Análisis de malware](../../deep_modules/malware/RESEARCH_STUDY.md)
- [Forense digital](../../deep_modules/forensics/RESEARCH_STUDY.md)
- [Inteligencia de amenazas](../../deep_modules/threat_intel/RESEARCH_STUDY.md)
- [Ingeniería inversa](../../deep_modules/reverse/RESEARCH_STUDY.md)
- [IoT y hardware](../../deep_modules/iot_hardware/RESEARCH_STUDY.md)
- [Gobernanza, riesgo y auditoría](../../deep_modules/governance/RESEARCH_STUDY.md)
- [Seguridad de datos](../../deep_modules/data_security/RESEARCH_STUDY.md)

Se incorporan referencias NIST SP 800-63-4, NISTIR 8259A/B/Rev.1, SP 800-193, SP 800-86 y marco de privacidad, manteniendo visibles las fechas y antigüedad de las guías.


## Cuarta entrega de estudios profundos (2026-11-18)

Se incorporaron ocho dominios:
- [Aprendizaje automático e ingeniería de IA](../../deep_modules/machine_learning/RESEARCH_STUDY.md)
- [Matemáticas y métodos cuantitativos](../../deep_modules/mathematics/RESEARCH_STUDY.md)
- [Ingeniería de software y calidad](../../deep_modules/software_engineering/RESEARCH_STUDY.md)
- [SOC, SIEM y SOAR](../../deep_modules/soc_siem/RESEARCH_STUDY.md)
- [EDR/XDR y endpoints](../../deep_modules/edr_xdr/RESEARCH_STUDY.md)
- [Threat hunting](../../deep_modules/threat_hunting/RESEARCH_STUDY.md)
- [Red Team autorizado](../../deep_modules/red_team/RESEARCH_STUDY.md)
- [Wireless, Bluetooth y NFC](../../deep_modules/wireless_security/RESEARCH_STUDY.md)

La biblioteca incorpora NIST AI 100-2 E2025 (actualiza E2023), y registra límites de antigüedad de NIST SP 800-94/115/137. Se documentan MITRE CAPEC/D3FEND, Sigma, Zeek, Suricata y especificaciones inalámbricas como referencias que requieren fijar versión.
