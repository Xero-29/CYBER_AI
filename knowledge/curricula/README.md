# Currículos técnicos por especialidad

Define la profundidad objetivo y los artefactos de aprendizaje de las 48 áreas de `knowledge/packs/`.

- `domain_curriculum.json`: currículo de cada dominio con niveles L0–L4, temas técnicos específicos, artefactos, laboratorio y evaluación.
- `knowledge_quality.py`: auditoría local de integridad estructural y madurez editorial.
- `../deep_modules/README.md`: índice de los 48 módulos de profundización, con temas, competencias, procedimiento, laboratorio, evaluación y requisitos de procedencia.

## Uso

```bash
python knowledge_quality.py
python knowledge_quality.py --json
python knowledge_quality.py --require-deep
```

L0 es orientación; L1 fundamentos y arquitectura; L2 metodología y controles; L3 análisis experto y validación; L4 investigación y evaluación crítica. Son objetivos editoriales, no certificaciones.

La existencia de un currículo o módulo no convierte automáticamente un pack en contenido profundo. La auditoría mide estructura, no exactitud semántica. Las fuentes externas solo cuentan como verificadas tras revisión real de procedencia, licencia, versión, integridad y contenido.

## Estado de los módulos de profundización

Se han creado 48 módulos, uno por cada área del manifiesto. Su estado inicial es `draft_structured_not_expert_validated`: definen ruta de trabajo, competencias, procedimiento, laboratorio, evaluación y requisitos de fuentes. No se contabilizan como manuales expertos terminados.

## Ampliación editorial obligatoria

1. Desarrollar cada tema con teoría, arquitectura, amenazas, controles y metodología.
2. Añadir laboratorios reproducibles, datos sintéticos y criterios de parada.
3. Incorporar casos anonimizados, ejercicios y rúbricas.
4. Verificar referencias primarias y registrar procedencia.
5. Ejecutar revisión técnica independiente y de vigencia.
6. Cambiar la madurez solo cuando exista evidencia.


## Investigación nivel L4/L5

- Protocolo de investigación: `../research/RESEARCH_PROTOCOL.md`.
- Registro de fuentes: `../research/source_registry.json` (solo metadatos oficiales revisados; lectura integral pendiente).
- Agendas específicas de las 48 áreas: `../deep_modules/<area>/RESEARCH_AGENDA.md`.
- Auditoría estructural: `python knowledge_research_audit.py` y `python -m pytest tests/test_knowledge_research_audit.py`.
- Las agendas no son papers, revisiones sistemáticas ni experimentos ejecutados. M4/M5 solo se asignan tras evidencia empírica y reproducción independiente.
