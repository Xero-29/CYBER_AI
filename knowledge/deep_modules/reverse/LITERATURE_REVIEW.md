# Revisión de literatura — Ingeniería inversa

**Corte:** 2026-11-19  
**Estado:** mapa exploratorio de fuentes y alcance; no revisión sistemática ni lectura integral.  
**Madurez:** M2 editorial como máximo; M3/M4/M5 pendientes.

## Pregunta

¿Cómo caracterizar binarios y firmware de forma reproducible, reconstruir comportamiento y limitar inferencias no sustentadas?

## Síntesis

Ghidra es una plataforma de ingeniería inversa que integra desensamblado, decompilación, scripting y análisis de binarios. Sus resultados dependen de arquitectura, formato, símbolos, compilación y configuración. El pseudocódigo es una reconstrucción aproximada y no recupera de forma garantizada el fuente original. La investigación debe contrastar hipótesis con ground truth y ejecución controlada.

NIST SSDF SP 800-218 ofrece prácticas para reducir vulnerabilidades en el ciclo de desarrollo, útiles para contextualizar hallazgos y correcciones, pero no es un manual de reversing. CWE clasifica debilidades y CAPEC patrones de ataque; estas taxonomías ayudan a normalizar hallazgos, pero no prueban explotabilidad ni impacto. Para afirmar una vulnerabilidad se requiere reproducibilidad, precondiciones, causa raíz y análisis de impacto.

## Fuentes registradas

- Ghidra Software Reverse Engineering Framework: https://ghidra-sre.org/
- NIST SSDF SP 800-218: https://doi.org/10.6028/NIST.SP.800-218
- CWE: https://cwe.mitre.org/
- CAPEC: https://capec.mitre.org/

## Identificadores del registro de fuentes

- `RESEARCH-REVERSE`
- `NIST-SP-800-218`
- `MITRE-CWE-TOP25-2025`
- `MITRE-CAPEC`

## Brechas

Leer documentación y fuentes completas; añadir estudios revisados por pares; comparar herramientas y arquitecturas; crear corpus de ground truth; ejecutar fuzzing y análisis diferencial en binarios propios; registrar falsos positivos y resultados negativos; obtener revisión independiente.

**Conclusión limitada:** mapa bibliográfico inicial, no evidencia de cobertura exhaustiva ni de eficacia de herramientas. No se han ejecutado experimentos.


**Límite empírico:** No se ha ejecutado experimento ni se dispone de validación empírica. La revisión no permite elevar la madurez por encima de M2.
