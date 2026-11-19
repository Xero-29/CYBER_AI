# Secciones de profundización — Threat hunting

## Modelo de amenazas
Partir de hipótesis sobre adversarios, TTP, activos y brechas de detección. Considerar telemetría parcial, sesgo de búsqueda, falsos positivos, cambios de entorno y adversarios que evaden reglas conocidas. Definir pregunta, alcance, ventana, fuentes, población y criterios de refutación antes de consultar.

## Detección
Construir consultas reproducibles sobre identidad, endpoint, DNS, proxy, cloud y red. Enriquecer con ATT&CK, inteligencia y contexto de activo; medir cobertura, latencia, calidad y retención. Distinguir hunting exploratorio de alerta productiva. Toda hipótesis debe producir evidencia verificable o quedar refutada/inconclusa.

## Respuesta a incidentes
Escalar hallazgos con evidencia mínima, timeline, activos, usuarios, hipótesis alternativas y confianza. Preservar consultas y resultados, coordinar contención con incident response y evitar acciones disruptivas durante exploración. Convertir patrones confirmados en detecciones con tests y control de falsos positivos.

## Casos prácticos
Hipótesis: un atacante usa PowerShell y DNS para persistencia en un entorno Windows de laboratorio. Consultar eventos de proceso, parent-child, DNS y tareas; construir timeline, buscar actividad similar y medir cobertura. Convertir hallazgo en regla Sigma y test de replay, documentando falsos positivos.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para MITRE ATT&CK, Sigma, MITRE CAR y documentación de telemetría. Mantener versión de consultas y fuentes.
