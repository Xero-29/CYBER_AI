# Secciones de profundización — Seguridad web y aplicaciones

## Modelo de amenazas
Dibujar navegador, frontend, API, backend, IdP, sesiones, almacenes, colas, integraciones y operadores. Enumerar entradas controlables, objetos sensibles, acciones privilegiadas y fronteras entre tenants. Priorizar BOLA/IDOR, escalada de función, SSRF, inyección, XSS, CSRF, deserialización, abuso de lógica, carreras y supply chain. Para cada amenaza registrar rol atacante, precondición, activo, impacto y control preventivo/detectivo.

## Detección
Instrumentar autenticaciones, denegaciones, cambios de privilegio, acceso a objetos, exportaciones, errores de parser, llamadas salientes y cambios de configuración. Correlacionar request ID, sujeto, tenant, endpoint, objeto y resultado sin registrar secretos. Detectar patrones de enumeración, volumen anómalo, SSRF y abuso de sesión. Validar reglas con tráfico benigno y pruebas controladas; medir precisión, recall y falsos positivos por endpoint.

## Respuesta a incidentes
Ante explotación confirmada, preservar logs y muestras mínimas, identificar versiones y rutas afectadas, bloquear temporalmente el vector sin destruir evidencia, revocar tokens y credenciales expuestas, corregir la causa raíz y revisar exposición de datos. Desplegar fix con pruebas negativas y regresión; revisar sesiones, cachés, colas y copias. Comunicar impacto real y potencial con incertidumbre explícita.

## Casos prácticos
En una aplicación multi-tenant, un usuario modifica el identificador de un objeto y obtiene registros de otro tenant. Reproducir con datos sintéticos y dos roles; confirmar si el servidor autoriza por objeto y tenant, no solo por sesión. Añadir test de autorización en API y UI, revisar endpoints hermanos y exportaciones, y verificar que los logs permiten atribuir actor, objeto y tenant sin filtrar PII.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para ASVS 5.0.0, WSTG, OWASP Top 10 y NIST SSDF. Fijar la versión de cada requisito y registrar pruebas, no solo el enlace al estándar.
