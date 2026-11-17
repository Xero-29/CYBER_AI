# Biblioteca de módulos de profundización

Esta colección transforma los 48 currículos de dominio en módulos editoriales con ruta técnica, procedimiento, laboratorio, evaluación y control de procedencia.

## Investigación nivel L4/L5

Cada especialidad dispone de una agenda de investigación en `./<area>/RESEARCH_AGENDA.md`. Siete dominios prioritarios cuentan además con una revisión bibliográfica inicial `LITERATURE_REVIEW.md`, vinculada por ID al registro de fuentes. Las revisiones son exploratorias y no representan revisiones sistemáticas completas ni experimentos ejecutados.

- Método obligatorio: `../research/RESEARCH_PROTOCOL.md`.
- Registro inicial de fuentes oficiales: `../research/source_registry.json`.
- Auditoría estructural y de trazabilidad: `python knowledge_research_audit.py` o `python knowledge_research_audit.py --json`.
- Revisiones iniciales: [AppSec/API](./appsec/LITERATURE_REVIEW.md), [respuesta a incidentes](./incident_response/LITERATURE_REVIEW.md), [DevSecOps](./devsecops/LITERATURE_REVIEW.md), [gestión de vulnerabilidades](./vuln_management/LITERATURE_REVIEW.md), [OT/ICS](./ot_ics/LITERATURE_REVIEW.md), [arquitectura segura](./secure_arch/LITERATURE_REVIEW.md) y [criptografía](./crypto/LITERATURE_REVIEW.md).

## Estado y uso

- Un módulo por cada área declarada en `knowledge/packs/manifest.json`.
- Los módulos son borradores estructurados para completar con teoría técnica específica, diagramas, casos, fuentes primarias verificadas y laboratorios reproducibles.
- El estado `draft_structured_not_expert_validated` es deliberado: no confundir una guía de desarrollo con conocimiento experto ya validado.
- No se deben marcar fuentes como verificadas hasta comprobar URL canónica, editor, versión, vigencia, licencia, integridad y correspondencia temática.
- Las pruebas activas requieren autorización expresa, alcance, límites de impacto y criterio de parada.

## Secuencia editorial obligatoria

1. Redactar contenido técnico original para cada tema y nivel L0–L4.
2. Añadir arquitectura, diagramas, modelos de amenaza, tablas y ejemplos.
3. Incorporar referencias primarias verificadas y atribución/licencia.
4. Crear laboratorios reproducibles con datos sintéticos y resultados esperados.
5. Añadir casos de estudio, ejercicios y rúbricas con respuestas razonadas.
6. Revisar técnicamente, comprobar vigencia y ejecutar pruebas de reproducibilidad.
7. Registrar revisión, autoría, cambios y madurez demostrada.

## Índice

- [Fundamentos](./foundations/README.md) — `foundations` · [Agenda de investigación](./foundations/RESEARCH_AGENDA.md)
- [Seguridad web y aplicaciones](./appsec/README.md) — `appsec` · [Agenda de investigación](./appsec/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./appsec/LITERATURE_REVIEW.md)
- [Seguridad de API](./api/README.md) — `api` · [Agenda de investigación](./api/RESEARCH_AGENDA.md)
- [Redes](./network/README.md) — `network` · [Agenda de investigación](./network/RESEARCH_AGENDA.md)
- [Linux y Unix](./linux/README.md) — `linux` · [Agenda de investigación](./linux/RESEARCH_AGENDA.md)
- [Windows y Active Directory](./windows_ad/README.md) — `windows_ad` · [Agenda de investigación](./windows_ad/RESEARCH_AGENDA.md)
- [Seguridad cloud](./cloud/README.md) — `cloud` · [Agenda de investigación](./cloud/RESEARCH_AGENDA.md)
- [Contenedores y Kubernetes](./containers/README.md) — `containers` · [Agenda de investigación](./containers/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./containers/LITERATURE_REVIEW.md)
- [Seguridad móvil](./mobile/README.md) — `mobile` · [Agenda de investigación](./mobile/RESEARCH_AGENDA.md)
- [Criptografía](./crypto/README.md) — `crypto` · [Agenda de investigación](./crypto/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./crypto/LITERATURE_REVIEW.md)
- [Identidad y acceso](./identity/README.md) — `identity` · [Agenda de investigación](./identity/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./identity/LITERATURE_REVIEW.md)
- [Análisis de malware](./malware/README.md) — `malware` · [Agenda de investigación](./malware/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./malware/LITERATURE_REVIEW.md)
- [Forense digital](./forensics/README.md) — `forensics` · [Agenda de investigación](./forensics/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./forensics/LITERATURE_REVIEW.md)
- [Respuesta a incidentes](./incident_response/README.md) — `incident_response` · [Agenda de investigación](./incident_response/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./incident_response/LITERATURE_REVIEW.md)
- [Inteligencia de amenazas](./threat_intel/README.md) — `threat_intel` · [Agenda de investigación](./threat_intel/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./threat_intel/LITERATURE_REVIEW.md)
- [Ingeniería inversa](./reverse/README.md) — `reverse` · [Agenda de investigación](./reverse/RESEARCH_AGENDA.md)
- [IoT y hardware](./iot_hardware/README.md) — `iot_hardware` · [Agenda de investigación](./iot_hardware/RESEARCH_AGENDA.md)
- [DevSecOps y supply chain](./devsecops/README.md) — `devsecops` · [Agenda de investigación](./devsecops/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./devsecops/LITERATURE_REVIEW.md)
- [Seguridad de IA](./ai_security/README.md) — `ai_security` · [Agenda de investigación](./ai_security/RESEARCH_AGENDA.md)
- [GRC, privacidad y auditoría](./governance/README.md) — `governance` · [Agenda de investigación](./governance/RESEARCH_AGENDA.md)
- [Gestión de vulnerabilidades](./vuln_management/README.md) — `vuln_management` · [Agenda de investigación](./vuln_management/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./vuln_management/LITERATURE_REVIEW.md)
- [Bug bounty autorizado](./bug_bounty/README.md) — `bug_bounty` · [Agenda de investigación](./bug_bounty/RESEARCH_AGENDA.md)
- [Arquitectura segura](./secure_arch/README.md) — `secure_arch` · [Agenda de investigación](./secure_arch/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./secure_arch/LITERATURE_REVIEW.md)
- [Seguridad de datos](./data_security/README.md) — `data_security` · [Agenda de investigación](./data_security/RESEARCH_AGENDA.md)
- [Ingeniería de software y calidad](./software_engineering/README.md) — `software_engineering` · [Agenda de investigación](./software_engineering/RESEARCH_AGENDA.md)
- [Aprendizaje automático e ingeniería de IA](./machine_learning/README.md) — `machine_learning` · [Agenda de investigación](./machine_learning/RESEARCH_AGENDA.md)
- [Hardware, firmware y sistemas embebidos](./hardware_security/README.md) — `hardware_security` · [Agenda de investigación](./hardware_security/RESEARCH_AGENDA.md)
- [Matemáticas, estadística y métodos numéricos](./mathematics/README.md) — `mathematics` · [Agenda de investigación](./mathematics/RESEARCH_AGENDA.md)
- [SOC, SIEM y SOAR](./soc_siem/README.md) — `soc_siem` · [Agenda de investigación](./soc_siem/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./soc_siem/LITERATURE_REVIEW.md)
- [EDR, XDR y endpoints](./edr_xdr/README.md) — `edr_xdr` · [Agenda de investigación](./edr_xdr/RESEARCH_AGENDA.md)
- [Threat hunting](./threat_hunting/README.md) — `threat_hunting` · [Agenda de investigación](./threat_hunting/RESEARCH_AGENDA.md)
- [Red Team autorizado](./red_team/README.md) — `red_team` · [Agenda de investigación](./red_team/RESEARCH_AGENDA.md)
- [Wireless, Bluetooth y NFC](./wireless_security/README.md) — `wireless_security` · [Agenda de investigación](./wireless_security/RESEARCH_AGENDA.md)
- [OT, ICS y SCADA](./ot_ics/README.md) — `ot_ics` · [Agenda de investigación](./ot_ics/RESEARCH_AGENDA.md) · [Revisión bibliográfica](./ot_ics/LITERATURE_REVIEW.md)
- [Telecomunicaciones y 5G](./telecom_5g/README.md) — `telecom_5g` · [Agenda de investigación](./telecom_5g/RESEARCH_AGENDA.md)
- [Ciberseguridad automotriz y CAN](./automotive_security/README.md) — `automotive_security` · [Agenda de investigación](./automotive_security/RESEARCH_AGENDA.md)
- [Satélites y sistemas espaciales](./satellite_security/README.md) — `satellite_security` · [Agenda de investigación](./satellite_security/RESEARCH_AGENDA.md)
- [Seguridad física ciberfísica](./physical_security/README.md) — `physical_security` · [Agenda de investigación](./physical_security/RESEARCH_AGENDA.md)
- [Correo, DNS y dominios](./email_dns_security/README.md) — `email_dns_security` · [Agenda de investigación](./email_dns_security/RESEARCH_AGENDA.md)
- [Fraude digital y abuso](./fraud_abuse/README.md) — `fraud_abuse` · [Agenda de investigación](./fraud_abuse/RESEARCH_AGENDA.md)
- [Ingeniería de privacidad](./privacy_engineering/README.md) — `privacy_engineering` · [Agenda de investigación](./privacy_engineering/RESEARCH_AGENDA.md)
- [Forense cloud](./cloud_forensics/README.md) — `cloud_forensics` · [Agenda de investigación](./cloud_forensics/RESEARCH_AGENDA.md)
- [Red teaming de IA y agentes](./ai_red_team/README.md) — `ai_red_team` · [Agenda de investigación](./ai_red_team/RESEARCH_AGENDA.md)
- [PKI, certificados y HSM](./pki_hsm/README.md) — `pki_hsm` · [Agenda de investigación](./pki_hsm/RESEARCH_AGENDA.md)
- [Criptografía poscuántica](./post_quantum_crypto/README.md) — `post_quantum_crypto` · [Agenda de investigación](./post_quantum_crypto/RESEARCH_AGENDA.md)
- [Continuidad y recuperación](./business_continuity/README.md) — `business_continuity` · [Agenda de investigación](./business_continuity/RESEARCH_AGENDA.md)
- [Seguridad de bases de datos](./database_security/README.md) — `database_security` · [Agenda de investigación](./database_security/RESEARCH_AGENDA.md)
- [Investigación de vulnerabilidades](./vulnerability_research/README.md) — `vulnerability_research` · [Agenda de investigación](./vulnerability_research/RESEARCH_AGENDA.md)
