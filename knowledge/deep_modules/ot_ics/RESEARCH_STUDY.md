# Investigación técnica: Seguridad OT, ICS, SCADA y sistemas ciberfísicos

**ID:** ot_ics · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 en elaboración · **Revisión de seguridad funcional:** pendiente.

> Toda prueba activa requiere autorización del propietario y análisis de impacto. En PLC, SCADA, energía, agua, transporte, edificios y procesos físicos, usar simuladores o bancos aislados; no experimentar en producción.

## Modelo operacional
OT incluye sistemas programables que observan o modifican el entorno físico. Sus prioridades pueden diferir de IT: seguridad de personas, integridad del proceso, disponibilidad, determinismo, continuidad y recuperación segura pueden prevalecer sobre confidencialidad. Un control que reinicia un servidor IT puede ser inaceptable si detiene una línea, altera una válvula o interrumpe protección.

El análisis debe integrar ciberseguridad y safety: consecuencias físicas, estados seguros, interlocks, modos degradados, ventanas de mantenimiento, dependencia del fabricante, ingeniería de control y operación humana. Clasificar activos por función, proceso, criticidad, zona, propietario, firmware, soporte, protocolo, conectividad y consecuencias de fallo.

## Arquitectura y zonas
Identificar sensores, actuadores, PLC, RTU, DCS, HMI, SCADA, historiadores, estaciones de ingeniería, servidores de salto, gateways, safety instrumented systems (SIS) y servicios corporativos. Modelar zonas/conduits y flujos permitidos; Purdue ayuda a comunicar arquitectura, pero no es garantía de seguridad ni taxonomía suficiente para toda instalación.

Separar redes de control, seguridad funcional, gestión, supervisión, DMZ industrial y enterprise; documentar excepciones y dependencias. El acceso remoto debe ser mediado, temporal, aprobado, grabado y revocable; evitar conexiones directas persistentes de proveedores. Proteger planos de gestión, backups de lógica/configuración, ingeniería y sincronización temporal.

## Protocolos y superficies
### Modbus TCP/RTU
Analizar autenticación según variante, semántica de coils/registers, funciones de lectura/escritura, gateways seriales, exposición de puertos, segmentación y validación de comandos. Cifrar el túnel no elimina riesgo de comandos maliciosos desde endpoint autorizado.

### DNP3
Estudiar arquitectura outstation/master, eventos, time synchronization, unsolicited responses, autenticación segura donde esté desplegada, gateway y operación degradada. Evaluar versión y compatibilidad del fabricante; no inferir soporte de Secure Authentication por nombre del protocolo.

### OPC UA
Revisar endpoints, certificados, trust lists, políticas de seguridad, modos Sign/SignAndEncrypt, gestión de usuarios, permisos de nodos, auditoría y actualización. Un canal seguro no compensa permisos excesivos ni certificados mal gestionados.

### Otros protocolos
Incluir EtherNet/IP/CIP, PROFINET, IEC 60870-5-104, IEC 61850, BACnet, HART, MQTT industrial y protocolos propietarios según sector. Cada ficha debe documentar edición, perfiles, autenticación, cifrado, roles, límites, seguridad funcional e interoperabilidad.

## Amenazas y fallos
- Acceso remoto comprometido y credenciales de proveedor.
- Estación de ingeniería infectada o con software no autorizado.
- Cambios no aprobados en lógica PLC, recetas, setpoints o firmware.
- Segmentación deficiente entre IT/OT o rutas de administración compartidas.
- Protocolo industrial expuesto sin autenticación adecuada.
- Manipulación de telemetría, alarmas, historian o sincronización temporal.
- Ransomware que afecta ingeniería, HMI, AD industrial o backups.
- Firmware vulnerable sin parche disponible.
- Fallo de safety, pérdida de visibilidad o modo inseguro por intervención de seguridad.
- Dependencia cloud/remota o IIoT que amplía superficie.

No convertir un escenario plausible en incidente observado sin evidencia de proceso, logs, configuración o telemetría.

## Controles por ciclo
**Gobernar:** política OT, roles, proveedores, inventario, riesgo de proceso, safety case, ventanas y gestión de cambios.

**Identificar:** inventario pasivo, mapa de flujos, criticidad, dependencias, firmware, EOL/EOS y rutas de acceso.

**Proteger:** segmentación, allowlisting de aplicaciones, MFA remoto, jump hosts, mínimo privilegio, backups offline, hardening validado, control de medios extraíbles y protección de estaciones de ingeniería.

**Detectar:** monitoreo pasivo compatible con OT, baseline de protocolos, alertas de comandos anómalos, cambios de lógica, acceso remoto, ingeniería y eventos de safety. Evitar escaneo intrusivo y agentes endpoint no aprobados.

**Responder:** playbooks coordinados con operaciones, ingeniería, safety, fabricante y continuidad; preservar evidencia sin interferir con proceso; aislar solo tras evaluar consecuencias físicas.

**Recuperar:** restaurar lógica/configuración validada, firmware, HMI, historian y backups; verificar proceso y safety antes de reconectar; retest y revisión post-incidente.

## Proceso de evaluación
1. Reunión con operaciones, ingeniería, safety, IT, seguridad y proveedor.
2. Acordar activos excluidos, proceso, estado seguro, ventanas, contactos y stop conditions.
3. Construir inventario pasivo y diagrama validado por operador.
4. Analizar configuración y flujos fuera de línea.
5. Revisar vulnerabilidades del fabricante y aplicabilidad por modelo/firmware.
6. Probar detección y recuperación en réplica/simulador.
7. Aprobar pruebas activas con análisis de riesgo y acompañamiento operacional.
8. Registrar impacto potencial, resultados, evidencia y desviaciones.
9. Probar restauración y operación segura, no solo arranque.

## Laboratorios y métricas
Labs: simulador PLC/HMI, OpenPLC en red aislada, emuladores Modbus/OPC UA, PCAP industriales sintéticos, historian de prueba y escenarios de backup/restore. Mantener red sin puente a producción, límites de recursos, imágenes fijadas y snapshots.

Métricas: porcentaje de activos OT inventariados, flujos con propietario, accesos remotos temporales vs permanentes, cambios de lógica autorizados, tiempo de detección, disponibilidad, tiempo de recuperación validado, integridad de backups y tasa de falsas alarmas.

## Estado normativo crítico
NIST SP 800-82 Rev. 3 (2023) es la guía final inspeccionada. **NIST SP 800-82 Rev. 4 se publicó como Initial Public Draft el 21 de septiembre de 2026**, con comentarios hasta el 30 de noviembre de 2026. Amplía sectores (agua, alimentos/agricultura, ferrocarril, marítimo, BACS, IIoT/cloud), se reestructura alrededor de CSF 2.0 y profundiza asset management, monitoring y zero trust. El borrador Rev. 4 no debe presentarse como estándar final ni sustituir silenciosamente Rev. 3. Registrar ambos con estado distinto. Complementar con ISA/IEC 62443 y normas sectoriales; no reproducir material normativo restringido.

## Fuentes primarias
- NIST SP 800-82 Rev. 3 final: https://doi.org/10.6028/NIST.SP.800-82r3
- NIST SP 800-82 Rev. 4 Initial Public Draft: https://csrc.nist.gov/pubs/sp/800/82/r4/ipd
- NIST notice Rev. 4: https://www.nist.gov/news-events/news/2026/09/guide-operational-technology-ot-security-nist-requests-comments-draft-sp
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- NIST SP 800-207 Zero Trust: https://doi.org/10.6028/NIST.SP.800-207
- CISA ICS Advisories: https://www.cisa.gov/news-events/cybersecurity-advisories

**Estado de evidencia:** se revisaron páginas oficiales de NIST para Rev. 3 y el borrador Rev. 4. No se afirma revisión integral de IEC 62443, inspección de una planta, ejecución de laboratorio ni aprobación de safety.
