# Revisión de literatura — forensics

**Corte editorial:** 2026-11-19  
**Estado:** revisión exploratoria de fuentes registradas y alcance oficial; no revisión sistemática ni lectura integral de todas las fuentes.  
**Madurez:** M2 editorial como máximo; M3/M4/M5 pendientes.

**Corte:** 2026-11-19
**Madurez:** M2 editorial; no M3/M4/M5. No se ha ejecutado experimento ni se dispone de validación empírica.

## Pregunta

¿Qué procedimientos de adquisición, preservación y análisis producen evidencia digital íntegra, reproducible y correctamente limitada en su interpretación?

## Síntesis

NIST SP 800-86 integra técnicas forenses en respuesta a incidentes y aborda archivos, sistemas operativos, tráfico y aplicaciones. El documento advierte que no es una guía exhaustiva paso a paso ni asesoría legal; los requisitos de admisibilidad y privacidad dependen de la jurisdicción. NIST SP 800-61 Rev. 3 conecta respuesta con gestión de riesgo del CSF 2.0. NIST SP 800-92 trata la gestión de logs; el proyecto de revisión de log management debe distinguirse del documento final vigente. Un hash verifica igualdad de bytes entre mediciones, no demuestra por sí solo origen, autenticidad ni corrección de adquisición. La agenda propone datasets de entrenamiento y evidencia sintética; no autoriza adquisición de sistemas ajenos.

## Fuentes primarias y técnicas que orientan el módulo

NIST SP 800-86 (https://doi.org/10.6028/NIST.SP.800-86), NIST SP 800-61 Rev. 3 (https://doi.org/10.6028/NIST.SP.800-61r3), NIST SP 800-92 (https://doi.org/10.6028/NIST.SP.800-92).

## Identificadores del registro de fuentes

- `NIST-SP-800-86`
- `NIST-SP-800-61r3`
- `NIST-SP-800-92`
- `NIST-SP-800-92R1-IPD`

## Límites de esta revisión

- Los identificadores anteriores acreditan que existe una referencia en el registro; no demuestran lectura íntegra.
- No se afirma evaluación de conformidad, certificación ni validación de producto.
- Las afirmaciones normativas deben comprobarse contra edición, erratas, jurisdicción y fecha vigentes.
- Las taxonomías y guías organizan el análisis; no sustituyen evidencia observada.
- No se ha ejecutado el protocolo experimental ni se han obtenido resultados confirmatorios.

## Brechas

1. Recuperar texto completo de cada fuente primaria y registrar páginas/secciones efectivamente leídas.
2. Extraer requisitos y afirmaciones concretas con vínculo a subtema y criterio de prueba.
3. Incorporar estudios empíricos revisados por pares con criterios de inclusión/exclusión reproducibles.
4. Contrastar recomendaciones, contradicciones, supuestos y limitaciones entre fuentes.
5. Ejecutar protocolos con corpus autorizado, ground truth, controles negativos y resultados brutos.
6. Someter el análisis a revisión independiente y registrar correcciones.

**Conclusión limitada:** esta revisión constituye un mapa inicial de literatura y fuentes. No permite afirmar exhaustividad documental ni madurez científica superior a M2.
