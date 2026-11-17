# Revisión de literatura inicial — SOC, SIEM y SOAR

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta
¿Qué arquitectura de logging y detección permite investigar incidentes con cobertura suficiente, integridad, retención y coste operacional controlado?

## Síntesis
NIST SP 800-92 (2006) describe infraestructura y procesos empresariales de gestión de logs, pero es antiguo y no debe confundirse con una guía actual de implementación SIEM. NIST publicó SP 800-92 Rev. 1 como borrador público inicial en octubre de 2023; NIST describe Rev. 1 como un playbook de planificación de mejoras y señala que reemplazará la guía original. El borrador debe etiquetarse como borrador, no como publicación final. NIST SP 800-61 Rev. 3 integra logging/detección dentro de la respuesta y mejora continua.

## Arquitectura a evaluar
Fuentes → transporte autenticado → normalización con esquema → almacenamiento íntegro → detección/correlación → triage → caso/acciones → métricas y retención. La calidad depende de sincronización temporal, cobertura, campos, identidad del origen, pérdida de eventos, retención, control de acceso y capacidad de consulta.

## Hipótesis / experimento (no ejecutado)
H1: un pipeline con contratos de telemetría y validación de campos reduce eventos inutilizables y tiempo de triage frente a ingestión sin control de calidad. H0: sin diferencia.
Banco: eventos sintéticos de autenticación, endpoint, red y cloud; inyectar campos ausentes, retraso, duplicados y desorden. Comparar ingestión básica con validación y dead-letter queue. Métricas: pérdida, duplicación, latencia p95, porcentaje parseado, precisión/recall de reglas, coste por GB y tiempo de triage. No conectar datos de producción.

## Brechas
Revisar el borrador Rev. 1 completo y su estado actual antes de fijar política; incorporar OpenTelemetry y formatos de eventos relevantes; probar escalabilidad, retención, inmutabilidad, control de acceso y detección ante evasión.

## Fuentes
- NIST SP 800-92 final: https://doi.org/10.6028/NIST.SP.800-92
- NIST SP 800-92 Rev. 1 initial public draft: https://doi.org/10.6028/NIST.SP.800-92r1.ipd
- NIST Log Management project: https://csrc.nist.gov/projects/log-management
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3

## Identificadores del registro de fuentes
- `NIST-SP-800-92`
- `NIST-SP-800-92R1-IPD`
- `NIST-LOG-MANAGEMENT-PROJECT`
- `NIST-SP-800-61r3`
