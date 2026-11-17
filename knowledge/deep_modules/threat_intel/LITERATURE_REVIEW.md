# Revisión de literatura inicial — Inteligencia de amenazas

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta
¿Cómo convertir inteligencia de amenazas en hipótesis defensivas verificables, con contexto y trazabilidad, evitando tratar ATT&CK como una lista exhaustiva de amenazas o como prueba de atribución?

## Síntesis
MITRE ATT&CK es una base de conocimiento de tácticas y técnicas adversarias basada en observaciones del mundo real. A la fecha de corte, la versión vigente indicada por MITRE es ATT&CK v20.1 (13-10-2026). La release v18 (octubre de 2025) cambió el modelo defensivo: reemplazó detections por Detection Strategies y Analytics y deprecó Data Sources. Por tanto, documentación o reglas que dependan de la página antigua de Data Sources deben migrarse y versionarse; esa página queda solo como referencia histórica. La distribución STIX versionada facilita consumir contenido estructurado, pero una coincidencia de técnica no prueba que un actor concreto haya ejecutado esa técnica.

## Flujo analítico
Requisitos de inteligencia → colección autorizada → normalización/validación → enriquecimiento → análisis de confiabilidad y contexto → hipótesis → difusión con confianza/limitaciones → feedback. Registrar fuente original, timestamp, expiración, confianza, TLP/compartición, deduplicación y relación entre observación e inferencia.

## Hipótesis / experimento (no ejecutado)
H1: correlacionar eventos sintéticos con ATT&CK Detection Strategies y analítica específica mejora la cobertura de detección frente a reglas etiquetadas solo con técnica. H0: no hay diferencia.
Banco: telemetría sintética mapeada a un subconjunto de técnicas, versión fija ATT&CK v20.1 y un SIEM local. Comparar mapeo technique-only con strategy/analytics; medir recall, precision, falsos positivos por endpoint-día, latencia, cobertura de fuentes y esfuerzo de mantenimiento. No usar IOC activo de terceros como blanco.

## Brechas
Leer ATT&CK Data Model y Detection Strategies en versión fijada; estudiar STIX/TAXII y calidad de feeds; incluir evaluación temporal de inteligencia caducada, sesgo de fuentes y falsos negativos. No realizar atribución sin evidencia multi-fuente.

## Fuentes
- MITRE ATT&CK Version History: https://attack.mitre.org/resources/versions/
- MITRE ATT&CK October 2025 release notes: https://attack.mitre.org/resources/updates/updates-october-2025/
- MITRE ATT&CK STIX data: https://github.com/mitre-attack/attack-stix-data

## Identificadores del registro de fuentes
- `MITRE-ATTACK-VERSION-HISTORY`
- `MITRE-ATTACK-V18-RELEASE`
- `MITRE-ATTACK-STIX-DATA`
