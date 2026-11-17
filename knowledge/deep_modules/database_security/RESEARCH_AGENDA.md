# Agenda de investigación: Seguridad de bases de datos

**Dominio:** `database_security` · **Objetivo:** L4 investigación · **Estado:** agenda propuesta, no resultados finales.

## Pregunta central

¿Qué propiedades, límites y costes de Seguridad de bases de datos pueden demostrarse formal o empíricamente, y qué incertidumbres permanecen ante cambios tecnológicos y modelos de amenaza?

## Estudios por tema

### 1. relacional, NoSQL y permisos

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de relacional, NoSQL y permisos están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

### 2. roles y separación de funciones

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de roles y separación de funciones están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

### 3. cifrado y secretos

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de cifrado y secretos están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

### 4. auditoría y consultas

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de auditoría y consultas están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

### 5. SQLi y exposición

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de SQLi y exposición están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

### 6. backup y recuperación

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de backup y recuperación están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

### 7. hardening y parches

- **Pregunta:** ¿Qué supuestos, garantías y modos de fallo de hardening y parches están demostrados, y cuáles se apoyan solo en afirmaciones o pruebas parciales?
- **Hipótesis provisional:** un enfoque de evaluación con propiedades explícitas, pruebas de conformidad y mediciones reproducibles detecta brechas que las comprobaciones superficiales no detectan.
- **Método:** revisión de normas y literatura; análisis formal/documental cuando corresponda; comparar implementaciones y baselines; crear vectores de prueba y casos de borde; medir interoperabilidad, rendimiento y fallos; repetir.
- **Métricas:** conformidad, cobertura, tasa de fallo, interoperabilidad, coste, rendimiento y reproducibilidad.
- **Entregable:** matriz de garantías y supuestos, protocolo, vectores/casos, resultados, limitaciones y artefactos reproducibles.

## Revisión de literatura

Priorizar estándares, especificaciones oficiales, RFC, documentos de organismos reconocidos y artículos revisados por pares. Registrar versión/edición, erratas, fecha y aplicabilidad. Diferenciar prueba formal, prueba de conformidad, benchmark y argumento de seguridad; no tratarlos como equivalentes.

## Protocolo de investigación

Definir pregunta, hipótesis falsable, variables, baseline, comparadores, entorno, versiones, métricas y criterio de refutación. Para investigación matemática/criptográfica, documentar modelo formal, supuestos y alcance de la prueba. Para sistemas de continuidad/recuperación, probar escenarios controlados con objetivos RTO/RPO definidos. Publicar scripts, datos permitidos, configuración, hashes y análisis.

## Seguridad y ética

No usar claves, certificados, datos ni sistemas de producción reales en experimentos. No degradar protecciones criptográficas en entornos reales. Para pruebas de continuidad, definir ventanas, aprobación y plan de reversión.

## Umbral

M4 requiere investigación y análisis; M5 revisión y reproducción independiente. Estado actual: `research_agenda_defined`.
