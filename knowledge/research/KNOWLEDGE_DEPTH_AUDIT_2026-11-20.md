# Auditoría de profundidad y reutilización de las 192 brechas — 2026-11-20

**Herramienta:** knowledge_depth_audit.py  
**Estado:** auditoría léxica/estructural; no es evaluación semántica ni científica.

## Resultado

| Métrica | Resultado |
|---|---:|
| Dominios | 48 |
| Temas/brechas | 192 |
| Tareas de validación | 192 |
| Bloques de sección | 1.344 |
| Variantes únicas entre secciones | 77 |
| Pares de duplicación exacta | 84.015 |
| Pares entre dominios | 82.208 |
| Claims respaldados | 0 |
| Experimentos no evaluados | 192 |
| Revisiones independientes no iniciadas | 192 |
| Fuentes pendientes de lectura integral | 192 |
| Brechas elegibles como expertas | 0 |

## Reutilización por sección

| Sección | Variantes únicas | Máxima reutilización |
|---|---:|---:|
| Propósito y alcance | 48 | 4 |
| Arquitectura y modelo de amenazas | 1 | 192 |
| Desarrollo técnico y controles | 7 | 55 |
| Procedimiento reproducible | 1 | 192 |
| Laboratorio y evaluación | 1 | 192 |
| Evidencia y limitaciones | 1 | 192 |
| Fuentes de partida | 18 | 120 |

## Interpretación

Las 192 brechas existen como borradores estructurados, pero gran parte de las secciones centrales reutiliza texto idéntico entre dominios. En particular, arquitectura, procedimiento, laboratorio y evidencia tienen una única variante para los 192 temas. Por tanto, el recuento 192/192 no significa 192 investigaciones específicas.

La auditoría compara texto normalizado y detecta duplicación exacta. No detecta todas las paráfrasis ni evalúa corrección técnica, actualidad, profundidad disciplinar o validez científica. El resultado debe complementarse con revisión semántica y trazabilidad claim-to-source.

## Puerta de promoción

Una brecha no puede promoverse por número de palabras, encabezados o estructura. Requiere contenido específico, fuentes leídas en el alcance declarado, claims trazables, experimentos cuando aplican, resultados reproducibles y revisión independiente. Actualmente el resultado es 0/192 elegibles.
