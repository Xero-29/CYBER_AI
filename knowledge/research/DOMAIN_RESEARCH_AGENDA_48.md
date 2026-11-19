# Matriz de investigación específica de las 48 especialidades

**Versión:** 1.0 · **Estado:** agenda de investigación propuesta; no resultados científicos.  
**Estándar:** `knowledge/EXPERT_RESEARCH_STANDARD.md` · **Madurez:** no M3/M4/M5 hasta cumplir evidencias y puertas G1–G8.

## Protocolo transversal
Cada línea debe convertirse en preregistro con población/sistema, unidad de análisis, baseline, variables, criterios de inclusión/exclusión, tamaño de muestra, semillas, versiones, criterios de refutación, análisis de incertidumbre, ética, seguridad, artefactos y revisión. Las pruebas activas se limitan a activos propios o autorizados y laboratorios aislados. Resultados negativos y desviaciones se conservan.

## Agenda por especialidad

### 1. Fundamentos (`foundations`)
**Pregunta:** ¿Qué combinación de inventario, modelado de amenazas y controles produce mayor reducción de riesgo verificable?
**Hipótesis de trabajo:** Comparar evaluación basada en escenarios frente a checklist, manteniendo población y criterios constantes.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Cobertura de activos, defectos reproducibles, riesgo residual, esfuerzo.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 2. Seguridad de aplicaciones (`appsec`)
**Pregunta:** ¿Qué combinación de análisis estático, dinámico, SCA y revisión manual reduce defectos explotables sin saturar triage?
**Hipótesis de trabajo:** Corpus de aplicaciones sintéticas vulnerables y benignas; comparación ciega de métodos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Precision, recall, F1, defectos confirmados, tiempo de triage.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 3. Seguridad de API (`api`)
**Pregunta:** ¿Qué pruebas detectan mejor BOLA/BFLA, abuso de flujo y fallos de contrato en APIs multi-tenant?
**Hipótesis de trabajo:** API de laboratorio con matriz de identidades, objetos, scopes y contratos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Cobertura de autorización, falsos positivos, violaciones confirmadas.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 4. Seguridad de redes (`network`)
**Pregunta:** ¿Qué segmentación reduce reachability no autorizada con coste operacional aceptable?
**Hipótesis de trabajo:** Topología virtual con baseline VLAN/ACL y política contextual.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Reachability prohibida, latencia p95, excepciones, fallos.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 5. Linux y Unix (`linux`)
**Pregunta:** ¿Qué combinación de namespaces, capabilities, LSM y seccomp reduce superficie sin romper funciones legítimas?
**Hipótesis de trabajo:** Servicios sintéticos con perfiles incrementales y pruebas de regresión.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Syscalls permitidas, escapes simulados, fallos funcionales, overhead.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 6. Windows y Active Directory (`windows_ad`)
**Pregunta:** ¿Qué controles de identidad, tiering y telemetría reducen rutas de privilegio en un bosque de laboratorio?
**Hipótesis de trabajo:** Bosque AD sintético con ACL/GPO y delegaciones conocidas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Rutas de privilegio, cobertura de eventos, tiempo de detección.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 7. Seguridad cloud (`cloud`)
**Pregunta:** ¿Qué controles de IAM, red y logging detectan y previenen configuraciones de alto riesgo en entornos multi-cuenta?
**Hipótesis de trabajo:** Landing zone sintética con cambios IaC controlados.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Permisos excesivos, exposición pública, drift, tiempo de remediación.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 8. Contenedores y Kubernetes (`containers`)
**Pregunta:** ¿Qué combinación de políticas de admisión, RBAC y network policies reduce privilegios y movimiento lateral?
**Hipótesis de trabajo:** Cluster efímero con workloads y roles sintéticos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Violaciones admitidas, reachability, falsos positivos, overhead.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 9. Seguridad móvil (`mobile`)
**Pregunta:** ¿Qué controles de almacenamiento, IPC y autenticación reducen fuga de datos entre versiones de OS?
**Hipótesis de trabajo:** Aplicación propia de prueba en emuladores y dispositivos de laboratorio.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Hallazgos confirmados, datos expuestos, cobertura por OS.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 10. Criptografía (`crypto`)
**Pregunta:** ¿Qué errores de integración criptográfica generan mayor riesgo pese al uso de primitivas aprobadas?
**Hipótesis de trabajo:** Revisión y pruebas de implementaciones didácticas con vectores oficiales.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Errores de nonce, validación, interoperabilidad, side-channel observable.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 11. Identidad y acceso (`identity`)
**Pregunta:** ¿Qué controles reducen privilegios persistentes y fallos de autorización en identidades humanas y workload?
**Hipótesis de trabajo:** IdP sintético con roles, tokens, lifecycle y rutas de delegación.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Cuentas huérfanas, permisos excesivos, revocación, falsos bloqueos.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 12. Análisis de malware (`malware`)
**Pregunta:** ¿Qué combinación de features estáticas y dinámicas mejora clasificación sin sobreajustar a familias conocidas?
**Hipótesis de trabajo:** Corpus autorizado y etiquetado, sandbox aislado y partición temporal.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Precision, recall, FPR, robustez a empaquetado, coste.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 13. Informática forense (`forensics`)
**Pregunta:** ¿Qué secuencia de adquisición maximiza evidencia relevante y minimiza alteración?
**Hipótesis de trabajo:** Imágenes y VMs con ground truth, adquisición repetida y control negativo.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Artefactos recuperados, alteración, reproducibilidad, tiempo.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 14. Respuesta a incidentes (`incident_response`)
**Pregunta:** ¿Qué diseño de playbook mejora contención y recuperación sin impacto colateral excesivo?
**Hipótesis de trabajo:** Tabletop y simulación de incidentes con injects y decisiones registradas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Tiempo a contención, RTO observado, impacto, acciones omitidas.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 15. Inteligencia de amenazas (`threat_intel`)
**Pregunta:** ¿Qué criterios de procedencia, corroboración y caducidad mejoran la utilidad operacional de inteligencia?
**Hipótesis de trabajo:** Feeds sintéticos/abiertos versionados y casos de decisión ciegos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Oportunidad, precisión, acción habilitada, IOC caducados.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 16. Ingeniería inversa (`reverse`)
**Pregunta:** ¿Qué técnicas de análisis recuperan semántica de binarios con mayor precisión y coste controlado?
**Hipótesis de trabajo:** Binarios propios de fuente conocida, símbolos retirados y variantes compiladas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Funciones identificadas, precisión de hipótesis, cobertura, tiempo.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 17. IoT y hardware (`iot_hardware`)
**Pregunta:** ¿Qué controles de provisioning, secure boot y OTA reducen riesgo de clonación y firmware no autorizado?
**Hipótesis de trabajo:** Plataforma de desarrollo propia con firmware y claves sintéticas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Actualizaciones rechazadas, rollback, exposición de secretos, recuperación.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 18. DevSecOps (`devsecops`)
**Pregunta:** ¿Qué controles del pipeline detectan cambios inseguros antes del release con menor fricción?
**Hipótesis de trabajo:** CI aislado con fallos sembrados y artefactos versionados.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Vulnerabilidades escapadas, tiempo feedback, falsos positivos, provenance.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 19. Seguridad de IA (`ai_security`)
**Pregunta:** ¿Qué controles externos al modelo reducen prompt injection y uso indebido de herramientas?
**Hipótesis de trabajo:** RAG y herramientas mock con corpus adversarial sintético.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Attack success rate, leakage, tool misuse, utilidad, falsos rechazos.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 20. Gobierno y riesgo (`governance`)
**Pregunta:** ¿Qué evidencia distingue controles diseñados de controles operativos eficaces?
**Hipótesis de trabajo:** Muestreo de controles en organización sintética con evidencias incompletas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Cobertura, fallos de operación, excepciones vencidas, riesgo residual.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 21. Gestión de vulnerabilidades (`vuln_management`)
**Pregunta:** ¿Qué modelo contextual prioriza mejor la remediación que CVSS aislado?
**Hipótesis de trabajo:** Dataset versionado con CVE/KEV/EPSS y activos sintéticos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Tiempo de remediación, exposición acumulada, falsos positivos.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 22. Bug bounty (`bug_bounty`)
**Pregunta:** ¿Qué criterios de reporte y retest mejoran reproducibilidad y calidad del triage?
**Hipótesis de trabajo:** Aplicación deliberadamente vulnerable y evaluadores ciegos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Reproducibilidad, duplicados, precisión de impacto, tiempo triage.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 23. Arquitectura segura (`secure_arch`)
**Pregunta:** ¿Qué proceso de threat modeling descubre fallos de trust boundary antes de implementación?
**Hipótesis de trabajo:** Dos diseños equivalentes evaluados con STRIDE/attack trees y tests.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Amenazas confirmadas, cobertura, cambios tardíos, riesgo residual.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 24. Seguridad de datos (`data_security`)
**Pregunta:** ¿Qué combinación de clasificación, autorización y DLP reduce exposición sin bloquear uso legítimo?
**Hipótesis de trabajo:** Flujos sintéticos con etiquetas y canales controlados.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Fuga simulada, falsos positivos, cobertura de linaje.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 25. Ingeniería de software (`software_engineering`)
**Pregunta:** ¿Qué mezcla de pruebas basadas en propiedades, fuzzing y revisión encuentra más fallos por coste?
**Hipótesis de trabajo:** Repositorios de ejemplo con defectos sembrados y ground truth.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Defectos confirmados, cobertura, mutation score, tiempo.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 26. Seguridad de ML (`machine_learning`)
**Pregunta:** ¿Qué defensas reducen poisoning y extracción bajo presupuestos de ataque definidos?
**Hipótesis de trabajo:** Dataset/modelo sintético con threat model y splits temporales.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Robust accuracy, attack success, leakage, utilidad.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 27. Seguridad de hardware (`hardware_security`)
**Pregunta:** ¿Qué controles de boot, debug y provisioning protegen una plataforma embebida bajo acceso físico definido?
**Hipótesis de trabajo:** Placa de desarrollo propia y firmware de laboratorio.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Bypass de boot, interfaces expuestas, recuperación, repetibilidad.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 28. Matemáticas para ciberseguridad (`mathematics`)
**Pregunta:** ¿Qué métodos estadísticos mejoran calibración y confianza de detecciones con prevalencia baja?
**Hipótesis de trabajo:** Dataset sintético con prevalencias controladas y ground truth.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Calibration error, precision-recall, intervalos, sensibilidad.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 29. SOC y SIEM (`soc_siem`)
**Pregunta:** ¿Qué combinación de normalización y correlación reduce ruido manteniendo cobertura de incidentes?
**Hipótesis de trabajo:** Logs sintéticos multi-fuente con casos etiquetados.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Precision, recall, ingest lag, alert-to-case ratio.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 30. EDR/XDR (`edr_xdr`)
**Pregunta:** ¿Qué fuentes y correlaciones aportan cobertura robusta ante gaps de sensores?
**Hipótesis de trabajo:** Replay multi-host y simulación de sensor offline.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Cobertura, latencia, pérdida, falsos positivos.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 31. Red Team (`red_team`)
**Pregunta:** ¿Qué ejercicios autorizados revelan fallos de control que no aparecen en pruebas aisladas?
**Hipótesis de trabajo:** Emulación segura en laboratorio con purple team y kill switch.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Controles validados, detección, contención, impacto.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 32. Seguridad inalámbrica (`wireless_security`)
**Pregunta:** ¿Qué configuraciones de autenticación y segmentación minimizan acceso no autorizado en WLAN?
**Hipótesis de trabajo:** APs aislados y clientes de prueba con matriz de perfiles.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Accesos indebidos, roaming, falsos positivos, cobertura.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 33. Seguridad OT/ICS (`ot_ics`)
**Pregunta:** ¿Qué controles pasivos y segmentación reducen exposición sin comprometer safety/availability?
**Hipótesis de trabajo:** Digital twin y protocolos industriales sintéticos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Visibilidad, cambios no autorizados detectados, disponibilidad.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 34. Telecomunicaciones 5G (`telecom_5g`)
**Pregunta:** ¿Cómo validar aislamiento de slices y seguridad de APIs SBA bajo fallos y carga?
**Hipótesis de trabajo:** 5G core simulator con identidades y slices sintéticos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Aislamiento, latencia, disponibilidad, fallos de autorización.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 35. Seguridad automotriz (`automotive_security`)
**Pregunta:** ¿Qué controles de gateway y actualización reducen riesgo de mensajes y firmware no autorizados?
**Hipótesis de trabajo:** HIL/simulador CAN con mensajes sintéticos y OTA de prueba.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Mensajes rechazados, replay detectado, rollback seguro.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 36. Seguridad satelital (`satellite_security`)
**Pregunta:** ¿Qué mecanismos de autenticación y anti-replay mantienen integridad de comandos con latencia/pérdida?
**Hipótesis de trabajo:** Simulador de telemetría y canal con condiciones controladas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Comandos no autorizados aceptados, disponibilidad, recuperación.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 37. Seguridad física (`physical_security`)
**Pregunta:** ¿Qué controles de acceso y monitorización detectan intrusión sin aumentar riesgo de seguridad humana?
**Hipótesis de trabajo:** Ejercicio controlado con escenarios físicos ficticios.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Tiempo detección, cobertura, falsas alarmas, evacuación segura.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 38. Correo y DNS (`email_dns_security`)
**Pregunta:** ¿Qué combinación SPF/DKIM/DMARC, autenticación y telemetría reduce spoofing/BEC?
**Hipótesis de trabajo:** Dominios y mensajes sintéticos, escenarios de forwarding y spoof.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Alineación, spoof detection, falsos positivos, tiempo contención.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 39. Fraude y abuso (`fraud_abuse`)
**Pregunta:** ¿Qué umbrales y modelos minimizan pérdida y falsos rechazos bajo cambio adversarial?
**Hipótesis de trabajo:** Dataset temporal sintético con costes asimétricos y segmentos.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** PR-AUC, calibration, loss, false decline, fairness.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 40. Ingeniería de privacidad (`privacy_engineering`)
**Pregunta:** ¿Qué técnicas reducen reidentificación manteniendo utilidad suficiente para un caso de uso?
**Hipótesis de trabajo:** Dataset sintético con ataques de linkage y auxiliares.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Riesgo reidentificación, utilidad, DP parameters, coste.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 41. Forense cloud (`cloud_forensics`)
**Pregunta:** ¿Qué estrategia de preservación produce timeline completo entre control plane, identidad y datos?
**Hipótesis de trabajo:** Tenant de prueba con audit logs, snapshots y eventos sembrados.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Completitud, hash integrity, ingest lag, reproducibilidad.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 42. Red Team de IA (`ai_red_team`)
**Pregunta:** ¿Qué pruebas adversariales revelan rutas de exfiltración y abuso de herramientas en agentes?
**Hipótesis de trabajo:** Agente aislado, RAG sintético, herramientas mock y canaries.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Attack success, leakage, tool misuse, severidad.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 43. PKI y HSM (`pki_hsm`)
**Pregunta:** ¿Qué proceso de rotación/revocación mantiene confianza durante fallos y compromiso de CA?
**Hipótesis de trabajo:** PKI de laboratorio con certificados y HSM simulado.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Tiempo revocación, cobertura, fallos cliente, recuperación.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 44. Criptografía poscuántica (`post_quantum_crypto`)
**Pregunta:** ¿Qué plan híbrido mantiene interoperabilidad y resistencia a downgrade durante migración?
**Hipótesis de trabajo:** Prototipo TLS/PKI de laboratorio con implementaciones PQC verificadas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Latencia, tamaño, interoperabilidad, fallos downgrade.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 45. Continuidad de negocio (`business_continuity`)
**Pregunta:** ¿Qué secuencia de recuperación cumple RTO/RPO ante compromiso simultáneo de identidad y backup?
**Hipótesis de trabajo:** Ejercicio tabletop + restore aislado con dependencias sembradas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** RTO/RPO observados, integridad, decisiones, dependencias omitidas.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 46. Seguridad de bases de datos (`database_security`)
**Pregunta:** ¿Qué controles de autorización y consulta reducen exposición de datos y abuso de consultas?
**Hipótesis de trabajo:** DB de prueba multi-tenant con permisos y entradas sintéticas.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Acceso indebido, consultas inseguras, rendimiento, falsos positivos.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.

### 47. Investigación de vulnerabilidades (`vulnerability_research`)
**Pregunta:** ¿Qué combinación de fuzzing y análisis estático encuentra fallos reproducibles con menor coste?
**Hipótesis de trabajo:** Parser propio con defectos sembrados y corpus controlado.
**Diseño mínimo:** definir baseline y dataset/topología/controlado, variar una dimensión principal, ejecutar pruebas positivas/negativas/límite, repetir y conservar artefactos con hashes.
**Métricas candidatas:** Unique crashes, coverage, reproducibilidad, tiempo triage.
**Entregables:** protocolo, corpus/dataset, scripts, logs, análisis, incertidumbre, amenazas a validez, conclusiones limitadas y plan de reproducción.


## Criterios de madurez
- M1: mapa temático y fuentes localizadas.
- M2: síntesis técnica específica con fuentes y límites.
- M3: protocolo preregistrado y revisión crítica de literatura.
- M4: experimento ejecutado, analizado y reproducible internamente.
- M5: revisión independiente y reproducción externa.
La agenda no otorga madurez por sí misma.