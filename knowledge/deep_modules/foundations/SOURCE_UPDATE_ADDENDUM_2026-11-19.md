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


## Revisión dirigida de NIST SP 800-57 Part 1 Rev. 6 — Initial Public Draft

Se descargó e inspeccionó el PDF oficial completo a nivel de disponibilidad (201 páginas) y se revisaron secciones técnicas seleccionadas; no se declara lectura lineal integral.

Secciones examinadas:
- Sección 4.3.6, cryptoperiod recommendations (pp. 27–39).
- Sección 5.2.3, key metadata (pp. 87–89).
- Sección 6, key states and transitions (pp. 89–96).
- Sección 7, key-management phases and functions (pp. 97–126).
- Sección 7.2.3, key change: re-keying vs key update (pp. 119–120).
- Sección 8.2, inventory management (pp. 129–130).

Hallazgos aplicados:
1. El IPD describe cuatro fases de gestión de claves: pre-operational, operational, post-operational y destroyed. Estas fases no deben confundirse con estados individuales.
2. Los estados de clave incluyen pre-activation, active, suspended, compromised y destroyed; la selección de estados depende del sistema.
3. Las transiciones de estado deben registrarse en logs de auditoría y metadata.
4. El inventario de claves de largo plazo debe contener referencias/punteros al material y metadata (owner/sponsor, tipo, algoritmo, longitud, uso, expiración); no debe copiar secretos o claves privadas salvo que también actúe como repositorio de backup/archivo.
5. Re-keying genera una clave nueva independiente; key update deriva la nueva del valor anterior y puede propagar el compromiso de una clave en la cadena.

El IPD no es final. La Rev. 5 sigue siendo la referencia final registrada hasta que NIST publique una revisión definitiva.

## Actualización de erratas de FIPS 204

La ficha oficial NIST consultada contiene planning note del 31 de julio de 2026 que remite a una hoja de erratas potenciales con varios problemas menores destinados a una futura actualización/revisión. Se registra como aviso oficial de errata; la hoja XLSX no pudo inspeccionarse en esta revisión. No afirmar conformidad algorítmica ni que los problemas estén corregidos.

## Fuentes oficiales nuevas para Identity

NIST SP 800-63-4 Rev. 4 final, publicada el 31 de julio de 2025, reemplaza SP 800-63-3 y cubre identity proofing, enrollment, authenticators, authentication management, federation y assertions. Sus partes SP 800-63B-4 (Authentication and Authenticator Management) y SP 800-63C-4 (Federation and Assertions) son referencias primarias para el tema Identity. Se verificaron metadatos y abstracts oficiales; los requisitos completos de cada parte siguen pendientes de revisión.

Fuentes:
- SP 800-57 Rev. 6 IPD PDF: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r6.ipd.pdf
- FIPS 204 errata notice: https://csrc.nist.gov/pubs/fips/204/final
- SP 800-63-4: https://csrc.nist.gov/pubs/sp/800/63/4/final
- SP 800-63B-4: https://csrc.nist.gov/pubs/sp/800/63/b/4/final
- SP 800-63C-4: https://csrc.nist.gov/pubs/sp/800/63/c/4/final
