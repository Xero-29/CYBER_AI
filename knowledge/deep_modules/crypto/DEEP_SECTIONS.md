# Secciones de profundización — Criptografía

## Modelo de amenazas
Definir adversario, capacidades, endpoints, claves, protocolos, horizonte de confidencialidad y propiedades requeridas. Amenazas: nonce repetido, entropía débil, downgrade, replay, validación incorrecta de certificados, side channels, exposición de claves, errores de composición y fallos de ciclo de vida. Distinguir seguridad del algoritmo, protocolo, implementación y operación; no inferir garantías desde un benchmark.

## Detección
Auditar inventario criptográfico, algoritmos y parámetros negociados, expiración/revocación de certificados, fallos de validación, usos anómalos de claves y eventos de KMS/HSM. Detectar suites obsoletas, downgrade, repetición, errores de aleatoriedad y uso de claves fuera de propósito. Los logs deben identificar key ID y operación sin revelar material secreto.

## Respuesta a incidentes
Ante sospecha de compromiso, identificar claves y datos afectados, limitar uso, revocar certificados/tokens, rotar claves por dependencia, re-envolver datos cuando corresponda y preservar auditoría HSM/KMS. Evaluar si hay datos históricos expuestos y si la clave antigua sigue siendo necesaria para recuperación. Evitar rotaciones simultáneas no coordinadas que provoquen pérdida de acceso.

## Casos prácticos
Construir laboratorio AEAD y mini-PKI: probar nonce duplicado, tag alterado, SAN incorrecto, certificado expirado y revocación. Medir resultados con vectores oficiales; ensayar rotación de clave de envoltura y recuperación de backup. Para transición poscuántica, comparar interoperabilidad y coste de implementaciones estandarizadas sin inventar combinaciones híbridas.

## Referencias
Fuentes y versiones en [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes-primarias): NIST SP 800-57, FIPS 203/204/205, RFC 9846 y guías de validación PKI. Revisar erratas y estado final de cada estándar antes de desplegar.
