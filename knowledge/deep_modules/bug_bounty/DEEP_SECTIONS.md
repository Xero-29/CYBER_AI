# Secciones de profundización — Bug bounty y divulgación coordinada

## Modelo de amenazas
El programa debe proteger activos, investigadores, usuarios y terceros. Amenazas: alcance ambiguo, pruebas destructivas, exfiltración excesiva, duplicados, reportes maliciosos, represalias, divulgación prematura y dependencia de plataformas. Delimitar dominios, cuentas, datos, horarios, técnicas prohibidas, rate limits y proceso de escalado.

## Detección
Triage de reportes por reproducibilidad, impacto, activo afectado, precondición, evidencia y duplicidad. Correlacionar hallazgos con logs defensivos y backlog de vulnerabilidades. Detectar abuso del programa, pruebas fuera de alcance y exposición de datos reales. Mantener trazabilidad de tiempos de acuse, validación, remediación y comunicación.

## Respuesta a incidentes
Si el reporte indica explotación activa, escalar al equipo de incidentes; preservar evidencia, restringir acceso de prueba y coordinar mitigación. No exigir más explotación cuando el impacto ya está demostrado. Notificar a terceros afectados, acordar divulgación y retest. Proteger datos del investigador y mantener canal seguro.

## Casos prácticos
Un investigador reporta BOLA con dos cuentas de prueba y evidencia mínima. Reproducir en staging, confirmar alcance, asignar severidad contextual, corregir autorización y pedir retest. Segundo escenario: SSRF reportada contra endpoint mock; verificar que no se accede a metadata o redes reales y documentar límites de seguridad.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para ISO/IEC 29147/30111, políticas de plataformas, OWASP y CISA. Las reglas del programa deben estar publicadas y versionadas.
