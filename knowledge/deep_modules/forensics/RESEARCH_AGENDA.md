# Agenda de investigación: Forense digital

**Dominio:** `forensics` · **Objetivo:** L4 investigación · **Estado:** propuesta, no resultados concluidos.

## Pregunta central

¿Qué métodos, arquitecturas y controles para Forense digital ofrecen mejoras reproducibles y medibles frente a las prácticas de referencia, considerando coste, contexto, amenazas y limitaciones?

## Líneas de investigación

### 1. cadena de custodia y evidencia

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de cadena de custodia y evidencia no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 2. adquisición forense y write blockers

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de adquisición forense y write blockers no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 3. filesystem, artefactos y timeline

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de filesystem, artefactos y timeline no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 4. memoria volátil y procesos

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de memoria volátil y procesos no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 5. logs, navegador y endpoints

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de logs, navegador y endpoints no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 6. PCAP, móviles y cloud

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de PCAP, móviles y cloud no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 7. reproducibilidad y reporte

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de reproducibilidad y reporte no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

## Revisión sistemática / mapeo de literatura

Registrar pregunta, bases consultadas, consultas exactas, rango temporal, idioma, fecha, criterios de inclusión/exclusión, proceso de deduplicación y motivos de descarte. Priorizar normas, papers revisados por pares, especificaciones, advisories y fuentes primarias. Evaluar calidad metodológica y conflicto de interés; no contar referencias sin lectura.

## Diseño de investigación

- Formular hipótesis nula y alternativa falsables.
- Definir población, unidad de análisis, variables, confusores y muestreo.
- Definir comparadores, baseline, métricas y análisis estadístico previo.
- Registrar entorno, versiones, hardware, dependencias y semillas.
- Realizar pruebas en laboratorio aislado y con autorización; documentar desviaciones.
- Evaluar validez interna, externa, de constructo y de conclusión.

## Artefactos de publicación

Estado del arte, taxonomía, threat model, protocolo, dataset/diccionario permitido, scripts, configuración, dependencias fijadas, SBOM, hashes, resultados brutos saneados, análisis, limitaciones, instrucciones de reproducción y revisión independiente.

## Ética y seguridad

No ampliar alcance ni realizar pruebas sobre terceros sin autorización. Minimizar datos y riesgo; en forense preservar cadena de custodia; en malware usar sandbox; en sistemas críticos simular; aplicar divulgación coordinada y proteger secretos.

## Umbral de madurez

M4 exige estudio de literatura, experimento ejecutado y análisis crítico. M5 exige revisión y reproducción independiente. Esta agenda solo define el plan inicial: `research_agenda_defined`.
