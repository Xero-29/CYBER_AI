# Seguridad de aplicaciones — Guía de dominio

**ID:** `appsec` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Asegura el ciclo de vida de aplicaciones web y servicios, desde requisitos y diseño hasta despliegue y operación. Cubre errores de lógica, validación, sesiones, autorización, dependencias, configuración y exposición de datos. Las pruebas dinámicas deben ejecutarse en entornos autorizados, con datos sintéticos y límites de carga.

## Arquitectura y superficies críticas
Revisar navegador, frontend, API, middleware, sesiones, base de datos, caché, almacenamiento de objetos, colas, servicios externos y pipeline CI/CD. Marcar límites entre usuario anónimo, usuario autenticado, roles, administradores y servicios máquina-a-máquina. Los principales fallos aparecen en validación de entrada, codificación de salida, control de acceso, confianza en cabeceras, serialización y manejo de errores.

## Competencias específicas
- Aplicar OWASP ASVS como catálogo verificable de requisitos.
- Revisar XSS reflejado/almacenado/DOM, inyección SQL/NoSQL/command, CSRF, SSRF, traversal y deserialización insegura.
- Evaluar autenticación, recuperación de cuenta, sesiones, MFA, cookies y expiración.
- Detectar IDOR/BOLA, escalada horizontal/vertical y fallos de autorización por función.
- Integrar SAST, DAST, SCA, análisis de secretos y revisión manual.
- Diseñar controles de seguridad para cabeceras, CORS, CSP, TLS y errores.

## Controles de diseño
- Validación positiva del lado servidor con esquemas explícitos; la validación cliente solo mejora UX.
- Consultas parametrizadas y APIs de acceso a datos con privilegios mínimos.
- Codificación contextual de salida y plantillas con autoescape.
- Protección CSRF para operaciones basadas en cookies; CORS no es control de autenticación.
- Sesiones con cookies Secure, HttpOnly y SameSite, rotación tras login y revocación.
- Autorización centralizada por recurso y acción, no solo por ruta o interfaz.
- Límites por usuario, IP, cuenta y operación; protección contra abuso y enumeración.
- Gestión central de secretos, dependencias fijadas y artefactos verificables.

## Metodología
1. Obtener diagrama, rutas, roles, modelos de datos y requisitos de seguridad.
2. Enumerar endpoints y operaciones sensibles; construir matriz rol-recurso-acción.
3. Revisar autenticación y autorización antes de buscar fallos de entrada.
4. Analizar código y dependencias; validar hallazgos con pruebas unitarias.
5. Ejecutar DAST en staging con cuentas de prueba y límites de tasa.
6. Correlacionar hallazgos entre SAST/DAST/SCA para reducir duplicados.
7. Demostrar impacto mínimo, sin extraer datos ni persistir acceso.
8. Proponer mitigación, prueba de regresión y responsable.
9. Repetir prueba después del cambio y conservar evidencia.

## Laboratorio seguro
Usar una aplicación deliberadamente vulnerable local, con dos usuarios ficticios y datos sintéticos. Crear pruebas de regresión para XSS, SQLi, CSRF, SSRF simulada y autorización horizontal. El ejercicio no debe apuntar a dominios externos ni exfiltrar información.

## Criterios de evaluación
Cobertura de rutas y roles, evidencia reproducible, ausencia de datos reales, falsos positivos documentados, prueba de regresión por hallazgo y riesgo residual aceptado por propietario.

## Marcos y herramientas
OWASP Top 10, OWASP ASVS, OWASP Testing Guide, CWE, Semgrep, Bandit, Ruff, ZAP y Burp Suite en laboratorio autorizado.

## Instrucciones para agentes IA
Prioriza revisión de código y pruebas locales. No propongas explotación destructiva, persistencia, evasión ni extracción de datos. Para cada hallazgo incluye precondición, componente, impacto, evidencia mínima, mitigación y test de regresión.

---

## Marco obligatorio de desarrollo experto e investigación

Este paquete se desarrolla conforme al [Estándar experto e investigación](../../EXPERT_RESEARCH_STANDARD.md). El estándar aplica a esta especialidad, no solo al currículo global.

**Estado del perfil:** estructura y mapa de evidencias definidos; el contenido técnico ampliado, la revisión integral de fuentes, los laboratorios ejecutados y la validación independiente se registran por separado. No se declara K4/K5 por la existencia de este marco.

Cada tema de esta especialidad debe desarrollarse como unidad independiente y cubrir: teoría, formalización pertinente, arquitectura, estándares versionados, implementación, análisis avanzado, seguridad adaptada al dominio, investigación, laboratorio/dataset, evaluación, Skills verificadas y trazabilidad. La matriz detallada de capas, evidencias, enfoque matemático y restricciones de laboratorio está en `knowledge/curricula/domain_curriculum.json`, dentro del perfil `appsec`.

**Madurez:** K1–K5 se asigna por tema y evidencia. Las ocho puertas G1–G8 deben mostrar estado explícito; lo no ejecutado o no revisado permanece pendiente. Las referencias descubiertas no cuentan como lectura completa y los laboratorios diseñados no cuentan como ejecutados.
