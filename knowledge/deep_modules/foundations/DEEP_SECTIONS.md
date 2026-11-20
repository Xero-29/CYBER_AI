# Secciones de profundización — Fundamentos de ciberseguridad

## Modelo de amenazas
Modelar el sistema como activos, identidades, procesos, datos, servicios y proveedores conectados por flujos y límites de confianza. Identificar adversarios externos, insiders, errores operativos y fallos de dependencia. Aplicar STRIDE a componentes y flujos; complementar con árboles de ataque para objetivos de negocio. Registrar capacidad, oportunidad, precondiciones, impacto, controles existentes e incertidumbre. No confundir amenaza con vulnerabilidad ni puntuación con riesgo residual.

## Detección
Definir telemetría mínima por capa: autenticación y autorización, cambios de configuración, procesos, conexiones, DNS, API, acceso a datos, administración cloud y estado de backups. Normalizar identidad de activo, sujeto, tiempo, acción y resultado. Medir cobertura y latencia de sensores antes de interpretar ausencia de alertas. Correlacionar eventos con contexto de activo y criticidad; documentar falsos positivos, falsos negativos y retención.

## Respuesta a incidentes
Preparar responsables, canal fuera de banda, autoridad de contención y criterios de escalado. Clasificar el incidente por alcance y servicios afectados; preservar evidencia y línea temporal; contener de forma proporcional; erradicar causa y persistencia; recuperar desde fuentes verificadas; validar integridad y monitorizar recurrencia. Registrar decisiones, aprobaciones, impacto, comunicaciones y lecciones aprendidas.

## Casos prácticos
Escenario: una cuenta de servicio expuesta permite consultar una API interna y extraer datos de prueba. El ejercicio debe trazar la credencial, identificar permisos excesivos, demostrar qué registros permiten detectar el acceso, revocar sesiones y secreto, comprobar ausencia de persistencia y restaurar el servicio. Variar el ejercicio con proveedor comprometido y error de configuración. Evidencia: timeline, consultas, decisiones y prueba de regresión.

## Referencias
La bibliografía primaria, versiones y límites de revisión están en [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes). Referencias base: NIST CSF 2.0, CIS Controls v8.1, NICE Framework y MITRE ATT&CK. Cada control debe enlazarse con versión y resultado verificable; la existencia de un marco no prueba implementación.
