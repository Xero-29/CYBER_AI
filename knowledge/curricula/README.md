# Currículos técnicos por especialidad

Define la profundidad objetivo y los artefactos de aprendizaje de las 48 áreas de `knowledge/packs/`.

- `domain_curriculum.json`: currículo de cada dominio con niveles L0–L4, temas técnicos específicos, artefactos, laboratorio y evaluación.
- `knowledge_quality.py`: auditoría local de integridad estructural y madurez editorial.

## Uso

```bash
python knowledge_quality.py
python knowledge_quality.py --json
python knowledge_quality.py --require-deep
```

L0 es orientación; L1 fundamentos y arquitectura; L2 metodología y controles; L3 análisis experto y validación; L4 investigación y evaluación crítica. Son objetivos editoriales, no certificaciones.

La existencia de un currículo no convierte automáticamente un pack en contenido profundo. La auditoría mide estructura, no exactitud semántica. Las fuentes externas solo cuentan como verificadas tras revisión real de procedencia, licencia, versión, integridad y contenido.

## Ampliación por dominio

1. Desarrollar cada tema con teoría, arquitectura, amenazas, controles y metodología.
2. Añadir laboratorios reproducibles, datos sintéticos y criterios de parada.
3. Incorporar casos anonimizados, ejercicios y rúbricas.
4. Verificar referencias primarias y registrar procedencia.
5. Ejecutar revisión técnica independiente y de vigencia.
6. Cambiar la madurez solo cuando exista evidencia.
