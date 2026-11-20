# Investigación técnica: PKI, certificados, HSM y módulos criptográficos

**ID:** pki_hsm · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de HSM/CA pendiente.

## Arquitectura PKI
Modelar Root CA, issuing CA, RA, OCSP/CRL, CT logs donde aplique, trust stores, certificate profiles, enrollment, renewal, revocation y relying parties. Definir trust anchors, path validation, name constraints, EKU/KU, SAN, policies, algorithm constraints, key usage y lifecycle.

## Gestión
Separar generación, custodia, backup, activation, rotation, revocation y destruction. HSM/KMS debe tener roles, dual control, quorum, audit logs, tamper resistance y disaster recovery. Una CA offline reduce exposición, pero aumenta complejidad de operación y recuperación.

## FIPS 140-3
FIPS 140-3 define requisitos para módulos criptográficos y niveles cualitativos; validar el certificado exacto del módulo, versión, firmware, operating environment, approved mode y security policy. Usar una librería con algoritmo aprobado no implica que el producto completo esté validado.

## Riesgos
CA compromise, weak issuance, misissued cert, private key export, weak entropy, stale trust, revocation latency, algorithm deprecation, certificate transparency gap, HSM misconfiguration, backup compromise y vendor lifecycle. Firmas de software requieren identidad de builder, provenance y verificación en despliegue.

## Laboratorios
Mini-PKI, issuance/renewal/revocation, expired/wrong SAN/wrong EKU, key rollover, OCSP/CRL unavailable, HSM simulator y disaster recovery. Medir issuance, revocation propagation, validation failures, key recovery y audit integrity.

## Fuentes
- NIST SP 800-57 Part 1 Rev. 5: https://doi.org/10.6028/NIST.SP.800-57pt1r5
- NIST FIPS 140-3: https://doi.org/10.6028/NIST.FIPS.140-3
- NIST CMVP: https://csrc.nist.gov/projects/cryptographic-module-validation-program
- IETF RFC 5280: https://www.rfc-editor.org/rfc/rfc5280.html

**Límite:** revisar política CA, perfil, validación de módulo y jurisdicción; no declarar FIPS validated sin certificado aplicable.
