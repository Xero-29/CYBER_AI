# CYBER_AI — Atlas de conocimiento en ciberseguridad

## Objetivo
Construir una biblioteca técnica modular, profunda, trazable y utilizable offline. El repositorio contiene código, catálogos, metadatos, documentación y pruebas. Los corpus, datasets, modelos y paquetes grandes se descargan por especialidad bajo demanda y se guardan fuera de Git.

## Niveles de profundidad
- L0: orientación, vocabulario, objetivos y límites.
- L1: fundamentos, arquitectura, protocolos y conceptos.
- L2: metodología profesional, configuración segura, detección, pruebas y respuesta.
- L3: análisis experto, correlación, automatización controlada y validación.
- L4: investigación, papers, reproducción responsable y evaluación crítica.
Los niveles describen profundidad editorial, no certifican competencia automática.

## Especialidades que debe cubrir el repositorio
- **foundations — Fundamentos:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **appsec — Seguridad web y aplicaciones:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **api — Seguridad de API:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **network — Redes:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **linux — Linux y Unix:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **windows_ad — Windows y Active Directory:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **cloud — Seguridad cloud:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **containers — Contenedores y Kubernetes:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **mobile — Seguridad móvil:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **crypto — Criptografía:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **identity — Identidad y acceso:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **malware — Análisis de malware:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **forensics — Forense digital:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **incident_response — Respuesta a incidentes:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **threat_intel — Inteligencia de amenazas:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **reverse — Ingeniería inversa:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **iot_hardware — IoT y hardware:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **devsecops — DevSecOps y supply chain:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **ai_security — Seguridad de IA:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **governance — GRC, privacidad y auditoría:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **vuln_management — Gestión de vulnerabilidades:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **bug_bounty — Bug bounty autorizado:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **secure_arch — Arquitectura segura:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.
- **data_security — Seguridad de datos:** fundamentos, arquitectura, amenazas, mitigaciones, metodología, herramientas, casos, laboratorios locales, evaluación y referencias versionadas.

- **software_engineering — Ingeniería de software y calidad:** Python, packaging, pruebas, CI/CD, análisis estático y calidad de código.
- **machine_learning — Aprendizaje automático e ingeniería de IA:** PyTorch, scikit-learn, NumPy, SciPy, gestión de riesgo de IA y MITRE ATLAS.
- **hardware_security — Hardware, firmware y sistemas embebidos:** resiliencia de firmware, Linux kernel, Zephyr e IoT.
- **mathematics — Matemáticas, estadística y métodos numéricos:** álgebra lineal, estadística, probabilidad y métodos numéricos.

## Fuentes de referencia iniciales
- NIST CSF y publicaciones: https://www.nist.gov/cyberframework y https://csrc.nist.gov/publications/sp
- OWASP, ASVS, WSTG y Cheat Sheets: https://owasp.org/ y https://cheatsheetseries.owasp.org/
- MITRE ATT&CK, CWE y CAPEC: https://attack.mitre.org/ , https://cwe.mitre.org/ y https://capec.mitre.org/
- CIS Controls y Benchmarks: https://www.cisecurity.org/
- FIRST CVSS y EPSS: https://www.first.org/cvss/ y https://www.first.org/epss/
- NVD y CISA KEV: https://nvd.nist.gov/ y https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Microsoft, AWS, Google Cloud, Kubernetes, Docker, Linux, Android y Apple: documentación oficial de cada fabricante.
- Nmap, Nuclei, Semgrep, Trivy, Zeek, Suricata, Wireshark, Sigma, YARA y Velociraptor: documentación oficial de cada proyecto.
- Laboratorios locales: OWASP Juice Shop, WebGoat y DVWA.

## Plantilla obligatoria por especialidad
Cada módulo debe incluir README (alcance, objetivos, prerequisitos y límites), teoría, arquitectura, amenazas y mitigaciones, metodología reproducible, herramientas con versiones y limitaciones, laboratorios aislados, casos anonimizados, referencias con licencia, evaluaciones con respuestas razonadas y changelog.

## Calidad y trazabilidad
No basta con descargar. Registrar editor, URL canónica, versión, fecha, idioma, licencia, tamaño, SHA-256, formato, estado de extracción, clasificación, duplicados y fecha de revisión. Verificar integridad y procedencia; conservar referencias; separar hechos, inferencias, hipótesis y recomendaciones; probar recuperación con preguntas de referencia. No ingerir material pirateado, sin procedencia o con derechos dudosos.

## Descarga selectiva y modo offline
La interfaz objetivo incluye: listar áreas; simular descarga y estimar espacio; descargar un área; perfiles minimal/standard/research; verificar hashes; consultar estado y espacio; impedir red en modo offline; buscar actualizaciones sin sobrescribir versiones validadas sin confirmación. Estos comandos solo deben anunciarse como disponibles cuando estén implementados y probados.

## Seguridad de laboratorios
Solo sistemas propios, locales o expresamente autorizados. No ejecutar acciones destructivas ni habilitar persistencia, robo de credenciales o evasión automatizada. Las pruebas activas requieren aprobación humana y alcance explícito.

## Métricas de madurez
Publicar por separado recursos catalogados, descargados, verificados, ingeridos, indexados y recuperables. Marcar contenido obsoleto y revisar fuentes de vulnerabilidades mensualmente y documentación estable trimestralmente. No afirmar cobertura o conocimiento que no se haya validado.


## Estado del catálogo versionado (v1.1.0)
El catálogo contiene 28 áreas y 98 referencias. Se añadieron 44 referencias en ingeniería de software, aprendizaje automático, hardware/firmware, matemáticas y especialidades de seguridad (ASVS, WSTG, seguridad de API, SLSA, OpenSSF, SBOM, respuesta a incidentes, D3FEND y otras fuentes primarias).

**Importante:** son referencias catalogadas, no conocimiento descargado ni ingerido. Las licencias permanecen como pendientes; no se ha marcado ningún recurso como descargado o verificado. El flujo de adquisición debe comprobar licencia, procedencia, fecha, hash, tamaño y formato antes de ingestión.
