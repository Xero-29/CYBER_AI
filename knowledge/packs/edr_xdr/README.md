# EDR y XDR — Guía de dominio

**ID:** `edr_xdr` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Diseña cobertura de detección y respuesta en endpoints, servidores, identidades, red y cloud. EDR/XDR agrega telemetría y acciones; puede causar impacto operacional si aísla equipos o mata procesos. Las acciones de respuesta requieren autoridad, alcance y reversibilidad.

## Competencias
- Comprender sensores, agentes, telemetría, consola y backend.
- Analizar procesos, árbol de ejecución, módulos, archivos, red y persistencia.
- Correlacionar endpoint con identidad, correo, DNS y cloud.
- Diseñar reglas de detección, exclusiones y prevención.
- Evaluar tamper protection, aislamiento y rollback.
- Gestionar alertas, evidencias, cuarentena y respuesta coordinada.
- Medir cobertura, falsos positivos, rendimiento y privacidad.

## Controles
- Agentes con tamper protection y política gestionada.
- Consola con RBAC, MFA y registro de acciones.
- Exclusiones limitadas, justificadas y con vencimiento.
- Actualizaciones firmadas y despliegue gradual.
- Telemetría con redacción y retención.
- Aislamiento de endpoint solo con autorización de incident commander.
- Integración SIEM con IDs correlacionables.
- Pruebas de impacto sobre rendimiento y aplicaciones críticas.

## Metodología
1. Inventariar sistemas, SO, criticidad y cobertura de agentes.
2. Revisar políticas, exclusiones, versiones y salud de sensores.
3. Mapear detecciones a ATT&CK y fuentes de telemetría.
4. Probar reglas con eventos sintéticos y benignos.
5. Medir falsos positivos y pérdida de telemetría.
6. Ensayar aislamiento y rollback en endpoints de laboratorio.
7. Verificar integración SIEM, alertas y auditoría.
8. Revisar privacidad, acceso y retención.
9. Mejorar cobertura según incidentes y cambios.

## Laboratorio
Endpoints virtuales desechables con EDR de prueba y eventos sintéticos. Simular detección, triage y aislamiento controlado; comprobar restauración de conectividad y registro de operador.

## Evaluación
Cobertura de activos medida, reglas versionadas, exclusiones acotadas, telemetría fiable y acciones de respuesta auditables.

## Referencias
MITRE ATT&CK, NIST SP 800-61, CIS Controls, vendor EDR/XDR hardening guides y Sigma.

## Instrucciones para agentes IA
No aísles endpoints ni mates procesos. Recomienda acciones y su impacto; el operador autorizado decide.