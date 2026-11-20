# Bug bounty y divulgación coordinada — Guía de dominio

**ID:** `bug_bounty` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Gestiona investigación de vulnerabilidades dentro de programas con alcance, reglas y autorización explícitos. Un programa público no autoriza cualquier activo, técnica, volumen o acceso a datos. El investigador debe preservar privacidad, disponibilidad y evidencia mínima; detenerse al confirmar impacto suficiente.

## Competencias
- Interpretar scope, exclusiones, safe harbor, límites de automatización y reglas de divulgación.
- Diferenciar activo autorizado, tercero, proveedor y recurso compartido.
- Identificar fallos de autenticación, autorización, lógica de negocio, APIs, web, móvil y cloud.
- Reducir falsos positivos y demostrar impacto sin extraer datos.
- Redactar informes reproducibles con precondición, evidencia y mitigación.
- Gestionar duplicados, severidad contextual, comunicación y retest.

## Controles de investigación
- Registrar programa, fecha, alcance, cuentas de prueba y límites.
- No probar DoS, spam, ingeniería social, persistencia ni acceso a datos ajenos salvo autorización expresa y específica.
- Usar cuentas y datos sintéticos; no descargar bases de datos ni secretos.
- Respetar límites de tasa, ventanas y mecanismos de exclusión.
- Detener pruebas cuando se detecte información real o impacto no previsto.
- Conservar evidencia mínima y redactar PII/credenciales.

## Metodología
1. Leer reglas y confirmar dominio, rutas, APIs, cuentas y exclusiones.
2. Crear matriz de activos y técnicas permitidas.
3. Reconocer superficie pasivamente antes de cualquier prueba.
4. Priorizar fallos de autorización y lógica de negocio con cuentas propias.
5. Validar una hipótesis con el mínimo número de solicitudes.
6. Capturar evidencia redactada, timestamps y pasos reproducibles.
7. Asignar severidad según impacto y contexto, no solo CVSS.
8. Enviar informe privado y no divulgar antes del proceso acordado.
9. Retestar corrección y cerrar el hallazgo.

## Laboratorio
Aplicación deliberadamente vulnerable local con dos tenants ficticios. Practicar IDOR, autorización de API y lógica de negocio con pruebas de regresión. No apuntar a programas reales en el laboratorio automatizado.

## Evaluación
Scope demostrado, impacto mínimo, evidencia reproducible, privacidad preservada, informe claro y retest verificable.

## Referencias
OWASP Web/API Testing Guides, CWE, CVSS, FIRST EPSS, CISA KEV y políticas oficiales de divulgación coordinada.

## Instrucciones para agentes IA
No infieras autorización a partir de un dominio o programa conocido. Si scope o permiso no están claros, limita el trabajo a análisis pasivo. No recomiendes extracción de datos, persistencia ni indisponibilidad.

## Arquitectura
Un programa de divulgación coordinada define propietario, política pública, alcance por activo, exclusiones, reglas de engagement, canal seguro, triage, severidad, SLA, coordinación con proveedores y publicación. El flujo es reporte → acuse → reproducción mínima → clasificación → asignación → corrección → retest → recompensa/divulgación. Separar activos autorizados de terceros y sistemas compartidos; documentar límites de prueba, ventanas, rate limits, datos prohibidos y canal de escalado para hallazgos críticos.
