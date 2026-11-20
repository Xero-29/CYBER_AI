# Secciones de profundización — SOC y SIEM

## Modelo de amenazas
Modelar fuentes, agentes, collectors, transporte, parser, almacenamiento, reglas, casos, SOAR y analistas. Amenazas: telemetría incompleta, parser corrupto, pérdida de eventos, manipulación de reglas, cuenta privilegiada abusada, alert fatigue y SIEM comprometido. Incluir integridad y disponibilidad del propio plano de monitorización.

## Detección
Definir casos de uso con fuente, campos obligatorios, lógica, ventana, severidad, contexto, excepción y evidencia. Normalizar identidad/activo/tiempo; medir cobertura y latencia por fuente. Validar con replay de logs y simulaciones benignas. Detectar desactivación de logging, gaps de ingestión, cambios no aprobados y consultas anómalas de analistas.

## Respuesta a incidentes
Crear caso con evidencia preservada, enriquecer contexto, asignar responsable y escalar según impacto. Las acciones SOAR deben tener allowlist, aprobación, timeout y rollback. Ante SIEM comprometido, usar fuente alternativa y verificar integridad de reglas, índices y cuentas. Registrar cada acción automática y humana.

## Casos prácticos
Ingerir logs sintéticos de autenticación, endpoint y DNS; crear detección de password spraying y correlación de inicio de sesión anómalo. Medir falsos positivos con actividad legítima, probar caída de collector y comprobar alerta por gap. Ejecutar playbook de aislamiento solo sobre endpoint simulado.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para MITRE ATT&CK, Sigma, ECS, OpenTelemetry y NIST SP 800-92. Registrar versión de parser, regla y esquema.
