# Investigación técnica: Respuesta a incidentes y recuperación

**ID:** incident_response · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 · **Ejercicio operacional:** pendiente.

## Modelo
La respuesta a incidentes es un ciclo continuo de preparación, detección, análisis, contención, erradicación, recuperación y aprendizaje, integrado en gestión de riesgo. No comienza cuando se declara un incidente: inventario, telemetría, identidades, backups, contactos, autoridad de decisión y ejercicios determinan su eficacia. NIST SP 800-61 Rev. 3 (abril 2025) sustituye Rev. 2 y alinea respuesta con CSF 2.0; Rev. 2 debe quedar como referencia histórica.

## Preparación
- Definir taxonomía de eventos/incidentes, severidad, impacto y umbrales de declaración.
- Asignar autoridad, RACI, contactos 24/7, comunicaciones fuera de banda, legal, privacidad, dirección, proveedores y reguladores.
- Mantener playbooks para ransomware, compromiso de identidad, cloud, exfiltración, malware, DDoS, supply chain, insider, OT y pérdida de datos.
- Centralizar telemetría con sincronización temporal, retención, control de acceso y protección contra alteración.
- Mantener herramientas forenses, almacenamiento de evidencia, cadena de custodia, imágenes limpias y procedimientos de adquisición.
- Probar backups, credenciales break-glass y capacidad de operar si correo, IdP o SIEM están comprometidos.

## Detección y análisis
Correlacionar EDR, identidad, DNS, proxy, firewall, cloud control plane, correo, aplicaciones, endpoint, red y logs OT según contexto. Evaluar alertas por fidelidad, contexto, prevalencia, activo, identidad, criticidad y comportamiento.

Cada caso registra timestamp normalizado, fuente, entidad, alcance, evidencia, hipótesis, confianza, acciones, analista y cadena de custodia. Separar hecho observado de inferencia y atribución. MITRE ATT&CK ayuda a describir comportamiento, pero no sustituye evidencia ni enumera todos los ataques.

## Contención, erradicación y recuperación
- Contener proporcionalmente: aislar host, revocar tokens, bloquear rutas, deshabilitar cuenta o restringir servicio tras valorar impacto y continuidad.
- Preservar evidencia antes de cambios destructivos cuando sea viable; documentar excepción si la seguridad exige actuar primero.
- Erradicar persistencia, credenciales comprometidas, tareas, artefactos, accesos externos y causa raíz; no limitarse a borrar malware.
- Recuperar desde fuentes confiables, rotar secretos, validar integridad y monitorizar reinfección.
- Confirmar servicio, integridad de datos, controles, monitoreo y aceptación del propietario antes de cerrar.
- En OT/sistemas físicos, coordinar con safety y operaciones; no aplicar aislamiento automático sin análisis del proceso.

## Forense y evidencia
Cadena de custodia: identificador único, origen, custodio, fecha/hora UTC, método, herramienta/versión, hash, almacenamiento, transferencias y motivo de acceso. Capturar volatile data cuando sea necesario y autorizado. Trabajar sobre copias verificadas; preservar originales. Registrar adquisición y limitaciones de herramientas.

## Playbook mínimo
1. Triage y validación del evento.
2. Identificación de activo, dueño, criticidad y alcance.
3. Declaración y asignación de incident commander.
4. Preservación de evidencia.
5. Hipótesis y cronología.
6. Contención aprobada y comunicación.
7. Erradicación y recuperación con validación.
8. Retest y monitoreo reforzado.
9. Reporte, notificación y revisión post-incidente.
10. Actualización de detecciones, controles, Skills y formación con aprobación.

Cada playbook debe incluir triggers, roles, comandos aprobados, precondiciones, impacto, criterios de escalamiento, rollback, comunicaciones y evidencia esperada.

## Métricas y ejercicios
MTTD/MTTA/MTTC/MTTR deben definirse consistentemente; medir tiempo hasta revocación y contención, cobertura de logs, alertas con evidencia suficiente, falsos positivos, tiempo de restauración frente a RTO y pérdida frente a RPO, reincidencia y acciones correctivas cerradas. Ejecutar tabletop, simulación técnica y recuperación completa con observadores y objetivos medibles. No optimizar solo MTTR: una contención rápida que destruye evidencia o afecta safety puede empeorar el resultado.

## Fuentes
- NIST SP 800-61 Rev. 3 (2025): https://doi.org/10.6028/NIST.SP.800-61r3
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- MITRE ATT&CK: https://attack.mitre.org/
- CISA Cybersecurity Advisories: https://www.cisa.gov/news-events/cybersecurity-advisories

**Estado de evidencia:** página oficial y abstract de NIST Rev. 3 inspeccionados. Los playbooks son un marco de trabajo; no se han ejecutado ejercicios ni validado tiempos de recuperación.
