# Arquitectura segura — Guía de dominio

**ID:** `secure_arch` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Integra seguridad en arquitectura empresarial, aplicaciones, datos, identidad, infraestructura y operación. El objetivo es que controles, riesgos y requisitos formen parte del diseño y puedan verificarse en producción. Un diagrama o checklist no demuestra que los controles estén desplegados.

## Competencias
- Definir requisitos de seguridad y atributos de calidad medibles.
- Modelar límites de confianza, flujos de datos y dependencias.
- Aplicar Zero Trust, least privilege, defense in depth y fail secure.
- Diseñar segmentación, identidad, secretos, cifrado y observabilidad.
- Evaluar resiliencia, privacidad, disponibilidad y recuperación.
- Analizar decisiones mediante ADRs y excepciones de riesgo.
- Diseñar arquitectura multi-tenant y separación de funciones.

## Patrones y controles
- Autenticación centralizada y autorización por recurso/acción.
- Identidades de workload y credenciales efímeras.
- APIs con esquemas estrictos, rate limits y trazabilidad.
- Segmentación de red y egress mínimo.
- Secret manager/KMS para material sensible.
- Logs estructurados con redacción y retención.
- Backups probados, recuperación y degradación segura.
- Supply chain con SBOM, firma y procedencia.
- Separación de planos de control, datos y administración.

## Metodología
1. Definir contexto, objetivos, criticidad, actores y restricciones.
2. Dibujar contenedores, componentes, flujos y trust boundaries.
3. Clasificar datos y asignar propietario y retención.
4. Elaborar threat model STRIDE y escenarios de abuso.
5. Seleccionar controles con requisitos de aceptación.
6. Documentar ADRs, trade-offs y riesgo residual.
7. Construir prototipo y validar controles de forma automatizada.
8. Revisar resiliencia, operación, backup y recuperación.
9. Verificar despliegue real y reevaluar ante cambios.

## Laboratorio
Diseñar una plataforma multi-tenant con frontend, API, workers, base de datos y proveedor externo. Producir diagramas, ADRs, threat model, matriz de controles y pruebas de aislamiento.

## Evaluación
Cada límite de confianza tiene controles, propietario y evidencia. Los requisitos son medibles, las decisiones trazables y los riesgos residuales aceptados por autoridad competente.

## Referencias
NIST SP 800-160, NIST CSF 2.0, ISO/IEC 27001/27002, SABSA, OWASP ASVS, C4 Model y AWS/Azure Well-Architected Frameworks.

## Instrucciones para agentes IA
No declares segura una arquitectura por cumplir un patrón. Expón supuestos, fallos de diseño, compensaciones y pruebas necesarias. No conviertas diagramas en evidencia de despliegue.