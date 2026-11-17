# Telecomunicaciones y 5G — Guía de dominio

**ID:** `telecom_5g` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege redes móviles y telecom: RAN, core, transporte, OSS/BSS, SIM/eSIM, roaming, interconexión, slicing, edge y virtualización de funciones. La disponibilidad y seguridad de emergencia son críticas. No realizar pruebas radioeléctricas, interferencia ni escaneos sobre redes comerciales.

## Arquitectura y amenazas
Revisar gNodeB, AMF, SMF, UPF, AUSF, UDM, NRF, PCF, NEF, SEPP, IMS, MEC, NFV, SDN, O-RAN, interfaces de gestión y supply chain. Riesgos: exposición de interfaces de gestión, abuso API SBA, configuración de slice, identidad SIM, roaming, signaling, virtualización y cadena de suministro.

## Competencias
- Entender 5G SBA, service-based interfaces y autenticación mutua.
- Revisar segmentación, slicing y aislamiento de tenants.
- Proteger SIM/eSIM, aprovisionamiento y credenciales.
- Analizar señalización SS7/Diameter/5G sin afectar redes reales.
- Evaluar NFV/CNF, Kubernetes y cloud-native core.
- Revisar seguridad O-RAN y cadena de suministro.
- Diseñar resiliencia, logging y detección de fraude.

## Controles
- mTLS y OAuth2 para interfaces SBA según especificación.
- Exposición mínima de NRF/NEF y APIs de gestión.
- Segmentación de planos control, usuario y operación.
- Gestión de certificados, secretos y ciclo de vida de SIM.
- Aislamiento de slices y límites de recursos.
- Hardening de CNF, nodos y pipelines.
- Telemetría de signaling y anomalías con privacidad.
- Redundancia y pruebas de recuperación sin afectar servicio.

## Metodología
1. Definir operador, laboratorio, interfaces y autorización.
2. Inventariar funciones, versiones, flujos y dependencias.
3. Revisar API, identidad, certificados y configuración.
4. Analizar aislamiento de slices y planos de red.
5. Evaluar virtualización, supply chain y acceso de proveedores.
6. Validar con simulador o testbed privado.
7. Medir disponibilidad, failover y detección.
8. Documentar riesgos y cambios con operador de red.

## Laboratorio
5G core de laboratorio con Open5GS/srsRAN y SIM de prueba. Validar mTLS, políticas de API y segmentación en red aislada. No emitir señales RF fuera de entorno legal y controlado.

## Evaluación
Interfaces restringidas, autenticación mutua, slices aislados, SIM gestionadas, logging útil y failover probado.

## Referencias
3GPP TS 33.501, GSMA NESAS, ETSI NFV Security, O-RAN security specifications y NIST SP 800-187.

## Instrucciones para agentes IA
No sugieras jamming, IMSI catching ni interceptación. Limita pruebas a simuladores, testbeds privados y autorizaciones documentadas.