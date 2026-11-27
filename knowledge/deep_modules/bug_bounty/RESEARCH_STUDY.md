# Investigación técnica: Bug bounty y divulgación coordinada de vulnerabilidades

**ID:** bug_bounty · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de programas reales pendiente.

## Gobernanza y alcance
Un programa de bug bounty es un canal controlado de investigación externa, no una autorización general para atacar cualquier activo de la organización. Publicar scope exacto, activos excluidos, tipos de prueba, cuentas de prueba, datos prohibidos, límites de disponibilidad, reglas de safe harbor, método de reporte, tiempos de respuesta, pagos, duplicados, severidad y criterios de cierre. Mantener inventario y propietario de cada activo.

## Investigación responsable
El investigador debe validar autorización, scope, reglas y ventana; minimizar impacto, no acceder a datos ajenos, no persistir, no exfiltrar y detenerse cuando se confirme exposición sensible. Reportar evidencia mínima reproducible, precondiciones, impacto, versión, request/response sanitizados y pasos de mitigación. No exigir pagos fuera de programa.

## Triage
Deduplicar, reproducir en entorno seguro, confirmar activo/versión, validar impacto, distinguir vulnerabilidad de hardening issue, asignar severidad y responsable, coordinar divulgación y retest. Evitar cerrar como informativo sin explicación. Registrar timeline y comunicación.

## Métricas
Tiempo a primera respuesta, tiempo a triage, tiempo a remediación, reportes válidos, duplicados, severidad, recurrencia, activos cubiertos, investigadores activos y calidad de feedback. Pagar por severidad no debe incentivar pruebas destructivas.

## Laboratorio
Portal de disclosure simulado, app vulnerable propia, scope y exclusions, test accounts, workflow de triage y retest. Evaluar que el programa no acepte pruebas fuera de scope ni datos personales reales.

## Fuentes
- OWASP Vulnerability Disclosure Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html
- CISA Vulnerability Disclosure Policy resources: https://www.cisa.gov/
- OWASP WSTG: https://wstg.owasp.org/
- NIST SP 800-115: https://doi.org/10.6028/NIST.SP.800-115

**Límite:** política y safe harbor dependen de jurisdicción; revisión legal antes de publicar programa.
