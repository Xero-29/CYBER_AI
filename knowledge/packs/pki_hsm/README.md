# PKI, certificados y HSM — Guía de dominio

**ID:** `pki_hsm` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y alcance
Diseña y opera confianza criptográfica: autoridades certificadoras, registro, emisión, validación, revocación, claves y módulos hardware. Una PKI es un sistema de gobierno y operación, no solo una CA. Las claves raíz requieren protección y procedimientos independientes.

## Componentes y amenazas
Inventariar Root CA, Issuing CA, RA, OCSP, CRL, repositorios, HSM, KMS, certificados TLS/code signing/client auth, perfiles, plantillas, algoritmos, custodios y dependencias. Riesgos: emisión indebida, clave CA expuesta, plantillas permisivas, expiración masiva, revocación no propagada, algoritmos obsoletos, backup de claves débil y falta de ceremonia de recuperación.

## Competencias
- Definir CP/CPS, políticas de emisión y separación de funciones.
- Diseñar jerarquía offline root y CA emisoras.
- Gestionar CSR, SAN, EKU, constraints, path validation y revocación.
- Operar HSM: particiones, roles, quorum, backup y firmware.
- Proteger code signing y claves de firmware.
- Automatizar ACME con políticas de identidad y límites.
- Planificar rotación, renovación, expiración y recuperación.

## Controles
- Root CA offline y activación mediante ceremonia documentada.
- HSM validado para el nivel de riesgo; M-of-N para operaciones críticas.
- Claves privadas no exportables cuando sea posible.
- Perfiles estrictos y validación de identidad antes de emitir.
- Separar roles de operador, auditor, custodio y aprobador.
- CRL/OCSP monitorizados y pruebas de revocación.
- Inventario de certificados con propietario, uso y vencimiento.
- Algoritmos y tamaños aprobados; plan de criptoagilidad.
- Backups cifrados y recuperación ensayada en entorno controlado.

## Metodología
1. Inventariar autoridades, claves, certificados, HSM y custodios.
2. Revisar CP/CPS, perfiles, plantillas y delegaciones.
3. Validar emisión, cadena, SAN, EKU, expiración y revocación.
4. Revisar ceremonias, quorum, logs y control físico.
5. Probar renovación y revocación con certificados de laboratorio.
6. Ensayar pérdida de CA emisora y restauración desde backup.
7. Medir certificados huérfanos, expirados y algoritmos heredados.
8. Aprobar cambios y registrar cadena de custodia de claves.

## Laboratorio
PKI local con OpenSSL/step-ca, CA raíz offline y CA intermedia de prueba. Emitir certificado TLS, validar cadena, revocar y verificar CRL/OCSP. No importar claves productivas ni utilizar HSM real para pruebas no aprobadas.

## Evaluación
Claves con custodios y protección, emisión restringida, revocación operativa, inventario actualizado y recuperación probada.

## Referencias
NIST SP 800-57, RFC 5280, RFC 6960, CA/Browser Forum Baseline Requirements, FIPS 140-3 y ETSI EN 319 401.

## Instrucciones IA
No pidas claves privadas ni PIN de HSM. No generes ni firmes certificados productivos. Toda ceremonia requiere operador humano, quorum y evidencia independiente.