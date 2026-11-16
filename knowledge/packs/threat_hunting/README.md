# Threat hunting — Guía de dominio

**ID:** `threat_hunting` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito
Busca actividad adversaria que no ha generado alertas suficientes. Un hunt parte de una hipótesis falsable y termina en una conclusión, detección o brecha de telemetría. No equivale a buscar IOC de forma indiscriminada ni a ejecutar técnicas ofensivas sobre sistemas.

## Preparación y fuentes
Fuentes: EDR, Sysmon, auditd, identidad, DNS, proxy, firewall, cloud control plane, correo, aplicaciones, NDR y telemetría de procesos. Documentar cobertura, latencia, retención, huecos, normalización y permisos de consulta. Definir ventana temporal y población de activos.

## Competencias
- Formular hipótesis basadas en ATT&CK, inteligencia o anomalías.
- Traducir hipótesis en consultas reproducibles (KQL, SPL, SQL, Sigma).
- Crear baselines por rol, host, servicio y horario.
- Correlacionar identidad, proceso, red y persistencia.
- Separar comportamiento benigno raro de actividad maliciosa.
- Construir detecciones y casos de regresión a partir de resultados.
- Documentar incertidumbre y cobertura limitada.

## Metodología
1. Escribir hipótesis, TTP, activos y ventana.
2. Identificar telemetría necesaria y validar calidad.
3. Crear consulta inicial y limitar coste/volumen.
4. Establecer baseline y exclusiones justificadas.
5. Investigar anomalías con pivotes trazables.
6. Confirmar con fuentes independientes o clasificar inconcluso.
7. Preservar evidencia y escalar incidentes según proceso.
8. Convertir comportamiento confirmado en detección y test.
9. Registrar cobertura, falsos positivos y próxima revisión.

## Controles
- Consultas read-only y cuotas de recursos.
- Acceso RBAC y minimización de datos personales.
- UTC, IDs correlacionables y retención definida.
- No ejecutar acciones sobre hosts desde el proceso de hunting.
- No considerar ausencia de telemetría como ausencia de amenaza.
- Revisar consultas antes de producción y versionarlas.

## Laboratorio
Logs sintéticos de Windows/Linux, DNS y autenticación. Formular hunts para uso anómalo de PowerShell, creación de servicios, cambios de privilegio y conexiones inusuales. Validar consultas con eventos positivos y negativos conocidos.

## Evaluación
Cada hunt tiene hipótesis, consulta, ventana, cobertura, resultado, falsos positivos, evidencias y decisión de detección/seguimiento.

## Referencias
MITRE ATT&CK, Sigma, Kusto Query Language, Splunk SPL, Elastic EQL, NIST SP 800-61 y Threat Hunting Maturity Model.

## Instrucciones IA
No concluyas compromiso solo por anomalía. Indica qué datos faltan y limita consultas a la autorización y ventana indicadas.