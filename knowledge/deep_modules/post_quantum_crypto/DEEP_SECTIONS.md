# Secciones de profundización — Criptografía poscuántica

## Modelo de amenazas
Evaluar harvest-now-decrypt-later, horizonte de confidencialidad, vida útil de datos, dependencia criptográfica y capacidad de actualización. Inventariar protocolos, certificados, bibliotecas, dispositivos y proveedores. Amenazas incluyen algoritmo obsoleto, implementación no validada, tamaños incompatibles, downgrade y transición híbrida improvisada.

## Detección
Mantener inventario criptográfico con algoritmo, versión, uso, endpoint, certificado, proveedor y fecha de migración. Detectar suites heredadas, certificados no renovables, bibliotecas sin soporte y negociación downgrade. Medir cobertura del inventario y compatibilidad de clientes; distinguir estándar final de borrador y errata.

## Respuesta a incidentes
Si una primitiva o implementación queda comprometida, clasificar datos y servicios expuestos, restringir negociación, migrar a perfil estandarizado, reemitir certificados y re-envolver datos según plan. Preservar interoperabilidad y fallback seguro; evitar activar algoritmos experimentales sin análisis.

## Casos prácticos
En testbed, comparar handshake clásico y perfil híbrido estandarizado disponible en la implementación probada. Medir latencia, tamaño de mensajes, memoria e interoperabilidad; verificar rechazo de downgrade y registrar versiones exactas. No extrapolar benchmark a seguridad matemática.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST FIPS 203/204/205, NIST migration guidance e IETF. Revisar erratas y perfiles antes de despliegue.
