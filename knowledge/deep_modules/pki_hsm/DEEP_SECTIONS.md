# Secciones de profundización — PKI y HSM

## Modelo de amenazas
Modelar raíz, CA subordinadas, RA, HSM, operadores, trust stores, emisión, revocación, backup, firmware y aplicaciones consumidoras. Amenazas: compromiso de CA, ceremonia defectuosa, exportación de clave, abuso de rol, certificado mal emitido, revocación no propagada y supply chain del HSM. Incluir custodia y continuidad.

## Detección
Auditar generación, importación, uso, backup, exportación, cambios de política, emisión, renovación y revocación. Detectar operaciones fuera de quorum, certificados anómalos, claves fuera de propósito y cambios en trust anchors. Correlacionar key ID, operador, rol, sesión y aprobación sin exponer material privado.

## Respuesta a incidentes
Ante compromiso de CA/HSM, detener emisión, preservar audit logs y estado, activar plan de revocación y distribución de nuevas trust anchors. Identificar certificados derivados, consumidores y ventanas de exposición. Restaurar desde backup validado y realizar ceremonia de recuperación documentada; comprobar que la revocación llega a todos los verificadores.

## Casos prácticos
En PKI offline de laboratorio, emitir certificado con SAN incorrecto y probar rechazo; simular compromiso de clave de CA de prueba, revocar certificados subordinados y emitir nueva cadena. Medir propagación de CRL/OCSP y continuidad de servicios.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-57, FIPS 140-3, RFC 5280 y documentación de HSM. Fijar nivel FIPS y certificado del módulo concreto.
