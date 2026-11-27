# Guía del evaluador — FND-01.01

**Acceso:** evaluadores. **Estado:** guía de corrección conceptual; no sustituye revisión independiente.  
**Instrumento relacionado:** `FND-01-01_COLD_ASSESSMENT_V1.md`.

## A. Enseñar — elementos esperados

Una respuesta competente no empieza con definiciones aisladas: fija sistema, misión, sujetos, datos, funciones y contexto. Explica progresivamente:
- seguridad: protección frente a compromisos/eventos adversos;
- safety: control de peligros y daños físicos/ambientales;
- privacidad: problemas para individuos/grupos por acciones de datos;
- confiabilidad: cumplimiento de una función especificada durante condiciones/horizonte;
- disponibilidad: función utilizable por población en ventana/condiciones;
- resiliencia: anticipar, resistir, degradar, recuperar y adaptar funciones esenciales.

Debe explicar que las propiedades se solapan sin ser equivalentes. Ejemplos fuertes: cifrado correcto con recolección desproporcionada; servicio con uptime alto pero operación peligrosa; backup no restaurable; fail-closed que bloquea una función vital. Comprobar transferencia mediante caso nuevo, no repetir definiciones.

## B. Explicar — mecanismo y evidencia

- Cifrado puede apoyar confidencialidad en reposo/tránsito, no autorización, minimización ni legitimidad del tratamiento.
- MFA puede elevar confianza de autenticación, no disponibilidad del IdP ni autorización correcta.
- Replicación puede reducir ciertos fallos, no fallos correlacionados de identidad, proveedor, DNS, plano de control, configuración o región.
- Logs pueden apoyar detección/accountability, pero aumentan superficie de datos; requieren minimización, acceso, integridad, reloj, retención y cadena de custodia.
- Disponibilidad requiere SLO/función/población/ventana y medición representativa.
- Privacidad requiere mapa de acciones de datos, finalidad, población, impactos y medidas; el cifrado no resuelve el riesgo del uso.
- Resiliencia requiere ensayos de restauración y validación de integridad, identidad, claves, configuración y dependencias.

La explicación debe separar mecanismo, propiedad, supuesto y evidencia.

## C. Analizar — respuesta esperada

Debe distinguir al menos:
- peligro: dosificación incorrecta puede dañar personas/ambiente;
- fallo accidental: error de configuración;
- amenaza adversarial: posible compromiso de proveedor/actualización, sin asumirlo como hecho;
- incertidumbre: lecturas inconsistentes, causa y estado real desconocidos.

No se debe ordenar desactivar validaciones. Una respuesta fuerte propone congelar cambios, preservar evidencia, pasar a un modo seguro previamente aprobado, verificar mediciones por fuente independiente, activar procedimiento local autorizado y escalar a ingeniería/operación safety. La decisión operacional concreta corresponde a responsables sectoriales con análisis de peligros.

Debe considerar que la caída de identidad afecta trazabilidad/autorización, que el proveedor es dependencia común, y que logs identificables requieren acceso/retención controlados. Comparar mantener el proceso en modo degradado aprobado frente a detener o aislar funciones según el análisis de peligros; justificar con datos y límites.

## D. Diseñar — propiedades convertidas en requisitos

Ejemplos:
- Safety: cualquier entrada fuera de rango o inconsistente conduce a un estado definido en el análisis de peligros, validado por autoridad competente.
- Seguridad: cambios remotos requieren origen verificado, autorización, integridad, aprobación y rollback.
- Privacidad: logs usan identificadores mínimos; finalidad, acceso, retención y borrado quedan definidos.
- Confiabilidad: función de dosificación cumple comportamiento especificado bajo condiciones verificadas.
- Disponibilidad: funciones críticas cumplen criterios de servicio en ventana y población definidas.
- Resiliencia: el modo degradado mantiene función esencial segura y permite recuperar configuración/identidad/datos con integridad.

Arquitectura debe separar red de proveedor, administración, control y supervisión; el acceso de emergencia debe ser nominal, temporal, limitado, auditado y revisado. Si identidad central no está disponible, usar mecanismo de contingencia previamente diseñado, no cuentas compartidas ni desactivación general de controles.

Telemetría: minimizar datos personales, separar logs de seguridad y operación cuando proceda, proteger integridad, sincronizar tiempo, controlar acceso y definir retención. Recuperación debe cubrir proveedor, claves, identidades, configuración conocida-buena y verificación independiente.

Plan de pruebas: actualización inválida, identidad caída, datos contradictorios, reloj incorrecto, log alterado, pérdida de región, recuperación y rollback. No basta con “hacer pentest”.

## E. Integración

Ejemplo: fail-closed reduce acceso no autorizado pero puede interrumpir servicio esencial; fail-open mejora continuidad a costa de exposición. La decisión exige análisis contextual, modo degradado, límites de tiempo, autorización y aceptación explícita del riesgo.

## Criterios de puntuación

**4:** responde con modelos, supuestos, dependencias, alternativas, incertidumbre, criterios de parada, métricas y evidencia; no hay fallos críticos.  
**3:** respuesta técnicamente correcta y suficientemente completa; omisiones menores no alteran la decisión.  
**2:** respuesta parcial; faltan dependencias, evidencia o trade-offs relevantes.  
**1:** enumera controles o definiciones, pero no demuestra causalidad.  
**0:** ausencia o errores conceptuales fundamentales.

No otorgar 4 por extensión o sofisticación verbal. Exigir que el candidato justifique por qué cada evidencia demuestra la propiedad reclamada y qué la refutaría.

## Límites de la guía

Esta guía es un patrón de corrección inicial elaborado por el autor del material. No es una clave validada externamente. Una revisión independiente debe comprobar que no introduce sesgos, que los criterios son adecuados para el dominio y que los casos evalúan las competencias declaradas.
