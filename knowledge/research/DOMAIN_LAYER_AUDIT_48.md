# Auditoría granular del estándar experto — 48 especialidades

**Corte:** 2026-11-19  
**Rama:** `knowledge/develop-foundations`  
**Norma:** [EXPERT_RESEARCH_STANDARD.md](../EXPERT_RESEARCH_STANDARD.md)  
**Matriz de máquina:** [DOMAIN_LAYER_AUDIT_48.json](DOMAIN_LAYER_AUDIT_48.json)

## Resultado de la inspección documental

Se inspeccionaron los 48 compendios técnicos. Todos tienen documentos y rutas de subtemas; sin embargo, la mera existencia de secciones no demuestra cobertura de las doce capas. En varios compendios se repiten bloques metodológicos transversales sin suficiente contenido disciplinar específico. En particular, 41 compendios siguen con contenido inicial y requieren ampliación profunda; seis (identity, malware, forensics, incident_response, threat_intel y reverse) recibieron reescritura disciplinar inicial. Foundations recibió una auditoría documental individual de sus siete temas contra las doce capas; las 84 celdas están en progreso, sin capas aprobadas, y la madurez permanece M2.

**Conclusión:** las 48 áreas siguen en M2 editorial. No hay base para declarar K3/K4/K5 ni G1–G8 aprobadas globalmente. La matriz JSON registra 7 unidades temáticas iniciales por área y 12 capas por tema. Los estados iniciales permanecen `not_assessed` hasta que existe evidencia mapeada; Foundations es la excepción actual: sus 84 celdas pasan a `in_progress` tras incorporar dossiers específicos, sin inferir aprobación.

## Doce capas que deben verificarse en cada tema

- **L1 — Fundamentos teóricos**
- **L2 — Fundamentos matemáticos y formales**
- **L3 — Arquitectura y funcionamiento interno**
- **L4 — Estándares y metodologías**
- **L5 — Implementación técnica**
- **L6 — Análisis avanzado**
- **L7 — Perspectiva de seguridad**
- **L8 — Investigación científica**
- **L9 — Laboratorios y datasets**
- **L10 — Evaluación y benchmarks**
- **L11 — Conocimiento operativo y Skills**
- **L12 — Trazabilidad y mantenimiento**

## Ocho puertas que deben verificarse por especialidad

- G1 Cobertura: currículo, dependencias, temas esenciales y brechas.
- G2 Fuentes: procedencia, autoridad, versión, licencia, lectura y afirmaciones respaldadas.
- G3 Profundidad: mecanismos, modelos, supuestos, variantes, límites y contraejemplos.
- G4 Aplicación: implementación, procedimientos, resultados esperados, verificación y rollback.
- G5 Experimentación: laboratorios ejecutados, controles, datos y resultados.
- G6 Evaluación: rúbricas, benchmarks, métricas, incertidumbre y falsos positivos/negativos.
- G7 Reproducibilidad: scripts, entorno, versiones, hashes y réplica.
- G8 Revisión independiente: especialista externo, hallazgos, respuestas y cierre.

## Inventario por especialidad

### 1. `ai_red_team`

1. Plan de pruebas y threat model
2. Prompt injection
3. Abuso de herramientas y agencia
4. RAG poisoning y cross-tenant
5. Exfiltración y extracción
6. Evaluación adversarial
7. Retest y reporte

**Estado:** dossier teórico V1 de 12 capas para los siete temas base incorporado; 84/84 celdas `in_progress`, ninguna `passed`; G1–G4 y G6 `in_progress`; G5/G7 `not_started` (etapa caliente); G8 `blocked`; madurez M2.

### 2. `ai_security`

1. Datos, modelos y pipelines
2. RAG, embeddings y ACL
3. Prompt injection directa e indirecta
4. Agentes, herramientas y permisos
5. Poisoning, extracción y privacidad
6. Robustez, sesgo y leakage
7. Provenance y seguridad de inferencia

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 3. `api`

1. Modelo de amenaza y arquitectura
2. Contratos y semántica HTTP
3. REST, OpenAPI, GraphQL y gRPC
4. Identidad, OAuth/OIDC y tokens
5. Autorización y aislamiento multi-tenant
6. Rate limiting y abuso de recursos
7. Webhooks, gateways y observabilidad

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 4. `appsec`

1. Modelo de seguridad de aplicación
2. Identidad, autenticación y sesión
3. Inyección y validación de entrada
4. XSS, CSRF, SSRF y deserialización
5. APIs y arquitectura distribuida
6. Criptografía, secretos y datos
7. SDLC, supply chain y verificación

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 5. `automotive_security`

1. ECU, CAN, LIN y Ethernet
2. Gateways y arquitectura zonal
3. UDS y actualización segura
4. Secure boot y HSM
5. V2X y telemática
6. ISO/SAE 21434 y TARA
7. HIL/SIL y divulgación

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 6. `bug_bounty`

1. Alcance y autorización
2. Reconocimiento pasivo y límites
3. Validación segura
4. Impacto mínimo y no exfiltración
5. Reporte y evidencia saneada
6. Triage y severidad
7. Divulgación y retest

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 7. `business_continuity`

1. BIA, RTO, RPO y dependencias
2. Continuidad y recuperación
3. Backups inmutables
4. DR y failover
5. Crisis y comunicaciones
6. Tabletop y simulacros
7. Mejora continua

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 8. `cloud`

1. Responsabilidad compartida y landing zones
2. IAM, federación y guardrails
3. VPC/VNet, endpoints y egress
4. KMS, secretos y ciclo de claves
5. Storage, snapshots y exposición pública
6. Audit logs y postura cloud
7. IaC, drift y respuesta

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 9. `cloud_forensics`

1. Logging y fuentes cloud
2. Snapshots y objetos
3. Identidad y control plane
4. Containers y serverless
5. Timeline distribuido
6. Legal hold y cadena de custodia
7. Correlación multi-cloud

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 10. `containers`

1. Namespaces, cgroups, seccomp y capabilities
2. Imágenes, registries, firmas y SBOM
3. Docker daemon y runtime
4. Kubernetes RBAC y admission
5. Network policies, secrets y etcd
6. Supply chain y control plane
7. Detección y respuesta runtime

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 11. `crypto`

1. Entropía, aleatoriedad y DRBG
2. Hashes, MAC, KDF y firmas
3. Cifrado simétrico, modos y AEAD
4. Intercambio de claves y KEM
5. TLS, SSH, IPsec y composición
6. Gestión y ciclo de vida de claves
7. Side channels y assurance

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 12. `data_security`

1. Clasificación y linaje
2. Cifrado en tránsito, reposo y uso
3. DLP, tokenización y enmascaramiento
4. Tenant isolation y auditoría
5. Retención y borrado verificable
6. Data lakes y pipelines
7. Exfiltración y respuesta

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 13. `database_security`

1. Relacional, NoSQL y permisos
2. Roles y separación de funciones
3. Cifrado y secretos
4. Auditoría y consultas
5. SQLi y exposición
6. Backup y recuperación
7. Hardening y parches

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 14. `devsecops`

1. SDLC y threat modeling
2. CI/CD, runners y secretos
3. SAST, SCA, DAST y gates
4. SBOM, provenance y SLSA
5. IaC y policy-as-code
6. Artefactos y releases
7. Supply chain response

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 15. `edr_xdr`

1. Telemetría endpoint
2. Procesos, memoria y filesystem
3. Detecciones conductuales
4. Aislamiento y respuesta controlada
5. Integración y correlación XDR
6. Tuning y falsos positivos
7. Forense y recuperación

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 16. `email_dns_security`

1. SPF, DKIM y DMARC
2. DNSSEC y delegación
3. TLS, MTA-STS y DANE
4. Phishing y BEC
5. Dominios y certificados
6. Reputación y detección
7. Recuperación de cuentas

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 17. `forensics`

1. Cadena de custodia e integridad
2. Adquisición y write blockers
3. Filesystems, artefactos y timeline
4. Memoria y artefactos volátiles
5. Forense de red, correo y navegador
6. Forense cloud y móvil
7. Análisis, informe y testimonio

**Estado:** domain_specific_editorial_rewrite_present; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 18. `foundations`

1. Modelos de seguridad y confianza
2. Inventario y clasificación de activos
3. Superficie de ataque y modelado de amenazas
4. Identidad y control de acceso
5. Criptografía y protección de datos
6. Detección, respuesta y recuperación
7. Gobierno, riesgo y aseguramiento

**Estado:** seven_topic_audits_documented_in_progress; 12 capas por tema: `in_progress` (84/84); G1–G7: `in_progress`; G8: `blocked`; madurez: M2. Evidencia: [auditoría disciplinar](../deep_modules/foundations/FOUNDATIONS_DEEP_DEVELOPMENT_V1.md), [revisión de fuentes](../deep_modules/foundations/SOURCE_REVIEW_AND_CLAIM_EVIDENCE_2026-11-19.md), [resultados sintéticos](../deep_modules/foundations/labs/results.json). Siete labs ejecutados localmente con datos sintéticos y 8 pruebas unitarias; falta réplica independiente, integración real aislada y revisión externa.

### Estado detallado de Foundations — auditoría 2026-11-19

| Tema | Capas | Corrección documental | Evidencia pendiente |
|---|---:|---|---|
| foundations-01 Modelos de seguridad y confianza | 12/12 en progreso | Modelo formal, arquitectura PDP/PEP, pruebas de autorización y fallos de confianza | Laboratorio ejecutado localmente; réplica y revisión independiente |
| foundations-02 Inventario y clasificación de activos | 12/12 en progreso | Esquema de activos, reconciliación multi-fuente, métricas y dataset sintético | Ground truth sintético ejecutado; validación con fuentes reales pendiente |
| foundations-03 Superficie de ataque y modelado de amenazas | 12/12 en progreso | DFD, attack graphs, STRIDE/abuse cases, evaluación ciega | Cobertura de rutas sintéticas ejecutada; acuerdo de revisores pendiente |
| foundations-04 Identidad y control de acceso | 12/12 en progreso | Ciclo de vida, federación, tokens, privilegios y revocación | Claims sintéticos probados; verificación JWT/protocolo real pendiente |
| foundations-05 Criptografía y protección de datos | 12/12 en progreso | Modelos criptográficos, ciclo de claves, AEAD, fallos y agilidad | HMAC sintético probado; vectores AES/AEAD, interoperabilidad y KMS pendientes |
| foundations-06 Detección, respuesta y recuperación | 12/12 en progreso | Pipeline de telemetría, respuesta, recuperación y métricas | Timeline sintético ejecutado; detección y evaluación sobre dataset real pendiente |
| foundations-07 Gobierno, riesgo y aseguramiento | 12/12 en progreso | Registro de riesgos, assurance case, roles y trazabilidad | Evidencia sintética evaluada; revisión ciega e independiente pendiente |

**Dictamen:** la cobertura documental por tema y capa fue añadida; no equivale a K3/K4/K5. G1–G4 continúan en progreso. G5–G7 en progreso por ejecución sintética local, métricas y repetición determinista; G8 bloqueada por falta de revisión independiente. No se promueven puertas a `passed`. Las fuentes NIST inspeccionadas no se consideran lectura integral.

### 19. `fraud_abuse`

1. Modelos de abuso y trust/safety
2. Identidad sintética y bots
3. Grafos y anomalías
4. Account takeover
5. Detección y fricción adaptativa
6. Privacidad y falsos positivos
7. Apelación y métricas

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 20. `governance`

1. Gobierno, apetito de riesgo y políticas
2. ISO 27001, NIST CSF y controles
3. Inventario y propietarios
4. Riesgo y planes de tratamiento
5. Auditoría y evidencia
6. Privacidad y terceros
7. Métricas y mejora

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 21. `hardware_security`

1. Amenazas de hardware y cadena física
2. Secure boot y root of trust
3. Firmware y rollback
4. Debug interfaces y protección
5. Side channels en laboratorio
6. TEE, HSM y enclaves
7. Attestation y lifecycle

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 22. `identity`

1. IAM, IGA, PAM y ciclo de vida
2. MFA resistente a phishing
3. OAuth 2.0, OIDC, SAML y Kerberos
4. RBAC, ABAC, ReBAC y autorización
5. Workload identity y secretos
6. Recertificación y SoD
7. Abuso y recuperación de cuentas

**Estado:** domain_specific_editorial_rewrite_present; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 23. `incident_response`

1. Preparación, gobierno, roles y severidad
2. Detección, triage y validación
3. Contención y preservación
4. Erradicación, recuperación y validación
5. Ransomware, BEC, cloud y supply chain
6. Comunicación y coordinación
7. Postmortem, métricas y mejora

**Estado:** domain_specific_editorial_rewrite_present; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 24. `iot_hardware`

1. MCU/SoC y buses
2. UART, SPI, I2C, JTAG y SWD
3. Firmware, bootloader y secure boot
4. OTA y rollback protection
5. Radio, sensores y gateways
6. Debug ports y secretos
7. Ciclo de vida y laboratorio

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 25. `linux`

1. Kernel, namespaces y capabilities
2. Usuarios, grupos, sudo y PAM
3. Permisos, ACL, SELinux y AppArmor
4. systemd, servicios y hardening
5. SSH, firewall, auditd y logs
6. Paquetes, SBOM y parches
7. Aislamiento y respuesta

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 26. `machine_learning`

1. Estadística y generalización
2. Datasets, leakage y splits
3. Feature engineering y pipelines
4. Robustez, drift y monitorización
5. Privacidad y poisoning
6. MLOps y reproducibilidad
7. Evaluación de modelos

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 27. `malware`

1. Formatos PE, ELF, Mach-O y documentos
2. Análisis estático e indicadores
3. Sandbox y análisis dinámico aislado
4. Persistencia, memoria y filesystem
5. YARA, Sigma, IOC y correlación
6. Familias y comportamiento
7. Contención, erradicación y reporte

**Estado:** domain_specific_editorial_rewrite_present; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 28. `mathematics`

1. Lógica y demostración
2. Álgebra lineal y cálculo numérico
3. Probabilidad e inferencia
4. Teoría de información y entropía
5. Grafos y optimización
6. Series temporales y anomalías
7. Incertidumbre y validación

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 29. `mobile`

1. Android sandbox, permisos y Keystore
2. iOS sandbox, entitlements y Keychain
3. Almacenamiento local y backups
4. TLS y confianza del dispositivo
5. Deep links, IPC, intents y WebView
6. MASVS/MSTG y análisis
7. MDM/MAM y respuesta

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 30. `network`

1. OSI/TCP-IP, routing y switching
2. VLAN, VRF, microsegmentación y Zero Trust
3. Firewalls, ACL, NAT y egress
4. DNS, DHCP, NTP, VPN, TLS e IPsec
5. Wi-Fi empresarial y acceso
6. PCAP, NetFlow, Zeek y detección
7. Resiliencia y gestión fuera de banda

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 31. `ot_ics`

1. Purdue, zonas y conduits
2. PLC, RTU, HMI y SCADA
3. Modbus, DNP3 y OPC UA
4. Safety y ventanas de cambio
5. Segmentación y acceso remoto
6. Inventario pasivo y detección
7. Respuesta coordinada con operaciones

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 32. `physical_security`

1. Zonificación y perímetros
2. Acceso y visitantes
3. CCTV y sensores
4. USB y medios extraíbles
5. Salas, racks y cableado
6. Convergencia físico-digital
7. Respuesta coordinada

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 33. `pki_hsm`

1. X.509 y cadena de confianza
2. CA y políticas CP/CPS
3. OCSP, CRL y CT
4. HSM y ceremonia de claves
5. mTLS y code signing
6. Rotación y expiración
7. Compromiso de CA

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 34. `post_quantum_crypto`

1. Harvest-now-decrypt-later
2. ML-KEM y ML-DSA
3. Híbridos e interoperabilidad
4. Inventario criptográfico
5. Rendimiento y restricciones
6. Cripto-agilidad
7. Plan de migración

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 35. `privacy_engineering`

1. Inventario y flujos de datos personales
2. Privacy by design y DPIA
3. Minimización y retención
4. Consentimiento y derechos
5. Pseudonimización y PET
6. Telemetría privada
7. Incidentes y evidencia

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 36. `red_team`

1. ROE, alcance y reglas de parada
2. Planificación basada en amenazas
3. Reconocimiento autorizado
4. Validación con impacto mínimo
5. Emulación ATT&CK
6. Evidencia y deconfliction
7. Retest y purple teaming

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 37. `reverse`

1. Arquitecturas, ABI y calling conventions
2. Desensamblado y depuración
3. Control flow y data flow
4. Parsing, formatos y protocolos
5. Ofuscación y anti-análisis
6. Fuzzing y análisis diferencial
7. Firmware y componentes embebidos

**Estado:** domain_specific_editorial_rewrite_present; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 38. `satellite_security`

1. Segmentos espacial y terrestre
2. TT&C y telemetría
3. RF y espectro
4. Firmware y estaciones terrestres
5. Resiliencia y anti-jamming
6. Identidad y criptografía
7. Simulación y coordinación

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 39. `secure_arch`

1. Requisitos y atributos de calidad
2. Contexto y límites de confianza
3. STRIDE, attack trees y abuse cases
4. Zero Trust y defensa en profundidad
5. Identidad, datos y secretos
6. Resiliencia y observabilidad
7. Revisión y ADR

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 40. `soc_siem`

1. Telemetría y normalización
2. SIEM y retención
3. Correlación y detección
4. ATT&CK coverage
5. SOAR y aprobaciones
6. Triage y gestión de casos
7. Detección como código

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 41. `software_engineering`

1. Diseño modular y contratos
2. Tipado y manejo de errores
3. Pruebas unitarias, integración y property tests
4. Concurrencia y rendimiento
5. Dependencias y packaging
6. CI, revisión y análisis estático
7. Observabilidad y rollback

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 42. `telecom_5g`

1. 5G Core y RAN
2. Slicing y service-based architecture
3. SIM/eSIM y AKA
4. Señalización y roaming
5. Virtualización y edge
6. Monitorización y fraude
7. Supply chain telecom

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 43. `threat_hunting`

1. Hipótesis basadas en TTP
2. Calidad de telemetría
3. KQL, Sigma y pivots
4. Líneas base y anomalías
5. Validación de hipótesis
6. Detecciones persistentes
7. Cobertura y reproducibilidad

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 44. `threat_intel`

1. Ciclo de inteligencia, PIR y requisitos
2. OSINT, fiabilidad, sesgos y validación
3. STIX, TAXII, MISP y modelado
4. TTP, ATT&CK y comportamiento
5. Atribución y campañas
6. Indicadores y utilidad operacional
7. Productos, difusión y feedback

**Estado:** domain_specific_editorial_rewrite_present; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 45. `vuln_management`

1. Descubrimiento e inventario
2. CVE, CWE, CVSS, EPSS y KEV
3. Priorización contextual
4. Validación y deduplicación
5. SLA, excepciones y parches
6. Verificación y regresión
7. Exposición y riesgo residual

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 46. `vulnerability_research`

1. CWE y root cause
2. Fuzzing y sanitizers
3. Análisis y reducción de casos
4. Reproducción aislada
5. Impacto y mitigación
6. Coordinated disclosure y CVE
7. Regresión y advisories

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 47. `windows_ad`

1. Windows internals, procesos y servicios
2. AD, Kerberos, LDAP y DNS
3. GPO, delegación, ACL y tiering
4. NTLM, LAPS, gMSA y credenciales
5. PowerShell, Sysmon y Event Logs
6. Defender, ASR y hardening
7. Abuso de identidad y recuperación AD

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

### 48. `wireless_security`

1. 802.11, WPA2/3 y 802.1X
2. Diseño RF y segmentación
3. Bluetooth LE y GATT
4. NFC y RFID
5. WIDS/WIPS y rogue AP
6. Captura en laboratorio
7. Hardening de dispositivos

**Estado:** generic_or_initial_compendium_requires_deep_audit; 12 capas por tema: `not_assessed`; G1–G8: `not_assessed`; madurez: M2.

## Regla de ejecución

1. Auditar cada tema contra las doce capas; marcar `not_applicable` solo con justificación disciplinar.
2. Identificar brechas concretas, no solo faltas de encabezados.
3. Investigar fuentes primarias y registrar lectura real por página/sección.
4. Desarrollar contenido técnico original con referencias y contraejemplos.
5. Diseñar y ejecutar laboratorios seguros; conservar datos, scripts, hashes y resultados.
6. Evaluar con pruebas positivas, negativas y casos límite.
7. Someter a revisión independiente y reproducción cuando corresponda.
8. Actualizar estados K1–K5 y G1–G8 únicamente con evidencia.

**Orden de trabajo recomendado:** completar el inventario tema×capa en los seis módulos ya reescritos y luego desarrollar los 42 compendios restantes en lotes priorizados por criticidad y dependencias. La automatización de búsqueda/descarga se implementará después como herramienta de remediación de brechas; no sustituye lectura crítica ni validación.
