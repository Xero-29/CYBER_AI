# Ingeniería de software segura — Guía de dominio

**ID:** `software_engineering` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Aplica prácticas de ingeniería para construir sistemas mantenibles, verificables y resistentes a fallos. Seguridad no es una fase final: debe integrarse en requisitos, diseño, código, pruebas, revisión, release y operación. Los cambios se prueban en entornos aislados antes de producción.

## Competencias
- Definir requisitos funcionales, no funcionales y de seguridad.
- Diseñar módulos con contratos, invariantes y límites de confianza.
- Aplicar validación de entrada, manejo de errores y autorización explícita.
- Crear pruebas unitarias, integración, propiedad, fuzz y regresión.
- Revisar concurrencia, transacciones, idempotencia y recuperación.
- Gestionar dependencias, versionado, CI/CD y migraciones.
- Diseñar observabilidad sin filtrar secretos.
- Realizar code review y análisis estático.

## Controles de diseño
- Tipos/esquemas estrictos y validación en frontera.
- Errores seguros, sin stack traces ni secretos al usuario.
- Consultas parametrizadas y serialización segura.
- APIs idempotentes y operaciones con límites.
- Configuración externa validada y secretos fuera del código.
- Dependencias fijadas y artefactos con procedencia.
- Test de regresión para cada fallo corregido.
- Migraciones reversibles y backups antes de cambios de esquema.

## Metodología
1. Definir criterios de aceptación y escenarios de abuso.
2. Crear diseño modular y ADRs.
3. Implementar cambios pequeños y revisables.
4. Añadir tests positivos, negativos y de límites.
5. Ejecutar lint, SAST, SCA y pruebas automatizadas.
6. Revisar permisos, secretos, logs y errores.
7. Construir artefacto reproducible y SBOM.
8. Desplegar gradualmente con monitorización y rollback.
9. Medir defectos, deuda técnica y recurrencia.

## Laboratorio
Servicio API local con autenticación y base de datos. Añadir una función de permisos, testear IDOR y corregir con una prueba de regresión. Simular migración y rollback con datos sintéticos.

## Evaluación
Código revisable, pruebas repetibles, cobertura de errores, dependencias fijadas, cambios reversibles y telemetría segura.

## Referencias
NIST SSDF, OWASP SAMM, CWE, SEI CERT Coding Standards, Google Engineering Practices y The Twelve-Factor App.

## Instrucciones para agentes IA
No modifiques archivos ajenos al alcance. No afirmes que una prueba pasó sin ejecutarla. Mantén cambios pequeños, explica invariantes y añade tests de regresión.