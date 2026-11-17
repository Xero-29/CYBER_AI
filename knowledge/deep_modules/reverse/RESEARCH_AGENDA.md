# Agenda de investigación: Ingeniería inversa

**Dominio:** `reverse` · **Objetivo:** L4 investigación · **Estado:** propuesta, no resultados concluidos.

## Pregunta central

¿Qué métodos, arquitecturas y controles para Ingeniería inversa ofrecen mejoras reproducibles y medibles frente a las prácticas de referencia, considerando coste, contexto, amenazas y limitaciones?

## Líneas de investigación

### 1. arquitecturas, ABI y calling conventions

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de arquitecturas, ABI y calling conventions no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 2. desensamblado y depuración

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de desensamblado y depuración no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 3. control flow y data flow

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de control flow y data flow no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 4. formatos binarios y linking

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de formatos binarios y linking no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 5. emulación y análisis aislado

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de emulación y análisis aislado no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 6. protecciones y empaquetado

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de protecciones y empaquetado no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
- **Hipótesis:** una taxonomía y controles derivados de evidencia mejoran la cobertura o reducen errores frente a baseline documentada.
- **Método:** revisión de literatura; análisis de estándares y documentación; construir taxonomía; seleccionar casos reproducibles; comparar baseline y propuesta; registrar datos y versiones; análisis crítico.
- **Métricas:** cobertura, precisión, reproducibilidad, tasa de fallo, coste operacional y robustez; operacionalizar antes del experimento.
- **Producto:** tabla comparativa, protocolo, resultados, análisis de incertidumbre, limitaciones y artefactos de reproducción.

### 7. reproducibilidad y divulgación

- **Pregunta:** ¿Qué fallos, supuestos y condiciones límite de reproducibilidad y divulgación no quedan cubiertos por las prácticas actuales y cómo pueden observarse?
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
