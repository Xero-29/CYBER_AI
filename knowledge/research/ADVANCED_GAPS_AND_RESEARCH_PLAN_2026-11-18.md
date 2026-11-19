# Registro de brechas avanzadas de conocimiento — 2026-11-18

**Estado:** 48 dominios contrastados; 192 líneas de investigación avanzada identificadas. Todas permanecen `identified_not_yet_assessed`: no se contabilizan como conocimiento incorporado ni validado.

## Hallazgo de auditoría

El manifiesto y el currículo cubren 48 dominios y siete temas iniciales por área. La matriz global mantiene requisitos temáticos, artefactos y puertas de validación en `not_assessed`. El corpus de estudios aporta síntesis iniciales, pero no demuestra cobertura exhaustiva, lectura integral, laboratorio ejecutado ni revisión independiente.

## Brechas transversales de mayor prioridad

1. **Identidad no humana y cloud-native Zero Trust:** workload identity, SPIFFE/SPIRE, service mesh, CIEM, identidad SaaS y credenciales de corta duración.
2. **Cadena de suministro de software y modelos:** provenance, attestations, SLSA, SBOM/model BOM, runners efímeros, datasets y pesos.
3. **Detección moderna:** ATT&CK Detection Strategies/Analytics, telemetría de calidad, cadenas de eventos, evaluación estadística y drift.
4. **IA agéntica:** autorización externa al modelo, aislamiento de herramientas, memoria/RAG multi-tenant, contaminación y evaluación multimodal.
5. **Cripto-agilidad y PQC:** inventario criptográfico, transición NIST IR 8547, interoperabilidad, medición y retiro de algoritmos heredados.
6. **Resiliencia y recuperación:** clean-room restore, backups verificados, ransomware, dependencia SaaS y recuperación de identidades.
7. **Sistemas ciberfísicos:** safety-security, firmware, radio, cadenas de suministro y acceso remoto de proveedores.
8. **Privacidad y regulación regional:** regulación colombiana y sectorial, PETs, DPIA, borrado verificable y evidencia de cumplimiento.
9. **Investigación reproducible:** revisión sistemática, criterios de inclusión, lectura de texto completo, hipótesis falsables, estadística e incertidumbre.
10. **Gobierno de fuentes:** licencias, versionado, hashes, estado de revisión, claim-to-source y vigilancia de cambios.

## Actualizaciones oficiales contrastadas

- NIST NICE Components 2.2.0: añade el rol de Cybersecurity Supply Chain Risk Management y actualiza competencias de criptografía y DevSecOps. https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220
- MITRE ATT&CK v20.1: historial oficial indica versión vigente desde 13-oct-2026. https://attack.mitre.org/resources/versions/
- ATT&CK v18: reemplazó el enfoque de detecciones aisladas por Detection Strategies/Analytics y deprecó Data Sources. https://attack.mitre.org/resources/updates/updates-october-2025/
- NIST IR 8547 Final: hoja de ruta de transición PQC publicada 27-oct-2026. https://doi.org/10.6028/NIST.IR.8547
- NIST SP 800-207A: identidad de aplicaciones/servicios y políticas Zero Trust cloud-native. https://doi.org/10.6028/NIST.SP.800-207A
- NIST SP 800-218A: perfil SSDF para desarrollo de IA generativa y modelos fundacionales; la página del proyecto NIST indica estado final. https://csrc.nist.gov/Projects/ssdf
- CIS Controls v8.1: 18 controles, salvaguardas priorizadas y grupos de implementación. https://www.cisecurity.org/controls/v8-1
- NIST SP 800-61 Rev. 3: respuesta a incidentes integrada con las seis funciones de CSF 2.0. https://doi.org/10.6028/NIST.SP.800-61r3

## Reglas de incorporación

- Cada brecha debe convertirse en unidades de conocimiento con definición, arquitectura, supuestos, amenaza, controles, fallos, métricas, ejemplos y límites.
- Cada afirmación normativa debe apuntar a una sección concreta de una fuente primaria y registrar versión, fecha de consulta y estado de lectura.
- Una URL HTTPS o un registro de catálogo no constituye evidencia suficiente.
- Los laboratorios deben incluir alcance, precondiciones, datos sintéticos, casos negativos, métricas, limpieza y criterios de parada.
- Mantener separados `catalogued`, `official_page_reviewed`, `metadata_reviewed`, `full_text_reviewed`, `experimentally_validated` e `independently_reproduced`.
- No elevar madurez por volumen de texto.

## Fuente de datos

La lista completa de brechas por dominio está en `ADVANCED_GAP_REGISTER.json`. El registro es un backlog de investigación, no un dataset de entrenamiento ni una afirmación de cobertura lograda.
