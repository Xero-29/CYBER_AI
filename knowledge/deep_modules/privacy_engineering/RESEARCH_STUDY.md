# Investigación técnica: Ingeniería de privacidad

**ID:** privacy_engineering · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Evaluación legal y de impacto pendiente.

## Principios
Privacy engineering incorpora privacidad desde requisitos y arquitectura: propósito, minimización, transparencia, control individual, seguridad, retención, exactitud y responsabilidad. Identificar sujetos, datos, finalidad, base jurídica, destinatarios, transferencias, procesadores, sistemas y riesgos de reidentificación.

## Modelado
Data flow mapping, privacy threat modeling, LINDDUN, DPIA/PIA, records of processing, data lineage, retention mapping y third-party assessment. Evaluar collection, use, sharing, inference, linkage, re-identification, surveillance, exclusion y breach.

## Técnicas
Pseudonymization, tokenization, encryption, access control, minimization, aggregation, synthetic data, differential privacy, federated learning y secure multiparty computation. Cada técnica tiene supuestos, trade-offs y parámetros; pseudonimizar no es anonimizar. Differential privacy requiere definir adjacency, epsilon/delta, composition, utility y threat model.

## Ciclo de vida y derechos
Diseñar acceso, rectificación, portabilidad, borrado, oposición y retención según jurisdicción. Borrado debe contemplar replicas, caches, backups, logs, data lakes y embeddings; documentar límites técnicos y legales. Privacy by design debe incluir pruebas y evidencia, no solo aviso de privacidad.

## Métricas
Data minimization, records coverage, retention violations, subject request SLA, reidentification risk, privacy incidents, access violations y utility/privacy trade-off.

## Laboratorios
Dataset sintético, pseudonymization, k-anonymity/differential privacy demonstration, linkage attacks, data deletion across replicas, ACL retrieval multi-tenant y log redaction.

## Fuentes
- NIST Privacy Framework: https://www.nist.gov/privacy-framework
- NIST AI RMF: https://doi.org/10.6028/NIST.AI.100-1
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-63-4: https://doi.org/10.6028/NIST.SP.800-63-4

**Límite:** la ingeniería no determina por sí sola la base jurídica; requiere asesoría legal local y revisión sectorial.
