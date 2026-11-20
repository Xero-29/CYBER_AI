# Secciones de profundización — EDR y XDR

## Modelo de amenazas
Incluir agente, kernel sensor, consola, tenant, canal de actualización, telemetría, backend cloud y acciones de respuesta. Amenazas: tampering, desinstalación, exclusión abusada, bypass, falso aislamiento, credenciales de consola robadas y proveedor comprometido. Distinguir cobertura real del sensor de capacidad anunciada.

## Detección
Correlacionar proceso, parent, hash, firma, memoria, persistencia, usuario, red y contexto de amenaza. Medir sensor health, lag, eventos perdidos, reglas activas y cobertura por OS. Probar detecciones con simulaciones seguras; medir precisión y recall. Revisar exclusiones y cambios de política.

## Respuesta a incidentes
Aislar host cuando esté autorizado, preservar telemetría y memoria, bloquear hash/certificado/IOC con caducidad, revocar sesiones, recoger artefactos y reconstruir endpoint. Verificar que aislamiento no rompe servicios críticos; documentar fallback si consola o proveedor no está disponible.

## Casos prácticos
Ejecutar simulación benigna de persistencia en VM de laboratorio y verificar detección de proceso, tarea programada y conexión. Probar aislamiento, recolección de evidencia y liberación controlada. Repetir con sensor desconectado para medir gap y alerta de salud.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para MITRE ATT&CK, documentación oficial EDR, Sigma y NIST. Registrar agente, policy, motor y versión de consola.
