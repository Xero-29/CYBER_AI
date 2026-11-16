# Criptografía poscuántica — Guía de dominio

**ID:** `post_quantum_crypto` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito
Prepara transición criptográfica ante riesgos de computación cuántica y obsolescencia de algoritmos. El problema inmediato es harvest-now-decrypt-later, vida útil de datos y dependencias criptográficas difíciles de sustituir. No implica que todos los sistemas deban migrar de inmediato ni que algoritmos nuevos eliminen riesgos de implementación.

## Competencias
- Inventariar algoritmos, protocolos, claves, certificados y vida útil de datos.
- Entender KEM, firmas y familias estandarizadas NIST PQC.
- Evaluar tamaños de claves, firmas, rendimiento y compatibilidad.
- Diseñar criptoagilidad y negociación híbrida.
- Gestionar HSM/KMS y actualización de firmware.
- Analizar dependencias TLS, VPN, PKI, code signing y backups.
- Preparar migración, rollback y validación interoperable.

## Controles
- Inventario criptográfico con propietario y fecha de retiro.
- Priorizar datos de larga confidencialidad y claves expuestas.
- No desplegar algoritmos experimentales sin política y evaluación.
- Probar esquemas híbridos donde estén estandarizados y soportados.
- Separar migración de KEM, firma y certificados.
- Mantener algoritmos clásicos seguros durante transición aprobada.
- Validar bibliotecas, side channels y actualizaciones HSM.
- Diseñar rollback y coexistencia sin downgrade inseguro.

## Metodología
1. Inventariar usos criptográficos y flujos.
2. Clasificar datos por confidencialidad y horizonte.
3. Identificar dependencias y puntos de sustitución.
4. Evaluar algoritmos NIST aprobados y estado de estándares.
5. Medir latencia, tamaño, interoperabilidad y límites.
6. Probar en laboratorio con bibliotecas mantenidas.
7. Planificar despliegue gradual y rollback.
8. Actualizar PKI, clientes, servidores y políticas.
9. Monitorizar fallos de negociación y compatibilidad.

## Laboratorio
Comparar handshake y tamaño de mensajes en TLS de laboratorio con configuraciones clásicas e híbridas soportadas por la versión de biblioteca. No crear algoritmos propios.

## Evaluación
Inventario completo, prioridad por vida útil, plan de migración, pruebas de interoperabilidad y estrategia de rollback.

## Referencias
NIST FIPS 203, FIPS 204, FIPS 205, NIST IR 8547, RFC PQC relevantes y NIST SP 800-57.

## Instrucciones para agentes IA
Verifica estado normativo y soporte de librería antes de recomendar despliegue. Distingue borrador, estándar final y experimento. No inventes compatibilidad.