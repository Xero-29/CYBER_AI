# Investigación técnica: Threat hunting y análisis proactivo

**ID:** threat_hunting · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación sobre telemetría propia pendiente.

## Modelo
Threat hunting es búsqueda estructurada de actividad no detectada por controles existentes. Parte de hipótesis basada en threat intel, arquitectura, incidentes, exposición o gaps de detección. No es escaneo indiscriminado ni búsqueda de IOC sin contexto.

## Ciclo
1. Formular hipótesis y comportamiento esperado.
2. Identificar activos, telemetría, ventana, población y limitaciones.
3. Diseñar consultas y baseline benigno.
4. Ejecutar búsqueda pasiva y controlada.
5. Investigar anomalías, validar alternativas y descartar falsos positivos.
6. Documentar hallazgo, evidencia, confianza y respuesta aprobada.
7. Convertir aprendizaje en detección y repetir para medir mejora.

## Fuentes y analítica
Correlacionar process, identity, DNS, proxy, firewall, EDR, cloud audit, email, network flow y application logs. ATT&CK ayuda a organizar hipótesis; ATT&CK Data Sources está deprecado desde v18, por lo que nuevas analíticas deben usar Detection Strategies/Analytics y telemetría vigente. D3FEND puede relacionar contramedidas, pero no prioriza ni prueba eficacia por sí solo.

## Técnicas analíticas
Rare event analysis, frequency/time baselines, graph traversal, sequence analytics, user/entity behavior, process lineage, DNS patterns, auth anomalies, lateral movement hypotheses y cloud control-plane changes. Controlar base rate y selección: una anomalía no es necesariamente amenaza.

## Métricas
Hypothesis yield, validated finding rate, false positive rate, time per hunt, telemetry coverage, new detections created, detection regression and recurrence. Reportar hunts negativos como evidencia de alcance limitado, no como prueba de ausencia de adversario.

## Laboratorios
Dataset sintético de endpoint/network/identity, ATT&CK-aligned behavior, anomalías benignas, timestamps retrasados y ruido. Probar hipótesis con consultas reproducibles, baselines y resultados esperados.

## Fuentes
- MITRE ATT&CK: https://attack.mitre.org/
- MITRE D3FEND: https://d3fend.mitre.org/
- NIST SP 800-137: https://doi.org/10.6028/NIST.SP.800-137
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3

**Límite:** el hunting depende de cobertura y calidad de telemetría; no permite demostrar ausencia de intrusión.
