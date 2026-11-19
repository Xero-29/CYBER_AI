# Agenda de investigación: Ingeniería inversa

**Dominio:** reverse · **Corte:** 2026-11-19 · **Madurez:** M2 editorial; no M3/M4/M5 · **Estado:** `research_agenda_defined`, protocolo propuesto; no ejecutado.
**Objetivo de diseño:** L4; madurez efectiva M2 editorial hasta lectura de fuentes y resultados reproducibles.

## Pregunta central

¿Qué combinación de análisis estático, dinámico, emulación y fuzzing permite reconstruir el comportamiento de binarios con precisión y límites de inferencia medibles?

## Protocolos específicos

### R1 — ABI y arquitectura
Unidad: funciones compiladas desde fuente conocida. Variar ISA, ABI, compilador, optimización y arquitectura. Baseline: símbolos y fuente disponibles para ground truth. Medir recuperación de argumentos, retornos, stack, registros y tipos. Casos: llamadas directas/indirectas, variádicas, excepciones e inlining.

### R2 — Desensamblado y decompilación
Unidad: binario de ground truth. Comparar herramientas y configuración fijada. Medir funciones detectadas, límites de bloques, CFG, pseudocódigo equivalente y falsos límites. Controlar símbolos, stripping, optimización y relocations.

### R3 — Control flow y data flow
Unidad: ruta de datos en programa propio. Variar aliasing, indirect calls, punteros, optimización y estado global. Medir rutas recuperadas, fuentes/sinks y falsos positivos de taint. Revisar manualmente muestra estratificada.

### R4 — Formatos y parsers
Unidad: parser propio y corpus válido/malformado. Variar endian, offsets, longitudes, truncamiento y campos duplicados. Fuzzing con sanitizers. Métricas: cobertura, crashes reproducibles, hangs, bugs confirmados y reducción de corpus.

### R5 — Emulación y anti-analysis didáctico
Unidad: programa benigno que cambia comportamiento según reloj, archivos o entorno. Comparar ejecución nativa y emulada. Medir diferencias observables y falsos supuestos del analista. No desarrollar técnicas para evadir detección real.

### R6 — Firmware y diffing
Unidad: dos builds de firmware propio. Variar versión, flags y configuración. Medir diferencias de funciones, strings, particiones, configuración y falsos cambios. Documentar qué no emula el laboratorio.

### R7 — Vulnerabilidades y divulgación
Unidad: fallo sintético en parser local. Confirmar causa, precondiciones, input mínimo, parche y regresión. Métricas: reproducibilidad, tiempo de diagnóstico, falsos positivos y regresión. No publicar PoC operativa contra sistemas de terceros.

## Hipótesis y controles

H1: una metodología que combina ground truth, análisis estático y pruebas dinámicas controladas reduce errores de reconstrucción frente a análisis de una sola herramienta. H0: no existe diferencia bajo la muestra definida. Comparar al menos dos herramientas cuando sea técnicamente razonable; registrar versiones, arquitectura y compilador.

## Protocolo común

1. Usar únicamente binarios, firmware y sistemas propios o autorizados.
2. Congelar fuente ground truth, compilador, flags, hash, herramientas y entorno.
3. Preparar corpus positivo, negativo, truncado y casos límite.
4. Fijar métrica primaria, exclusiones y tamaño de muestra antes de medir.
5. Ejecutar en VM aislada, sin red por defecto y con snapshot.
6. Conservar scripts, logs, crashes minimizados y resultados brutos.
7. Repetir desde entorno limpio y revisar hipótesis alternativas.

## Métricas y amenazas a validez

Medir exactitud de reconstrucción, cobertura CFG, precisión de clasificación, cobertura de fuzzing, bugs confirmados, reproducibilidad y coste. Reportar resultados por arquitectura, compilador, flags y herramienta. Amenazas: heurísticas del decompilador, símbolos, optimización, instrumentación, sesgo del corpus y diferencia entre emulación y hardware real.

## Reproducibilidad

Conservar scripts, datos, hashes, versiones, configuración, logs y pasos de ejecución para permitir repetición independiente.

## Entregables

Protocolo, ground truth, corpus con hash/licencia, scripts, versiones, resultados, errores, incertidumbre, limitaciones, parche y test de regresión.

## Madurez

M2: contenido y protocolo diseñados. M3 requiere lectura de fuentes; M4 requiere ejecución y reproducción interna; M5 requiere revisión independiente y reproducción por segundo operador. Estado actual: no ejecutado.
