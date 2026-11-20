# Respuesta a incidentes — Guía de dominio

**ID:** `incident_response` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Coordina preparación, detección, análisis, contención, erradicación, recuperación y aprendizaje. El objetivo es limitar daño y restaurar operaciones con seguridad, no ejecutar acciones impulsivas. La respuesta debe integrar SOC, TI, legal, privacidad, negocio, comunicaciones y proveedores.

## Tipos de incidente
Preparar escenarios de ransomware, compromiso de identidad, fuga de datos, malware, abuso cloud, compromiso de proveedor, DDoS, insider, pérdida de dispositivo y vulnerabilidad explotada. Clasificar por impacto en confidencialidad, integridad, disponibilidad, seguridad física, privacidad y obligaciones regulatorias.

## Competencias específicas
- Definir severidad, roles, escalamiento y autoridad de decisión.
- Construir línea temporal y alcance con evidencia.
- Preservar logs y sistemas críticos antes de cambios irreversibles.
- Elegir contención proporcional y reversible.
- Erradicar persistencia, credenciales comprometidas y rutas de acceso.
- Recuperar desde fuentes verificadas y monitorizar reinfección.
- Gestionar comunicación, notificación y cadena de custodia.
- Ejecutar postmortem sin culpa y convertir hallazgos en controles.

## Preparación y controles
- Playbooks por escenario, contactos y suplencias.
- Inventario de activos críticos, dependencias y propietarios.
- Logging centralizado con retención y acceso protegido.
- Backups aislados, inmutables cuando sea viable y restauraciones probadas.
- Cuentas break-glass controladas y MFA.
- Canales de comunicación alternos y plantillas de crisis.
- Reglas de preservación de evidencia y contacto legal.
- Métricas: MTTD, MTTA, MTTC, MTTR, alcance, impacto y recurrencia.

## Metodología operativa
1. Detectar, validar y registrar el incidente con identificador único.
2. Asignar incident commander y equipo según severidad.
3. Establecer hechos confirmados, hipótesis y lagunas.
4. Preservar evidencia volátil y establecer línea temporal.
5. Determinar alcance: identidades, sistemas, datos, proveedores y regiones.
6. Seleccionar contención con impacto y reversibilidad documentados.
7. Erradicar causa raíz y cerrar rutas de acceso.
8. Recuperar por fases, validar integridad y aumentar monitorización.
9. Evaluar obligaciones de notificación con asesoría competente.
10. Realizar revisión posterior, acciones y pruebas de cierre.

## Laboratorio seguro
Ejercicio de mesa con ransomware simulado sobre archivos sintéticos y cuentas ficticias. Practicar decisiones de aislamiento, comunicación, preservación, restauración y verificación. No cifrar equipos reales ni desconectar sistemas productivos durante el ejercicio.

## Criterios de evaluación
Roles activados a tiempo, decisiones registradas, evidencia preservada, alcance justificado, recuperación validada, comunicaciones coordinadas y acciones con propietario/plazo.

## Marcos y fuentes
NIST SP 800-61 Rev. 3, CISA Incident Response Playbooks, FIRST CSIRT Services Framework, MITRE ATT&CK y ISO/IEC 27035.

## Instrucciones para agentes IA
No aísles, apagues, borres ni restaures activos por iniciativa propia. Recomienda opciones con impacto y reversibilidad; la autoridad humana decide. Separa hechos, hipótesis y recomendaciones.

## Arquitectura
El sistema de respuesta conecta fuentes de señal (endpoint, identidad, red, cloud, aplicaciones y terceros), colectores, SIEM/casos, equipo de guardia, responsables de negocio, asesoría legal/privacidad y capacidades de contención/recuperación. Separar canal de mando fuera de banda del entorno potencialmente comprometido. Definir quién puede aislar endpoints, revocar sesiones, bloquear indicadores, preservar evidencia y restaurar servicios; cada acción debe tener autorización, impacto conocido, reversibilidad y registro. La arquitectura contempla dependencias críticas, comunicaciones degradadas y continuidad durante indisponibilidad del plano principal.

## Controles
Mantener plan aprobado, roles y suplencias, contactos fuera de banda, inventario de activos críticos, playbooks versionados, sincronización horaria y retención de logs. Preservar evidencia antes de cambios destructivos cuando sea viable; contener proporcionalmente, documentar decisiones y cadena de custodia. Probar backups y restauración, validar integridad antes de reconectar, rotar secretos comprometidos y revisar persistencia. Toda excepción de contención debe tener propietario, justificación, vencimiento y monitoreo compensatorio.
