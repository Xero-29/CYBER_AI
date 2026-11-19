# Actualización de fuentes y control de vigencia — Foundations

**Corte:** 2026-11-19. Este addendum amplía `SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md`; no afirma lectura completa de documentos cuyo texto íntegro no fue inspeccionado.

## SP 800-57 Part 1 Rev. 6 — IPD
NIST publicó el Initial Public Draft el 5 de diciembre de 2025. El periodo de comentarios cerró el 5 de febrero de 2026 y NIST publicó los comentarios recibidos. El documento es un borrador inicial, no una publicación final. El registro mantiene Rev. 5 como publicación final y Rev. 6 IPD como material de evolución. Los cambios propuestos incluyen Ascon, FIPS 203/204/205 y tratamiento separado de claves para establecimiento y almacenamiento. No migrar requisitos operativos a partir del IPD sin comparar la versión final cuando exista.

## FIPS 203 — aviso de errata
La ficha oficial mantiene nota de planificación fechada 17 de noviembre de 2025: NIST identificó un problema que corregirá en una futura actualización/revisión y publica hoja de erratas potenciales. El estado registrado es aviso oficial revisado; el contenido de la hoja de cálculo y el texto algorítmico íntegro siguen pendientes. No presentar conformidad de implementación basándose únicamente en la ficha.

## SP 800-53 Release 5.2.0
La publicación y el resumen oficial de cambios se inspeccionaron. Cambios destacados incluyen SA-24 (Design for Cyber Resiliency), SA-15(13) (Logging Syntax), SI-02(07) (Root Cause Analysis) y revisión de SI-07(12). El catálogo completo y las correspondientes guías de evaluación no se leyeron integralmente. El registro conserva este límite.

## OWASP ASVS 5.0.0
El portal oficial identifica la versión 5.0.0 como estable y publicada el 30 de mayo de 2025; ofrece PDF, DOCX y CSV. Esto valida versión y alcance del estándar, no revisión de cada requisito.

## MITRE ATT&CK v20.1
El historial oficial identifica v20.1 como versión vigente desde el 13 de octubre de 2026. Se revisaron las release notes de octubre 2026 y el historial de versiones. El catálogo STIX completo no se inspeccionó objeto por objeto. ATT&CK no es modelo probabilístico ni prueba de aplicabilidad de técnicas.

| Fuente | Evidencia revisada | No revisado / límite |
|---|---|---|
| SP 800-57 Rev. 5 / Rev. 6 IPD | Metadatos, abstract, propuesta de cambios y estado del comentario público | Texto completo y futura revisión final |
| FIPS 203 | Ficha oficial y aviso de errata potencial | PDF completo y hoja de cálculo de erratas |
| SP 800-53 5.2.0 | Anuncio y resumen de cambios oficiales | Catálogo completo y evaluación 800-53A completa |
| OWASP ASVS 5.0.0 | Portal, versión estable, fecha y formatos | CSV/PDF requisito por requisito |
| ATT&CK v20.1 | Version history y release notes de octubre 2026 | Objetos STIX y relevancia por entorno |

Fuentes oficiales:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd
- https://csrc.nist.gov/files/pubs/sp/800/57/pt1/r6/ipd/docs/sp800-57pt1r6-ipd-comments-received.pdf
- https://csrc.nist.gov/pubs/fips/203/final
- https://csrc.nist.gov/news/2025/nist-releases-revision-to-sp-800-53-controls
- https://csrc.nist.gov/csrc/media/Projects/risk-management/800-53%20Comment%20Site/SP800-53-r5.2.0-changes.pdf
- https://asvs.owasp.org/
- https://attack.mitre.org/resources/versions/
- https://attack.mitre.org/resources/updates/updates-october-2026/
