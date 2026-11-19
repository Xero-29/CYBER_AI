# Evaluación en frío — FND-01.01

**Versión:** 1.0. **Estado:** instrumento preparado, no administrado.  
**Propósito:** comprobar transferencia de conocimiento, no memoria literal.  
**Condiciones:** 120 minutos sugeridos; sin consultar el dossier durante la resolución; se permite calculadora y papel; toda respuesta debe declarar supuestos. El evaluador debe usar variantes no publicadas si el candidato ya conoce el caso.

## Instrucciones al candidato

Resuelve los cuatro bloques. Debes enseñar, explicar, analizar y diseñar. No se aceptan listas de controles sin causalidad ni afirmaciones absolutas. Distingue hechos, supuestos, inferencias y preguntas que requieren autoridad sectorial.

## A. Enseñar — 20 puntos

Diseña una microlección de 15 minutos para un ingeniero de software que confunde privacidad con confidencialidad y resiliencia con backup.

Incluye:
1. prerrequisitos y tres objetivos observables;
2. explicación progresiva de las seis propiedades: seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia;
3. dos ejemplos que demuestren diferencias y dos contraejemplos;
4. una actividad de comprobación y criterios para detectar si el alumno solo memorizó definiciones.

## B. Explicar — 20 puntos

Una plataforma de salud cifra expedientes, usa MFA, replica datos en dos regiones y conserva logs detallados. Explica, paso a paso:
1. qué propiedades podrían mejorar con cada mecanismo;
2. qué propiedades NO quedan demostradas por esos mecanismos;
3. cómo el procesamiento excesivo de datos puede crear riesgo de privacidad sin intrusión;
4. por qué dos regiones pueden compartir una causa común de fallo;
5. qué evidencia concreta permitiría sostener afirmaciones sobre disponibilidad, privacidad y resiliencia.

Incluye un diagrama lógico textual de dependencias y al menos tres supuestos explícitos.

## C. Analizar — 30 puntos

**Caso no visto:** una empresa de agua opera un sistema de dosificación. Una actualización remota del proveedor introduce un error de configuración; el operador detecta lecturas inconsistentes. La identidad central está caída, el proceso automático sigue funcionando y el equipo local propone desactivar validaciones para recuperar rapidez. Los logs contienen identificadores de empleados y detalles operativos.

Analiza:
- activos, misión, personas y funciones esenciales;
- peligros safety, amenazas cibernéticas, fallos accidentales y causas comunes;
- propiedades afectadas y conflictos;
- dependencias de identidad, proveedor, telemetría y control local;
- incertidumbre y datos que faltan;
- opciones de contención/modo degradado;
- criterios para detener, escalar o reanudar;
- riesgos residuales y quién debe aceptarlos.

Compara al menos dos alternativas. No prescribas una maniobra física concreta: define los límites de decisión y exige la validación de ingeniería/operación competente.

## D. Diseñar — 30 puntos

Diseña una arquitectura conceptual de continuidad segura para el sistema del caso C.

Entregables:
1. requisitos verificables de seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia;
2. arquitectura y límites de confianza;
3. procedimiento de acceso local de emergencia sin convertirlo en bypass permanente;
4. telemetría con minimización, integridad, retención y acceso gobernado;
5. continuidad y recuperación incluyendo identidad, configuración, proveedores, claves y datos;
6. plan de verificación estática con casos positivos, negativos, fallo y recuperación;
7. criterios de aceptación, observabilidad y rollback;
8. riesgos residuales, supuestos y autoridad responsable.

## E. Integración y reflexión — 10 puntos

Describe un escenario en que maximizar una propiedad empeora otra. Explica qué información cambiaría tu decisión, cómo evitarías falsa precisión y qué evidencia nueva podría refutar tu diseño.

## Rúbrica y umbrales

Puntúa cada bloque de 0 a 4:
- 0: ausente o técnicamente incorrecto.
- 1: enumera conceptos sin causalidad ni contexto.
- 2: resuelve el caso básico, pero omite dependencias o límites importantes.
- 3: razonamiento correcto, contextualizado, verificable y con riesgos residuales.
- 4: integra modelos, contraejemplos, incertidumbre, alternativas, criterios de parada y evidencia; transfiere a un dominio nuevo.

Puntuación ponderada: A 20, B 20, C 30, D 30, E 10 (normalizar a 100 si se desea). Umbral de trabajo: al menos 3/4 en cada bloque y ningún error crítico. El promedio no compensa un bloque deficiente.

## Fallos críticos automáticos

- equiparar privacidad con cifrado/confidencialidad;
- equiparar safety con ciberseguridad;
- asumir que backup equivale a resiliencia;
- asumir independencia de regiones sin analizar dependencias;
- desactivar controles de seguridad/safety sin autoridad ni análisis de peligros;
- declarar riesgo bajo por falta de incidentes observados;
- presentar un diseño como validación empírica;
- no identificar a quién puede dañar el procesamiento de datos.

## Registro del evaluador

Registrar candidato/fecha/versión del instrumento, tiempo, respuestas originales, puntaje por dimensión, errores críticos, preguntas de seguimiento, evaluador y conflicto de interés. No publicar datos personales del candidato en la biblioteca. La evaluación aún no ha sido administrada.


> **Estado de versión:** este instrumento V1 queda supersedido por [FND-01-01_COLD_ASSESSMENT_V2.md](FND-01-01_COLD_ASSESSMENT_V2.md). Se detectó que sus ponderaciones sumaban 110 puntos. V2 corrige el total a 100 y añade variantes A/B/C. No usar V1 para nuevas administraciones.
