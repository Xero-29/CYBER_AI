# Investigación técnica: Fundamentos de ciberseguridad

**ID:** foundations · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Revisión experta pendiente.

## Marco conceptual
La ciberseguridad protege activos, servicios, procesos y personas frente a fallos y acciones adversarias. La unidad de análisis no es el dispositivo aislado: es el sistema socio-técnico formado por activos, identidades, software, datos, proveedores, instalaciones, procesos y decisiones. Distinguir amenaza, vulnerabilidad, exposición, probabilidad, impacto, riesgo inherente, controles y riesgo residual.

## Principios y propiedades
- Confidencialidad: acceso solo a sujetos autorizados.
- Integridad: modificación solo autorizada y detectable.
- Disponibilidad: servicio utilizable dentro de requisitos.
- Autenticidad, responsabilidad, trazabilidad, privacidad y resiliencia complementan CIA.
- Mínimo privilegio, separación de funciones, deny-by-default, defensa en profundidad, secure defaults y recuperación.
- Seguridad y safety se relacionan, pero no son intercambiables.

## Sistemas, redes y datos
Dominar arquitectura CPU/memoria/procesos, kernel/userland, filesystem, virtualización, redes TCP/IP, DNS, identidad, autenticación, autorización, criptografía, bases de datos, APIs, cloud y sistemas distribuidos. Para cada activo documentar propietario, clasificación, ubicación, dependencias, ciclo de vida, interfaces, exposición y evidencia.

## Gestión de riesgo
NIST CSF 2.0 organiza resultados en Govern, Identify, Protect, Detect, Respond y Recover. Se usa para perfilar resultados y comunicar riesgo; no prescribe por sí mismo una implementación técnica. CIS Controls v8.1 proporciona safeguards priorizados; NICE 2.2.0 describe work roles, competency areas y tareas/conocimientos/habilidades. No convertir marcos de resultados o competencias en una certificación automática.

## Modelado de amenazas
Describir sistema, activos, actores, trust boundaries y flujos. Enumerar amenazas mediante STRIDE, attack trees y misuse cases. Estimar riesgo con método documentado; declarar supuestos, incertidumbre, apetito, controles y residual. Una puntuación no sustituye juicio ni contexto.

## Método de aprendizaje y evaluación
Para cada concepto, exigir definición precisa, modelo, ejemplo, contraejemplo, amenaza, mitigación, prueba y limitación. Evaluar con preguntas aplicadas, lectura de diagramas, análisis de logs, diseño de controles y ejercicios de explicación. Métricas: precisión conceptual, tasa de resolución, transferencia a escenarios nuevos, falsos positivos y consistencia entre evaluadores.

## Laboratorios
Crear red local segmentada, usuarios/roles, servidor, API, base de datos y telemetría. Simular errores de autorización, exposición de servicio, mala configuración y recuperación. Mantener snapshots, datos sintéticos, alcance y destrucción del entorno.

## Fuentes
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29
- NICE Framework v2.2.0: https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1
- MITRE ATT&CK: https://attack.mitre.org/

**Límite:** síntesis inicial; no acredita que cada estándar se haya leído íntegramente ni que el currículo sea exhaustivo.
