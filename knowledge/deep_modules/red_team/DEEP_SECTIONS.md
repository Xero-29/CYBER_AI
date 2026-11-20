# Secciones de profundización — Red team

## Modelo de amenazas
Definir objetivo de ejercicio, activos autorizados, adversario simulado, reglas, exclusiones, ventanas, terceros y límites de impacto. Modelar rutas de ataque como hipótesis, no como permiso implícito. Amenazas operativas: alcance accidental, persistencia, impacto en producción, exposición de datos y abuso de infraestructura de mando.

## Detección
Alinear cada técnica simulada con fuentes de telemetría, detecciones esperadas y criterios de observación. Medir si SOC detecta, clasifica y responde; registrar cobertura ATT&CK, tiempo, falsos positivos y puntos ciegos. Evitar medir éxito solo por acceso alcanzado; la calidad defensiva y seguridad del ejercicio son resultados centrales.

## Respuesta a incidentes
Mantener canal de emergencia y kill switch; detener inmediatamente ante impacto no previsto, datos reales, sistema safety-critical o pérdida de control. Coordinar con blue team según modalidad; preservar evidencia, cerrar cuentas temporales, retirar infraestructura y verificar ausencia de persistencia al finalizar.

## Casos prácticos
Ejercicio purple team en laboratorio: simular phishing benigno, ejecución controlada y movimiento entre dos VMs autorizadas. Validar alertas y respuesta en cada fase, activar parada si se supera alcance, retirar artefactos y comparar detecciones antes/después. El reporte separa objetivo, técnica, evidencia, limitación y riesgo residual.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para MITRE ATT&CK, PTES, NIST SP 800-115 y reglas de engagement. Ningún escenario autoriza pruebas fuera del alcance firmado.
